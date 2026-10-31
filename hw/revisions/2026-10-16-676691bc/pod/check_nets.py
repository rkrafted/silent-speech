#!/usr/bin/env python3
"""Assert every connection that matters in the ss-pod v1 netlist (rev 0.3).

    kicad-cli sch export netlist -o hw/pod/pod.net hw/pod/pod.kicad_sch
    python3 hw/pod/check_nets.py hw/pod/pod.net

Each rule prints [ok] or [FAIL]; exit 1 if any rule fails. Pins are found by their datasheet
NAME where the symbol has names (ADS1298, MCP73831, LP5907), so a pin-number slip cannot pass.
Standard library only.
"""
import re
import sys


def parse(text):
    toks = re.findall(r'"(?:[^"\\]|\\.)*"|\(|\)|[^\s()]+', text)
    stack, cur = [], []
    for t in toks:
        if t == "(":
            stack.append(cur)
            cur = []
        elif t == ")":
            done, cur = cur, stack.pop()
            cur.append(done)
        else:
            cur.append(t[1:-1] if t.startswith('"') else t)
    return cur[0]


def kids(node, key):
    return [c for c in node if isinstance(c, list) and c and c[0] == key]


def kid(node, key):
    k = kids(node, key)
    return k[0] if k else None


def load(path):
    root = parse(open(path, encoding="utf-8").read())
    nets = {}
    for n in kids(kid(root, "nets"), "net"):
        nodes = set()
        for nd in kids(n, "node"):
            pf = kid(nd, "pinfunction")
            pin = kid(nd, "pin")[1]
            func = re.sub(r"_%s$" % re.escape(pin), "", pf[1]) if pf else ""   # KiCad 10: "NAME_pin"
            nodes.add((kid(nd, "ref")[1], pin, func))
        nets[kid(n, "name")[1].lstrip("/")] = nodes          # local labels are "/NAME"
    return nets


def load_values(path):
    root = parse(open(path, encoding="utf-8").read())
    return {(kid(c, "ref")[1], kid(c, "value")[1]) for c in kids(kid(root, "components"), "comp")}


def norm(f):
    """Pin name without KiCad overbar/subscript markup: ~{CS} -> CS, V_{DD} -> VDD."""
    return re.sub(r"[~_]?\{([^}]*)\}", r"\1", f).upper()


