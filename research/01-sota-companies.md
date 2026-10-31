# Track 01 — State of the art and the companies

*Silent-speech interfaces (SSIs): what has actually been demonstrated, on what hardware, by whom,
and what companies claim as of late 2026. Inline `[n]` citations map to the numbered Sources list.
Every number is quoted as the source gives it. Demonstrated results are separated from company
claims, and anything I could not verify is marked **unverified**.*

## How to read this file

- **Demonstrated** = published in a paper/thesis/patent with a method, dataset and metric.
  **Claim** = marketing, press, or a product page.
- "Silent" is used inconsistently. Three distinct behaviours get called silent speech:
  1. **Internally articulated / subvocalised** — no sound, no externally observable muscle
     movement, often while not exhaling. This is what MIT's AlterEgo patent defines as *internally
     articulated speech* `[8]`, and what this project targets.
  2. **Silently mouthed / minimally articulated** — articulators move (possibly visibly); only
     sound is suppressed. Most "silent EMG" papers, including Gaddy & Klein, are this `[13]`.
  3. **Vocalised but quiet** — audible or near-audible; not silent.
- Almost every high-accuracy number is on a **small closed vocabulary** (tens of words). Open-
  vocabulary WER is a different, much harder problem. Do not compare the two.

---

## 1. MIT Media Lab AlterEgo (2018–2020)

### 1.1 The original IUI 2018 paper

A. Kapur, S. Kapur, P. Maes, *AlterEgo: A Personalized Wearable Silent Speech Interface*,
IUI 2018, pp. 43–53 `[1]`.

**Sensor front end (exact):**
- **7 channels**, "sourced … from the following areas – the laryngeal region, hyoid region, levator
  anguli oris, orbicularis oris, platysma, anterior belly of the digastric, mentum" `[1]`. The 7
  sites were selected "from an initial 30-point grid" `[6]`.
- A feature-ranked region list is also given: 1 Mental, 2 Inner laryngeal, 3 Outer laryngeal,
  4 Hyoid, 5 Inner infra-orbital, 6 Outer infra-orbital, 7 Buccal `[1]`.
- Two electrode types: TPE-plastic **gold-plated silver, 1.45 mm diameter** with **Ten20 paste**,
  or **passive dry Ag/AgCl, 4 mm diameter**. The pasted electrodes "offer superior data quality"
  and were used for all reported results `[1]`.
- **Reference** on the wrist or earlobe; **bias** electrode for ~60 Hz cancellation `[1]`.
- **Sampled at 250 Hz, differentially amplified at 24× gain (Texas Instruments, OpenBCI)** `[1]`.
  The 2018 S.M. thesis repeats "250 Hz … 24 gain" `[2]`. The ML4H 2020 follow-up adds that data
  was "digitized using 24-bit Analog-to-Digital converter and sampled at 250 Hz" `[5]`.
- **AFE part number:** none of the papers name a chip. The project's own code repository initialises
  `ADS1299_Vref = 4.5`, `ADS1299_gain = 24.0` and an 8-channel, 31-byte packet `[11]`, which
  indicates a **Texas Instruments ADS1299** (the ADC on OpenBCI boards). This is a code artefact,
  not a statement in the papers — treat the exact chip as **inferred, not officially confirmed**.
- Preprocessing: fourth-order IIR Butterworth **1.3–50 Hz**, hardware 60 Hz notch, then
  **Independent Component Analysis (ICA)** `[1]`. (The thesis states 1.3–10 Hz — a discrepancy
  between the two `[2]`.)
- Features: MFCC-style representation, **0.025 s** frames with **0.01 s** step; classified by a
  1-D CNN (400 filters, kernel 3, stride 1, ReLU, max-pool; repeated twice; FC 200; sigmoid), Adam,
  50% dropout, one Titan X GPU `[1]`.
- Output: **bone-conduction headphones**, making it a closed loop `[1]`.

**Data, vocabulary, and result:**
- Pilot **3 participants**, ~**5 h of internally vocalised text**; main corpus **~31 h of silently
  spoken text**, same 3 participants `[1]`.
- Evaluation vocabulary was **10 classes (digits 0–9)**; **10 participants (6 female, 19–31 y,
  μ = 23.6 y)**, each shown **750 digits** (each digit exactly 75 times), 80/20 split, **10 runs** `[1]`.
- Users were instructed to "read the number to themselves, **without producing a sound and moving
  their lips**" `[1]`.
- **Result:** "The average accuracy over all runs for all the users is **92.01%**" `[1]`. The
  abstract summarises this as "**92% median word accuracy**" `[1]` — the paper uses both wordings.
  Average live latency: **0.427 s** `[1]`.
- The S.M. thesis reports the same **92.01% for a 10-word vocabulary** and an information transfer
  rate of **10.302 ± 1.47 bits/s** (max 11.913, min 7.639) `[2]`.
- Other vocabulary sets demonstrated but not the headline: IoT commands, world-clock cities,
  calendar, chess moves, reply phrases `[1]`.

**Honest reading:** a **closed-vocabulary, 10-class digit task**. The paper says accuracy is "at par
with … state-of-the-art speech recognition systems … albeit on smaller vocabulary sets" `[1]`.

### 1.2 The continuous-speech and clinical follow-ups (2019 M.Eng. theses)

