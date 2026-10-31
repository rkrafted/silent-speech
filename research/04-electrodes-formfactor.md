# Track 04 — Electrode sites and concealed form factors

*Research notes for a personal R&D silent-speech wearable. Inline `[n]` citations map to the
numbered Sources list at the end. Demonstrated results are separated from claims/marketing. All
numbers are quoted exactly as the source gives them. Pages I could not fetch myself are marked
"unverified". PDFs were read through a text proxy (`r.jina.ai`) because direct PDF fetch is
unsupported.*

*Scope: which facial/neck sites carry silent-speech information; electrode materials for long
wear; concealed form factors (jawline, under-chin, behind-ear, glasses, in-ear, collar); daily-wear
drift and recalibration; then concrete concealed layouts ranked by invisibility vs expected
accuracy.*

Status: COMPLETE (v1) — all sub-searches merged. Length is above the suggested 2,000–5,000-word
target because the track contains many independent verified numbers (sites, impedances, wear times,
accuracies); nothing unverified is presented as fact.

## 1. Which facial and neck sites carry the silent-speech signal

### 1.1 AlterEgo (MIT Media Lab, IUI 2018) — the reference layout

AlterEgo is the closest published system to this project: non-invasive, 7 channels, silent
(mouth closed, no discernible movement), single-user personalised. Full paper [2].

**Electrodes and signal chain.** The device uses **7 channels** sampled at **250 Hz**, differenced
against a reference placed "either on the wrist or the earlobe", with bias-based cancellation of
~60 Hz line interference, and **24× gain** (Texas Instruments / OpenBCI) [2]. Two electrode
variants were built: "TPE plastic, gold plated silver electrodes (1.45 mm diameter conductive
area), in combination with Ten20 (polyoxyethylene (20) cetyl ether) conductive paste … or passive
dry Ag/AgCl electrodes (4 mm diameter conductive area)". The dry option works, but the paper
states "the former offer superior data quality. Therefore, we report experiments, data collection
and results based on the former" [2].

**Where the 7 electrodes went.** Signals are sourced from: "the laryngeal region, hyoid region,
levator anguli oris, orbicularis oris, platysma, anterior belly of the digastric, mentum" [2].
Roughly half the channels sit on the neck/larynx/hyoid (front-of-neck, below the jaw) and half on
the lower face around the mouth and chin.

**How those sites were chosen.** The authors started from "an initial 30-point grid spatially
covering" the laryngeal, hyoid, buccal, mental, oral and infraorbital regions, and "ranked
potential target locations according to the filter-based feature ranking, evaluating how signals
sourced from each target were able to better differentiate between word labels". "Symmetrical
equivalents of target locations across the craniocaudal axis were ignored in order to avoid feature
repetition." The final ranking of regions was [2]:

| Rank | Region |
|------|--------|
| 1 | Mental |
| 2 | Inner laryngeal |
| 3 | Outer laryngeal |
| 4 | Hyoid |
| 5 | Inner infra-orbital |
| 6 | Outer infra-orbital |
| 7 | Buccal |

That ranking is directly relevant to concealment: the top four ranked regions (mental = chin,
laryngeal, hyoid) are all **below the mouth**, i.e. hidden from a front view, while the lower-ranked
infra-orbital (under-eye) and buccal (cheek) sites are the visible ones.

**Demonstrated result.** 10 participants (6 female, 19–31, mean age 23.6), none with prior
experience. Each saw 750 randomly sequenced digits and was told to "read the number to themselves,
without producing a sound and moving their lips". Word accuracy was evaluated on an 80/20
train/test split with 10 runs: "The average accuracy over all runs for all the users is 92.01%",
with "92% median word accuracy" [2]. Average computational latency from end of utterance to
transcription was **0.427 seconds** [2]. Vocabulary for this evaluation was the arithmetic set
(10 digits 0–9 plus multiply, add, subtract, divide, percent) — a **closed vocabulary**; the corpus
is ~31 hours of silently spoken text across sessions plus ~5 hours of pilot data [2].

**Form factor in the paper.** "a wearable that is worn around the back of the head, with extensions
landing on the face to record signals from the afore-stated target areas … The band is 3D printed
using photopolymer resin with a brass rod supporting it structurally … The extensions are brass
supports". This is the bulky prototype; MIT News separately reports that "in current experiments,
the researchers are getting comparable results using only four electrodes along one jaw" [1]. That
four-electrode one-jaw configuration is a claim about ongoing work, not a published accuracy figure.

### 1.2 Gaddy & Klein (UC Berkeley, EMNLP 2020) — 8 channels, open vocabulary

The other canonical sEMG-speech dataset. Full paper [3].

**Electrodes and signal chain.** "Eight channels are collected at a sample rate of 1000 Hz",
OpenBCI Cyton board; "Gold-plated electrodes are used with Ten20 conductive electrode paste";
"We use a monopolar electrode configuration, with a shared reference electrode behind one ear. An
electrode connected to the Cyton board's bias pin is placed behind the other ear" [3]. The
reference/bias are **behind the ears** — exactly where a hearing-aid pod would sit.

**The eight sites (Table 3 of [3]):**

| # | Location |
|---|----------|
| 1 | left cheek just above mouth |
| 2 | left corner of chin |
| 3 | below chin back 3 cm |
| 4 | throat 3 cm left from Adam's apple |
| 5 | mid-jaw right |
| 6 | right cheek just below mouth |
| 7 | right cheek 2 cm from nose |
| 8 | back of right cheek, 4 cm in front of ear |
| ref | below left ear |
| bias | below right ear |

Asymmetric (right-biased) montage. Sites 2 and 3 are **under/behind the chin**, site 4 is on the
**throat**; sites 5–8 are on the visible right side of the face, but site 8 is "4 cm in front of
ear", near the jaw hinge where a glasses temple or sideburn would hide it.

**Dataset.** Single speaker, **18.6 hours** total: 3.6 h silent + 3.9 h vocalized parallel data
(1588 utterances) and 11.2 h non-parallel vocalized (5477 utterances); open vocabulary of
**9828 words**; a separate closed-vocabulary set of 67 words (dates/times) [3].

**Demonstrated results (silent input, generated audio transcribed).**

| Condition | Metric | Baseline trained on vocalized EMG | Gaddy target-transfer model |
|---|---|---|---|
| Closed vocab (67 words) | human WER | 88.8% | **3.6%** |
| Closed vocab, throat electrode removed | human WER | 64.6% | — |
| Open vocab (9828 words) | human WER | 95.1% | **74.8%** |
| Open vocab | automatic WER (DeepSpeech) | 91.2% | **68.0%** |
| Open vocab, throat electrode removed | automatic WER | 88.0% | — |

All from [3]. ASR WER on the original vocalized test audio was 9.5%, "a lower bound for this
evaluation" [3]. These are **silent (mouthed) input** results — the strongest evidence that
facial+neck sEMG carries word-level information without voicing.

**Ablation: which channels matter (Section 4.3.2 of [3]).** They "sample 10 random combinations of
four electrodes to remove (out of 70 possible combinations)". The three best four-electrode subsets
removed {4,5,7,8}, {3,5,7,8}, {2,5,7,8}. Electrodes **5, 7, 8 (mid-jaw, upper cheek, back cheek)
"appear in all of these, indicating that they may be contributing less to the performance of the
model"**. Removing those three alone gave a WER of **75.3%** versus **68.0%** for all eight. The
best four-electrode model reached **76.8%** WER — worse than eight electrodes. Within this
8-channel set, the mouth/chin/throat channels carry most of the information and the cheek/jaw
channels carry least; but dropping channels still costs accuracy in open vocabulary.

**The "throat electrode" caveat.** Removing site 4 (throat) *improved* a model trained only on
vocalized EMG (88.8%→64.6% closed; 91.2%→88.0% open) [3]. That is not evidence that the throat is
useless. The authors explain: "Since one may hypothesize that most of the differences between
silent and vocalized EMG will take place near the vocal folds … removing the throat electrode
substantially improves intelligibility for the direct transfer baseline. Although this modification
removes potentially useful information, it also removes divergence between the silent and
vocalized EMG signals" [3]. The laryngeal/throat channel is where silent and vocalized articulation
differ most — for a **silent-only** system that is fine; for a cross-mode system it is a domain-shift
problem to solve, not a channel to delete.

### 1.3 AlterEgo in MS patients with dysphonia — 8 electrodes, 4 face + 4 neck

Follow-up study [4] with 3 MS patients with dysphonia. "the device uses 8 signal electrodes -
4 on the face and 4 on the neck - and a reference and bias electrodes on each earlobe".
Electrodes were "pre-gelled Ag/AgCl surface electrodes"; data digitized with a **24-bit** ADC at
**250 Hz**. "The electrode positions were initially chosen from Kapur et al. (2018), and further
empirically tweaked after repeated testing for feature-dense signals." (A Figure 2 caption says
"sampled at 1 kHz" while the Methods say 250 Hz — inconsistent; the Methods figure is the reliable
one.)

**Demonstrated result:** 15 sentences × 10 trials per patient, 15-class sentence classification.
Test accuracy 0.79 (±0.01), 0.87 (±0.01), 0.77 (±0.02) for P1–P3; mean overall accuracy 0.81;
mean information transfer rate 203.73 bits/min [4]. This is **whole-sentence classification with
15 classes**, not open-vocabulary word decoding.

### 1.4 Under-chin and jawline only — the e-tattoo patch

Liu et al. (2020) attached an epidermal sEMG patch "to a tester's lower jaw and the left and right
sides of the face, representing three different sEMG channels from three targeted muscle groups":
**anterior belly of digastric (ABD), buccinators (BUC), and zygomaticus (ZYG)** [8]. The ABD
electrode sits under the chin (concealed); BUC and ZYG are on the visible cheek. Silent-speech
results, 30 trials per word, 10-fold cross-validation, LDA classifier [8]:

| Instruction set | Words | Combined 3-channel accuracy | Best single channel |
|---|---|---|---|
| Action (Front, Back, Left, Right, Stop) | 5 | 89.6 ± 0.6% | 80.9 ± 0.9% |
| Emotion (Happy, Sad, Hello, Goodbye, Hug, Love) | 6 | 92.7 ± 0.5% | 81.9 ± 0.6% |

