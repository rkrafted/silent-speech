# Track 08 — Ear-region sensing for silent speech (in-ear, behind-ear, mastoid, jaw-angle)

Working report. Status: complete (sections 0–8, 91 numbered sources). Every factual claim carries an
inline `[n]`; numbered Sources at the end. **Demonstrated** results are separated from
**claims/marketing**. Numbers are quoted exactly as the source gives them.

Scope from `tracks/08-ear-region.md`: every silent-speech or jaw/tongue-activity sensing idea located
at or near the ear, because the owner wants a hidden hearing-aid / earbud / headphone form factor.
Everything below is about what can be sensed within roughly 3 cm of the ear, plus the hearing-aid
form factor that would host it.

## 0. Why the ear is the strongest concealment site (framing)

The owner's hard constraint is "barely different from the normal face". The ear is the only region
where a sensor can be made *completely* invisible by being a normal object: a hearing aid, an earbud,
a headphone cushion, glasses temples, or a sticker behind the ear. Every face site used by
AlterEgo-class systems (cheek, chin, submental, lips) is visible; the ear canal is not. The price is
distance from the articulators — the face sites sit directly on the speech muscles, the ear does not
— so the signal is weaker and more mixed than face sEMG.

What can actually be transduced at the ear divides into five physically different channels, and
conflating them is the main source of hype in this area:

| Channel | Physical quantity | Nearest speech structure | Best current evidence |
|---|---|---|---|
| Myogenic (EMG/ExG) | muscle action potentials, volume-conducted | jaw muscles (masseter/temporalis/digastric) for jaw; weak tongue/lip leakage | around-ear cEEGrid, mixed EEG+EMG [1][2] |
| Neural (ear-EEG) | cortical potentials | temporal cortex near the upper cEEGrid row | 64-word silent decoding 56.6% offline / 47.2% online [2] |
| Mechanical (deformation) | ear-canal shape/volume change | jaw hinge / TMJ motion couples to the canal wall | EarCommand WER 10.02%, EarSSR 93% words [8][9] |
| Acoustic / vibration | tissue-borne and canal-borne sound | voicing, tongue, NAM | behind-ear NAM mic, 93.5% word on 20k vocab [5][6] |
| Inertial / vascular | head and canal micro-motion, blood | jaw motion, pulse | ear-IMU (EarGate, OESense) [14][20]; in-ear PPG for jaw motion **unverified** |

Three consequences for the build:

1. **Around-ear electrodes are not "EMG electrodes".** In the strongest ear-region study the array
   is described as picking up "both cortical and articulatory EMG-related signals" [2], and the
   lower row sits "near jaw muscles" while the upper row is "near the temporal cortex" [2]. The
   signal is a mixture; whether the useful variance is myogenic or neural is still argued [2].
2. **The ear is a jaw sensor, not (yet) a tongue sensor.** Jaw/tongue movement reach the ear mainly
   through the temporomandibular joint and the ear canal wall, which is why the mechanical systems
   (§4) get high command accuracy while free-text decoding stays hard.
3. **Accuracy numbers at the ear are closed-set classification, not dictation.** The three headline
   ear results are 10 words (96%) [3], 25 sentence-ID (92.24%) [1], and 64 words (56.6% offline /
   47.2% online) [2]. None is open-vocabulary dictation, and [1]'s 92.24% is identification of one
   of 25 full sentences (chance 4.00%), not word error rate [1]. Any plan should target
   command-level accuracy first and treat dictation as a separate, much harder milestone.

## 1. Ear anatomy as a sensor budget: what speech-relevant tissue is within ~3 cm

