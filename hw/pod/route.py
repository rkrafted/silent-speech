#!/usr/bin/env python3
"""Autoroute hw/pod/pod.kicad_pcb with Freerouting, then refill zones and run DRC.

    python3 hw/pod/gen_pcb.py && python3 hw/pod/route.py [max_passes]

Steps: KiCad exports a Specctra DSN (In1.Cu is a power plane, so Freerouting only connects GND to it
with vias), Freerouting routes it headless, KiCad imports the session file, refills zones, saves, and
DRC prints a summary. The routed board is pod.kicad_pcb itself; re-running gen_pcb.py discards routing.
"""
import collections
import json
import os
import subprocess
import sys

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
PCB = os.path.join(HERE, "pod.kicad_pcb")
JAR = os.path.expanduser("~/tools/freerouting/freerouting.jar")
WORK = os.path.join(HERE, "route")
os.makedirs(WORK, exist_ok=True)
DSN, SES = os.path.join(WORK, "pod.dsn"), os.path.join(WORK, "pod.ses")
passes = sys.argv[1] if len(sys.argv) > 1 else "100"

b = pcbnew.LoadBoard(PCB)
u2 = b.FindFootprintByReference("U2")
if u2 is None or len(u2.Pads()) == 0:
    sys.exit("REFUSED: U2 is the NINA placeholder (no pads).")
if not pcbnew.ExportSpecctraDSN(b, DSN):
    sys.exit("DSN export failed")
if os.path.exists(SES):
    os.remove(SES)
cmd = ["java", "-jar", JAR, "-de", DSN, "-do", SES, "-mp", passes, "--gui.enabled=false"]
print(" ".join(cmd))
r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
open(os.path.join(WORK, "freerouting.log"), "w").write(r.stdout + r.stderr)
if not os.path.exists(SES):
    sys.exit("Freerouting produced no session file; see route/freerouting.log")
b = pcbnew.LoadBoard(PCB)
if not pcbnew.ImportSpecctraSES(b, SES):
    sys.exit("SES import failed")
# Freerouting necks tracks down to 0.076 mm at some pads; JLCPCB's minimum is 0.09 mm
T = b.Tracks()
widened = 0
for i in range(len(T)):
    t = T[i]
    if t.GetClass() == "PCB_TRACK" and t.GetWidth() < pcbnew.FromMM(0.09):
        t.SetWidth(pcbnew.FromMM(0.09))
        widened += 1
print("widened %d necked-down tracks to 0.09 mm" % widened)
# Freerouting worked to 0.10 mm; the check uses the fab's real limits (JLCPCB 6-layer: 0.09 mm space,
# 0.2 mm via hole to copper), so widening a necked track by 7 um does not show up as a violation.
ds = b.GetDesignSettings()
ds.m_HoleClearance = pcbnew.FromMM(0.20)
ds.m_NetSettings.GetDefaultNetclass().SetClearance(pcbnew.FromMM(0.09))
pcbnew.SaveBoard(PCB, b)
rep = os.path.join(WORK, "drc.json")
subprocess.run(["kicad-cli", "pcb", "drc", "--refill-zones", "--save-board", "--schematic-parity",
                "--format", "json", "-o", rep, PCB], capture_output=True)
d = json.load(open(rep))
print("violations:", dict(collections.Counter((v["severity"], v["type"]) for v in d["violations"])))
print("unrouted:", len(d.get("unconnected_items", [])))
print("schematic parity issues:", len(d.get("schematic_parity", [])))
