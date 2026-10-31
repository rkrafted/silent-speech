#!/usr/bin/env python3
"""Generate hw/pod/pod.kicad_sch for ss-pod v1 (rev 0.3: rev 0.2 + MobilECG-II comparison changes).

Every part uses the stock KiCad library symbol when one exists (pin numbers verified by the KiCad
librarians), so ERC checks real pin types. Custom symbols only for the u-blox NINA-B306 (pin table
UBX-17052099 R15 Table 8), the TPD4E1B06 ESD array and the 2x6 pogo connector.

Layout: one A1 sheet, six labelled blocks. Each pin gets a short wire to a net label or a power
symbol; parts that serve a pin sit next to that pin's block. Power nets use power symbols:
GND, +3V3 (LDO2: module + ADS DVDD), +3.3VA (LDO1: ADS AVDD only), +BATT (battery after the
reverse-polarity FET). Rev 0.7: no charging on the pod (cartridge charged in the dock).

    python3 hw/pod/gen_sch.py && kicad-cli sch erc ... && python3 hw/pod/check_nets.py ...
"""
import os
import re
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "pod.kicad_sch")
LIB = "/usr/share/kicad/symbols/%s.kicad_sym"
ROOT = "0f0d9c2a-1b2c-4d3e-8f90-1a2b3c4d5e6f"
G = 2.54
STUB = 2 * G

# ---------------------------------------------------------------- library access


def lib_block(lib, name):
    s = open(LIB % lib, encoding="utf-8").read()
    i = s.find('\n\t(symbol "%s"' % name)
    if i < 0:
        raise KeyError("%s:%s" % (lib, name))
    i += 1
    d = 0
    for j in range(i, len(s)):
        if s[j] == "(":
            d += 1
        elif s[j] == ")":
            d -= 1
            if d == 0:
                return s[i:j + 1]


def flat_block(lib, name):
    """Library symbol with `extends` resolved (graphics + pins copied from the parent)."""
    b = lib_block(lib, name)
    m = re.search(r'\(extends "([^"]+)"\)', b)
    if not m:
        return b
    parent = flat_block(lib, m.group(1))
    p = m.group(1)
    parent = parent.replace('(symbol "%s"' % p, '(symbol "%s"' % name, 1)
    parent = parent.replace('(symbol "%s_' % p, '(symbol "%s_' % name)
    for prop in ("Value", "Footprint", "Datasheet", "Description"):
        mc = re.search(r'\(property "%s" "([^"]*)"' % prop, b)
        if mc:
            parent = re.sub(r'(\(property "%s" ")[^"]*(")' % prop,
                            lambda mm: mm.group(1) + mc.group(1).replace("\\", "\\\\") + mm.group(2),
                            parent, count=1)
    return parent


PIN_RE = re.compile(r'\(pin (\w+) (\w+)\s*\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)\)\s*\(length ([-\d.]+)\)'
                    r'(.*?)\(name "([^"]*)".*?\(number "([^"]*)"', re.S)


def pins_of(block):
    return {m[9]: (float(m[3]), float(m[4]), int(float(m[5])), m[8], m[1]) for m in PIN_RE.finditer(block)}


# ---------------------------------------------------------------- custom symbols


def custom_symbol(name, left, right, top=(), bottom=(), width=30.48, ref="U"):
    """left/right/top/bottom: lists of (num, name, type) or None for a gap."""
    rows = max(len(left), len(right), 1)
    h = (rows + 1) * G
    hw = width / 2
    cols = max(len(top), len(bottom), 1)
    w = max(width, (cols + 1) * G)
    hw = w / 2
    lines = ['(symbol "%s"' % name, '(pin_names (offset 1.016))', '(exclude_from_sim no)',
             '(in_bom yes)', '(on_board yes)',
             '(property "Reference" "%s" (at 0 %.2f 0) (effects (font (size 1.27 1.27))))' % (ref, h / 2 + 2.54),
             '(property "Value" "%s" (at 0 %.2f 0) (effects (font (size 1.27 1.27))))' % (name.split(":")[-1], -h / 2 - 2.54),
             '(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))',
             '(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))',
             '(symbol "%s_0_1"' % name.split(":")[-1],
             '(rectangle (start %.2f %.2f) (end %.2f %.2f) (stroke (width 0.254) (type default)) (fill (type background)))'
             % (-hw, h / 2, hw, -h / 2), ')',
             '(symbol "%s_1_1"' % name.split(":")[-1]]

    def pin(num, nm, typ, x, y, ang):
        lines.append('(pin %s line (at %.2f %.2f %d) (length 2.54) (name "%s" (effects (font (size 1.016 1.016)))) '
                     '(number "%s" (effects (font (size 1.016 1.016)))))' % (typ, x, y, ang, nm, num))

    top_y = (rows - 1) * G / 2
    for i, p in enumerate(left):
        if p:
            pin(p[0], p[1], p[2], -hw - 2.54, top_y - i * G, 0)
    for i, p in enumerate(right):
        if p:
            pin(p[0], p[1], p[2], hw + 2.54, top_y - i * G, 180)
    lx = -(cols - 1) * G / 2
    for i, p in enumerate(top):
        if p:
            pin(p[0], p[1], p[2], lx + i * G, h / 2 + 2.54, 270)
    for i, p in enumerate(bottom):
        if p:
            pin(p[0], p[1], p[2], lx + i * G, -h / 2 - 2.54, 90)
    lines += [')', ')']
    return "\n".join(lines)