Two MIT M.Eng. theses extend AlterEgo from isolated words to continuous sentences and to patients:

- **Wadkins, "A Continuous Silent Speech Recognition System for AlterEgo" (2019)** `[3]`: single-
  speaker continuous silent speech. Reported results (their Table 5.1): 10-word/20-sentence
  vocabulary **0.933** single-label accuracy / **0.115** CNN+CTC error / **0.070** with a language
  model; 20-word/200-sentence vocabulary **0.827** / **0.148** / **0.107**. The thesis states
  "transcribing continuous silent speech at a rate of over **100 words per minute**", a 20-word
  average of **102.4 WPM**, a **10.7% word error rate**, and **345.8 bits per minute** `[3]`.
  (The thesis also quotes 11.4% and 16.4% elsewhere — an internal inconsistency; flag both `[3]`.)
- **Wu, "AlterEgo as a Speech Interface for ALS Patients" (2019)** `[4]`: 5 ALS patients and 3 MS
  patients; ALS validation scores averaged ~**70%**, "with many scores in the high seventies and up
  to **100%**"; MS averaged **54%** (range 31–83%). The device could "distinguish between about
  10 words with over 90% accuracy when given a 15 minutes training period" `[4]`. Wu's clinical
  conclusion was that ALS was the best-suited condition and quick, urgent communication the best
  application `[4]`.
- There is **no peer-reviewed ALS paper** from the group (2021–2023); the ALS data exists only in
  Wu's 2019 thesis `[4]`. Mark the "ALS clinical paper" as **unverified / does not appear to exist**.

### 1.3 The clinical paper: MS with dysphonia (ML4H 2020)

A. Kapur, U. Sarawgi, E. Wadkins, M. Wu, N. Hollenstein, P. Maes, *Non-Invasive Silent Speech
Recognition in Multiple Sclerosis with Dysphonia*, PMLR 116:25–38, 2020 `[5]`.

- **8 signal electrodes: 4 on the face and 4 on the neck**, plus reference and bias on each
  earlobe `[5]`. (Down from 8 in the lab; the ALS thesis used 6 `[4]`.)
- Dataset: **3 MS patients with dysphonia**, 15 sentence classes × 10 trials each; recordings
  30–40 min; per-patient test accuracy **0.79 (±0.01), 0.87 (±0.01), 0.77 (±0.02)**; mean **0.81**
  at a mean **203.73 bits/min** (per-patient 223.15 / 227.39 / 160.66) `[5]`.
- "Silent speech refers to the act of minimally articulating words without producing sounds"; the
  authors "allowed minimal movements during articulation as per the comfort of patients" `[5]`.
  This is **minimal articulation, not strict zero-movement internal speech**.

### 1.4 The AlterEgo patent — the clearest definition of "silent"

US application **US20190074012A1**, "Methods and Apparatus for Silent Speech Interface" (published
2019-03-07), granted as **US10878818** ("10,878,818", issued 2020-12-29) `[7][8]`.

- **"Internally articulated speech"** = speech that "(a) occurs without any audible sound of speech
  and without any visible movement of any muscle of the person's face or neck; and (b) occurs at
  least partially when the person is not exhaling" `[8]`.
- Measured signal at the electrodes: RMS **≥ 8 µV and ≤ 20 µV** in the illustrated configuration `[8]`.
- Claimed electrode regions: **mental (chin), oral (lips), infraorbital, buccal (maxillary),
  submental, submaxillary, hyoid, carotid fossa**; reference on ear or arm `[8]`. (These are the
  *patent's* claimed regions; the *papers* name only the 7 sites in §1.1. Masseter, temporalis,
  zygomaticus and submental do **not** appear in the AlterEgo papers `[1][2][3][4][5]`.)
- Prototype section repeats **250 Hz, 24× gain**, 1.3–50 Hz Butterworth, ICA, 1-D CNN,
  **3 participants (1 female, mean age 29.33)** `[8]`.
- Wearable: a **curved structure supported by the ear**, a **bone-conduction transducer behind the
  ear**, and a **clip-on extension** housing jawline/oral/mental electrodes `[8]`.
- Claim 1 is broad: head/neck skin electrodes + analysis to recognise internally articulated speech,
  "wherein at least a portion … occurs when the user is not exhaling" `[8]`.

### 1.5 What the MIT project page says today

The project page describes AlterEgo as a non-invasive wearable peripheral neural interface enabling
conversation "without opening their mouth, and without externally observable movements — simply by
articulating words internally", with bone-conduction feedback, targeting ALS and MS `[6]`. It states
the project "originated at the MIT Media Lab in 2018 and **spun off as a for-profit company in early
2025**" `[6]`.

---

## 2. The AlterEgo company (2025 spin-out)

- **Spun off in early 2025** from the MIT Media Lab `[6]`; the TLO page marks the IP
  "**Exclusively Licensed**" `[7]`. A 2025-04-21 assignment of US10878818 to "AlterEgo AI, Inc. +
  MIT" is listed on Google Patents (reported; Google Patents blocked automated fetching during this
  research, so treat the exact date as **unverified**).
- **Public unveiling 8 September 2025**; presentation at the Axios AI+ Summit, Washington D.C.,
  17 September 2025 `[9]`.
