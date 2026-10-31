# Silent-speech patents for a hidden jaw wearable

Sweep of CN, US, KR, JP, EP/DE/WO patents and applications on silent / subvocal speech
sensed at the face, jaw, chin, submental, cheek, neck, throat, behind-ear and ear-canal
sites, plus the inventors' papers, code and datasets.

**Method.** Queried Google Patents (search XHR), then pulled full records from the
Lens.org public patent pages (title, applicants, inventors, priority, legal status,
family, abstract and — where Lens holds it — claims/description). Inventors were then
traced through the professional literature via OpenAlex, PubMed E-utilities and GitHub.
Everything in `sources-patents.jsonl` was opened live; `check_sources.py` verifies it.

**Honest limits.**
* Google Patents started returning HTTP 503 part-way through (IP-burst throttle, shared
  with the sibling sessions of this series). Lens.org served 45 of 61 candidates in full;
  the rest are US/WO *applications* that Lens does not serve (`US_2024…_A1` → 400). They
  are listed in "still to fetch" at the end and are **not** in the sources file.
* Lens does not hold claims or description for CN/DE/JP/KR records, so for those the
  claimed sites below come from the machine-translated abstract and title, not the claims.
  Where a field is unknown it says "not in the fetched record".
* Status and term dates are Lens's legal-status fields as of this session.

**This is not legal advice.** The "watch out" section reports what the claims say, nothing
about infringement, validity or freedom to operate.

---

## (a) Top 10 ideas to use for a hidden jaw device

1. **Train on a high-density array, deploy on a few discrete dry electrodes, and put the
   transfer learning in the middle.** USTC's granted `CN113288183B` builds a source-domain
   network from a high-density sEMG image set and a target-domain network from a
   channel-sparse set, then calibrates with transfer learning and claims robustness to
   electrode shift and cross-user variation. This is exactly the "calibrate once, wear
   something small" architecture we need. Source: `CN113288183B` (USTC, 2021).
2. **Use a Transformer decoder, not a CNN.** The same USTC group's `CN114863912A` replaces
   the classifier with a Transformer decoding network for silent sEMG. For a small command
   vocabulary with long-range temporal structure this is the cheapest accuracy win.
   Source: `CN114863912A` (USTC, 2022).
3. **Augment the tiny corpus with back-translation.** The Chinese defence lab's
   `CN114822541A` feeds silent sEMG features into an SAEM model and uses back-translation
   to expand/regularise. Our one-user dataset will be small; this is a concrete recipe.
   Source: `CN114822541A` (National Defense Science and Technology Innovation Institute,
   2022).
4. **Pretrain self-supervised, then fine-tune on the user.** `emg2speech` synthesises
   speech from orofacial EMG with self-supervised learning and releases code; this directly
   attacks the labelled-data bottleneck. Sources: Gowda, Comstock & Miller, ACL 2026;
   `https://github.com/HarshavardhanaTG/emg2speech`.
5. **Copy a published electrode-placement practice before buying an amplifier.** Meltzner
   et al. 2018 is the clearest sEMG-sensor-and-algorithm paper for silent speech, and Zhu
   et al. 2020 searched electrode configurations for silent speech and reports which
   placements carry the information. Sources: PMID 29855428; PMID 33181497.
6. **Keep the sensor count small — extra modalities were tried and dropped.** The Tianjin
   and defence-lab silent-speech applications that added a lip camera, vocal-cord vibration
   or oral ultrasound are all `DISCONTINUED` (`CN111723717A`, `CN113887339A`,
   `CN111899713A`). Pure sEMG is the lean, surviving route. Source: same three records.
7. **Add one hidden non-EMG channel in the earbud for gating/features.** Ear-canal
   deformation is informative enough for machine learning (CochlearMotion 2025), and Apple
   already claims an in-ear accelerometer for bone-conduction ASR triggering
   (`US11683632B2`). Use a deformation/IMU channel for onset detection, and avoid claiming
   the Apple trigger combination. Sources: CochlearMotion 2025; `US11683632B2`.