# NINA-B306-00B, UBX-17052099 R15 Table 8. EGP = exposed centre ground pads, EAGP = exposed
# antenna-area ground pads (NINA-B306 only); both MUST go to GND (the layout footprint carries them).
NINA_LEFT = [("10", "VCC", "power_in"), ("9", "VCC_IO", "power_in"), ("31", "VBUS(5V in)", "passive"), None,
             ("19", "RESET_N/P0.18", "input"), ("15", "SWDIO", "bidirectional"), ("11", "SWDCLK", "input"),
             None, ("13", "ANT(B301 only)", "passive"), ("54", "USB_DP", "bidirectional"),
             ("55", "USB_DM", "bidirectional"), ("28", "NFC1/P0.09", "bidirectional"),
             ("29", "NFC2/P0.10", "bidirectional"), ("8", "SWO/P1.00", "bidirectional")]
NINA_RIGHT = [("32", "GPIO_32/P0.11", "bidirectional"), ("33", "GPIO_33/P1.09", "bidirectional"),
              ("34", "GPIO_34/P1.08", "bidirectional"), ("35", "GPIO_35/P1.01", "bidirectional"),
              ("36", "GPIO_36/P1.02", "bidirectional"), ("37", "GPIO_37/P1.03", "bidirectional"),
              ("38", "GPIO_38/P1.10", "bidirectional"), ("39", "GPIO_39/P1.11", "bidirectional"),
              ("40", "GPIO_40/P1.15", "bidirectional"), ("16", "GPIO_16/P0.03/AIN1", "bidirectional"),
              None,
              ("17", "GPIO_17/P0.28", "bidirectional"), ("18", "GPIO_18/P0.02", "bidirectional"),
              ("20", "GPIO_20/P0.31", "bidirectional"), ("1", "GPIO_1/P0.13", "bidirectional"),
              ("2", "GPIO_2/P0.14", "bidirectional"), ("3", "GPIO_3/P0.15", "bidirectional"),
              ("4", "GPIO_4/P0.16", "bidirectional"), ("5", "GPIO_5/P0.24", "bidirectional"),
              ("7", "GPIO_7/P0.25", "bidirectional"), ("21", "GPIO_21/P1.12", "bidirectional"),
              ("22", "GPIO_22/P1.13", "bidirectional"), ("23", "GPIO_23/P0.29", "bidirectional"),
              ("24", "GPIO_24/P0.30", "bidirectional"), ("25", "GPIO_25/P0.04", "bidirectional"),
              ("27", "GPIO_27/P0.05", "bidirectional"), ("41", "GPIO_41/P1.14", "bidirectional"),
              ("42", "GPIO_42/P0.26", "bidirectional"), ("43", "GPIO_43/P0.06", "bidirectional"),
              ("44", "GPIO_44/P0.27", "bidirectional"), ("45", "GPIO_45/P0.07", "bidirectional"),
              ("46", "GPIO_46/P0.12", "bidirectional"), ("47", "GPIO_47/P0.23", "bidirectional"),
              ("48", "GPIO_48/P0.21", "bidirectional"), ("49", "GPIO_49/P0.22", "bidirectional"),
              ("50", "GPIO_50/P0.20", "bidirectional"), ("51", "GPIO_51/P0.17", "bidirectional"),
              ("52", "GPIO_52/P0.19", "bidirectional")]
NINA_BOTTOM = [("6", "GND", "power_in"), ("12", "GND", "power_in"), ("14", "GND", "power_in"),
               ("26", "GND", "power_in"), ("30", "GND", "power_in"), ("53", "GND", "power_in"),
               ("56", "EGP", "power_in"), ("57", "EAGP", "power_in")]

# TPD4E1B06 in DCK (SC70-6): TI SLVSBQ8E Table 4-1, DCK column (checked 2026-10-07).
TPD_MAP = {"IO1": "1", "IO2": "2", "GND": "3", "IO3": "4", "IO4": "5", "NC": "6"}

# MAX17048 1-cell fuel gauge, TDFN-8 2 x 2 (rev 0.7). Pin table checked 2026-10-17 against the datasheet copy
# (19-6171, "Pin/Bump Descriptions" p. 6) in research/jaw/lcsc-parts.md item 5: identical.
MAX_PINS = {"1": "CTG", "2": "CELL", "3": "VDD", "4": "GND", "5": "ALRT", "6": "QSTRT", "7": "SCL", "8": "SDA",
            "9": "EP"}
CUSTOM = {
    "pod:MAX17048": custom_symbol("pod:MAX17048",
                                  [("3", "VDD", "power_in"), ("2", "CELL", "input"), ("1", "CTG", "input"),
                                   ("6", "QSTRT", "input")],
                                  [("8", "SDA", "bidirectional"), ("7", "SCL", "input"),
                                   ("5", "ALRT", "open_collector")],
                                  bottom=[("4", "GND", "power_in"), ("9", "EP", "passive")], width=15.24),
    "pod:NINA-B306": custom_symbol("pod:NINA-B306", NINA_LEFT, NINA_RIGHT, bottom=NINA_BOTTOM, width=40.64),
    "pod:TPD4E1B06": custom_symbol("pod:TPD4E1B06",
                                   [(TPD_MAP["IO1"], "IO1", "passive"), (TPD_MAP["IO2"], "IO2", "passive"),
                                    (TPD_MAP["IO3"], "IO3", "passive"), (TPD_MAP["IO4"], "IO4", "passive")],
                                   [(TPD_MAP["NC"], "NC", "no_connect")],
                                   bottom=[(TPD_MAP["GND"], "GND", "passive")], width=12.7, ref="D"),
}