**The canal itself (the electrode's real estate).**

- Adult external auditory canal (EAC) length from an HRCT 3-D centreline study of 64 ears:
  **27.46 mm (male) vs 25.44 mm (female)**; **27.99 mm (right) vs 25.87 mm (left)** [51]. The osseous
  (bony) part averages **9.61 mm** in 250 canals (mean age 28.43 y), and 64% of canals are conical
  [52].
- The **cartilaginous part has "thick subcutaneous tissue … with numerous ceruminous glands"**;
  glands do not enter the cartilage [53]. The **bony part has thin skin directly over bone**, and it
  is where malignant (necrotising) otitis externa concentrates [76]. Conclusion: the **cartilaginous
  canal (lateral ~two-thirds) is the safe electrode/microphone contact zone**; the bony part is the
  one to avoid abrading.
- Mid-canal cross-sectional area is quoted at **25–70 mm²** (Stinson & Lawton, as reproduced in [50]).
  Deriving a diameter from those areas gives roughly **5.6–9.4 mm** — enough for a custom earmold
  carrying a ring of 2–4 small electrodes, which is how IDUN and Naox do it [33][39].

**Muscles reachable within ~3 cm.** The auricle itself has **3 extrinsic + 6 intrinsic muscles, all
facial-nerve innervated**, and sEMG has been recorded from the anterior (AAM), superior (SAM),
posterior auricular (PAM) and tragicus muscles [59]. PAM sits directly behind the ear and is a
routine sEMG site in auditory-attention research, with electrodes behind both ears [67][68][69].

The speech-relevant muscles near the ear are mostly **jaw** muscles:

| Muscle | Where relative to the ear | Speech role | Evidence / distance |
|---|---|---|---|
| Posterior auricular (PAM) | directly behind ear / over mastoid | not speech; a stable near-ear sEMG site | [59][67][68][69] |
| Masseter | jaw angle, below/anterior to tragus | jaw closing; dominant in-ear jaw artifact | masseteric nerve **33.61 mm** (95% CI 10.37–56.86) from tragus [62]; artifact evidence [40] |
| Temporalis | temple, above ear | jaw closing / chewing | EMG and bend sensor on eyeglass temple [90] |
| Posterior digastric belly | under/behind jaw angle (~3–6 cm from earlobe) | hyoid elevation, tongue–jaw coordination | targeted in an 8-channel SSI montage [61] |
| Stylohyoid | deep to the jaw angle / carotid triangle | hyoid elevation | targeted in the same montage [61] |
| Platysma / sternocleidomastoid | neck, below jaw line | facial/neck tension | pilot targeted 14 muscles incl. both [61] |

**Published near-ear electrode montages** are the practical answer to "where do I put them":

- **Freitas et al. (2015)** placed pairs **"inferior to the ear between the mastoid process and the
  mandible angle"**, one **"superior to the mandibular notch, superficial to the mandibular fossa"**,
  one submandibular midway between jaw angle and mental prominence, one beneath the mental
  prominence, with the **reference on the mastoid**. Their behind-ear channel detected **velum
  movement** with **32.5% frame error across all speakers (23.4% best)** — proof that a mastoid–jaw-
  angle channel carries articulation information, and a reminder that its raw error is high [60].
- **Salomons et al. (2025)** targeted 14 muscles and settled on **8 bipolar channels**: digastric,
  depressor anguli oris, risorius, levator labii superioris, masseter, zygomaticus major, depressor
  labii inferioris, stylohyoid; electrodes placed mid-muscle along fibre direction, sampled at
  **2048 Hz** [61].
- **Lapatki et al. (2003)**: **4 mm diameter, 1.5 mm thick electrodes, bipolar IED 8 mm**, 7 perioral
  muscles, **>98%** placements secure, **crosstalk <25%** [65].
- **Wang et al. (2020)**: 120 high-density sEMG electrodes over neck/face; small selected subsets
  reach 80% accuracy, "few more" reach 85/90/95% [64]. **Zaretsky et al. (2017)**: 42 channels
  including masseter, orbicularis oris, submental and paralaryngeal, reduced to 16 optimal positions
  [66]. **Rong & Pattee**: masseter / anterior temporalis / anterior belly digastric sEMG separates
  ALS from controls with factors ≥90% accurate — useful as a jaw-muscle signal-quality reference,
  not as speech decoding [63].

**Crosstalk physics — the constraint that decides the electrode layout.** Surface EMG from a distant
muscle at the same site is only ~**6%** of the target amplitude and does **not** fall when the
inter-electrode distance (IED) is below **4 cm**; the target amplitude rises steeply up to a 5 cm IED
[70]. Crosstalk increases with electrode area and with IED, and is worse for single- than
double-differential recording [71]. Filter selectivity decreases as IED increases [72]; a nonlinear
spatio-temporal filter cuts crosstalk RMS by ~**20%** [73]; a 20 mm IED has been suggested for a
large muscle [78]. The ear-canal/eardrum-side montage is at the **tiny-IED extreme**, which is good
news for rejecting distant neck muscles but also means the **masseter/temporalis signal will dominate
whatever is picked up near the ear** — the tongue is not directly observable there.

**Safety and tolerability.** Otitis externa is frequently self-inflicted by trauma or objects in the
canal, and hearing-aid wearers are "especially prone to infection" [74]; hearing aids and foreign
bodies are listed risk factors [75]. A 2025 review of in-ear EEG electrodes states that
biocompatible materials are required and that the open problems are **anatomical variability,
ergonomics and motion artifacts** during long-term wear [77]. A **subdermal electrode behind the ear
has no quantified risk source in this work — unverified**; the anatomical hazards to avoid are the
**posterior auricular artery** (main supply to the external ear [54]), the **great auricular nerve**
(mastoid→GAN **27.71 mm**, inferior ear→GAN **31.03 mm**, lobular branch ~**4.5 mm** deep, entering
the tympanoparotid fascia in 100% of 20 hemifaces [57][58]), and the **auriculotemporal nerve**, which
ascends between the TMJ and the EAC [55]; the concha and a small area behind the ear are also
innervated by the **chorda tympani** (facial nerve), so ear-region skin sensation is multi-nerve and
tolerability must be tested rather than assumed [56]. The tympanic membrane is approximately **1 cm**
in diameter [82].

## 2. In-ear / ear-canal electrophysiology (EMG, EEG, ExG)

**Question 1: do in-ear electrodes see jaw/tongue/speech muscle activity?** For **jaw/masseter EMG,
yes — demonstrated.** For **tongue or phoneme-level articulation, no — not demonstrated** by any
source found here.

The best direct evidence is a study designed to characterise this:

- Kappel et al. (2017), 9 subjects, scalp EEG plus ear-EEG: "Artifacts related to jaw muscle
  contractions were present all over the scalp and in the ear, with the highest SNR deteriorations
  in the gamma band. The SNR deterioration for jaw artifacts were in general higher in the ear
  compared to the scalp" [40]. So the ear is **more** exposed to jaw-muscle artifact than the scalp,
  not less — which is bad for ear-EEG and good for jaw-EMG.
- OpenEarable ExG (2024): an open-source earable with an AD7124-4 24-bit ADC and "up to 7 sensing
  channels (incl. 1 reference) plus ground", Dätwyler SoftPulse in-ear electrodes, gain ~50,
  "sampling rates of up to 19,200 SPS … over serial" and "up to 500 SPS" over BLE. In 3 male
  participants it detected alpha EEG, smooth-pursuit EOG, and jaw-clench EMG ("clear rise in signal
  amplitude … during jaw muscle clenching"). MIT-licensed hardware/firmware [35].
- Avramidou et al. (2024), "From Ear-EEG to Ear-ExG: The Jaw Artifact is a Keeper", used a cEEGrid
  around the ear and "systematically recorded the jaw artifact in a series of experimental scenarios
  engaging the muscles involved in mastication and speech production", separating chewing from
  speaking with p<0.05 [41].
- Naox's cleared in-ear EEG device (see below) was validated with protocols that included
  "artifact-inducing tasks (e.g., eye movements, speech, jaw clenching)" — i.e. the regulator saw
  speech and jaw activity as expected in-ear artifacts [39].

What does **not** exist in any fetched source: decoding of tongue articulation, phonemes, or words
from **in-ear** EMG. The strongest silent-speech EMG result at the ear remains the headphone-earmuff
textile array (96% on 10 control words), which sits on the **concha/earmuff skin, not in the canal**
[3]. Treat "in-ear EMG dictation" as unproven.

**Question 2: is ear-EEG usable?** Yes, with the caveat that near-ear sources are fine and far
sources are not.

- Mikkelsen et al. (2015), 13 subjects, 32 scalp + 12 ear electrodes, g.tec USBamp at 256 Hz, custom
  3D-printed earpieces, impedance <10 kΩ: ASSR SNR **22.1 ± 8.5** (ear) vs **21.8 ± 4.0** (TP9/TP10),
  scalp–ear correlation **0.96 ± 0.03**; the authors conclude "ear-EEG has the same signal-to-noise
  ratio as scalp" EEG for near-ear sources; MMN was "difficult to monitor" [36].
- cEEGrid (Bleichner & Debener 2017): 10 electrodes per grid, Ag/AgCl polymer thick-film ink, 3 mm
  contacts, 12 or 18 mm spacing, polyamide flex, **>7 h** wear; P300 classification ~70%; auditory
  attention ~70% (69% vs 85% for an 84-channel cap in one task); alpha, EOG and ECG also recovered
  [37]. Debener et al. (2015) had 10 participants wear two cEEGrids "at least seven hours" with
  morning/afternoon P300 classifiers >70% both sessions [38].
- Dry electrodes: Kappel et al. (2019), 12 subjects, four paradigms (ASSR, SSVEP, MMN, alpha), all
  significant at p<0.05 using actively shielded nanostructured dry electrodes in an individualised
  soft earpiece; MMN needed an opposite-ear reference [42]. Goverdovsky et al. (2016) used
  viscoelastic generic earpieces with conductive-cloth electrodes and saline [43].
- The ear-centred-sensing editorial lists EEG, ECG, EMG, EOG and EDA as recordable from the ear and
  warns that small intra-aural distances give high impedance and demand good amplifiers [44].

**Commercial in-ear electrophysiology.**

| Device | Montage | Key specs | Status |
|---|---|---|---|
| IDUN Guardian 3 | "one channel in the right ear … referenced to the reference electrode in the left ear"; ground on left earhook | DRYODE dry sensor, impedance (typ.) **<200 kΩ**, 24-bit, ±100 mV, output **250 Hz**, BLE 5+, 8+ h, **24 g** | "Research Device. It is not a medical device." [33] |
| Naox NX01 | 1 bipolar EEG channel, two active **dry silver** electrodes in earbuds, single-use eartips, T7–T8-like derivation | FDA 510(k) **K251550 cleared 25 Nov 2025**; max continuous recording **10 h**; adults and children 6+; multi-centre studies incl. jaw-clench/speech artifacts and overnight sleep | cleared (regulatory) [39] |
| Cebreo Medical NeuroBuds | in-ear EEG | CE-marked; "monitoring periods of up to three months"; no channel/rate numbers | claim/marketing [46] |
| Neurable MW75 Neuro | EEG sensors in headphone ear pads | no channel count or validation published | claim/marketing [47] |
| OpenEarable ExG | in-ear + around-ear ExG | up to **7** sensing channels; open source [35] | research platform |
| Mentalab, Emotiv | mobile/scalp EEG | **no in-ear product found** | unverified [48][49] |

**What this means for electrodes vs. the dry/gel trade-off.** AESSI's gel cEEGrids were required to be
**below 20 kΩ** before every session [1]; IDUN's dry in-ear sensor is specified at **<200 kΩ typical**
[33]. That order-of-magnitude impedance gap, plus the fact that the ear sees more jaw artifact than
the scalp [40], predicts that a dry in-ear EMG array will be dominated by motion/jaw artifact unless
the ear tip is mechanically stable. For the owner's one-user, long-calibration regime this is
survivable (artifact can be modelled per user), but it is the main engineering risk in the in-ear
electrode path.

## 3. Behind-the-ear and mastoid sites, and the flagship around-ear results

### 3.1 The around-ear cEEGrid is the best-evidenced ear electrode layout

Two 2026 studies define the state of the art, and they measure different things — read them together.

**AESSI (Xu et al., 2026)** [1] — closed-set **sentence identification**, cross-day, online:

- Bilateral cEEGrid around-ear arrays, **20 electrodes total**, TMSi SAGA 32+ at **1 kHz**, average
  reference, ground on the left arm; channels 18 and 20 excluded for high impedance, leaving
  **18 channels**; all channels had to be **<20 kΩ** before each session [1].
- **24 native Mandarin speakers** (11 women, 18–46 y), **44 sessions, 11,000 trials**; 25 short
  Mandarin sentences of **6 characters each**; a **3 s** silent-articulation window per trial [1].
- Mode: participants "were instructed to **silently articulate** the target sentence once during the
  3 s cue and to try to **avoid whispering**" [1] — i.e. *mouthed/silent articulation*, not pure
  imagery.
- Result: **92.24%** participant-macro-averaged accuracy **without test-day calibration** (chance
  **4.00%**), exceeding the best adapted baseline by **50.57 percentage points**. Five participants
  returned **≥21 days** after their last recording, had electrodes reapplied, and completed **50
  independently randomized online tests each**, achieving **98.0% overall** accuracy; median CPU
  preprocessing + inference was **31.70 ms** [1].

**Inoue et al. (2026, J. Neural Eng.)** [2] — **64-word** vocabulary, much harder, and the most
complete ear-region dataset:

- cEEGrid around the ear + OpenBCI Cyton + Daisy, **16 channels**, sampling **125 Hz**. The paper
  states the placement explicitly: "the upper electrodes located near the temporal cortex and the
  lower electrodes positioned near **jaw muscles**, making it suitable for capturing both **cortical
  and articulatory EMG-related signals**" [2].
- **72 h** of around-ear EEG from **24 healthy participants plus one individual with incomplete
  locked-in syndrome (LIS)**, across silent, vocalized and attempted speech; combined with prior EMG
  + high-density EEG datasets for **282.4 total h** of training data [2]. Core cEEGrid silent-speech
  set: 24 participants, 192 runs, **11.3 h**; attempted-speech set: 1 participant, 136 runs, 7.9 h
  [2].
- **64 words** (2–7 moras), presented one at a time; participants silently, vocally or attemptedly
  articulated [2].
- Results: training on the heterogeneous dataset reached **56.6%** accuracy for healthy users and
  **47.3%** for the LIS participant (offline). Online Top-1/Top-5: **47.2% / 76.0%** healthy and
  **26.5% / 49.1%** LIS; online accuracy fell ~**14.6 pp** (healthy) and ~**16.9 pp** (LIS) versus
  offline. Fine-tuning for a new vocabulary added **22 percentage points** over training from
  scratch; for the LIS participant, their own data carried ~**4×** the weight of healthy data [2].
- Preprocessing: 50 Hz notch, common average reference, **1–60 Hz** band-pass, down-sampled to
  **120 Hz** [2].

**Read the two together:** 92.24% is identification of one of **25 whole sentences** (chance 4%) from
a 3 s window [1]; 47.2–56.6% is **64-word** decoding with word-level articulation [2]. The around-ear
array is excellent at coarse, well-separated classes and much weaker at word-level dictation. Any
plan that quotes "92% around-ear" as if it were dictation is misreading AESSI.

### 3.2 What the around-ear signal actually is

It is a **mixture**, and this is the central technical uncertainty:

- The cEEGrid lower row sits over jaw muscles and the paper calls the signal "cortical and
  articulatory EMG-related" [2]. Independent work shows the ear is *more* exposed to jaw-muscle
  artifact than the scalp [40], and that around-ear electrodes capture jaw EMG during both
  mastication and speech production [41].
- The same arrays also read facial muscle activity: Knierim et al. (2021) used cEEGrids to
  differentiate **reading, speaking, chewing, jaw clenching and six posed emotion expressions** with
  a Random Forest [4].
- So "around-ear silent speech" is best understood as **mostly distal jaw/facial EMG plus a smaller
  cortical component**, decoded by a learned model that does not need to separate them.

### 3.3 Sites behind the ear, on the mastoid, and just below the lobe

- **Posterior auricular (PAM) sEMG** behind both ears is a stable, published site [59][67][68][69] —
  the easiest "hidden" electrode location, but it is not itself a speech muscle.
- **Mastoid ↔ mandible-angle channel**: Freitas et al. detected velum movement from a pair
  "inferior to the ear between the mastoid process and the mandible angle", with 32.5% frame error
  across speakers (23.4% best) [60]. This is the closest published "behind-the-ear speech channel".
- **Contact microphone on the mastoid** is the NAM site, and the best ear-region *speech* accuracy
  in this whole report (§5) [5][6][7].
- **QuietSync / "Whispering Wearables" (ICMI 2024)** combines an IMU "attached to the lower part of
  the headphones near the ear" with contact ExG electrodes on headphones, glasses (nose **and behind
  the ear**) and face; **9 participants**, **12 commands at 94.2%** accuracy, silent [83].
- **In-ear magnetosensing (EarMag, 2025)**: jaw/head gestures via a magnet in the mouth and an
  in-ear sensor; 21 participants, 17 orofacial exercises, **76% accuracy for five exercises on an
  unseen test set of ten users** [84].
- **Patents and filings point the same way.** Naqi Logix's SEC Reg-A filing describes an earbud that
  "integrates … electromyographic (EMG), electroencephalographic (EEG), and electrocardiographic
  (ECG) signals, along with inertial measurement units (IMUs)" for "jaw clenches, eyebrow movements,
  eye blinks", with **no channel count, sample rate, accuracy, users or wear duration published**
  [45]. Its patent `US20260037066A1` "Earbud sensory assembly" claims **three electrodes contacting
  ear anatomic locations (concha / tragus / triangular fossa)** that produce an "electrophysiologic
  measurement" (ECG, EEG or EMG) used to "determine a gesture" — jaw clench, mouth, forced eye blink,
  eyebrow raise — classified with "XGBoost random forest" [87]. Wispr AI's `US20240221738A1` (granted
  `US12482449B2`, 2025) claims a wearable with an EMG sensor "when the user is silently speaking" and
  an **ear-hook** form factor (FIG 6A) feeding an LLM [86].
