# Reference-board comparison (2026-10-11)

Boards cloned by local lane item `ref-boards` into hw/pod/ref/ext/ (gitignored). MobilECG-II parsed from its own
netlist (holter.net, Eeschema 2015) and PCB (holter.kicad_pcb) by Claude; 12-lead-holter-ecg read from docs/hardware.md
(it is a MobilECG-II derivative: same IO filter, HC-05 instead of the BLE module, 6 layers).

## MobilECG-II (ADS1298 + STM32F4 + TiWi-uB2 BLE, clinical-grade Holter)
| Item | MobilECG-II | Ours (rev 0.2) | Verdict |
|---|---|---|---|
| Electrode input | 470R -> 47pF + 0402 ESD -> 0402 ferrite -> 10k -> 47pF -> ADS (2-stage RC + bead) | ESD array -> 2.2k -> 1nF -> ADS | Ours OK for EMG (Cyton values). Their bead + 2nd stage add RF rejection; see change 3 |
| BIAS/RLD to body | RLD amp -> 10k series + 47pF + ferrite + 470R + ESD | RLD -> ESD, **no series R** | **Change 1**: add series R (answers our reviewer Q5) |
| RLD network | 392k ‖ 10nF, RLDINV=RLDIN | 392k ‖ 10nF | Same |
| Driven shield | OPA379 buffers RLDOUT onto the cable shields | none (flex strip) | v2 idea: driven guard plane in the strip (needs a 13th contact) |
| SPI/control lines | **51R series array (RP3)** on every ADS digital line | direct | **Change 2**: add 33-51R series on SCLK, MOSI, CS_N, MISO, DRDY |
| VCAP/VREF caps | VREFP 10u+100n, VCAP1 22u, VCAP2 1u+100n, VCAP3/4 1u | same values | Same |
| AVDD | 2.8 V from a **TLV61220 boost** + 4.7uH LC filter | 3.3 V from TPS7A2033 LDO (6.7 uVrms) | Ours quieter; no change |
| DVDD | 1.8 V + TXB0106 level shifter | 3.3 V direct | Ours simpler; fine (DVDD 1.65-3.6 V) |
| Clock | external (CLKSEL low, from MCU) | internal osc (CLKSEL high) | Both valid |
| Unused GPIO | floating | tied to GND | Ours per datasheet |
| Stack / ground | 4 layers, 1.6 mm, **one GND net poured on all 4 layers, no split** | 4 layers, L2 solid GND, single GND net | Same approach -> confirms reviewer Q5-style "no split" |
| Placement | ADS on bottom; BLE module 26.6 mm away; nearest boost 15.4 mm; board 47 x 52 mm | ~35 x 20 mm, NINA ~10-15 mm from ADS | We are 2x closer: keep SPI short, stitch GND vias, inputs on the side away from the antenna |

## 12-lead-holter-ecg
Same IO filter idea (TPD1E0B06 per line + ferrite + 2nd-order RC, corner ~225 kHz), 6-layer stack with a dedicated
ground layer, fabricated and assembled at JLCPCB. No BLE. Nothing new beyond confirming the bead + ESD pattern.

## Rev 0.3 changes (all three applied 2026-10-12, see design-notes 2a)
1. BIAS series resistor (MobilECG uses 10k). Limits current into the body, isolates RLD from strip capacitance.
2. 5 x 0402 series resistors (33-51R) at the driving end: SCLK/MOSI/CS_N near the NINA, MISO/DRDY near the ADS.
   Slower edges = less digital noise into the inputs; costs ~5 parts.
3. Optional insurance: 0402 ferrite bead per electrode line (10 parts) against BLE-burst pickup on the strip
   ("BLE buzz" at the connection interval). Ours already gives an estimated ~40 dB at 2.4 GHz (2.2k + 1nF);
   beads add ~20 dB more. Cost: 10 parts, ~10 mm2 board area in the tightest part of the pod.
