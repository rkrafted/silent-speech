# Will the behind-the-ear BLE pod stay connected? 2.4 GHz link study

Item: research/jaw/ble-link. Answers the question in `hw/pod/design-notes.md` §7: will a
behind-the-ear pod with a **NINA-B306** (nRF52840, internal PCB antenna, 0 dBm / +8 dBm) keep a
BLE link to a phone under hats, hoodies, coats and next to smart glasses?

**Short answer.** A 1 m link to a phone in a front pocket or hand has tens of dB of margin, even
with a hat and a coat. The links that fail are the ones where something conductive sits within a
few mm of the pod antenna (glasses temple, battery, metal zip, metallised/foil-dot lining) or
where the phone is in the **opposite back pocket** and the wearer is walking. Long-range
**LE Coded PHY** buys the most dB of any single fix, but many phones do not scan Coded
advertising, so it cannot be the only plan. Keep the pod antenna clear of metal, use +8 dBm, and
buffer on-pod flash.

All numbers below are quoted with a source tag `[S1]..[S16]` resolved at the end. Numbers marked
**(estimate)** are my arithmetic or inference, not a measurement.

---

## 0. What was checked first, and what this is not

- **Local tools:** `inventory` has no RF/link-budget tool (its search cannot run because it writes
  its vector cache outside the sandbox). No prior BLE-link research existed in the repo.
- **Repo finder:** `prior_art check` on this idea returned only weak/indirect overlaps (phone-body
  articles, unrelated repos). There is no reusable path-loss tool to build on, so this is a
  literature study plus an arithmetic link budget.
- **Open access only.** Every source was opened and its URL re-checked live by
  `check_sources.py` (16/16 verified). Paywalled IEEE papers were replaced by open versions
  (e.g. the ear-to-ear paper is on arXiv `[S9]`).
- **The strongest gap:** I could not open a peer-reviewed study that measures *dropout rate* of
  true-wireless earbuds or hearing aids, nor a study of a 2.4 GHz antenna **1 cm** from a
  smart-glasses temple. The closest direct measurement is a 2.4 GHz chip antenna next to an
  aluminium plate `[S14]`. Treat the detuning and coexistence numbers in §4 as the literature
  bound, and measure on the first boards.

---

## 1. On-body 2.4 GHz path loss: head/ear to waist, pockets, chest, hand

### 1.1 Body-surface (on-body) model

The IEEE 802.15.6 channel-model contribution `[S1]` fits `PL(d) = a*log10(d_mm) + b + N(0,σ)` to
measurements on a walking subject at 2.4 GHz:

| Environment | a | b | σ |
|---|---|---|---|
| Anechoic chamber | 29.3 | −16.8 | 6.89 dB |
| Hospital room | 6.60 | +36.1 | 3.80 dB |

The paper explicitly notes the path loss caused by the body "often reaches **25 dB**" in the
anechoic chamber and is "less than **10 dB**" in the hospital room, i.e. multipath fills the body
shadow. Its body-to-external (CM4) section measured the antenna gain toward the back drop by
**~20 dB** from body shadowing `[S1]`.

Plugging in the head-to-waist/pocket distances (body-surface nodes both on the body):

| Link | Distance | Median PL, room model `[S1]` | 90th pct (+1.28σ) | 99th pct (+2.33σ) |
|---|---|---|---|---|
| behind-ear → waist | 0.3 m | 52.4 dB | 57.3 dB | 61.3 dB |
| behind-ear → front pocket | 0.5 m | 53.9 dB | 58.8 dB | 62.8 dB |
| behind-ear → front pocket (anechoic, worst-case shadow) | 0.5 m | 62.3 dB | 71.1 dB | 78.4 dB |
| behind-ear → hand (arm down) | 0.8 m | 55.2 dB | 60.1 dB | 64.1 dB |