- The Subvocal Company is **not** an ear device: its own site says "An under-chin wearable … **It
  sits under the chin, not on the face**" and "The sensor reads muscle signals **under your chin**"
  [21]; the YC page names no form factor [22]. Its "**more than 200 words per minute**" figure comes
  from a founder interview and is a **claim** with no vocabulary, accuracy or N reported [88].

### 3.4 The ear-EEG signal-quality gradient (and where the hype is)

- Geirnaert et al. (2025) recorded scalp, around-ear and in-ear EEG simultaneously on the same
  auditory-attention task: **83.4% (scalp), 67.2% (around-ear), 61.1% (in-ear)** on 60 s decision
  windows; adding an external reference or a few scalp electrodes via greedy selection boosted
  accuracy by over **10 percentage points**, especially for in-ear [79].
- Kaongoen et al. (2021) tested the true "internal" case — **5-class speech imagery** with no
  articulation — using ear-EEG versus a 32-channel scalp cap: **38.2%** average (max 43.8%) for
  ear-EEG vs **43.1%** (max 55.0%) for scalp, against **20%** chance; **7 of 10** subjects showed no
  significant difference [80].
- The 2026 *Nature Sensors* review states that ear-centred and in-ear EEG devices "have matched
  traditional scalp set-ups in decoding accuracy while enhancing comfort and form factor" [81]. The
  primary studies above show a **5–22 percentage-point gap** depending on task, and the review's own
  body text notes the artefact problem [79][80][81]. Treat "matched scalp" as *task-dependent*.
- For calibration, note where the training data goes: Naqi's in-ear EEG device was cleared with
  speech and jaw clenching as **artifacts to be tolerated** [39], while AESSI/Inoue treat the jaw
  component as **signal to be decoded** [1][2]. Same physics, opposite framing.

### 3.5 The neck/face comparison, for honesty

The strongest EMG silent-speech numbers are still **not** at the ear: SilentWear's textile **neck**
band reaches **84.8 ± 4.6% (vocalized)** and **77.5 ± 6.6% (silent)** on 8 commands, dropping to
59.3 ± 2.2% cross-session for silent speech [89]; the 2018 MIT AlterEgo face/jaw array reported
"92% median word accuracy" [85]. The face/neck numbers are on smaller vocabularies and different
tasks, so they are not a like-for-like accuracy comparison, but they are consistently higher than the
around-ear 64-word result [2][85][89]. The 2025 AlterEgo company publishes no sensor site,
vocabulary, accuracy or user count — **claim only, specs unverified** [85][91].

## 4. Ear-canal deformation and in-ear mechanical/acoustic sensing

This family needs no skin electrodes and no visible hardware: the earphone's **own speaker and
microphone** become the sensor. The ear canal changes shape when the jaw moves (the TMJ lies
immediately anterior to the canal, with the auriculotemporal nerve ascending between the two [55]),
so an acoustic probe of the canal can recover jaw/articulator motion [8][9].

**Active acoustic / ultrasonic probing.**

| System | Sensor + method | Subjects | Vocabulary | Reported result | Mode |
|---|---|---|---|---|---|
| EarCommand (IMWUT 2022) | earphone, canal deformation from jaw/articulator motion | 12 (secondary) [8] | 32 word commands / 25 sentence commands | **WER 10.02%** word-level, **12.33%** sentence-level [8] | silent |
| EarSSR (IEEE TMC 2024) | in-ear speaker+mic, FMCW ultrasound **16–22 kHz**, 2-ch CNN "SSrNet" | **50 volunteers** [9] | letters + words/phrases | **82%** single-letter, **93%** word/phrase; nonspeech SVDD **95.08%**; latency **0.625 s**; **385 mW**; shallow earphone fit drops word accuracy **93% → 72%** [9] | silently mouthed |
| ReHEarSSE (CHI 2024) | earbud ultrasound, ear-canal shape, CTC model | unverified | **100 unseen words** | **89.3%** [16] | silent |
| HEar-ID (UbiComp Companion 2025) | ANC earbuds, ultrasound **17.5–23 kHz** + 0–11 kHz | **11 users** [17] | 50 words | Top-1 **67.3%** overall (90.25% for 8/11 users); auth TPR 81.76%, FPR 3.2% [17] | whisper/near-silent |
| CanalScan (IEEE TMC 2024) | smartphone earpiece speaker + top mic, 16 kHz send / 48 kHz record, random forest | **20 participants** [13] | 6 tongue–jaw movements | **94.84% recall / 95.00% precision**, user-independent [13] | gesture (not speech) |
| EarDynamic (IMWUT 2021) | inaudible beeps + reflection, canal deformation while speaking | unverified | authentication | recall **97.38%**, F1 **96.84%** [11] | voiced (auth, not decoding) |
| EarIO (IMWUT 2022) | two speaker+mic pairs, tracks facial parameters | 16 participants [15] | 52 facial parameters | **86 Hz**, **154 mW** [15] | mouthed |
| EarSense (MobiCom 2020) | earphone speaker retasked as input transducer | 18 volunteers [10] | 6 teeth-tap/slide gestures | no per-user training [10] | gesture |