LIBSYMS = {
    "Analog_ADC:ADS1298xPAG": ("Analog_ADC", "ADS1298xPAG"),
    "Regulator_Linear:TPS7A20xxxDBV": ("Regulator_Linear", "TPS7A20xxxDBV"),
    "Battery_Management:MCP73831-2-OT": ("Battery_Management", "MCP73831-2-OT"),
    "Transistor_FET:AO3401A": ("Transistor_FET", "AO3401A"),
    "Device:D_Zener": ("Device", "D_Zener"),
    "Device:R": ("Device", "R"),
    "Device:C": ("Device", "C"),
    "Device:C_Polarized": ("Device", "C_Polarized"),
    "Device:FerriteBead": ("Device", "FerriteBead"),
    "Connector:TestPoint": ("Connector", "TestPoint"),
    "Memory_Flash:W25Q128JVP": ("Memory_Flash", "W25Q128JVP"),
    "Connector_Generic:Conn_01x02": ("Connector_Generic", "Conn_01x02"),
    "Connector_Generic:Conn_01x01": ("Connector_Generic", "Conn_01x01"),
    "Connector_Generic:Conn_01x06": ("Connector_Generic", "Conn_01x06"),
    "Mechanical:MountingHole": ("Mechanical", "MountingHole"),
    "power:GND": ("power", "GND"),
    "power:+3V3": ("power", "+3V3"),
    "power:+3.3VA": ("power", "+3.3VA"),
    "power:+BATT": ("power", "+BATT"),
    "power:PWR_FLAG": ("power", "PWR_FLAG"),
}
BLOCKS = {}
for lid, (lib, nm) in LIBSYMS.items():
    b = flat_block(lib, nm)
    BLOCKS[lid] = b.replace('(symbol "%s"' % nm, '(symbol "%s"' % lid, 1)
BLOCKS.update(CUSTOM)
PINS = {lid: pins_of(b) for lid, b in BLOCKS.items()}
POWER = {"GND": "power:GND", "+3V3": "power:+3V3", "+3.3VA": "power:+3.3VA",
         "+BATT": "power:+BATT"}

# ---------------------------------------------------------------- sheet builder
out = []
parts = []          # (ref, lib_id, value, footprint, lcsc, mpn)
_pwr = [0]


def snap(v):
    return round(round(v / 1.27) * 1.27, 2)


def u():
    return str(uuid.uuid4())


def eff(size=1.27, just=None, hide=False):
    s = "(effects (font (size %.2f %.2f))" % (size, size)
    if just:
        s += " (justify %s)" % just
    if hide:
        s += " (hide yes)"
    return s + ")"


def symbol_instance(ref, lid, value, x, y, rot=0, fp="", in_bom=True, mirror=None, val_at=None, hide_val=False,
                    on_board=None, dnp=False):
    """on_board defaults to in_bom (power symbols: neither); a pads-only part is on_board but not in_bom."""
    x, y = snap(x), snap(y)
    on_board = in_bom if on_board is None else on_board
    out.append('(symbol (lib_id "%s") (at %.2f %.2f %d)%s (unit 1) (exclude_from_sim no) (in_bom %s) '
               '(on_board %s) (dnp %s) (uuid "%s")'
               % (lid, x, y, rot, " (mirror %s)" % mirror if mirror else "", "yes" if in_bom else "no",
                  "yes" if on_board else "no", "yes" if dnp else "no", u()))
    hide_ref = ref.startswith("#")
    in_bom = in_bom and not hide_ref
    pys = [py for (_, py, _, _, _) in PINS[lid].values()] or [0]
    if lid in ("Device:R", "Device:C", "Device:C_Polarized", "Device:FerriteBead"):
        r_at, v_at = (x + 2.54, y - 1.27, 0, "left"), (x + 2.54, y + 1.27, 0, "left")
    else:
        r_at, v_at = (x, y - max(pys) - 3.81, 0, None), (x, y - min(pys) + 3.81, 0, None)
    if val_at:
        v_at = val_at
    out.append('(property "Reference" "%s" (at %.2f %.2f %d) %s)' % (ref, r_at[0], r_at[1], r_at[2], eff(just=r_at[3], hide=hide_ref)))
    out.append('(property "Value" "%s" (at %.2f %.2f %d) %s)' % (value, v_at[0], v_at[1], v_at[2], eff(just=v_at[3], hide=hide_val)))
    out.append('(property "Footprint" "%s" (at %.2f %.2f 0) %s)' % (fp, x, y, eff(hide=True)))
    out.append('(property "Datasheet" "" (at %.2f %.2f 0) %s)' % (x, y, eff(hide=True)))
    for num in PINS[lid]:
        out.append('(pin "%s" (uuid "%s"))' % (num, u()))
    out.append('(instances (project "pod" (path "/%s" (reference "%s") (unit 1))))' % (ROOT, ref))
    out.append(')')


def pin_xy(x, y, lid, num):
    x, y = snap(x), snap(y)
    px, py, ang, _, _ = PINS[lid][num]
    return x + px, y - py, ang


OUTWARD = {0: (-1, 0), 180: (1, 0), 90: (0, 1), 270: (0, -1)}


def wire(x1, y1, x2, y2):
    out.append('(wire (pts (xy %.2f %.2f) (xy %.2f %.2f)) (stroke (width 0) (type default)) (uuid "%s"))'
               % (x1, y1, x2, y2, u()))