(The abstract quotes 89.04% and 92.33%; the Results text quotes 89.6 ± 0.6% and 92.7 ± 0.5% —
a small internal inconsistency, both from [8].) In a real-time HMI demo the accuracy dropped to
**77.6%** for the 5 action commands (ABD channel) and **83.6%** for the 6 emotion commands (ZYG
channel) [8]. This is **one tester**, 5–6 classes, word classification — not open vocabulary — but
it is direct evidence that a channel on the **under-chin (ABD)** muscle carries discriminative
silent-speech information.

### 1.5 Channel reduction: how few electrodes, and which ones

This is the decisive question for concealment, and the literature converges hard.

**AlterEgo/Berkeley-style optimised arrays.**
- Zhu et al. recorded **120 closely spaced electrodes** over facial and neck muscles for 10 silently
  spoken digits. "only ten optimal electrodes could achieve a classification accuracy of 86% for
  English and 94% for Chinese", versus **40 non-optimised electrodes** for comparable accuracy; the
  optimal sites were "mostly distributed on the neck instead of the facial region" [38].
- Deng et al. reduced **64-channel** arrays to **8 separate electrodes** for 33 Chinese subvocal
  words, using transfer learning robust to electrode shift and cross-user variability (no exact
  accuracy in the abstract) [60].
- A 320-channel facial+neck array (10 subjects, 14 vowel and 15 consonant tasks) reached
  **85.78% (consonants)** and **79.42% (vowels)**, with left–right symmetric activation
  (correlation "> 0.9") [39].
- Zhuang et al. (4 subjects, 5 Chinese phrases) found **neck-muscle classification accuracy higher
  than facial**, and combining neck + face higher again [59].

**Gaddy's own channel ablation (the strongest single dataset).** The EMNLP 2020 paper sampled
10 random four-electrode-removal sets of 70; the best removed {4,5,7,8}, {3,5,7,8}, {2,5,7,8}, with
the **best four-electrode model at 76.8% WER versus 68.0% for all eight**, and removing only
5,7,8 alone giving **75.3%** [3]. Gaddy's **PhD dissertation** went further, sampling **35 of the 70
four-electrode subsets**: the best were **{1,2,3,8} = 45.1% WER**, **{2,3,4,7} = 46.0%**,
**{1,2,3,7} = 46.6%**; *all* four-electrode models ranged **~45–54% WER (9–18 points worse than all
electrodes)**. The dissertation's electrode-importance order is **2, 3, 1, 7, 4, 6, 8, 5**, and it
states that "the two electrodes on and below the chin are the most important … could be picking up
tongue movement", while the outer jaw and far-back cheek are least important [61]. Cross-session
held-out WER in the dissertation was **41.3%, 41.8%, 43.6%, 47.3%** — roughly **5–11 points worse**
than in-session; that dissertation says a session embedding "did not substantially improve
performance so was not used", whereas the 2020 paper did use a 32-dimensional session embedding
[3][61].

**Independent re-analysis of the same 8-channel dataset.** Hwang, Lee & Lee (2026) found the
backward-elimination order **6, 7, 8, 5, 4, 1** (leaving electrodes 2 and 3 most critical); the
single-removal impact order **3, 2, 7, 1, 5, 4, 8, 6**; **single-channel WER exceeded 100%**; and
the best four-electrode subset **{1,3,5,6} = 47.2% WER** [62]. Per-phoneme error rate was
**16.0% with 8 channels** vs **17.1%** even for the worst single-channel ablation, and each site
carried a different phonetic role: electrode 8 (posterior masseter) for bilabials, 7 (zygomaticus
major) for high front vowels, 3 (sternohyoid) for voiceless fricatives/low vowels, 2 (depressor
anguli oris) for labiodentals, 6 (orbicularis oris) for round vowels [62]. Note the **disagreement
with Gaddy**: Gaddy's dissertation says the chin/submental pair (2,3) dominates and 8 is least
useful; Hwang picks 8 as critical for bilabials. Both agree 2 and 3 are near the top.

**A vocalized-only, open-vocabulary minimum.** Lee et al. (2025) report on **voiced** speech (not
silent): 8 channels **15.5% WER**; 4 electrodes {2,3,4,6} **22.9%**; 3 electrodes {2,4,6}
**31.6%**; 2 electrodes {2,4} **46.9%** [63] — a usable degradation curve. Electrode 2 was strongest
for tongue tip ("anterior genioglossus") and electrode 3 for "posterior submental proximal to
genioglossus"; **electrode 4 (paralaryngeal) alone gave r = 0.73 for loudness and 0.32 for pitch**,
the highest of any single electrode; the minimal 2-electrode set is **submental/chin +
paralaryngeal** [63].

**Other reductions.** A laryngectomy pilot (2026) with a 20-electrode face/jaw/neck montage found
**9 of 20 electrodes captured 95%** of the multi-channel signal, with human WER **20.2%** on 499
dates/times [65]. Satterlee et al. (2025) used a **single EMG channel + a single EEG channel** for
4 sentences/10 words and reported **95.25% sentence-level** accuracy (word-level not stated) [66].

**Net reading:** 2–4 well-chosen channels can work for small closed vocabularies but cost 9–18 WER
points versus a full montage [61][62][63]; the two most consistently valuable channels are
**under-chin/submental (Gaddy 2 and 3)**, and a paralaryngeal/neck channel adds voicing/loudness
information [63].

### 1.6 A hard limit: mouthed speech decodes, "mentally rehearsed" speech did not

Meltzner et al. (Interspeech 2008) used **11 sEMG sensors across six anatomical regions**
(supralabial, labial, sublabial, submental neck, midline neck, lateral neck), 9 subjects, 65 words,
digitised at 20 kHz with a 20–450 Hz band-pass [64]. Results: **vocalized 92.1%**, **mouthed 86.7%**
(digits 98.3% / 96.7%) — but "**mentally rehearsed speech produced no usable signal — recognition
impossible**" [64]. This is the single most important risk in the whole brief: the owner's goal
mentions "internal articulation / subvocalisation". What is demonstrated to work is **minimal but
real articulation** ("voiceless and internal articulation of words … minimal movements", as in
AlterEgo [4]), not pure inner speech with a fully relaxed articulator system. Any layout decision
should be tested against mouthed/minimally-articulated speech, not silently-read text with no muscle
engagement.

### 1.7 Neck-only (necklace / neckband) form factors

Wu et al. (Interspeech 2024) avoid face adhesives entirely: "dry electrodes are placed around the
neck instead." Reported result: "11-word, multi-speaker **voiced** EMG classifiers trained on data
recorded with this device achieve **92.7% accuracy**"; ablations "reveal the importance of having
more than two electrodes on the neck"; and "phonological analyses reveal similar classification
confusions between neck-only and neck-and-face form factors" [5]. **This is voiced (normally
spoken) EMG, 11-word closed vocabulary, word classification.**

The same group's full paper (**SilentWear**) is the better source: "a fully wearable, textile-based
neck interface", 14 differential channels, SpeechNet "a lightweight 15k-parameter CNN",
"achieving an average cross-validated accuracy of 84.8 ± 4.6% and 77.5 ± 6.6% for vocalized and
silent speech, respectively, over eight representative human-machine interaction commands collected
over multiple days"; "In an inter-session setting, the system achieves average accuracies of
71.1 ± 8.3% and 59.3 ± 2.2% for vocalized and silent speech, respectively"; incremental fine-tuning
gave "more than 10% accuracy recovery with less than 10 minutes of additional user data";
"63.9 µJ per inference with a latency of 2.47 ms"; "a total power consumption of 20.5 mW …
enables continuous operation for more than 27 hours" [13]. An earlier conference slide for the same
system quoted 14 channels with SoftPulse dry electrodes, 87 ± 3% (vocalized) / 68 ± 3% (silent)
aggregated, 64 ± 18% / 54 ± 7% inter-session, and <22 mW [11]. The numbers moved between the slide
and the paper — use the arXiv v2 values [13] and the slide for the hardware description.

### 1.8 What this means for site selection

- The information-dense, concealable sites are **mental/chin, submental (below chin), hyoid,
  laryngeal/throat and the jawline**. AlterEgo's top-ranked regions are exactly these [2], Gaddy's
  most valuable channels sit on the mouth/chin/throat [3], and the under-chin ABD channel alone
  identified 5 action words at 80.9 ± 0.9% [8].
- The visible sites — infra-orbital, buccal/cheek, mid-jaw — were ranked lowest by AlterEgo [2] and
  Gaddy's ablation flags them as least useful [3]. Hiding them costs comparatively little.
- Behind-ear/below-ear is already used for **reference and bias** in both systems [2][3], and is
  where a hearing-aid-style pod belongs.
- Neck-only dry electrodes give 92.7% on an 11-word **voiced** task [5] and 77.5 ± 6.6% on an
  8-class **silent** task cross-validated, falling to 59.3 ± 2.2% cross-session after repositioning
  [13]. Silent decoding from the neck alone is therefore demonstrated but degrades hard across
  sessions.
- Open-vocabulary silent decoding from 8 mixed face+neck channels is still only **68% WER
  (automatic) / 74.8% (human)** [3]. Concealment has to be paid for with data and adaptation.

## 2. Electrode technology

### 2.1 Wet Ag/AgCl gel / conductive paste — the accuracy baseline

Every high-accuracy silent-speech result above used wet or pasted electrodes on the face:

- AlterEgo: gold-plated silver, **1.45 mm diameter** conductive area, with Ten20 paste [2].
- Gaddy: gold-plated electrodes with Ten20 paste [3].
- MS study: "pre-gelled Ag/AgCl surface electrodes" [4].
- cEEGrid: "ten flex-printed Ag/AgCl electrodes" per ear, applied with electrolyte gel
  (Abralyt HiCl) and a double-sided adhesive after abrasive-gel and alcohol skin prep [7].

**How good is wet, really?** A 3M Red Dot 2267 electrode pair measured **409 Ω** at 10 Hz against
the AAMI limit of **≤2,000 Ω**, with DC offset **7.7 mV** after >8 h at 2 V DC (AAMI ≤100 mV) [29].
But once applied to skin, a commercial Ag/AgCl gel electrode measured **80.4 kΩ at 10 Hz** on the
forearm [30]. So the datasheet number is not the on-body number.