8. **Let an LLM clean up the decoder.** Mohapatra et al. 2025 test EMG-to-text conversion
   with an LLM; this is the cheapest route from noisy personal EMG to usable text.
   Source: ACL 2025 short paper.
9. **Design the electrode patch as a flexible layered dry patch.** Soochow's
   `CN109745045A` stacks a flexible substrate, insulating layer, flexible electrode layer
   with probe/interconnect geometry and a second insulator — and it is `DISCONTINUED`, so
   the geometry itself is free to reuse. For softness, the Rogers-group conformal
   mechano-acoustic platform (`US11154232B2`) is the reference. Sources: `CN109745045A`;
   `US11154232B2`.
10. **Frame it as voice restoration, not augmentation.** The clinical sEMG silent-speech
    claim (`US12505842B2`, Cornell) and the laryngectomy restoration study (PMID 42694022)
    show the credible use case and give a validation protocol. Sources: `US12505842B2`;
    PMID 42694022.

---

## (b) Design dead-ends others already hit

| Dead-end | Who tried it | Evidence |
|---|---|---|
| Injecting artificial excitation into the vocal tract | Tosaya/Sliwa, `US7082395B2` (priority 1999) | Now **EXPIRED** (term 2021-03-04); never became a product. Hardware-heavy. |
| Magnetic tracer on the tongue + sensor array around the mouth | Georgia Tech, `US8242880B2` and `US9911358B2` | Both **INACTIVE**. Works (sub-mm), but needs an intraoral tracer — not hidden, not for a jaw patch. |
| Fusing sEMG with a lip camera | Tianjin, `CN113887339A`; defence lab, `CN111899713A` | Both **DISCONTINUED**; camera needs line of sight, occlusion and privacy problems. Cornell's camera route (`US12400473B2`) is a different owner but same exposure. |
| Adding vocal-cord vibration to facial EMG | Tianjin, `CN111723717A` | **DISCONTINUED** — the two-sensor combination was dropped. |
| Oral-cavity ultrasound probe for silent speech | Defence lab, `CN111899713A` | **DISCONTINUED**; an intraoral probe cannot be hidden and is uncomfortable. |
| Kitchen-sink multimodal fusion (EEG + EMG + lip + eye + physiology) | Defence lab, `CN111190484B` | Claim is **ACTIVE** but the approach is heavy; its discontinued siblings suggest the fusion did not deliver. |
| Optical facial-micromovement decoding | Q (Cue) Ltd, `US12154572B2` | **ACTIVE** and acquired by Apple, but camera/lighting/occlusion dependent and needs the face visible. |
| In-ear microphone for command input | Qualcomm, `US10678502B2` | **ACTIVE**, but it is acoustic, not silent — no occlusion-free silent channel. |
| Cross-user generic EMG model with no calibration | Meta/CTRL-labs parent claims (`US11216069B2` etc.) | Claims require a trained model but the wearable still needs per-user data; generic transfer alone is not the answer for one user. |

---

## (c) All patents read (35)

Status/term are Lens legal-status fields. "Sites" are as stated in the fetched
abstract/claims; "not in record" means Lens holds no claims/description for that record.