**Passive mechanical.** EarGate and OESense use the **occlusion effect** — with the canal sealed,
bone-conducted sound below ~50 Hz is boosted by up to 40 dB and is largely immune to outside noise
[14][20]. OESense reports **99.3%** step recall, **98.3%** recall for 5 activities and **97.0%** for
5 tapping gestures across **31 subjects**, at **746 mW** and **40.85 ms** latency [14]. JawSense uses
an ear-worn IMU/accelerometer for unvoiced jaw tracking; its accuracy and user count are
**unverified** (abstract only) [12].

**What the deformation family really proves for this build.** Three things:

1. **The jaw-to-canal coupling is large and repeatable.** EarSSR gets 93% word/phrase accuracy on 50
   volunteers [9]; CanalScan gets ~95% on 6 tongue–jaw movements, user-independent [13]. This is the
   most robust jaw signal available at the ear, and it needs no electrodes at all.
2. **The articulation is dominated by the jaw, not the tongue/lips.** Every system above is a fixed
   command set. None reports open-vocabulary dictation, and EarSSR explicitly did not implement
   sentence-level recognition [9]. Bilabial and tongue-only distinctions are where this family is
   expected to fail, because the canal only sees the mechanical consequence of jaw motion.
3. **Fit quality is the dominant error term, not the classifier.** EarSSR's word accuracy falls from
   93% to 72% with a shallow earphone fit [9]. Any ear-region build must treat the mechanical
   interface (ear-tip seal, earmold) as the first-order design problem.

## 5. In-ear microphones, NAM and bone-conducted vibration

**The in-ear microphone is already in the product.** Every active-noise-cancelling earbud and most
modern hearing aids contain an inward-facing microphone a few millimetres from the eardrum [20].
EarGate shows what that microphone sees: with the canal occluded, the occlusion effect boosts
bone-conducted sound below ~50 Hz by up to 40 dB, so the in-ear mic is a high-SNR vibration pickup
that largely rejects outside noise [20]. For gait, EarGate low-pass filters at 50 Hz and reaches up
to **97.26% balanced accuracy** on 31 subjects (single-session; 92.46% across conditions), and it
explicitly shows that human speech (300–3400 Hz) and music are separable from the low-frequency
signal by filtering [20]. Read the other way, that figure is also evidence that **the in-ear
microphone does capture speech-related vibration** — EarGate had to filter speech out to isolate gait.

**Non-Audible Murmur (NAM) is the strongest ear-site *speech* result, and it is not subvocal.** A
contact microphone bonded behind the ear (over the mastoid) picks up tissue-conducted NAM:

- Nakajima et al. (Eurospeech 2003): stethoscopic NAM microphone "attached behind the talker's ear",
  16 kHz, 2,100 NAM samples, **>90% accuracy** with monophone HMMs, robust to background music/TV.
  NAM is defined as inaudible speech **without vocal-fold vibration**, explicitly distinguished from
  whisper (which nearby listeners can hear) [5].
- Heracleous et al. (Interspeech 2004): 20k-vocabulary Japanese dictation, MAP adaptation gives
  **93.5% word accuracy** (MLLR 90.3%) [6].
- **Interspeech 2005 ("Remodeling of the Sensor for NAM")**: a soft-silicone NAM microphone improves
  to **93.9%** word accuracy versus **88.9%** for the stethoscopic type on the same task; 25-keyword
  spotting reaches 88.2% detection at 4 false alarms (FOM 85.6%); the body acts as a low-pass filter
  (~36 dB attenuation at 5 kHz vs 1 kHz) [7].

The catch is the mode: NAM is *inaudible but actually produced* — the talker still articulates a
murmur, so it is closer to "silent-out-loud" than to the owner's "internal articulation". The other
catch is coupling: the microphone must be pressed to the mastoid skin, and it also picks up ordinary
speech transmitted through the body (BTOS) [7]. No primary source found in this work demonstrates
open-vocabulary speech decoding from an in-ear microphone with **no** articulation at all — mark
"in-ear mic for pure subvocalisation" **unverified**.

**Modern earbud approaches chose ultrasound over microphone-NAM.** ReHEarSSE [16] and HEar-ID [17]
probe the canal with 16–23 kHz ultrasound and decode the reflected canal shape; HEar-ID additionally
uses a 0–11 kHz "whisper" band [17]. WhisperMask (AH 2024) is a low-sensitivity diaphragm microphone
in a mask, not in-ear, and reports +30% whispered-speech recognition accuracy at 80 dB background
versus a pin mic/earbuds [19]. A CHI 2025 late-breaking prototype, SilentWhisper, targets inaudible
faint-whisper input from an earbud; its accuracy and user count could not be verified from the
abstract [18].

**Build implication.** A NAM-style contact microphone behind the earlobe/mastoid is the *cheapest*
path to real word-level speech at the ear with no electrodes and no implant — 93.5% word accuracy on
a 20k vocabulary is still, 20+ years later, better than any electrode-based around-ear system on
free speech [6]. Its cost is that the user must **actually articulate** a murmur rather than merely
think: the source defines NAM as inaudible to nearby listeners [5], so the "no sound" constraint can
be met, but the articulators still move — the same mouthed-vs-imagined distinction that applies
everywhere else in this report.

## 6. Hearing-aid form factors and what actually fits

**Styles and the space budget.** NIDCD describes BTE as a hard case behind the ear with the
electronics in the case and a plastic earmold in the ear; ITE as fitting "completely inside" the
outer ear; ITC and CIC as fitting in the ear canal; smaller styles "have less space available for
batteries and additional devices" and "their reduced size limits their power and volume" [23].
Starkey's own style page describes IIC as inserted at the second bend of the canal and "the smallest,
most discreet" [24]. **Per-style millimetre dimensions could not be verified from a fetched page**
(every manufacturer spec sheet is a PDF), so treat any mm figure for BTE/ITE/CIC/IIC as unverified
until a datasheet is read.

