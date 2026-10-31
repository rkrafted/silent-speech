#!/usr/bin/env python3
"""Route the few connections Freerouting leaves open, with clearance-correct A* on a 0.05 mm grid.

    python3 hw/pod/finish_route.py            # reads route/drc.json (from route.py), edits pod.kicad_pcb

Every pad, track, via, NPTH hole and keep-out on the board is rasterised per copper layer (the GND
pours are ignored: they refill around new copper). Tracks may use F.Cu, In2, In3 and B.Cu; a layer
change costs a via. The result is checked by KiCad's DRC afterwards; this script only proposes copper.
"""
import heapq
import json
import math
import os
import subprocess
import sys

import numpy as np
import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pod_geom as G  # noqa: E402

PCB = os.path.join(HERE, "pod.kicad_pcb")
REP = os.path.join(HERE, "route", "drc.json")
STEP = 0.05
CLR = 0.10                       # router margin (DRC checks the fab's 0.09)
VIA_R, VIA_DRILL = 0.225, 0.20
LAYERS = [pcbnew.F_Cu, pcbnew.In2_Cu, pcbnew.In3_Cu, pcbnew.B_Cu]
ALL_CU = LAYERS + [pcbnew.In1_Cu, pcbnew.In4_Cu]
X0, Y0, X1, Y1 = G.BOARD
NX, NY = int(round((X1 - X0) / STEP)) + 1, int(round((Y1 - Y0) / STEP)) + 1
mm = pcbnew.ToMM


def cell(x, y):
    return int(round((x - X0) / STEP)), int(round((y - Y0) / STEP))


def pos(i, j):
    return X0 + i * STEP, Y0 + j * STEP


def width_for(netname):
    return 0.2 if netname in ("+BATT", "VBUS", "/BAT_RAW") else 0.15


def items_on(b, layer):
    out = []
    for f in b.GetFootprints():
        for p in f.Pads():
            if p.IsOnLayer(layer):
                out.append((p.GetNetname(), p.GetEffectiveShape(layer), p.GetBoundingBox()))
    T = b.Tracks()
    for k in range(len(T)):
        t = T[k]
        if t.GetClass() == "PCB_VIA" or t.GetLayer() == layer:
            out.append((t.GetNetname(), t.GetEffectiveShape(layer), t.GetBoundingBox()))
    return out


def raster(b, netname, inflate):
    """occ[layer][i, j] = True where a track centre (or via centre) of `netname` may NOT go."""
    occ = {}
    for la in ALL_CU:
        g = np.zeros((NX, NY), dtype=bool)
        for nn, sh, bb in items_on(b, la):
            if nn == netname:
                continue
            r = inflate
            i0, j0 = cell(mm(bb.GetX()) - r - STEP, mm(bb.GetY()) - r - STEP)
            i1, j1 = cell(mm(bb.GetRight()) + r + STEP, mm(bb.GetBottom()) + r + STEP)
            for i in range(max(0, i0), min(NX, i1 + 1)):
                for j in range(max(0, j0), min(NY, j1 + 1)):
                    if g[i, j]:
                        continue
                    x, y = pos(i, j)
                    if sh.Collide(pcbnew.SHAPE_CIRCLE(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)), 1),
                                  pcbnew.FromMM(r)):
                        g[i, j] = True
        occ[la] = g
    # board edge ring, NPTH holes, antenna keep-out: all layers
    blk = np.zeros((NX, NY), dtype=bool)
    edge = 0.35 + inflate - CLR
    for i in range(NX):
        for j in range(NY):
            x, y = pos(i, j)
            if x < X0 + edge or x > X1 - edge or y < Y0 + edge or y > Y1 - edge:
                blk[i, j] = True
    kx1, ky1, kx2, ky2 = G.antenna_keepout()
    a0, b0 = cell(kx1 - inflate, ky1 - inflate)
    a1, b1 = cell(kx2 + inflate, ky2 + inflate)
    blk[max(0, a0):a1 + 1, max(0, b0):b1 + 1] = True
    holes = [(hx, hy, 1.1) for hx, hy in G.HOLES]
    for f in b.GetFootprints():
        for p in f.Pads():
            if p.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH:
                holes.append((mm(p.GetPosition().x), mm(p.GetPosition().y), mm(p.GetDrillSize().x) / 2))
    for hx, hy, hr in holes:
        rr = hr + inflate + 0.1
        i0, j0 = cell(hx - rr, hy - rr)
        i1, j1 = cell(hx + rr, hy + rr)
        for i in range(max(0, i0), min(NX, i1 + 1)):
            for j in range(max(0, j0), min(NY, j1 + 1)):
                x, y = pos(i, j)
                if (x - hx) ** 2 + (y - hy) ** 2 < rr * rr:
                    blk[i, j] = True
    for la in occ:
        occ[la] |= blk
    return occ


