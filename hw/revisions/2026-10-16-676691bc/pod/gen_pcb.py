#!/usr/bin/env python3
"""Generate hw/pod/pod.kicad_pcb (ss-pod v1 board, 24 x 30 mm, parts on both sides) from pod.net.

Placement is written here part by part; routing is done afterwards by Freerouting on the exported
Specctra DSN. Re-run after any schematic change:

    kicad-cli sch export netlist -o hw/pod/pod.net hw/pod/pod.kicad_sch
    python3 hw/pod/gen_pcb.py

Stack: 6 layers. F.Cu and B.Cu parts + signals, In1.Cu and In4.Cu solid GND planes (no tracks; one
right under each assembled side), In2.Cu and In3.Cu signals and the 3.3 V supplies.
TOP (F): pogo grid, NINA-B306 (antenna at the top edge), power, SPI series R.
BOTTOM (B, battery side): ADS1298 + its decoupling, electrode ESD + bead + RC filters, flash, test pads.
Coordinates are seen from the top (x right, y down), board corner at (100, 100); see pod_geom.py.
"""
import math
import os
import sys

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_nets  # noqa: E402  (netlist parser)
import pod_geom as G  # noqa: E402

NET = os.path.join(HERE, "pod.net")
OUT = os.path.join(HERE, "pod.kicad_pcb")
SYSLIB = "/usr/share/kicad/footprints"
NINA_FP = os.path.join(HERE, "lib", "pod.pretty", "u-blox_NINA-B306.kicad_mod")
MM = pcbnew.FromMM


def V(x, y):
    return pcbnew.VECTOR2I(MM(x), MM(y))


# ------------------------------------------------------------------ netlist
root = check_nets.parse(open(NET, encoding="utf-8").read())
comps = {}
for c in check_nets.kids(check_nets.kid(root, "components"), "comp"):
    ref = check_nets.kid(c, "ref")[1]
    fp = check_nets.kid(c, "footprint")
    ts = check_nets.kid(c, "tstamps")
    comps[ref] = (fp[1] if fp else "", check_nets.kid(c, "value")[1], ts[1] if ts else "")
pin_net = {}
for n in check_nets.kids(check_nets.kid(root, "nets"), "net"):
    name = check_nets.kid(n, "name")[1]       # keep KiCad's "/LABEL" names (schematic parity)
    for nd in check_nets.kids(n, "node"):
        pin_net[(check_nets.kid(nd, "ref")[1], check_nets.kid(nd, "pin")[1])] = name
net_pins = {}
for (r, p), nn in pin_net.items():
    net_pins.setdefault(nn, []).append((r, p))

# ------------------------------------------------------------------ board + helpers
board = pcbnew.NewBoard(OUT)
board.SetCopperLayerCount(6)
board.SetLayerType(pcbnew.In1_Cu, pcbnew.LT_POWER)          # GND plane under the top side
board.SetLayerType(pcbnew.In4_Cu, pcbnew.LT_POWER)          # GND plane under the bottom (ADS1298) side
# ------------------------------------------------------------------ design rules (JLCPCB 4-layer standard)
ds = board.GetDesignSettings()
ds.m_MinClearance = MM(0.09)
ds.m_TrackMinWidth = MM(0.09)              # JLCPCB 4-layer minimum; Freerouting necks to 0.095 at pads
ds.m_ViasMinSize = MM(0.40)
ds.m_MinThroughDrill = MM(0.20)
ds.m_ViasMinAnnularWidth = MM(0.10)
ds.m_HoleClearance = MM(0.20)              # JLCPCB multilayer via hole to copper: 0.2 mm (confirm in review)
ds.m_HoleToHoleMin = MM(0.25)
ds.m_CopperEdgeClearance = MM(0.30)
ns = ds.m_NetSettings
dflt = ns.GetDefaultNetclass()
dflt.SetTrackWidth(MM(0.10))               # JLCPCB 6-layer standard: 0.09/0.09 mm
dflt.SetClearance(MM(0.10))
dflt.SetViaDiameter(MM(0.45))
dflt.SetViaDrill(MM(0.20))
pwr = pcbnew.NETCLASS("Power")
pwr.SetTrackWidth(MM(0.20))               # <= 100 mA charge current
pwr.SetClearance(MM(0.10))                # 5 V / 100 mA: no extra spacing needed
pwr.SetViaDiameter(MM(0.45))
pwr.SetViaDrill(MM(0.20))
pwr.SetPriority(0)
ns.SetNetclass("Power", pwr)
# Only the battery/charge path is wide: +3V3/+3.3VA carry a few mA and must reach 0.5 mm-pitch TQFP pins
POWER_NETS = ("+BATT", "/BAT_RAW", "VBUS")
ns.ClearNetclassPatternAssignments()          # the .kicad_pro keeps old patterns otherwise
for pn in POWER_NETS:
    ns.SetNetclassPatternAssignment(pn, "Power")

