#!/bin/sh
# Full rebuild of the pod board from the schematic generator. Stops at the first failing step.
set -e
cd "$(dirname "$0")"
python3 gen_sch.py
kicad-cli sch erc --severity-error --exit-code-violations -o erc.rpt pod.kicad_sch
kicad-cli sch export netlist -o pod.net pod.kicad_sch
python3 check_nets.py pod.net | tail -1
python3 gen_nina_fp.py
python3 gen_pcb.py
python3 route.py 100
python3 finish_route.py
kicad-cli pcb drc --refill-zones --save-board --schematic-parity --exit-code-violations --severity-error \
    --format json -o route/drc.json pod.kicad_pcb
echo "pod board: DRC clean"