def power_symbol(net, x, y, dx, dy):
    lid = POWER[net]
    _pwr[0] += 1
    if net == "GND":
        rot = {(0, 1): 0, (0, -1): 180, (1, 0): 90, (-1, 0): 270}[(dx, dy)]
    else:
        rot = {(0, -1): 0, (0, 1): 180, (-1, 0): 90, (1, 0): 270}[(dx, dy)]
    # net name just beyond the symbol, reading away from the pin, so neighbours do not collide
    if dx:
        val = (x + dx * 7.0, y, rot, "left" if dx > 0 else "right")   # field angle follows the symbol
    else:
        val = (x, y + dy * 4.5, 90, "right" if dy > 0 else "left")
    symbol_instance("#PWR%03d" % _pwr[0], lid, net, x, y, rot, in_bom=False, val_at=val,
                    hide_val=(net == "GND" and dx != 0))


def label(net, x, y, dx, dy):
    ang, just = {(1, 0): (0, "left bottom"), (-1, 0): (180, "right bottom"),
                 (0, -1): (90, "left bottom"), (0, 1): (270, "right bottom")}[(dx, dy)]
    out.append('(label "%s" (at %.2f %.2f %d) %s (uuid "%s"))' % (net, x, y, ang, eff(just=just), u()))


def tie(x, y, ang, net, stub=STUB):
    """Wire from a pin end outward, ending in a power symbol, a label, or a no-connect flag."""
    if net is None:
        out.append('(no_connect (at %.2f %.2f) (uuid "%s"))' % (x, y, u()))
        return
    dx, dy = OUTWARD[ang]
    ex, ey = x + dx * stub, y + dy * stub
    wire(x, y, ex, ey)
    if net in POWER:
        power_symbol(net, ex, ey, dx, dy)
    else:
        label(net, ex, ey, dx, dy)


def place(ref, lid, value, x, y, nets, fp="", lcsc="", mpn="", stub=STUB, hide_val=False, in_bom=True, dnp=False):
    """nets: {pin number: net or None}. Pins not listed are an error (no silent floating pins)."""
    symbol_instance(ref, lid, value, x, y, fp=fp, hide_val=hide_val, in_bom=in_bom, on_board=True, dnp=dnp)
    if not dnp:
        parts.append((ref, lid, value, fp, lcsc, mpn))
    missing = set(PINS[lid]) - set(nets)
    if missing:
        raise SystemExit("%s: pins without a net or None: %s" % (ref, sorted(missing, key=lambda s: int(s))))
    for num, net in nets.items():
        px, py, ang = pin_xy(x, y, lid, num)
        if PINS[lid][num][4] == "no_connect" and net is None:
            continue                    # KiCad no_connect pin type needs no flag
        tie(px, py, ang, net, stub)


def two_pin(ref, lid, value, x, y, top, bottom, fp, lcsc="", mpn="", hide_val=False):
    """Vertical R/C: pin 1 up to `top`, pin 2 down to `bottom`."""
    place(ref, lid, value, x, y, {"1": top, "2": bottom}, fp=fp, lcsc=lcsc, mpn=mpn, hide_val=hide_val)


def text(s, x, y, size=1.8, bold=False):
    out.append('(text "%s" (exclude_from_sim no) (at %.2f %.2f 0) (effects (font (size %.2f %.2f)%s) '
               '(justify left bottom)) (uuid "%s"))' % (s, x, y, size, size, " (bold yes)" if bold else "", u()))


def frame(title, x1, y1, x2, y2, note=""):
    out.append('(rectangle (start %.2f %.2f) (end %.2f %.2f) (stroke (width 0.2) (type dash)) (fill (type none)) '
               '(uuid "%s"))' % (x1, y1, x2, y2, u()))
    text(title, x1 + 2.54, y1 + 5.08, 2.5, True)
    if note:
        text(note, x1 + 2.54, y1 + 9.0, 1.4)


# footprints / LCSC numbers (bom.csv is written from these)
R0402 = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"
C0603 = "Capacitor_SMD:C_0603_1608Metric"
C0805 = "Capacitor_SMD:C_0805_2012Metric"
RES = {"100R": ("C25076", "0402WGF1000TCE"), "4.7k": ("C25900", "0402WGF4701TCE"), "0R": ("C17168", "0402WGF0000TCE"),
       "2.2k": ("C25879", "0402WGF2201TCE"), "392k": ("C27007", "0402WGF3923TCE"),
       "10k": ("C25744", "0402WGF1002TCE"), "100k": ("C25741", "0402WGF1003TCE"),
       "1M": ("C26083", "0402WGF1004TCE"), "33R": ("TBD", "RC0402FR-0733RL")}
CAP = {"1nF": (C0402, "C1523", "0402B102K500NT"), "10nF": (C0402, "C15195", "CL05B103KB5NNNC"),
       "100nF": (C0402, "C1525", "CL05B104KO5NNNC"), "1uF": (C0402, "C52923", "CL05A105KA5NQNC"),
       "10uF": (C0805, "C15850", "CL21A106KAYNNNE"), "22uF": (C0805, "C45783", "CL21A226MAQNNNE")}


def R(ref, val, x, y, top, bottom):
    two_pin(ref, "Device:R", val, x, y, top, bottom, R0402, *RES[val])


def FB(ref, x, y, top, bottom):
    # GHz-band 0402 bead against BLE-burst pickup on the strip (MobilECG-II / 12-lead holter pattern).
    # OPEN: confirm >= 1 kohm at 2.4 GHz on the Murata curve and get the LCSC number.
    two_pin(ref, "Device:FerriteBead", "BLM15HD182SN1D", x, y, top, bottom, "Inductor_SMD:L_0402_1005Metric",
            "C76888", "BLM15HD182SN1D", hide_val=True)     # value too long for the 15 mm column; see sheet note


