# Track 05 — ML pipeline: turning signals into words for one user

*Research report for the silent-speech wearable project. Status: COMPLETE.*

Scope: open datasets and their licences, open code, model architectures and demonstrated results
for silent-speech decoding (closed vocabulary and open vocabulary), transfer from voiced to silent
speech, LLM rescoring, self-supervised/cross-modal pretraining, cross-session adaptation, how much
per-user data is needed, recording protocol, real-time constraints (phone vs on-device vs RTX 3090),
and evaluation (WER/CER, session drift). Finishes with a staged training plan.

Conventions (from `BRIEF.md`): inline `[n]` citations map to the numbered Sources list at the end.
Numbers are quoted exactly as the source gives them. **Demonstrated** results (with dataset size,
vocabulary, open vs closed vocab, silent vs mouthed vs voiced) are kept separate from
**claims/marketing**. Anything not verified against a page I fetched is marked
"(unverified — subresearch pass)" or "(unverified)".

**One-paragraph answer.** For a single user, the realistic path is: collect paired silently-mouthed
+ vocalised facial-EMG recordings over months; use a small convolutional/recurrent model with a CTC
head for direct EMG→text; pretrain/seed from public data and a generic model; decode with a
character/word language model and optional LLM rescoring. Closed command sets are reachable in
weeks (reference: 92% median word accuracy on a 10-word set [13]; 4% WER on a 67-word templated set
[1]). Open-vocabulary dictation is a months-scale, ~18–20 h single-speaker effort whose demonstrated
best is **12.2% WER** (MONA LISA, non-invasive silent EMG [10]) — and Gaddy's own open-vocab CTC
text model is only ~28% WER [3]. A 2026 replication shows the *acoustic* error rate, not the
language model, is the binding constraint on further gains [27].

## 1. Datasets

