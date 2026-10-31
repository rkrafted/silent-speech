#!/usr/bin/env python3
"""Generate the two mating tabs for the pod's 3 x 4 pogo grid (2-layer, 1.6 mm, ENIG):

  hw/tab_electrode/tab_electrode.kicad_pcb  10 contact pads (E1..E8, REF, BIAS) -> right-angle 1x10
                                            2.54 mm header for snap-electrode leads (pin 1 = E1 ...
                                            pin 9 = REF, pin 10 = BIAS). NO pads at P11/P12, so the
                                            charger pins can never reach the electrodes.
  hw/tab_charger/tab_charger.kicad_pcb      USB-C (5.1k CC pull-downs) -> pads at P11 (VBUS), P12 (GND)
                                            only.

Both tabs sit above the pod on 3.0 mm M2 nylon spacers, same orientation, so every pad and hole uses
the pod's own coordinates (pod_geom.py). The pod-facing side (B.Cu) carries ONLY the contact pads:
any other copper there could be pressed through the solder mask by a pogo tip and short a pin.
Through-hole pins (header, USB-C shell) sit in the overhang left of x = 100, off the pod.
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
    def __init__(self, path, x0, x1):
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
        e = pcbnew.PCB_SHAPE(self.b)
        e.SetShape(pcbnew.SHAPE_T_RECT)
        e.SetStart(V(x0, Y0))
        e.SetEnd(V(x1, Y1))
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
        x0, y0, x1, y1 = self.box
        o = z.Outline()
        o.NewOutline()
        for px, py in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
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
ELEC = [("P%d" % i, "E%d" % i) for i in range(1, 9)] + [("P9", "REF"), ("P10", "BIAS")]
t = Tab(os.path.join(HERE, "..", "tab_electrode", "tab_electrode.kicad_pcb"), 94.6, 110.4)
HX = 98.6                                          # header pad column (overhang, off the pod)
HY0 = (Y0 + Y1) / 2 - 4.5 * 2.54                   # pin 1
# rot 180 points the pins left (off the pod) and stacks pins 2..10 upward from pin 1, so pin 1 is the
# BOTTOM position. Position j (0 = top) carries ELEC[j]: pin 10 = E1 ... pin 2 = REF, pin 1 = BIAS.
nets = {str(10 - j): n for j, (_, n) in enumerate(ELEC)}
t.fp(os.path.join(SYSLIB, "Connector_PinHeader_2.54mm.pretty"), "PinHeader_1x10_P2.54mm_Horizontal", "J1",
     HX, HY0 + 2.54 * 9, rot=180, nets=nets, value="1x10 2.54 R/A")
# via per contact, inside the pad, offset by column so every via sits on its own horizontal lane
OFF = (-0.9, 0.0, 0.9)
lanes = []
for ref, netname in ELEC:
    x, y = G.GRID[ref]
    col = G.COLS.index(x)
    vy = y + OFF[col]
    contact(t, ref, netname)
    t.via(x, vy, netname)
    lanes.append((vy, x, netname))
lanes.sort()
pins = [HY0 + 2.54 * i for i in range(10)]
# river routing: header pin i -> lane i (both sorted). Traces going down turn later the higher they
# start; traces going up turn later the lower they start. No crossings on F.Cu.
up = [i for i in range(10) if pins[i] > lanes[i][0]]
down = [i for i in range(10) if pins[i] <= lanes[i][0]]
xs = {}
for k, i in enumerate(sorted(down, reverse=True)):        # lowest-starting down trace turns first
    xs[i] = 99.9 + 0.5 * k
for k, i in enumerate(sorted(up)):                        # highest-starting up trace turns first
    xs[i] = 99.85 + 0.45 * k
for i in range(10):
    vy, vx, netname = lanes[i]
    if netname != nets[str(10 - i)]:
        raise SystemExit("header order mismatch at pin %d" % (i + 1))
    x = min(xs[i], vx)
    t.track([(HX, pins[i]), (x, pins[i]), (x, vy), (vx, vy)], netname)
# silkscreen labels beside each header pin (top side), plus a title
LABEL = {"REF": "R", "BIAS": "B"}
for j, (_, netname) in enumerate(ELEC):
    tx = pcbnew.PCB_TEXT(t.b)
    tx.SetText(LABEL.get(netname, netname))
    tx.SetPosition(V(HX + 1.5, pins[j]))
    tx.SetLayer(pcbnew.F_SilkS)
    tx.SetTextSize(V(0.8, 0.8))
    tx.SetTextThickness(MM(0.15))
    tx.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_LEFT)
    t.b.Add(tx)
t.bottom_keepout()
t.save()

# ------------------------------------------------------------------ charger tab
c = Tab(os.path.join(HERE, "..", "tab_charger", "tab_charger.kicad_pcb"), 88.0, 110.4)
CX, CY = 91.7, (Y0 + Y1) / 2
usb = c.fp(os.path.join(SYSLIB, "Connector_USB.pretty"), "USB_C_Receptacle_HRO_TYPE-C-31-M-12", "J1", CX, CY,
           rot=270, value="TYPE-C-31-M-12",
           nets={"A1": "GND", "B12": "GND", "A12": "GND", "B1": "GND", "SH": "GND", "A4": "VBUS", "B9": "VBUS",
                 "A5": "CC1", "B5": "CC2", "A9": "VBUS_B", "B4": "VBUS_B"})  # VBUS on A4/B9 only: plenty for 100 mA, and no loop that
                                                # would cut the GND pour into an island
pad = {}
for p in usb.Pads():
    q = p.GetPosition()
    pad.setdefault(p.GetNumber(), (pcbnew.ToMM(q.x), pcbnew.ToMM(q.y)))
R0402 = os.path.join(SYSLIB, "Resistor_SMD.pretty")
c.fp(R0402, "R_0402_1005Metric", "R1", pad["A5"][0] + 2.2, pad["A5"][1], nets={"1": "CC1", "2": "GND"}, value="5.1k")
c.fp(R0402, "R_0402_1005Metric", "R2", pad["B5"][0] + 2.2, pad["B5"][1] - 0.5, nets={"1": "CC2", "2": "GND"},
     value="5.1k")
c.track([pad["A5"], (pad["A5"][0] + 1.72, pad["A5"][1])], "CC1")
b5 = pad["B5"]
c.track([b5, (b5[0] + 0.96, b5[1]), (b5[0] + 1.46, b5[1] - 0.5), (b5[0] + 1.72, b5[1] - 0.5)], "CC2")
contact(c, "P11", "VBUS")
contact(c, "P12", "GND")
vx, vy = G.GRID["P11"]
c.via(vx, vy - 0.9, "VBUS")
gx, gy = G.GRID["P12"]
c.via(gx, gy - 0.9, "GND")
# VBUS: receptacle A4/B9 -> 0.5 mm trace -> via in the P11 contact
a4 = pad["A4"]
bus_x = a4[0] + 3.4
c.track([a4, (bus_x, a4[1]), (bus_x, vy - 0.9), (vx, vy - 0.9)], "VBUS", width=0.5)
c.gnd_pour_top()
c.bottom_keepout()
c.save()