def C(ref, val, x, y, top, bottom="GND"):
    fp, lcsc, mpn = CAP[val]
    two_pin(ref, "Device:C", val, x, y, top, bottom, fp, lcsc, mpn)


def CP(ref, val, x, y, top, bottom, fp, lcsc, mpn):
    """Polarized cap: pin 1 (+) up to `top`, pin 2 (-) down to `bottom`."""
    two_pin(ref, "Device:C_Polarized", val, x, y, top, bottom, fp, lcsc, mpn)


# ================================================================ 1. electrodes
frame("1. Electrode pogo pins + input protection", 15, 15, 215, 200,
      "Pogo pins P1-P12 (top side, gold) -> ESD array (electrode side) -> ferrite bead -> 2.2k series -> 1nF to GND -> ADS1298. RC: OpenBCI Cyton; bead: MobilECG-II.")
# 12 individual SMD spring pins (Harwin P70-1000045R, LCSC C17702549: 0.4 um Au plunger, 10k cycles, 2 A,
# 3.5 mm free / 2.9 mm working height, pad 2.2 mm). Placed on the TOP side with every other part, in a
# 2 x 6 grid at 3.0 mm pitch at one board end; the strip tab / charger tab presses ENIG pads onto them.
# Rev 0.7: P11 = CLK_POGO (ADS clock, for linking two pods; was VBUS) and P12 = GND (the link's shared ground).
# A strip without a link has no pads at P11/P12, so neither touches skin.
POGO = ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "REF_ELEC", "BIAS", "CLK_POGO", "GND"]
for i, net in enumerate(POGO):
    place("P%d" % (i + 1), "Connector_Generic:Conn_01x01", "pogo %s" % net, 45, 40 + i * 5.08, {"1": net},
          fp="pod:Harwin_P70-1000045R_pad2.2", lcsc="C17702549", mpn="P70-1000045R")
for i, (ref, a, b_, c, d) in enumerate([("D2", "E1", "E2", "E3", "E4"), ("D3", "E5", "E6", "E7", "E8"),
                                        ("D4", "REF_ELEC", "BIAS", "CLK_POGO", None)]):
    place(ref, "pod:TPD4E1B06", "TPD4E1B06DCKR", 40, 115 + i * 26,
          {TPD_MAP["IO1"]: a, TPD_MAP["IO2"]: b_, TPD_MAP["IO3"]: c, TPD_MAP["IO4"]: d,
           TPD_MAP["GND"]: "GND", TPD_MAP["NC"]: None},
          fp="Package_TO_SOT_SMD:SOT-363_SC-70-6", lcsc="C840093", mpn="TPD4E1B06DCKR")
for i in range(8):
    x = 85 + i * 15
    FB("FB%d" % (i + 1), x, 40, "E%d" % (i + 1), "E%d_F" % (i + 1))
    R("R%d" % (i + 1), "2.2k", x, 70, "E%d_F" % (i + 1), "IN%dP" % (i + 1))
    C("C%d" % (i + 1), "1nF", x, 100, "IN%dP" % (i + 1))
FB("FB9", 85, 140, "REF_ELEC", "REF_F")
R("R9", "2.2k", 85, 170, "REF_F", "REF")
C("C9", "1nF", 100, 170, "REF")
FB("FB10", 145, 140, "BIAS", "BIAS_F")
C("C10", "1nF", 130, 170, "BIAS_F")
# 10k isolates the RLD amp from C10 + strip capacitance (no cap directly on RLDOUT) and limits body current
R("R25", "10k", 160, 170, "RLDOUT", "BIAS_F")
text("REF electrode feeds all eight INxN (referential montage). BIAS pad <- bead <- 10k R25 <- RLDOUT (MobilECG-II: 10k).", 85, 192, 1.4)
text("FB1-FB10: Murata BLM15HD182SN1D (0402, GHz-band bead). P11 CLK_POGO <- 100R R31 <- ADS CLK; ESD on D4 IO3.", 85, 196, 1.4)
# two-pod clock link (rev 0.7): 100R limits the current into the pin when a lead is plugged or the far pod is off,
# and slows the 2 MHz edges on the lead; the ESD channel is the spare one in D4
R("R31", "100R", 175, 170, "CLK_SYNC", "CLK_POGO")

# ================================================================ 2/3. ADS1298
frame("2. ADS1298 analog front end + 3. bias drive (RLD)", 225, 15, 470, 300,
      "Unipolar: AVDD 3.3V from LDO1 only, DVDD 3.3V from LDO2. Caps per TI SBAS459K Figure 106, placed at the package.")