nets = {}


def net(name):
    if name not in nets:
        ni = pcbnew.NETINFO_ITEM(board, name)
        board.Add(ni)
        nets[name] = ni
    return nets[name]


def lib_path(lib):
    return os.path.join(HERE, "lib", lib + ".pretty") if lib in ("pod", "placeholder") else \
        os.path.join(SYSLIB, lib + ".pretty")


placed = {}
PLACEHOLDER = not os.path.exists(NINA_FP)


def load(ref):
    fpid, value, ts = comps[ref]
    lib, name = fpid.split(":", 1)
    if ref == "U2" and PLACEHOLDER:
        lib, name = "placeholder", "NINA_placeholder"
    fp = pcbnew.FootprintLoad(lib_path(lib), name)
    if fp is None:
        raise SystemExit("footprint not found: %s" % fpid)
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetFPID(pcbnew.LIB_ID(*fpid.split(":", 1)))
    if ts:
        fp.SetPath(pcbnew.KIID_PATH("/" + ts))
    for pad in fp.Pads():
        nn = pin_net.get((ref, pad.GetNumber()))
        if nn:
            pad.SetNet(net(nn))
    fp.Reference().SetLayer(pcbnew.F_Fab)       # too dense for silkscreen refs; assembly drawing uses Fab
    fp.Reference().SetTextSize(V(0.45, 0.45))
    fp.Reference().SetTextThickness(MM(0.07))
    board.Add(fp)
    placed[ref] = fp
    return fp


def pad_xy(ref, num):
    pads = [p for p in placed[ref].Pads() if p.GetNumber() == str(num)]
    if not pads:
        raise SystemExit("%s has no pad %s" % (ref, num))
    q = pads[0].GetPosition()
    return pcbnew.ToMM(q.x), pcbnew.ToMM(q.y)


def put(ref, x, y, rot=0, side="F", toward=None, axis=None):
    """Place a part. Bottom parts are flipped about their own centre. For 2-pin parts, `toward`
    (x, y) picks the rotation (along `axis` 'h' or 'v') that puts pad 1 closest to that point."""
    fp = placed.get(ref) or load(ref)
    fp.SetPosition(V(x, y))
    if side == "B" and not fp.IsFlipped():
        fp.Flip(V(x, y), pcbnew.FLIP_DIRECTION_LEFT_RIGHT)
    cands = [rot]
    if toward is not None:
        cands = {"h": [0, 180], "v": [90, 270], None: [0, 90, 180, 270]}[axis]
    best = None
    for r in cands:
        fp.SetOrientationDegrees(r)
        if toward is None:
            break
        px, py = pad_xy(ref, 1)
        d = (px - toward[0]) ** 2 + (py - toward[1]) ** 2
        if best is None or d < best[0]:
            best = (d, r)
    if best:
        fp.SetOrientationDegrees(best[1])
    return fp


def near_pin(ic, pin):
    return pad_xy(ic, pin)


# ------------------------------------------------------------------ TOP: grid, holes, module
for ref, (x, y) in G.GRID.items():
    put(ref, x, y)
