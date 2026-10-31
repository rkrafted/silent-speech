#!/usr/bin/env python3
"""Generate the bench electrode tab for the pod's 3 x 4 pogo grid (2-layer, 1.6 mm, ENIG):

  hw/tab_electrode/tab_electrode.kicad_pcb  10 contact pads (E1..E8, REF, BIAS) -> upright SMD 2x5 2.54 mm
                                            header J1 on the tab's top face, INSIDE the pod outline (rev 0.5:
                                            L-shaped tab, no overhang). Pin order comes from route_tab.py (the
                                            first order Freerouting routes on F.Cu alone), printed on the silk.
                                            Rev 0.7: P11 (CLK) and P12 (GND) contacts -> upright SMD 1x2 header
                                            J2 above the grid, so a 2-wire lead links two pods' tabs (shared ADS
                                            clock + ground). (A single 2x6 header did not route on one layer.)
                                            The charger tab is gone: the pod has no charging.

The tab sits above the pod on 3.0 mm M2 nylon spacers, same orientation, so every pad and hole uses
the pod's own coordinates (pod_geom.py). The pod-facing side (B.Cu) carries ONLY the contact pads:
any other copper there could be pressed through the solder mask by a pogo tip and short a pin.
"""
import os
import sys

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pod_geom as G  # noqa: E402

MM = pcbnew.FromMM
SYSLIB = "/usr/share/kicad/footprints"
PODLIB = os.path.join(HERE, "lib", "pod.pretty")
Y0, Y1 = G.BOARD[1], G.BOARD[3]
VIA_D, VIA_DRILL, TRACK = 0.45, 0.20, 0.15


def V(x, y):
    return pcbnew.VECTOR2I(MM(x), MM(y))


def lset(layer):
    s = pcbnew.LSET()
    s.AddLayer(layer)
    return s


class Tab:
    def __init__(self, path, x0, x1, poly=None):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path = path
        self.b = pcbnew.NewBoard(path)
        self.b.SetCopperLayerCount(2)
        ds = self.b.GetDesignSettings()
        ds.m_MinClearance = MM(0.15)
        ds.m_TrackMinWidth = MM(0.15)
        ds.m_HoleClearance = MM(0.25)
        ds.m_CopperEdgeClearance = MM(0.3)
        ds.m_MinThroughDrill = MM(0.2)
        ds.m_ViasMinSize = MM(0.45)
        nc = ds.m_NetSettings.GetDefaultNetclass()
        nc.SetTrackWidth(MM(TRACK))
        nc.SetClearance(MM(0.15))
        nc.SetViaDiameter(MM(VIA_D))
        nc.SetViaDrill(MM(VIA_DRILL))
        self.nets = {}
        self.poly = poly or [(x0, Y0), (x1, Y0), (x1, Y1), (x0, Y1)]
        for (ax, ay), (bx, by) in zip(self.poly, self.poly[1:] + self.poly[:1]):
            e = pcbnew.PCB_SHAPE(self.b)
            e.SetShape(pcbnew.SHAPE_T_SEGMENT)
            e.SetStart(V(ax, ay))
            e.SetEnd(V(bx, by))
            e.SetLayer(pcbnew.Edge_Cuts)
            e.SetWidth(MM(0.1))
            self.b.Add(e)
        self.box = (x0, Y0, x1, Y1)
        for i, (hx, hy) in enumerate(G.HOLES):
            self.fp(PODLIB, "M2_NPTH_clamp", "H%d" % (i + 1), hx, hy)

    def net(self, name):
        if name not in self.nets:
            n = pcbnew.NETINFO_ITEM(self.b, name)
            self.b.Add(n)
            self.nets[name] = n
        return self.nets[name]

    def fp(self, lib, name, ref, x, y, rot=0, bottom=False, nets=None, value=""):
        f = pcbnew.FootprintLoad(lib, name)
        f.SetReference(ref)
        f.SetValue(value or name)
        f.Reference().SetLayer(pcbnew.F_Fab)
        f.SetPosition(V(x, y))
        f.SetOrientationDegrees(rot)
        for p in f.Pads():
            if nets and p.GetNumber() in nets:
                p.SetNet(self.net(nets[p.GetNumber()]))
        self.b.Add(f)                      # must be on the board before Flip (KiCad 10 crashes otherwise)
        if bottom:
            f.Flip(V(x, y), pcbnew.FLIP_DIRECTION_LEFT_RIGHT)
        return f

    def track(self, pts, netname, width=TRACK, layer=pcbnew.F_Cu):
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            t = pcbnew.PCB_TRACK(self.b)
            t.SetStart(V(ax, ay))
            t.SetEnd(V(bx, by))
            t.SetWidth(MM(width))
            t.SetLayer(layer)
            t.SetNet(self.net(netname))
            self.b.Add(t)

    def via(self, x, y, netname):
        v = pcbnew.PCB_VIA(self.b)
        v.SetPosition(V(x, y))
        v.SetWidth(MM(VIA_D))
        v.SetDrill(MM(VIA_DRILL))
        v.SetNet(self.net(netname))
        self.b.Add(v)

    def bottom_keepout(self):
        """B.Cu: no tracks/pours anywhere (pads are allowed, they are the contacts)."""
        z = pcbnew.ZONE(self.b)
        z.SetLayerSet(lset(pcbnew.B_Cu))
        o = z.Outline()
        o.NewOutline()
        for px, py in self.poly:
            o.Append(MM(px), MM(py))
        z.SetIsRuleArea(True)
        z.SetDoNotAllowTracks(True)
        z.SetDoNotAllowZoneFills(True)
        z.SetDoNotAllowVias(False)
        z.SetDoNotAllowPads(False)
        z.SetDoNotAllowFootprints(False)
        z.SetZoneName("pod side: contacts only")
        self.b.Add(z)

    def gnd_pour_top(self):
        z = pcbnew.ZONE(self.b)
        z.SetLayerSet(lset(pcbnew.F_Cu))
        z.SetNet(self.net("GND"))
        x0, y0, x1, y1 = self.box
        o = z.Outline()
        o.NewOutline()
        for px, py in ((x0 + .5, y0 + .5), (x1 - .5, y0 + .5), (x1 - .5, y1 - .5), (x0 + .5, y1 - .5)):
            o.Append(MM(px), MM(py))
        z.SetMinThickness(MM(0.2))
        z.SetLocalClearance(MM(0.3))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
        self.b.Add(z)

    def save(self):
        pcbnew.ZONE_FILLER(self.b).Fill(self.b.Zones())
        pcbnew.SaveBoard(self.path, self.b)
        print("wrote", self.path)


