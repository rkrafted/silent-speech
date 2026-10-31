#!/usr/bin/env python3
"""Generate and route hw/dock/dock.kicad_pcb: the cartridge charging dock (rev 0.7, 2 layers, 1.6 mm, ENIG).

Rev 0.7 moved all charging off the pod. A battery cartridge (hw/cartridge) comes off the pod and lies FACE DOWN on
the dock: its cell and its two tall spring pins point down, and the pins land on two 1.8 mm gold pads here, at the
same 5.55 mm height they meet on the pod. Because the cartridge is flipped, the dock's pads are the MIRROR image
(about the cartridge's centre line x = 112) of the pod's pads in pod_geom.CART_PADS, and so is the keying chamfer.
Magnets in the printed cradle hold the cartridge down, the same way the case holds it on the pod.

    USB-C (power only, 5.1k CC pull-downs) -> SMAJ5.0A TVS -> MCP73831-2 (4.20 V)
    -> R_PROG 15k = 1000 V / 15k = 67 mA (about 0.55 C for the 120 mAh 402020 cell) -> BATT+ pad
    STAT -> 1k -> LED (charging = lit). The dock is not worn, so it may light; fit or skip D2/R4 at order time.

Same coordinate frame as the pod (seen from above, dock top face = F.Cu). Cartridge zone x 100-124, y 104.4-130,
charger strip y 130-142 with the USB-C mouth at the bottom edge.

    python3 hw/pod/gen_dock.py           # writes, routes (Freerouting) and DRC-checks the dock
"""
import json
import os
import subprocess
import sys

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pod_geom as G  # noqa: E402

MM = pcbnew.FromMM
DIR = os.path.join(HERE, "..", "dock")
OUT = os.path.join(DIR, "dock.kicad_pcb")
WORK = os.path.join(DIR, "route")
JAR = os.path.expanduser("~/tools/freerouting/freerouting.jar")
SYSLIB = "/usr/share/kicad/footprints"
PODLIB = os.path.join(HERE, "lib", "pod.pretty")
X0, X1, Y0, Y1 = 100.0, 124.0, 104.4, 142.0
MIRROR_X = 112.0                                   # cartridge centre line (cartridge outline x 100-124)
CH = 2.0                                           # keying chamfer: bottom-left on the cartridge -> bottom-right here
CART_Y1 = 130.0


def V(x, y):
    return pcbnew.VECTOR2I(MM(x), MM(y))


def mirror(p):
    return (2 * MIRROR_X - p[0], p[1])


os.makedirs(WORK, exist_ok=True)
b = pcbnew.NewBoard(OUT)
b.SetCopperLayerCount(2)
ds = b.GetDesignSettings()
ds.m_MinClearance = MM(0.15)
ds.m_TrackMinWidth = MM(0.15)
ds.m_HoleClearance = MM(0.25)
ds.m_CopperEdgeClearance = MM(0.3)
ds.m_MinThroughDrill = MM(0.2)
ds.m_ViasMinSize = MM(0.45)
nc = ds.m_NetSettings.GetDefaultNetclass()
nc.SetTrackWidth(MM(0.3))                          # charge current is 67 mA; 0.3 mm everywhere is simple and safe
nc.SetClearance(MM(0.15))
nc.SetViaDiameter(MM(0.6))
nc.SetViaDrill(MM(0.3))
nets = {}


def net(name):
    if name not in nets:
        n = pcbnew.NETINFO_ITEM(b, name)
        b.Add(n)
        nets[name] = n
    return nets[name]


def edge(poly, layer=pcbnew.Edge_Cuts, w=0.1):
    for (ax, ay), (bx, by) in zip(poly, poly[1:] + poly[:1]):
        e = pcbnew.PCB_SHAPE(b)
        e.SetShape(pcbnew.SHAPE_T_SEGMENT)
        e.SetStart(V(ax, ay))
        e.SetEnd(V(bx, by))
        e.SetLayer(layer)
        e.SetWidth(MM(w))
        b.Add(e)


def fp(lib, name, ref, x, y, rot=0, pads=None, value=""):
    f = pcbnew.FootprintLoad(lib, name)
    if f is None:
        sys.exit("footprint not found: %s:%s" % (lib, name))
    f.SetReference(ref)
    f.SetValue(value or name)
    f.Reference().SetLayer(pcbnew.F_Fab)
    f.SetPosition(V(x, y))
    f.SetOrientationDegrees(rot)
    for p in f.Pads():
        if pads and p.GetNumber() in pads:
            p.SetNet(net(pads[p.GetNumber()]))
    b.Add(f)
    return f


def text(s, x, y, layer=pcbnew.F_SilkS, size=0.8):
    t = pcbnew.PCB_TEXT(b)
    t.SetText(s)
    t.SetPosition(V(x, y))
    t.SetLayer(layer)
    t.SetTextSize(V(size, size))
    t.SetTextThickness(MM(0.15))
    b.Add(t)


edge([(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)])
# where the cartridge lies (mirrored chamfer), for the cradle designer and the assembly drawing
edge([(X0, Y0), (X1, Y0), (X1, CART_Y1 - CH), (X1 - CH, CART_Y1), (X0, CART_Y1)], layer=pcbnew.F_Fab)