- **Form factor (press, not a datasheet):** a "wearable headset [that] hooks around the ear and
  runs along the jawline" `[10]` — consistent with the ear-supported curved structure plus clip-on
  electrode extension in the patent `[8]`. It "detects faint neuromuscular signals in the face and
  throat when a person internally verbalizes words", decoded by ML, responses delivered over
  bone-conduction audio `[9]`.
- **People:** Arnav Kapur, CEO; **Max Newlon, COO**, previously at BrainCo `[10]`.
- **Funding:** "AlterEgo has **not disclosed details about funding**, launch timing, or
  commercialization strategy" `[9]`. A startup profile lists MMoth Fund and MIT Media Lab as
  investors with no amount (**unverified**) `[10]`.
- **Claims:** "world's first near-telepathic wearable" `[10]`; ALS accessibility and human
  augmentation `[10]`. Kapur: "AlterEgo isn't about reading your mind… It's about creating a private
  channel between you and the digital world" `[10]`.
- **No public accuracy/WER, vocabulary size, channel count, or sample rate has been released.** The
  last peer-reviewed data remains the 2018–2020 MIT work `[1][5]`. Do not assume the 92% digit
  accuracy transfers to the 2025 product.

---

## 3. Meta / CTRL-labs — the sEMG wristband (Nature 2025)

P. Kaifosh, T. R. Reardon & CTRL-labs at Reality Labs, *A generic non-invasive neuromotor interface
for human–computer interaction*, Nature 645(8081):702–711, 23 July 2025, DOI
10.1038/s41586-025-09255-w `[12]`. This is the most rigorous large-scale non-invasive neuromotor
result to date, but it is **not silent speech** — it decodes no speech at all.

**Hardware (exact):** **48 pogo-pin dry electrodes** (gold-plated brass, 6.5 mm) into **16 bipolar
sEMG channels**; paired-sensing spacing 20 mm centre-to-centre; circumferential spacing 10.6/12/13/15
mm across four band sizes; **2000 Hz per channel**; input-referred noise **2.46 µVrms**; analog gain
~190; ADC full-scale 2.5 V; **~65.5 dB** dynamic range; input impedance ~10 TΩ; dry, no gel; Bluetooth;
**>4 h** battery; IMU present but unused `[12]`.

**Scale:** demographic total **n = 11,236**; training corpora of **162 (wrist), 4,900 (discrete
gestures), 6,627 (handwriting)** participants; online naive test n = 17 / 24 / 20 `[12]`.

**Demonstrated:** offline "**greater than 90% classification accuracy for held-out participants in
handwriting and gesture detection**", wrist-angle-velocity error "**less than 13° s⁻¹**"; online
median **0.66 target acquisitions/s**, **0.88 gesture detections/s**, **handwriting 20.9 WPM**;
personalisation improves handwriting "by **16%**" `[12]`.

**Why it matters here:** it proves a **dry-electrode wristband** can generalise **across thousands of
people without per-person calibration**, and that performance scales as a **power law with data and
parameters** `[12]`. It validates the engineering pattern (dry electrodes, high sample rate, generic
model, optional personalisation) — not the silent-speech application.

---

## 4. Other companies in the space

