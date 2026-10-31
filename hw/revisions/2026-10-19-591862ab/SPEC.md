# Sensor pod v1: full design spec (single source of truth)

Rev 0.7 (built 2026-10-16: pod, tab, cartridge and dock all pass DRC). Written 2026-10-16 from every owner decision since 2026-10-01 (chat transcripts re-read).
When this file and another doc disagree, this file wins. Fix the other doc.
`[owner]` = the owner decided it. `[Claude]` = my engineering choice (can be overruled). `[verify]` = not yet confirmed.

## 0. Things I had forgotten or changed without asking (found in this review)

1. **Magnets.** Oct 6–7 you asked for magnetic charging, and the strip was to click on magnetically, like a smartwatch
   charger. On Oct 14 I replaced the magnets with M2 nylon screws and spacers and never told you. **Restored:** the
   worn strip, the battery cartridge and the dock all hold on with magnets in the case (§4). Screws are only for
   the bench electrode tab.
2. **Two pods.** The Oct 7 plan was that each pod talks to the phone on its own, synced by radio, with no wire. My
   rev 0.7 plan assumed a wire between the pods without asking where that wire would run (behind the neck? under
   the chin?). **Fixed:** radio sync is the default, and a wired clock link is an option (§6).
3. **Sample rate.** On Oct 7 we agreed **1000 samples/s by default**, with 500 only as a weak-link fallback. The design notes
   still said "500–1000".
4. **Stale docs.** design-notes.md still says "rev 0.4" in its title. Its §6 still describes the 150 mAh pouch, and
   its idle text assumes a 200 mAh cell. The review README still describes the USB charger.
5. **I2C pins.** My plan said "I2C must not use the near-antenna pins", but every free pin far from the antenna is
   already used. Now handled in §3.
6. **The dock pads must be mirrored.** The cartridge lies upside down on the dock, so the pad pattern must be the
   mirror image of the pod's. Easy to get wrong.
7. **No USB means no power from the programmer.** Flashing firmware needs a cell fitted (cartridge or bench JST).

## 1. What it is and who it is for [owner]
- Hidden, non-invasive silent-speech input: surface EMG from the jaw / under the chin / behind the ear.
  - English first, Latvian later.
  - No implant.
  - Nothing visible on the face.
- First market segment: consumer hands-free input (CE / RED route, no medical claims).
- Pipeline:
  - pod → phone (iOS **and** Android) → the user's own Mac or server, or local models;
  - text goes to Brilliant Labs **Halo** glasses (display, mic, camera).
- Target: **under 12 % WER on the owner's own data** (commands and own vocabulary first). Speed matters: snappy,
  minimum input lag.
- Also an open tinkering platform: it records and stores raw data, and has spare pins for add-ons.
- Deadline 2026-12-31. One MVP order: JLCPCB, 2 assembled pods. **It must work first time.** The schematic and its
  review are Claude's ("bulletproof").

## 2. Where it sits on the head [owner]
- **Pod:** low behind the ear, on the bone behind the earlobe (mastoid).
  - The Halo's **round battery tip** sits above it, at the end of the glasses arm.
  - The pod must not touch it, and the antenna keeps about 2 cm clear of it.
  - The case is shaped from the owner's head scan.
- **Skin side** = the pod's top board face (radio module, pogo grid). REF and BIAS sit on the bone right under the
  pod.
- **Outer side** = the bottom board face (ADS1298) plus the battery cartridge, which can therefore be swapped while
  worn.
- **Antenna:** at the board edge, pointing away from the head and away from the Halo tip, with no metal within 5–10 mm.
  - It must work under a hat, hood or coat.
  - Expect reduced range; about 1 m to the phone is enough. Check RSSI on the first boards.
- **Electrodes:** 10 contacts = 8 signal + REF + BIAS.
  - **v1 (this order):** ECG hydrogel snap electrodes on leads, through the bench electrode tab.
  - **Later:** a Y-shaped skin-tone flex strip (jaw angle → mid-jaw → chin corner → under the chin, with a throat
    branch) that presses straight onto the pogo pins. Its spots are decided by the cup recordings.
  - The e-tattoo strip comes after that.
- **Two pods worn at once** (one behind each ear = 16 channels) [owner, Oct 16].