The public speech-EMG landscape is small and splits into: (a) **silent-speech EMG with parallel
vocalised recordings** (Gaddy; UC Davis orofacial), (b) **large non-speech motor-EMG datasets**
(Meta's emg2qwerty, emg2pose) useful for pretraining and benchmarking, and (c) older **vocalised /
whispered / silent speech-EMG corpora** (EMG-UKA) with small free subsets. Only (a) and (c) are
speech; only Gaddy's is open-vocabulary, single-speaker and silent.

| Dataset | Year | Subjects | Size | Ch / rate | Vocabulary | Mode | Access / licence |
|---|---|---|---|---|---|---|---|
| **Gaddy Silent Speech EMG** [1][3][4] | 2020 | 1 | 18.6 h total; parallel 3.6 h silent + 3.9 h vocalised (1,588 utts); non-parallel vocalised 11.2 h (5,477 utts); closed-vocab 26 min silent / 30 min vocalised (500 utts) | 8 ch @ 1000 Hz (OpenBCI Cyton) | open: **9,828 words**; closed: **67 words** | silent (mouthed) + vocalised | Zenodo 4064409, 3.9 GB, **CC-BY-4.0** |
| **EMG-UKA** [21] | 2014 | 8 | 7:32 h over 63 sessions; **free trial 1:52 h** (silent portion ≈22 min — unverified — subresearch pass) | 6 ch @ 600 Hz (unverified — subresearch pass) | 108-word test vocab (small sessions) | audible, whispered, **silent** | free trial at KIT; full version on request |
| **UC Davis orofacial EMG (Gowda)** [20] | 2024 | **16** (12 F, 4 M) | 13 gestures + 38 phonemes + 36 words, ×10 reps each; ~40 GB (unverified) | **22 monopolar ch @ 5000 Hz** (BrainVision actiCHamp) | 38 phonemes, 36 words (closed) | audible + silent | OSF `ym5jd`, described as "the largest publicly available speech EMG dataset to date"; licence CC-BY-4.0 (reported) [20] |
| **emg2qwerty** [5][6][7] | 2024 | 108 | 346.4 h, 1,135 sessions, 5,262,671 keystrokes | 32 ch @ 2 kHz, 12-bit | open, lexicon-free | **silent touch typing, not speech** | repo **CC BY-NC-SA 4.0** (README misstates NC-4.0) |
| **emg2pose** [8][9] | 2024 | 193 | 370 h, 29 stages | 16 ch @ 2 kHz | hand pose | not speech | **CC BY-NC-SA 4.0** |
| **KaraOne** [22] | 2015 | 14 | 24 GB | 64-ch **EEG** @ 1 kHz | 11 prompts | imagined + vocalised | free academic only |
| **Pragmatic Mandarin** [17] | 2025 | 30 | ~24 h EEG + 24 h sEMG + 8 h audio | sEMG 6 ch @ 1 kHz (reported) | 10 items | imagined, silent, overt | ScienceDB, request-gated |
| **AlterEgo** [13] | 2018 | — | no public release found; subresearch pass reports 16 screening electrodes → 7 selected and a 2020 follow-up with 3 MS patients (unverified) | — | ~20-command applications (unverified — subresearch pass) | internal/silent | **not released** |

Notes:

- **Gaddy is the only dataset that directly matches this build**: one user, 8 channels, silent EMG
  with parallel audio, an open 9,828-word vocabulary, CC-BY-4.0 [1][4]. Use it as the primary
  pretraining and pipeline-validation corpus.
- The Gaddy recordings are **silently mouthed**, not purely internal [1]. That is an upper bound if
  the owner keeps the face still.
- The emg2qwerty README says CC-BY-NC-4.0 but the **actual LICENSE file is CC BY-NC-SA 4.0**
  (ShareAlike added); verified by fetching the file [6][7]. Same for emg2pose [9]. Non-commercial
  only, and ShareAlike propagates to derivative weights.
- KaraOne is **EEG**, not EMG — a reminder not to blur modalities [22].
- The Mandarin dataset is request-gated ("Request Access", approval 5–7 business days per the
  subresearch pass); full text could not be fetched, so most fields are unverified [17].

## 2. Open code and licences

| Repo | What it is | Framework | Licence | Pretrained weights |
|---|---|---|---|---|
| `dgaddy/silent_speech` | Official code for EMNLP 2020, ACL 2021 and the Berkeley dissertation; EMG→speech synthesis **and** EMG→text CTC recognition [3] | PyTorch (CUDA 11.8 env), HiFi-GAN submodule, `ctcdecode` 1.0.3, KenLM, DeepSpeech 0.7.0 for eval [3] | **MIT** (Copyright 2021 David Gaddy) [3][12] | Yes — Zenodo 6747411 (vocoder/transduction) and 7183877 (recognition) [3] |
| `tbenst/silent_speech` | MONA LISA (2024): cross-modal contrastive silent-speech recognition; README claims 7.3% WER on open-vocab validation [11] | PyTorch Lightning, Hydra, SLURM scripts [11] | LICENSE file is Gaddy's **MIT** text (inherited from the fork); the MONA additions' terms are therefore ambiguous [12] | No published checkpoints [11] |
| `facebookresearch/emg2qwerty` | TDS ConvNet + CTC baselines, generic/personalised training, 6-gram KenLM beam decoder [6] | PyTorch Lightning + Hydra [6] | **CC BY-NC-SA 4.0** (README says NC-4.0) [6][7] | Yes — generic + personalised checkpoints + LM via git-lfs [6] |
| `facebookresearch/emg2pose` | sEMG→hand-pose baselines (not speech) [8] | PyTorch Lightning + Hydra [8] | **CC BY-NC-SA 4.0** [9] | Yes (per repo) |
| `HarshavardhanaTG/emg2speech` | 2025 EMG→speech: manifold/GRU EMG→phoneme plus self-supervised-speech EMG→audio; ALS participant [18][19] | PyTorch; S3/WavLM-style targets [18] | **No LICENSE file (HTTP 404) → all rights reserved; do not copy** [19] | OSF data/checkpoints (reported) [19] |
| `parlance/ctcdecode` | CTC beam-search decoder used by Gaddy's repo [3] | C++/PyTorch | **MIT** | n/a |
| `kensho-technologies/pyctcdecode` | Pure-Python CTC beam search + KenLM | Python | **Apache-2.0** | n/a |
| `kpu/kenlm` | n-gram LM toolkit | C++ | **LGPL-2.1** (copyleft — matters on redistribution) | n/a |

Practical notes:

- The recipe that matters most for a single user is Gaddy's, and it is **MIT code + CC-BY data**
  [3][4][12] — clean for personal R&D.
- emg2qwerty/emg2pose and anything trained on them are **non-commercial + ShareAlike** [7][9].
- MONA LISA's inherited MIT file is not a clear grant for the new code [12]; treat as research-only.
- Gaddy's repo pins an old toolchain (DeepSpeech 0.7.0, `ctcdecode` 1.0.3) [3]; comparisons require
  the same 0.7.0 scorer.
- MONA LISA reproduction is heavy: "An individual model trains on one A100 for 24-48 hours… The full
  model sweep as done in the paper trains 60 models" [11], and the contrastive losses need an
  A100 80 GB [10].

## 3. Model approaches and demonstrated results

### 3.1 Closed-vocabulary classification (the command-word regime)

- **AlterEgo (MIT Media Lab, IUI 2018)**: wearable silent-speech interface using neuromuscular
  signals from internal speech articulators, with bone-conduction output; the paper reports **92%
  median word accuracy** [13]. The subresearch pass read the PDF and reports a core study over
  digits 0–9 plus operator words with **10 participants**, each shown **750 digits (75 of each)**,
  silent reading "without producing a sound and moving their lips", average accuracy **92.01%** and
  mean latency **0.427 s**; a pilot used ~5 h and the main corpus ~31 h from 3 participants
  (unverified — subresearch pass; the fetched abstract states 92% median [13]). The 92% is a
  **10-class digit task**, not open vocabulary.
- **AlterEgo follow-ups.** Kapur et al., ML4H/PMLR 2020 (verified): 10 trials of 15 sentences from
  each of **3 multiple-sclerosis patients with dysphonia**, mean overall test accuracy **0.81** at a
  mean information transfer rate of **203.73 bits per minute** [34]. A 2019 MIT MEng thesis reports
  continuous decoding with CNN+CTC on 10- and 20-word vocabularies (11.5%→**7.0%** and 14.8%→
  **10.7%** with an LM) (unverified — subresearch pass) [35].
- Historical context as reported by MONA LISA [10]: HMM work reached 87% on a 10-word vocabulary
  (Maier-Hein 2005); Jou et al. reached 70% on 100 words; Elmahdy & Morsy (2017) reached 20% WER on
  20 words. These are citations inside [10], not independently verified here.
- **Synthetic on-MCU command demo (SilentWear, 2026)**: 8 HMI commands, 14-channel textile neckband,
  15k-parameter CNN, average cross-validated accuracy **84.8±4.6% vocalised / 77.5±6.6% silent**
  over multiple days [26].

### 3.2 Open-vocabulary decoding: the Gaddy line

All of this uses **silently mouthed** speech, 8 facial electrodes, 1 kHz, one speaker, open
vocabulary.

- **Gaddy & Klein, EMNLP 2020** [1]. Synthesise audible speech from silent EMG (MFCC prediction +
  WaveNet), evaluate by transcribing the synthesised audio. Because silent recordings have no usable
  audio targets, audio targets are transferred from the parallel vocalised recording via DTW,
  refined by CCA and predicted-audio alignment. Headline: closed-vocab date/time condition improves
  "from 64% to 4%" (human WER); open vocabulary "from 88% to 68%" automatic (95%→75% human) [1].
  Architecture: 112 hand-designed features → 3-layer bidirectional LSTM (1024 hidden) → 26 MFCCs at
  100 Hz; 32-dim session embeddings [1].
- **Gaddy & Klein, ACL 2021** [2]. Replaces hand-designed features with 1-D residual convolutions
  (resample 1000→800 Hz), adds 6 bidirectional Transformer layers with relative position embeddings
  (k=100 frames = 1 s each way) and an auxiliary phoneme loss. Automatic open-vocab WER **68.0 →
  42.2**. Ablations: hand-designed features 45.2, LSTM 46.0, no phoneme loss 51.7. Human evaluators:
  36.1% and 28.5% (average 32.3%) [2].
- **Gaddy dissertation / 2022** (reported in [3]): direct **EMG→text CTC** reaches "a WER of
  approximately 28%"; the latest audio-synthesis model "approximately 36%" [3].
- **MONA LISA (Benster et al., 2024)** [10]. Adds cross-modal contrastive losses (crossCon, supTcon)
  that let audio-only LibriSpeech train a shared EMG/audio latent space, latent-space DTW, and
  **LISA** — prompting GPT-3.5/GPT-4 with the top-k beam candidates. Results: open-vocab **silent**
  WER **28.8% → 12.2%**; **vocal** EMG **23.3% → 3.7%**; Brain-to-Text 2024 **9.8% → 8.9%** [10].
  The repo README claims **7.3% WER on open-vocab validation** [11]. Architecture: EMG ResNet +
  audio ResNet + latent Transformer decoder, 38 output characters (a–z, 0–9, word boundary, blank),
  CTC + contrastive losses [11].

### 3.3 2025–2026: self-supervised targets, ALS, and the reranking ceiling

- **emg2speech (Gowda et al., 2025)** [18]: self-supervised speech (S3) representations are
  "strongly linearly related to the electrical power of muscle activity" — a simple linear mapping
  predicts EMG power from S3 with **r = 0.85**; EMG power vectors for distinct articulatory gestures
  form separable clusters. They map EMG into the S3 space and synthesise speech **without explicit
  articulatory modelling or vocoder training**, demonstrated with a participant with ALS silently
  articulating [18].
- **Direct phonemic EMG→text without audio targets** (Gowda & Miller, 2025) [20]: sequence-to-
  sequence EMG-to-text at the phoneme level, explicitly avoiding the paired-audio requirement of
  Gaddy/MONA so it can apply to people who can no longer speak. The paper frames EMG signals as
  living on the manifold of symmetric positive-definite matrices for data- and parameter-efficient
  models suitable for embedded devices [20]. The subresearch pass reports silent-only results:
  **12% WER / 88% word accuracy** on a 67-word vocabulary, **PER 48.47% / WER 73.53%** on a
  ~6,500-word silent vocabulary, and at matched 8 electrodes / 1 kHz **27% WER vs Gaddy's 64%**
  with a **~1.4 M-parameter model vs Gaddy's ~40 M (25× smaller)** (unverified — subresearch
  pass) [20].