**Battery volume sets the floor.** Zinc-air cells (MicroBattery's published table) [25]:

| Size | Capacity | Diameter × height | Mass |
|---|---|---|---|
| 10 | 100 mAh | 5.8 mm × 3.6 mm | 0.3 g |
| 312 | 170 mAh | 7.9 mm × 3.6 mm | 0.58 g |
| 13 | 300 mAh | 7.9 mm × 5.4 mm | 0.83 g |
| 675 | 650 mAh | 11.6 mm × 5.4 mm | 1.83 g |

Rechargeable hearing-aid button cells are NiMH (not Li-ion), rated "charged more than 600 times",
with a pocket charger that "fully charge[s] two batteries in only two hours" [26]. Li-ion capacities
for modern hearing aids/earbuds could **not** be verified [unverified].

**Electronics vs. shell — the hard constraint.** A size-10 CIC/IIC shell has roughly a 5.8 mm circle
to work with [25]. The TI **ADS1299**, the standard 8-channel EEG/EMG AFE used by OpenBCI, is a
TQFP-64 package of **12 mm × 12 mm** [29]; the Intan RHD-series (16/32/64 channels, 2.4 µV rms noise,
up to 30 kS/s) is available in QFN/BGA **and bare die** [30]. The OpenBCI Cyton reference board is
**2.41" × 2.41" (≈61.2 mm × 61.2 mm)** [31]. Consequences:

1. **A stock-package AFE cannot go inside a CIC/IIC.** Either put the AFE in a BTE/RIC case and run
   only electrodes or a flex lead into the canal, or use a bare-die AFE (Intan) / a small custom AFE.
2. **A BTE/RIC case is the realistic host** for AFE + radio + battery; the canal part becomes a
   passive electrode or microphone assembly. This is exactly the split used by RIC hearing aids.
3. **Power budget is small.** Size-10 zinc-air gives 100 mAh at 1.45 V [25]; an ADS1299-class 8-channel
   stream at ~1 kHz plus BLE will drain that quickly, so one or two channels at low duty cycle is the
   practical in-ear configuration.

**Shell fabrication.** Formlabs' BioMed Clear is a documented biocompatible hard-shell/earmold resin
made in an ISO 13485 facility with an FDA Device Master File; it is certified to ISO 10993-5, -10 and
-23 and USP Class VI, is autoclavable, prints at 50 or 100 µm layers, and has 52 MPa tensile strength
/ 2.1 GPa modulus [27][28]. It requires a dedicated resin tank to preserve biocompatibility [28].
**Co-printing electrodes or flexible circuits into a soft-silicone earmold is unverified** — no
fetched source confirms a process. Dreve Fotoplast, EnvisionTEC and Materialise pages were not
retrievable [unverified]. IP ratings for hearing aids were not verified.

**Ear-EEG already exists in a hearing-aid-like form factor.** Aarhus University opened a centre for
ear-EEG in 2019, describing ear-EEG as measuring "extremely small voltage changes on the surface of
the skin inside the ear"; it is funded by the families behind WS Audiology and UNEEG Medical plus the
William Demant Foundation (which owns Oticon) [32]. IDUN Technologies' Guardian earbuds use "a
proprietary in-ear electroencephalography (EEG) electrode", "one channel in the right ear which is
being referenced to the reference electrode in the left ear", with ground on the left earhook; IDUN
labels it a Research Device, "not a medical device" [33]. This is the documented minimal in-ear
montage: **one active in-ear electrode per side, cross-ear reference, earhook ground** [33]. Naox has
an **FDA-cleared** in-ear EEG device (510(k) K251550, one bipolar channel, dry silver electrodes,
max 10 h) [39] — so in-ear electrophysiology is no longer purely a research form factor.

**Bone-conduction output in the same form factor.** Cochlear Baha 6 Max is **9.8 g** without battery
(size 312); MED-EL BONEBRIDGE is **<9 g including battery** (675P); Oticon Ponto 5 Mini is **14 g**
without battery (13); MED-EL ADHEAR is **15 g** (13) [34]. A behind-the-ear bone-conduction actuator
is therefore a 9–17 g object — visible behind the ear, but not on the face, and it shares the same
real estate as the sensor.

## 7. Combinations: ear electrodes + one thin strip under the jaw

The ear's blind spot is the **anterior articulators**: the lips, tongue tip and the submental/digastric
complex are not directly under the ear, and their surface EMG is heavily attenuated at the ear. The
single strongest around-ear system implicitly admits this: Inoue et al.'s heterogeneous training set combined cEEGrid
around-ear data with **63-channel whole-brain EEG and 5-channel facial EMG on the cheek, upper lip,
lower lip, chin and throat** [2]. The ear array is the concealment layer; the face/neck channels
carry articulation.

Evidence that a hybrid pays off:

- Adding the eego dataset (facial EMG at 5 sites) improved the around-ear decoder, and the authors
  treat cross-device, cross-task data as the reason the 64-word decoder works at all [2].
- QuietSync pairs an IMU near the ear with contact ExG on headphones, glasses (**nose and behind the
  ear**) and face — a hybrid that reaches 94.2% on 12 commands [83].
- EarMag puts a magnet in the mouth and senses it in-ear, avoiding skin electrodes at the ear's blind
  spot but requiring something inside the mouth [84].
- Gaddy & Klein's 8 monopolar sites include one "**4 cm in front of ear**" [61] — the ear-adjacent
  anchor of a conventional face array, and exactly where a behind-ear pod would transition to a
  jaw strip.
- Bipolar recording with **8 mm IED and 4 mm electrodes** keeps perioral crosstalk under 25% [65],
  so a thin strip does not need large pads; the montage of digastric + stylohyoid + masseter from
  [61] is a ready-made target set.

**A concrete route.** One BTE/RIC pod behind the ear holding the AFE + radio + battery, with:
(i) a soft custom earmold carrying 1–3 in-canal/concha electrodes, (ii) 2–4 retroauricular/mastoid
electrodes on the pod's skin side, and (iii) a thin flex strip (or an e-tattoo) running from the pod
down behind the jaw angle to 1–2 submental/digastric sites, hidden by the jawline and hair. The
user's own skin-friendly adhesive or a glasses temple can hold the strip. The brief's fallback — a
small **subdermal** lead — would make the strip invisible, but the relevant anatomy is unforgiving:
avoid the **great auricular nerve** (inferior ear→GAN 31.03 mm; lobular branch ~4.5 mm deep [57][58])
and the **posterior auricular artery** [54], and there is **no quantified safety source for a
behind-ear subdermal electrode** in this work [unverified]. Treat subdermal as a later, medically
supervised option, not the first build.

**Cost of the hybrid.** Invisibility drops from "looks like a hearing aid/earbud" (ear-only) to
"looks like a hearing aid plus a barely-visible jawline strip" — still far from AlterEgo's visible
face tentacles, and still within the brief's "barely different from normal" if the strip is thin and
skin-toned.

## 8. Ranked ear-region designs and the exact experiment to run first

### 8.1 Ranked designs

Ranked for this owner (one user, hidden form factor, long calibration allowed, one hired EE). "Command
accuracy" means a fixed small vocabulary; "dictation" means open/free text.

| # | Design | Invisibility | Command accuracy (evidence) | Dictation | DIY difficulty |
|---|---|---|---|---|---|
| 1 | **Around-ear cEEGrid-style ExG** (concha + retroauricular, gel or dry) + BTE pod | High (BTE / headphone / glasses temple) | High: **92.24%** on 25 sentences cross-day [1]; **56.6% offline / 47.2% online** on 64 words [2] | Low–medium (64-word closed set is the ceiling today) | Medium: 8–18 ch, ADS1299/Intan, electrode placement repeatability |
| 2 | **Ear-canal deformation / ultrasonic earbud** | Highest (a normal earbud) | High: **93%** word / 82% letter [9]; EarCommand **WER 10.02%** (32 words) [8]; ReHEarSSE **89.3%** (100 words) [16]; HEar-ID **67.3%** (50 words, 11 users) [17] | Low: fixed vocab, sentence level not built [9] | Medium–high: custom acoustic stack, 16–22 kHz FMCW, fit-critical (93%→72% on shallow fit [9]) |
| 3 | **Behind-ear contact mic (NAM)** | High (behind the lobe) | **Highest speech accuracy: 93.5–93.9% word on a 20k vocabulary** [6][7] | Medium (real words, but requires a murmur) | Low–medium: contact mic + ADC + tight mastoid coupling [5] |
| 4 | **Hybrid ear ExG + under-jaw strip** | Medium (thin jawline strip) | Highest: adds digastric/stylohyoid/submental channels [61]; heterogeneous training helps [2] | Medium | Medium: flex strip + adhesive + routing, same AFE |
| 5 | **In-ear dry EMG micro-gestures (Naqi-style)** | Highest (earbud) | Unknown: **no published accuracy** [87]; jaw-clench is demonstrably detectable [35][40][41] | Unproven (gesture interface) | Medium: dry in-ear electrodes, high impedance [33] |
| 6 | **Pure ear-EEG speech imagery** | High | Low: **38.2%** on 5 classes vs 20% chance (ear-EEG) [80] | Very low in this timeframe | Medium: ear-EEG hardware exists [33][39] |

**Recommendation.** Build **#1 (around-ear ExG) and #3 (behind-ear contact mic) into the same BTE
pod** first: they share the pod, both are cheap, and each covers the other's weakness (#1 handles
articulation classes, #3 gives real word-level acoustic evidence). Keep the jaw strip (#4) as the
planned upgrade if the ear-only tongue/lip test fails. Treat #2 as the "consumer-normal" end state
once the sensing question is settled, and park #6.

### 8.2 The exact experiment to run first

**Question.** For this one user, does an ear-region electrode array carry information about **tongue
and lip** articulation, or only about **jaw** movement? This single result decides whether the hidden
ear-only design is viable or whether the under-jaw strip is mandatory.

**Hardware (borrow or buy, no custom PCB yet).** An OpenBCI Cyton + Daisy (16 ch, ADS1299, 125 Hz)
— the exact amplifier used by Inoue et al. [2] — or an OpenEarable ExG board [35]. Electrodes:

- 6–8 around the right ear: tragus, concha, two retroauricular, mastoid, jaw angle (a cEEGrid [37]
  or hand-placed Ag/AgCl).
- Reference: left mastoid; ground: bony arm/elbow.
- 2 "truth" channels on the submental/digastric midline as a comparison array [61].
- Record a second block with **dry** electrodes to quantify the penalty vs gel [33].

**Task (one ~60-minute session, 20–30 trials per condition, self-paced).**

1. Rest.
2. Jaw clench (pure masseter).
3. Jaw open/close (pure jaw).
4. Tongue tip up / left / right with the jaw held still (pure tongue).
5. Bilabial vs alveolar vs velar silent syllables: "pa", "ta", "ka" (isolates lip vs tongue vs jaw).
6. Six to ten silently mouthed control words (e.g. the 10-word set from [3]).

**Analysis.** Band-pass 20–450 Hz, notch 50/60 Hz, epoch, extract log power + spectral features per
channel; train a linear discriminant / small SVM with leave-one-trial-out. Run three arms: ear-only,
submental-only, and the fusion. The **key number is ear-only accuracy on conditions 4–5**: if
ear-only is at chance for tongue/lip contrasts while the submental channel is not, the ear cannot
dictate and the jaw strip is required.

**Pass/fail criteria.** Jaw conditions (2–3) should exceed ~70% single-trial from the ear alone if
the array is seated correctly (the jaw artifact is strong [40]). Tongue/lip conditions (4–5) above
chance by a clear margin are the go/no-go for an ear-only dictation path; at chance, go to design #4.

**Second, parallel check (30 minutes, no electrodes).** Tape a contact/stethoscope microphone over
the mastoid and have the user murmur a 50-word list; confirm the NAM path works for this user's
anatomy before investing in the pod [5][6]. If it does, design #3 may be the fastest route to real
word accuracy while the electrode work continues.

**Why this experiment first.** It is the cheapest test that discriminates between the two build
futures (hidden ear-only vs hidden-plus-strip), it reuses documented hardware and montages
[2][35][61], and its failure mode is informative rather than fatal.

## Sources

Sources 1–91, numbered in order of the report's topic blocks. Where only an abstract/record could be
fetched (publisher blocked the full text) it is marked; those claims are limited to what the fetched
record states.

**Around-ear flagship and ear-region framing**

1. Xiran Xu, Mochu Dong, Yujie Yan, Chenxi Wang, Yu Jiao, Jing Chen. "AESSI: An Around-Ear Silent
   Speech Interface for Cross-Day Online Reuse without Test-Day Calibration." arXiv:2609.21436, 18 Sep
   2026. https://arxiv.org/abs/2609.21436 (full PDF fetched)
2. Masakazu Inoue et al. "Large-scale training data enhances silent speech decoding with around-ear
   EEG." *J. Neural Eng.* 23 (2026) 026027. doi:10.1088/1741-2552/ae54d0.
   https://beta.iopscience.iop.org/article/10.1088/1741-2552/ae54d0/pdf (full PDF fetched)
3. Chenyu Tang et al. "Wireless Silent Speech Interface Using Multi-Channel Textile EMG Sensors
   Integrated into Headphones." arXiv:2504.13921, 11 Apr 2025; published *IEEE Trans. Instrum. Meas.*
   2025, doi:10.1109/TIM.2025.3583386. https://arxiv.org/abs/2504.13921 (full PDF fetched)
4. Michael T. Knierim, Max Schemmer, Monica Perusquía-Hernández. "Exploring the Recognition of Facial
   Activities Through Around-the-Ear Electrode Arrays (cEEGrids)." *Information Systems and
   Neuroscience: NeuroIS Retreat 2021*, Springer, pp. 47–55, 2021. doi:10.1007/978-3-030-88900-5_6.
   https://publikationen.bibliothek.kit.edu/1000131815 (abstract page fetched)

**Non-Audible Murmur (NAM) and in-ear/behind-ear microphones**

5. M. Nakajima, H. Kashioka, K. Shikano, N. Campbell. "Non-audible murmur recognition."
   *Eurospeech 2003*. https://www.isca-archive.org/eurospeech_2003/nakajima03_eurospeech.html
   (PDF fetched)
6. P. Heracleous, H. Nakajima, S. Lee, H. Saruwatari, K. Shikano. "Non-Audible Murmur (NAM) Speech
   Recognition Using a Stethoscopic NAM Microphone." *Interspeech 2004*, doi:10.21437/Interspeech.2004-559.
   https://www.isca-archive.org/interspeech_2004/heracleous04_interspeech.pdf (full PDF fetched)
7. "Remodeling of the Sensor for Non-Audible Murmur (NAM)." *Interspeech 2005*.
   https://www.isca-archive.org/interspeech_2005/nakajima05_interspeech.pdf (full PDF fetched)
20. Andrea Ferlini, Dong Ma, Robert Harle, Cecilia Mascolo. "EarGate: Gait-based User Identification
   with In-ear Microphones." *ACM MobiCom 2021/2022*, doi:10.1145/3447993.3483240.
   https://ar5iv.labs.arxiv.org/html/2108.12305 (full text fetched)

**Ear-canal deformation, in-ear acoustic and gesture sensing**

8. Jin, Gao, Xu, Choi, Li, Liu, Li, Jin. "EarCommand: 'Hearing' Your Voice Commands by Listening to
   Your Ear Canal Deformations Using Wireless Earphones." *Proc. ACM IMWUT* 6(2), 2022,
   doi:10.1145/3534613. https://api.crossref.org/works/10.1145/3534613 (abstract fetched)
9. Xue Sun, Jie Xiong, Chao Feng, Haoyu Li, Yuli Wu, Dingyi Fang, Xiaojiang Chen. "EarSSR: Silent
   Speech Recognition Using Earphone." *IEEE Trans. Mobile Computing* 23(8):8493–8507, 2024,
   doi:10.1109/TMC.2024.3356719. https://chaof94.github.io/Papers/EarSSR.pdf (full PDF fetched)
10. Prakash, Yang, Wei, Hassanieh, Choudhury. "EarSense: Earphones as a Teeth Activity Sensor."
    *ACM MobiCom 2020*, doi:10.1145/3372224.3419197.
    https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3372224.3419197 (abstract fetched)
11. Wang, Tan, Zhang, Ren, Wang, Yang. "EarDynamic: An Ear Canal Deformation Based Continuous User
    Authentication System." *Proc. ACM IMWUT* 5(1), 2021, doi:10.1145/3448098.
    https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3448098 (abstract fetched)
12. Khanna, Srivastava, Pan, Jain, Nguyen. "JawSense: Enabling Unvoiced Jaw Movement Tracking with
    Ear-Worn IMUs." *ACM HotMobile 2021*, doi:10.1145/3446382.3450270.
    https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3446382.3450270 (abstract fetched;
    no accuracy/users in abstract — unverified)
13. Yetong Cao, Chao Cai, Anbo Yu, Fan Li, Xiaochen Li, Jun Luo. "CanalScan / Tongue-Jaw Movement
    Recognition Through Acoustic Sensing on Smartphones." *IEEE Trans. Mobile Computing* 2024,
    doi:10.1109/TMC.2022.3222594. https://yetongcao.github.io/files/CanalScanTMC-Final.pdf (full PDF
    fetched)