def main(path):
    nets = load(path)
    values = load_values(path)
    net_of = {(r, p): name for name, ns in nets.items() for r, p, _ in ns}
    by_func = {}
    for name, ns in nets.items():
        for r, p, f in ns:
            by_func.setdefault((r, norm(f)), []).append((p, name))
    fails = []

    def check(ok, msg):
        print(("[ok]   " if ok else "[FAIL] ") + msg)
        if not ok:
            fails.append(msg)

    def pins_on(net):
        return {(r, p) for r, p, _ in nets.get(net, set())}

    def func_net(ref, func):
        hits = by_func.get((ref, norm(func)), [])
        return {n for _, n in hits}

    def refs_on(net):
        return {r for r, _, _ in nets.get(net, set())}

    # --- analog inputs --------------------------------------------------------------
    inn = [func_net("U1", "IN%dN" % i) for i in range(1, 9)]
    check(all(s == {"REF"} for s in inn), "IN1N..IN8N all on REF (referential montage)")
    check(pins_on("REF") - {p for p in pins_on("REF") if p[0] == "U1"} == {("R9", "2"), ("C9", "1")},
          "REF = 8x INxN + R9 (2.2k) + C9 (1nF) only")
    check(pins_on("REF_ELEC") == {("P9", "1"), ("FB9", "1"), ("D4", net_pin("D4", "IO1"))},
          "REF_ELEC = pogo P9 + ESD D4 + bead FB9")
    check(pins_on("REF_F") == {("FB9", "2"), ("R9", "1")}, "REF_F = FB9 -> R9 only")
    for i in range(1, 9):
        p = pins_on("IN%dP" % i)
        e = pins_on("E%d" % i)
        u1 = {x for x in p if x[0] == "U1"}
        check(len(u1) == 1 and func_net("U1", "IN%dP" % i) == {"IN%dP" % i}
              and p - u1 == {("R%d" % i, "2"), ("C%d" % i, "1")}
              and ("FB%d" % i, "1") in e and ("P%d" % i, "1") in e and len({x for x in e if x[0] in ("D2", "D3")}) == 1
              and len(e) == 3 and pins_on("E%d_F" % i) == {("FB%d" % i, "2"), ("R%d" % i, "1")},
              "E%d: pogo %d + ESD -> FB%d bead -> R%d 2.2k -> IN%dP, C%d 1nF to GND" % (i, i, i, i, i, i))
    for i in range(1, 11):
        check(net_of.get(("C%d" % i, "2")) == "GND", "C%d (input EMI cap) to GND" % i)

    # --- bias / RLD -----------------------------------------------------------------
    u1_rldout = {p for p in pins_on("RLDOUT") if p[0] == "U1"}
    check(func_net("U1", "RLDOUT") == {"RLDOUT"} and len(u1_rldout) == 1
          and pins_on("RLDOUT") - u1_rldout == {("R10", "1"), ("C11", "1"), ("R25", "1")},
          "RLDOUT = feedback R10/C11 + series R25 only (no capacitive load on the amp output)")
    check(pins_on("BIAS_F") == {("R25", "2"), ("C10", "1"), ("FB10", "2")}, "BIAS_F = R25 10k -> C10 1nF + bead FB10")
    check(pins_on("BIAS") == {("P10", "1"), ("FB10", "1"), ("D4", net_pin("D4", "IO2"))},
          "BIAS = pogo P10 + ESD D4 + bead FB10 (RLD reaches the body only through 10k)")
    check(func_net("U1", "RLDINV") == {"RLDINV"} and pins_on("RLDINV") - {p for p in pins_on("RLDINV") if p[0] == "U1"}
          == {("R10", "2"), ("C11", "2")}, "RLDINV = R10 392k || C11 10nF from RLDOUT only (TI SBAU171D 4.8)")
    check(len([1 for r, p, _ in nets.get("BIAS", set()) if r.startswith("P") and r[1:].isdigit()]) == 1, "exactly one bias electrode")

    # --- ADS1298 supplies and strap pins ---------------------------------------------
    for f in ("AVDD", "AVDD1"):
        check(func_net("U1", f) == {"+3.3VA"}, "%s on +3.3VA (LDO1)" % f)
    for f in ("AVSS", "AVSS1", "DGND", "RESV1", "DAISY_IN", "VREFN"):
        check(func_net("U1", f) == {"GND"}, "%s on GND" % f)
    for f in ("TESTP_PACE_OUT1", "TESTP_PACE_OUT2", "RLDIN"):
        check(func_net("U1", f) == {"+3.3VA"}, "%s on AVDD (TI pin table note 1: unused pins to AVDD)" % f)
    for f in ("GPIO1", "GPIO2", "GPIO3", "GPIO4"):
        check(func_net("U1", f) == {"GND"}, "%s shorted to DGND (TI: GPIOs are inputs, do not float)" % f)
    check(func_net("U1", "DVDD") == {"+3V3"}, "DVDD on +3V3 (LDO2)")
    check(func_net("U1", "CLKSEL") == {"+3V3"}, "CLKSEL high = internal oscillator")
    for f, net, caps in (("VREFP", "VREFP", {"C12", "C13"}), ("VCAP1", "VCAP1", {"C14"}), ("VCAP2", "VCAP2", {"C15"}),
                         ("VCAP3", "VCAP3", {"C16"}), ("VCAP4", "VCAP4", {"C17"}), ("WCT", "WCT", {"C33"}),
                         ("RLDREF", "RLDREF", {"C32"})):
        check(func_net("U1", f) == {net} and refs_on(net) - {"U1"} == caps
              and all(net_of.get((c, "2")) == "GND" for c in caps), "%s decoupled by %s to GND" % (f, "+".join(sorted(caps))))
    check(func_net("U3", "OUT") == {"+3.3VA"} and func_net("U4", "OUT") == {"+3V3"}, "LDO1 -> +3.3VA, LDO2 -> +3V3")
    check(not any(r == "U2" for r, _, _ in nets.get("+3.3VA", set())), "no radio pin on the analog supply")
    check({r for r, _, _ in nets.get("+3.3VA", set())} <= {"U1", "U3", "C18", "C19", "C26"},
          "+3.3VA feeds only the ADS1298 and its caps")

    # --- digital link ADS1298 <-> NINA-B306 -------------------------------------------
    # rev 0.4: every ADS line on a NINA pin that u-blox does not flag as near the radio; no series R
    link = {"START": ("START", "4"), "ADS_RESET": ("RESET", "5"), "ADS_PWDN": ("PWDN", "7"),
            "SCLK": ("SCLK", "2"), "MOSI": ("DIN", "8"), "MISO": ("DOUT", "1"), "CS_N": ("CS", "3"),
            "DRDY": ("DRDY", "25")}
    for net, (f, npin) in link.items():
        check(func_net("U1", f) == {net} and net_of.get(("U2", npin)) == net,
              "%s: ADS1298 %s <-> NINA pin %s" % (net, f, npin))
    for npin in ("32", "33", "34", "35", "36", "37", "38", "39"):      # old inner-ring pins now free
        check(not net_of.get(("U2", npin), "unconnected").split("-")[0] in link, "NINA pin %s no longer used" % npin)
    check(not any(r in {p[0] for n in nets.values() for p in n} for r in ("R26", "R27", "R28", "R29", "R30")),
          "no SPI series resistors (rev 0.4)")
    check(net_of.get(("R20", "1")) == "ADS_PWDN" and net_of.get(("R20", "2")) == "GND", "PWDN pulled low at boot")
    check(net_of.get(("R21", "1")) == "+3V3" and net_of.get(("R21", "2")) == "CS_N", "CS pulled high at boot")
    check(net_of.get(("R22", "1")) == "START" and net_of.get(("R22", "2")) == "GND", "START pulled low at boot")
    check(net_of.get(("R23", "1")) == "+3V3" and net_of.get(("R23", "2")) == "ADS_RESET", "RESET pulled high at boot")
    check(func_net("U1", "CLK") == {"CLK_SYNC"} and ("TP1", "1") in pins_on("CLK_SYNC"), "CLK on test pad TP1")

    # --- radio supply, programming, 5 V safety ----------------------------------------
    check(net_of.get(("U2", "10")) == "+3V3" and net_of.get(("U2", "9")) == "+3V3", "NINA VCC and VCC_IO on +3V3")
    check(all(net_of.get(("U2", p)) == "GND" for p in ("6", "12", "14", "26", "30", "53", "56", "57")),
          "NINA GND pins + EGP + EAGP on GND")
    check(pins_on("VBUS_MOD") == {("U2", "31"), ("R16", "2")} and net_of.get(("R16", "1")) == "VBUS",
          "NINA VBUS (5 V input) <- R16 2.2k <- VBUS")
    five_v = {"VBUS", "BAT_RAW", "+BATT"}
    check(not any(r == "U2" for n in five_v for r, _, _ in nets.get(n, set())),
          "no 3.3 V radio GPIO on a net that can exceed 3.6 V (VBUS, STAT, battery)")
    # Tag-Connect TC2030 ARM SWD pinout: 1 VCC, 2 SWDIO, 3 nRESET, 4 SWCLK, 5 GND, 6 SWO (open)
    check(net_of.get(("U2", "15")) == "SWDIO" and net_of.get(("J3", "2")) == "SWDIO", "SWDIO on J3.2")
    check(net_of.get(("U2", "11")) == "SWDCLK" and net_of.get(("J3", "4")) == "SWDCLK", "SWDCLK on J3.4")
    check(net_of.get(("U2", "19")) == "MOD_RESET" and net_of.get(("J3", "3")) == "MOD_RESET"
          and net_of.get(("R13", "1")) == "+3V3", "RESET_N on J3.3 with R13 pull-up")
    check(net_of.get(("J3", "1")) == "+3V3" and net_of.get(("J3", "5")) == "GND", "J3 VCC/GND")
    check(("J3", "6") not in net_of or net_of[("J3", "6")].startswith("unconnected"), "J3.6 SWO open")

    # --- power path -------------------------------------------------------------------
    check(pins_on("BAT_RAW") == {("J2", "1"), ("Q2", "3"), ("TP15", "1")}, "battery + (plug or sled) -> AO3401A drain only")
    check(("TP16", "1") in pins_on("GND"), "battery sled - contact on GND")
    check(net_of.get(("Q2", "2")) == "+BATT" and net_of.get(("Q2", "1")) == "GND" and net_of.get(("J2", "2")) == "GND",
          "AO3401A source -> +BATT, gate -> GND (reverse-polarity protection)")
    check(func_net("U5", "V_{DD}") == {"VBUS"} and func_net("U5", "V_{BAT}") == {"+BATT"}
          and func_net("U5", "V_{SS}") == {"GND"}, "MCP73831: VDD=VBUS, VBAT=+BATT, VSS=GND")
    check(func_net("U5", "PROG") == {"PROG"} and pins_on("PROG") - {("U5", "5")} == {("R11", "1")}
          and net_of.get(("R11", "2")) == "GND", "PROG = R11 10k to GND (100 mA)")
    check(not any(r == "U5" and f.upper() == "STAT" for ns in nets.values() if len(ns) > 1 for r, p, f in ns),
          "MCP73831 STAT left open (5 V-swinging output, no LED, no GPIO)")
    check(("C28", "1") in pins_on("VBUS") and ("C29", "1") in pins_on("+BATT"), "10 uF on VBUS and on VBAT")
    check(net_of.get(("D5", "1")) == "VBUS" and net_of.get(("D5", "2")) == "GND", "TVS cathode on VBUS, anode GND")
    check(("P11", "1") in pins_on("VBUS") and net_of.get(("P12", "1")) == "GND", "pogo 11 = VBUS, 12 = GND (adjacent: charger tab)")
    for u in ("U3", "U4"):
        check(func_net(u, "IN") == {"+BATT"} and func_net(u, "EN") == {"+BATT"} and func_net(u, "GND") == {"GND"},
              "%s: IN and EN on +BATT" % u)
    check(net_of.get(("R14", "1")) == "+BATT" and pins_on("BAT_SENSE") == {("R14", "2"), ("R15", "1"), ("C30", "1"),
                                                                           ("U2", "16")}
          and net_of.get(("R15", "2")) == "GND", "battery divider 1M/1M -> NINA pin 16 (P0.03/AIN1)")
    check(not any(r.startswith("LED") for ns in nets.values() for r, _, _ in ns), "no LEDs on the board (hidden wearable)")

    # --- flash + expansion -------------------------------------------------------------
    q = {"QSPI_CS": ("51", "1"), "QSPI_CLK": ("52", "6"), "QSPI_IO0": ("50", "5"), "QSPI_IO1": ("48", "2"),
         "QSPI_IO2": ("49", "3"), "QSPI_IO3": ("47", "7")}
    for net, (npin, fpin) in q.items():
        check(net_of.get(("U2", npin)) == net and net_of.get(("U6", fpin)) == net, "flash %s: NINA %s <-> W25Q128 %s" % (net, npin, fpin))
    check(net_of.get(("U6", "8")) == "+3V3" and net_of.get(("U6", "4")) == "GND" and net_of.get(("R24", "2")) == "QSPI_CS",
          "flash on +3V3, CS pulled up")
    for i, npin in enumerate(("17", "18", "20", "21", "22"), start=1):
        check(net_of.get(("U2", npin)) == "EXP%d" % i and ("TP%d" % (7 + i), "1") in pins_on("EXP%d" % i),
              "expansion pad EXP%d = NINA pin %s" % (i, npin))

    # --- protection on every electrode line ------------------------------------------
    for i in range(1, 11):
        check(("FB%d" % i, "BLM15HD182SN1D") in values, "FB%d is a GHz bead" % i)
    check(("R25", "10k") in values, "R25 BIAS series = 10k")
    esd_io = {n for n, ns in nets.items() for r, p, f in ns if r in ("D2", "D3", "D4") and f.startswith("IO")}
    check({"E%d" % i for i in range(1, 9)} | {"REF_ELEC", "BIAS"} <= esd_io, "ESD on all 10 electrode lines")
    check(all(func_net(d, "GND") == {"GND"} for d in ("D2", "D3", "D4")), "ESD arrays grounded")

    print("%d rules failed" % len(fails) if fails else "all rules passed")
    return 1 if fails else 0


def net_pin(ref, func):
    """TPD4E1B06 pin number for a function, read from gen_sch.py's single TPD_MAP table."""
    return _TPD.get(func, "?")


_TPD = {}
if __name__ == "__main__":
    import os
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_sch.py")).read()
    _TPD.update(eval(re.search(r"TPD_MAP = (\{.*?\})", src).group(1)))
    sys.exit(main(sys.argv[1]))
