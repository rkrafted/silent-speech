# Track 12 — Fast personalization: maximum decoder per minute of recording

Scope: pretrain-then-adapt for EMG; per-user adapters / LoRA / session embeddings; how many minutes
of a new user's data buy how much accuracy; what silent EMG cannot see; recording-script design for
information-per-minute; whether human-written pronunciation rules help; where QLoRA actually fits
(a local LLM rescorer, not the EMG model). Ends with a 6-hour one-day recording plan and recipe.

All numbers are quoted as the source states them. Preprints are marked. Sources are numbered at the
end and every claim carries its source.

---

## 1. Executive summary

1. **Pretrained encoder + short per-user fine-tune; the data budget is minutes, not hours.** Cleanest
   measurement: 27 subjects, closed 50-sentence corpus, initialise from a released single-subject
   checkpoint, pretrain on 26 others, fine-tune the target: **3 min of target calibration → 20.5% CER
   / 31.7% WER, statistically indistinguishable from the full ~13-min pool (21.7% / 31.9%)**; 1 min →
   25.4% CER (significantly worse); 10 min → 18.6% CER [6].
2. **Zero-shot cross-user transfer is unreliable.** emg2qwerty generic model = **51.78% CER** on
   held-out users vs **6.95% CER** after fine-tuning on that user [4]. Amputee myoelectric transfer
   "fails outright" zero-shot until 3 labelled repetitions are given [8]. Meta's wristband is the
   exception: 162–6,627 participants per task gives >90% offline accuracy zero-shot, and
   personalisation adds only 16% [9]. **Budget for calibration.**
3. **Adaptation method: full fine-tuning of the small EMG model beat every adapter at every budget**
   in a 77-subject study, and a subject-specific MLP adapter (2,201 params) gave **no detectable
   benefit** on speech EMG [6,7]. A gradient-free prototypical rule recovers **52–78%** of
   fine-tuning's gain with no optimiser [7]. Checkpoint initialisation is itself worth ~23 CER points
   and 5/27 folds of stability [6].
4. **Silent EMG sees place and manner well; voicing and nasality badly.** Forced-choice accuracies
   from the best silent-EMG model: place **96.6%**, oral manner **92.9%**, nasality **89.1%**,
   voicing **88.1%** — but over a *phoneme-context* baseline needing no EMG, the gains are **+16.2,
   +13.3, +4.8 and +2.8** points [2]. Across corpora voicing is only ~**63%** separable from EMG on
   two classes (chance 50%) vs ~81% from audio, and 45-phone frame accuracy is **16.8%** [38,39].
   **Add EGG or a throat accelerometer/radar for voicing, or let the LM fix it.**
5. **Quantisation is irrelevant to the EMG model** (0.05M–109M parameters: 5.29M [4,5], 2.58M/1.38M
   [5], 4.4M [9], 3.6M [13], ~50k [11]). Non-quantized LoRA *does* apply — it is used on a ~50k TCN
   for test-time adaptation [11]. The demonstrated compression route is **distillation**: >100M →
   50× smaller with <1.5% absolute loss [12].
6. **QLoRA's home here is the LLM corrector on the 3090.** LLM n-best rescoring gives **5–25%**
   relative WER improvement [18]; constrained decoding to the n-best/lattice gives **up to 12%**
   versus free generation [16]. A 7–8B model QLoRA-fits in **~17 GB** [14]; data needs are
   **~1k–10k curated examples** [14,43]. The published ceiling: Myovox reaches **18.53% WER** with a
   QLoRA-7B reranker but reranking is exhausted because the EMG **phone error rate (~20.9%)** is the
   binding constraint [28].
7. **A 6-hour day buys a closed personal vocabulary, not open dictation.** Parallel voiced+silent
   recording is mandatory [1,2]; TIMIT/CMU-ARCTIC coverage plus minimal pairs; ~3 reps/prompt; 20–30
   min blocks; finish with a clean 3–13 min calibration set.

---

## 2. Pretrain-then-adapt: how many minutes buy how much accuracy

### 2.1 Gaddy & Klein's protocol (the reference)

Single speaker, 8 facial channels at 1000 Hz (OpenBCI Cyton, gold electrodes, Ten20 paste,
monopolar, reference behind one ear) with the eight electrode positions documented explicitly
(cheek, chin, below-chin, throat, mid-jaw, cheeks, in front of the ear) [1]. The released dataset
is ~18.6–20 h from that one speaker [1,3], distributed as (T, 8) raw EMG with the prompt text per
sample (Zenodo, CC-BY-4.0) [27].

| Condition | Data | Vocab | Result |
|---|---|---|---|
| Closed (date/time) | 500 utterances, 26 min silent + 30 min vocalized, one session | 67 words | human **WER 3.6%** |
| Open (Gutenberg) | 3.6 h silent + 3.9 h vocalized parallel (1588 utts) + 11.2 h non-parallel vocalized (5477 utts); **18.6 h** | **9828 words** | **68.0% WER** automatic, **74.8%** human |

Direct voiced→silent transfer gives 91.2% WER (88.8% human closed); deleting the throat electrode
improves it to 88.0% (64.6% closed) because that channel diverges most between modes [1]. Their
target-transfer method (DTW alignment of silent→vocalized EMG, refined by CCA and predicted audio)
reaches **68.0%**; without CCA 69.8%, without audio alignment 76.5% [1]. Architecture: 3-layer
biLSTM, 1024 hidden units, 26-dim MFCC target, **32-dim session embedding appended to every EMG
timestep** [1]. The 2021 follow-up replaced hand features with residual convolutions + a 6-layer
Transformer and added an **auxiliary phoneme loss**: **42.2%** automatic (human 36.1%/28.5%; no
phoneme loss 51.7, LSTM 46.0, hand features 45.2) [2]. Code is public [2].

**The protocol rule that follows: silent EMG has no synchronous audio target, so record the same
utterance twice — once voiced, once silently — and transfer the audio onto the silent signal.**

### 2.2 emg2qwerty: the largest cross-user benchmark

**108 users, 1,135 sessions, 346.4 hours, 5,262,671 keystrokes**, 2 kHz, 16 channels/wristband,
average 18.0 min/session (9.5–47.5) [4]. Benchmark: 100 users train the generic model, **8 held-out
test users**; personalisation uses their remaining sessions [4].

| Model | Test CER (no LM) | Test CER (char LM) |
|---|---|---|
| Generic (no personalization) | 55.38 ± 4.10 | **51.78 ± 4.61** |
| Personalized (random-init) | 15.38 ± 5.88 | 9.55 ± 5.16 |
| **Personalized (finetuned from generic)** | **11.28 ± 4.45** | **6.95 ± 3.61** |