The anechoic row is the pessimistic head/ear-shadow case (σ 6.89 dB); the room rows are the
typical indoor case. **Head-only paths are expensive:** the ear-to-ear creeping-wave study `[S9]`
measured **79 dB** link loss on the heterogeneous Duke phantom and **49 / 64 / 71 / 75 dB** on the
SAM head as the shell and pinnae are made realistic; the pinnae alone add up to **13 dB** and head
size up to **10 dB**. Anything that forces the path over the head instead of around the jaw costs
tens of dB.

### 1.2 Moving (dynamic shadowing)

Cotton `[S2]` measured 2.45 GHz on-body links (front-left-waist to right-head, right-knee,
right-wrist) in an anechoic chamber while the subject walked, and off-body links during a 360°
rotation at 1.5 m and 4 m. A shadowed dominant component persists on every link; the wrist link
has the widest spread, and body rotation produces the deepest off-body fades. This is the
mechanism behind the "phone in the opposite back pocket" failure: the wearer's torso crosses the
LOS path once per stride or turn, not a constant loss. Design for the fade, not for the median.

The body-BAN thesis `[S11]` adds the reliability side: **RSSI ≥ −90 dBm corresponds to PRR ≥ 95 %**,
below −90 dBm the variance grows, and the body-area experiment adopts a conservative
**−85 dBm target**.

**Take-away:** median head-to-pocket on-body loss is ≈ 52–56 dB indoors; the 99th percentile is
≈ 61–64 dB; a forced over-the-head path can be 75–79 dB. Add phone-in-pocket body loading and
clothing on top.

---

## 2. Clothing and accessories at 2.4 GHz

| Item | What the sources support | Number |
|---|---|---|
| Wet fabric / sweat | Button sensor antenna measured wet: moisture shifts S11 and radiation efficiency `[S10]`; a flexible wearable antenna at 2.4 GHz was characterised specifically under bending and moisture loading `[S13]` | Detuning/degradation, not a clean dB; worst case can pull the antenna off resonance |
| Metallised / "foil dot" lining | Not directly measured in any open source I could open. A conductive lining next to the antenna is the same geometry as the aluminium-plate test in `[S14]` | **(estimate)** treat as metal at < 20 mm: several dB of mismatch loss, up to −10 dB S11, and a possible shield |
| Metal zip / buttons under the antenna | Same geometry as `[S14]` | **(estimate)** 3–10 dB depending on spacing |
| Cotton / wool / fleece / down / leather (dry) | No open peer-reviewed dB table found that isolates each fabric at 2.4 GHz. Dry textiles are mostly dielectric loading, not absorption | **(estimate)** 1–3 dB each layer over the antenna; a thick coat adds a few dB of absorption/scattering |
| Knit hat directly over the antenna | Dielectric loading plus trapped moisture; `[S13]` shows moisture is the dominant effect | **(estimate)** 2–5 dB dry, worse when wet |
| Hood / collar between pod and phone | Same body-shadow mechanism as §1 | **(estimate)** 3–10 dB |

**Honest gap:** the clothing question deserves a bench measurement (wear the pod under each
garment and log RSSI), because the open literature measures body and moisture, not down vs
fleece. The safe design rule is: **never put a conductive layer (foil-dot lining, metal zip,
metallised membrane) within ~2 cm of the pod antenna**, and keep the knit hat from sitting
directly on the antenna face. Both are layout/appearance decisions, not firmware fixes.

---

## 3. Real devices

### 3.1 NINA-B306 / nRF52840

| Parameter | Value | Source |
|---|---|---|
| Chip | nRF52840 | `[S4]` |
| Conducted TX | +8 dBm typical (NINA-B306); EIRP +10 dBm | `[S3]`, `[S4]` |
| RX sensitivity, 1 Mbit/s | −94 dBm (module); nRF52840 chip −95 dBm | `[S3]`, `[S12]` |
| RX sensitivity, Coded (long range) | −100 dBm (module); nRF52840 chip −103 dBm | `[S3]`, `[S12]` |
| Max throughput (marketing) | 1.4 Mbit/s | `[S3]`, `[S4]` |
| Supported rates | 1 Mbps, 2 Mbps, Coded 500 kbps (S=2), Coded 125 kbps (S=8) | `[S3]` |