def astar(start, goals, trk, via):
    """start/goals: sets of (layer_index, i, j). trk[l]: blocked for a track centre on signal layer l.
    via: blocked for a via centre (any layer)."""
    h = lambda n: min(abs(n[1] - g[1]) + abs(n[2] - g[2]) for g in goals)
    openq = [(h(s), 0, s, None) for s in start]
    heapq.heapify(openq)
    came, cost = {}, {s: 0 for s in start}
    moves = [(1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1), (1, 1, 1.414), (1, -1, 1.414), (-1, 1, 1.414),
             (-1, -1, 1.414)]
    while openq:
        f, g, n, parent = heapq.heappop(openq)
        if n in came:
            continue
        came[n] = parent
        if n in goals:
            path = [n]
            while came[path[-1]] is not None:
                path.append(came[path[-1]])
            return path[::-1]
        l, i, j = n
        nbrs = []
        for di, dj, c in moves:
            a, bq = i + di, j + dj
            if 0 <= a < NX and 0 <= bq < NY and not trk[l][a, bq]:
                nbrs.append(((l, a, bq), c))
        if not via[i, j]:
            for l2 in range(len(LAYERS)):
                if l2 != l:
                    nbrs.append(((l2, i, j), 25))
        for m, c in nbrs:
            ng = g + c
            if ng < cost.get(m, 1e18):
                cost[m] = ng
                heapq.heappush(openq, (ng + h(m), ng, m, n))
    return None


def endpoint_cells(b, item, netname, trk):
    """Cells of an unconnected item (pad or track) that the router may start from / end at."""
    x, y = item["pos"]["x"], item["pos"]["y"]
    out = set()
    for l, la in enumerate(LAYERS):
        if la not in ITEM_LAYERS.get(item["uuid"], ()):
            continue
        ci, cj = cell(x, y)
        for i in range(ci - 4, ci + 5):
            for j in range(cj - 4, cj + 5):
                if 0 <= i < NX and 0 <= j < NY and not trk[l][i, j]:
                    out.add((l, i, j))
    return out


def stitch_islands(b):
    """GND pour fragments (F/B) with no via get one stitching via where it fits."""
    filler = pcbnew.ZONE_FILLER(b)
    filler.Fill(b.Zones())
    T = b.Tracks()
    gvias = [T[k].GetPosition() for k in range(len(T)) if T[k].GetClass() == "PCB_VIA" and T[k].GetNetname() == "GND"]
    vmap = None
    added = 0
    for z in b.Zones():
        if z.GetIsRuleArea() or z.GetNetname() != "GND":
            continue
        for la in (pcbnew.F_Cu, pcbnew.B_Cu):
            if not z.IsOnLayer(la):
                continue
            polys = z.GetFilledPolysList(la)
            for k in range(polys.OutlineCount()):
                if any(polys.Contains(v, k) for v in gvias):
                    continue
                if vmap is None:
                    occ = raster(b, "GND", max(CLR + VIA_R, VIA_DRILL / 2 + 0.2))
                    vmap = np.zeros((NX, NY), dtype=bool)
                    for l2 in ALL_CU:
                        vmap |= occ[l2]
                bb = polys.COutline(k).BBox()
                i0, j0 = cell(mm(bb.GetX()), mm(bb.GetY()))
                i1, j1 = cell(mm(bb.GetRight()), mm(bb.GetBottom()))
                placed = False
                for i in range(max(0, i0), min(NX, i1 + 1)):
                    for j in range(max(0, j0), min(NY, j1 + 1)):
                        if vmap[i, j]:
                            continue
                        x, y = pos(i, j)
                        ring = [(x + 0.25 * math.cos(a * math.pi / 4), y + 0.25 * math.sin(a * math.pi / 4))
                                for a in range(8)] + [(x, y)]
                        if all(polys.Contains(pcbnew.VECTOR2I(pcbnew.FromMM(px), pcbnew.FromMM(py)), k)
                               for px, py in ring):
                            vo = pcbnew.PCB_VIA(b)
                            vo.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
                            vo.SetWidth(pcbnew.FromMM(2 * VIA_R))
                            vo.SetDrill(pcbnew.FromMM(VIA_DRILL))
                            vo.SetNet(b.FindNet("GND"))
                            b.Add(vo)
                            gvias.append(vo.GetPosition())
                            added += 1
                            placed = True
                            break
                    if placed:
                        break
                if not placed:
                    print("island on %s near (%.2f, %.2f): no room for a via" % (
                        "F" if la == pcbnew.F_Cu else "B", mm(bb.GetCenter().x), mm(bb.GetCenter().y)))
    print("stitching vias added:", added)