| # | Patent | Owner | Form factor | Claimed sites / sensor | Status (term) | Link |
|---|---|---|---|---|---|---|
| 1 | US10621973B1 | Vocasso Inc | headset over the ear | chin, neck, behind the ear; EMG electrodes + chin IMU | ACTIVE 2038-07-06 | https://www.lens.org/lens/patent/US_10621973_B1 |
| 2 | US8082149B2 | Biosensic LLC (Schultz, Waibel) | not in record | ≥1 electrode, myoelectric signal → speech | ACTIVE 2030-07-19 | https://www.lens.org/lens/patent/US_8082149_B2 |
| 3 | US12505842B2 | Cornell University | cutaneous sensor unit | chin, neck, face; articulatory sEMG, silent speech | ACTIVE 2041-03-16 | https://www.lens.org/lens/patent/US_12505842_B2 |
| 4 | US12400473B2 | Cornell University | head- or neck-mounted | chin, cheek, neck, face; camera or acoustic skin-deformation | ACTIVE 2042-01-30 | https://www.lens.org/lens/patent/US_12400473_B2 |
| 5 | US11216069B2 | Meta / Facebook Tech | wearable(s) | neuromuscular sensors + audio → text | ACTIVE 2038-05-08 | https://www.lens.org/lens/patent/US_11216069_B2 |
| 6 | US11036302B1 | Meta / Facebook Tech | wearable device | neuromuscular sensors + trained model → text | ACTIVE 2038-05-08 | https://www.lens.org/lens/patent/US_11036302_B1 |
| 7 | US12579768B2 | Meta Platforms Tech | wearable / XR | neuromuscular sensors (wrist embodiment) → text/XR | ACTIVE 2039-11-15 | https://www.lens.org/lens/patent/US_12579768_B2 |
| 8 | US12154572B2 | Q (Cue) Ltd | camera-based | facial skin micromovements, pre-vocalisation | ACTIVE 2043-07-19 | https://www.lens.org/lens/patent/US_12154572_B2 |
| 9 | US12482449B2 | Wispr AI Inc | wearable speech input | speech-muscle activation patterns, incl. EMG | ACTIVE 2044-03-24 | https://www.lens.org/lens/patent/US_12482449_B2 |
| 10 | US10678502B2 | Qualcomm | in-ear device | in-ear microphone, speech recognition | ACTIVE 2037-11-13 | https://www.lens.org/lens/patent/US_10678502_B2 |
| 11 | US11683632B2 | Apple Inc | ear canal | microphone + ear-canal accelerometer (bone conduction) | ACTIVE 2037-05-04 | https://www.lens.org/lens/patent/US_11683632_B2 |
| 12 | US9779758B2 | Google Inc | head-mountable | microphone + head vibration/motion sensor | ACTIVE 2032-07-26 | https://www.lens.org/lens/patent/US_9779758_B2 |
| 13 | US10679644B2 | IBM | multi-sensor | multiple sensors, whispered/silent speech → amplified speech | ACTIVE 2037-12-19 | https://www.lens.org/lens/patent/US_10679644_B2 |
| 14 | US11397799B2 | Ericsson | device | subvocalised melody → authentication | ACTIVE 2038-12-27 | https://www.lens.org/lens/patent/US_11397799_B2 |
| 15 | US11154232B2 | Univ Colorado / Illinois | soft conformal skin patch | mechano-acoustic + electrophysiology, any skin site | ACTIVE 2039-03-04 | https://www.lens.org/lens/patent/US_11154232_B2 |
| 16 | US8242880B2 | Georgia Tech | intraoral | magnetic tracer on tongue, sensor near mouth | INACTIVE 2030-02-03 | https://www.lens.org/lens/patent/US_8242880_B2 |
| 17 | US9911358B2 | Georgia Tech | intraoral | tongue tracer + magnetic sensor array, silent speech interface | INACTIVE 2035-03-15 | https://www.lens.org/lens/patent/US_9911358_B2 |
| 18 | US7082395B2 | Tosaya / Sliwa | vocal-tract excitation | chin, oral, ear; injected excitation for inaudible speech | EXPIRED 2021-03-04 | https://www.lens.org/lens/patent/US_7082395_B2 |
| 19 | CN113288183B | USTC | high-density + discrete electrodes | facial–neck surface EMG, transfer learning | ACTIVE 2041-05-20 | https://www.lens.org/lens/patent/CN_113288183_B |
| 20 | CN114863912A | USTC | surface electrodes | sEMG silent voice, Transformer decoder | ACTIVE 2042-05-05 | https://www.lens.org/lens/patent/CN_114863912_A |
| 21 | CN114822541A | Nat. Defense Sci-Tech Innovation Inst. | surface electrodes | silent sEMG + SAEM model + back-translation | ACTIVE 2042-04-25 | https://www.lens.org/lens/patent/CN_114822541_A |
| 22 | CN112151030B | Nat. Defense Sci-Tech Innovation Inst. | multimodal | lip image + facial EMG + audio | ACTIVE 2040-09-07 | https://www.lens.org/lens/patent/CN_112151030_B |
| 23 | CN111190484B | Nat. Defense Sci-Tech Inst. + Tianjin AI | multimodal | EEG + EMG + lip + eye + physiology | ACTIVE 2039-12-25 | https://www.lens.org/lens/patent/CN_111190484_B |
| 24 | CN111899713A | Nat. Defense Sci-Tech Innovation Inst. | multimodal | facial EMG + lip image + oral ultrasound | DISCONTINUED | https://www.lens.org/lens/patent/CN_111899713_A |
| 25 | CN113887339A | Tianjin University | sEMG + camera | sEMG fused with lip image | DISCONTINUED | https://www.lens.org/lens/patent/CN_113887339_A |
| 26 | CN111723717A | Tianjin University | sEMG + vibration | facial EMG + vocal-cord vibration | DISCONTINUED | https://www.lens.org/lens/patent/CN_111723717_A |
| 27 | CN109745045A | Soochow University | flexible electrode patch | layered flexible myoelectric patch | DISCONTINUED | https://www.lens.org/lens/patent/CN_109745045_A |
| 28 | CN110996782B | Bose Corp | in-ear | ≥2 in-ear electrodes, action affects signal | ACTIVE 2038-06-26 | https://www.lens.org/lens/patent/CN_110996782_B |
| 29 | CN112424859B | Meta (CN) | wearable(s) | neuromuscular sensors + audio → text | ACTIVE 2039-05-07 | https://www.lens.org/lens/patent/CN_112424859_B |
| 30 | CN115705841A | STMicroelectronics | accelerometer | bone-conduction accelerometer, no microphone | PENDING | https://www.lens.org/lens/patent/CN_115705841_A |
| 31 | JP7149492B2 | Control Bionics Ltd | EMG device | EMG-assisted communication, context UI | ACTIVE 2038-11-16 | https://www.lens.org/lens/patent/JP_7149492_B2 |
| 32 | KR20250142168A | ETRI (Korea) | attachable optical sensor | optical-fibre lattice sensor for silent communication | PENDING | https://www.lens.org/lens/patent/KR_20250142168_A |
| 33 | KR102270653B1 | Inha University | head/neck sensor unit | articulatory physical properties incl. oral-tongue sensor | ACTIVE 2038-09-27 | https://www.lens.org/lens/patent/KR_102270653_B1 |
| 34 | DE102020110901B4 | Altavo GmbH | vocal-tract sensing | patient vocal-tract signal + healthy speech → artificial voice | ACTIVE 2040-04-23 | https://www.lens.org/lens/patent/DE_102020110901_B4 |
| 35 | JP6960189B2 | Suzhou Yichuan Electronic Tech | vocalisation device | mouth/throat vocaliser hardware | ACTIVE 2038-11-23 | https://www.lens.org/lens/patent/JP_6960189_B2 |