- **Myovox (2026)** [27] is a careful single-author replication/extension on the single-subject
  emg2speech General Corpus (**vocalised**, 31-channel — *not* silent speech; do not quote its
  18.53% as silent-speech SOTA). It takes the corpus from a published **51.17% WER** to **18.53%
  WER** in three separable moves: (1) recover missing open-vocab decode settings →
  a faithful 40.63% WER / 39.02% PER baseline; (2) causal encoder → bidirectional Conformer trained
  by four-term cross-modal distillation against WavLM-Large layer-9 features → 26.14% WER / 22.34%
  PER; (3) ensemble two acoustic models and rerank their multi-scale n-best lists with a
  QLoRA-fine-tuned 7B LM → 18.53% WER. **The decisive negative result**: reranking is exhausted at
  ~18.5% because the binding constraint is the EMG acoustic **phone error rate (~20.9%)**, not the
  LM; the correct words are absent from the acoustic posteriors, so no reranker can reach the
  **9.30% n-best oracle**. Test = 400 held-out sentences under the authors' 8,500/760/400 split [27].
  This is one author's preprint (unverified by peer review) but it is the clearest available
  quantification of where the errors actually come from.
- **Typing proxy, causal attention (2025)** [15]: on sEMG typing, attention architectures reduce
  online generic CER **24.98% → 20.34%** and offline personalised CER **10.86% → 10.10%**, while
  remaining fully causal, with a lightweight LM correction pipeline.
- **Typing proxy, new SOTA (SplashNet, NeurIPS 2025)** [38]: three changes — Rolling Time
  Normalization, Aggressive Channel Masking, and a bilateral Split-and-Share encoder — plus a
  five-fold spectral-resolution cut (33→6 bands) give **35.7% CER zero-shot / 5.5% after
  fine-tuning** (mini variant 36.4% / 5.9%) versus the cited baseline's 51.8% / 7.0%, i.e. 31% and
  21% relative improvements "without requiring additional data" [38].
- **Self-supervised pretraining on EMG (emg2vec, EMBC 2024)** [37]: self-supervised pretraining for
  EMG-based silent speech reports a relative WER improvement over from-scratch training of **7.32%**
  with full labelled data and **5.18%** with only **20%** labelled data (speech synthesis +2.91% at
  20% data). The abstract does not state the corpus (unverified — subresearch pass; the IEEE
  abstract was not retrievable) [37].
- **Decoder-loss comparison.** emg2qwerty tested cross-entropy, CTC, seq2seq and RNN-T and found
  CTC best for its setting [5]; for the LLM-adaptor task, cross-entropy (0.65 WER) beat CTC (0.70)
  and a BiLSTM backbone (0.53) beat Transformer (0.79) (unverified — subresearch pass) [16].

### 3.4 LLM rescoring

1. **Post-hoc rescoring (LISA)** [10]: beam search yields k candidates; an LLM picks the best. It is
   model-agnostic and can run off-device. MONA LISA used beam size 5000 at inference (≈1% WER gain
   over smaller beams) and ensembled the 10 best models by validation WER [10]. This is the
   mechanism behind the 12.2% silent / 3.7% vocal numbers [10].
2. **LLM as decoder/adapter** [16]: map EMG features into an LLM's input space and decode directly,
   reporting average **WER 0.49** on a **closed-vocabulary** unvoiced EMG-to-text task and nearly
   20% improvement over specialised models with "just six minutes" of data [16].
