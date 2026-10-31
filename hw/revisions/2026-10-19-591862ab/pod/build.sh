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
python3 fix_gnd_pin.py U1 51        # rev 0.5: the re-route leaves this ADS GND pin on an unstitched pour sliver
python3 fix_gnd_pin.py U1 20        # rev 0.7: same for pin 20 (island under the module, no room for a via)
kicad-cli pcb drc --refill-zones --save-board --schematic-parity --exit-code-violations --severity-error \
    --format json -o route/drc.json pod.kicad_pcb
echo "pod board: DRC clean"