14. Dong Ma, Andrea Ferlini, Cecilia Mascolo. "OESense: Employing Occlusion Effect for In-ear Human
    Sensing." *ACM MobiSys 2021*, doi:10.1145/3458864.3467680.
    https://www.repository.cam.ac.uk/items/5eaa0508-e58e-4d64-a8d7-b2c00f690dee (abstract fetched)
15. Li, Zhang, Liang, Guimbretière, Zhang. "EarIO: A Low-power Acoustic Sensing Earable for
    Continuously Tracking Detailed Facial Movements." *Proc. ACM IMWUT* 6(2), 2022,
    doi:10.1145/3534621. https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3534621
    (abstract fetched)
16. Dong, Chen, Nishiyama, Sezaki, Wang, Christofferson, Mariakakis. "ReHEarSSE: Recognizing
    Unheard-ear Secret Speech." *ACM CHI 2024*, doi:10.1145/3613904.3642095.
    https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3613904.3642095 (abstract fetched)
17. Dong, Xu, He, Han, Christofferson, Chen, Taya, Nishiyama, Sezaki. "HEar-ID: ..." arXiv:2512.16518,
    2025. https://ar5iv.labs.arxiv.org/html/2512.16518 (full text fetched)
18. Hiraki, Rekimoto. "SilentWhisper." *ACM CHI EA 2025*, doi:10.1145/3706599.3721185.
    https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3706599.3721185 (abstract fetched;
    accuracy/users unverified)
19. Hiraki, Kanazawa, Miura, Yoshida, Mochimaru, Rekimoto. "WhisperMask." *ACM AH 2024*,
    doi:10.1145/3652920.3652925. https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3652920.3652925
    (abstract fetched)

**Companies**

21. The Subvocal Company. "Murmur — Control your computer in silence." https://subvocal.company/
    (site fetched)
22. Y Combinator. "The Subvocal Company" company page (Fall 2026). 
    https://www.ycombinator.com/companies/the-subvocal-company (page fetched)

**Hearing-aid form factors, batteries, fabrication, electronics, bone conduction**

23. NIDCD (NIH). "Hearing Aids," NIH Pub. 99-4340, updated 11 Oct 2022.
    https://www.nidcd.nih.gov/health/hearing-aids
24. Starkey. "Hearing aid styles." https://www.starkey.com/hearing-aids/styles
25. MicroBattery (Micropower Battery Company). "Hearing Aid Battery Guide."
    https://www.microbattery.com/hearing-aid-battery-guide
26. MicroBattery. "Rechargeable Hearing Aid Batteries."
    https://www.microbattery.com/hearing-aid-batteries/rechargeable.html
27. Formlabs. "Biocompatible Resin for Audio Applications," 24 Sep 2020.
    https://formlabs.com/eu/blog/biocompatible-audio-applications/
28. Formlabs. "Using BioMed Clear Resin." https://formlabs.com/ch/support/Using-BioMed-Clear-Resin/
29. Texas Instruments. "ADS1299 — 8-channel, 24-bit ADC for EEG/ECG." https://www.ti.com/product/ADS1299
30. Intan Technologies. "RHD2000 Amplifier Chips." https://intantech.com/products_RHD2000.html
31. OpenBCI. "Cyton Specs." https://docs.openbci.com/Cyton/CytonSpecs/
32. Aarhus University. "Aarhus University opens the world's first centre for ear-EEG," 20 Dec 2019.
    https://ece.au.dk/en/currently/news/show/artikel/aarhus-university-opens-the-worlds-first-centre-for-ear-eeg-2
33. IDUN Technologies. "IDUN Guardian Earbuds" docs and product specifications.
    https://docs.idunguardian.com/en/page-1a-igeb ; https://docs.idunguardian.com/en/page-1g-product-specifications ;
    https://iduntechnologies.com/ (all fetched)