put("H1", *G.HOLES[0])
put("H2", *G.HOLES[1])
put("U2", *G.NINA_CENTRE, rot=G.__dict__.get("NINA_ROT", 0))

# ------------------------------------------------------------------ BOTTOM: ADS1298
ADS = (116.0, 114.0)
u1 = put("U1", *ADS, side="B")
# choose the rotation that puts the inputs (pins 1-16) on the left, toward the filter rows
best = None
for r in (0, 90, 180, 270):
    u1.SetOrientationDegrees(r)
    xs = [pad_xy("U1", n)[0] for n in range(1, 17)]
    if best is None or sum(xs) < best[0]:
        best = (sum(xs), r)
u1.SetOrientationDegrees(best[1])

# filter rows (bottom, under the pogo grid): ESD -> bead -> 2.2k -> 1nF -> ADS. Rows follow the
# ADS input order; REF at the end nearest the REF pins' middle, BIAS at the RLD end.
lines = []
for i in range(1, 9):
    lines.append((pad_xy("U1", {1: 16, 2: 14, 3: 12, 4: 10, 5: 8, 6: 6, 7: 4, 8: 2}[i])[1],
                  ("FB%d" % i, "R%d" % i, "C%d" % i)))
lines.sort()
top_is_rld = pad_xy("U1", 63)[1] < ADS[1]
rows = [("FB9", "R9", "C9")] + [l[1] for l in lines] + [("FB10", "C10", "R25")]
if top_is_rld:
    rows = [("FB10", "C10", "R25")] + [l[1] for l in lines] + [("FB9", "R9", "C9")]
X_FB, X_R, X_C = 101.4, 103.6, 105.8
for i, (a, b, c) in enumerate(rows):
    y = 109.6 + 1.5 * i
    put(a, X_FB, y, side="B", toward=(X_FB - 2, y), axis="h")      # pad 1 (electrode) to the left
    put(b, X_R, y, side="B", toward=(X_R - 2, y), axis="h")
    put(c, X_C, y, side="B", toward=(X_C - 2, y), axis="h")
put("R25", X_C, 109.6 + 1.5 * (0 if top_is_rld else 9), side="B", toward=(X_C + 2, 0), axis="h")

# ESD arrays in the four free corners of the grid area (bottom)
put("D2", 101.75, 102.4, rot=90, side="B")
put("D3", 101.75, 127.6, rot=90, side="B")
put("D4", 108.65, 127.6, rot=90, side="B")


# ADS decoupling: each cap 2.0 mm outside its pin, pad 1 toward the pin
def decap(ref, pin, out=2.0, along=0.0):
    px, py = pad_xy("U1", pin)
    dx, dy = px - ADS[0], py - ADS[1]
    if abs(dx) > abs(dy):
        x, y = px + (out if dx > 0 else -out), py + along
        ax = "h"
    else:
        x, y = px + along, py + (out if dy > 0 else -out)
        ax = "v"
    put(ref, x, y, side="B", toward=(px, py), axis=ax)


sgn = 1 if pad_xy("U1", 55)[0] > pad_xy("U1", 54)[0] else -1
sgb = 1 if pad_xy("U1", 26)[0] > pad_xy("U1", 24)[0] else -1
decap("C18", 21, out=2.05)            # AVDD
decap("C12", 24, out=2.05, along=-0.15 * sgb)   # VREFP 100n
decap("C17", 26, out=2.05, along=0.15 * sgb)    # VCAP4
decap("C15", 30, out=2.05)            # VCAP2
decap("C19", 54, out=2.05, along=-0.6 * sgn)    # AVDD1
decap("C16", 55, out=2.05, along=0.6 * sgn)     # VCAP3
decap("C32", 60, out=2.05)            # RLDREF
decap("C33", 64, out=2.05)            # WCT
decap("C21", 50, out=2.05)            # DVDD
sgd = 1 if pad_xy("U1", 49)[0] > pad_xy("U1", 50)[0] else -1
decap("C20", 50, out=2.05, along=1.1 * sgd)   # DVDD pin 48 (corner; right side has no room)
# bulk caps (0805) in a second row above the 0402 decaps, clear of the antenna keep-out (y < 103.4).
# Pad 1 sits exactly in line with a free gap so its pre-route runs straight to the pin:
# C14 (VCAP1) pad 1 above pin 28 (no 0402 there); C13 (VREFP) pad 1 above pin 25, between C12 and C17.
p25, p28 = pad_xy("U1", 25), pad_xy("U1", 28)
put("C13", p25[0] - 1.0 * sgb, 104.3, side="B", toward=(p25[0], 110), axis="h")   # VREFP 10u
put("C14", p28[0] + 1.0 * sgb, 104.3, side="B", toward=(p28[0], 110), axis="h")   # VCAP1 22u
p61, p63 = pad_xy("U1", 61), pad_xy("U1", 63)
ry = p63[1] + (3.6 if p63[1] > ADS[1] else -3.6)
put("R10", p61[0] - 0.4, ry, side="B", toward=p63, axis="h")
put("C11", p61[0] - 0.4, ry + (1.2 if ry > ADS[1] else -1.2), side="B", toward=p63, axis="h")

