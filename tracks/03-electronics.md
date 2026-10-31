Track 03-electronics. What an electrical engineer needs to build the board.
- Biopotential analog front-ends usable for sEMG: TI ADS1299 / ADS1298 / ADS1294, Intan RHD2132/RHD2164,
  ADI AD8232/ADAS1000, Cerelog, newer 2024–2026 parts. Noise (µVrms), channels, sample rates, power, price.
- sEMG requirements for speech muscles: bandwidth (~20–450 Hz or wider?), sample rate (AlterEgo used?),
  gain, input-referred noise, CMRR, driven-right-leg / bias electrode, reference placement, motion
  artifacts, powerline rejection.
- MCU + radio: nRF52840 / nRF5340 / ESP32-S3, BLE throughput for N channels x 24-bit x 1–2 kHz,
  on-device inference options (TinyML, Ambiq Apollo, nRF54), latency.
- Power: battery size for all-day wear, power budget per block.
- Existing open hardware to copy: OpenBCI Cyton/Ganglion, HackEEG, FreeEEG32, PiEEG, Neuroidss,
  OpenEMG / BioAmp EXG (Upside Down Labs), ADS1299 reference designs, any open AlterEgo replication.
- Safety: battery-only isolation, IEC 60601 leakage limits as guidance, never connect to mains while worn.
- Output channel: bone-conduction transducers or tiny in-ear speakers; driver ICs.
Finish with a proposed block diagram + a starter BOM (part numbers, rough cost) for (a) a bench prototype
using off-the-shelf boards and (b) a miniaturised custom board.
Output: research/03-electronics.md
