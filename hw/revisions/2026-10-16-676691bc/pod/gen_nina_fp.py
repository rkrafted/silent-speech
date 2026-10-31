#!/usr/bin/env python3
"""Write lib/pod.pretty/u-blox_NINA-B306.kicad_mod from the verified pad table in nina_pads.json.

Pad table: u-blox NINA-B3 data sheet UBX-17052099 land pattern, cross-checked pad by pad against the
LCSC/EasyEDA footprint for C6127317 (largest disagreement 75 um; data sheet wins). Frame: top view,
origin at the body centre, +y down, um. Antenna end at +y (pads 57 = EAGP sit at its corners).
EGP (12 centre pads) are all pad "56", EAGP (4) are all pad "57", matching the schematic symbol.
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
pads = json.load(open(os.path.join(HERE, "nina_pads.json")))
sig = sorted(p[0] for p in pads if p[1] == "signal")
assert sig == list(range(1, 56)), "signal pads must be exactly 1..55"
assert sum(p[1] == "egp" for p in pads) == 12 and sum(p[1] == "eagp" for p in pads) == 4
# no two pads may overlap or sit closer than 0.2 mm (land-pattern sanity)
for a, b in itertools.combinations(pads, 2):
    gx = abs(a[2] - b[2]) - (a[4] + b[4]) / 2
    gy = abs(a[3] - b[3]) - (a[5] + b[5]) / 2
    if max(gx, gy) < 200:
        sys.exit("pads %s and %s closer than 0.2 mm" % (a[:4], b[:4]))
mm = lambda v: v / 1000.0
lines = ['(footprint "u-blox_NINA-B306"', '\t(version 20241229)', '\t(generator "pod")', '\t(layer "F.Cu")',
         '\t(descr "u-blox NINA-B306 (nRF52840, internal antenna) 10 x 15 mm LGA. UBX-17052099 land pattern, '
         'checked against LCSC C6127317. Antenna end at +y. EGP = pad 56, EAGP = pad 57.")',
         '\t(tags "u-blox NINA-B3 BLE module")', '\t(attr smd)',
         '\t(property "Reference" "REF**" (at 0 -8.3 0) (layer "F.SilkS") (effects (font (size 0.6 0.6) (thickness 0.1))))',
         '\t(property "Value" "NINA-B306" (at 0 0 0) (layer "F.Fab") (effects (font (size 0.6 0.6) (thickness 0.1))))',
         '\t(fp_rect (start -5 -7.5) (end 5 7.5) (stroke (width 0.1) (type solid)) (fill no) (layer "F.Fab"))',
         '\t(fp_line (start -5 4.4) (end 5 4.4) (stroke (width 0.1) (type dash)) (layer "F.Fab"))',
         '\t(fp_text user "ANTENNA" (at 0 6 0) (layer "F.Fab") (effects (font (size 0.6 0.6) (thickness 0.1))))',
         '\t(fp_rect (start -5.25 -7.75) (end 5.25 7.75) (stroke (width 0.05) (type solid)) (fill no) (layer "F.CrtYd"))',
         '\t(fp_line (start -5.12 -7.62) (end -3.6 -7.62) (stroke (width 0.12) (type solid)) (layer "F.SilkS"))',
         '\t(fp_line (start -5.12 -7.62) (end -5.12 -6.3) (stroke (width 0.12) (type solid)) (layer "F.SilkS"))',
         '\t(fp_circle (center -5.6 -5.7) (end -5.45 -5.7) (stroke (width 0.15) (type solid)) (fill yes) (layer "F.SilkS"))']
for num, kind, x, y, w, h in pads:
    lines.append('\t(pad "%d" smd rect (at %.3f %.3f) (size %.3f %.3f) (layers "F.Cu" "F.Paste" "F.Mask"))'
                 % (num, mm(x), mm(y), mm(w), mm(h)))
lines.append(')')
out = os.path.join(HERE, "lib", "pod.pretty", "u-blox_NINA-B306.kicad_mod")
open(out, "w").write("\n".join(lines) + "\n")
print("wrote", out, len(pads), "pads")