Best user 3.16% CER with LM; finetuning from the checkpoint beats random-init by 27% relative
(computed), p < .005 [4]. The model is "simply unusable" zero-shot, and "models tend to become
usable at a CER of approximately 10% or less" [4]. Architecture: **4 TDS conv blocks, 32-sample
kernels, 1-second receptive field, 5.29M parameters**, log-spectral features, SpecAugment +
electrode-rotation + temporal-jitter augmentation, CTC, 6-gram character LM; rotation-invariance
modules survive band re-donning [4,5].

### 2.3 The three-minute result (2026 preprint)

Le et al., arXiv:2609.21288 [6]: 27 participants, each <0.5 h (21.3 min average), **Aloud** and
**Mimed**, closed **50-sentence TIMIT** corpus, leave-one-subject-out, 8-channel lower-face/neck
montage, initialise from Gaddy's ~18.7 h checkpoint (15.1 h vocalized + 3.6 h silent), pretrain on
26, fine-tune the target.

| Condition (n=27) | CER % | WER % |
|---|---|---|
| Pretrain + fine-tune (MLP adapter) | 21.7 ± 12.5 | 31.9 ± 17.0 |
| Pretrain + fine-tune (no adapter) | 22.5 ± 13.3 | 33.3 ± 18.3 |
| Pretrain + fine-tune from random init | 44.9 ± 29.5 | 58.8 ± 26.0 |
| Pretrain zero-shot | 49.3 ± 20.8 | 63.1 ± 21.1 |
| Checkpoint + fine-tune (no multi-subject pretrain) | 67.6 ± 5.9 | 96.7 ± 5.0 |

Calibration sweep: **1 min = 25.4% CER / 36.6% WER** (significantly worse than full, p=0.003/0.009);
**3 min = 20.5% / 31.7%** (p=0.27/0.88); 5 min n.s.; **10 min = 18.6%**; full ~13 min = 21.7% [6].
Macro CER falls **74.4% (1 pretraining subject) → 21.7% (26)**; random-init pretraining failed to
converge in **5/27 folds** [6]. Mimed is harder than Aloud: **27.9% vs 15.4% CER** (p=3×10⁻⁵) [6].
Two stated caveats: the sweep fixed epochs, not updates, so 3 min is "the shortest tested budget"
not proven equivalence; and **removing the five evaluation sentences from all training data pushes
CER/WER to 78.6% / 99.9%** [6] — the headline number is largely sentence-set familiarity.

### 2.4 What to do with the calibration repetitions

Odeyemi & Zhang, arXiv:2609.20296 [7]: four ways to spend *exactly the same* labelled repetitions,
77 subjects, budgets up to 5 reps (DB1) / 4 (DB2/DB5). **Full fine-tuning is most accurate at every
budget**; a **gradient-free prototypical rule recovers 52–78% of its benefit with no optimiser and
no per-user weights**; "a single labeled repetition taken after a first session would recover
approximately as much as the best label-free adaptation" [7]. Their conclusion: "The widespread
intuition that a good representation only needs a fresh classifier is incorrect here" [7]. The
companion paper (arXiv:2609.20297) transfers to **11 transradial amputees**: zero-shot fails
outright; with **3 labelled repetitions** it reaches **0.779 macro-F1 vs 0.589** for a per-user
clinic classifier, for every subject; **40 intact subjects transferred better than 10 amputees**,
and combining sources was best [8].

### 2.5 Meta Nature 2025: personalisation on a very large model