**How long does it last?** The conductive gel "usually dries within a relatively short period of
time (e.g., 1 h)", which is why clinical recording is "typically limited to less than 1 h"; in a
controlled comparison, SNR fell from **22.6 dB to 10.7 dB after 2 h**, and after 3 h "the Ag/AgCl
signal disappeared" [30]. Reviews also cite "skin reaction ranging from liquid-related discomfort to
eventual allergic contact dermatitis" [32][44]. **Conclusion: wet gel is a bench/calibration
electrode, not a daily-wear electrode.**

### 2.2 Dry electrodes — measured impedance and demonstrated face/neck use

- **AlterEgo's dry option:** "passive dry Ag/AgCl electrodes (4 mm diameter conductive area)" —
  usable, but the wet gold+paste version offered "superior data quality" and was used for all
  reported results [2]. The 92% figure is *not* a dry-electrode result.
- **Metal thin films (20 volunteers, 10 Hz, in vivo during exercise):** skin–electrode impedance was
  **≈4.0 × 10⁵ Ω for Ti–Au**, **≈7.0 × 10⁵ Ω for Ti–Ag and Ti–Cu**, **≈1.7 × 10⁶ Ω** in the
  intermetallic zone, up to **≈3.0 × 10⁷ Ω for Ti–Al**; the hydrogel Ag/AgCl reference averaged
  **1.6 × 10⁵ Ω**. The dry pair was cleaned/disinfected and reused over **14 days**, fixed under
  tape "to keep the same pressure" [32]. Dry metal therefore sits roughly 2.5–200× above wet, and
  needs pressure.
- **Soft dry conductor:** a porous PEDOT:PSS/PDMS sponge (r = 1 cm, t = 2 mm) gave **277.5 kΩ
  without gel** and **12.2 kΩ with conductive hydrogel at 10 Hz**; a planar screen-printed
  PEDOT:PSS electrode of the same size gave **247 kΩ / 63 kΩ**. Motion spikes >1 V appeared with
  planar and Ag/AgCl electrodes but the sponge kept a clean ECG; initial SNR was 23.1 dB (sponge),
  22.6 dB (Ag/AgCl), 20.3 dB (planar) [30].
- **Necklace dry electrodes** (Interspeech 2024): 92.7% on 11 voiced words, multi-speaker [5].
- **ETH neckband dry electrodes:** textile-based, fully dry, 20.5 mW, 14 differential channels [13].
- **QuietSync foam dry electrodes (Microsoft):** "3D-printed molds, castable urethane foam
  [Smooth-On FlexFoam-It 6], and conductive medical electrode ink" (Creative Materials 113-09);
  stated limitation "ink wear over time, which can be addressed by reapplying and curing the ink"
  [10]. 12 commands at 94.2% with these plus an IMU [10].
- **Textile towel electrodes with graphene/PEDOT:PSS coating** (Cambridge): in the EMG band
  (10–150 Hz) "the impedance of the textile electrodes is comparable to that of wet electrodes"; at
  1–10 Hz they "exhibit slightly higher capacitance, likely due to air gaps" [9]. Because they are
  non-adhesive they suffer "variability in contact pressure", "micro-slippage and triboelectric
  effects" and "capacitive coupling instability" below 20 Hz; removing the 20–450 Hz band-pass drops
  accuracy from 96% to **76.5%** [9].

### 2.3 Textile electrodes — quantified and launderable

Three commercial Shieldex metallised fabrics on a skin phantom at 50 Hz under a fixed **225 g**
load: silver-plated PA6/elastane knit **199 Ω** (face) / **204 Ω** (reverse); Ag + conductive-silicone
warp knit **180 Ω** (reverse) but **8.90 kΩ** (silicone face); woven Ag/Cu/Sn PA66 **928 Ω**; versus
a commercial Ag/AgCl electrode **313 Ω** — the silicone face was ~50× worse than its reverse [40].
After **20 standard laundering cycles**, the woven Ag/Cu/Sn fabric stayed at ~**0.03 Ω**, the
silver-plated knit rose from **0.31 ± 0.05 Ω to 0.52 ± 0.08 Ω** (face) and **0.34 ± 0.05 Ω to
0.65 ± 0.08 Ω** (reverse) [40]. On humans (n = 9, Fp1), a textile dry electrode agreed with
simultaneous Ag/AgCl at grand-mean **r = 0.92**, **CCC = 0.96**, RMS bias **−7%**; multipin EEG work
puts the optimal normal force at **2–3 N** [40]. Launderable silver-knit fabric is therefore a
credible choice for a collar or headband, provided the conductive face (not the silicone) touches
skin and the garment is pressed on with 2–3 N.

### 2.4 Hydrogel / gel-free "biopotential" electrodes

A crosslinker-free PEDOT:PSS-doped hydrogel (PPHG, 1 mm × 1.7 cm) was benchmarked against Ambu
BlueSensor L Ag/AgCl in **39 participants**. Ag/AgCl showed "the highest overall contact impedance
and the most pronounced signal instability at 10 Hz and in the 50/60 Hz range", while PPHG stayed
lower and converged by ≈10 Hz; PPHG gave coefficient of variation **<10%** across 0.5–100 Hz versus
**>50–60%** for Ag/AgCl at low frequencies; reuse across **five sessions** did not degrade it; and
it gave a **2.2-fold** improvement in inter-lead classification accuracy [31]. The paper reports
these as relative values, so absolute kΩ and multi-day water retention are **unverified** [31].

### 2.5 Ultrathin epidermal / "electronic tattoo" electrodes

**Graphene e-tattoo (GET, Akinwande group).** Total thickness **463 ± 30 nm**, optical transmittance
**84–88%** (400–800 nm), stretchability >40%, sheet resistance **1994.33 ± 264 Ω/sq**, mechanical
stiffness **1.48 N/m** versus epidermis **3.9 N/m**; full conformability is predicted below **510 nm**
[33]. GET–skin impedance was "comparable with the gel electrode–skin impedance" even though the GET
area (**~0.245 cm²**) was >10× smaller than the gel electrode (**~2.6 cm²**); a 13 µm
graphene/polyimide electrode was **>1 order of magnitude higher**. Bare GET stayed conformal **>4 h**
(first delamination at **4 h 23 min**); with <1 µm liquid bandage, no delamination up to **52 h**
with low impedance, and at **96 h** a crack raised impedance by ~1 order of magnitude [33]. A later
300-nm GET did **15 h** of ambulatory palm electrodermal monitoring and, "with the protection of
liquid bandage, GET can stay on the skin for up to three days"; no adhesive is needed (van der Waals)
[34].

**Gold nanomesh (Someya group).** Electrospun PVA nanofibres (diameters generally 300–900 nm) coated
with **100-nm gold**, total thickness "a few micrometers", initial resistance **10–100 Ω**; it
survived **>1440 min** of continuous water flow with only a **1.02-fold** resistance rise, whereas
PVA-only lost conductivity within **105 s**. At 6 h only **2/6** PVA-only electrodes stayed below
1 kΩ versus **6/6** blend electrodes, and on the palm after 4 h **3/8** versus **8/8** (all <50 Ω).
The 2017 work reported a **one-week** skin patch test in which inflammation was "significantly
suppressed", with successful EMG recording [35][36].

**Rogers-style epidermal electronics.** Thickness **~30 µm**, effective elastic moduli **<150 kPa**,
bending stiffness **<1 nN·m**, areal mass density **<3.8 mg/cm²**; filamentary-serpentine devices
reach ~140 kPa and ~0.3 nN·m, with interfacial contact pressure ~**10–12.5 kPa** (below the ~20 kPa
skin-sensitivity threshold), van der Waals adhesion, and no resistance degradation after **1000
stretch cycles at 30% strain**. It recorded throat EMG during silent word articulation with **>90%**
classification accuracy [37].

**Liu et al. 2020 (Soochow / NUS) — the e-tattoo actually validated on silent speech.** Cu/polyimide
filamentary-serpentine mesh: "Cu (400 nm in thickness)" electrodes "9 mm in diameter with FS meshes
of 0.1 mm in width and 0.2 mm in radius of curvature", encapsulated in PI (2.4 µm layers), **total
patch thickness < 10 µm**, "peeling strength of larger than 1 N cm−1", surviving 20% strain with no
cracks. It is transferred onto a "sterile wound dressing (polyurethane)" providing "great
adhesiveness … without falling off" [8]. Demonstrated 3 channels (ABD/BUC/ZYG) on silent 5- and
6-word sets at 89.6 ± 0.6% and 92.7 ± 0.5% [8]. Wear duration not reported — **unverified**.

### 2.6 Skin-coloured and transparent electrodes

- **PGIN (PEDOT:PSS/graphene-oxide interpenetrating network):** ~**115 nm** thick, conductivity
  **2060 S cm⁻¹ at 88% transparency**, **110%** stretchability, **3.5×** lower interfacial impedance
  than a commercial electrode, and **92%** silent-speech recognition accuracy from facial EMG
  (6 channels, 8 volunteers) [43].
- **Liquid-metal-printed ITO:** bare ITO >90% visible transmittance; with a **14 nm Au** coating
  transparency stayed **>50%**, impedance dropped a further **50%** to parity with Ag/AgCl, and ECG
  SNR reached **31 dB** (+50% vs bare ITO, +5% vs gel) [42].
- A specifically **skin-tone/colour-matched** biopotential electrode with published impedance is
  **unverified** in this search. The demonstrated concealment strategy is still *placement*, not
  optical camouflage.

### 2.7 Adhesion, sweat and irritation for e-tattoos

GET adheres by van der Waals forces alone, is removed with ordinary adhesive tape, and is breathable
because of its open mesh [33]. Nanomesh uses water-sprayed, partially dissolving PVA as a transient
adhesive and is gas-permeable; one-week patch test showed suppressed inflammation [35]. Kirigami
PEDOT:PSS/PVA/AgNW/PU electrodes maintained signal after water rinsing, ultrasonic cleaning, and
under sweat/wet/movement conditions [41]. Long-duration reports: **52 h** (GET + liquid bandage,
low impedance) [33] and **3 days** (later GET) [34]; the **96-h GET crack** is the clearest failure
datum [33]. Dedicated quantitative multi-day **hydrocolloid/conductive-adhesive** fixation studies
for EMG are **unverified**.

### 2.8 PEDOT:PSS and conductive-polymer coatings — the practical lever on impedance