34. University of Southampton, AIS Device Choice. "The design, size, fit and weight of the processor."
    https://aisdevicechoice.soton.ac.uk/thinking-about-my-lifestyle-bchi/the-design-size-fit-and-weight-of-the-processor/

**In-ear / ear-canal electrophysiology (hardware and artifacts)**

35. Lepold, Röddiger, King, Kunze, Maurer, Beigl. "OpenEarable ExG: Open-Source Hardware for
    Ear-based ExG Sensing." *UbiComp Companion 2024*. https://ar5iv.labs.arxiv.org/html/2410.06533v1 ;
    code: https://github.com/OpenEarable/open-earable-ExG (full text fetched)
36. Mikkelsen, Kappel, Mandic, Kidmose. "EEG Recorded from the Ear: Characterizing the Ear-EEG
    Method." *Front. Neurosci.* 9:438, 2015. https://pmc.ncbi.nlm.nih.gov/articles/PMC4649040/
37. Bleichner, Debener. "Concealed, Unobtrusive Ear-Centered EEG Acquisition: cEEGrids for Transparent
    EEG." *Front. Hum. Neurosci.* 11:163, 2017. https://pmc.ncbi.nlm.nih.gov/articles/PMC5383730/
38. Debener, Emkes, De Vos, Bleichner. "Unobtrusive ambulatory EEG using a smartphone and flexible
    printed electrodes around the ear." *Sci. Rep.* 5:16743, 2015. doi:10.1038/srep16743.
    https://api.semanticscholar.org/graph/v1/paper/DOI:10.1038/srep16743
39. Naox Technologies. FDA 510(k) K251550 summary (cleared 25 Nov 2025).
    https://fda.innolitics.com/submissions/NE/subpart-b-neurological-diagnostic-devices/OMC/K251550?doc=summary
40. Kappel, Looney, Mandic, Kidmose. "Physiological artifacts in scalp EEG and ear-EEG." *BioMed Eng
    OnLine* 16:103, 2017. doi:10.1186/s12938-017-0391-2.
    https://api.semanticscholar.org/graph/v1/paper/DOI:10.1186/s12938-017-0391-2 (abstract fetched;
    quoted sentence from record)
41. Avramidou, Derleth, Keller, Djilas, Launer, Hadjileontiadis. "From Ear-EEG to Ear-ExG: The Jaw
    Artifact is a Keeper." *ACM*, 2024. doi:10.1145/3696593.3696601.
    https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3696593.3696601 (abstract fetched)
42. Kappel, Rank, Toft, Andersen, Kidmose. "Dry-Contact Electrode Ear-EEG." *IEEE Trans. Biomed.
    Eng.* 66(1):150–158, 2019. doi:10.1109/TBME.2018.2835778.
    https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/TBME.2018.2835778 (abstract fetched)
43. Goverdovsky, Looney, Kidmose, Mandic. "In-Ear EEG From Viscoelastic Generic Earpieces."
    *IEEE Sensors J.* 16(1):271–277, 2016.
    https://pure.au.dk/portal/da/publications/in-ear-eeg-from-viscoelastic-generic-earpieces-robust-and-unobtru/
44. Bleichner, Kidmose, Voix. "Editorial: Ear-Centered Sensing." *Front. Neurosci.* 13:1437, 2020.
    https://pmc.ncbi.nlm.nih.gov/articles/PMC6979066/
45. Naqi Logix Inc. SEC Form 1-A/A, 26 Jun 2026.
    https://content-archive.fast-edgar.com/20260626/AK22G22CLZ22M96222ZF2ZY2HBWN2222O286/ea0294471-1aa1_naqi.htm
46. Cebreo Medical. "Cebreo Medical receives CE mark for NeuroBuds," press release, 15 Sep 2026.
    https://www.afp.com/en/agency/inside-afp/external-press-releases/cebreo-medical-receives-ce-mark-neurobudsr-discreet-ear
47. Neurable. "Neurable launches first smart brain-computer interface enabled headphones."
    https://www.neurable.com/news/neurable-launches-first-smart-brain-computer-interface-enabled-headphones-for-consumer-market
48. Mentalab. https://mentalab.com/
49. Emotiv. https://www.emotiv.com/

**Ear anatomy, muscles, montages, crosstalk, safety**

50. Voss et al. "Comprehensive Measurements and Analyses of Ear Canal Geometry From Late Infancy
    Through Late Adulthood." *Trends in Hearing* 29, 2025.
    https://pmc.ncbi.nlm.nih.gov/articles/PMC12198549/
51. Cao et al. "External auditory canal length measurement by HRCT 3-D centreline" (in Chinese).
    *Zhonghua Er Bi Yan Hou Tou Jing Wai Ke Za Zhi* 60(11):1431–8, 2025.
    https://pubmed.ncbi.nlm.nih.gov/41330587/
52. Singh et al. "Morphometry of the External Auditory Canal." *Indian J Otolaryngol Head Neck Surg*
    71(Suppl 2):1115–22, 2019. https://pubmed.ncbi.nlm.nih.gov/31750135/
53. Ikari et al. "Anatomy of the external auditory canal." *Ann Anat* 195(2):128–36, 2013.
    https://pubmed.ncbi.nlm.nih.gov/23036351/
54. Nguyen, Duong. "Anatomy, Head and Neck, Posterior Auricular Artery." StatPearls.
    https://pubmed.ncbi.nlm.nih.gov/31536293/
55. Das, Breiner. "Anatomy, Head and Neck: Auriculotemporal Nerve." StatPearls.
    https://pubmed.ncbi.nlm.nih.gov/31334960/
56. Rao, Tadi. "Anatomy, Head and Neck, Chorda Tympani." StatPearls.
    https://pubmed.ncbi.nlm.nih.gov/31536194/
57. Altafulla et al. "Great auricular nerve anatomy." *World Neurosurg* 125:e403–7, 2019.
    https://pubmed.ncbi.nlm.nih.gov/30703599/
58. Jeon et al. "Great auricular nerve lobular branch." *PLoS One* 14(10):e0222324, 2019.
    https://pmc.ncbi.nlm.nih.gov/articles/PMC6786628/
59. Hochreiter et al. "Auricular muscles: anatomy and sEMG." *Diagnostics* 13(3):554, 2023.
    https://pmc.ncbi.nlm.nih.gov/articles/PMC9914547/
60. Freitas et al. "Electromyography of the velum and articulators (electrode positions)." *PLoS One*
    10(6):e0127040, 2015. https://pmc.ncbi.nlm.nih.gov/articles/PMC4466523/
61. Salomons et al. "Electrode Setup for Electromyography-Based Silent Speech Interfaces: A Pilot
    Study." *Sensors* 25(3):781, 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC11821129/
    (MDPI landing page blocked; PMC full text fetched)
62. Latif, Meller. "Masseteric nerve landmarks." *Facial Plast Surg Aesthet Med* 28(4):394–403, 2026.
    https://pubmed.ncbi.nlm.nih.gov/40793952/
63. Rong, Pattee. "Jaw sEMG during speech (masseter/temporalis/digastric)." *Clin Neurophysiol* 2022.
    https://pubmed.ncbi.nlm.nih.gov/35033773/
64. Wang et al. "High-density sEMG of neck/face for speech." *IEEE EMBC 2020*.
    https://pubmed.ncbi.nlm.nih.gov/33018661/
65. Lapatki et al. "Perioral sEMG electrode array." *J Neurosci Methods* 123(2):117–28, 2003.
    https://pubmed.ncbi.nlm.nih.gov/12606061/
66. Zaretsky et al. "Optimal electrode positions for speech muscles." *Eur Arch Otorhinolaryngol*
    274(2):989–95, 2017. https://pubmed.ncbi.nlm.nih.gov/27581722/
67. Schroeer et al. "Posterior/superior auricular muscle sEMG." *J Neurophysiol* 2024.
    https://pubmed.ncbi.nlm.nih.gov/38896795/
68. Mai et al. "Posterior auricular muscle sEMG." *eNeuro* 2025.
    https://pubmed.ncbi.nlm.nih.gov/40998587/
69. Steiner et al. "Auricular muscle sEMG classification." *Diagnostics* 2024.
    https://pubmed.ncbi.nlm.nih.gov/39410562/
70. Vieira et al. "Surface EMG crosstalk and inter-electrode distance." *Sci Rep* 7:13300, 2017.
    https://pmc.ncbi.nlm.nih.gov/articles/PMC5643316/
71. Frahm et al. "Crosstalk in surface EMG: electrode size and IED." *Muscle Nerve* 46(2):228–36,
    2012. https://pubmed.ncbi.nlm.nih.gov/22806372/
72. Mesin et al. "Effect of inter-electrode distance on selectivity." *Med Eng Phys* 31(3):374–83,
    2009. https://pubmed.ncbi.nlm.nih.gov/18585945/
73. Mesin. "Nonlinear spatio-temporal filtering to reduce crosstalk." *J Neural Eng* 21(1), 2024.
    https://pubmed.ncbi.nlm.nih.gov/38277703/
74. Bell. "Otitis externa." *Postgrad Med* 78(3):101–4, 1985.
    https://pubmed.ncbi.nlm.nih.gov/4034442/