### What changed between family members (design evolution)

* **Biosensic / Schultz `US8082149B2`** — 45-member family. The US line continues as
  `US11222185B2` and `US11972227B2`, i.e. the same "electrode + myoelectric speech
  processing" idea was kept alive for well over a decade. Europe split into
  `EP2274742A1` → `EP2548201A1` → `EP2849178A2/A3`; national grants
  `CN102084417B`, `JP6345638B2`, `KR101445904B1`. Lesson: the foundational claim was
  re-filed repeatedly, so the early priority date does not make the space free.
* **Meta neuromuscular speech `US11216069B2` / `US11036302B1`** — a 182-member extended
  family. `US12579768B2` (2026 grant) is the XR continuation, and `CN112424859B` is the
  Chinese grant of the same claim. Same claim text, multiple jurisdictions.
* **Apple `US11683632B2`** — three US grants in sequence: `US10313782B2` →
  `US11102568B2` → `US11683632B2`. The ear-canal accelerometer trigger was narrowed/reissued
  rather than replaced, so an earbud accelerometer must be checked against all three.
* **Google `US9779758B2`** — `US9135915B1` first, then `US9779758B2`, same head-mounted
  vibration-gating idea.
* **IBM `US10679644B2`** — sibling `US10529355B2` plus applications
  `US20190189145A1`/`US20190371356A1`; the multi-sensor silent/whispered claim was filed
  twice.