## 3. Electronics, rev 0.7
| Block | Part | Notes |
|---|---|---|
| EMG front end | ADS1298IPAG (TQFP-64), 8 ch, unipolar 3.3 V, internal 2.4 V ref | 1000 SPS default, gain ×6 or lower. Lead-off detection on, feeding the app's "electrode lost contact" warning |
| Input filter, per line ×10 | TPD4E1B06 ESD → BLM15HD182SN1D bead → 2.2 k → 1 nF | BIAS: RLDOUT → 10 k → 1 nF + bead → pad. RLD loop 392 k ∥ 10 nF |
| Radio + MCU | u-blox NINA-B306 (nRF52840), internal antenna | antenna keep-out on all layers; EAGP pads grounded |
| Storage | W25Q128JV 16 MB QSPI NOR | ~11 min of raw 8-ch data. Bridges BLE drop-outs and cartridge swaps |
| Power in | cartridge pads TP15 (BATT+) / TP16 (BATT−), or the bench JST SH J2; **one cell at a time** | AO3401A reverse-polarity FET; C29 bulk on +BATT |
| Regulators | 2 × TPS7A2033 (AVDD alone; DVDD + module) | EN tied to IN, always on |
| **Fuel gauge (new)** | MAX17048 (TDFN-8 2 × 2) on +BATT | real % per cartridge in the app; I2C, 4.7 k pull-ups to +3V3 |
| Battery divider | 1 M / 1 M + 100 nF on pin 16 | **kept** as a fallback reading if the gauge fails |
| **Clock select (new)** | ADS1298 CLKSEL → a free NINA pin, 100 k pull-up | default = internal clock; firmware pulls it low to take an outside clock (§6) |
| **CLK_SYNC (new)** | ADS1298 CLK → 100 Ω → pogo **P11**, ESD on D4's spare channel | was VBUS. 1 M pull-down so it never floats |
| Programming | Tag-Connect TC2030-NL pads (SWD) | cable TC2030-CTX-NL + J-Link EDU Mini or nRF52840 DK. Later updates over BLE OTA. **A cell must be fitted** |
| Expansion | 5 GPIO pads + 3V3 + GND | for tinkering: IMU, mic, vibration motor and so on |
| Lights | **none** [owner] | every status goes to the app |
| **Removed in rev 0.7** | MCP73831, R11, C28, D5 TVS, R16, the VBUS net, the charger tab | charging moves to the dock (§5) |

**Pin rules:**
- The ADS1298 link stays on module pins 1–5, 7, 8 and 25, which are not near the radio.
- Every other free pin (16–18, 20–24) is near the radio. u-blox: "below 10 kHz only".
- I2C to the fuel gauge runs at 100 kHz, but only for about 1 ms once a minute, timed between BLE events. The duty
  cycle is about 0.002 %, so I accept that, and it becomes a reviewer question.
- Built: I2C on EXP4 (SDA, pin 21) + EXP5 (SCL, pin 22), which keeps the analog-capable EXP1–3 free. CLKSEL on pin 23.
- The I2C bus is also brought out on the expansion pads, so add-on sensors share it.
- CLKSEL is static, so any free pin will do.
- NINA pin 31 (VBUS) with no USB: the u-blox documents on file don't say [verify].
  - Rev 0.7 leaves it unconnected, with a 0402 pad to GND left unfitted, so the reviewer's answer costs no respin.
  - It becomes a reviewer question.

**Pogo grid** (Harwin P70-1000045R × 12, 3 × 4 at 3.0 mm, 2.9 mm working height):
- P1–P8 = E1–E8, P9 = REF, P10 = BIAS;
- **P11 = CLK_SYNC, P12 = GND** (only used to link two pods).
- A strip without a link has no pads at P11/P12, so neither touches skin.

## 4. Mechanics
- **Board:** 24 × 30 mm, 6 layers, 1.6 mm, ENIG, parts on both sides. **Never made bigger without asking.**
  - 24 × 28 was checked and rejected. Cell 20 mm + screw-head clearance + the 4.3 mm cartridge-pad strip = exactly
    28 mm, with no room for the case's ±0.4 mm cartridge tolerance.