75. Ruddy, Bickerton. "Otitis externa." *Drugs* 43(2):219–35, 1992.
    https://pubmed.ncbi.nlm.nih.gov/1372220/
76. Bernheim, Sade. "Malignant external otitis and the osseous canal." *J Laryngol Otol* 103(4):366–8,
    1989. https://pubmed.ncbi.nlm.nih.gov/2715689/
77. Mihai et al. "In-ear EEG electrodes: review." *Sensors* 25(11):3321, 2025.
    https://research.chalmers.se/publication/547020
78. Farina et al. "Inter-electrode distance for a large muscle (trapezius)." *Eur J Appl Physiol*
    86(6):469–78, 2002. https://pubmed.ncbi.nlm.nih.gov/11944093/

**Ear-EEG decoding gradient, ear-region companies/patents, comparison results**

79. Geirnaert, Kappel, Kidmose. "Scalp, Around-Ear and In-Ear EEG for Neural Attention Decoding."
    arXiv:2505.14478, 2025. https://arxiv.org/abs/2505.14478 (full PDF fetched)
80. Kaongoen et al. "Speech-imagery-based brain–computer interface system using ear-EEG."
    *J. Neural Eng.* 18:016023, 2021, doi:10.1088/1741-2552/abd10e.
    http://nmail.kaist.ac.kr/paper/JNE2021.pdf (full PDF fetched)
81. "Sensing technologies for silent speech interfaces." *Nature Sensors* (2026).
    https://www.nature.com/articles/s44460-025-00010-2 (full PDF fetched)
82. StatPearls. "Anatomy, Head and Neck, Tympanic Membrane."
    https://pubmed.ncbi.nlm.nih.gov/28846242/
83. Srivastava, Tashev et al. "Whispering Wearables: Multimodal Approach to Silent Speech
    Recognition with Head-Worn Devices" (QuietSync). *ACM ICMI 2024*, doi:10.1145/3678957.3685720.
    https://www.microsoft.com/en-us/research/wp-content/uploads/2024/11/Microsoft_Silent_Speech_Recognition_ICMI_2024-672d5717ed40e.pdf
    (abstract fetched; PDF blocked)
84. van Oort, Sáenz, Tirtajana, Pawełczak. "EarMag: In-ear magnetosensing." *UbiComp Companion
    2025*, doi:10.1145/3714394.3757254.
    https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3714394.3757254 (abstract fetched)
85. Arnav Kapur, Shreyas Kapur, Pattie Maes. "AlterEgo: A Personalized Wearable Silent Speech
    Interface." *ACM IUI 2018*, pp. 43–53. https://www.media.mit.edu/publications/alterego-IUI/
86. Wispr AI Inc. US20240221738A1 / US12482449B2, "Wearable speech input device" (ear hook, EMG
    silent speech). https://patents.google.com/patent/US20240221738A1/en
87. Naqi Logix Inc. US20260037066A1, "Earbud sensory assembly" (published 2026-02-05).
    https://patents.google.com/patent/US20260037066A1/en
88. Entrepreneur News Network. "Aarush Yadav, Subvocal Company, $1.3M AI wearable," 30 Sep 2026.
    https://entrepreneurnewsnetwork.com/2026/09/30/aarush-yadav-subvocal-company-1-3-million-ai-wearable/
89. Spacone, Benini et al. "SilentWear: textile neck EMG silent speech." arXiv:2603.02847, Mar 2026.
    https://arxiv.org/abs/2603.02847
90. Hossain et al. "Temporalis and ear-canal mechanical sensing during chewing." *IEEE Sensors J*
    20(10):5379–88, 2020. https://pubmed.ncbi.nlm.nih.gov/33746621/
91. AlterEgo (company). https://www.alterego.io/ (site fetched; specs unverified)

## Key takeaways for the build

1. **The ear is the best concealment site and a jaw sensor.** Around-ear and in-ear electrodes
   demonstrably capture jaw/masseter activity [40][41][35], and canal deformation tracks jaw motion
   (EarSSR 93% word, EarCommand WER 10.02%) [9][8]. They do **not** demonstrably capture tongue/lip
   articulation well enough for free text; no source decodes words from in-ear EMG.
2. **Around-ear cEEGrid is the reference electrode layout.** AESSI: 18 channels, 1 kHz, 24 users,
   **92.24%** on 25 Mandarin sentences cross-day without test-day calibration (chance 4.00%) [1];
   Inoue: 16 channels, 125 Hz, **56.6% offline / 47.2% online** on 64 words with mixed EEG+EMG [2].
   Both are silent articulation (mouthed), not pure imagery.
3. **Command vs dictation must be budgeted separately.** Every ear result ≥89% is closed-set
   (10–100 words/commands) [3][9][8][16][17]; the only multi-word ear numbers are 47.2–56.6% [2].
   Plan a command vocabulary first.
4. **The behind-ear contact microphone is the sleeper option.** NAM gives **93.5–93.9% word
   accuracy on a 20k vocabulary** [6][7] from a mastoid-coupled mic — far better than any electrode
   result — but the user must actually articulate a murmur (inaudible to nearby listeners [5]), not
   merely think.
5. **Pure ear-EEG speech imagery is weak today.** 5-class imagery: **38.2%** ear-EEG vs 43.1%
   scalp-EEG against 20% chance [80]; ear-EEG decoding degrades scalp (83.4%) → around-ear (67.2%)
   → in-ear (61.1%) [79]. Do not plan a mind-reading build.
6. **Earphone-based canal sensing needs no electrodes or adhesive** (it reuses the earphone's own
   speaker and mic), but it is fit-critical: EarSSR word accuracy falls **93% → 72%** with a shallow
   fit and it has no sentence-level mode [9].
7. **The electronics/shell constraint is real.** A size-10 cell is **5.8 × 3.6 mm / 100 mAh** [25],
   while the stock ADS1299 is **12 × 12 mm** [29]. Put the AFE/radio/battery in a BTE/RIC pod and only
   electrodes or a mic in the canal; use Intan bare die if in-canal processing is required [30].
   Formlabs BioMed Clear is the one documented biocompatible hard-shell resin (ISO 10993, USP VI)
   [27][28]; electrode co-printing into soft silicone is unverified.
8. **Canal safety is not optional.** The bony canal has thin skin over bone and is where malignant
   otitis externa concentrates [76]; hearing aids predispose to otitis externa [74][75]; in-ear
   electrode reviews name anatomical variability and long-term wear as unsolved [77]. Avoid the great
   auricular nerve (~31 mm below the ear, lobular branch ~4.5 mm deep [57][58]) and the posterior
   auricular artery [54]. Behind-ear subdermal electrode safety is **unverified** in this work.
9. **Recommended ear build:** one BTE pod containing around-ear/concha ExG **plus** a mastoid contact
   mic, with 2–4 small dry electrodes (8 mm IED keeps perioral crosstalk <25% [65]); add the thin
   under-jaw strip to digastric/submental only if the ear-only tongue/lip test fails [61][2].
10. **First experiment:** one ~1 h session on an OpenBCI Cyton+Daisy (as in [2]) or OpenEarable ExG
    [35], 6–8 ear electrodes + 2 submental "truth" channels, testing rest / jaw clench / jaw
    open-close / tongue directions / "pa-ta-ka" / silent words. The go/no-go is **ear-only accuracy
    above chance on the tongue/lip conditions**, not on jaw (jaw will work).

## Open questions

1. **Does this user's ear-only array carry tongue/lip information at all?** No published study
   isolates this; the first experiment (§8.2) is designed to answer it directly.
2. **Is the around-ear cEEGrid signal mostly EMG or EEG?** Inoue et al. call it "cortical and
   articulatory EMG-related" [2] but never separate the two. If it is mostly jaw EMG, a cheaper
   myogenic-only front end may match it.
3. **Can dry in-ear electrodes support silent-speech decoding?** IDUN's dry sensor is specified at
   <200 kΩ [33] versus AESSI's required <20 kΩ gel [1]; no study has attempted silent-speech
   decoding with dry in-ear ExG.
4. **What is the true cross-day stability of a fixed custom earmold** (rather than re-applied gel
   cEEGrids)? AESSI measured electrode reapplication [1]; an earmold removes that variable but adds
   pressure/occlusion effects. Untested.
5. **Does modern ASR (Whisper-class) push NAM well past the 2004 HMM results** of 93.5–93.9% [6][7],
   and is the murmur genuinely inaudible to a person sitting 1 m away? Only the older papers report
   the inaudibility claim [5].
6. **Is there any safe, quantified behind-ear subdermal electrode path** (the brief's fallback)? No
   primary source was found; this needs a dedicated surgical/regulatory review.
7. **What is the best fusion of around-ear ExG + ear-canal deformation + mastoid NAM mic?** No study
   combines all three, and they are complementary (muscle, mechanics, acoustics).
8. **Do the Naqi [87] and Wispr AI [86] ear-region patents gate an ear-only dictation design**, or do
   they only cover micro-gestures / ear-hook EMG? Freedom-to-operate is unresolved.