# ------------------------------------------------------------------ locked pre-routes: ADS decoupling
# Each cap's pad 1 -> its own pin: straight, or one bend just outside the pin row. Shortest loops, and
# Freerouting keeps them (locked) instead of wandering around the 0.5 mm-pitch pin field.
PRE_SEGS = []


def pre_route(ref, pin, width=0.2):
    cx, cy = pad_xy(ref, 1)
    px, py = pad_xy("U1", pin)
    ox, oy = (1 if px > ADS[0] else -1, 0) if abs(px - ADS[0]) > abs(py - ADS[1]) else (0, 1 if py > ADS[1] else -1)
    tx, ty = px + ox * 0.74, py + oy * 0.74          # outer end of the pin pad
    if abs((cx - px) if oy else (cy - py)) < 0.05:
        pts = [(cx, cy), (px, py)]
    elif oy:
        pts = [(cx, cy), (cx, ty + oy * 0.65), (px, ty + oy * 0.3), (px, py)]   # enter the pin end-on
    else:
        pts = [(cx, cy), (tx + ox * 0.65, cy), (tx + ox * 0.3, py), (px, py)]
    nn = pin_net[("U1", str(pin))]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        t = pcbnew.PCB_TRACK(board)
        t.SetStart(V(ax, ay))
        t.SetEnd(V(bx, by))
        t.SetWidth(MM(width))
        t.SetLayer(pcbnew.B_Cu)
        t.SetNet(net(nn))
        t.SetLocked(True)
        board.Add(t)
        PRE_SEGS.append((ax, ay, bx, by, width / 2, nn))


for ref, pin in (("C18", 21), ("C12", 24), ("C13", 24), ("C17", 26), ("C14", 28), ("C15", 30), ("C19", 54),
                 ("C16", 55), ("C32", 60), ("C33", 64), ("C21", 50)):
    pre_route(ref, pin)