**Augmental (MouthPad)** — an intraoral **tongue + head-movement trackpad**, **not silent-speech
decoding** `[20]`. MIT Media Lab spin-off; raised a **$4M seed** (Forbes, Oct 2024, listed on
Augmental's news page) `[20]`; CES 2025 Innovation Award honoree `[20]`; went on public US sale on
22 July 2026 and introduced **VOX**, "a privacy-first microphone pendant for voice-driven computing"
`[20]`. In Jan 2024 TechCrunch reported Augmental "is working on head tracking and 'silent speech'"
`[22]` — no silent-speech product or accuracy number has been published. Note the mouthpiece is
**inside the mouth**, the opposite of "barely different from a normal face" for many users.

**Wispr — pivoted away from silent speech.** Founded 2021 for wearables + silent speech, it pivoted
to the **voiced dictation app Wispr Flow** `[19][26]`. It raised **$280M in a Series B** announced
17 Aug 2026, led by Menlo Ventures, total capital **$361M**; revenue grew "more than 150% in each of
the past four quarters"; used across "more than 125,000 businesses" `[19]`. Dealroom's headline says
"$2B valuation" while its body text says "$1.29B valuation" — **the two conflict; quote both** `[19]`.
Alongside the raise Wispr previewed **Canto**, a speech model it says "cuts word error rates from
over 30% to roughly 5% to 10% in difficult conditions" `[19]`. That is **voiced ASR, not silent
speech**.

**The Subvocal Company** — Y Combinator-backed startup (Fall 2026), founded by Georgia Tech students
Aarush Yadav and Arnav Kumar `[21]`. A **behind-the-ear wearable** that "pick[s] up bio signals
around your face" and uses a "proprietary foundation thought-to-text AI model" `[21]`. It "secured a
**$500k pre-seed** … from … Afore Capital" `[21]`; a separate report adds YC's $500k for ~$1.3M total
(**unverified**) `[21]`. **Demonstrated (per Georgia Tech):** "a working letter-level prototype that
can spell out words using your thoughts at **30 words per minute**" `[21]`. A press item claiming
"above 200 words per minute" conflicts with the 30 WPM figure and is **unverified** `[21]`.

**Q.ai / Q (Cue) Ltd. (Israel)** — **camera + audio + ML** analysis of facial "micromovements" for
whispered/silent speech; CEO Aviad Maizels. **Acquired by Apple** around Jan/Feb 2026 in a reported
**~$1.6–2B** deal (TNW headline "$2B") `[23]`. This is an off-body **optical** approach, so it is
occlusion/lighting sensitive. The deal was confirmed by press coverage but no technical paper or
product spec is public.

*The following four items come from a secondary company/patent sweep and were **not independently
verified** against their primary pages in this research; treat as leads.* **Altavo GmbH (Dresden)** —
radar/ultrasound vocal-tract sensing plus artificial-voice synthesis, a TU Dresden spin-off, research
stage `[25]`. **Naqi Logix** — an in-ear "silent and invisible interface" (EMG + EEG + ECG + IMU)
triggered by facial micro-gestures; a Reg A+ filing reportedly seeks up to $18,525,000 `[25]`.
**Voiceitt** — acoustic ASR for **non-standard/dysarthric** speech; **not silent speech** `[25]`.

**Adjacent implant players (not this project's target, but the benchmark to beat; secondary reports,
not independently verified here):** Blackrock Neurotech's penetrating array with AI TTS reportedly
restored speech for an ALS patient at **97% accuracy and a 125,000-word vocabulary** (Aug 2024) `[27]`;
Paradromics reported real-time speech in its first participant (Sept 2026) `[28]`; Neuralink's VOICE
study targets **140 WPM** versus academic BCI ~18 WPM (Sept 2026) `[29]`. These are invasive and are
covered in more depth by the implant track.

---

## 5. Academic state of the art in silent speech

### 5.1 Gaddy & Klein — "Digital Voicing of Silent Speech" (EMNLP 2020, Best Paper)

D. Gaddy, D. Klein, EMNLP 2020, pp. 5521–5530, arXiv:2010.02960 `[13]`.

- Task = **digital voicing**: synthesise audible speech from silent facial/neck sEMG, then transcribe
  it. The WER is the intelligibility of the synthesised audio, **not** direct EMG-to-text `[13]`.
- Dataset: **surface EMG, one speaker, ~18.6 h**. Closed vocabulary 500 utterances, **67 words**;
  open vocabulary (Project Gutenberg) 3.6 h silent + 3.9 h vocalised + 11.2 h non-parallel
  vocalised = **18.6 h**, **9,828 words** `[13]`.
- Hardware: **OpenBCI Cyton, 8 channels at 1000 Hz**, gold-plated + Ten20 paste, monopolar, shared
  reference behind one ear, bias behind the other `[13]`. (Compare AlterEgo 250 Hz `[1]`.)
- **Exact WER:** closed-vocabulary human transcription **3.6%** (baseline 88.8%, no-throat 64.6%);
  open-vocabulary automatic **68.0%** (baseline 91.2%, no-throat 88.0%, without CCA 69.8%, without
  audio alignment 76.5%; ASR on the original audio 9.5% lower bound); open-vocabulary human **74.8%**
  (baseline 95.1%) `[13]`.
- The headline "64% → 4%" is the **closed-vocabulary date/time domain**; open vocabulary is 68% WER.

### 5.2 Gaddy & Klein — "An Improved Model for Voicing Silent Speech" (ACL-IJCNLP 2021)

D. Gaddy, D. Klein, ACL-IJCNLP 2021 short papers, pp. 175–181 `[14]`.

- Raw EMG + convolutional front end + Transformer layers + an auxiliary phoneme-prediction task;
  EMG resampled 1000 → 800 Hz `[14]`.
- **Open-vocabulary automatic WER 42.2%, improved from 68.0% — an absolute 25.8% reduction** `[14]`.
- Human intelligibility: **36.1% and 28.5% WER (average 32.3%)** `[14]`. Same single speaker `[14]`.

### 5.3 Benster et al. — MONA LISA (2024, arXiv preprint)

T. Benster, G. Wilson, R. Elisha, F. R. Willett, S. Druckmann, *A Cross-Modal Approach to Silent
Speech with LLM-Enhanced Recognition*, arXiv:2403.05583, 2 Mar 2024 `[15]`. **Peer review status:
arXiv preprint only.**

- **Modality: surface EMG, not ultrasound**, reusing the Gaddy & Klein (2020) dataset plus
  LibriSpeech `[15]`. **One participant**; open vocabulary `[15]`.
- Method: MONA cross-modal contrastive losses align EMG with audio; **LISA** prompts GPT-3.5 / GPT-4
  with the top-k beam candidates and asks it to pick the coherent one `[15]`.
- **Exact WER:** silent EMG **28.8% → 12.2%**; vocal EMG **23.3% → 3.7%**; their own baseline was
  30.4% silent / 15.1% vocal on validation; Brain-to-Text 2024 **9.8% → 8.9%** `[15]`.
- Claim: "first instance where noninvasive silent speech recognition on an open vocabulary has
  cleared the threshold of **15% WER**" `[15]`. Part of the gain is **language modelling**, not
  better sensing.

### 5.4 EMG-UKA corpus and the KIT/Bremen line (Wand, Schultz et al.)

M. Wand, M. Janke, T. Schultz, *The EMG-UKA Corpus for Electromyographic Speech Processing*,
Interspeech 2014 `[16]`.

- **6-channel** gelled Ag/AgCl setup (4 mm) over six articulatory muscles: levator anguli oris
  (ch 2,3), zygomaticus major (2,3), platysma (4,5), depressor anguli oris (5), anterior belly of
  the digastric (1), tongue (1,6); reference on nose / behind ears; ground on wrist `[16]`.
- Recorder Varioport (Becker Meditec): amplification **1170**, 16-bit, 0.033 µV/bit, 0.9–295 Hz,
  **600 Hz** sampling; audio 16 kHz `[16]`.
- Corpus: **63 sessions, 8 speakers**, English, three speaking modes (**audible, whispered,
  silent**), parallel 50-sentence blocks `[16]`.
- Reference WER: audible small sessions **22.82%**, large **12.00%**; by mode, session-dependent
  totals **audible 26.90%, whispered 28.19%, silent 48.29%** `[16]`. Silent speech is roughly twice
  the error of audible on the same corpus — a clean quantification of the silent-speech penalty.

### 5.5 Gowda & Miller — direct EMG-to-text without audio (2025/2026)

H. T. Gowda, L. M. Miller (UC Davis), *Non-invasive electromyographic speech neuroprosthesis: a
geometric perspective*, arXiv:2502.05762 v3, 20 Apr 2026 `[17]`.

- **31 monopolar electrodes** across neck, chin, jaw, cheek and lips; **actiCHamp Plus** amplifier,
  **5000 Hz** sampling; ground on left earlobe, reference on right `[17]`.
- Dataset: **~8 h silent-speech EMG from one healthy participant**, **>6,500 unique words**, 11,000
  sentences (training 8,000 / validation 1,000 / test 1,970) `[17]`.
- **Direct sequence-to-sequence EMG-to-text with no time-aligned audio**, using SPD covariance
  matrices + BiGRU + CTC, decoded with a WFST language model `[17]`.
- **Result: mean PER 48.47%, mean WER 73.53%** on the 1,970-sentence open-vocabulary test set; a
  spectrogram baseline gave **89.25% PER / 100% WER** `[17]`. The authors explicitly caution that
  these WERs "should not be compared one-to-one" with Gaddy/Benster because the settings differ `[17]`.
- They also note Littlejohn et al. (2025) report **74% WER** on the Gaddy & Klein dataset `[17]`.

### 5.6 The modality landscape (Nature Sensors review, Jan 2026)

C. Tang et al., *Sensing technologies for silent speech interfaces*, Nature Sensors 1:16–26, 2026
`[18]` — a peer-reviewed review that is useful for comparing approaches. Selected exact numbers:

| Modality (all on/off-body) | Reported result |
|---|---|
| Depth camera, 30 commands | **91.3% within-user, 74.9% cross-user** accuracy |
| Ultrasound tongue imaging | **3.6 s decoding speed, ~33% WER**, several dozen commands |
| Smartphone acoustic (inaudible echoes) | **>90% word-level, <10% sentence-level WER** |
| Glasses/earbuds/headphones acoustic | **>90% accuracy on >100 words** |
| Facial accelerometer array | **94.65 ± 2.54%** on 40 English words |
| Differential IMU (articulator vs forehead/ear) | **92%** avg across 7 users, 93 sentences |
| TENG (triboelectric) lip array | **94.5%** on 20 words |
| Tattoo-like facial EMG | up to **110 words**, **92.6%** average |
| Textile EMG headphone earmuffs | **96%** on 10 words |
| Ultrathin silicon strain gauges | **87.53%** on 100 words |
| Ionic-hydrogel throat sensor | **95%** on 26 instructions |
| Textile strain choker | **95.25%** on 20 words |
| ECoG (invasive, benchmark only) | up to **78 words/min at ~25% WER** |

All from `[18]`. The review's conclusion: **on-body** systems currently offer the best balance of
accuracy and deployability; in-body gives unmatched neural access but is invasive `[18]`. Note the
pattern: nearly all sub-100-word results are **closed-vocabulary classification**; the only
open-vocabulary sentence results are the ~12–74% WER EMG systems in §5.1–5.5 `[13][14][15][17]`.

### 5.7 Other threads worth tracking

- **Self-supervised pretraining for EMG SSI** — "emg2vec" (IEEE, 2024/2025) applies self-supervised
  pretraining to EMG-based SSIs `[30]`; this is the most plausible route to reducing the per-user
  calibration burden that all the above systems share.
- **Soft/active EMG materials** — a 2025 Wiley paper on a soft active EMG interface for
  ML-enabled silent speech recognition `[30]`.
- **Wearable magnetometers for silent speech** (bioRxiv 2025) and **ultrasound-based silent
  conversation** (2026 press) `[25]` — early, unverified against peer review.

---

## 6. Comparison table

| System | Modality | Sensor sites | Channels | Vocab | Silent / mouthed | Result | Year |
|---|---|---|---|---|---|---|---|
| MIT AlterEgo IUI `[1]` | surface EMG | face/neck: laryngeal, hyoid, levator anguli oris, orbicularis oris, platysma, digastric, mentum | 7 | 10 digits (+ command sets) | internally articulated, no lip movement | **92.01%** avg word accuracy, 10 users, 0.427 s latency | 2018 |
| AlterEgo thesis `[2]` | surface EMG | same 7 | 7 | 10 words | internal articulation | 92.01%; **10.302 bits/s** ITR | 2018 |
| Wadkins thesis `[3]` | surface EMG | 8 (4 face, 4 neck) | 8 | 10–20 words | continuous silent | **10.7%** WER, **102.4 WPM**, 345.8 bits/min (20-word) | 2019 |
| Wu ALS thesis `[4]` | surface EMG | 6 face/neck | 6 | ~10 words | silent (trained ladder) | ALS ~**70%** avg (up to 100%); MS 54% | 2019 |
| ML4H MS clinical `[5]` | surface EMG | 8 (4 face, 4 neck) | 8 | 15 sentences | **minimally articulated** | **0.81** mean accuracy, **203.73 bits/min** | 2020 |
| AlterEgo patent `[8]` | surface EMG | mental, oral, infraorbital, buccal, submental, submaxillary, hyoid, carotid fossa | 7 prototype | n/a | internally articulated, may be non-exhaling | claims; RMS 8–20 µV; 250 Hz / 24× | 2019 |
| AlterEgo company `[9][10]` | surface EMG | ear-hook + jawline | undisclosed | undisclosed | "internally verbalizes" | **no public numbers**; claim only | 2025 |
| Meta/CTRL-labs `[12]` | surface EMG | wrist | 16 bipolar (48 pins) | 9 gestures + handwriting | **not speech** | >90% offline; **20.9 WPM** handwriting; 0.88 gestures/s | 2025 |
| Gaddy & Klein `[13]` | surface EMG | face/neck, 8 sites | 8 @ 1000 Hz | 67 / 9,828 | silently **mouthed** | **3.6%** closed human; **68.0%** open auto | 2020 |
| Gaddy & Klein `[14]` | surface EMG | same | 8 @ 800 Hz | 9,828 | silently mouthed | **42.2%** open auto; **32.3%** human avg | 2021 |
| MONA LISA `[15]` | surface EMG | Gaddy 8 | 8 | open | silently mouthed | **12.2%** silent / **3.7%** vocal (LLM) | 2024 |
| EMG-UKA baseline `[16]` | surface EMG | 6 articulatory muscles | 6 @ 600 Hz | 50-sentence blocks | audible / whispered / silent | silent WER **48.29%** vs audible **26.90%** | 2014 |
| Gowda & Miller `[17]` | surface EMG | 31 sites neck/chin/jaw/cheek/lips | 31 @ 5000 Hz | **>6,500 words** | silently voiced, **no audio targets** | **73.53%** WER / 48.47% PER | 2025/26 |
| Q.ai → Apple `[23][24]` | optical (camera) | face | n/a | n/a | whispered/silent | acquired ~$1.6–2B; no WER public | 2026 |
| Subvocal Company `[21]` | bio-signals (EMG) | behind the ear | undisclosed | letter-level | subvocalised | **30 WPM** letter-level prototype (self) | 2026 |
| Augmental MouthPad `[20]` | intraoral touch/IMU | inside mouth | n/a | gestures | **not speech** | shipping; $4M seed | 2024–26 |

---

## Sources

1. A. Kapur, S. Kapur, P. Maes, "AlterEgo: A Personalized Wearable Silent Speech Interface", IUI
   2018, pp. 43–53. PDF: https://dam-prod.media.mit.edu/x/2018/03/23/p43-kapur_BRjFwE6.pdf ; MIT
   page: https://www.media.mit.edu/publications/alterego-IUI/ (fetched 2026)
2. A. Kapur, "Human-Machine Cognitive Coalescence through an Internal Duplex Interface", S.M.
   thesis, MIT Media Arts and Sciences, 2018. https://dspace.mit.edu/handle/1721.1/120883
3. E. J. Wadkins, "A Continuous Silent Speech Recognition System for AlterEgo, a Silent Speech
   Interface", M.Eng. thesis, MIT EECS, 2019. https://dspace.mit.edu/handle/1721.1/123121
4. M. Wu, "AlterEgo as a Speech Interface for ALS Patients", M.Eng. thesis, MIT EECS, 2019.
   https://dspace.mit.edu/handle/1721.1/123009
5. A. Kapur, U. Sarawgi, E. Wadkins, M. Wu, N. Hollenstein, P. Maes, "Non-Invasive Silent Speech
   Recognition in Multiple Sclerosis with Dysphonia", PMLR 116:25–38, 2020.
   https://proceedings.mlr.press/v116/kapur20a.html
6. MIT Media Lab, "AlterEgo — Overview".
   https://www.media.mit.edu/projects/alterego/overview/ (fetched 2026)
7. MIT Technology Licensing Office, "Wearable Non-Invasive Silent Speech Interface" (fetched 2026).
   https://tlo.mit.edu/industry-entrepreneurs/available-technologies/wearable-non-invasive-silent-speech-interface
8. "Methods and Apparatus for Silent Speech Interface", US20190074012A1 (pub. 2019-03-07); granted
   US10878818 (2020-12-29). https://patentimages.storage.googleapis.com/21/c6/73/4ebe4f5637c730/US20190074012A1.pdf
9. MIT Media Lab / Decrypt, "'Near Telepathic' Wearable Lets You Communicate Silently With
   Devices", 8 Sept 2025.
   https://www.media.mit.edu/articles/exclusive-startup-lets-you-query-ai-with-silent-speech/
10. Fast Company SA, "AlterEgo launches world's first near-telepathic wearable", 11 Sept 2025.
    https://fastcompany.co.za/tech/2025-09-11-alterego-launches-worlds-first-near-telepathic-wearable-this-is-how-it-works/
11. GitHub, bigdatasciencegroup/AlterEgo, project code artifact (2020; ADS1299 constants in
    boston-home/data/serial_data.py). https://github.com/bigdatasciencegroup/AlterEgo
12. P. Kaifosh, T. R. Reardon, CTRL-labs at Reality Labs, "A generic non-invasive neuromotor
    interface for human-computer interaction", Nature 645(8081):702–711, 2025, DOI
    10.1038/s41586-025-09255-w. Open access: https://pmc.ncbi.nlm.nih.gov/articles/PMC12443603/
13. D. Gaddy, D. Klein, "Digital Voicing of Silent Speech", EMNLP 2020, pp. 5521–5530,
    arXiv:2010.02960. https://aclanthology.org/2020.emnlp-main.445/
14. D. Gaddy, D. Klein, "An Improved Model for Voicing Silent Speech", ACL-IJCNLP 2021, pp. 175–181.
    https://aclanthology.org/2021.acl-short.23/
15. T. Benster, G. Wilson, R. Elisha, F. R. Willett, S. Druckmann, "A Cross-Modal Approach to Silent
    Speech with LLM-Enhanced Recognition", arXiv:2403.05583, 2024.
    https://arxiv.org/abs/2403.05583
16. M. Wand, M. Janke, T. Schultz, "The EMG-UKA Corpus for Electromyographic Speech Processing",
    Interspeech 2014. https://www.isca-archive.org/interspeech_2014/wand14b_interspeech.pdf
17. H. T. Gowda, L. M. Miller, "Non-invasive electromyographic speech neuroprosthesis: a geometric
    perspective", arXiv:2502.05762 v3, 2026. https://arxiv.org/abs/2502.05762
18. C. Tang, L. Qi, S. Gao, Z. Zhang, W. Yi, M. Xu, E. Occhipinti, Y. Pan, L. G. Occhipinti, "Sensing
    technologies for silent speech interfaces", Nature Sensors 1:16–26, 2026, DOI
    10.1038/s44460-025-00010-2. https://www.nature.com/articles/s44460-025-00010-2
19. Dealroom, "Wispr Flow raises $280M at $2B valuation in Series B", 17 Aug 2026.
    https://dealroom.co/news/145354-wispr-flow-raises-280m-at-2b-valuation-in-series-b/
20. Augmental, "News & Press" (fetched 2026; lists MouthPad public + VOX, 22 July 2026, and the
    Forbes $4M seed, Oct 2024). https://www.augmental.tech/news
21. Georgia Tech Honors Program, "JMHP Student Secures $500k Seed Funding for Startup",
    29 Sept 2026.
    https://honors.gatech.edu/index.php/whats-happening/see-all-news/jmhp-student-secures-500k-seed-funding-startup
22. TechCrunch, "Accessibility startup Augmental is working on head tracking and 'silent speech'",
    10 Jan 2024. https://techcrunch.com/2024/01/10/augmental-head-tracking/
23. The Next Web, "Apple buys 'Silent Speech' AI startup for $2B, because talking is so 2025" (2026).
    https://thenextweb.com/news/apple-buys-silent-speech-ai-startup-for-2b-because-talking-is-so-2025
24. UC Today, "Apple Taps Q.ai Tech – Will Face-Controlled AI Change How We Use Devices?",
    2 Feb 2026 (supporting coverage; not directly cited).
    https://uctoday.com/apple-taps-q-ai-tech-will-face-controlled-ai-change-how-we-use-devices
25. Secondary company/patent sweep (2026) used for Altavo, Naqi Logix, Voiceitt, wearable-magnetometer
    and ultrasound items. Primary pages not all fetched; **treat as unverified leads**. Company pages:
    https://www.naqilogix.com/ ; https://www.voiceitt.com/
26. TechCrunch, "Wispr Flow raises $30M from Menlo Ventures for its AI-powered dictation app",
    24 June 2025.
    https://techcrunch.com/2025/06/24/wispr-flow-raises-30m-from-menlo-ventures-for-its-ai-powered-dictation-app/
27. Blackrock Neurotech, "Using AI and Brain Implants, Researchers Reconnect ALS Patient with Their
    Lost Voice", Aug 2024.
    https://blackrockneurotech.com/insights/using-ai-and-brain-implants-researchers-reconnect-als-patient-with-their-lost-voice/
28. Medical Design & Outsourcing, "Paradromics BCI design for durability, longevity", 29 Sept 2026.
    https://www.medicaldesignandoutsourcing.com/paradromics-bci-design-durability-longevity/
29. OrissaPOST, "I love you: three words, huge leap for Neuralink", 18 Sept 2026.
    https://www.orissapost.com/i-love-you-three-words-huge-leap-for-neuralink/
30. "emg2vec: Self-supervised Pretraining in Electromyography-based Silent Speech Interfaces",
    IEEE, 2024/2025. https://xplorestaging.ieee.org/document/10781736 ; Wiley, "Soft Active
    Electromyography Interface for Machine Learning-Enabled Silent Speech Recognition", 2025.
    https://advanced.onlinelibrary.wiley.com/doi/pdf/10.1002/aisy.70440
    (Both are leads; not independently fetched in this research.)

## Key takeaways for the build

1. **The 92% AlterEgo number is a 10-class digit task, not open-vocabulary speech.** The real,
   honest state of the art for open-vocabulary non-invasive silent speech is **~12% WER** with an
   LLM rescoring layer on one speaker (MONA LISA `[15]`), **~42% WER** without one (Gaddy 2021 `[14]`),
   and **~73% WER** when no audio-aligned training data exists at all (Gowda 2026 `[17]`). Plan for
   tens of percent WER, not 92%.
2. **AlterEgo's own best claim of "invisible" is the patent's definition — no visible face/neck
   movement and no exhalation `[8]`.** That is the right target for the owner. But every *demonstrated*
   high-accuracy result used either mouthed/minimal articulation `[5][13][16]` or a fixed small
   vocabulary `[1][3][5]`.
3. **The electrode layout that works is face/neck, not wrist.** The recurring validated site set is
   mental/chin, oral/lips, submental/submaxillary, hyoid, and laryngeal/digastric `[1][4][8][16]`.
   Masseter/temporalis/zygomaticus are **not** in the AlterEgo papers — don't design around them.
4. **Channel count has crept up, not down:** 6–8 channels in AltErgo/EMG-UKA `[1][16]`, 31 channels
   for the current best open-vocabulary EMG-to-text `[17]`, 16 bipolar in Meta's wristband `[12]`.
   A 16–32 channel dry-electrode face/neck array is the defensible design point.
5. **Sample rate:** AlterEgo used **250 Hz** `[1]`; EMG-UKA **600 Hz** `[16]`; Gaddy **1000 Hz** `[13]`;
   Gowda **5000 Hz** `[17]`; Meta **2000 Hz** `[12]`. Higher rates preserve MUAP detail and are cheap
   on a custom PCB; 1–2 kHz is a reasonable starting point, with 250 Hz as the proven minimum.
6. **The AFE is commodity.** OpenBCI/TI ADS1299-class, 24-bit, 24× gain, dry or gelled electrodes
   `[1][5][8][11]`. The hard parts are electrode mechanics (contact stability across sessions `[1][3]`)
   and per-user calibration.
7. **Session and user dependence is the documented failure mode** of every sEMG SSI: "data collected
   in previous sessions … does not necessarily generalize to future sessions" and "each user must
   train the system on their own examples" `[3]`. One-user training data collection is therefore the
   right plan — but budget for re-calibration every session.
8. **Language models are now part of the decoding stack and buy real WER.** MONA LISA's jump to 12.2%
   is largely LLM rescoring `[15]`; Wispr's Canto claims 30% → 5–10% WER on hard voiced audio `[19]`.
   An LLM/WFST rescoring layer is a cheap, high-leverage addition.
9. **Cross-user generalisation is a data-scale problem, not an algorithm problem** (Meta: 1,000s of
   participants, power-law scaling `[12]`). One user cannot replicate that, so personalisation is
   mandatory — consistent with the owner's willingness to do long calibration.
10. **The commercial field is splitting:** AlterEgo and The Subvocal Company pursue face/ear sEMG
    `[9][21]`; Wispr abandoned silent speech for voiced dictation and raised $280M `[19]`; Apple
    bought an optical micromovement startup `[23]`. Silent speech is still pre-product — no company
    has published a peer-reviewed open-vocabulary WER on shipping hardware.

## Open questions

1. **What did AlterEgo's 2025 demo actually decode, and at what WER?** No accuracy, vocabulary,
   channel count or sample rate has been published `[9][10]`. Is the product still the 2018
   10-class digit classifier, the Wadkins 20-word continuous model `[3]`, or something new?
2. **Can the "no visible movement, not exhaling" condition `[8]` be decoded at useful accuracy?**
   Every demonstrated high-accuracy result allowed mouthed/minimal articulation `[5][13][16]`. The
   gap between strict internal articulation and minimal articulation is unquantified.
3. **What is the realistic per-user calibration cost?** No paper reports hours-to-usable for a new
   user. The Gowda protocol (8 h, one speaker, 31 electrodes) `[17]` is the most detailed, and it
   still ends at 73% WER.
4. **Does dry-electrode face/neck sEMG reach the ~12% WER of gelled lab setups?** Gaddy used paste
   `[13]`; Meta used dry electrodes but on the wrist `[12]`. No dry face/neck open-vocabulary result
   was found.
5. **How much of MONA LISA's 12.2% is sensing vs language modelling?** Replicating the LLM rescoring
   layer independently would separate the two `[15]`.
6. **What is Q.ai's actual modality and accuracy, and what will Apple ship?** The acquisition is
   real `[23][24]` but no technical paper or product spec is public.