ads = {}
for num, (px, py, ang, nm, typ) in PINS["Analog_ADC:ADS1298xPAG"].items():
    n = nm.upper()
    m = re.match(r"IN(\d)([PN])", n)
    if m:
        ads[num] = "IN%sP" % m.group(1) if m.group(2) == "P" else "REF"
    elif n in ("AVDD", "AVDD1"):
        ads[num] = "+3.3VA"
    elif n in ("AVSS", "AVSS1", "DGND", "RESV1", "DAISY_IN"):
        ads[num] = "GND"                     # RESV1 / DAISY_IN: tie to logic low (TI pin table)
    elif n.startswith("TESTP_PACE") or n.startswith("TESTN_PACE") or n == "RLDIN":
        ads[num] = "+3.3VA"                  # TI pin table footnote 1: "Connect unused pins to AVDD"
    elif n == "DVDD":
        ads[num] = "+3V3"
    elif n == "CLKSEL":
        ads[num] = "CLKSEL"                  # rev 0.7: NINA GPIO, 100k pull-up = internal oscillator by default
    elif n.startswith("GPIO"):
        ads[num] = "GND"                     # TI: GPIOs are inputs after reset, "short these pins to DGND"
    elif n == "NC":
        ads[num] = None                      # TI: may be left open
    else:
        ads[num] = {"VREFP": "VREFP", "VREFN": "GND", "VCAP1": "VCAP1", "VCAP2": "VCAP2", "VCAP3": "VCAP3",
                    "VCAP4": "VCAP4", "WCT": "WCT", "RLDREF": "RLDREF", "RLDINV": "RLDINV", "RLDOUT": "RLDOUT",
                    "DIN": "MOSI", "DOUT": "MISO", "SCLK": "SCLK", "~{CS}": "CS_N", "CS": "CS_N",
                    "START": "START", "~{RESET}": "ADS_RESET", "RESET": "ADS_RESET", "~{PWDN}": "ADS_PWDN",
                    "PWDN": "ADS_PWDN", "~{DRDY}": "DRDY", "DRDY": "DRDY", "CLK": "CLK_SYNC"}[nm]
place("U1", "Analog_ADC:ADS1298xPAG", "ADS1298IPAG", 330, 130, ads,
      fp="Package_QFP:TQFP-64_10x10mm_P0.5mm", lcsc="GLOBAL", mpn="ADS1298IPAG")
# decoupling, reference, VCAPs (TI Figure 106)
for i, (ref, val, net) in enumerate([("C18", "100nF", "+3.3VA"), ("C19", "1uF", "+3.3VA"),
                                     ("C20", "100nF", "+3V3"), ("C21", "1uF", "+3V3"),
                                     ("C12", "100nF", "VREFP"), ("C13", "10uF", "VREFP"),
                                     ("C15", "1uF", "VCAP2"),
                                     ("C16", "1uF", "VCAP3"), ("C17", "1uF", "VCAP4"),
                                     ("C33", "1nF", "WCT"), ("C32", "100nF", "RLDREF")]):
    C(ref, val, 240 + i * 15, 245, net)
# Rev 0.8: VCAP1 22 uF is a Vishay polymer tantalum (T58MM226M6R3C0300, 1608-09, 0.9 mm) instead of X5R:
# the datasheet (SBAS459K p. 96) wants a tantalum or C0G part where the board sees vibration. Pad 1 = +.
# Placed in the next free slot of the capacitor row (the list above is one shorter).
CP("C14", "22uF 6.3V polymer Ta", 240 + 11 * 15, 245, "VCAP1", "GND", "Capacitor_Tantalum_SMD:CP_EIA-1608-10_AVX-L",
   "C215879", "T58MM226M6R3C0300")
# RLD feedback: TI SBAU171D section 4.8, R8 392k || C20 10nF between RLDOUT and RLDINV
R("R10", "392k", 420, 230, "RLDOUT", "RLDINV")
C("C11", "10nF", 435, 230, "RLDOUT", "RLDINV")
# defined states while the nRF52840 boots (its GPIOs are inputs until firmware runs)
R("R20", "100k", 240, 280, "ADS_PWDN", "GND")      # ADS stays powered down until firmware
R("R21", "100k", 255, 280, "+3V3", "CS_N")          # SPI deselected
R("R22", "100k", 270, 280, "START", "GND")          # no conversions
R("R23", "100k", 285, 280, "+3V3", "ADS_RESET")     # not held in reset
R("R33", "100k", 300, 280, "+3V3", "CLKSEL")        # rev 0.7: internal clock unless firmware pulls it low (slave pod)
R("R32", "1M", 315, 280, "CLK_SYNC", "GND")         # CLK never floats (input with no link, or tri-stated)
# No SPI series resistors (rev 0.3 had 33R, removed 2026-10-14): on the 24 x 30 board the ADS1298 sits
# directly under the module's outer pin column, so each SPI line is ~3 mm pad -> via -> pad. That is
# electrically short for nRF standard-drive edges, and there is no room for five more parts there.
text("Firmware: CONFIG3 RLDREF_INT=1, PD_RLD=1; gain x6 or lower for EMG; 1000 SPS (500 = weak-link fallback); SRB not used. Two pods: master CLK_EN=1, slave CLKSEL low.", 300, 295, 1.4)

# ================================================================ 4. radio
frame("4. Radio: u-blox NINA-B306-00B (nRF52840, internal antenna, 32.768 kHz crystal inside)", 480, 15, 760, 300,
      "ADS link on the outer left pin column (pins 1-5, 7, 8) + pin 25: none near the radio (UBX-17052099). EXP1-5 ARE near the radio: < 10 kHz only.")
nina = {num: None for num in PINS["pod:NINA-B306"]}
nina.update({"51": "QSPI_CS", "52": "QSPI_CLK", "50": "QSPI_IO0", "48": "QSPI_IO1", "49": "QSPI_IO2",
             "47": "QSPI_IO3", "17": "EXP1", "18": "EXP2", "20": "EXP3", "21": "EXP4", "22": "EXP5",
             "10": "+3V3", "9": "+3V3", "31": "VBUS_MOD", "19": "MOD_RESET", "23": "CLKSEL", "15": "SWDIO", "11": "SWDCLK",
             "2": "SCLK", "8": "MOSI", "1": "MISO", "3": "CS_N", "25": "DRDY", "4": "START",
             "5": "ADS_RESET", "7": "ADS_PWDN", "16": "BAT_SENSE"})