Kaifosh, Reardon et al., *Nature* 645:702–711 (2025) [9]: 48 pogo-pin electrodes in **16 bipolar
channels**, 2 kHz, **2.46 μVrms** input-referred noise, ~65.5 dB dynamic range, no gel/skin prep
(~10 TΩ ∥ 10 pF) [9]. **11,236 participants** total, 162–6,627 per task; band removed and
repositioned between sessions. Offline held-out accuracy **>90%** for handwriting and gestures;
closed loop 0.66 acquisitions/s, 0.88 gesture detections/s, **20.9 WPM handwriting**; single-
participant models do not transfer across people (98% of own models beat every other's), while
cross-*session* transfer is much easier; performance follows power laws in data and parameters [9].
Personalising handwriting improves it "by **16%**" [9]; the exact calibration budget behind that is
**unverified** (the 2024 preprint reportedly said "up to 30%").

### 2.6 Architecture and normalisation beat adapter cleverness

SplashNet [5] changes three things on emg2qwerty: **Rolling Time Normalization** (causal online
z-scoring, "requires no calibration"), **Aggressive Channel Masking**, and a **Split-and-Share**
weight-shared per-hand encoder. Zero-shot test CER **51.78% → 35.67%** (31% relative), fine-tuned
**~7.0% → 5.5%** (21% relative), at **2.58M** params (mini: **1.38M**, ¼ params, 0.6× FLOPs); RTN
alone cut zero-shot CER 47.18% → **39.15%** (p=6e-44) [5]. Mehlman et al. scale a vanilla
Transformer on the same data from **2.2M → 109M** params, generic CER **35.9% → 30.5%**
(personalized **9.7% → 6.8%**), then distil it **50× smaller with <1.5% absolute loss**; distillation
gives the small student a **+4.0-point** absolute gain over training it directly [12]. This is the
right compression tool for EMG decoders.

### 2.7 Session/domain-shift toolkit

Recurring, transferable mechanisms: a **32-dim session embedding** on every timestep [1,2]; **causal
per-session normalisation (RTN)** [5]; **electrode-rotation augmentation + rotation-invariant input**
for re-donning [4]; **LoRA on convolutional layers + experience replay** for test-time adaptation of
a ~50k TCN across sessions, with **MAML** "competitive in one- and two-shot regimes" [11]; and the
LM-pseudo-label loop. In an invasive BCI (BrainGate2 participant T5, 403 days, 15 sessions), LM-
corrected pseudo-labels kept online handwriting WER at **6.16%** vs **26.51%** without
recalibration (offline 3.68% vs 2.05% ground-truth lower bound), at **~9 s per update**, with **~10
sentences** recovering most lost accuracy [10]. The transferable idea is the pseudo-label loop, not
the surgery.

### 2.8 Data-efficiency summary

| New-user data | Method | Task | Result | Source |
|---|---|---|---|---|
| 0 min | cross-user model | closed 50-sentence EMG speech | 49.3% CER | [6] |
| 1 min | fine-tune multi-subject ckpt | closed 50-sentence EMG speech | 25.4% CER / 36.6% WER | [6] |
| **3 min** | fine-tune multi-subject ckpt | closed 50-sentence EMG speech | **20.5% CER / 31.7% WER** | [6] |
| 10 min | fine-tune multi-subject ckpt | closed 50-sentence EMG speech | 18.6% CER | [6] |
| 3 reps | full fine-tune | amputee myoelectric gesture | 0.779 vs 0.589 macro-F1 | [8] |
| 4–5 reps | full fine-tune / prototypical | myoelectric gesture DBs | best; 52–78% of gain | [7] |
| 8 sessions | fine-tune generic TDS | wrist typing (emg2qwerty) | 6.95% vs 51.78% CER | [4] |
| unspecified | personalisation | wrist handwriting (Nature) | +16% | [9] |

**Bottom line: pretrain across users/sessions; 3–13 minutes of the owner's own aligned
silent+voiced data is the adaptation budget, and it buys a closed personal vocabulary.**

---

## 3. What silent EMG can and cannot see

Gaddy & Klein 2021 report a frequency-normalised phoneme confusion and forced-choice
articulatory-feature accuracy [2]. Most-confused pairs (confusion %, accuracy %): dʒ/tʃ 13.2, 49.4;
v/f 10.4, 72.0; **p/b 10.3, 64.3**; **m/b 9.3, 74.3**; **k/g 8.9, 77.2**; ʃ/tʃ 8.3, 59.8; **p/m
8.1, 73.0**; **t/d 7.2, 64.0**; **z/s 6.6, 80.0**; ɪ/ɛ 6.5, 60.6; **t/n 6.3, 67.1**; ɪ/ɜ 6.0;
ɹ/ɚ 5.7; t/s 5.5; ɛ/æ 4.7; u/oʊ 4.3; θ/ð 4.1; ɜ/æ 3.2; ɪ/æ 3.1 [2]. Their reading: "many of the
confusions are between pairs of consonants that differ only in voicing … voicing signals appear to
be subdued in silent speech"; nasals confuse with stops "due to the role of the velum and its
relatively large distance from the surface electrodes"; vowels confuse with each other and with
consonants [2].

Forced-choice articulatory accuracy (majority class / phoneme context only / full EMG), and the EMG
gain over context [2]:

| Feature | Majority | Context | EMG | **Gain** |
|---|---|---|---|---|
| **Place** | 56.2 | 80.4 | **96.6** | **+16.2** |
| **Oral manner** | 40.5 | 79.6 | **92.9** | **+13.3** |
| Nasality | 64.5 | 84.3 | 89.1 | +4.8 |
| Voicing | 65.1 | 85.3 | 88.1 | **+2.8** |

Interpretation: place and oral manner are genuinely visible in facial/neck EMG; **voicing is
laryngeal and nasality is velar, and both are nearly fully recovered from linguistic context, not
from the muscle signal.** This is consistent with the throat-electrode finding (removing the
mode-divergent laryngeal channel *improved* transfer) [1] and with Meltzner et al. 2008, where
**mentally rehearsed** speech was undecodable "due to a lack of sufficient sEMG activity" while
vocalized/mouthed words reached **92.1% / 86.7%** on a 65-word vocabulary with 11 face/neck sites
and 9 speakers [23]. Silent articulation is intrinsically harder than voiced: 27.9% vs 15.4% CER
[6]; 86.7% vs 92.1% word accuracy [23].

**Independent confirmation from larger studies.** Wand's thesis (reproducing the ICASSP 2011
phone-confusion study) reports feature-class classification accuracy on two corpora, EMG vs
acoustic: **manner 47.73% / 47.65% vs 69.38% / 75.92%**, **position 55.59% / 51.24% vs 56.48% /
66.43%**, **voicing only 62.63% / 63.37% vs 80.77% / 80.14%** (two classes, chance 50%), and
frame-level phone accuracy **16.8% / 16.6%** over 45 phones; the thesis states plainly that
voicing "depends on glottal activity, which is not captured by our EMG setup" [38]. Salomons et
al. (Spanish, 8 face/neck channels, 30 phones) measured **35.98% EMG vs 69.68% audio** frame
accuracy at a **13.10% chance level**, with confusions exceeding the correct class: **i→e 32.86%
vs i correct 25.18%**, **u→o 38.68% vs 37.57%**, **b→p 16.49% vs 15.67%**, **g→k 11.39% vs
0.57%** [39]. Meltzner et al. 2017 reached **10.3% WER on a 2,500-word vocabulary with 8 sensors**
across 8 laryngectomy users (**13.6%** with 4 sensors), but with a finite-state grammar, not a
statistical language model [40]. Voicing is recoverable only by adding a glottal sensor: EGG
"allow[s] inclusion of reliable voicing information" in a parallel EMA/EPG/EGG recognition system
[41]. The build consequence is direct: **facial/neck EMG alone cannot resolve voicing minimal
pairs; add EGG or a throat accelerometer/radar, or let the LM fix them** [38,39,41].

Consequence for the build: **any system that must separate pat/bat or mat/bat is relying on the LM
and the vocabulary, not the electrodes.** Small closed vocabularies were already ≥86–92% in
2008–2018 (Meltzner 65 words [23]; AlterEgo ~20 words, ~92%, 7 of 16 screened electrode sites, later
4 along one jaw, with ~15 min customisation + 90 min use and only the last two network layers
retrained [26]). That is the realistic target class for a one-day, one-user build.

---

## 4. Recording-script design for maximum information per minute

### 4.1 Corpora and their exact specs

- **TIMIT** is the reference diphone design [19,22]: **6,300 sentences, 10 per speaker, 630 speakers,
  8 dialect regions**. Texts: **2 SA** shibboleths read by all (1,260 tokens), **450 SX
  "phonetically-compact"** (each speaker reads 5; each text read by 7 speakers; 3,150 tokens),
  **1,890 SI "phonetically-diverse"** from Brown/Playwrights (each read once; 1,890 tokens) —
  **2,342 distinct texts**. SX "provide a good coverage of pairs of phones, with extra occurrences
  of phonetic contexts thought to be either difficult or of particular interest"; SI "maximized the
  variety of allophonic contexts" [22]. **Copy that SA/SI/SX structure.**
- **Harvard sentences** (IEEE, 1969): **720 phrases in 72 lists of 10**, phonetically balanced at
  English phoneme frequencies [21].
- **CMU ARCTIC**: **1,132 sentences** from out-of-copyright Gutenberg prose, phonetically balanced
  US English, with 16 kHz waveforms and simultaneous EGG [20] — same style as Gaddy's open-vocab
  training text.
