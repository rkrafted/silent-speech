#!/usr/bin/env python3
"""Route the electrode tab (rev 0.5, L-shaped, upright SMD 2x5 header) on F.Cu only.

The pod-facing side (B.Cu) must carry only the contact pads, so every trace is on F.Cu and the routing
has to be planar. Which header pin carries which electrode is free (the silkscreen prints the order),
so this tries pin orders until Freerouting routes all 10 nets with no B.Cu track and a clean DRC:

    python3 hw/pod/route_tab.py            # writes hw/tab_electrode/tab_electrode.kicad_pcb
"""
import json
import os
import random
import subprocess
import sys

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
PCB = os.path.join(HERE, "..", "tab_electrode", "tab_electrode.kicad_pcb")
JAR = os.path.expanduser("~/tools/freerouting/freerouting.jar")
WORK = os.path.join(HERE, "..", "tab_electrode", "route")
os.makedirs(WORK, exist_ok=True)
DSN, SES, REP = (os.path.join(WORK, n) for n in ("tab.dsn", "tab.ses", "drc.json"))
NETS = ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "REF", "BIAS"]


def attempt(order):
    env = dict(os.environ, TAB_ORDER=",".join(order))
    subprocess.run([sys.executable, os.path.join(HERE, "gen_tabs.py")], env=env, check=True, capture_output=True)
    b = pcbnew.LoadBoard(PCB)
    if not pcbnew.ExportSpecctraDSN(b, DSN):
        sys.exit("DSN export failed")
    if os.path.exists(SES):
        os.remove(SES)
    subprocess.run(["java", "-jar", JAR, "-de", DSN, "-do", SES, "-mp", "40", "--gui.enabled=false"],
                   capture_output=True, text=True, timeout=600)
    if not os.path.exists(SES):
        return None
    b = pcbnew.LoadBoard(PCB)
    if not pcbnew.ImportSpecctraSES(b, SES):
        return None
    T = b.Tracks()                      # KiCad 10: index the list, its iterator is broken
    back = [T[i] for i in range(len(T)) if T[i].GetClass() == "PCB_TRACK" and T[i].GetLayer() == pcbnew.B_Cu]
    for t in back:                      # never allowed on the pod-facing side
        b.Remove(t)
    # Freerouting necks tracks down at pads; JLCPCB's 2-layer minimum is 0.127 mm (5 mil)
    T = b.Tracks()
    for i in range(len(T)):
        if T[i].GetClass() == "PCB_TRACK" and T[i].GetWidth() < pcbnew.FromMM(0.127):
            T[i].SetWidth(pcbnew.FromMM(0.127))
    b.GetDesignSettings().m_TrackMinWidth = pcbnew.FromMM(0.127)
    pcbnew.ZONE_FILLER(b).Fill(b.Zones())
    pcbnew.SaveBoard(PCB, b)
    subprocess.run(["kicad-cli", "pcb", "drc", "--refill-zones", "--save-board", "--format", "json", "-o", REP, PCB],
                   capture_output=True)
    d = json.load(open(REP))
    errs = [v for v in d["violations"] if v["severity"] == "error"]
    return {"unrouted": len(d.get("unconnected_items", [])), "errors": len(errs), "back_tracks": len(back),
            "types": sorted({v["type"] for v in errs})}


rng = random.Random(7)
orders = [["REF", "E4", "E2", "E5", "E8", "E1", "BIAS", "E7", "E3", "E6"],   # routed fully on the 2026-10-16 search
          NETS, ["E1", "E4", "E2", "E5", "E3", "E6", "E7", "E8", "REF", "BIAS"]]
while len(orders) < 40:
    o = NETS[:]
    rng.shuffle(o)
    orders.append(o)
best = None
for i, o in enumerate(orders):
    r = attempt(o)
    print(i, ",".join(o), r, flush=True)
    if r and r["unrouted"] == 0 and r["errors"] == 0:
        print("ROUTED with order", ",".join(o))
        break
    if r and (best is None or (r["unrouted"], r["errors"]) < (best[1]["unrouted"], best[1]["errors"])):
        best = (o, r)
else:
    sys.exit("no order routed cleanly; best: %s" % (best,))