def nudge_clearance(b, rep):
    """Track-vs-copper clearance a few um short (a necked track widened to 0.09 mm): search small moves
    of the violating segment's free vertices (not ones sitting on a pad) and keep the first that clears
    every other-net item on that layer by 0.092 mm."""
    import itertools
    d = json.load(open(rep))
    T = b.Tracks()
    tr = [T[k] for k in range(len(T))]
    by_id = {str(t.m_Uuid.AsString()): t for t in tr}
    pad_pts = [(p.GetPosition(), p.GetNetname()) for f in b.GetFootprints() for p in f.Pads()]
    fixed = 0
    for v in d["violations"]:
        if v["type"] != "clearance":
            continue
        cand = [by_id.get(i.get("uuid")) for i in v["items"]]
        cand = [t for t in cand if t is not None and t.GetClass() == "PCB_TRACK"]
        if not cand:
            continue
        t0 = cand[0]
        netname, la = t0.GetNetname(), t0.GetLayer()
        free = [q for q in (t0.GetStart(), t0.GetEnd())
                if not any(q == pp and pn == netname for pp, pn in pad_pts)]
        segs = [t for t in tr if t.GetClass() == "PCB_TRACK" and t.GetNetname() == netname
                and any(t.GetStart() == q or t.GetEnd() == q for q in free)]
        others = [p.GetEffectiveShape(la) for f in b.GetFootprints() for p in f.Pads()
                  if p.IsOnLayer(la) and p.GetNetname() != netname]
        others += [t.GetEffectiveShape(la) for t in tr
                   if t.GetNetname() != netname and (t.GetClass() == "PCB_VIA" or t.GetLayer() == la)]
        orig = {id(t): (t.GetStart(), t.GetEnd()) for t in segs}
        steps = [0, -0.03, 0.03, -0.06, 0.06, -0.1, 0.1, -0.15, 0.15, -0.2, 0.2, -0.3, 0.3]
        moves = sorted(itertools.product(steps, steps, repeat=len(free)), key=lambda m: sum(map(abs, m)))
        ok = False
        for m in moves[:4000]:
            shift = {(q.x, q.y): pcbnew.VECTOR2I(q.x + pcbnew.FromMM(m[2 * k]), q.y + pcbnew.FromMM(m[2 * k + 1]))
                     for k, q in enumerate(free)}
            for t in segs:
                a, c = orig[id(t)]
                t.SetStart(shift.get((a.x, a.y), a))
                t.SetEnd(shift.get((c.x, c.y), c))
            if not any(t.GetEffectiveShape(la).Collide(o, pcbnew.FromMM(0.092)) for t in segs for o in others):
                ok = True
                break
        if not ok:
            for t in segs:
                t.SetStart(orig[id(t)][0])
                t.SetEnd(orig[id(t)][1])
        fixed += ok
    print("clearance nudges applied: %d" % fixed)