- Minimal-pair word lists (PB-50, CID W-22, NU-6) and the **Rainbow Passage** (Fairbanks 1960) are
  useful for over-sampling confusable contrasts and for a repeatable warm-up, but their exact specs
  are **unverified** here.

### 4.2 How the silent-speech papers chose prompts

Gaddy & Klein: template-generated date/time expressions closed-vocab (>50,000 possible, 500
recorded, 67-word vocab) and **Project Gutenberg** books open-vocab (1,588 parallel utterances,
9,828-word vocab); "Both speaking modes of an utterance were collected within a single session to
ensure that electrode placement is consistent between them" [1]. Le et al.: **50 TIMIT sentences,
nominally 3 repetitions per mode** (Aloud, Mimed, Subvocal), fixed 45/5 split [6]. emg2qwerty:
random dictionary words + filtered Wikipedia sentences [4].

### 4.3 Active learning

Best quantitative result found (myoelectric control, not speech): with least-confidence,
smallest-margin and entropy-reduction sampling, "With only 3.2 min of data carefully selected by the
active learner, the decoder outperforms random sampling by 4–5 and ~2%" for able-bodied and
limb-difference participants; smallest-margin/least-confidence were best [24]. **Only abstract-level
content was retrievable, so this figure is quoted as reported and is unverified here.** No paper was
found that actively selects *which prompts a subject speaks* (stimulus selection) rather than which
recorded samples to label — **an open gap**. Practical version: after an initial fine-tune,
re-record the highest-loss items.

### 4.4 Session length, fatigue, repetition counts

No measured accuracy-vs-minutes fatigue slope for facial silent EMG was verifiable. Documented sEMG
drift causes: **muscle fatigue, electrode displacement, posture difference, user adaptation over
time, inter-subject variation**, plus **perspiration/humidity and gel drying** [25]. Best protocol
anchors: **18.0 min average (9.5–47.5)** with re-donning between sessions [4], **~30 min per mode**
[1], **21.3 min** [6]. All doff/re-don between blocks. **Design 20–30 min blocks with rest and
re-donning.** Repetitions: budgets of 1, 2, 3, 5 reps tested; full fine-tuning won at every budget
and one repetition after a first session recovers about as much as the best label-free adaptation
[7]. In sentence EMG, **1 min → 25.4% CER, 3 min → 20.5%, 10 min → 18.6%** [6]. **~3 reps/prompt is
the practical ceiling.**

### 4.5 Voiced-vs-silent mismatch

Parallel voiced+silent recording in one donning is the primary correction [1]. The throat electrode
diverges most; deleting it improved direct transfer 88.8→64.6 WER (closed) and 91.2→88.0 (open) [1].
Either train the DTW+CCA transfer or down-weight the mode-sensitive channels. Silent/mimed is harder
than voiced: 27.9% vs 15.4% CER [6]; 86.7% vs 92.1% accuracy [23]. A 32-dim session embedding
absorbs placement change [1,2]. No A/B of hands-free vs normal posture for silent speech was found —
**unverified**.

---

## 5. Do human-written pronunciation rules help directly?

**Honest answer: yes, but mostly as *structure* (vocabulary and lexicon) or as a prior that is
re-estimated from data — not as a frozen hand-written decoder component.** Every primary source
found with decoder-side gains uses confusion matrices or feature detectors **estimated from aligned
data**; human knowledge chooses the representation. No source shows a hand-written confusion table
beating a measured one, and several show it hurting when wrong.

*Articulatory features as outputs.* Metze & Waibel's 76 hand-picked feature streams cut WER **13.4%
→ 11.6%** (Broadcast News) and **23.5% → 21.9%** (ESST), but "Initial experiments on Switchboard
data have not yet led to significant improvements" [29]. Stouten & Martens: "there exists no purely
articulatory driven ASR system that outperforms state-of-the-art systems driven by acoustic
features"; their best phonological-feature system reached **6.11% WER vs 3.69%** for MFCC [30]. King
et al. found acoustic 8.4% vs articulatory 8.9% clean WER, but **50.2% vs 43.6% at 0 dB**, and
dismiss early approaches as "these early (and often failed) attempts, which generally used
knowledge-based 'expert systems' methods"; allowing schwa deletion makes "support" confusable with
"sport" [31]. Measured articulation gave a 17% relative phone-error reduction; recovered
articulation gave none [31].

*Confusion matrices inside decoders.* Morales & Cox's WFST substitution form "failed to increase
performance with high intelligibility dysarthric speakers, or with normal speakers, and in some
cases, the performance was worse than the baseline", because it depends on predicted-phoneme
accuracy [32]. PhoenixDSR (2026 preprint) learns a global+personalized confusion prior for an LLM
decoder: **CER 22.4% baseline → 30.0% plain LLM post-edit → 20.2% global prior → 18.3%
personalized** (PER 19.8 → 27.1 → 16.7 → 13.7); few-shot adaptation updates *only* the prior [33].
Torre et al. used a learned confusion matrix for vocabulary selection: "20% WER relative reduction
using the automatic alternative transcription generation procedure for a 37 word vocabulary, and
over 50% (20%) WER relative reduction using our unrestricted (restricted by groups of synonyms)
vocabulary selection procedure instead of randomly selected vocabularies" [34].

*LLM post-correction.* PAC interleaves graphemes and phonemes and adds homophone distractors:
LibriSpeech test-clean N=2000, **WER 1.69 → 1.18**, biased-WER **8.00 → 2.50 → 2.35 → 1.97 → 1.91**
(grapheme+phoneme context, +phoneme, +distractor, +RL) — most of the gain from the distractor/RL,
not the phone annotation [35]. Counterweight: Gu et al. show that in the low-error regime "LLMs
overcorrect and hallucinate", and a specialised error model beats them "with 15x fewer parameters"
(1.5/3.3% WER) [36]. Constrained decoding with a pronunciation lexicon pays: context-FST biasing
cut named-entity WER **57%**, mapped pronunciations a further **31%** (70.6% overall WERR, +10%
inference time) [37].

**Ranked for this build:** (1) **prune the vocabulary / avoid minimal pairs** — 20–50% relative WER
reduction vs random [34], and it shapes the recording script; (2) **build the phoneme→word lexicon
FST** — necessary infrastructure [37]; (3) **use a confusion prior for LM rescoring, but estimate
and update it** [32,33]; (4) prompt-set/context biasing helps hotwords, not the general decoder
[35,37]; (5) a hand-written articulatory-feature output layer is **not** top-tier [29,30,31].