- PEDOT:PSS on a porous PDMS sponge: **12.2 kΩ at 10 Hz with gel** vs 277.5 kΩ dry; **5.25×** below
  a planar printed PEDOT:PSS electrode and **6.7×** below Ag/AgCl [30].
- Kirigami PEDOT:PSS/PVA/AgNW/PU: **≈59.76 kΩ at 10 Hz** and **≈27.41 kΩ at 100 Hz**, sheet
  resistance **3.9 Ω/sq**, >100% stretch, stable over 1000 cycles at 50%. Pristine PEDOT:PSS is
  ≈**80 kΩ at 10 Hz / 32 kΩ at 100 Hz**; the authors call **6–10 kΩ** the "ideal" electrode–skin
  range [41].
- PGIN reached **2060 S cm⁻¹** with 3.5× lower impedance [43].

The takeaway for a dry face/neck build: coating a soft, high-surface-area substrate with
PEDOT:PSS (or using a conductive hydrogel layer) is what brings dry impedance into the same order as
wet, and it is the single most cited trick in this literature [30][41][43].

### 2.9 Bio-signal AFEs for the custom PCB (miniaturisation)

- **Intan RHD2000:** RHD2216 16-ch bipolar / RHD2132 32-ch unipolar / RHD2164 64-ch, 16-bit ADC,
  "up to 30 kSamples/s per channel", "Low noise floor: 2.4 μV rms typical", on-chip impedance
  measurement. Headstages: 16-ch **23 × 13 mm / 0.79 g**; 32-ch **24 × 15 mm / 0.94 g**;
  64-ch **21 × 14 mm / 1.30 g** [55].
- **TI ADS1299:** 4-, 6- or 8-channel, 24-bit, simultaneous sampling; "Input-Referred Noise: 1 μVPP
  (70-Hz BW)"; "250 SPS to 16 kSPS"; CMRR –110 dB; programmable gain 1–24; input bias current
  300 pA; TQFP-64 body **10.00 mm × 10.00 mm** [56]. SilentWear uses two **ADS1298** parts [13].
- **BioGAP-Ultra (open source, GAP9 + nRF5340):** 16-ch ExG, mainboard **2.6 × 3.0 × 1.3 cm³**;
  up to 15.6 GOPs DSP and 32.2 GMACs at 370 MHz; streaming power **32.8 mW** (EEG-PPG headband),
  **26.7 mW** (EMG sleeve), **9.3 mW** (ECG-PPG chestband); EMG+ACC reach-and-grasp classification
  79.9% ± 5.7% at 23.6 mW [57].
- **MyoWare 2.0:** single-channel, **37.57 mm × 35.90 mm** board, input bias current 250 pA
  (max 1 nA), 3.3–5 V [69].

This matters for concealment: a behind-ear pod can be built from one ADS1299 (up to 8 channels,
10×10 mm) or the 16-ch 23×13 mm Intan headstage, which fits a hearing-aid-sized enclosure far more
easily than a face-spanning array.

## 3. Concealed form factors

### 3.1 Around-ear and behind-ear (cEEGrid style)

The cEEGrid is the best-evidenced concealed bio-electrode form factor: "ten flex-printed
Ag/AgCl electrodes" in a C-shape around the ear, fixed with a double-sided adhesive and gel, read
out by a wireless 24-channel head-mounted amplifier (SMARTING), 24-bit, 500 Hz [7][46]. Impedances
"ranged from 0.6 to 83.6 kOhm with a median value of 13.5 kOhm"; decoder performance was "unaffected
by variability in channel impedances" [7]. Demonstrated on 18 participants for target-speaker
detection: one cEEGrid (8 channels) **64.88%**, two cEEGrids (16 channels) **69.33%**, versus
**84.78%** for an 84-channel cap and **82.78%** for the 16 cap channels nearest the ears [7].

**Wear-time evidence for cEEGrid is stronger than for any other concealed array.** In the original
validation, ten participants "wore two cEEGrid systems for at least seven hours"; P300 test–retest
reliability was r ≥ .74 and a classifier trained in the morning retained "> 70%" accuracy
six-to-seven hours later [45]. At home for sleep staging, cEEGrid plus an mBrainTrain amplifier gave
M = 7.48 h per night with κ = 0.67 [48]. A hearing-device integration (17 participants) used
"10 electrodes placed around the ear (cEEGrid) and 3 electrodes spread out in the concha" and found
"signal quality is better for around-the-ear electrodes than for in-concha electrodes" [47]. In-ear
(earbud) dry electrodes can record "a single bipolar EEG channel using a cross-ear electrode
configuration"; versus a 64-electrode wet cap the RMS values were comparable and in ~80% of cases
cross-correlation with scalp EEG was significant, but alpha amplitudes were smaller and SNR
"slightly lower" [49].

Crucially, [7] is **EEG (brain signals), not EMG.** It proves the *form factor* (concealed around-ear
array, hearing-aid-adjacent readout) works for neural signals, and that around-ear channels carry
speech-relevant information — but the authors' framing is "concealed ear-EEG … potential to be used
in the brain-computer interface steering of hearing aids" [7].

**AESSI closes most of that gap and is the strongest concealed silent-speech result found** [12].
AESSI uses "bilateral cEEGrid around-ear arrays comprising 20 electrodes in total"; channels 18 and
20 "were consistently excluded from recording because of high contact impedance, leaving 18
electrophysiological input channels", acquired at 1 kHz with a TMSi SAGA 32+. It collected **44
sessions from 24 participants**, each session 10 blocks × 25 Mandarin sentences (250 trials), and
decodes a **fixed 25-sentence set** from a 3-second silent-articulation window. Results:
**92.24% mean cross-day accuracy without test-day calibration** (chance 4.00%), exceeding "the best
adapted baseline by 50.57 percentage points"; five participants returned "at least 21 days after
each participant's last recording" and, with frozen models and no test-day adaptation, scored
**245/250 = 98.00%** online; "median preprocessing and inference time in CPU replay was 31.70 ms"
[12]. Caveats stated by the authors: the input is "around-ear mixed electrophysiology" and the
study "does not separately quantify the contributions of different physiological sources"
(facial/jaw EMG vs EEG); it is closed-set sentence classification, not open vocabulary; and before
each session "all 18 channels had impedances below 20 kΩ" [12]. The paper also records that
Inoue et al.'s around-ear 64-word system required "640 labeled trials on the test day" for
fine-tuning [12]. That system reports **56.6% (healthy participants) and 47.3% (locked-in
individual)** on 64-word classification from around-ear EEG, with online top-1/top-5 of
**47.2%/76.0%** (healthy) and **26.5%/49.1%** (LIS); fine-tuning added "22 percentage points" [51].
Ear-EEG speech *imagery* on 4 commands was weaker still: **38.2%** versus **43.1%** for scalp EEG
(chance 20%) [50].

Two systems do demonstrate around-ear/on-ear **EMG** for silent commands:

- **Headphone earmuff textile EMG** (Cambridge): four graphene/PEDOT:PSS towel electrodes inside
  the earmuff + ESP32-S3, sampled at 1 kHz, 20–450 Hz band-pass, 3-second windows. Dataset: 10
  control words, 4 subjects, each word repeated 100 times (balanced), 80/20 split. Result:
  **96%** overall with a 1D SE-ResNet that uses squeeze-and-excitation to down-weight poorly
  coupled channels; **single-channel accuracy drops by nearly 40%** and removing the filter drops
  it to 76.5% [9].
- **QuietSync** (Microsoft): dry foam ExG electrodes on "headphones, glasses (nose and behind the
  ear), and face (for VR)", plus an IMU at the lower ear. 9 participants, 12 commands, **94.2%**
  accuracy; mean latency 1.35 s; fine-tunable with "only 5 samples" per user [10]. (The
  introduction claims "over 95% accuracy" while the abstract and conclusion say 94.2% — quote
  94.2%.)

### 3.2 Under-chin / jawline

- AlterEgo's top-ranked regions (mental, laryngeal, hyoid) and its "4 electrodes along one jaw"
  follow-up [1][2].
- Gaddy's sites 2 and 3 ("left corner of chin", "below chin back 3 cm") and site 4 (throat) [3].
- Liu et al.'s ABD (anterior belly of digastric) patch electrode under the lower jaw, which alone
  reached 80.9 ± 0.9% on 5 silent action words [8].
- The **reference and bias electrodes in both AlterEgo and Gaddy sit below/behind the ear**
  [2][3] — an under-chin array plus a behind-ear pod is a natural two-piece design.

### 3.3 Glasses

QuietSync's glasses configuration places ExG electrodes at "the nose and behind the ear" and
reports it as one of four form factors (headphones, earphones, glasses, VR/XR) covered by the same
94.2% system [10]. This is the only glasses-integrated silent-speech **EMG** result fetched here.
(Note: EchoSpeech, cited by [9] and [10], is acoustic sensing on eyewear, not electrodes —
unverified here.)

**JINS MEME** is the commercial precedent for glasses-integrated biopotentials: it measures
"horizontal and vertical EOG … with three metal dry electrodes placed near nasion and both sides of
rhinion, of which positions correspond to the bridge and nose pads of eyewear", plus a six-axis
motion sensor and Bluetooth [52]. That is EOG, not EMG, but it proves the nose-pad and temple real
estate can host dry electrodes in a normal-looking frame. The Wispr AI patent claims glasses
variants with EMG "near the bottom of the lens frames in contact with a cheek", "along the temple
arms", and "on the nose bridge" [6].

### 3.4 Neck, collar, necklace

- Wu et al. necklace, dry electrodes around the neck: 92.7% on 11 **voiced** words, multi-speaker,
  with an ablation showing >2 electrodes are needed [5].
- ETH Zürich neckband (SilentWear): 14 dry differential channels around the neck, textile-based,
  fully dry, 20.5 mW; silent cross-validated **77.5 ± 6.6%**, leave-one-session-out **59.3 ± 2.2%**
  [13].
- A collar/scarf/neckband hides the array completely and needs no face adhesive — the trade-off is
  the large cross-session drop [11].
- **SpeeChin** is a smart necklace with an infrared camera under the chin — **not EMG** — yet it is
  the strongest under-chin concealed-sensor result: 20 participants, **90.5% on 54 English
  commands** and **91.6% on 44 Chinese commands** cross-session [53]. It shows the under-chin site is
  valuable enough that a non-EMG modality targets it too, and that a collar-concealed sensor can
  carry a vocabulary two orders of magnitude larger than AlterEgo's.