* **Cornell facial tracking `US12400473B2`** — `EP4150520A1`/`B1` and the US chain
  `US20230077010A1` → `US20240212388A1` → `US20250060782A1`, i.e. the expression-tracking
  disclosure spawned several continuations after the first grant.
* **Wispr AI `US12482449B2`** — family includes `US12105876B2`, `US12374317B2`,
  `US12482449B2` and roughly a dozen `US2024…` applications (including the ones Lens would
  not serve). One specification, many claims: silent speech, gestures and user interaction.
* **Q (Cue) `US12154572B2`** — 101 family members across AU/CA/CN/EP, so the micromovement
  approach is protected very broadly despite being camera-based.
* **STMicroelectronics `CN115705841A`** — same disclosure as `EP4131256A1`,
  `US20230045064A1` and grant `US12603087B2`; accelerometer-only bone-conduction speech.
* **Control Bionics `JP7149492B2`** — AU applications `AU2018367613A1/B2` and
  `AU2022268375A1/B2`, plus US `US11284844B2` → `US12455623B2` → `US20260178124A1`.
  Continuations grow the UI/context claims, not the sensor.
* **ETRI `KR20250142168A`** — `JP2025146625A`, granted `JP7714768B1` and
  `US20250299677A1`; Korea, Japan and the US covered for the optical-fibre sensor.
* **Altavo `DE102020110901B4`** — `DE…A1` → `B4` → `B8`, plus `EP4139917A1/B1`,
  `US20230154450A1` and `WO2021214065A1`.
* **Inha University `KR102270653B1`** — a 34-member Korean family (`KR102152775B1`,
  `KR102174188B1`, `KR102180331B1`, …); the lab protected many articulatory-sensing
  variations.
* **Georgia Tech** — `US20090309747A1` → `US8242880B2` (tongue magnetic) and
  `US20140342324A1` → `US9911358B2` (wireless tongue tracking + silent speech interface).
  Both now INACTIVE.
* **USTC** — `CN113288183A` → `CN113288183B` and `CN114863912A` → `CN114863912B`; the
  transfer-learning and Transformer variants were both granted.

---

## (d) Watch-out list — active claims close to a jaw/ear EMG wearable

**Not legal advice.** These are summaries of what the claims/abstracts state, to decide what
to read with a patent attorney. The full claims for US/EP records are in the Lens page
linked in the table; CN/JP/KR claim text was not in the fetched record.