Connecting to §3: the axes a human most wants to write rules about (voicing, nasality) are exactly
where silent EMG adds least over context [2], so a hand-written voicing rule mostly duplicates the
LM. Rules demonstrably pay when they change the decoding problem — **vocabulary and lexicon.**

---

## 6. Where QLoRA actually fits

### 6.1 Quantising the EMG model: not worth it

At 0.05M–109M parameters [4,5,9,11,12,13], fp16 weights are tens to a few hundred MB and are not the
bottleneck (activations are). QLoRA's headline is "finetune a 65B parameter model on a single 48GB
GPU" [14]. What transfers is **non-quantized LoRA/adapters**: LoRA on a 50k TCN makes test-time
adaptation practical [11], but a 2,201-param subject MLP gave no benefit on speech EMG [6], and full
fine-tuning beat every adapter in the 77-subject study [7]. For one owner with a 5–10M model on one
desktop GPU, **plain full fine-tuning is the simplest correct choice**; use LoRA for many parallel
variants. Compression = **distillation** (>100M → 50× smaller, <1.5% absolute loss) [12].

### 6.2 QLoRA on the 3090

QLoRA "reduces memory usage enough to finetune a 65B parameter model on a single 48GB GPU while
preserving full 16-bit finetuning task performance" using 4-bit NormalFloat (NF4), double
quantization and paged optimizers [14]. Quality: mean 5-shot MMLU (7B–65B) **BFloat16 53.0, Float4
52.2, NFloat4+DQ 53.1** — "NF4 with double quantization matches BFloat16 performance, while FP4 is
consistently one percentage point behind"; Guanaco reaches "99.3% of the performance level of
ChatGPT" after 24 h on one GPU; 16-bit full fine-tuning of LLaMA 65B needs "more than 780 GB", QLoRA
<48 GB [14]. LoRA gives "10,000 times" fewer trainable parameters and 3× less GPU memory than
GPT-3 175B Adam fine-tuning, with rank as low as 1–2 sufficient [15]. **24 GB envelope:** 7B/8B
comfortably (~17 GB QLoRA / 20 GB LoRA [42]); 13B with micro_batch_size 1 and grad_accum 2 [42];
33B with paged optimizers + double quant [14]; 65B does not fit on one 24 GB card (needs 46–48 GB)
[14,42].

### 6.3 The corrector: numbers and guardrails

- **Use the n-best, not the 1-best.** 1-best input *degraded* LibriSpeech test_clean 2.88 → 3.02;
  5-best gave 4.7% and 10-best 7.2% gains (2.88 → 2.67) [16]. Using only 1-best degraded a
  transducer 6.90 → 8.25, with the corrector "mak[ing] many unnecessary changes ... to make the
  sentence more 'reasonable'" and deletion errors rising 1.7 → 2.2 [17].
- **Constrain and interpolate.** Restricting generation to the n-best/lattice with a score
  interpolation weight λ ≈ 0.75 gave "up to 12% WER reduction" (10-best lattice: test_clean 2.88 →
  2.53, test_other 7.06 → 6.31) [16].
- **Generative rescoring: 5–25% relative WER improvement.** ProGRes reduced CommonVoice WER 12.38%
  → 9.32% (24.7% relative) and 42.94% → 40.84% (4.9% relative), interpolating ASR confidence with
  LLM score at α ≈ 0.05–0.6; a permissive prompt was "prone to cause hallucinations, in the form of
  unnecessary sentence extensions, repeated sentences, or unrelated additions" [18].
- Practical recipe: EMG n-best → LLM proposes/ranks → candidates constrained to plausible EMG
  hypotheses → linear interpolation of EMG confidence and LLM score. For one user: a
  **vocabulary/grammar-constrained decoder (WFST)** plus an LLM rescore, never free-form rewriting.

### 6.4 How much data for the personal LLM

QLoRA found "a 9k sample dataset (OASST1) outperformed a 450k sample dataset (FLAN v2,
subsampled)" [14]. NVIDIA guidance: LoRA for "hundreds to low thousands of rows, or at most about
10K well-curated training examples", conservative LR, dedup, early stopping, because a tiny dataset
can "over-update" the model [43]. Very high rank (r=768) overfits the adaptation task [15].
**Target ~1,000–10,000 clean owner-specific examples; validate on held-out text; stop early.**

### 6.5 The one published silent-EMG + QLoRA pipeline, and its ceiling

Myovox [28] is a **single-subject, 31-channel facial sEMG** open-vocabulary decoder that takes the
emg2speech General Corpus from a published 51.17% WER to **18.53% WER** in three measured moves:
reproduce missing decode settings for a faithful **40.63%** baseline; replace the causal encoder with
a bidirectional Conformer distilled against **WavLM-Large layer-9** audio features (**26.14% WER /
22.34% PER**); then ensemble two acoustic models, union their multi-scale n-best lists and rerank
with a **QLoRA-fine-tuned 7B LM** (**18.53% WER**) on the 400-sentence held-out test set [28]. The
authors' negative result is the key sentence for this project: reranking is **exhausted at 18.5%
because the binding constraint is the EMG phone error rate (~20.9%), not the language model** — the
correct words are absent from the acoustic posteriors, so no reranker reaches the **9.30% n-best
oracle** [28]. **Put money into electrodes, montage, calibration and the encoder, not a bigger LLM.**

---

## 7. A one-day (≈6 h) recording plan and adaptation recipe