3. **Ceiling** [27]: if the acoustic phone error rate is ~20.9%, no LM rescoring can beat the 9.30%
   n-best oracle. Expect LLM rescoring to give large gains at high baseline WER and to saturate
   once the acoustic model is the bottleneck.

## 4. How much per-user data is needed

| Regime | Data used | Result | Source |
|---|---|---|---|
| 10-word command set | 3 participants, ~31 h silently spoken; eval 75 reps/word | **92.01% mean accuracy** (abstract: 92% median), 0.427 s latency | [13] + subresearch pass (unverified) |
| 67-word templated commands | **26 min silent + 30 min vocalised**, 500 utts, single session | **4%** human WER with target transfer (3.6% per subresearch pass) | [1] |
| 65–2,200-word closed corpora | 2–3 h training per subject | best phoneme WER 7.3% (202-word); 8.9% mean (2,200-word) | Meltzner 2018 [29], reported by subresearch pass (unverified) |
| Open-vocab dictation | **18.6 h total** (3.6 h silent parallel + 3.9 h vocalised parallel + 11.2 h vocalised non-parallel), one speaker | 42.2–68% WER (Gaddy); **12.2%** (MONA LISA) | [1][2][10] |
| Open-vocab, short calibration | 27 subjects, **<0.5 h each (21.3 min avg)**; pretrain + fine-tune | **21.7% CER / 31.9% WER** closed 50-sentence corpus; **3 min calibration → 20.5% CER / 31.7% WER, no significant difference from the full ~13-min pool**; no calibration 49.3% CER | [24] |
| Typing proxy personalisation | avg **3.2 h/subject** across ~10 sessions; ~6 sessions (derived ≈1.8 h) for personal models | **51.78% generic vs 6.95% personalised** test CER | [5] |
| Unvoiced EMG, closed vocab | "just six minutes" | WER 0.49; ~20% better than specialised models | [16] |
| On-device commands, repositioned | **<10 min** incremental fine-tuning | **>10% accuracy recovery** after repositioning | [26] |

Inferences:

1. **A closed command set is cheap.** Gaddy's 67-word condition used 26 minutes of silent data in
   one session to reach 4% human WER [1]; SilentWear reaches ~78% on 8 silent commands [26].
2. **Open-vocabulary is expensive.** Every strong open-vocab result retrains on the same ~18.6 h
   single-speaker corpus [1][2][10][3]. No published result demonstrates open-vocab silent-EMG
   decoding from ~1 h of data.
3. **Data was still scaling at 15 h** in Gaddy's Figure 4 ("improvements continue even when
   increasing data size beyond fifteen hours"; exact per-point values are graph-only — approximate)
   [1]. Keep collecting.
4. **Parallel silent+vocalised data is the high-value data.** Removing the non-parallel vocalised
   recordings cost only 3.6 points (71.6% WER), whereas removing a proportional mix of both data
   types cost much more (76%) [1].
5. **Pretraining substitutes for per-user data.** MONA uses LibriSpeech [10]; Le et al. show
   multi-subject pretraining moving macro CER from **74.4% with 1 pretraining participant to 21.7%
   with 26** [24].
6. **Personalisation dominates raw scale.** Same architecture, same data: 51.78% CER generic vs
   6.95% personalised+fine-tuned [5].
7. **Large cross-user generic models are possible for motor tasks, but still benefit from
   personalisation.** CTRL-labs' generic wrist-sEMG interface, trained on data from thousands of
   participants, gives out-of-the-box performance on users not in the training set: median 0.5
   target acquisitions/s in a continuous navigation task, 0.9 gesture detections/s in a discrete
   gesture task, and handwriting at 17.0 adjusted words per minute; personalisation improves input
   bandwidth "up to 30%" [28]. The analogous cross-user generic model for facial speech EMG does not
   yet exist publicly [1][10].

## 5. Recording protocol

From Gaddy [1] and emg2qwerty [5], plus the subresearch pass:

1. **Record every prompt in both modes within one session** so electrode placement matches between
   silent and vocalised; silent is aligned to vocalised by DTW [1]. Some vocalised-only sessions
   (non-parallel) are still useful [1].
2. **Segment at the utterance level** and store the read text with each instance [1].
3. **Re-don the electrodes between sessions** and deliberately capture placement variance
   [1][5]. Gaddy absorbs it with a 32-dim session embedding [1][2]; emg2qwerty uses band-rotation
   augmentation + a rotation-invariance module [5].
4. **Prompts**: Project Gutenberg sentences for open vocabulary [1]; random dictionary words +
   filtered Wikipedia sentences for typing [5]; TIMIT SX / phonetically balanced sets plus the
   user's real vocabulary for a personal corpus (subresearch pass).
5. **Session length**: Gaddy ~30 min of each mode [1]; emg2qwerty avg 18.0 min (range 9.5–47.5) [5];
   Meltzner used 4–6 h with breaks [29] (unverified — subresearch pass). Shorter, frequent sessions are
   easier to sustain.
6. **Quality control**: real-time EMG display and a re-record option; Meltzner [29] excluded 3/19
   subjects for noise/non-attention (unverified — subresearch pass).
7. **Splits**: hold out utterances (Gaddy: 30 val / 100 test) [1]; hold out whole sessions and users
   (emg2qwerty: 8 held-out users, 2 val + 2 test sessions each) [5].

## 6. Real-time constraints and compute

**Sampling and frame rates seen in the literature**

| System | Input | Window / hop | Output frame rate |
|---|---|---|---|
| Gaddy 2020 [1] | 8 ch, 1 kHz | 27 ms window / 10 ms hop | 100 Hz |
| Gaddy 2021 [2] | 8 ch, 1 kHz → 800 Hz | conv ×8 downsample | 100 Hz |
| emg2qwerty [5] | 32 ch, 2 kHz | 32 ms window / **8 ms hop** | 125 Hz |
| Gowda geometry [20] | 22 ch, 5 kHz | 50 ms / 20 ms (v3; unverified — subresearch pass) | 50 Hz |
| SilentWear [26] | 14 ch, 500 Hz | per-utterance (400–1400 ms ablation) | per-utterance |

