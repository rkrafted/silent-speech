#!/usr/bin/env python3
"""Make the JLCPCB order files for one board: Gerbers + drill (zip), BOM csv, CPL (placement) csv.

    python3 hw/pod/fab.py pod            # hw/pod/pod.kicad_pcb        -> hw/fab/pod/
    python3 hw/pod/fab.py tab_electrode  # hw/tab_electrode/...       -> hw/fab/tab_electrode/
    python3 hw/pod/fab.py tab_charger

Refuses to run if the design-rule check (with zones refilled) has any error, if anything is left
unrouted, or if the pod still carries the NINA placeholder footprint.
"""
import csv
import json
import os
import shutil
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.dirname(HERE)
BOARDS = {"pod": os.path.join(HERE, "pod.kicad_pcb"),
          "tab_electrode": os.path.join(HW, "tab_electrode", "tab_electrode.kicad_pcb"),
          "tab_charger": os.path.join(HW, "tab_charger", "tab_charger.kicad_pcb"),
          "cartridge": os.path.join(HW, "cartridge", "cartridge.kicad_pcb")}     # rev 0.6: order at 0.6 mm thick
# tabs have no schematic; their few parts are listed here (LCSC numbers: confirm at BOM upload)
TAB_BOM = {"tab_electrode": [("2x5 2.54mm SMD vertical pin header", "J1", "PinHeader_2x05_P2.54mm_Vertical_SMD", "")],
           "tab_charger": [("USB-C receptacle HRO TYPE-C-31-M-12", "J1", "USB_C_Receptacle_HRO_TYPE-C-31-M-12", "C165948"),
                           ("5.1k 0402", "R1,R2", "R_0402_1005Metric", "C25905")],
           "cartridge": [("JST SH 2-pin horizontal socket SM02B-SRSS-TB", "J1",
                          "JST_SH_SM02B-SRSS-TB_1x02-1MP_P1.00mm_Horizontal", "C160402"),
                         ("SMD pogo pin, about 5.5 mm working height, gold", "P1,P2", "Pogo_SMD_tall_pad2.0", "")]}
LAYERS = "F.Cu,In1.Cu,In2.Cu,In3.Cu,In4.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts"
NO_PART = ("TP", "H", "J3")          # pads / holes / Tag-Connect footprint: nothing to assemble


def run(*args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode not in (0, 5):    # kicad-cli drc returns 5 when violations exist
        sys.exit("failed: %s\n%s%s" % (" ".join(args), r.stdout, r.stderr))
    return r


def main(name):
    pcb = BOARDS[name]
    out = os.path.join(HW, "fab", name)
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(os.path.join(out, "gerber"))
    if name == "pod":
        import pcbnew
        b = pcbnew.LoadBoard(pcb)
        u2 = b.FindFootprintByReference("U2")
        if u2 is None or len(u2.Pads()) == 0:
            sys.exit("REFUSED: U2 is the NINA placeholder (no pads). Add lib/pod.pretty/u-blox_NINA-B306.kicad_mod.")
    rep = os.path.join(out, "drc.json")
    run("kicad-cli", "pcb", "drc", "--refill-zones", "--save-board", "--severity-error", "--format", "json",
        "-o", rep, pcb)
    d = json.load(open(rep))
    errs = [v for v in d["violations"] if v["severity"] == "error"]
    unconn = d.get("unconnected_items", [])
    if errs or unconn:
        for v in errs[:20]:
            print(" ", v["type"], " | ".join(i["description"][:60] for i in v["items"]))
        sys.exit("REFUSED: %d DRC errors, %d unrouted connections (%s)" % (len(errs), len(unconn), rep))
    g = os.path.join(out, "gerber")
    run("kicad-cli", "pcb", "export", "gerbers", "--layers", LAYERS if name == "pod" else LAYERS.replace(
        "In1.Cu,In2.Cu,In3.Cu,In4.Cu,", ""), "--subtract-soldermask", "-o", g + "/", pcb)
    run("kicad-cli", "pcb", "export", "drill", "--format", "excellon", "--excellon-separate-th",
        "--excellon-units", "mm", "--generate-map", "--map-format", "gerberx2", "-o", g + "/", pcb)
    with zipfile.ZipFile(os.path.join(out, name + "_gerbers.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(g)):
            z.write(os.path.join(g, f), f)
    # placement (CPL) in JLC's column names
    pos = os.path.join(out, "pos.csv")
    run("kicad-cli", "pcb", "export", "pos", "--format", "csv", "--units", "mm", "--side", "both",
        "--exclude-dnp", "-o", pos, pcb)
    rows = list(csv.DictReader(open(pos)))
    with open(os.path.join(out, name + "_cpl.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])
        for r in rows:
            if r["Ref"].startswith(NO_PART):
                continue
            w.writerow([r["Ref"], r["PosX"] + "mm", r["PosY"] + "mm",
                        "Top" if r["Side"].lower().startswith("top") else "Bottom", r["Rot"]])
    # BOM in JLC's column names
    with open(os.path.join(out, name + "_bom.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Comment", "Designator", "Footprint", "LCSC Part #"])
        if name == "pod":
            for r in csv.DictReader(open(os.path.join(HERE, "bom.csv"))):
                w.writerow([r["Value"] + " " + r["MPN"], r["Reference"], r["Footprint"].split(":")[-1],
                            "" if r["LCSC"] in ("TBD", "GLOBAL") else r["LCSC"]])
        else:
            for row in TAB_BOM[name]:
                w.writerow(row)
    print("ok: %s -> %s" % (name, out))


if __name__ == "__main__":
    for n in sys.argv[1:] or ["pod", "tab_electrode", "tab_charger", "cartridge"]:
        main(n)