- **Thickness:** about 10.5 mm bare, about 12 mm in a thin case. Outside size about 25.6 × 31.6 × 12 mm in the case.
- **Battery cartridge** [owner: swappable, sold separately]:
  - **Not round.** A flat square 402020 LiPo pouch (20 × 20 × 4 mm, about 120 mAh, with protection circuit) plugs into a
    JST SH socket on a 0.6 mm thin board (24 × 25.6 mm).
  - That board is the pod's back cover.
  - Two tall spring pins (about 5.5 mm working height) press onto two gold pads on the pod. The pads are diagonal,
    2.9 mm apart, so + and − can never be bridged.
  - Keying chamfer.
  - Runtime about 17–20 h at 5–6 mA; requirement **≥ 14–18 h** [owner].
  - A swap restarts the pod (about 1 s plus a BLE reconnect); the flash buffer covers the gap.
  - EU 2023/1542 (user-replaceable batteries from 18 Feb 2027): met by the cartridge [verify].
- **Holding things on: magnets, smartwatch-style** [owner Oct 6–7, restored]:
  - Small N52 disc magnets in the printed case hold the cartridge, the worn flex strip and the pod on the dock.
  - Keyed, so nothing fits the wrong way round.
  - Keep magnets ≥ 5 mm from the antenna end.
  - The board's two NPTH holes double as locating posts for the case.
  - The 12 pogo pins push back about 12 × 0.5 N [verify from the Harwin sheet]. The magnet pair must beat that with
    margin (for example 2 × Ø4 × 2 mm N52), which is checked on the print.
- **Bench electrode tab** (v1 recording only):
  - Screws on with M2 nylon screws on 3.0 mm spacers.
  - Has an upright SMD header for the snap leads, all traces on its top layer.
  - Rev 0.7: the 2 × 5 electrode header stays, plus a **1 × 2 link header** (CLK, GND) above the grid, so two
    tabs can be linked with a short lead. A single 2 × 6 header was tried and did not route on one layer.
  - It stands about 21 mm off the pod; bench only. The worn strip adds about 3 mm.
- **Thinner pod (owner 2026-10-16, being checked):** shorter spring pins (about 2.5 mm free height) plus a 1.2 mm
  board would bring it from about 12 mm to about 11.0 mm in the case with a 1.2 mm FDM wall (10.6 mm with a 0.8 mm
  resin wall). Then the radio module (2.2 mm) plus the wall sets the skin-side height, not the pins.
  - **Lookup result, 2026-10-17 (research/jaw/lcsc-parts.md items 8–9):**
    - 1.2 mm 6-layer is offered at the same price ($48.70 for 5 boards), with the same rules.
    - Short pins exist: YIYUAN YTC1P-1807-01 (C42419351), 2.5 mm free / 2.0 working, 1 µin gold. Xinyangze
      YZ153915020R-01 (C5157371), 2.0 / 1.6, 3 µin gold.
    - Both have far thinner gold than the Harwin (0.4 µm ≈ 16 µin).
    - With a 1.2 mm PETG wall the radio module already sets the skin-side height (3.6 mm), above the Harwin tips
      (3.5 mm). So short pins save about 0 mm there, and only help with a 0.8 mm resin wall.
    - Recommendation: keep the Harwin pins, take the 1.2 mm board, giving about 11.0 mm (≈ 11.4 mm at 1.6 mm). The parts lookup (items 8–9) checks the parts
  and JLCPCB. Walls are **not** thinned: the owner worries how a thin wall holds up worn on skin all day.
- **Skin contact [owner concern]:** the pod gives off almost no heat (about 20 mW), so the skin warms the case, not the
  electronics.
  - Standard SLA resin is not skin-safe for all-day wear (uncured residue can irritate). Use PETG, a certified
    skin-contact resin, or a thin silicone sleeve on the skin face.
  - FDM wall at least 1.2 mm (3 perimeters at 0.4 mm). 0.8 mm only for resin.
- **Case:** FDM-printed (PETG for wear, PLA for fit tests).
  - Shaped to the head scan.
  - Thin wall at the antenna.
  - Magnet pockets, cartridge clip and alignment to about ±0.4 mm.
  - Not designed yet.