- **Streaming-ready design, but the benchmark itself is offline.** emg2qwerty trains on 4 s windows
  padded asymmetrically with **900 ms past and 100 ms future** context "to minimize the dependency
  on future inputs and facilitate streaming applications"; TDS receptive field 1 s [5]. It reports
  no latency benchmark and no parameter count [5].
- **Causality costs little.** "Typing Reinvented" (CMU, 2025) converts the pipeline to strictly
  causal encoders: generic **online** CER 24.98% (causal TDS) → **20.34%** (3-layer causal
  Conformer); personalised **offline** CER **10.10%**; generic offline is 43.21%. It states "each
  inference takes roughly 50 ms", users "must wait 4 seconds before the first keystroke appears" in
  its prototype, and proposes a 50 ms sliding window with 4 s historical padding for an "effective
  latency of approximately 100 ms", targeting "under 50 ms" [15].
- **Gaddy's models are non-causal** (bidirectional LSTM/Transformer, ±1 s attention) with no
  streaming evaluation [1][2]; MONA LISA is offline/ensemble [10]. So the ~28%/12.2% open-vocab
  numbers come with an unmeasured latency penalty.
- **The only measured low-latency streaming neural speech decoding found** is brain-to-voice work on
  ECoG decoding in 80-ms increments, whose framework is claimed to generalise to EMG; no surface-EMG
  latency measurement exists in that line (reported by subresearch pass — unverified) [33].
- **On-device command decoding is demonstrated.** SilentWear deploys a **15,489-parameter**
  SpeechNet CNN (8-bit post-training quantisation, ≈15.13 kB) on a GAP9 MCU + NE16 NPU:
  **2.47 ms** and **63.9 µJ per inference**, **20.5 mW** total for acquisition + inference +
  wireless, **27.1 h** on a 150 mAh Li-Po, for 8 silent commands (77.5±6.6% accuracy) [26]. AESSI
  reports **31.70 ms** median preprocessing + inference on CPU replay for a 25-sentence around-ear
  silent interface (92.24% mean accuracy) [25].
- **No phone / Jetson / Cortex-M benchmark for EMG-to-*text*** was found; the only measured
  embedded results are classification/command systems [26][25]. Bioformers (Sensors 2023) report
  transformer edge optimisation on a GAP8 RISC-V SoC for sEMG gesture recognition with 7.8×–44.5×
  less energy per inference and +3.1% accuracy vs a CNN baseline, plus 1.03×–1.35× further savings
  from dynamic (early-exit) inference (reported by subresearch pass — unverified) [31].
- **Model sizes.** Gowda's geometry paper measures Gaddy's baseline at ~**40 M** parameters and
  reports its own geometric/SPD model at ~**1.4 M** (25× smaller) with **27% WER vs Gaddy's 64%**
  at matched 8 electrodes / 1 kHz (unverified — subresearch pass; the fetched text confirms the
  SPD-manifold approach and data/parameter efficiency claim but not the numbers) [20]. MONA LISA's
  ResNet/Transformer stack is much larger [10][11].
- **Training compute.** MONA LISA: one **A100 80 GB** for 24–48 h per model, 60 models for the
  sweep [11]; contrastive batches up to 128K–256K timesteps fit on 80 GB [10]. emg2qwerty: generic
  on 8× A10, personalised on 1× A10 each, 150 epochs [5]. Gaddy's models fit a single consumer GPU
  [1][2]. SilentWear trained on a GTX 1080 (reported — unverified) [26].
- **RTX 3090 (24 GB).** Gaddy-scale training and inference are comfortable; MONA-scale contrastive
  training is not (80 GB was required) [10][11]. Fine-tuning a published Gaddy checkpoint [3] is the
  sensible 3090 path to open-vocab. Phone/MCU inference for open-vocab models is **unverified**;
  MCU inference is proven only for tiny command classifiers [26].
- **Latency budgets.** The electromechanical delay means electrical excitation precedes physical
  articulation by ~60 ms, enabling predictive/negative-latency decoding [14][5]. HCI response-time
  limits are **0.1 s** for "reacting instantaneously", **1.0 s** for uninterrupted flow, and
  **10 s** for keeping attention [30]; a 2017 study measured a ~60 ms perception threshold for
  mouse latency (reported by subresearch pass — unverified) [32]. A silent-typing interface that
  wants to feel direct therefore needs end-to-end latency near or below ~100 ms — the range the
  causal emg2qwerty work is targeting [15], and already achieved for command classification on an
  MCU (2.47 ms) [26].

## 7. Evaluation: WER/CER and session drift

- **Metrics.** WER = word-level Levenshtein / reference length; CER = character-level Levenshtein /
  reference length [5]. Gaddy evaluates **audio synthesis** by transcribing synthesised audio with
  DeepSpeech 0.7.0 and computing WER [1][2]; emg2qwerty computes CER directly against the keylogger
  [5]. Always state whether the metric is on synthesised audio or direct text: Gaddy's 36% vs 28%
  gap is exactly that distinction [3].
- **Usability thresholds.** emg2qwerty: "models tend to become usable at a CER of approximately 10%
  or less" [5]. MONA LISA: the SSI viability threshold is "approximately 15% WER" [10].
- **Session drift is the dominant error source.** emg2qwerty attributes domain shift to cross-user
  anatomy, cross-session band placement, and cross-user behaviour; unpersonalised performance on a
  new user is **over 50% CER**, and its personalisation stack recovers to 6.95% [5].