for num in ("6", "12", "14", "26", "30", "53", "56", "57"):
    nina[num] = "GND"
place("U2", "pod:NINA-B306", "NINA-B306-00B", 620, 120, nina,
      fp="pod:u-blox_NINA-B306", lcsc="C6127317", mpn="NINA-B306-00B")
C("C22", "100nF", 500, 240, "+3V3")
C("C23", "1uF", 515, 240, "+3V3")
# Rev 0.7: no USB on the pod. Rev 0.8: VBUS tied to GND through R34 0R (fitted), as Nordic's no-USB reference
# configuration and DevZone threads 35658 / 48589 say (research/jaw/chip-forums.md Q5).
place("R34", "Device:R", "0R", 530, 240, {"1": "VBUS_MOD", "2": "GND"}, fp=R0402, lcsc="C17168",
      mpn="0402WGF0000TCE")
R("R13", "100k", 545, 240, "+3V3", "MOD_RESET")
for i, (ref, net, nm) in enumerate([("TP1", "CLK_SYNC", "CLK (2-chip sync)"), ("TP2", "START", "START")]):
    place(ref, "Connector:TestPoint", nm, 580 + i * 22, 270, {"1": net},
          fp="pod:TestPad_D0.8mm")
# SWD programming: Tag-Connect TC2030-NL footprint (pads + 3 holes, no part fitted). The TC2030-CTX-NL cable
# presses on, so firmware is flashed without soldering. Tag-Connect ARM SWD pinout: 1 VCC, 2 SWDIO, 3 nRESET,
# 4 SWCLK, 5 GND, 6 SWO (not used: SWO left open).
place("J3", "Connector_Generic:Conn_01x06", "SWD Tag-Connect TC2030-NL", 640, 270,
      {"1": "+3V3", "2": "SWDIO", "3": "MOD_RESET", "4": "SWDCLK", "5": "GND", "6": None},
      fp="Connector:Tag-Connect_TC2030-IDC-NL_2x03_P1.27mm_Vertical", mpn="no part (pads only)", in_bom=False)
# M2 NPTH holes either side of the pogo grid: the electrode tab and the charger tab screw down on 3.0 mm nylon
# spacers, which holds them at the pogo working height (2.9-3.0 mm). Nylon screws: no metal near the inputs.
for i, ref in enumerate(("H1", "H2")):
    place(ref, "Mechanical:MountingHole", "M2 NPTH", 680 + i * 20, 270, {}, fp="pod:M2_NPTH_clamp")

# ================================================================ 5. power
frame("5. Power: battery cartridge, reverse-polarity FET, two LDOs", 15, 310, 470, 530,
      "Rev 0.7: no charger on the pod. Cells are charged in the cartridge on the dock (hw/dock).")
place("J2", "Connector_Generic:Conn_01x02", "LiPo 1S protected", 30, 355, {"1": "BAT_RAW", "2": "GND"},
      fp="Connector_JST:JST_SH_SM02B-SRSS-TB_1x02-1MP_P1.00mm_Horizontal", lcsc="C160402", mpn="SM02B-SRSS-TB(LF)(SN)")
# Battery-cartridge contacts (rev 0.6): two 1.8 mm gold pads on the bottom face, in parallel with J2. The swappable
# battery cartridge (hw/cartridge: cell on a 0.6 mm board, two spring pins up to these pads) clips on without
# tools. Use ONE cell at a time (J2 or the cartridge), never both. The cartridge's + also goes through the AO3401A,
# so a reversed cell is blocked like a reversed plug.
place("TP15", "Connector:TestPoint", "BATT+ cartridge contact", 30, 440, {"1": "BAT_RAW"}, fp="pod:TabPad_D1.8mm")
place("TP16", "Connector:TestPoint", "BATT- cartridge contact", 55, 440, {"1": "GND"}, fp="pod:TabPad_D1.8mm")
# P-FET reverse protection: D to battery, S to load, G to GND. On when the cell is right way round
# (Vgs = -Vbat), conducts both ways so the charger can charge through it; off when reversed.
place("Q2", "Transistor_FET:AO3401A", "AO3401A", 75, 360, {"3": "BAT_RAW", "2": "+BATT", "1": "GND"},
      fp="Package_TO_SOT_SMD:SOT-23", lcsc="C15127", mpn="AO3401A")
C("C29", "10uF", 180, 395, "+BATT")                 # bulk on +BATT (cartridge contacts and spring pins)
place("U3", "Regulator_Linear:TPS7A20xxxDBV", "TPS7A2033PDBVR (LDO1, AVDD)", 300, 455,
      {"1": "+BATT", "3": "+BATT", "2": "GND", "5": "+3.3VA", "4": None},
      fp="Package_TO_SOT_SMD:SOT-23-5", lcsc="C2862740", mpn="TPS7A2033PDBVR")
C("C24", "1uF", 270, 490, "+BATT")
C("C26", "1uF", 330, 490, "+3.3VA")
place("U4", "Regulator_Linear:TPS7A20xxxDBV", "TPS7A2033PDBVR (LDO2, +3V3)", 400, 455,
      {"1": "+BATT", "3": "+BATT", "2": "GND", "5": "+3V3", "4": None},
      fp="Package_TO_SOT_SMD:SOT-23-5", lcsc="C2862740", mpn="TPS7A2033PDBVR")