Assumptions: 8-channel facial/neck EMG (Gaddy positions [1] or the montage of [6]), 1 kHz, one
speaker, an electrical engineer available, and a pretrained checkpoint (Gaddy's public
silent_speech checkpoint [2] and/or the owner's earlier sessions).

**Rule zero: every prompt is recorded voiced first, then silently articulated, in the same session
and electrode placement** [1]. This parallel stream is non-negotiable.

| Block | Time | Content | Why |
|---|---|---|---|
| 1 Setup + baseline | 0:00–0:30 | Placement, impedance check, 30 s MVC reference, voiced-only Rainbow Passage | Normalisation + drift check |
| 2 Phonetic coverage | 0:30–2:00 | ~450 TIMIT SX/SI (or 720 Harvard, ~30 lists) | Diphone/phoneme coverage at English frequencies [19,21,22] |
| 3 Prosody/style | 2:00–2:45 | ~200 CMU ARCTIC sentences | Natural reading, Gutenberg-like [20] |
| 4 Minimal pairs | 2:45–3:30 | p/b t/d k/g f/v s/z, m/b n/d ŋ/g, ɪ/ɛ ɛ/æ u/oʊ, p/t/k triplets | Over-samples the confusable axes [2] |
| 5 Real vocabulary | 3:30–4:30 | Owner's actual commands/domain sentences | Closed personal corpus, biggest payoff |
| 6 Active-learning top-up | 4:30–5:15 | Re-record ~200 highest-loss items after a quick fine-tune | Spend the last hour where the model is wrong [24] |
| 7 Calibration hold-out | 5:15–5:45 | 3–13 min of fresh sentences in both modes + repeat drift check | Matches the calibration protocol [6] |

**Blocks of 20–30 min** with 5–10 min rest and contact re-check (protocol anchors: 18.0 min avg
[4], 21.3 min [6], ~30 min per mode [1]); **~3 reps/prompt max** [6,7]. Priority if short:
**6 ≈ 5 > 4 > 2 > 3**.

**Adaptation recipe:** (1) start from the pretrained checkpoint and verify it decodes the owner at
all (checkpoint init ≈ +23 CER points and 5/27 folds of stability [6]); (2) full fine-tune the
5–10M model on all parallel silent data with a **32-dim session embedding** and **causal RTN**
[1,5], using **CTC + auxiliary phoneme loss** [2,6]; (3) add a **vocabulary-restricted LM** then an
**n-best LLM rescore** trained on owner text with LoRA/QLoRA (§6.3); (4) keep adapting after each
use session via active-learning top-ups and optionally LM pseudo-labels as in CORP [10]; (5) for
donning-time adaptation, 4–5 reps/class with the gradient-free prototypical rule [7].

**Expected accuracy (honest):**
- Closed personal vocabulary (50–200 items), 3–13 min calibration, matched montage: **~20–26% CER /
  32–37% WER** by analogy with [6] before LM rescoring. A strong constrained LM on a *closed*
  command set can be usable; open dictation is not.
- The strongest published **single-subject open-vocabulary** result is **18.53% WER**, but on
  *vocalized* 31-channel EMG with a Conformer + WavLM distillation + QLoRA-7B reranker [28]; silent
  is harder (27.9% vs 15.4% CER [6]). Treat 18.5% as an unreachable-in-one-day ceiling.
- Training from scratch with no cross-user checkpoint needs Gaddy-scale data: **~18 h for 68% WER**
  (2020) or **42.2%** (2021) [1,2].
- **Do not expect** emg2qwerty's 6.95% CER [4] or Meta's 20.9 WPM [9]: those rest on 108–6,627
  pretraining users.

---

## Key takeaways for the build

- **Pretrain across sessions/users, then fine-tune the whole small model.** 3–13 min of the owner's
  aligned silent+voiced data is the budget; checkpoint initialisation is worth tens of CER points
  [6,7].
- **Record every prompt voiced, then silent, in the same session and placement.** Target transfer
  from voiced audio is the only documented way to train on silent EMG [1,2].
- **Voicing and nasality are not in the EMG.** EMG gain over a phoneme-context baseline: +16.2
  (place), +13.3 (manner), +4.8 (nasality), +2.8 (voicing) [2]. Put voicing in the LM and the
  vocabulary.
- **Normalise causally per session and make the input rotation-invariant.** RTN alone cut zero-shot
  CER by 8 points; rotation-invariance handles re-donning [4,5].
- **Do not quantise the EMG model** (0.05M–109M params); use full fine-tuning, non-quantized LoRA,
  or distillation [4,5,12]. **QLoRA on the 3090 belongs to the LLM corrector**, trained on the
  owner's text: ~1k–10k curated examples, 7–8B at ~17 GB, 4-bit NF4 [14,42,43].
- **Constrain the corrector to the EMG n-best/vocabulary and interpolate scores.** Free-form
  correction hallucinates; constrained decoding gave up to 12% WER reduction [16,18].
- **Design prompts for diphone coverage plus minimal pairs, not volume.** TIMIT (6,300 sentences,
  SA/SI/SX) and Harvard (720 phonetically balanced sentences) are ready-made; CMU ARCTIC (1,132)
  adds prose [19,20,21,22]. Spend the last hour on the model's confusions and reserve a clean 3-min
  calibration hold-out [6,24].
- **Day-one realistic outcome: closed personal vocabulary at ~20–30% CER before LM rescoring; open
  dictation is out of reach for a one-day, one-user build.**

## Open questions

1. **What is the open-vocabulary curve?** The 3-min result is closed-corpus and collapses to 78.6%
   CER on unseen sentences [6]. No published silent-EMG, open-vocabulary calibration-vs-CER curve
   exists for a new user — the number that matters for real use.
2. **How much of the 18.7 h Gaddy checkpoint transfers to a different montage/person?** A benefit is
   measured across montages [6], but the channel-mapping/re-referencing mechanisms are unexplained.
3. **When do adapters win?** Adapters lost at every budget [7] and did nothing in [6], yet LoRA is
   useful for *test-time* session adaptation of a TCN [11]. Resolve for 5–10M silent-speech models.
4. **Can voicing be recovered by an extra sensor** (laryngeal accelerometer, neck mechanomyography,
   ultrasound, radar) enough to change vocabulary design? This is the highest-value cross-track
   question raised by §3.
5. **What is the exact Nature-2025 personalisation budget** behind the 16% claim? Unverified; it
   would calibrate how much a large cross-user pool helps a single owner.
6. **How much does the owner's own text buy the LLM rescorer**, measured as end-to-end WER on silent
   EMG rather than ASR-rescoring WER on speech? No published silent-EMG + personal-LLM pipeline
   exists yet.
7. **Does active *stimulus* selection beat random prompt selection?** No paper found; the closest
   evidence is sample-level active learning [24].

---

## Sources

1. D. Gaddy, D. Klein, "Digital Voicing of Silent Speech", EMNLP 2020.
   https://ar5iv.labs.arxiv.org/html/2010.02960 ; https://aclanthology.org/2020.emnlp-main.445/
   (fetched 2026)
2. D. Gaddy, D. Klein, "An Improved Model for Voicing Silent Speech", ACL 2021, arXiv:2106.01933.
   https://arxiv.org/abs/2106.01933 ; full text and appendices via
   https://arxiv.org/html/2106.01933v2 (fetched 2026). Code: https://github.com/dgaddy/silent_speech
3. D. Gaddy, "Voicing Silent Speech", PhD thesis, UC Berkeley, Technical Report UCB/EECS-2022-68,
   May 2022. https://www2.eecs.berkeley.edu/Pubs/TechRpts/2022/EECS-2022-68.html (fetched 2026)
4. V. Sivakumar, J. Seely, A. Du, S. R. Bittner, A. Berenzweig, A. Bolarinwa, A. Gramfort,
   M. I. Mandel, "emg2qwerty: A Large Dataset with Baselines for Touch Typing using Surface
   Electromyography", NeurIPS 2024 Datasets and Benchmarks, arXiv:2410.20081.
   https://arxiv.org/abs/2410.20081 ; tables via https://arxiv.org/e-print/2410.20081 (fetched
   2026). Code: https://github.com/facebookresearch/emg2qwerty