## 5. Charging: dock only (rev 0.7) [owner, Oct 16]
- **No charging on the pod at all.** Cells charge outside the pod, so a forgotten charge never stops you: swap
  cartridges.
- **Dock board (new):**
  - USB-C power-only receptacle (5.1 k CC pull-downs) → SMAJ5.0A TVS → MCP73831-2 (4.20 V).
  - R_PROG 15 k = about 67 mA (0.55 C for 120 mAh).
  - 4.7–10 µF in and out.
- **Contacts:** two pads in the **mirror image** of the pod's pads, so the cartridge's spring pins land on them when
  it lies face down on the dock. The magnets hold it.
- One cartridge per dock (a multi-bay dock later).
- **Dock charge LED:** included and fitted by default (D2 + R4). You can drop it from the dock BOM. The pod itself never lights.
- **EU common charger rule 2022/2380:**
  - It covers listed radio-equipment categories that charge over a wire. The pod charges no way at all, and the dock
    is not a radio device, so it most likely does not apply [verify].
  - Using USB-C on the dock satisfies it anyway.

## 6. Two pods together
- **Default, no wire:**
  - Each pod is its own BLE peripheral to the phone.
  - Each stamps every sample block with its own timer, and the phone maps both timers onto one clock using the shared
    BLE connection events.
  - It resamples the slow drift between the two ADS1298 internal oscillators.
  - Target alignment better than 1 sample (1 ms), which is plenty for speech EMG.
  - No cable behind the neck or under the chin.
- **Optional wired link** (bench now; worn later, if the two strips meet under the chin):
  - The master pod outputs its ADS clock on P11 (CONFIG1 CLK_EN).
  - The slave pulls CLKSEL low and runs off that clock.
  - P12 GND joins the two grounds, so both pods sample on the same clock with zero drift.
  - **START sync:** no extra pin. Both pods start on a BLE command, and the fixed whole-sample offset between them is
    removed from the timestamps. Why: no free pins, and with a shared clock the offset never changes.
- **Only one pod drives BIAS** when two are worn (the other has RLD powered down), so two bias amplifiers never fight.
- The phone also connects to the Halo, so 3 BLE links. The data rate is about 192 kbit/s raw per pod; 2 M PHY with long
  packets carries both.

## 7. Firmware rules
- **Power-up:**
  - PWDN/RESET sequence, then SDATAC, then registers.
  - CONFIG3: internal reference, RLDREF internal, RLD on (master only when two pods).
- **Rate:** 1000 SPS. Weak-link fallback, in order:
  1. lossless compression (about 2×);
  2. 500 SPS;
  3. BLE Coded PHY where the phone supports it.
  The app warns when the signal or an electrode is weak.
- **Battery:**
  - % from MAX17048, with BAT_SENSE as the fallback.
  - Warn and stop below 3.5 V (LDO dropout about 3.4 V).
- **Idle:** ADS powered down, slow advertising.
- **Swap:** buffer to flash, then reconnect and back-fill.
- **No LEDs.** Status, battery and recording all go to the app.

## 8. Phone and data [owner]
- **App:** iOS + Android. Receives 1–2 pods plus the Halo, decodes, and sends text to the glasses.
- **Heavy models:** run on the user's own rig (for example Mac Studios or a home server).
- **Data:** the owner's own recordings, plus a same-evening fine-tune loop.
- **Rules:** synthetic data never enters the eval sets; the hidden holdout stays hidden.

## 9. Before ordering (unchanged list, plus rev 0.7 items)
1. Rev 0.7 built and clean: DRC 0, unconnected 0, parity 0, ERC 0, net rules pass.
2. LCSC numbers for: pogo for the cartridge, the 2 × 5 and 1 × 2 SMD headers, bead, flash, MAX17048 (plus its pin
   table, to confirm U7), and the dock's 15 k, 1 k and LED. The parts lookup is queued.
3. Design review under NDA (Valectron → Boik → Upwork). Package rebuilt with `hw/pod/review.sh`; NDA annex hash
   84e4945f…52b8 (2026-10-17: part numbers filled, 1.2 mm board).
4. NINA-B306 stock (only about 38 at LCSC), ADS1298 price, CPL rotations in JLC's preview.
5. Case with magnets and the cartridge clip (needed to use the cartridge, not to order the boards).
