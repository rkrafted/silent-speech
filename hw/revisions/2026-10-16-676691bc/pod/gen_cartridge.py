#!/usr/bin/env python3
"""Generate hw/cartridge/cartridge.kicad_pcb: the swappable battery cartridge (rev 0.6, 2 layers, 0.6 mm).

The cartridge is the pod's bottom: a 20 x 20 x 4 mm pouch cell lies on it (cell area from pod_geom.CELL), the
cell's JST SH plug goes into J1 once, and two tall SMD pogo pins (P1 BATT+, P2 BATT-) press up onto the pod's
contact pads TP15/TP16 in the strip the cell leaves free. Swapping = unclip one cartridge, clip in a charged one:
no tools, no soldering. Same coordinates as the pod, seen from the pod's top; the cartridge's F.Cu faces the pod.

Heights (pod bottom face down): bottom parts <= 1.25 + foam 0.3 + cell 4.0 = 5.55 mm to the cartridge's top face,
so the pins need about 5.5 mm working height. J1 (2.95 mm) sits under LDO2 (1.1 mm): 1.5 mm to spare.
J1 pin 1 = + (same polarity as the pod's own J2), so any cell that fits the pod fits the cartridge.
"""
import os
import sys

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pod_geom as G  # noqa: E402

MM = pcbnew.FromMM
OUT = os.path.join(HERE, "..", "cartridge", "cartridge.kicad_pcb")
SYSLIB = "/usr/share/kicad/footprints"
PODLIB = os.path.join(HERE, "lib", "pod.pretty")
X0, X1, Y0, Y1 = 100.0, 124.0, 104.4, 130.0
CH = 2.0                                           # keying chamfer, bottom-left corner


def V(x, y):
    return pcbnew.VECTOR2I(MM(x), MM(y))


os.makedirs(os.path.dirname(OUT), exist_ok=True)
b = pcbnew.NewBoard(OUT)
b.SetCopperLayerCount(2)
ds = b.GetDesignSettings()
ds.SetBoardThickness(MM(0.6))
ds.m_MinClearance = MM(0.15)
ds.m_TrackMinWidth = MM(0.15)
ds.m_CopperEdgeClearance = MM(0.3)
nets = {}


def net(name):
    if name not in nets:
        n = pcbnew.NETINFO_ITEM(b, name)
        b.Add(n)
        nets[name] = n
    return nets[name]


poly = [(X0, Y0), (X1, Y0), (X1, Y1), (X0 + CH, Y1), (X0, Y1 - CH)]
for (ax, ay), (bx, by) in zip(poly, poly[1:] + poly[:1]):
    e = pcbnew.PCB_SHAPE(b)
    e.SetShape(pcbnew.SHAPE_T_SEGMENT)
    e.SetStart(V(ax, ay))
    e.SetEnd(V(bx, by))
    e.SetLayer(pcbnew.Edge_Cuts)
    e.SetWidth(MM(0.1))
    b.Add(e)


def fp(lib, name, ref, x, y, rot=0, pads=None, value=""):
    f = pcbnew.FootprintLoad(lib, name)
    f.SetReference(ref)
    f.SetValue(value or name)
    f.SetPosition(V(x, y))
    f.SetOrientationDegrees(rot)
    for p in f.Pads():
        if pads and p.GetNumber() in pads:
            p.SetNet(net(pads[p.GetNumber()]))
    b.Add(f)
    return f


def track(pts, netname, w=0.3):
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        t = pcbnew.PCB_TRACK(b)
        t.SetStart(V(ax, ay))
        t.SetEnd(V(bx, by))
        t.SetWidth(MM(w))
        t.SetLayer(pcbnew.F_Cu)
        t.SetNet(net(netname))
        b.Add(t)


(ax, ay), (bx, by) = G.CART_PADS["BATT+"], G.CART_PADS["BATT-"]
fp(PODLIB, "Pogo_SMD_tall_pad2.0", "P1", ax, ay, pads={"1": "BATT+"}, value="pogo 5.5mm BATT+")
fp(PODLIB, "Pogo_SMD_tall_pad2.0", "P2", bx, by, pads={"1": "BATT-"}, value="pogo 5.5mm BATT-")
# JST SH socket, mouth toward -x: the cell's plug sits in the strip beside the pins, its leads run to the cell edge
JX, JY = 120.6, 127.2
j = fp(os.path.join(SYSLIB, "Connector_JST.pretty"), "JST_SH_SM02B-SRSS-TB_1x02-1MP_P1.00mm_Horizontal", "J1",
       JX, JY, rot=270, pads={"1": "BATT+", "2": "BATT-"}, value="cell plug (JST SH, pin 1 = +)")
pad = {}
for p in j.Pads():
    q = p.GetPosition()
    pad.setdefault(p.GetNumber(), (pcbnew.ToMM(q.x), pcbnew.ToMM(q.y)))
p1, p2 = pad["1"], pad["2"]
track([p1, (ax + 1.6, p1[1]), (ax + 0.9, ay), (ax, ay)], "BATT+")
track([p2, (bx + 1.6, p2[1]), (bx + 0.9, by), (bx, by)], "BATT-")
# labels on the outer face (B.Silkscreen, mirrored) and the cell outline on the pod face (F.Fab)
for text, x, y, layer, mirror in (("ss-pod battery cartridge", 112.0, 112.0, pcbnew.B_SilkS, True),
                                  ("cell 20x20x4, plug into J1 (pin 1 = +)", 112.0, 114.0, pcbnew.B_SilkS, True),
                                  ("+", ax - 1.7, ay, pcbnew.F_SilkS, False), ("-", bx - 1.7, by, pcbnew.F_SilkS, False)):
    t = pcbnew.PCB_TEXT(b)
    t.SetText(text)
    t.SetPosition(V(x, y))
    t.SetLayer(layer)
    t.SetTextSize(V(0.8, 0.8))
    t.SetTextThickness(MM(0.15))
    t.SetMirrored(mirror)
    b.Add(t)
cx0, cy0, cx1, cy1 = G.CELL
r = pcbnew.PCB_SHAPE(b)
r.SetShape(pcbnew.SHAPE_T_RECT)
r.SetStart(V(cx0, cy0))
r.SetEnd(V(cx1, cy1))
r.SetLayer(pcbnew.F_Fab)
r.SetWidth(MM(0.1))
b.Add(r)
pcbnew.SaveBoard(OUT, b)
print("wrote", OUT)