def contact(tab, ref, netname):
    x, y = G.GRID[ref]
    tab.fp(PODLIB, "TabPad_D2.5mm", ref, x, y, bottom=True, nets={"1": netname})


# ------------------------------------------------------------------ electrode tab
ELEC = [("P%d" % i, "E%d" % i) for i in range(1, 9)] + [("P9", "REF"), ("P10", "BIAS"), ("P11", "CLK"), ("P12", "GND")]
LINK = os.environ.get("TAB_LINK", "CLK,GND").split(",")          # J2 pin 1, pin 2
# L-shaped tab, all inside the pod outline: the grid part (x 100-110.4) plus a foot over the pod's low parts
# (flash, charger, FET: all <= 1.25 mm, the tab rides 3.0 mm up), stopping 0.5 mm short of the JST socket
# (2.95 mm tall) and well clear of the module's antenna end.
FOOT_X1, FOOT_Y0 = 118.5, 116.0
t = Tab(os.path.join(HERE, "..", "tab_electrode", "tab_electrode.kicad_pcb"), 100.0, FOOT_X1,
        poly=[(100.0, Y0), (110.4, Y0), (110.4, FOOT_Y0), (FOOT_X1, FOOT_Y0), (FOOT_X1, Y1), (100.0, Y1)])
HX, HY = 114.0, 123.0                               # upright SMD 2x5 header, pin 1 top left
# header pin -> electrode net. route_tab.py tries orders until one routes on F.Cu alone and passes it in.
ORDER = os.environ.get("TAB_ORDER", "REF,E6,E3,E5,E4,E2,E1,E8,BIAS,E7").split(",")   # found by route_tab.py
nets = {str(i + 1): n for i, n in enumerate(ORDER)}
t.fp(os.path.join(SYSLIB, "Connector_PinHeader_2.54mm.pretty"), "PinHeader_2x05_P2.54mm_Vertical_SMD", "J1",
     HX, HY, nets=nets, value="2x5 2.54 SMD vertical")
# two-pod link header (rev 0.7) in the free corner above the grid: below the H1 screw head (r ~1.9 mm), left of
# the tab's inner edge (x 110.4), clear of the row-1 contact vias
LX, LY = 106.8, 108.0
t.fp(os.path.join(SYSLIB, "Connector_PinHeader_2.54mm.pretty"), "PinHeader_1x02_P2.54mm_Vertical_SMD_Pin1Left", "J2",
     LX, LY, nets={"1": LINK[0], "2": LINK[1]}, value="1x2 2.54 SMD vertical (link)")
for s_, (dx, dy) in ((LINK[0][0], (-3.4, -1.27)), (LINK[1][0], (3.0, 1.27))):
    lt = pcbnew.PCB_TEXT(t.b)
    lt.SetText(s_)
    lt.SetPosition(V(LX + dx, LY + dy))
    lt.SetLayer(pcbnew.F_SilkS)
    lt.SetTextSize(V(0.7, 0.7))
    lt.SetTextThickness(MM(0.12))
    t.b.Add(lt)
# via per contact, inside the pad, offset by column so every via sits on its own horizontal lane
OFF = (-0.9, 0.0, 0.9)
for ref, netname in ELEC:
    x, y = G.GRID[ref]
    contact(t, ref, netname)
    t.via(x, y + OFF[G.COLS.index(x)], netname)
# silkscreen pin legend in the free strip left of the header (top side)
LABEL = {"REF": "R", "BIAS": "B"}
for row in range(5):
    tx = pcbnew.PCB_TEXT(t.b)
    tx.SetText("%s %s" % (LABEL.get(ORDER[2 * row], ORDER[2 * row]), LABEL.get(ORDER[2 * row + 1], ORDER[2 * row + 1])))
    tx.SetPosition(V(101.0, 121.0 + 1.0 * row))
    tx.SetLayer(pcbnew.F_SilkS)
    tx.SetTextSize(V(0.7, 0.7))
    tx.SetTextThickness(MM(0.12))
    tx.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_LEFT)
    t.b.Add(tx)
t.bottom_keepout()
t.save()
