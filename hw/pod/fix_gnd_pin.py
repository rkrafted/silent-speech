#!/usr/bin/env python3
"""Connect one isolated GND pad to the nearest GND via with finish_route's clearance-correct A*.

    python3 hw/pod/fix_gnd_pin.py U1 51

Used in rev 0.5: after the re-route, ADS1298 pin 51 (GND between the two DVDD pins 50/52) kept only a
0.3 mm sliver of B.Cu pour that no via reached, so DRC listed it as unconnected.
"""
import math
import sys

import numpy as np
import pcbnew

import finish_route as FR

ref, num = sys.argv[1], sys.argv[2]
import json, os  # noqa: E401,E402
fin = os.path.join(os.path.dirname(FR.PCB), "route", "drc_finish.json")
if os.path.exists(fin) and not json.load(open(fin)).get("unconnected_items"):
    sys.exit(print("nothing unconnected after finish_route: %s.%s left alone" % (ref, num)))
b = pcbnew.LoadBoard(FR.PCB)
FR.ITEM_LAYERS = {}
pad = [p for p in b.FindFootprintByReference(ref).Pads() if p.GetNumber() == num][0]
if pad.GetNetname() != "GND":
    sys.exit("%s.%s is not on GND" % (ref, num))
w = FR.width_for("GND")
occ_t = FR.raster(b, "GND", FR.CLR + w / 2)
occ_v = FR.raster(b, "GND", max(FR.CLR + FR.VIA_R, FR.VIA_DRILL / 2 + 0.2))
trk = [occ_t[la] for la in FR.LAYERS]
via = np.zeros((FR.NX, FR.NY), dtype=bool)
for la in FR.ALL_CU:
    via |= occ_v[la]
px, py = FR.mm(pad.GetPosition().x), FR.mm(pad.GetPosition().y)
start = set()
for l, la in enumerate(FR.LAYERS):
    if pad.IsOnLayer(la):
        ci, cj = FR.cell(px, py)
        for i in range(ci - 3, ci + 4):
            for j in range(cj - 3, cj + 4):
                if not trk[l][i, j]:
                    start.add((l, i, j))
goals = set()
T = b.Tracks()
for k in range(len(T)):
    t = T[k]
    if t.GetClass() == "PCB_VIA" and t.GetNetname() == "GND":
        gi, gj = FR.cell(FR.mm(t.GetPosition().x), FR.mm(t.GetPosition().y))
        for l in range(len(FR.LAYERS)):
            goals.add((l, gi, gj))
path = FR.astar(start, goals, trk, via)
if not path:
    sys.exit("no path from %s.%s to a GND via" % (ref, num))
net = b.FindNet("GND")
pts = [(FR.LAYERS[l], *FR.pos(i, j)) for (l, i, j) in path]
pts = [(pts[0][0], px, py)] + pts


def seg(la, a, c):
    if math.hypot(a[0] - c[0], a[1] - c[1]) < 1e-6:
        return
    t = pcbnew.PCB_TRACK(b)
    t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(a[0]), pcbnew.FromMM(a[1])))
    t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(c[0]), pcbnew.FromMM(c[1])))
    t.SetWidth(pcbnew.FromMM(w))
    t.SetLayer(la)
    t.SetNet(net)
    b.Add(t)


run_la, run_start, prev, prev_dir = pts[0][0], pts[0][1:], pts[0][1:], None
for la, x, y in pts[1:]:
    if la != run_la:
        seg(run_la, run_start, prev)
        v = pcbnew.PCB_VIA(b)
        v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(prev[0]), pcbnew.FromMM(prev[1])))
        v.SetWidth(pcbnew.FromMM(2 * FR.VIA_R))
        v.SetDrill(pcbnew.FromMM(FR.VIA_DRILL))
        v.SetNet(net)
        b.Add(v)
        run_la, run_start, prev_dir = la, prev, None
        continue
    d = (round(x - prev[0], 4), round(y - prev[1], 4))
    n = math.hypot(*d) or 1
    d = (round(d[0] / n, 3), round(d[1] / n, 3))
    if prev_dir is not None and d != prev_dir:
        seg(run_la, run_start, prev)
        run_start = prev
    prev_dir, prev = d, (x, y)
seg(run_la, run_start, prev)
pcbnew.SaveBoard(FR.PCB, b)
print("routed %s.%s to GND: %d cells" % (ref, num, len(path)))