### 3.5 Masks and other concealment

Liu et al.'s patch is laminated on the jaw/face and hidden by being ultrathin [8]; cEEGrid hidden
behind the ear and under hair [7]; earmuff textile electrodes hidden inside headphones the owner is
already wearing [9].

- **Hand-worn, lip-adjacent EMG:** a soft active EMG interface uses a fingertip electrode
  "positioned near the lips" (liquid-metal interconnects, transparent flexible printed electrodes,
  elastomer encapsulation) and reports **97.2 ± 1.3% mean accuracy across three subjects on a
  30-word vocabulary** [54]. Concealment here is by hand posture, not by the face — a different
  interaction model, but it shows that a 30-word silent vocabulary is reachable without any face
  electrode.
- **Beard-hidden, high-collar, and EMG smart-mask** form factors: **no primary source verified** in
  this search. Treat as unverified.

### 3.6 Relevant patent

Wispr AI's US20240221738A1 (priority 2023-01-04, assignee Wispr AI Inc., inventors Garg, Kothari,
Leonardo; published 2024-07-04, granted as US12482449B2 on 2025-11-25) describes silent speech in a
user-interaction system and claims an ear-hook with a "preauricular downstem … in front of the
tragus" and a "postauricular downstem … behind the ear and adjacent the mastoid process", with EMG
sensors and a postauricular reference [6]. I read the patent front matter and a description snippet
myself; the detailed claim text was read during this research, so treat the exact claim wording as
**partially verified**. For context, the muscle-interface patent lineage is Ctrl Labs / Meta
**US 10,528,135 B2**, which claims "a plurality of muscle activity sensors to be worn on an arm of a
user" (forearm, not face) [58]. **No granted AlterEgo-assigned patent was located — unverified.**

## 4. Daily-wear practicalities: drift and recalibration

### 4.1 How much the signal changes across sessions

- Forearm flexors (23 adults): averaged normalised EMG had an **intra-session ICC of 0.90**, but when
  electrodes were **removed and replaced inter-day**, reliability was "poor, ICC < 0.50", with
  normalised standard error of measurement **23–45%** at low grip forces [16].
- HDsEMG arrays on lower-limb muscles (12 participants, 3D-scanned ground truth): at **10 cm**
  electrode distance the combined absolute percent difference was **14.4%** (mean frequency),
  **16.0%** (median frequency), **14.9%** (peak frequency) and **56.8%** for total power. At the
  **same location, reapplication-only** median differences were "consistently <30% for all muscles
  and activities" except one condition at **31.4%**; mean/median frequency were smallest
  (**<5.5%**), total power greatest (**>20%**). An electrode shift of just **1 cm** made **12–21%**
  of feature differences exceed the reapplication-only difference [17]. Limb, not face, but it cleanly
  separates *shift* error from *re-application* error.
- Dry gold epidermal electrodes (4 days, upper limb): largest individual impedance change over four
  days was **11 MΩ at 53 Hz and 12 MΩ at 151 Hz**; inter-subject variability 3.3 MΩ / 1.4 MΩ;
  **ICC 0.62 (95% CI 0.0–0.97) at 53 Hz** and **0.69 (0.0–0.98) at 151 Hz** [15].
- Silent-speech-specific repositioning: Maier-Hein et al. (7 channels, 10 digits, 3 subjects) went
  from **97.3% with the same electrode positions to 76.2% after repositioning, recovering to 87.1%
  after adaptation** [67]. Wand et al. compensated array-position shifts by linear interpolation for
  **14.3% relative WER improvement on development and 12.9% relative on evaluation** versus
  classical session adaptation [68].

### 4.2 Cross-session silent-speech evidence

- **Around-ear (AESSI):** **92.24%** cross-day with **no test-day calibration**, and **98.00%**
  online after **≥21 days** with frozen models [12]. This is the least recalibration-hungry result
  found — but it is a **closed 25-sentence set** and "mixed electrophysiology" (EEG+EMG mix), so it
  is not direct evidence for a face-only EMG build.
- **Neckband (SilentWear):** cross-validated 84.8 ± 4.6% (vocalized) / 77.5 ± 6.6% (silent), falling
  to **71.1 ± 8.3% / 59.3 ± 2.2%** leave-one-session-out with repositioning; fine-tuning with
  **<10 minutes** of new data recovered **>10% accuracy** [13].
- **Face+neck sEMG:** Gaddy & Klein reattached electrodes each session and handled the shift with a
  **32-dimensional session embedding** appended to every time step [3]. Segmented lower-face+neck
  sEMG (8 channels, 27 subjects, 50-sentence closed corpus): zero-shot (no target calibration)
  **49.3% CER**; **3 minutes** of target calibration reached **20.5% CER / 31.7% WER**, versus
  **21.7% CER / 31.9% WER** for a full ~**13-minute** pool (not significantly different), while
  **1 minute** was significantly worse at **25.4% CER** (p=0.003) [19].
- **Session-independent facial EMG (EMG-UKA, 48 sessions):** baseline target-session WER **18.8%**
  (development) / **29.9%** (held-out evaluation); unsupervised domain-adversarial adaptation cut it
  to **15.6%** (**17.0% relative**) / **28.5%** (**4.7% relative**) [18]. The small held-out gain is
  the caution: the method "varies drastically" by session combination [18].
- AlterEgo collected its ~31-hour corpus "in different sessions to be able to regularize the
  recognition model for session independence" [2]; its per-day protocol is not reported in the paper
  read here — **cross-day protocol unverified**.

### 4.3 How much recalibration data is needed

- **3 minutes** of labelled target data was statistically indistinguishable from the full ~13-minute
  calibration pool for face+neck sEMG sentence decoding; **1 minute** was not [19].
- **<10 minutes** recovered >10% accuracy after neckband repositioning [13].
- Cross-user myoelectric encoders (77 subjects): with only **4–5 repetitions** of each gesture, full
  fine-tuning was most accurate at every budget, and a gradient-free prototypical rule recovered
  **52–78%** of its benefit, making adaptation feasible "at donning time" [24].
- Around-ear 64-word decoding (Inoue et al.): healthy participants completed **640 labelled trials on
  the test day** (10 rounds × 64 words) for fine-tuning before online use [12].
- Unsupervised domain-adversarial self-calibration for multi-day EMG gesture recognition exists
  (SCADANN: 3 sessions over 14 days, users self-place the armband), but its per-condition numbers
  could not be retrieved — **unverified** [25].

**Practical reading for a one-user build:** budget a 1–3 minute re-calibration each session (or
~10 minutes to recover most of the loss after a big shift), and store a per-session embedding /
domain tag. Zero-calibration across days is demonstrated for around-ear closed-set decoding [12],
not for face-only open-vocabulary sEMG.

### 4.4 Skin safety and wear limits

- FDA/ISO 10993-1 contact-duration categories: **Limited ≤24 h; Prolonged >24 h to 30 days;
  Long-term/Permanent >30 days**. For intact-skin surface devices the required endpoints are
  **cytotoxicity, sensitisation, and irritation/intracutaneous reactivity** [14].
- Ag/AgCl gel electrodes "are limited to short-term use due to skin irritation and signal
  degradation as the gel dries out" [15].
- **Acrylate allergy is common enough to plan for.** Of 204 diabetes-device users, **16.2%** were
  patch-test positive to device allergens, rising to **28.1%** among those with skin rash vs
  **1.1%** without; top allergens were isobornyl acrylate **10.3%**, N,N-dimethylacrylamide **4.9%**,
  2-hydroxyethyl acrylate **3.4%**, dicyclohexylmethane-4,4'-diisocyanate **2.9%** [20].
- **Nickel** is a recognised contact allergen [28]; nickel- and Ag/AgCl-specific allergy prevalence
  in electrode users is **unverified**.
- Dry gold electrodes on silicone tape were worn "**continuously over four days**" with
  "**no perceived irritation**" and no significant signal-quality trend, removed for showers [15].
  Longer than 4 days is **unverified**.
- ANSI/AAMI EC12:2000/(R)2020 "Disposable ECG electrodes" exists as the US standard for disposable
  ECG electrodes; a specific maximum wear time in EC12 is **unverified** [26].

### 4.5 Adhesives for multi-day wear

- MARSI (medical adhesive-related skin injury) is erythema/skin alteration "that persist[s] for
  **30 minutes or more** after adhesive removal"; the 2024 consensus gave **20 statements** [21].
- ICU multicentre study (108 patients): MARSI prevalence **25.9%**, most commonly maceration
  **39.4%** and irritant contact dermatitis **24.2%**; risk rose with the number of adhesives
  (p=0.001) [22].
- Spinal-surgery cohort (140 patients): **45%** developed MARSI within 10 days; the **acrylate**
  dressing group had cumulative incidence **56.8%** vs **31.8%** for **silicone** (p=0.003), a
  **2.55×** higher risk [23].
- **Silicone** "Kind Removal" tape was chosen for the 4-day dry-electrode study because it is
  "gentle on the skin and can be reattached **more than 20 times**" [15]. Hydrocolloid wear
  durations in EMG use are **unverified**.

**Implication:** use silicone adhesives, not acrylic, for anything reapplied daily; expect MARSI
rates of 25–45% if you keep adhesives on for days at a time [21][22][23].

### 4.6 Sweat and impedance over hours

- Dry-electrode impedance "**decreased for the first two hours before stabilizing for 2–7 h
  post-application**"; over the last five hours it averaged **252 kΩ at 53 Hz and 139 kΩ at
  151 Hz** [15].
- Dry electrodes generally sit at "high kΩ–high MΩ", wet at "low kΩ–low MΩ"; **>100 kΩ at 53 Hz**
  was still considered acceptable for sEMG [15].
