# Repo shortlist (Claude-verified, 2026-10-09)

Source: `research/jaw/repos-scan.md` — 364 repos (pushed since 2024-06) fetched by tools/reposcan/fetch.py
(local lane item repo-scan-v2), ranked 0-3 by the local Qwen3.8-9B via tools/reposcan/rank.py. Each
entry below was re-read from its README by Claude. The 9B over-scored: ~30 emg2qwerty forks (wrist EMG ->
keystrokes, not speech) got 3, CrabLabsLLC/ADS129x got 3 but is an ADS1293 (3-ch) driver.

"No licence" = all rights reserved: read and learn from it, do not copy code.

## Decoder / data (phone side)
| Repo | What it is | Licence | Use |
|---|---|---|---|
| MyoVerse/emg2speech | Gowda et al., ACL 2026: orofacial sEMG -> speech via self-supervised speech (S3) representations; EMG power linear in S3 features (r=0.85); dataset + notebooks | none | Strongest recent method + data; read paper, re-implement |
| HarshavardhanaTG/emg2speech | Gowda & Miller, NeurIPS 2025 TS4H workshop: face/neck sEMG -> phonemes, SPD-manifold GRU, large vocab | none | Phoneme decoder design; pretrained checkpoints |
| MateusAquino/subvocalization-emg | Bachelor thesis: record + train subvocalized-word CNN on OpenBCI Cyton (same front-end values as ours) | BSD-3 | Day-1 small-vocab baseline + recording pipeline we can copy |
| DoladoEric/SSI-BaseLine-Implementation | CMU 11-785 project: depthwise conv + bi-Mamba + CTC (text + phonemes) on the Gaddy silent-speech data | none | Open-vocab architecture reference |
| lee-jhwn/multimodal-speech-biosignals | Interspeech 2026: 18 VCV syllables spoken/silent/imagined, rtMRI+EEG+3 sEMG | code MIT, data restrictive | Minor (3 EMG channels) |

## Firmware / app (pod side)
| Repo | What it is | Licence | Use |
|---|---|---|---|
| integra-lib/ads129x | Header-only C++20 ADS1294/6/8 driver, daisy chain, timing rules (tSCCS, tSDECODE, 4 MHz cmd / 20 MHz data); example = our exact config (1 kSPS, gain 6, internal 2.4 V ref) | none | Checklist for our SPI timing + register init |
| jackparsons93/OpenBCI_Projects | ADS1299 on nRF52840 with Zephyr: SPI tests + BLE streaming firmware, Python 8-ch BLE logger | GPL-3.0 | Closest working nRF52840 + ADS129x + BLE code |
| aewoonge-creator/ads1299-nrf54-ble-eeg | ADS1299 + nRF54L15 Zephyr firmware, Nordic UART BLE, Web Bluetooth GUI (register control, test signal, CSV) | none | Bring-up GUI idea: browser talks to pod directly |
| miruns/mock1299 | Python BLE peripheral that pretends to be an ADS1299 device (8-ch frames, packet-loss/jitter injection) | none | App dev before boards arrive (what ads129x-emulator can't do) |
| pieeg-club/ironbci | ADS1299 + STM32 BLE 8-ch wearable, Android SDK, Python SDK, 3D-printed headset, 633 stars | none | App/SDK structure reference |
| nikki-uwu/Meower | ESP32-C3 + 2x ADS1299, 16 ch, WiFi, manufacturing-ready PCB, 136 stars | Apache-2.0 | v2 (two ADCs) layout reference |
| brainflow-dev/brainflow | Standard biosignal SDK (1770 stars) | MIT-style | Add a pod board driver later -> every BrainFlow tool works |

## User-supplied
| Repo | Verdict |
|---|---|
| mateusglucas/ads129x-emulator | VHDL (FPGA) ADS129x emulator, 2023 — not usable without an FPGA; mock1299 / firmware test mode cover the need |
| RobertCsordas/MobilECG-II | Open clinical-grade ECG Holter: KiCad hardware, OpenSCAD case, firmware, Android (396 stars, 2023). HW CC-BY-SA, SW GPLv3. Compare its ADS1298 layout before ours |
| shriram-m/12-lead-holter-ecg | 2018 student build: ADS1298 + STM32 + HC-05 classic BT, 6-layer KiCad, JLCPCB. MIT. Check its IO filter + register init docs |

## Rejected (high 9B score, wrong on reading)
CrabLabsLLC/ADS129x (ADS1293), PranavKalkunte/subvocal and Wega-Labs/noema (plans/SDK shells), NeuroVox-v2.0 (forearm
gestures), CP-PHASE4_Subvocalization (AD8232, 0.5-40 Hz cuts most speech EMG), emg2qwerty forks (wrist typing).
