#!/bin/sh
# Rebuild the NDA review package hw/review/ and hw/sensor-pod-review.zip from the current boards (rev 0.7).
# Run after build.sh, route_tab.py, gen_dock.py and fab.py. Prints the zip's sha256 for the NDA annexes.
set -e
cd "$(dirname "$0")"
R=../review
kicad-cli sch export pdf -o $R/schematic.pdf pod.kicad_sch >/dev/null 2>&1
T=$(mktemp -d)
kicad-cli pcb export pdf --mode-multipage --scale 5 --sketch-pads-on-fab-layers --crossout-DNP-footprints-on-fab-layers \
    --layers F.Cu,F.Fab,In1.Cu,In2.Cu,In3.Cu,In4.Cu,B.Cu,B.Fab --cl Edge.Cuts -o $T/layers.pdf pod.kicad_pcb >/dev/null 2>&1
mv $T/layers.pdf $R/layout_layers.pdf
rmdir $T
cp design-notes.md lib/pod.pretty/u-blox_NINA-B306.kicad_mod $R/
rm -f $R/tab_charger_*
for b in pod tab_electrode cartridge dock; do
    cp ../fab/$b/${b}_gerbers.zip ../fab/$b/${b}_bom.csv ../fab/$b/${b}_cpl.csv $R/
done
cd ..
rm -rf sensor-pod-review sensor-pod-review.zip
cp -r review sensor-pod-review
# fixed file times in the zip (the PDFs still embed their creation time, so every run gives a new hash:
# run this once, then copy the printed hash into both NDA annexes)
find sensor-pod-review -exec touch -d 2026-10-16T00:00:00 {} +
zip -qrX sensor-pod-review.zip sensor-pod-review
rm -r sensor-pod-review
unzip -l sensor-pod-review.zip | tail -1
sha256sum sensor-pod-review.zip