5. N. Hadidi, J. Chan, E. Feghhi, J. Kao, "SplashNet: Split-and-Share Encoders for Accurate and
   Efficient Typing with Surface Electromyography", arXiv:2506.12356, 2025.
   https://ar5iv.labs.arxiv.org/html/2506.12356 (fetched 2026)
6. C. Le, B. Fumagalli, Y. Esmaeili, X. Chen, T. He, N. Emami, A. Flinker, Y. Wang, "Multi-Subject
   Pretraining Enables Short-Calibration Personalization for Closed-Corpus Surface EMG Speech
   Decoding", arXiv:2609.21288, Sep 2026 (preprint). https://arxiv.org/abs/2609.21288 ; full text
   https://arxiv.org/html/2609.21288v1 (fetched 2026)
7. J. Odeyemi, W. J. Zhang, "Personalising a Cross-User Surface Electromyography Encoder Under a
   Small Calibration Budget", arXiv:2609.20296, Jul 2026 (preprint).
   https://arxiv.org/abs/2609.20296 (fetched 2026)
8. J. Odeyemi, W. J. Zhang, "Intact-to-Amputee Transfer in Surface-EMG Gesture Decoding: Training
   Source and Calibration Budget", arXiv:2609.20297, Jul 2026 (preprint).
   https://arxiv.org/abs/2609.20297 (fetched 2026)
9. P. Kaifosh, T. R. Reardon et al. (CTRL-labs at Reality Labs), "A generic non-invasive neuromotor
   interface for human-computer interaction", Nature 645(8081):702–711, 2025.
   https://pmc.ncbi.nlm.nih.gov/articles/PMC12443603/ (fetched 2026); DOI 10.1038/s41586-025-09255-w
10. C. Fan, N. Hahn, F. Kamdar, D. Avansino, G. H. Wilson, L. Hochberg, K. V. Shenoy,
    J. M. Henderson, F. R. Willett, "Plug-and-Play Stability for Intracortical Brain-Computer
    Interfaces", NeurIPS 2023. https://pmc.ncbi.nlm.nih.gov/articles/PMC11086983/ (fetched 2026)
11. N. Touko, M. O. A. Ellis, C. Capone, A. Burrello, E. Donati, L. Manneschi, "Lightweight
    Test-Time Adaptation for EMG-Based Gesture Recognition", arXiv:2601.04181, 2026 (preprint).
    https://ar5iv.labs.arxiv.org/html/2601.04181 (fetched 2026)
12. N. Mehlman, J.-C. Gagnon-Audet, M. Shvartsman, K. Niu, A. H. Miller, S. Sodhani, "Scaling and
    Distilling Transformer Models for sEMG", arXiv:2507.22094, 2025.
    https://ar5iv.labs.arxiv.org/html/2507.22094 (fetched 2026)
13. M. Fasulo, G. Spacone, T. M. Ingolfsson, Y. Li, L. Benini, A. Cossettini, "TinyMyo: a Tiny
    Foundation Model for Flexible EMG Signal Processing at the Edge", arXiv:2512.15729, 2025.
    https://ar5iv.labs.arxiv.org/html/2512.15729 (fetched 2026)
14. T. Dettmers, A. Pagnoni, A. Holtzman, L. Zettlemoyer, "QLoRA: Efficient Finetuning of Quantized
    LLMs", NeurIPS 2023, arXiv:2305.14314. https://arxiv.org/abs/2305.14314 (fetched 2026)
15. E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, W. Chen, "LoRA: Low-Rank
    Adaptation of Large Language Models", arXiv:2106.09685, 2021.
    https://ar5iv.labs.arxiv.org/html/2106.09685 (fetched 2026)
16. R. Ma, M. J. F. Gales, K. M. Knill, M. Qian, "N-best T5: Robust ASR Error Correction using
    Multiple Input Hypotheses and Constrained Decoding Space", Interspeech 2023, arXiv:2303.00456.
    https://ar5iv.labs.arxiv.org/html/2303.00456 (fetched 2026)
17. R. Ma, M. Qian, P. Manakul, M. Gales, K. Knill, "Can Generative Large Language Models perform
    ASR error correction?", arXiv:2307.04172, 2023. (Fetched by a sub-search; used only for the
    1-best degradation and deletion-error figures.)
18. A. D. Tur, A. Moumen, M. Ravanelli, "ProGRes: Prompted Generative Rescoring on ASR N-Best",
    arXiv:2409.00217, 2024. https://ar5iv.labs.arxiv.org/html/2409.00217 (fetched 2026)
19. J. S. Garofolo, L. F. Lamel, W. M. Fisher, J. G. Fiscus, D. S. Pallett, N. L. Dahlgren, V. Zue,
    "TIMIT Acoustic-Phonetic Continuous Speech Corpus", LDC93S1, LDC, 1993.
    https://catalog.ldc.upenn.edu/LDC93S1 (fetched 2026)
20. A. W. Black, K. Lenzo, "CMU ARCTIC Databases", LTI, Carnegie Mellon University.
    http://festvox.org/cmu_arctic/ (fetched 2026); prompt list
    http://festvox.org/cmu_arctic/cmuarctic.data
21. "IEEE Recommended Practice for Speech Quality Measurements", IEEE Trans. Audio and
    Electroacoustics 17(3):225–246, 1969, DOI 10.1109/TAU.1969.1162058 — the Harvard sentences
    (720 phrases, 72 lists of 10); lists fetched via https://en.wikipedia.org/wiki/Harvard_sentences
    (fetched 2026)
22. "The DARPA TIMIT Acoustic-Phonetic Continuous Speech Corpus (TIMIT)" readme, NIST, 1990
    (corpus: MIT/SRI/TI; LDC93S1). https://catalog.ldc.upenn.edu/docs/LDC93S1/timit.readme.html
    (fetched 2026)