R0402, C0805 = os.path.join(SYSLIB, "Resistor_SMD.pretty"), os.path.join(SYSLIB, "Capacitor_SMD.pretty")
# --- contacts: the cartridge's spring pins land here (mirror of the pod's TP15 / TP16)
bp, bm = mirror(G.CART_PADS["BATT+"]), mirror(G.CART_PADS["BATT-"])
fp(PODLIB, "TabPad_D1.8mm", "TP1", *bp, pads={"1": "VBAT"}, value="BATT+ contact")
fp(PODLIB, "TabPad_D1.8mm", "TP2", *bm, pads={"1": "GND"}, value="BATT- contact")
text("+", bp[0] + 1.7, bp[1])
text("-", bm[0] + 1.7, bm[1])
# --- USB-C power-only receptacle, mouth at the bottom edge
UX, UY = 112.0, 138.9
fp(os.path.join(SYSLIB, "Connector_USB.pretty"), "USB_C_Receptacle_HRO_TYPE-C-31-M-12", "J1", UX, UY,
   value="TYPE-C-31-M-12",
   pads={"A1": "GND", "B12": "GND", "A12": "GND", "B1": "GND", "SH": "GND", "A4": "VBUS", "B9": "VBUS",
         "A9": "VBUS", "B4": "VBUS", "A5": "CC1", "B5": "CC2"})
fp(R0402, "R_0402_1005Metric", "R1", 110.0, 132.6, rot=90, pads={"1": "CC1", "2": "GND"}, value="5.1k")
fp(R0402, "R_0402_1005Metric", "R2", 114.2, 132.6, rot=90, pads={"1": "CC2", "2": "GND"}, value="5.1k")
fp(C0805, "C_0805_2012Metric", "C1", 106.2, 132.6, pads={"1": "VBUS", "2": "GND"}, value="10uF 25V")
fp(os.path.join(SYSLIB, "Diode_SMD.pretty"), "D_SMA", "D1", 103.0, 137.5, rot=90, pads={"1": "VBUS", "2": "GND"},
   value="SMAJ5.0A")
# --- charger
fp(os.path.join(SYSLIB, "Package_TO_SOT_SMD.pretty"), "SOT-23-5", "U1", 120.0, 136.3,
   pads={"1": "STAT", "2": "GND", "3": "VBAT", "4": "VBUS", "5": "PROG"}, value="MCP73831T-2ACI/OT")
fp(R0402, "R_0402_1005Metric", "R3", 122.6, 135.6, rot=90, pads={"1": "PROG", "2": "GND"}, value="15k")
fp(C0805, "C_0805_2012Metric", "C2", 120.0, 132.4, pads={"1": "VBAT", "2": "GND"}, value="10uF 25V")
fp(os.path.join(SYSLIB, "LED_SMD.pretty"), "LED_0603_1608Metric", "D2", 120.0, 140.2,
   pads={"1": "STAT", "2": "LED_A"}, value="LED red (charging)")
fp(R0402, "R_0402_1005Metric", "R4", 122.3, 139.6, rot=90, pads={"1": "VBUS", "2": "LED_A"}, value="1k")
# --- two M2 holes for the printed cradle, under the cartridge's cell (no parts there)
for i, (hx, hy) in enumerate(((102.6, 107.0), (121.4, 107.0))):
    fp(PODLIB, "M2_NPTH_clamp", "H%d" % (i + 1), hx, hy)
text("cartridge face down", 112.0, 112.0, size=1.0)
text("USB-C 5V, 67 mA", 112.0, 114.0, size=1.0)
# GND pour on the back
z = pcbnew.ZONE(b)
ls = pcbnew.LSET()
ls.AddLayer(pcbnew.B_Cu)
z.SetLayerSet(ls)
z.SetNet(net("GND"))
o = z.Outline()
o.NewOutline()
for px, py in ((X0 + .4, Y0 + .4), (X1 - .4, Y0 + .4), (X1 - .4, Y1 - .4), (X0 + .4, Y1 - .4)):
    o.Append(MM(px), MM(py))
z.SetMinThickness(MM(0.2))
z.SetLocalClearance(MM(0.25))
z.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
b.Add(z)
pcbnew.SaveBoard(OUT, b)

# --- route (Freerouting) and check
dsn, ses, rep = (os.path.join(WORK, n) for n in ("dock.dsn", "dock.ses", "drc.json"))
b = pcbnew.LoadBoard(OUT)
if not pcbnew.ExportSpecctraDSN(b, dsn):
    sys.exit("DSN export failed")
if os.path.exists(ses):
    os.remove(ses)
subprocess.run(["java", "-jar", JAR, "-de", dsn, "-do", ses, "-mp", "40", "--gui.enabled=false"],
               capture_output=True, text=True, timeout=600)
if not os.path.exists(ses) or not pcbnew.ImportSpecctraSES(b, ses):
    sys.exit("Freerouting produced no session")
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(OUT, b)
subprocess.run(["kicad-cli", "pcb", "drc", "--refill-zones", "--save-board", "--format", "json", "-o", rep, OUT],
               capture_output=True)
d = json.load(open(rep))
errs = [v for v in d["violations"] if v["severity"] == "error"]
print("dock: %d DRC errors, %d unconnected" % (len(errs), len(d.get("unconnected_items", []))))
for v in errs[:15]:
    print("  ", v["type"], v["description"])
sys.exit(1 if errs or d.get("unconnected_items") else 0)