C("C25", "1uF", 370, 490, "+BATT")
C("C27", "1uF", 430, 490, "+3V3")
# ERC: nets fed by a connector or a FET have no power_out pin; flag them as intentionally powered
for i, net in enumerate(["GND", "+BATT"]):   # rev 0.7: no charger, so +BATT has no power_out pin either
    place("#FLG%02d" % (i + 1), "power:PWR_FLAG", "PWR_FLAG", 40 + i * 20, 505, {"1": net})
    parts.pop()

# ================================================================ 6. monitor + status
frame("6. Battery monitor: MAX17048 fuel gauge + divider fallback (no LEDs: status in the phone app)", 480, 310, 760, 400,
      "MAX17048 on +BATT, I2C on EXP4 (SDA) / EXP5 (SCL), 4.7k pull-ups; bus also on the expansion pads. Divider 1M/1M = fallback.")
place("U7", "pod:MAX17048", "MAX17048G+T10", 640, 360,
      {"3": "+BATT", "2": "+BATT", "1": "GND", "6": "GND", "8": "EXP4", "7": "EXP5", "5": None, "4": "GND",
       "9": "GND"},
      fp="Package_DFN_QFN:TDFN-8-1EP_2x2mm_P0.5mm_EP0.8x1.2mm", lcsc="C2682616", mpn="MAX17048G+T10")
C("C35", "100nF", 590, 345, "+BATT")                # datasheet: bypass VDD with 0.1 uF
R("R35", "4.7k", 700, 345, "+3V3", "EXP4")
R("R36", "4.7k", 715, 345, "+3V3", "EXP5")
R("R14", "1M", 500, 345, "+BATT", "BAT_SENSE")
R("R15", "1M", 515, 345, "BAT_SENSE", "GND")
C("C30", "100nF", 530, 345, "BAT_SENSE")

# ================================================================ 7. flash + expansion
frame("7. 16 MB flash (record without a phone) + expansion pads (open hardware: add sensors later)", 480, 410, 760, 530,
      "W25Q128JV on the nRF52840 QSPI pins (u-blox recommended QSPI pins). EXP1-3: spare GPIOs (I2C/SPI/UART/PWM; analog). EXP4/EXP5 = I2C SDA/SCL (fuel gauge bus, add sensors on it).")
place("U6", "Memory_Flash:W25Q128JVP", "W25Q128JVPIQ (16 MB)", 540, 470,
      {"1": "QSPI_CS", "2": "QSPI_IO1", "3": "QSPI_IO2", "4": "GND", "5": "QSPI_IO0", "6": "QSPI_CLK",
       "7": "QSPI_IO3", "8": "+3V3", "9": "GND"},
      fp="Package_SON:WSON-8-1EP_6x5mm_P1.27mm_EP3.4x4.3mm", lcsc="C190862", mpn="W25Q128JVPIQ")
C("C34", "100nF", 505, 465, "+3V3")
R("R24", "100k", 590, 455, "+3V3", "QSPI_CS")      # flash deselected while the nRF boots
for i, (net, nm) in enumerate([("EXP1", "EXP1 P0.28/AIN4"), ("EXP2", "EXP2 P0.02/AIN0"), ("EXP3", "EXP3 P0.31/AIN7"),
                               ("EXP4", "EXP4 SDA P1.12"), ("EXP5", "EXP5 SCL P1.13"), ("+3V3", "EXP 3V3"), ("GND", "EXP GND")]):
    place("TP%d" % (8 + i), "Connector:TestPoint", nm, 615 + i * 20, 500, {"1": net},
          fp="pod:TestPad_D0.8mm")

# ================================================================ file
head = ['(kicad_sch (version 20250114) (generator "eeschema") (generator_version "9.0")',
        '(uuid "%s")' % ROOT, '(paper "A1")',
        '(title_block (title "ss-pod v1: ADS1298 + nRF52840 (NINA-B306) EMG pod") (rev "0.7") '
        '(company "ss-pod") (comment 1 "Rev 0.7: no charger, MAX17048, CLKSEL GPIO + CLK on P11; rev 0.6: cartridge pads TP15/TP16; rev 0.4: ADS link on NINA outer pins; rev 0.3: BIAS 10k, ferrites") '
        '(comment 2 "Analog front end: TI SBAS459K + ADS1298ECG-FE (SBAU171D) + OpenBCI Cyton (CC BY-SA 4.0)"))',
        '(lib_symbols']
used = sorted({p[1] for p in parts} | set(POWER.values()) | {"power:PWR_FLAG"})
for lid in used:
    head.append(BLOCKS[lid])
head.append(')')
tail = ['(sheet_instances (path "/" (page "1")))', '(embedded_fonts no)', ')']
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(head + out + tail) + "\n")

# BOM grouped by value + MPN
groups = {}
for ref, lid, val, fp, lcsc, mpn in parts:
    if ref.startswith(("TP", "H")) or ref == "J3":
        continue
    shown = "pogo pin" if val.startswith("pogo ") else val.split(" (")[0]
    groups.setdefault((shown, mpn, fp, lcsc), []).append(ref)
with open(os.path.join(HERE, "bom.csv"), "w", encoding="utf-8") as f:
    f.write("Reference,Qty,Value,Footprint,MPN,LCSC\n")
    for (val, mpn, fp, lcsc), refs in sorted(groups.items(), key=lambda kv: kv[1][0]):
        f.write('"%s",%d,"%s","%s","%s","%s"\n' % (",".join(refs), len(refs), val, fp, mpn, lcsc))
print("wrote %s: %d parts, %d BOM lines" % (OUT, len(parts), len(groups)))