- Signal quality was stable despite that: over four days **SNR 50.5 ± 6.2 dB, SMR 8.7 ± 8.7 dB**,
  no trend, average coefficient of variation **<10%** [15]. A direct sweat-driven impedance curve
  over hours is **unverified** (explicitly beyond that study's scope) [15].

### 4.7 Cleaning, reusability and donning

- Reusable dry sensors (Delsys Trigno): cleaned "with isopropyl alcohol or a mild detergent solution
  … **before and after each use**", never fully submersed; sessions "as long as **8 hours**"; skin
  prep is hair removal, alcohol wipe, tape debridement and dilute ionic soap [27].
- **Donning/doffing times were not found in any primary source — unverified.** AESSI verified all
  18 channels below 20 kΩ before each session, implying a non-trivial setup step but reporting no
  time [12].

## 5. Candidate concealed layouts (ranked by invisibility vs expected accuracy)

Ranked most invisible first. "Expected accuracy" is anchored to the closest demonstrated system,
not to marketing. Layouts A and B are the two hidden, non-face options with published silent-speech
numbers; C is the face-based option with the best concealable accuracy; D is the adhesive-free
fallback.

### Layout A — Headphone earmuff textile EMG array (most invisible)
- **Sites:** 4 textile electrodes inside the earmuff, around/over the ear (no adhesive, no face
  contact).
- **Electrode type:** graphene/PEDOT:PSS-coated "towel" textile, dry, breathable [9].
- **Electronics:** ESP32-S3 + 4 EMG readout circuits inside the earmuff housing, LiPo, Wi-Fi to
  phone/PC [9].
- **Expected accuracy:** **96% on 10 silent control words** demonstrated with 4 subjects [9].
  Single-channel drops ~40%, so 4 channels with per-channel attention is the point [9].
- **Invisibility:** total — it is a pair of headphones. **Risk:** no cross-session or
  open-vocabulary evidence; the same group's own filtering ablation shows how fragile dry
  non-adhesive contact is [9].

### Layout B — Bilateral around-ear cEEGrid (hidden by hair / hearing-aid form; best cross-day evidence)
- **Sites:** C-shaped flex-printed array around each ear (cEEGrid: 10 electrodes per ear, 20 total,
  18 usable channels after excluding high-impedance channels) [7][12].
- **Electrode type:** flex-printed Ag/AgCl with electrolyte gel + double-sided adhesive per
  application [7]; the 4-day dry-epidermal electrode study suggests a dry replacement is plausible
  but unproven around the ear [15].
- **Electronics:** wireless 24-channel head-mounted amplifier (TMSi SAGA 32+ in AESSI, 1 kHz) [12];
  a behind-ear or behind-head pod of the kind already used by cEEGrid studies [7].
- **Expected accuracy:** **92.24% cross-day with no test-day calibration** on a fixed 25-sentence
  Mandarin set (chance 4.00%), and **98.00%** online after **≥21 days** with frozen models (245/250);
  median preprocessing+inference 31.70 ms [12]. This is the strongest concealment/robustness result
  found. **Caveat:** AESSI's input is "around-ear mixed electrophysiology" and the authors "do not
  separately quantify the contributions of different physiological sources" [12] — it is not proven
  face-only EMG, and the task is 25-way sentence classification, not open vocabulary.
- **Invisibility:** very high — behind/around the ear, hair and a hearing-aid-style pod cover it;
  the mouth is unobstructed [12].
- **Risk:** requires gel + fresh adhesive per session [7]; 2 of 20 channels were dead on impedance
  grounds in AESSI [12]; independent replication of the 92%/98% figures is not yet available.

### Layout C — Under-chin + jawline e-tattoo patch with a behind-ear pod (best accuracy-per-visibility)
- **Sites:** submental/ABD under the chin, plus jawline/submental digastric and hyoid channels;
  avoid infra-orbital and mid-cheek sites (lowest-ranked [2], least useful [3]). Optional 1 visible
  cheek channel as a control.
- **Electrode type:** ultrathin (<10 µm) Cu/polyimide serpentine e-tattoo on a wound-dressing
  backing (peel strength >1 N/cm, 20% strain tolerance) [8]; or, simpler to prototype, dry
  Ag/AgCl behind/under the jaw with a low-impedance conductive-polymer coating.
- **Electronics:** thin flex interconnect along the jaw to a behind-ear pod (the reference/bias
  position already used by AlterEgo and Gaddy [2][3]).
- **Expected accuracy:** the under-chin ABD channel alone reached **80.9 ± 0.9%** on 5 silent words,
  and a 3-channel ABD+BUC+ZYG patch reached **89.6 ± 0.6% (5 words)** and **92.7 ± 0.5% (6 words)**
  [8] — single tester. For open vocabulary, the realistic reference is Gaddy's 8-channel result:
  **68% WER automatic, 74.8% human** [3].
- **Invisibility:** high from the front (chin/jaw), lower in profile; the behind-ear pod is
  hearing-aid-normal.
- **Risk:** e-tattoo wear duration unverified [8]; dry submental channels will sag across sessions
  like the neckband's [11].

### Layout D — Neckband / collar (dry, no adhesive, moderate concealment)
- **Sites:** 14 differential dry electrodes around the neck (SilentWear layout) [11][13] or the
  smaller necklace montage [5].
- **Electrode type:** SoftPulse dry electrodes (Datwyler) [11], textile-based, fully dry [13].
- **Electronics:** BioGAP-Ultra / two ADS1298 AFEs, nRF53 BLE; 20.5 mW total, >27 h continuous,
  2.47 ms on-device inference [11][13].
- **Expected accuracy:** **77.5 ± 6.6%** silent (cross-validated) and **59.3 ± 2.2%** silent
  leave-one-session-out after repositioning; **84.8 ± 4.6%** / **71.1 ± 8.3%** for vocalized; <10
  minutes of new data recovered >10% [13]. Voiced 11-word necklace variant: 92.7% [5].
- **Invisibility:** hidden by a collar, scarf, or hoodie; no face contact, no adhesive.
- **Risk:** largest cross-session degradation of the adhesive-free options, and silent accuracy is
  well below the face- and ear-based systems [13].

### Reference points not recommended as the primary layout
- **Full AlterEgo-style face + neck array:** 92.01% average on 10 digits, silent [2] — the best
  closed-vocabulary silent result — but visible tentacle electrodes around the mouth/jaw.
- **QuietSync glasses/headphones/VR dry ExG + IMU:** 94.2% on 12 commands, 9 users, 1.35 s latency
  [10]. Excellent form-factor coverage; only 12 commands and a 5-sample per-user fine-tune [10].

## Sources

1. MIT News, "Computer system transcribes words users 'speak silently'", 2018.
   https://news.mit.edu/2018/computer-system-transcribes-words-users-speak-silently-0404
2. A. Kapur, S. Kapur, P. Maes, "AlterEgo: A Personalized Wearable Silent Speech Interface",
   23rd International Conference on Intelligent User Interfaces (IUI 2018), pp. 43–53.
   https://dam-prod.media.mit.edu/x/2018/03/23/p43-kapur_BRjFwE6.pdf
   (abstract page: https://www.media.mit.edu/publications/alterego-IUI/)
3. D. Gaddy, D. Klein, "Digital Voicing of Silent Speech", EMNLP 2020, pp. 5521–5530.
   https://aclanthology.org/2020.emnlp-main.445.pdf
4. A. Kapur, U. Sarawgi, E. Wadkins, M. Wu, N. Hollenstein, P. Maes, "Non-Invasive Silent Speech
   Recognition in Multiple Sclerosis with Dysphonia", Proceedings of Machine Learning Research
   116:25–38 (ML4H at NeurIPS 2019), 2020.
   https://andymatuschak.org/files/papers/Kapur%20et%20al%20-%202020%20-%20Non-Invasive%20Silent%20Speech%20Recognition%20in%20Multiple%20Sclerosis%20with%20Dysphonia.pdf
   (abstract page: https://www.media.mit.edu/publications/non-invasive-silent-speech-recognition-in-multiple-sclerosis-with-dysphonia/)
5. P. Wu et al., "Towards EMG-to-Speech with Necklace Form Factor", Interspeech 2024.
   https://www.isca-archive.org/interspeech_2024/wu24k_interspeech.html
6. Wispr AI Inc., "Systems and methods for using silent speech in a user interaction system",
   US20240221738A1 (granted as US12482449B2), priority 2023-01-04, published 2024-07-04.
   https://patents.google.com/patent/US20240221738A1/en
7. B. Mirkovic, M. G. Bleichner, M. De Vos, S. Debener, "Target Speaker Detection with Concealed
   EEG Around the Ear", Frontiers in Neuroscience 10:349, 2016.
   https://pmc.ncbi.nlm.nih.gov/articles/PMC4961688/
8. H. Liu et al., "An epidermal sEMG tattoo-like patch as a new human–machine interface for
   patients with loss of voice", Microsystems & Nanoengineering 6:16, 2020.
   https://pmc.ncbi.nlm.nih.gov/articles/PMC8433406/
9. C. Tang et al., "Wireless Silent Speech Interface Using Multi-Channel Textile EMG Sensors
   Integrated into Headphones", arXiv:2504.13921, 2025.
   https://arxiv.org/abs/2504.13921
10. T. Srivastava, R. M. Winters, Y.-T. Wang, T. M. Gable, T. LaScala, I. J. Tashev, "Whispering
    Wearables: Multimodal Approach to Silent Speech Recognition with Head-Worn Devices" (QuietSync),
    ICMI '24, 2024.
    https://www.microsoft.com/en-us/research/wp-content/uploads/2024/11/Microsoft_Silent_Speech_Recognition_ICMI_2024-672d5717ed40e.pdf
11. F. Meier, G. Spacone, S. Frey, L. Benini, A. Cossettini, "A Parallel Ultra-Low Power Silent
    Speech Interface based on a Wearable, Fully-dry EMG Neckband", ETH Zürich PULP Platform,
    presented 21.10.2025.
    https://pulp-platform.org/docs/sensors2025/GiusySpacone_sensors_PULP.pdf
12. X. Xu, M. Dong, Y. Yan, C. Wang, Y. Jiao, J. Chen, "AESSI: An Around-Ear Silent Speech Interface
    for Cross-Day Online Reuse without Test-Day Calibration", arXiv:2609.21436, 2026.
    https://arxiv.org/abs/2609.21436
13. G. Spacone, S. Frey, G. Pollo, A. Burrello, D. Jahier Pagliari, V. Kartsch, A. Cossettini,
    L. Benini, "SilentWear: an Ultra-Low Power Wearable System for EMG-based Silent Speech
    Recognition", arXiv:2603.02847v2, 2026. https://arxiv.org/abs/2603.02847
14. U.S. FDA, "Biocompatibility Evaluation Endpoints by Contact Duration Periods", content current
    09/07/2023.
    https://www.fda.gov/medical-devices/biocompatibility-assessment-resource-center/biocompatibility-evaluation-endpoints-contact-duration-periods
15. M. Yamagami, K. M. Peters, I. Milovanovic, I. Kuang, Z. Yang, N. Lu, K. M. Steele, "Assessment
    of Dry Epidermal Electrodes for Long-Term Electromyography Measurements", Sensors 18(4):1269,
    2018. https://www.mdpi.com/1424-8220/18/4/1269
16. A. Hashemi Oskouei, M. G. Paulin, A. B. Carman, "Intra-session and inter-day reliability of
    forearm surface EMG during varying hand grip forces", Journal of Electromyography and
    Kinesiology 23(1):216–22, 2013. https://pubmed.ncbi.nlm.nih.gov/22999075/
17. F. Douglas, M. Pei, C. Kuo, "Characterizing the Effect of Electrode Shift & Sensor Reapplication
    on Common sEMG Features in Lower Limb Muscles", arXiv:2410.16262, 2024.
    https://arxiv.org/abs/2410.16262
18. M. Wand, T. Schultz, J. Schmidhuber, "Domain-Adversarial Training for Session Independent
    EMG-based Speech Recognition", Interspeech 2018, pp. 3167–3171.
    https://www.isca-archive.org/interspeech_2018/wand18_interspeech.html
19. C. Le, B. Fumagalli, Y. Esmaeili, X. Chen, T. He, N. Emami, A. Flinker, Y. Wang,
    "Multi-Subject Pretraining Enables Short-Calibration Personalization for Closed-Corpus Surface
    EMG Speech Decoding", arXiv:2609.21288, 2026. https://arxiv.org/abs/2609.21288
20. J. Ulriksdotter, M. Mowitz, T. Sukakul, M. Bruze, N. Hamnerius, C. Svedman, "Patch Testing in
    Individuals With Diabetes Using Medical Devices. Part 2—Contact Allergy to Medical Device
    Allergens and New Patch Test Recommendations", Contact Dermatitis 95(2):169–181, 2026.
    https://europepmc.org/article/MED/41936552
21. A. Barton, D. Broadhurst, J. Hitchcock, C. Lund, L. McNichol, C. R. Ratliff, J. T. Moraes,
    S. Yates, M. Gray, "Medical Adhesive-Related Skin Injury at 10 Years: An Updated Consensus",
    Journal of Wound, Ostomy and Continence Nursing 51(5S):S2–S8, 2024.
    https://europepmc.org/article/MED/39313961
22. D. F. Pio, S. D. P. P. da Silva, D. N. Cortez, J. T. Moraes, "Prevalence of skin injuries related
    to medical adhesives in Brazilian hospitals: a multicenter study", Revista Brasileira de
    Enfermagem 78(Suppl 4):e20240279, 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC12700576/
23. T. Y. Yang, J. E. Park, J. B. Kim, N. H. Lee, "Incidence and Characteristics of Medical
    Adhesive-Related Skin Injuries in Patients Following Spinal Surgery: A Prospective Observational
    Study", International Wound Journal 22(4):e70457, 2025.
    https://europepmc.org/article/MED/40240309
24. J. Odeyemi, W. J. Zhang, "Personalising a Cross-User Surface Electromyography Encoder Under a
    Small Calibration Budget", arXiv:2609.20296, 2026. https://arxiv.org/abs/2609.20296
25. U. Côté-Allard, G. Gagnon-Turcotte, A. Phinyomark, K. Glette, E. Scheme, F. Laviolette,
    B. Gosselin, "Unsupervised Domain Adversarial Self-Calibration for Electromyography-based
    Gesture Recognition", arXiv:1912.11037, 2019/2020. https://arxiv.org/abs/1912.11037
26. AAMI, "ANSI/AAMI EC12:2000/(R)2020; Disposable ECG electrodes".
    https://array.aami.org/doi/10.2345/9781570201394
27. Delsys, "General Trigno Support" (sensor cleaning, skin preparation, recording duration).
    https://delsys.com/support/general-trigno/
28. G. Genchi, A. Carocci, G. Lauria, M. S. Sinicropi, A. Catalano, "Nickel: Human Health and
    Environmental Toxicology", International Journal of Environmental Research and Public Health
    17(3):679, 2020. https://pmc.ncbi.nlm.nih.gov/articles/PMC7037090/
29. 3M, "3M™ Red Dot™ Monitoring Electrode with pre-attached lead wire" (product brochure),
    2021. https://multimedia.3m.com/mws/media/1655167O/reddot-leadwire-brochure-web.pdf
30. L.-W. Lo, G. Zhao, S. Aono et al., "Stretchable Sponge Electrodes for Long-Term and
    Motion-Artifact-Tolerant Recording of High-Quality Electrophysiologic Signals", ACS Nano
    16(8):11792–11801, 2022. https://pmc.ncbi.nlm.nih.gov/articles/PMC9413418/
31. A. Alsaafeen, N. Ziogas et al., "Systematic Benchmarking of a Noise-Tolerant Conductive
    Hydrogel Electrode for Epidermal Bioelectronics", Advanced Science 13(20):e15131, 2026.
    https://pmc.ncbi.nlm.nih.gov/articles/PMC13067809/
32. C. Lopes, P. Fiedler et al., "Me-Doped Ti–Me Intermetallic Thin Films Used for Dry
    Biopotential Electrodes: A Comparative Case Study", Sensors 21(23):8143, 2021.
    https://pmc.ncbi.nlm.nih.gov/articles/PMC8662430/
33. N. Kabiri Ameri, R. Ho, H. Jang et al., "Graphene Electronic Tattoo Sensors", ACS Nano
    11(8):7634–7641, 2017. https://www.readkong.com/page/graphene-electronic-tattoo-sensors-the-university-of-3943850
34. H. Jang, K. Sel, E. Kim et al., "Graphene e-tattoos for unobstructive ambulatory
    electrodermal activity sensing on the palm enabled by heterogeneous serpentine ribbons",
    Nature Communications 13:6604, 2022. https://pmc.ncbi.nlm.nih.gov/articles/PMC9633646/
35. A. Miyamoto, S. Lee, N. F. Cooray et al., "Inflammation-free, gas-permeable, lightweight,
    stretchable on-skin electronics with nanomeshes", Nature Nanotechnology 12:907–913, 2017.
    https://www.nature.com/articles/nnano.2017.125
36. A. Mimuro, K. Ebihara, Z. Liang et al., "Breathable nanomesh electrodes with improved water
    resistance and stretchability for skin impedance monitoring", npj Flexible Electronics 10:38,
    2026. https://www.nature.com/articles/s41528-026-00542-8
37. D.-H. Kim, N. Lu, R. Ma et al., "Epidermal Electronics", Science 333:838–843, 2011.
    https://www.osti.gov/pages/servlets/purl/1875151
38. M. Zhu et al., "Towards optimizing electrode configurations for silent speech recognition
    based on high-density surface electromyography", Journal of Neural Engineering 18(1), 2021.
    https://doi.org/10.1088/1741-2552/abca14
39. X. Tan et al., "Extracting Spatial Muscle Activation Patterns in Facial and Neck Muscles for
    Silent Speech Recognition Using High-Density sEMG", IEEE Transactions on Instrumentation and
    Measurement 72:1–13, 2023. https://doi.org/10.1109/TIM.2023.3277930
40. C. Andrés Yanzón, M. Ferre-Martínez et al., "Commercial Metallized Textiles for Dry EEG
    Electrodes: Structure, Textile-Level Durability, and Controlled Frontal Validation Against
    Ag/AgCl", Sensors 26(16):5036, 2026. https://www.mdpi.com/1424-8220/26/16/5036
41. Y. Xia, Y. Liu, B. Kim et al., "Kirigami-Structured, Low-Impedance, and Skin-Conformal
    Electronics for Long-Term Biopotential Monitoring and Human–Machine Interfaces", Advanced
    Science 11(1):2304871, 2024. https://pmc.ncbi.nlm.nih.gov/articles/PMC10767437/
42. M. Rahman, Z. Ong, A. Tiwari, J. Scheideler, "Printing flexible two-dimensional indium tin
    oxide for multifunctional transparent bioelectrodes", MRS Advances, 2025.
    https://par.nsf.gov/servlets/purl/10604925
43. "Ultrathin Bioelectrode Array with Improved Electrochemical Performance for
    Electrophysiological Sensing and Modulation" (PEDOT:PSS/graphene-oxide interpenetrating
    network), ACS Nano, 2024. https://par.nsf.gov/servlets/purl/10582528
44. S. Wu, C. Yang, X. Zhu et al., "Materials, Devices, and Systems of On-Skin Electrodes for
    Electrophysiological Monitoring and Human–Machine Interfaces", Advanced Science
    8(2):2001938, 2020. https://pmc.ncbi.nlm.nih.gov/articles/PMC7816724/
45. S. Debener, R. Emkes, M. De Vos, M. Bleichner, "Unobtrusive ambulatory EEG using a smartphone
    and flexible printed electrodes around the ear", Scientific Reports 5:16743, 2015.
    https://pubmed.ncbi.nlm.nih.gov/26572314/
46. M. G. Bleichner, S. Debener, "Concealed, Unobtrusive Ear-Centered EEG Acquisition: cEEGrids
    for Transparent EEG", Frontiers in Human Neuroscience 11:163, 2017.
    https://doi.org/10.3389/fnhum.2017.00163
47. F. Denk, M. Grzybowski, S. M. A. Ernst, B. Kollmeier, S. Debener, M. G. Bleichner,
    "Event-Related Potentials Measured From In and Around the Ear Electrodes Integrated in a Live
    Hearing Device for Monitoring Sound Perception", Trends in Hearing 22, 2018.
    https://doi.org/10.1177/2331216518788219
48. C. da Silva Souto et al., "Flex-Printed Ear-EEG Sensors for Adequate Sleep Staging at Home",
    Frontiers in Digital Health 3:688122, 2021. https://doi.org/10.3389/fdgth.2021.688122
49. L. Moumane et al., "Signal quality evaluation of an in-ear EEG device in comparison to a
    conventional cap system", Frontiers in Neuroscience 18:1441897, 2024.
    https://doi.org/10.3389/fnins.2024.1441897
50. N. Kaongoen, J. Choi, S. Jo, "Speech-imagery-based brain-computer interface system using
    ear-EEG", Journal of Neural Engineering 18(1):016023, 2021.
    https://doi.org/10.1088/1741-2552/abd10e
51. M. Inoue et al., "Large-scale training data enhances silent speech decoding with around-ear
    EEG", Journal of Neural Engineering 23(2):026027, 2026.
    https://doi.org/10.1088/1741-2552/ae54d0
52. S. Kanoh et al., "Development of eyewear to detect movement of eyes and body" (JINS MEME),
    Transactions of the Japanese Society for Medical and Biological Engineering
    53(Supplement):S167_03, 2015. https://doi.org/10.11239/jsmbe.53.S167_03
53. R. Zhang et al., "SpeeChin: A Smart Necklace for Silent Speech Recognition", Proceedings of
    the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies 5(4):192, 2021.
    https://doi.org/10.1145/3494987
54. "Soft Active Electromyography Interface for Machine Learning-Enabled Silent Speech
    Recognition", Advanced Intelligent Systems, 2026. https://doi.org/10.1002/aisy.70440
55. Intan Technologies, "RHD Electrophysiology Amplifier Chips", accessed 2026.
    https://intantech.com/products_RHD2000.html
56. Texas Instruments, "ADS1299-x Low-Noise, 4-, 6-, 8-Channel, 24-Bit Analog-to-Digital
    Converter for EEG and Biopotential Measurements (Rev. C)", SBAS499C, 2017.
    https://www.ti.com/lit/ds/symlink/ads1299.pdf
57. S. Frey, G. Spacone, A. Cossettini, M. Guermandi, P. Schilk, L. Benini, V. Kartsch,
    "BioGAP-Ultra: A Modular Edge-AI Platform for Wearable Multimodal Biosignal Acquisition and
    Processing", arXiv:2508.13728, 2025. https://arxiv.org/abs/2508.13728
58. Ctrl Labs Corp / Meta Platforms Technologies LLC, "Wearable muscle interface systems, devices
    and methods that interact with content displayed on an electronic display", US 10,528,135 B2,
    granted 2020-01-07 (priority 2013-01-14). https://patents.google.com/patent/US10528135B2/en
59. J. Zhuang et al., "Comparison of Contributions between Facial and Neck Muscles for Speech
    Recognition Using High-Density surface Electromyography", IEEE CIVEMSA, 2019.
    https://ieeexplore.ieee.org/document/9071636
60. Z. Deng et al., "Silent Speech Recognition Based on Surface Electromyography Using a Few
    Electrode Sites Under the Guidance From High-Density Electrode Arrays", IEEE Transactions on
    Instrumentation and Measurement 72, 2023. https://ieeexplore.ieee.org/document/10043837
61. D. M. Gaddy, "Voicing Silent Speech", PhD dissertation, UC Berkeley, 2022.
    https://www2.eecs.berkeley.edu/Pubs/TechRpts/2022/EECS-2022-68.pdf
62. I. Hwang, J. Lee, K. Lee, "EMG-to-Speech with Fewer Channels", arXiv:2602.06460, 2026.
    https://arxiv.org/abs/2602.06460
63. J. Lee et al., "Articulatory Feature Prediction from Surface EMG during Speech Production",
    arXiv:2505.13814, 2025. https://arxiv.org/abs/2505.13814
64. G. S. Meltzner et al., "Speech Recognition for Vocalized and Subvocal Modes of Production
    using Surface EMG Signals from the Neck and Face", Interspeech 2008.
    https://www.isca-archive.org/interspeech_2008/meltzner08_interspeech.pdf
65. "Noninvasive Speech Restoration After Total Laryngectomy Using Surface Electromyography:
    Pilot Study", Laryngoscope Investigative Otolaryngology, 2026.
    https://doi.org/10.1002/lio2.70559
66. N. Satterlee et al., "Sentence-Level Silent Speech Recognition Using a Wearable EMG/EEG Sensor
    System with AI-Driven Sensor Fusion and Language Model", Sensors 25(19):6168, 2025.
    https://doi.org/10.3390/s25196168
67. L. Maier-Hein, F. Metze, T. Schultz, A. Waibel, "Session Independent Non-Audible Speech
    Recognition Using Surface Electromyography", IEEE ASRU 2005.
    http://www.cs.cmu.edu/afs/cs/Web/People/fmetze/interACT/Publications_files/publications/asru2005_maier-hein7910_submission20696.pdf
68. M. Wand, C. Schulte, M. Janke, T. Schultz, "Compensation of recording position shifts for a
    myoelectric Silent Speech Recognizer", IEEE ICASSP 2014.
    https://ieeexplore.ieee.org/document/6853968
69. SparkFun, "MyoWare 2.0 Muscle Sensor — Product Overview", DEV-18977, 2022.
    http://www.mouser.com/pdfDocs/Productoverview-SparkFun-DEV-18977.pdf

## Key takeaways for the build

1. **The information sits in concealable places.** AlterEgo's top-ranked regions are mental (chin),
   inner/outer laryngeal and hyoid [2]; Gaddy's importance order is 2, 3, 1, 7, 4, 6, 8, 5, with
   "the two electrodes on and below the chin … the most important" [61]; and 10 optimised of 120
   high-density electrodes (mostly on the neck) matched 40 arbitrary ones [38]. Visible cheek and
   under-eye sites are consistently the least useful [3][61].
2. **Few channels cost real accuracy.** 2–4 channels are 9–18 WER points worse than a full montage
   on open speech [61][62][63]. Plan for 7–14 channels for open vocabulary; use 2–4 only for
   closed command sets.
3. **Three legitimate "barely visible" options exist, with published numbers:** headphone-earmuff
   textile dry electrodes, 96% on 10 silent words [9]; bilateral around-ear cEEGrid, 92.24%
   cross-day with no calibration on 25 sentences and 98.00% after ≥21 days [12]; dry neckband,
   77.5 ± 6.6% silent within-session and 59.3 ± 2.2% cross-session [13].
4. **Wet gel is a lab tool, not a wearable electrode.** It dries in ~1 h and the Ag/AgCl signal is
   gone by ~3 h [30]. Dry metal is 2.5–200× higher impedance and needs 2–3 N pressure [32][40];
   coating the substrate with PEDOT:PSS or adding a conductive hydrogel layer is the documented way
   to close that gap [30][41][43].
5. **Epidermal e-tattoos are the most invisible and the only genuinely multi-day option.** Graphene
   e-tattoos are 463 nm thick, survived 52 h with a liquid bandage, and failed at 96 h; gold nanomesh
   passed a one-week inflammation test; Liu's <10 µm Cu/PI patch is the one e-tattoo actually
   validated on silent speech (89.6 ± 0.6% / 92.7 ± 0.5% on 5 / 6 words) [33][35][8].
6. **Plan the skin, not just the signal.** Use silicone adhesives, not acrylic (one surgical cohort:
   45% MARSI, acrylate 56.8% vs silicone 31.8%, 2.55× risk) [23]; acrylate allergy was 16.2% in a
   204-user device cohort [20]; 4 days of continuous dry-electrode wear with no perceived irritation
   is demonstrated [15]; ISO 10993 categories are ≤24 h / >24 h–30 d / >30 d [14].
7. **Recalibration budget: ~1–3 minutes per session.** On face+neck sEMG, 3 minutes of target data
   was statistically indistinguishable from a full ~13-minute pool, and 1 minute was worse [19];
   <10 minutes recovered >10% accuracy after neckband repositioning [13]; around-ear is the one
   layout with demonstrated zero-calibration cross-day reuse [12]. Keep a per-session/domain tag
   either way [3][12].
8. **Hard limit: pure inner speech did not decode.** "Mentally rehearsed speech produced no usable
   signal — recognition impossible" in Meltzner 2008 [64]; what works is minimal but *real*
   articulation, as in AlterEgo ("without producing a sound and moving their lips" but with
   neuromuscular engagement) [2] and Gaddy ("mouth words as naturally as possible") [3]. The owner
   must pick and rehearse one consistent minimal-articulation style — "subvocalisation" as a
   training protocol, not passive thinking.
9. **Suggested first build:** start with 7 AlterEgo sites [2] or the 8 Gaddy sites [3] using
   Ag/AgCl + Ten20 (all high-accuracy results used wet/paste [2][3][4][8]), then move the winning
   4–6 channels to **under-chin + paralaryngeal dry electrodes with a behind-ear pod**. Add the
   headphone-earmuff or cEEGrid path for the invisible daily mode.
10. **The safest concealment bet is placement, not material.** Under-chin, behind-ear and
    in-earmuff placements each have published silent-speech accuracy; skin-tone-matched or
    transparent electrodes for silent-speech EMG are **unverified** [43].

## Open questions

1. **Face-only, zero-calibration cross-day decoding** — demonstrated only for around-ear mixed
   electrophysiology [12], not for face/neck sEMG. Can a one-user face build reach it?
2. **Per-user optimal channel set** — every site study is on other people's anatomy; this owner
   needs a channel-selection experiment (start from 16–30 candidate sites, prune to 4–8)
   [2][38][61].
3. **E-tattoo durability beyond 4 days** and re-application cost: only 52 h (clean) and 96 h
   (cracked) are quantified [33]; multi-day hydrocolloid fixation is unverified.
4. **How little articulation is enough?** The Meltzner null result [64] versus AlterEgo's
   92% [2] leaves the "minimal movement" boundary undefined and untested for a single daily user.
5. **cEEGrid commercial availability and current specs** — the vendor page is now a parked domain
   (404 on the product datasheet), so live impedance/wear figures are unverified [45].
6. **Skin-tone-matched or fully transparent biopotential electrodes** with published impedance and
   silent-speech validation — unverified; PGIN (88% transparent, 92% on facial EMG, 6 ch, 8 users)
   is the closest [43].
7. **Donning/doffing time** for a multi-channel face/neck array — no primary measurement found.
8. **Do the 92.24% / 98.00% AESSI numbers replicate** outside the originating lab and on a
   non-Mandarin, larger sentence set? [12]
9. **Hydrogel water retention over days** on face/neck skin — unverified [31].
10. **Channel count vs open-vocabulary accuracy for a dry behind-ear + under-chin array** — no
    published system combines exactly those; this is the build's core experiment.