| Patent | Why it is close | What the claim actually says |
|---|---|---|
| `US12482449B2` (Wispr AI) | **Closest.** A wearable that reads speech-muscle activation patterns incl. EMG. | "a speech input device wearable on a user and configured to receive an electronic signal indicative of a user's speech muscle activation patterns … the electronic signal may include EMG data". |
| `US12505842B2` (Cornell) | **Closest.** Cutaneous sEMG of articulatory muscles for silent speech. | Personal device with a cutaneous sensor unit detecting surface EMG from articulatory muscles for recognition of silent speech in a patient. |
| `US10621973B1` (Vocasso) | **Direct.** The exact chin + neck EMG + jaw IMU combination. | "a chin electrode … a neck electrode … a chin Inertial Measurement Unit … in a position over the neck, under the chin and behind the ear". |
| `US8082149B2` + `US11222185B2` + `US11972227B2` (Biosensic/Schultz) | **Foundational and broad.** At least one electrode reading a myoelectric speech signal. | "capturing a myoelectric signal from a user using at least one electrode … amplifying … filtering … converting … into a digital signal". |
| `US11216069B2`, `US11036302B1`, `US12579768B2` (Meta) and `CN112424859B` (Meta CN) | **Broad.** Wearable neuromuscular sensors + trained model → text. | "a plurality of neuromuscular sensors … configured to continuously record a plurality of neuromuscular signals … trained inference model … determine text". |
| `CN113288183B`, `CN114863912A` (USTC) | **Very close in China.** Facial–neck sEMG silent speech, high-density + discrete electrodes. | High-density and channel-sparse sEMG image sets, source/target domain transfer learning, word-classification network for silent speech. |
| `CN112151030B`, `CN114822541A` (Nat. Defense Sci-Tech Inst.) | **Close in China.** Facial EMG silent speech, with lip/audio and back-translation variants. | Synchronous lip image + facial EMG + audio encoding; and silent sEMG → SAEM + back-translation. |
| `US11683632B2` (Apple) | **Close for an earbud.** Ear-canal accelerometer + microphone triggers ASR. | "an accelerometer worn in an ear canal of a user to generate a non-acoustic signal representing a bone conduction vibration … to trigger". |
| `CN110996782B` (Bose) | **Close for an earbud.** In-ear electrodes controlling another device. | "at least two electrodes, a processor … a signal obtained via the first or second electrode and affected by the user's action" controls another device. |
| `CN115705841A` / `EP4131256A1` / `US12603087B2` (STMicro) | **Close for a jaw/ear accelerometer.** Accelerometer-only speech recognition. | Accelerometer senses vibrations of one or more bones; "does not receive audio input"; voice command and NL recognition from that signal alone. |
| `DE102020110901B4` / `EP4139917B1` (Altavo) | **Close in Europe.** Vocal-tract signal + artificial voice from jaw/neck sensing. | Record healthy speaker's audio, record patient's vocal-tract signal articulating the same text, generate an artificial voice. |
| `US9779758B2` (Google) | **Medium.** Non-microphone head-mounted vibration/motion gates speech. | "vibration data … detected by a sensor other than the microphone … associated with a head-mountable device … determine whether the speaker is speaking". |
| `US10679644B2` / `US10529355B2` (IBM) | **Medium.** Multi-sensor silent/whispered speech → amplified speech. | "receives sensor data from multiple sensors … associated with the low amplitude speech … map the sensor data to … speech". |

---

## Still to fetch (next session, when the Google Patents throttle has cleared)

These candidates were found in the search sweep and are deliberately **not** in
`sources-patents.jsonl` because their record was not opened live. Fetch them from Google
Patents, then add their claims (sites, electrode count, status) and their rows to the table:

* Wispr AI applications: `US20240221751A1`, `US20240221719A1`, `US20240220811A1`
  (family of `US12482449B2`, already read).
* Q (Cue) applications: `US20250028804A1`, `US20250036732A1`, `US20250036731A1`
  (family of `US12154572B2`, already read).
* Pison Technology `US20230088533A1`; Ericsson `US20210390167A1`; Google
  `WO2025038844A1`; Microsoft `WO2018223388A1`; Xpanceo `WO2025014394A1`;
  Shanghai Youwei `WO2023088083A1`.
* Schultz et al. `US20160314781A1` (EMG speech, second Schultz family); Sony
  `CN112840397A` (already in table); Alcatel-Lucent `US20100131268A1`,
  `US20120136660A1` (vocal-tract probing); Georgia Tech `US20130090931A1`
  (multimodal communication); Medibotics `US20150370320A1`.

## Reproduce

```bash
python3 scripts/patent_search.py "silent speech interface" "subvocal electromyography"
python3 scripts/fetch_lens.py US10621973B1 CN113288183B      # -> research/jaw/raw/ (gitignored)
python3 scripts/patent_summarize.py                          # compact facts for the table
python3 scripts/build_sources.py                             # -> research/jaw/sources-patents.jsonl
python3 ~/theprojects/orchestrator/bin/check_sources.py research/jaw/sources-patents.jsonl \
    --min 40 --min-new 30 --kinds paper,patent --known research
```