### 3.2 Arduino Nano 33 BLE (same NINA-B306 module) — real RSSI/range reports

`[S5]` is the most useful field data for our exact module:

- several boards were detected only **< 2 m** and reliable at **~1 m**;
- the root cause was **two missing components in the NINA-B306 antenna matching network**;
- one *good* board reached **40 m line-of-sight outdoors** (phone in hand, 1.5 m high, walking) but
  dropped values, and another reached only **~4–5 m**;
- `[S6]` adds host-radio dependence: **45–50 cm** to a laptop's built-in Bluetooth card vs **> 5 m**
  to a phone vs **7–8 m** after a USB adapter swap, with the case still on.

**Implication:** the range spread between individual boards is huge and is set by antenna matching
and ground plane, not by the module part number. Check the first boards' RSSI, and add the
matching-network inspection to the bring-up checklist.

### 3.3 Hearing aids and true-wireless earbuds

The open source I could open is the binaural-hearing-aid propagation model `[S9]`, which shows the
ear-to-ear link spends 49–79 dB and is dominated by head size, pinna and the creeping path. The
"phone in the opposite back pocket" problem is the **off-body** counterpart of the same body
shadow, measured as rotation fades in `[S2]`.

**Honest gap:** no open, measured earbud/hearing-aid **dropout rate** (packets lost per minute as a
function of pocket) was found. Do not quote one. The first prototype should log RSSI and packet
loss while the wearer walks with the phone in each pocket; that measurement is the real answer.

---

## 4. Metal near the antenna, and two BLE links to one phone

### 4.1 Detuning by a nearby metal object

`[S14]` is the closest open measurement to our case. A commercial 2.4 GHz chip antenna next to a
parallel aluminium plate:

- **S11 degrades to −10 dB at 20–30 mm** and **−5 dB at 15 mm** separation;
- a purpose-built shorted microstrip antenna kept **average mismatch loss better than −11 dB S11
  and under 0.4 dB mismatch** up to 20 mm, and reached **PER 1e-5 at ~60 dB** propagation loss over
  a 50 cm link.

u-blox's integration manual `[S15]` asks for the module at the centre of a board edge, **≥ 10 mm of
ground plane on both sides**, the ground cut out under the antenna, the four EAGP pads grounded,
and **10 mm clearance to the case and to metal parts**. The design notes already record that a
30 × 20 × 10 mm pod cannot meet the 10 mm rule.

**Estimate for a smart-glasses temple or battery ~1 cm from the pod:** the small PCB antenna sees
several dB of mismatch plus a possible frequency shift; budget **3–6 dB** extra loss and expect the
2.4 GHz resonance to move. This is the single most important thing to measure on hardware, because
a shifted resonance can cost far more than 6 dB at the band edges.

### 4.2 Two 2.4 GHz links to one phone (pod + earbuds/glasses)

The phone has one 2.4 GHz radio that time-shares the connections; coexistence is handled by the
link layer (37 channels, adaptive frequency hopping, scheduling) and there is **no open measured
number I could verify** for the pod's throughput loss when a second link is active. `[S12]` ran its
BLE 5 tests "with interference testbed", and `[S16]` defines the channel/PHY rules. Treat this as a
**latency/retry risk**, not a coverage risk: the pod can lose airtime and see retries, so buffer on
the pod rather than stream live. A 2-link bench test (pod + earbuds connected, walk around) is the
next measurement.

---

## 5. Phone side

### 5.1 Receiver sensitivity

`[S8]` measures one current combo module at PER < 30.2 %:

| PHY | Sensitivity |
|---|---|
| LE Coded S=8 (125 kbit/s) | **−104 dBm** |
| LE Coded S=2 (500 kbit/s) | **−101.4 dBm** |
| LE 1M (37-byte) | **−97.5 dBm** |
| LE 1M (255-byte) | −96.5 dBm |
| LE 2M | **−95.4 dBm** |

The nRF52840 (and therefore the NINA-B306) is −95 dBm at 1M and −103 dBm at Coded `[S12]`. Phone
RX varies by model; the measured module above is a fair "good phone" anchor. For a conservative
plan, assume a phone RX of **−90 dBm** and verify the actual handset; two phones are never equal.

### 5.2 Which phones support LE Coded PHY

`[S7]` is the live community list from Nordic and Android developers:

- **reported working** for Coded-primary scanning/advertising: Samsung Galaxy S10 and newer, S21,
  Galaxy Tab A7, OnePlus 7 and newer, Xiaomi Poco X3 NFC, Samsung M51;
- **reported not working**: Google Pixel (no Coded-primary scan), Samsung Galaxy A32 5G, some
  OnePlus 6/6T units;
- Android's API only offers scanning on **1M** or **1M + LE_Coded**, not Coded-only.

So Coded PHY is a **per-phone** capability. The pod must advertise on 1M (so any phone can find
and connect it) and then negotiate Coded for the data phase if the phone supports it.

### 5.3 Throughput with 7.5–15 ms connection intervals

`[S12]` measured nRF52840 links with connection intervals of **7.5, 50 and 400 ms** and ATT MTUs
of 23, 158 and 247 bytes. Over **LE 2M**, 50 ms interval and 247-byte MTU, throughput fell from
**992.5 kbit/s at 0 m to 128.9 kbit/s at 100 m**. The highest throughput was at 7.5 ms with
247-byte MTU; larger intervals lose throughput once bit errors appear. Over LE 1M expect roughly
half those rates (2M doubles the symbol rate), and over Coded S=8 roughly one eighth; u-blox quotes
a 1.4 Mbit/s marketing maximum `[S3]`.

**(estimate)** for a 7.5–15 ms interval, 1M PHY, DLE and a strong link: a few hundred kbit/s to
≈1 Mbit/s at 7.5 ms, and roughly 100–400 kbit/s at 15 ms; Coded S=2 is ≈1/2 of 1M and S=8 ≈1/8.
That is still thousands of times more than a silent-speech pod needs, so **throughput is not the
bottleneck**; coverage and latency are.

---

## 6. Link budget for our case

**Assumptions.** NINA-B306 with internal PCB antenna, antenna gain ≈ **+2 dBi** (EIRP +10 dBm at
+8 dBm conducted `[S3]`); phone antenna gain **0 dBi**; free-space loss
`32.45 + 20log10(2450) + 20log10(d_m/1000)`. The excess-loss column is an **(estimate)** anchored
to the cited medians: body/head shadow `[S1][S2][S9]`, clothing/hat `[S10][S13]`, metal detuning
`[S14]`, coexistence `[S12][S16]`.

| Scenario | d | FSPL | body/head | clothing+hat | metal/coexist | Total PL | RX at +8 dBm | RX at 0 dBm |
|---|---|---|---|---|---|---|---|---|
| **Best** — pod on ear, phone in hand/front chest, standing, t-shirt | 0.5 m | 34.2 | 8 | 1 | 0 | **43.2** | −33.2 | −41.2 |
| **Typical** — front trouser pocket, light jacket, walking | 1.0 m | 40.2 | 15 | 3 | 4 | **62.2** | −52.2 | −60.2 |
| **Worst** — opposite back pocket, knit hat + foil-lined coat + glasses 1 cm, walking | 1.0 m | 40.2 | 28 | 11 | 8 | **87.2** | −77.2 | −85.2 |

Margins vs the phone receiver, using `[S8]` and the conservative −90 dBm phone:

| Scenario / TX | 1M (−97.5) | Coded S=2 (−101.4) | Coded S=8 (−104) | vs conservative −90 dBm |
|---|---|---|---|---|
| Best, +8 dBm | 64.3 | 68.2 | 70.8 | 56.8 |
| Best, 0 dBm | 56.3 | 60.2 | 62.8 | 48.8 |
| Typical, +8 dBm | 45.3 | 49.2 | 51.8 | 37.8 |
| Typical, 0 dBm | 37.3 | 41.2 | 43.8 | 29.8 |
| Worst, +8 dBm | 20.3 | 24.2 | 26.8 | 12.8 |
| Worst, 0 dBm | 12.3 | 16.2 | 18.8 | **4.8** |

Reverse path (phone → pod) uses the module RX (−94 dBm at 1M, −100 dBm Coded `[S3]`). With a phone
at +4 dBm and the worst-case 87.2 dB loss, the 1M margin is ≈ 11 dB and the 0 dBm phone case
≈ 7 dB. **The return path is the tighter one when the phone is deep in a pocket.**

**What fails first (ranked):**

1. **A conductive layer over the antenna** — metallised/foil-dot lining, metal zip, wet knit hat.
   This can detune the antenna out of band, so the static "a few dB" understates it and the link
   can drop entirely.
2. **Metal at ~1 cm** (glasses temple, battery, earring) — S11 can fall to −5…−10 dB `[S14]`;
   budget 3–6 dB and check the band edge.
3. **Walking with the phone in the opposite back pocket** — the torso fade `[S2]` plus a poor phone
   RX (−90 dBm) can consume the 12 dB worst-case 1M margin. This is the scenario to log.
4. **0 dBm TX.** At 0 dBm the worst-case 1M margin is 12 dB (phone RX) / ~7 dB (return). +8 dBm
   buys 8 dB for 9 mA extra (4.9 → 14.1 mA `[S3]`).
5. **Coexistence** with earbuds/glasses — retries and latency, not coverage.

What does **not** fail: typical front-pocket use. Even the conservative 0 dBm case has ~30 dB
margin there.

---

## 7. Ranked fixes (highest gain first)

| # | Fix | Supported gain | Cost / caveat |
|---|---|---|---|
| 1 | **Antenna placement and ground plane** — module at a board edge, ≥ 10 mm ground both sides, cut-out under the antenna, EAGP grounded `[S15]`; keep the lens/battery/metal away from the antenna face | Avoids 3–10 dB of detuning `[S14]`; turns the 1–40 m board spread `[S5]` into a known value | Mechanical: the pod is small, so this is the hardest fix; measure S11/RSSI on rev 1 |
| 2 | **Run +8 dBm, not 0 dBm** | +8 dB `[S3]` | 4.9 → 14.1 mA on TX `[S3]`; keep 0 dBm as the low-battery fallback |
| 3 | **Negotiate LE Coded PHY** (advertise on 1M, switch data to Coded S=2/S=8) | +4 dB (S=2) to +6.5 dB (S=8) vs 1M `[S8]`, roughly 2–4× range `[S12][S16]` | Phone support is per-model and cannot be assumed `[S7]`; Coded costs airtime and throughput |
| 4 | **Buffer on the pod + on-pod flash** | Removes data loss during 100–500 ms walking fades `[S2]`; 1 MB flash ≈ minutes of a low-rate bio signal | Adds BOM and firmware complexity; this is the reliability backstop when 1–3 cannot be achieved |
| 5 | **Adaptive data rate + compression + phone-placement guidance** | Compression cuts airtime and thus loss exposure; user guidance (same-side pocket/hand) avoids the 10–28 dB opposite-pocket penalty `[S2]` | Needs a user-facing hint and a link-quality controller; use RSSI −85…−90 dBm as the trigger `[S11]` |

Antenna placement and the glasses clearance are **hardware rev 1 decisions**; PHY, TX power,
buffering and compression are firmware and can be added later.

---

## Sources