# flash + test pads (bottom, lower right)
# LDOs on the bottom, beside the ADS1298's lower supply pins (the flash moved to the top)
put("U3", 116.0, 127.4, side="B")                                # LDO1 -> AVDD
put("C24", 115.4, 124.6, side="B", toward=(113, 124.6), axis="h")
put("C26", 117.4, 124.6, side="B", toward=(119, 124.6), axis="h")
put("U4", 120.6, 127.4, side="B")                                # LDO2 -> +3V3
put("C25", 119.5, 124.6, side="B", toward=(118, 124.6), axis="h")
put("C27", 121.5, 124.6, side="B", toward=(123, 124.6), axis="h")
# test/expansion pads (rev 0.6): moved from the bottom-edge strip to the free spot by H1, so the strip is free for
# the battery-cartridge contacts. They stay reachable: the cartridge comes off.
for i, ref in enumerate(["TP1", "TP2", "TP8", "TP9", "TP10", "TP11", "TP12", "TP13", "TP14"]):
    put(ref, 109.1 + 1.3 * (i % 3), 102.1 + 1.3 * (i // 3), side="B")

# battery-cartridge contacts (rev 0.6): in the bottom-edge strip the 20 x 20 mm cell leaves free (cell at
# y 104.8-124.8, clear of the H1 screw head), between D4 and LDO1. The cartridge's spring pins land here.
# diagonal, 2.9 mm apart: a misplaced spring pin can never bridge + and - (that would short the cell)
put("TP15", *G.CART_PADS["BATT+"], side="B")                    # BATT+ (BAT_RAW, before the AO3401A)
put("TP16", *G.CART_PADS["BATT-"], side="B")                    # BATT- (GND)

# ------------------------------------------------------------------ TOP: power + module support
put("J3", 105.2, 107.15)                                         # SWD Tag-Connect, between H1 and the grid
put("D5", 105.2, 122.93)                                         # VBUS TVS right under P11
put("C28", 109.0, 126.75, toward=(109.0, 125), axis="v")         # VBUS 10u, next to U5 VDD
put("U5", 112.7, 125.0)                                          # MCP73831
put("R11", 115.35, 124.6, toward=(115.35, 126), axis="v")
put("C29", 112.3, 128.6, toward=(110, 128.6), axis="h")        # +BATT 10u
put("Q2", 116.1, 128.2)
put("J2", 121.05, 126.675)                                       # JST SH, opening at the bottom edge
# 16 MB flash right under the module's QSPI pin row (pins 47-52): ~4 mm, top layer only
put("U6", 115.0, 119.4, rot=270)
put("C34", 110.75, 117.8, toward=(110.75, 116), axis="v")        # flash VCC decoupling
put("R24", 110.75, 120.1, toward=(110.75, 122), axis="v")        # QSPI_CS pull-up
# pulls, battery divider, VBUS_MOD series R: two columns at the right edge, below the module
for i, ref in enumerate(["R20", "R22", "R23", "R13", "R21", "R16", "R14", "R15", "C30"]):
    put(ref, 118.9 + 1.05 * (i % 5), 116.7 + 2.1 * (i // 5), toward=(0, 0), axis="v")
# module supply decoupling in the strip right of the module, beside VCC/VCC_IO (pins 10, 9)
put("C22", 122.27, 102.4, toward=pad_xy("U2", 10), axis="v")    # corner strip: keeps x > 121.2 free
put("C23", 123.3, 102.4, toward=pad_xy("U2", 9), axis="v")    # for the SPI vias beside pins 1-8

missing = sorted(set(comps) - set(placed))

# reload so every pad's cached copper shape reflects its final flip/rotation (KiCad caches them)
pcbnew.SaveBoard(OUT, board)
board = pcbnew.LoadBoard(OUT)
placed = {f.GetReference(): f for f in board.GetFootprints()}
nets = {n: board.FindNet(n) for n in list(nets)}

# ------------------------------------------------------------------ GND fan-out vias
# Freerouting treats GND as the In1 plane net but does not drop vias for SMD pads, so every GND pad
# gets its own short stub + via here, before routing. A candidate via must clear every other pad on
# both sides (vias go through), the NPTH holes, other vias, the board edge and the antenna keep-out.
FAN_NET = "GND"
VIA_R, VIA_DRILL, CLR = 0.225, 0.20, 0.16     # GND is in the Power class: 0.15 mm clearance
vias, stubs, fan_fail = [], [], []
holes = [(*G.HOLES[0], 1.1), (*G.HOLES[1], 1.1)] + \
    [(pcbnew.ToMM(p.GetPosition().x), pcbnew.ToMM(p.GetPosition().y), pcbnew.ToMM(p.GetDrillSize().x) / 2)
     for p in placed["J3"].Pads() if p.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH]
all_pads = [p for f in placed.values() for p in f.Pads() if p.GetAttribute() != pcbnew.PAD_ATTRIB_NPTH]
kx1, ky1, kx2, ky2 = G.antenna_keepout()


def seg_dist2(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy or 1e-12
    u = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    return (px - ax - u * dx) ** 2 + (py - ay - u * dy) ** 2


def seg_seg_close(ax, ay, bx, by, cx, cy, dx, dy, lim):
    """True if segments AB and CD come closer than lim (sampled; segments here are < 3 mm)."""
    for i in range(11):
        t = i / 10
        if seg_dist2(ax + t * (bx - ax), ay + t * (by - ay), cx, cy, dx, dy) < lim * lim:
            return True
        if seg_dist2(cx + t * (dx - cx), cy + t * (dy - cy), ax, ay, bx, by) < lim * lim:
            return True
    return False


def via_ok(x, y, src, stub_layer):
    bx0, by0, bx1, by1 = G.BOARD
    if not (bx0 + 0.6 < x < bx1 - 0.6 and by0 + 0.6 < y < by1 - 0.6):
        return False
    if kx1 - 0.4 < x < kx2 + 0.4 and y < ky2 + 0.4:
        return False
    for hx, hy, hr in holes:
        if (x - hx) ** 2 + (y - hy) ** 2 < (hr + VIA_R + 0.3) ** 2:
            return False
    sx, sy = (pcbnew.ToMM(src.GetPosition().x), pcbnew.ToMM(src.GetPosition().y)) if src is not None else (x, y)
    for vx, vy, vn in vias:
        lim = 0.55 if vn == FAN_NET else 2 * VIA_R + CLR
        if (x - vx) ** 2 + (y - vy) ** 2 < lim ** 2:
            return False
        if vn != FAN_NET and seg_dist2(vx, vy, sx, sy, x, y) < (VIA_R + 0.125 + CLR) ** 2:
            return False                              # new stub would pass another net's via
    for ax, ay, bx, by, hw, sn in PRE_SEGS:          # locked tracks and earlier stubs
        if sn == FAN_NET:
            continue
        if seg_dist2(x, y, ax, ay, bx, by) < (VIA_R + hw + CLR) ** 2:
            return False
        if src is not None and seg_seg_close(sx, sy, x, y, ax, ay, bx, by, 0.125 + hw + CLR):
            return False
    circ = pcbnew.SHAPE_CIRCLE(V(x, y), MM(VIA_R))
    seg = None
    if src is not None:
        seg = pcbnew.SHAPE_SEGMENT(src.GetPosition(), V(x, y), MM(0.25))
    for p in all_pads:
        if p is src:
            continue
        same = p.GetNetname() == FAN_NET
        for la in (pcbnew.F_Cu, pcbnew.B_Cu):
            if not p.IsOnLayer(la):
                continue
            sh = p.GetEffectiveShape(la)
            if sh.Collide(circ, MM(0.02 if same else CLR)):
                return False
            if seg is not None and la == stub_layer and not same and sh.Collide(seg, MM(CLR)):
                return False
    return True


def add_via(x, y, src=None, layer=None, netname="GND"):
    v = pcbnew.PCB_VIA(board)
    v.SetPosition(V(x, y))
    v.SetWidth(MM(2 * VIA_R))
    v.SetDrill(MM(VIA_DRILL))
    v.SetNet(net(netname))
    board.Add(v)
    vias.append((x, y, netname))
    if src is not None:
        t = pcbnew.PCB_TRACK(board)
        t.SetStart(src.GetPosition())
        t.SetEnd(V(x, y))
        t.SetWidth(MM(0.25))
        t.SetLayer(layer)
        t.SetNet(net(netname))
        board.Add(t)
        PRE_SEGS.append((pcbnew.ToMM(src.GetPosition().x), pcbnew.ToMM(src.GetPosition().y), x, y, 0.125, netname))


def lock_path(pts, netname, layer, width):
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        t = pcbnew.PCB_TRACK(board)
        t.SetStart(V(ax, ay))
        t.SetEnd(V(bx, by))
        t.SetWidth(MM(width))
        t.SetLayer(layer)
        t.SetNet(net(netname))
        t.SetLocked(True)
        board.Add(t)
        PRE_SEGS.append((ax, ay, bx, by, width / 2, netname))


# TPS7A20 EN (pin 3) tied to IN (pin 1): loop outside the GND pin 2, on the LDO's own (bottom) side
for ldo in ("U3", "U4"):
    (x1, y1), (x3, y3) = pad_xy(ldo, 1), pad_xy(ldo, 3)
    o = -1 if x1 < pcbnew.ToMM(placed[ldo].GetPosition().x) else 1
    lock_path([(x1, y1), (x1 + o * 0.95, y1), (x3 + o * 0.95, y3), (x3, y3)], "+BATT", pcbnew.B_Cu, 0.25)
# ADS1298 CLKSEL (pin 52, +3V3) joins the pin-50 DVDD decoupling track just outside the pin row
p50, p52 = pad_xy("U1", 50), pad_xy("U1", 52)
oy = 1 if p50[1] > ADS[1] else -1
tip = p50[1] + oy * 0.74
lock_path([p52, (p52[0], tip + oy * 0.3), (p50[0], tip + oy * 0.65)], "+3V3", pcbnew.B_Cu, 0.2)
# SWDIO (module pin 15) is boxed in by the antenna keep-out: escape via just inside the module
FAN_NET = "/SWDIO"
sx, sy = pad_xy("U2", 15)
for dy in (1.15, 1.25, 1.35, 1.5, 1.65, 1.8, 2.0):
    for dx in (0.0, 0.15, -0.15, 0.3, -0.3, 0.45, -0.45, 0.6):
        if via_ok(sx + dx, sy + dy, None, None):
            lock_path([(sx, sy), (sx + dx, sy + dy)], "/SWDIO", pcbnew.F_Cu, 0.15)
            add_via(sx + dx, sy + dy, None, None, "/SWDIO")
            break
    else:
        continue
    break
else:
    print("WARNING: no escape via for SWDIO")
FAN_NET = "GND"

# NINA centre ground pads (EGP, pad 56): one via in the middle of every 2 x 2 group (touches no pad)
egp = [(pcbnew.ToMM(p.GetPosition().x), pcbnew.ToMM(p.GetPosition().y)) for p in placed["U2"].Pads()
       if p.GetNumber() == "56"]
key = {(round(x, 2), round(y, 2)) for x, y in egp}
for x, y in egp:
    quad = [(round(x + dx, 2), round(y + dy, 2)) for dx in (0, 1.15) for dy in (0, 1.15)]
    if all(q in key for q in quad) and via_ok(x + 0.575, y + 0.575, None, None):
        add_via(x + 0.575, y + 0.575)       # (the ADS1298 sits under the module on the bottom side)

FAN_NET = "GND"


def fan_out(netname):
    global FAN_NET
    FAN_NET = netname
    fail = []
    for f in placed.values():
        fx, fy = pcbnew.ToMM(f.GetPosition().x), pcbnew.ToMM(f.GetPosition().y)
        for p in f.Pads():
            if p.GetNetname() != netname or p.GetAttribute() != pcbnew.PAD_ATTRIB_SMD:
                continue
            if f.GetReference() == "U2" and p.GetNumber() == "56":
                continue
            layer = pcbnew.F_Cu if p.IsOnLayer(pcbnew.F_Cu) else pcbnew.B_Cu
            px, py = pcbnew.ToMM(p.GetPosition().x), pcbnew.ToMM(p.GetPosition().y)
            half = max(pcbnew.ToMM(p.GetSize().x), pcbnew.ToMM(p.GetSize().y)) / 2
            ox, oy = px - fx, py - fy
            base = math.atan2(oy, ox) if (ox or oy) else 0.0
            done = False
            for d in (half + 0.4, half + 0.6, half + 0.85, half + 1.1, half + 1.4):
                for k in range(17):                      # 0, +-22.5 ... +-157.5, 180 degrees from outward
                    a = base + (k // 2) * (math.pi / 8) * (1 if k % 2 == 0 else -1) if k < 16 else base + math.pi
                    x, y = px + d * math.cos(a), py + d * math.sin(a)
                    if via_ok(x, y, p, layer):
                        add_via(x, y, p, layer, netname)
                        done = True
                        break
                if done:
                    break
            if not done:
                fail.append("%s.%s" % (f.GetReference(), p.GetNumber()))
    return fail


fan_fail = fan_out("GND")
n_gnd = len(vias)
# (+3V3 is routed as a normal net on the two inner signal layers; no power plane)
vias_gnd = n_gnd
print("GND fan-out: %d vias, no room for: %s" % (vias_gnd, ", ".join(fan_fail) or "none"))

# ------------------------------------------------------------------ outline, planes, keep-outs
x0, y0, x1, y1 = G.BOARD
edge = pcbnew.PCB_SHAPE(board)
edge.SetShape(pcbnew.SHAPE_T_RECT)
edge.SetStart(V(x0, y0))
edge.SetEnd(V(x1, y1))
edge.SetLayer(pcbnew.Edge_Cuts)
edge.SetWidth(MM(0.1))
board.Add(edge)


def zone(layers, netname, pts, rule=False, prio=0, name=""):
    z = pcbnew.ZONE(board)
    z.SetLayerSet(layers)
    if netname:
        z.SetNet(net(netname))
    o = z.Outline()
    o.NewOutline()
    for px, py in pts:
        o.Append(MM(px), MM(py))
    if rule:
        z.SetIsRuleArea(True)
        z.SetDoNotAllowTracks(True)
        z.SetDoNotAllowVias(True)
        z.SetDoNotAllowPads(True)
        z.SetDoNotAllowZoneFills(True)
        z.SetDoNotAllowFootprints(False)
    else:
        z.SetMinThickness(MM(0.2))
        z.SetLocalClearance(MM(0.2))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
        z.SetAssignedPriority(prio)
    if name:
        z.SetZoneName(name)
    board.Add(z)
    return z


def lset(*layers):
    s = pcbnew.LSET()
    for la in layers:
        s.AddLayer(la)
    return s


ins = 0.5
rect = [(x0 + ins, y0 + ins), (x1 - ins, y0 + ins), (x1 - ins, y1 - ins), (x0 + ins, y1 - ins)]
zone(lset(pcbnew.In1_Cu), "GND", rect, name="GND plane")
zone(lset(pcbnew.F_Cu, pcbnew.B_Cu), "GND", rect, name="GND pour")
zone(lset(pcbnew.In4_Cu), "GND", rect, name="GND plane 2")
kx1, ky1, kx2, ky2 = G.antenna_keepout()
zone(pcbnew.LSET.AllCuMask(), "", [(kx1, ky1), (kx2, ky1), (kx2, ky2), (kx1, ky2)], rule=True,
     name="antenna keep-out")

ring = pcbnew.ZONE(board)
ring.SetLayerSet(pcbnew.LSET.AllCuMask())
ro = ring.Outline()
ro.NewOutline()
for px, py in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
    ro.Append(MM(px), MM(py))
ro.NewHole()
for px, py in ((x0 + .35, y0 + .35), (x1 - .35, y0 + .35), (x1 - .35, y1 - .35), (x0 + .35, y1 - .35)):
    ro.Append(MM(px), MM(py), 0, 0)
ring.SetIsRuleArea(True)
ring.SetDoNotAllowTracks(True)
ring.SetDoNotAllowVias(True)
ring.SetDoNotAllowZoneFills(False)
ring.SetDoNotAllowPads(False)
ring.SetDoNotAllowFootprints(False)
ring.SetZoneName("edge: no tracks")
board.Add(ring)

pcbnew.ZONE_FILLER(board).Fill(board.Zones())
pcbnew.SaveBoard(OUT, board)
print("wrote %s: %d/%d footprints placed" % (OUT, len(placed), len(comps)))
if missing:
    print("NOT PLACED:", ", ".join(missing))
if PLACEHOLDER:
    print("WARNING: U2 is a PLACEHOLDER (no pads). Do not route or order until lib/pod.pretty/"
          "u-blox_NINA-B306.kicad_mod exists.")