- **Cross-session adaptation numbers.** Wand et al. (2018) adapt the network frontend to a new
  session with **unsupervised** domain-adversarial training [23]; the subresearch pass reports target
  session WER 18.8% → 15.6% (dev) and 29.9% → 28.5% (held-out eval) (unverified — the fetched
  abstract states the method, not the numbers) [23]. Wand & Schultz (2014) pre-train on multiple
  sessions and adapt to the current session without an enrollment phase; the subresearch pass
  reports 7-session WER **34.9% → 30.2%** and 15-session **27.0% → 23.3%** (unverified — abstract
  only describes the method) [36]. Both use **audible** EMG, so the drift magnitude for silent
  articulation may differ.
- **Cross-day reuse is achievable for small command sets.** AESSI: 24 participants, 44 recordings,
  25 Mandarin sentences; **92.24% mean accuracy with no test-day calibration**; five participants
  retested **≥21 days later** completed 50 randomized online tests each at **98.0% overall
  accuracy**, with 31.70 ms median CPU latency [25]. SilentWear shows the opposite tension:
  accuracy drops 84.8%→71.1% (vocalised) and 77.5%→59.3% (silent) across sessions, recovered by
  <10 min of incremental fine-tuning [26].
- **Leakage trap.** Myovox shows what happens when model selection leaks: excluding the evaluation
  sentences from all training data changes CER/WER from 21.7%/31.9% to **78.6%/99.9%** [24]. Keep
  strict train/val/test separation by sentence, session and day.

## 8. Staged training plan for this build

Accuracy expectations are anchored to the sources above. Plan for the calibration burden to shrink
as pretraining improves.

**Stage 0 — harness and reproduction (week 1–2).** Fork `dgaddy/silent_speech` (MIT) [3][12].
Download the CC-BY Gaddy corpus [4] and reproduce a published number (e.g. the ~28% CTC WER
[3]) before recording anything. Set up MFA phoneme alignments [11] and a KenLM/CTC decoder [3].
Add the emg2qwerty personalisation pattern (generic → per-user fine-tune) as a template [5][6].
*Exit criterion: one end-to-end number reproduced from a published checkpoint.*

**Stage 1 — 20–100 command words (month 1 of recording).** Record parallel silent + vocalised
utterances of the same prompts in the same session, 8 facial channels at 1 kHz, Gaddy's electrode
map [1]. Target ~30 min of silent data over 3–5 short sessions, dozens of repetitions per command.
Train a small closed-set classifier on the **silent** recordings. Expected: **~78–92% word
accuracy**; anchors are SilentWear's 77.5±6.6% on 8 silent commands [26] and AlterEgo's 92% median
[13]. *Exit criterion: owner can trigger ~20–50 commands silently.*