| Tag | Source |
|---|---|
| S1 | IEEE P802.15-08-0416-04-0006, *Channel models for wearable and implantable WBANs* (Aoyagi, 2008). https://mentor.ieee.org/802.15/dcn/08/15-08-0416-04-0006-channel-models-for-wearable-and-implantable-wbans.pdf |
| S2 | S. L. Cotton, *A Statistical Model for Shadowed Body-Centric Communications Channels*, IEEE TAP 2014. https://pureadmin.qub.ac.uk/ws/files/17981408/a_statistical_model.pdf |
| S3 | u-blox, *NINA-B3 series data sheet* UBX-17052099. https://www.u-blox.com/sites/default/files/NINA-B3_DataSheet_UBX-17052099.pdf |
| S4 | u-blox, *NINA-B30 series product page*. https://www.u-blox.com/en/product/nina-b30-series-open-cpu-0 |
| S5 | Arduino forum, *BLE very weak signal* (Nano 33 BLE). https://forum.arduino.cc/t/ble-very-weak-signal/631751 |
| S6 | Arduino forum, *Distance bluetooth range Arduino Nano 33 BLE*. https://forum.arduino.cc/t/distance-bluetooth-range-arduino-nano-33-ble/1156765 |
| S7 | nordicsemi/Android-BLE-Library issue #166, *List of Coded PHY Supported/Tested Phones*. https://github.com/nordicsemi/Android-BLE-Library/issues/166 |
| S8 | BDE Technology, *Bluetooth LE Performance: Receiver Characteristics* (BDE-BW3551P1). https://www.bdecomm.com/uploads/resource/bde-bw3551p1_html/bde-bw3551p1_html/topics/bluetooth_le_performance_receiver_characteristics.html |
| S9 | R. Chandra, A. J. Johansson, *A Link Loss Model for the On-body Propagation Channel for Binaural Hearing Aids* (arXiv:1304.1739, 2013). https://arxiv.org/abs/1304.1739 |
| S10 | S. M. Ali et al., *Design and Evaluation of a Button Sensor Antenna…*, Micromachines 2022. http://eprints.gla.ac.uk/267765/1/267765.pdf |
| S11 | UNSW thesis, *Link quality estimation and transmit power control for wireless body area networks*. https://unsworks.unsw.edu.au/bitstreams/c3303e33-c830-427c-bfc8-8b38621d9fca/download |
| S12 | *Bluetooth 5 performance analysis for inter-vehicular communications*, Wireless Networks 2022 (Zenodo). https://zenodo.org/records/10578188 |
| S13 | *Bend and Moisture Effects … U-Shaped Slotted Wearable Antenna … 2.4 GHz*, Sensors 2019 (PubMed 30991753). https://pubmed.ncbi.nlm.nih.gov/30991753/ |
| S14 | N. Nakamoto et al., *Radio propagation and antenna design for 2.4 GHz wireless harness inside ICT equipment*, ICACT 2013. http://icact.org/upload/2013/0034/20130034_finalpaper.pdf |
| S15 | u-blox, *NINA-B3 series system integration manual* UBX-17056748. https://www.u-blox.com/en/docs/UBX-17056748 |
| S16 | Bluetooth SIG, *Bluetooth Core Specification 6.0*. https://www.bluetooth.com/specifications/specs/core-specification-6-0/ |

Machine-readable version: `research/jaw/sources-ble.jsonl`.

## What to measure on rev 1 (next steps)

1. S11 of the pod antenna in free space, on a head phantom, and 10 mm from a metal plate / glasses
   temple (target: no worse than −6 dB across 2.40–2.48 GHz).
2. RSSI + packet-loss log while walking, phone in: hand, front pocket, same-side back pocket,
   opposite back pocket, under a coat, under a knit hat.
3. Two-link test: pod + earbuds connected to one phone, log retries/latency.
4. Confirm which test phones actually support Coded-primary scan/advertise `[S7]` before relying
   on Coded for the data phase.