def main():
    d = json.load(open(REP))
    pairs = d.get("unconnected_items", [])
    b = pcbnew.LoadBoard(PCB)
    global ITEM_LAYERS
    ITEM_LAYERS = {}
    for f in b.GetFootprints():
        for p in f.Pads():
            ITEM_LAYERS[str(p.m_Uuid.AsString())] = [la for la in LAYERS if p.IsOnLayer(la)]
    T = b.Tracks()
    for k in range(len(T)):
        t = T[k]
        ITEM_LAYERS[str(t.m_Uuid.AsString())] = LAYERS if t.GetClass() == "PCB_VIA" else [t.GetLayer()]
    done, failed = 0, []
    for v in pairs:
        a, c = v["items"]
        desc = a["description"]
        if "Zone" in desc:
            failed.append("GND pour island (handled by stitching)")
            continue
        netname = desc.split("[")[1].split("]")[0]
        w = width_for(netname)
        occ_t = raster(b, netname, CLR + w / 2)
        occ_v = raster(b, netname, max(CLR + VIA_R, VIA_DRILL / 2 + 0.2))
        trk = [occ_t[la] for la in LAYERS]
        via = np.zeros((NX, NY), dtype=bool)
        for la in ALL_CU:
            via |= occ_v[la]
        s, g = endpoint_cells(b, a, netname, trk), endpoint_cells(b, c, netname, trk)
        if not s or not g:
            failed.append("%s: endpoint blocked" % netname)
            continue
        path = astar(s, g, trk, via)
        if not path:
            failed.append("%s: no path" % netname)
            continue
        net = b.FindNet(netname)
        # emit: join the item's exact point to the path ends, merge straight runs, vias at layer changes
        pts = [(l, *pos(i, j)) for (l, i, j) in path]
        pts = [(pts[0][0], a["pos"]["x"], a["pos"]["y"])] + pts + [(pts[-1][0], c["pos"]["x"], c["pos"]["y"])]

        def add_track(l, p0, p1):
            if abs(p0[0] - p1[0]) < 1e-6 and abs(p0[1] - p1[1]) < 1e-6:
                return
            t = pcbnew.PCB_TRACK(b)
            t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(p0[0]), pcbnew.FromMM(p0[1])))
            t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(p1[0]), pcbnew.FromMM(p1[1])))
            t.SetWidth(pcbnew.FromMM(w))
            t.SetLayer(LAYERS[l])
            t.SetNet(net)
            b.Add(t)

        run_l, run_start = pts[0][0], pts[0][1:]
        prev, prev_dir = pts[0][1:], None
        for l, x, y in pts[1:]:
            if l != run_l:                           # layer change: close the run, drop a via
                add_track(run_l, run_start, prev)
                vo = pcbnew.PCB_VIA(b)
                vo.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(prev[0]), pcbnew.FromMM(prev[1])))
                vo.SetWidth(pcbnew.FromMM(2 * VIA_R))
                vo.SetDrill(pcbnew.FromMM(VIA_DRILL))
                vo.SetNet(net)
                b.Add(vo)
                run_l, run_start, prev_dir = l, prev, None
                continue
            dvec = (round(x - prev[0], 4), round(y - prev[1], 4))
            n = math.hypot(*dvec) or 1
            dvec = (round(dvec[0] / n, 3), round(dvec[1] / n, 3))
            if prev_dir is not None and dvec != prev_dir:
                add_track(run_l, run_start, prev)
                run_start = prev
            prev_dir, prev = dvec, (x, y)
        add_track(run_l, run_start, prev)
        done += 1
        print("routed %s (%d cells)" % (netname, len(path)))
    stitch_islands(b)
    pcbnew.SaveBoard(PCB, b)
    print("finished %d, left: %s" % (done, failed or "none"))
    rep2 = os.path.join(HERE, "route", "drc_finish.json")
    subprocess.run(["kicad-cli", "pcb", "drc", "--refill-zones", "--format", "json", "-o", rep2, PCB],
                   capture_output=True)
    b = pcbnew.LoadBoard(PCB)
    nudge_clearance(b, rep2)
    pcbnew.SaveBoard(PCB, b)


if __name__ == "__main__":
    main()