**Stage 2 — phrases and templated sentences (months 2–3).** Extend to a few hundred phrases /
slot-filling grammar (Gaddy's date-time templates are the model [1]). Train CTC sequence models on
silent EMG with a character/word LM. Expected: **single-digit to ~15% WER**; anchors are Gaddy's
4% on 67 templated words [1], Le et al.'s 21.7% CER / 31.9% WER on a closed 50-sentence corpus with
21.3 min of subject data [24], and the LLM-adapter's 49% WER from six minutes [16].

**Stage 3 — open-vocabulary dictation (months 3–12, ≥18 h silent data).** Only attempt at Gaddy
corpus scale. In increasing order of risk/cost:
1. Gaddy 2021 recipe: raw EMG → residual conv → relative-position Transformer + auxiliary phoneme
   loss + DTW target transfer + CTC text decoder [2][3]. Published: **~28% WER** direct text,
   42.2% audio-synthesis automatic, 32.3% human [2][3].
2. Add LLM rescoring over top-k beams with a strong local/API LLM [10][16]. Published best:
   **12.2% open-vocab silent WER** [10]; repo claims 7.3% validation [11]. Expect saturation near
   the acoustic PER limit [27].
3. Add cross-modal/external-audio pretraining (MONA-style) or S3-target regression [10][18]. This
   needs A100-class memory for the contrastive variant [10]; on a 3090, fine-tune a published
   checkpoint or use frozen encoders/smaller batches [3].

**Cross-cutting.** Keep a per-session embedding or adapt per session [1][5]. Report session-wise and
user-wise splits, and re-measure drift every session [5]. Expect the "Silent Lombard Effect" —
articulation drifts without auditory feedback — to move the silent data away from the vocalised
reference over time [14]. Budget **~3 min of target-subject calibration** per session if the
Le et al. result transfers [24], and **<10 min** of incremental fine-tuning after repositioning
[26].

## Sources

1. David Gaddy, Dan Klein, *Digital Voicing of Silent Speech*, EMNLP 2020, arXiv:2010.02960 — https://arxiv.org/abs/2010.02960 (HTML: https://arxiv.org/html/2010.02960v1)
2. David Gaddy, Dan Klein, *An Improved Model for Voicing Silent Speech*, ACL 2021, arXiv:2106.01933 — https://arxiv.org/abs/2106.01933 (HTML: https://arxiv.org/html/2106.01933v2)
3. `dgaddy/silent_speech` README (WER figures, Zenodo model links, toolchain) — https://github.com/dgaddy/silent_speech (raw: https://raw.githubusercontent.com/dgaddy/silent_speech/master/README.md)
4. David Gaddy, *Silent Speech EMG* dataset, Zenodo, 2 Oct 2020, DOI 10.5281/zenodo.4064409, CC-BY-4.0 — https://zenodo.org/records/4064409
5. V. Sivakumar et al., *emg2qwerty: A Large Dataset with Baselines for Touch Typing using Surface Electromyography*, NeurIPS 2024, arXiv:2410.20081 — https://arxiv.org/abs/2410.20081 (HTML: https://arxiv.org/html/2410.20081v3)
6. `facebookresearch/emg2qwerty` README (dataset size, decoders, licence statement, checkpoints) — https://github.com/facebookresearch/emg2qwerty (raw: https://raw.githubusercontent.com/facebookresearch/emg2qwerty/main/README.md)
7. `facebookresearch/emg2qwerty` LICENSE — actual text is **CC BY-NC-SA 4.0** — https://raw.githubusercontent.com/facebookresearch/emg2qwerty/main/LICENSE
8. S. Salter et al., *emg2pose: A Large and Diverse Benchmark for Surface Electromyographic Hand Pose Estimation*, NeurIPS 2024, arXiv:2412.02725 — https://arxiv.org/abs/2412.02725
9. `facebookresearch/emg2pose` LICENSE — **CC BY-NC-SA 4.0** — https://raw.githubusercontent.com/facebookresearch/emg2pose/main/LICENSE
10. T. Benster, G. Wilson, R. Elisha, F. R. Willett, S. Druckmann, *A Cross-Modal Approach to Silent Speech with LLM-Enhanced Recognition* (MONA LISA), arXiv:2403.05583 — https://arxiv.org/abs/2403.05583 (HTML: https://arxiv.org/html/2403.05583v1)
11. `tbenst/silent_speech` README (MONA LISA; 7.3% validation WER; A100 24–48 h/model, 60-model sweep; 38-char CTC) — https://raw.githubusercontent.com/tbenst/silent_speech/master/README.md
12. `tbenst/silent_speech` LICENSE — MIT text, Copyright 2021 David Gaddy (inherited from the fork) — https://raw.githubusercontent.com/tbenst/silent_speech/master/LICENSE
13. A. Kapur, S. Kapur, P. Maes, *AlterEgo: A Personalized Wearable Silent Speech Interface*, IUI 2018, pp. 43–53 — https://www.media.mit.edu/publications/alterego-IUI/
14. K. Xu et al., *Silent Speech Interfaces in the Era of Large Language Models: A Comprehensive Taxonomy and Systematic Review*, arXiv:2603.11877 — https://arxiv.org/abs/2603.11877 (HTML: https://arxiv.org/html/2603.11877v1)
15. K. Lee et al., *Typing Reinvented: Towards Hands-Free Input via sEMG*, arXiv:2511.18213 — https://arxiv.org/abs/2511.18213
16. P. Mohapatra, A. Pandey, X. Zhang, Q. Zhu, *Can LLMs Understand Unvoiced Speech? Exploring EMG-to-Text Conversion with LLMs*, ACL 2025, arXiv:2506.00304 — https://arxiv.org/abs/2506.00304
17. R. Zhao et al., *An open dataset of multidimensional signals based on different speech patterns in pragmatic Mandarin*, Scientific Data 2025 — https://www.nature.com/articles/s41597-025-06213-z (**full text not fetched; most fields unverified**)
18. H. T. Gowda, D. C. Comstock, L. M. Miller, *emg2speech: Synthesizing speech from electromyography using self-supervised speech models*, arXiv:2510.23969 — https://arxiv.org/abs/2510.23969
19. `HarshavardhanaTG/emg2speech` — LICENSE file absent (HTTP 404) — https://github.com/HarshavardhanaTG/emg2speech (raw: https://raw.githubusercontent.com/HarshavardhanaTG/emg2speech/main/LICENSE)
20. H. T. Gowda, Z. D. McNaughton, L. M. Miller, *Geometry of orofacial neuromuscular signals: speech articulation decoding using surface electromyography*, arXiv:2411.02591 — https://arxiv.org/abs/2411.02591
21. M. Wand, M. Janke, T. Schultz, *The EMG-UKA corpus for electromyographic speech processing*, Interspeech 2014 — https://www.isca-archive.org/interspeech_2014/wand14b_interspeech.html
22. S. Zhao, F. Rudzicz, *The KARA ONE Database* (EEG, not EMG), ICASSP 2015 — http://www.cs.toronto.edu/~complingweb/data/karaOne/karaOne.html
23. M. Wand, T. Schultz, J. Schmidhuber, *Domain-Adversarial Training for Session Independent EMG-based Speech Recognition*, Interspeech 2018 — https://www.isca-archive.org/interspeech_2018/wand18_interspeech.html (**numeric WER values reported by a subresearch pass, not independently fetched — unverified**)
24. C. Le et al., *Multi-Subject Pretraining Enables Short-Calibration Personalization for Closed-Corpus Surface EMG Speech Decoding*, arXiv:2609.21288 — https://arxiv.org/abs/2609.21288
25. X. Xu et al., *AESSI: An Around-Ear Silent Speech Interface for Cross-Day Online Reuse without Test-Day Calibration*, arXiv:2609.21436 — https://arxiv.org/abs/2609.21436
26. G. Spacone et al., *SilentWear: an Ultra-Low Power Wearable System for EMG-based Silent Speech Recognition*, arXiv:2603.02847 — https://arxiv.org/abs/2603.02847
27. V. Madishetty, *Myovox: Reading Speech from the Muscles of the Face*, arXiv:2609.17548 — https://arxiv.org/abs/2609.17548
28. CTRL-labs at Reality Labs, D. Sussillo, P. Kaifosh, T. Reardon, *A generic noninvasive neuromotor interface for human-computer interaction*, bioRxiv 2024, DOI 10.1101/2024.02.23.581779 — https://www.biorxiv.org/content/10.1101/2024.02.23.581779v1
29. G. S. Meltzner et al., *Development of sEMG sensors and algorithms for silent speech recognition*, J. Neural Engineering 15(4):046031, 2018 — https://doi.org/10.1088/1741-2552/aac965 (**full text not fetched; all numbers from a subresearch pass — unverified**)
30. J. Nielsen, *Response Times: The 3 Important Limits*, Nielsen Norman Group, 1993 — https://www.nngroup.com/articles/response-times-3-important-limits/
31. X. Xie et al., *Reducing the Energy Consumption of sEMG-Based Gesture Recognition at the Edge Using Transformers and Dynamic Inference*, Sensors 23(4):2065, 2023 — https://doi.org/10.3390/s23042065 (**full text not fetched — unverified**)
32. S. Forch, T. Franke, N. Rauh, J. F. Krems, *Are 100 ms Fast Enough? Characterizing Latency Perception Thresholds in Mouse-Based Interaction*, HCII 2017 — https://doi.org/10.1007/978-3-319-58475-1_4 (**full text not fetched — unverified**)
33. P. Littlejohn, *AI-Driven Speech Neuroprostheses for Restoring Naturalistic Communication and Embodiment*, UC Berkeley EECS-2025-147, 2025 — https://www2.eecs.berkeley.edu/Pubs/TechRpts/2025/EECS-2025-147.html (**not fetched — streaming result reported by subresearch pass — unverified**)
34. A. Kapur, U. Sarawgi, E. Wadkins, M. Wu, N. Hollenstein, P. Maes, *Non-Invasive Silent Speech Recognition in Multiple Sclerosis with Dysphonia*, PMLR 116:25–38, 2020 — https://proceedings.mlr.press/v116/kapur20a.html
35. E. Wadkins, *A Continuous Silent Speech Recognition System for AlterEgo*, MIT MEng thesis, 2019 — http://www.ericwadkins.com/doc/MEng_Thesis_FINAL.pdf (**full text not fetched — unverified**)
36. M. Wand, T. Schultz, *Towards real-life application of EMG-based speech recognition by using unsupervised adaptation*, Interspeech 2014 — https://www.isca-archive.org/interspeech_2014/wand14_interspeech.html (**numeric values reported by a subresearch pass — unverified**)
37. H. Hou et al., *emg2vec: Self-supervised Pretraining in Electromyography-based Silent Speech Interfaces*, IEEE EMBC 2024, DOI 10.1109/EMBC53108.2024.10781736 — https://doi.org/10.1109/EMBC53108.2024.10781736 (**abstract page not retrievable — unverified**)
38. N. Hadidi, J. Chan, E. Feghhi, J. C. Kao, *SplashNet: Split-and-Share Encoders for Accurate and Efficient Typing with Surface Electromyography*, NeurIPS 2025 — https://papers.nips.cc/paper_files/paper/2025/hash/f29af347aedbdaa316043aa8457a8fb6-Abstract-Conference.html

## Key takeaways for the build

- **Start with Gaddy.** `dgaddy/silent_speech` (MIT) + the CC-BY Gaddy corpus is the only
  fully open, directly relevant stack: 1 speaker, 8 ch @ 1 kHz, silent + parallel vocalised,
  9,828-word open vocabulary [1][3][4].
- **Closed commands are cheap; open vocab is not.** 26 min of silent data reached 4% human WER on a
  67-word templated set [1]; every strong open-vocab result uses the same ~18.6 h single-speaker
  corpus [1][2][10].
- **Silent ≠ vocalised.** Train on silent data; use vocalised recordings only as alignment/target
  sources (DTW + CCA + predicted-audio, or latent-space DTW) [1][2][10] — direct transfer from
  vocalised models costs tens of WER points [1].
- **Personalise.** 51.78% generic vs 6.95% personalised+fine-tuned CER on the typing proxy [5];
  SplashNet's architectural changes push the fine-tuned figure to **5.5%** and zero-shot to 35.7%
  with no extra data [38]; only ~3 min of target-subject calibration may be needed once a
  multi-subject model exists [24].
- **The best demonstrated silent open-vocab number is 12.2% WER** (MONA LISA, non-invasive silent
  EMG [10]); Gaddy's own CTC text model is ~28% [3]. Treat >15% WER as the viability threshold [10].
- **LLM rescoring helps but has a ceiling.** LISA gives the 28.8→12.2 jump [10]; Myovox shows the
  acoustic PER (~20.9%) caps reranking at ~18.5% with a 9.30% oracle [27]. Myovox's 18.53% is
  **vocalised**, not silent — do not quote it as silent-speech SOTA [27].
- **Pretraining on external audio or other users buys data efficiency.** LibriSpeech via cross-modal
  contrast [10]; S3/WavLM targets [18][27]; multi-subject pretraining 74.4%→21.7% CER [24];
  self-supervised EMG pretraining (emg2vec) reports ~5.2% relative WER gain with only 20% labelled
  data (unverified) [37].
- **On-device command decoding is proven; on-device open-vocab is not.** SilentWear: 15k-param CNN,
  63.9 µJ/inference, 2.47 ms, 20.5 mW, >27 h on an MCU [26]; AESSI: 31.70 ms CPU [25].
- **Licence traps:** emg2qwerty/emg2pose are **CC BY-NC-SA 4.0** (README for emg2qwerty is wrong) [7][9];
  emg2speech has **no licence** (all rights reserved) [19]; KenLM is LGPL-2.1.
- **Plan for drift and leakage.** Re-measure session-to-session; re-don electrodes deliberately [5];
  excluding eval sentences changed CER/WER from 21.7/31.9 to 78.6/99.9 in one study [24].

## Open questions

1. **How much of Gaddy's transfer pipeline still matters** once you have months of your own paired
   silent+vocalised data? Possibly none — but nobody has published a single-user, no-vocalised-data
   open-vocab result.
2. **Is "silently mouthed" enough, or does the owner need truly still-face internal articulation?**
   All open-vocab numbers use mouthed speech [1]; internal-only figures are much weaker and mostly
   closed-vocab [13].
3. **Does 3-minute calibration [24] transfer to a high-channel facial montage and open vocabulary**,
   or is it specific to a standardised montage and a closed 50-sentence corpus?
4. **On-device open-vocabulary inference**: no fetched source shows a full open-vocab EMG-to-text
   model running on a phone/MCU; the MCU demo is a 15k-parameter command classifier [26].
5. **Electrode-channel budget**: Gaddy used 8 [1], UC Davis 22 [20], emg2speech 31 [27]. How few
   facial channels retain open-vocab performance is not established in the sources fetched.
6. **LLM rescoring privacy/latency**: LISA needs GPT-3.5/4 [10]; a local 7B reranker worked for
   Myovox [27], but its latency and integration with a wearable loop are unreported.
7. **Long-term drift of silent articulation** (the "Silent Lombard Effect" [14]) over months of
   one-user data: no longitudinal single-user silent-EMG study was found.