23. G. S. Meltzner, J. Sroka, J. T. Heaton, L. D. Gilmore, G. Colby, S. Roy, N. Chen, C. J. De Luca,
    "Speech recognition for vocalized and subvocal modes of production using surface EMG signals
    from the neck and face", Interspeech 2008.
    https://www.isca-archive.org/interspeech_2008/meltzner08_interspeech.html (fetched 2026)
24. M. Szymaniak, A. Krasoulis, K. Nazarpour, "Recalibration of myoelectric control with active
    learning", Frontiers in Neurorobotics 16:1061201, 2022.
    https://www.frontiersin.org/journals/neurorobotics/articles/10.3389/fnbot.2022.1061201/full
    (fetched 2026; only abstract-level content retrievable, so the 3.2-min / 4–5% / ~2% figures are
    quoted as reported and are **unverified** here)
25. I. Kyranou, S. Vijayakumar, M. S. Erden, "Causes of Performance Degradation in Non-invasive
    Electromyographic Pattern Recognition in Upper Limb Prostheses", Frontiers in Neurorobotics
    12:58, 2018. https://www.frontiersin.org/journals/neurorobotics/articles/10.3389/fnbot.2018.00058
    (fetched 2026)
26. L. Hardesty, "Computer system transcribes words users 'speak silently'", MIT News, 4 April 2018
    (AlterEgo; reports Kapur, Kapur, Maes, IUI 2018).
    https://news.mit.edu/2018/computer-system-transcribes-words-users-speak-silently-0404 (fetched
    2026)
27. D. Gaddy, "Silent Speech EMG" dataset, Zenodo v1.0, 2 October 2020.
    https://zenodo.org/records/4064409 (fetched 2026); CC-BY-4.0
28. V. Madishetty, "Myovox: Reading Speech from the Muscles of the Face", arXiv:2609.17548, Jul
    2026 (preprint). https://arxiv.org/abs/2609.17548 (fetched 2026)
29. F. Metze, A. Waibel, "A flexible stream architecture for ASR using articulatory features",
    ICSLP 2002. https://www.isca-archive.org/icslp_2002/metze02_icslp.pdf (fetched 2026; PDF text
    extracted with pypdf)
30. F. Stouten, J.-P. Martens, "Speech Recognition with Phonological Features: Some issues to
    attend", Interspeech 2006.
    https://www.isca-archive.org/interspeech_2006/stouten06_interspeech.pdf (fetched 2026; PDF text
    extracted)
31. S. King, J. Frankel, K. Livescu, E. McDermott, K. Richmond, M. Wester, "Speech production
    knowledge in automatic speech recognition", J. Acoust. Soc. Am. 121(6), 2007.
    http://www.cs.cmu.edu/~ziada/selectedpapers/King2007Jasa.pdf (fetched 2026; PDF text extracted)
32. O. Caballero Morales, S. Cox, "On the Estimation and the Use of Confusion-Matrices for
    Improving ASR Accuracy", Interspeech 2009.
    https://www.isca-archive.org/interspeech_2009/morales09_interspeech.pdf (fetched 2026; PDF text
    extracted)
33. Y. Wu, Y. Xu, J. Wang, X. Zhao, J. Jiang, Z. Luo, "PhoenixDSR: Phoneme-Guided and LLM-Enhanced
    Dysarthric Speech Recognition", ICASSP 2026 preprint. https://wyx.hai-lab.cn/files/icassp2026.pdf
    (fetched 2026; PDF text extracted)
34. D. Torre, L. Villarrubia, L. Hernandez, J. M. Elvira, "Automatic Alternative Transcription
    Generation and Vocabulary Selection for Flexible Word Recognizers", ICASSP 1997.
    https://www2.spsc.tugraz.at/people/franklyn/ICASSP97/pdf/author/ic971463.pdf (fetched 2026; PDF
    text extracted)
35. L. Fu, Y. Xin, S. Zeng, L. Fan, Y. Wu, X. He, "PAC: Pronunciation-Aware Contextualized Large
    Language Model-based Automatic Speech Recognition", arXiv:2509.12647, 2025.
    https://arxiv.org/pdf/2509.12647 (fetched 2026; PDF text extracted)
36. Z. Gu, T. Likhomanenko, R. H. Bai, E. McDermott, R. Collobert, N. Jaitly, "Revisiting ASR Error
    Correction with Specialized Models", arXiv:2405.15216 (v2, 2026).
    https://arxiv.org/pdf/2405.15216 (fetched 2026; PDF text extracted)
37. R. Huang, O. Abdel-hamid, X. Li, G. Evermann, "Class LM and Word Mapping for Contextual Biasing
    in End-to-End ASR", Interspeech 2020.
    https://www.isca-archive.org/interspeech_2020/huang20f_interspeech.pdf (fetched 2026; PDF text
    extracted)
38. M. Wand, "Advancing Electromyographic Continuous Speech Recognition", PhD thesis, Karlsruhe
    Institute of Technology (KIT), 2014 (§4.4 reproduces the ICASSP 2011 phone-confusion study).
    https://publikationen.bibliothek.kit.edu/1000040667/3371786 (fetched 2026; PDF text extracted)
39. I. Salomons, C. del Blanco, E. Navas, I. Hernáez, "Spanish Phone Confusion Analysis for
    EMG-Based Silent Speech Interfaces", Interspeech 2023.
    https://www.isca-archive.org/interspeech_2023/salomons23_interspeech.pdf (fetched 2026; PDF
    text extracted)
40. G. S. Meltzner, J. T. Heaton, Y. Deng, G. De Luca, S. H. Roy, J. C. Kline, "Silent Speech
    Recognition as an Alternative Communication Device for Persons with Laryngectomy", IEEE/ACM
    Trans. Audio, Speech, and Language Processing 25(12):2386–2398, 2017.
    https://pmc.ncbi.nlm.nih.gov/articles/PMC5851476/ (fetched 2026)
41. Y. Uraga, T. Hain, "Automatic Speech Recognition Experiments with Articulatory Data",
    Interspeech 2006. https://www.isca-archive.org/interspeech_2006/uraga06_interspeech.pdf
    (fetched 2026; PDF text extracted)
42. Axolotl documentation, "Llama 2" model page (QLoRA/LoRA VRAM guidance for 7B/13B; official
    project docs). https://docs.axolotl.ai/docs/models/llama-2.html (fetched by a sub-search 2026;
    cited for the 24 GB recipe figures)
43. NVIDIA NeMo / Nemotron, "small-dataset-lora" pattern (official guidance: LoRA for hundreds to
    ~10K curated rows, conservative LR, dedup, early stopping). Sourced from the NVIDIA-NeMo
    Nemotron repository (fetched by a sub-search 2026; used only for the data-volume guidance)
