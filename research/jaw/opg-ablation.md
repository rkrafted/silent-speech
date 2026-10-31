# Optical palatography (OPG/EOS): sensor-position ablation and what it means for a palate-free layout

Research note, compiled from public papers only. Scope: the TU Dresden / Aachen OPG-EOS line
(Peter Birkholz, Simon Preuß/Stone, João Possamai de Menezes, Arne-Lukas Fietkau, Christoph
Wagner and co-authors), plus one component datasheet. No device was built or measured here; all
numbers below are quoted from the papers named in each section. Full access records are in
`sources-opg-ablation.jsonl`.

**Headline:** the 2025 15-sensor study is real. It is an ESSV 2025 paper by Fietkau, Menezes and
Birkholz, not a journal article, and it has **no DOI**. Its ablation is *group-wise* (lip vs
lateral vs midsagittal), not sensor-by-sensor. It confirms that all three groups help, but the
published tables do not isolate the alveolar-ridge sensors, so the "alveolar ridge alone" question
cannot be answered from it.

A terminology warning that matters for every number below: in this literature "silent speech"
usually means **no acoustic signal is used by the recogniser**, not that the speaker made no sound.
Stone & Birkholz state it outright: "The words were produced in a natural way, i.e., with phonation
and at an unregulated speaking rate of each speaker's individual choice" [2020, §3.1]. The 2025
paper defines its task as "the recognition of spoken command words without the use of acoustic
speech data" and does not report instructing participants to mouth or whisper. Treat all OPG
accuracies as **acoustic-free articulation recognition**, not validated mouthed-silent decoding.

---

## 1. The 2025 15-sensor study: citation, participants, vocabulary, model, accuracy

**Citation.** Arne-Lukas Fietkau, João Vitor Possamai de Menezes, Peter Birkholz, "Evaluating
optopalatography sensor positions for silent command word recognition", in S. Grawunder (ed.),
*Studientexte zur Sprachkommunikation: Elektronische Sprachsignalverarbeitung 2025* (TUDPress,
Dresden), pp. 69–76. Conference: ESSV 2025, Halle/Saale, 5–7 March 2025.

**DOI.** None. A Crossref bibliographic query and a DataCite query for the exact title returned no
record for this paper; the ESSV proceedings do not assign DOIs. Cite the publisher PDF:
`https://www.essv.de/pdf/2025_69_76.pdf?id=1237`.

**What was recorded.** "A corpus consisting of 10 repetitions of 100 different words was recorded
by 4 speakers and served as input data for a recurrent neural network." The four were "healthy male
subjects (S1: fluent German speaker, S2 - S4: native Germans) with the ages 30-45 years"; each
"used their own individually manufactured OPG pseudo palate." Total: 100 words × 10 repetitions ×
4 speakers = 4,000 examples. The vocabulary is 80 German words taken from two earlier studies plus
20 English robot-command words (`start`, `stop`, `left`, `right`, `forward`, `backward`, ...).

**Hardware.** "Fifteen sensors are placed on one pseudo palate"; the 2024 description of the same
OPG2023 device says these are "lip (2 pairs) and tongue (13 pairs)" and that each pair is "a VCSEL
and a phototransistor". Sampling is 100 Hz, the ADC is 18-bit, and there is "a mechanism for
ambient light compensation."

**Model.** One bidirectional LSTM layer, then a fully connected layer and log-softmax (PyTorch).
Thirty random-search hyperparameter sets were generated once and reused across all evaluations;
the search covered batch size, hidden neurons, dropout and epochs, with learning rate fixed at
0.01, AdamW, negative log-likelihood, early-stopping patience 20. Inputs are raw per-sensor ADC
values, min–max normalised per sensor on training statistics.

**Accuracy** (Table 4/5 of the paper):

| Protocol | Speakers in training | Mean accuracy | Per-speaker |
|---|---|---|---|
| Single speaker | 1 | **81.25%** (SD 14.22) | 89.00 / 86.00 / 93.00 / 57.00% |
| Leave-one-speaker-out | 3 | **47.93%** (SD 15.51) | 56.90 / 53.80 / 59.70 / 21.30% |
| Multi-speaker | 4 | **90.25%** | — |

The authors call 90.25% "comparable to the state-of-the-art" and compare it with 90.67% from a
100-word sEMG study (Wu et al. 2022). The best single speaker reached 93.00% (single-speaker) and
59.70% (LOSO); the mean is dragged down by S4, "an outlier in comparison to the other 3 speakers",
whose single-speaker score was 57.00% and whose LOSO score was 21.30%.

**Is this the "2025 15-sensor study" in the brief?** Yes: 15 sensors, 2025, silent-command-word
task, 4 participants, 100-word vocabulary, neural model, accuracy. The closest alternative, and the
direct predecessor, is the 2024 Interspeech demonstrator by the same group: same OPG2023 device,
15 sensor pairs, but only **one speaker, 40 German words, and DTW pattern matching, 98.38%**
(5-fold cross-validation). The 2025 paper explicitly frames itself as the harder, multi-speaker
expansion of that 98.38% result.

**Closest few-sensor, non-personalized study (2022).** Wagner, Stappenbeck, Wenzel, Steiner,
Lehnert and Birkholz evaluated "an optopalatographic device that does not require a personalized
dental retainer": **nine** optical proximity sensors at 100 Hz, "fixated against the hard palate
with a specifically developed palatal adhesive". Corpus: eight tongue exercises (not words) from
nine healthy individuals. Classifier: DTW-kNN, **97.9% cross-validation / 61.4% inter-speaker**.
This is gesture recognition rather than command-word recognition, but it is the only OPG accuracy
in the literature for a device that is *not* individually fitted, and it is the number a
palate-free design has to beat.

**What the 2025 paper does not report.** No instruction to produce the words silently, no
audio-condition comparison, no mouthed-vs-voiced test, no open-vocabulary or continuous-speech
result, and no per-sensor ablation.

---

## 2. The ablation: which positions carry information, and what each removal costs

The ablation removes whole sensor groups, not individual sensors. There are four input sets:
all 15; no lip; no lateral; and no lip + no lateral, which is the same as midsagittal-only. The
paper's own summary is unambiguous: "the accuracy with all 15 sensors was in all cases the
highest" and "every sensor region investigated in the ablation study has a positive influence on
the recognition accuracy."

### 2.1 Region-level ablation (the only per-position numbers published)

Single-speaker evaluation, mean over 4 speakers (Table 4):

| Sensor set | Mean | SD | Δ absolute | Δ relative |
|---|---|---|---|---|
| All 15 | 81.25% | 14.22 | — | — |
| No lip | 76.00% | 18.00 | −5.25 pp | −6.46% |
| No lateral | 67.25% | 33.78 | −14.00 pp | −17.23% |
| No lip, no lateral (midsagittal only) | 77.25% | 16.08 | −4.00 pp | −4.92% |

Leave-one-speaker-out, mean over 4 folds (Table 4):

| Sensor set | Mean | SD | Δ absolute | Δ relative |
|---|---|---|---|---|
| All 15 | 47.93% | 15.51 | — | — |
| No lip | 39.80% | 12.21 | −8.13 pp | −16.96% |
| No lateral | 24.78% | 15.46 | −23.15 pp | −48.30% |
| No lip, no lateral | 40.35% | 11.10 | −7.58 pp | −15.81% |

Multi-speaker, all 4 speakers in one pool (Table 5):

| Sensor set | Accuracy | Δ absolute | Δ relative |
|---|---|---|---|
| All 15 | 90.25% | — | — |
| No lip | 88.00% | −2.25 pp | −2.49% |
| No lateral | 88.50% | −1.75 pp | −1.94% |
| No lip, no lateral | 80.75% | −9.50 pp | −10.53% |

### 2.2 Reading the table

- **Multi-speaker (the generalisation setting that matters for a product): lip is the single most
  informative group.** Removing the two lip sensors costs 2.25 pp, slightly more than removing all
  lateral sensors (1.75 pp). Removing both costs 9.50 pp — much more than the sum of the two
  individual costs (4.00 pp). That super-additivity is the paper's most interesting result: lip and
  lateral information are not redundant when the model must cover several speakers.
- **Single-speaker and LOSO say the opposite about lateral sensors, but the authors attribute it to
  model failure, not signal.** "No lateral" collapses to 67.25% single-speaker and 24.78% LOSO,
  worse than removing both groups. The paper states this is "model underfitting, as none of the 30
  hyperparameters sets resulted in accuracies if not equal, at least similar to the case when
  neither lip nor lateral sensors were used", and it is amplified by S4. Excluding S4, single-speaker
  means become 86.00% (no lip), 86.67% (no lateral) and 86.33% (both) — "no sensible differences
  when different sensor regions are removed" for one speaker. Do not quote the −14.00 pp / −23.15 pp
  rows as clean sensor-value estimates.
- **The midsagittal core is most of the device.** Midsagittal-only still reaches 77.25% single-speaker
  (95.1% of the full-set accuracy) and 40.35% LOSO (84.2% of full). The 13 tongue sensors include the
  midsagittal line plus lateral tongue sensors; the paper never gives the split count, because the
  position map is a colour figure, not a table.
- **The most valuable single region is the lips in the many-speaker case; the most valuable dense
  region is the midline.** With only 2 lip sensors, losing them costs 2.49% relative in the
  multi-speaker model. Losing all lateral sensors costs 1.94% relative there. Neither group alone is
  close to the full set once both are removed (10.53% relative).

### 2.3 The per-sensor table the brief asks for does not exist

The paper publishes no leave-one-sensor-out table. What exists is a named-position map in the
companion 2025 radar+OPG paper: **S11 lip opening, S12 lip protrusion, S13 alveolar, S14
post-alveolar, S21 hard palate, S31 hard palate, S41 velar**. Those are region labels for the
midsagittal sensors; the 15-sensor palate repeats positions laterally. No accuracy is reported for
S13 alone, for S13+S14, or for any "teeth line" subset.

| Named position | What it senses | Isolated ablation reported? |
|---|---|---|
| S11 | lip opening | No (only the 2-sensor lip group: −2.25 pp multi, −5.25 pp single) |
| S12 | lip protrusion | No (same group) |
| S13 | alveolar | **No** |
| S14 | post-alveolar | **No** |
| S21, S31 | hard palate (midline) | No (only "midsagittal only" as a set) |
| S41 | velar | No |
| lateral group | side tongue/palate | Group only: −1.75 pp multi, −14.00 pp single, −23.15 pp LOSO |

**Answer to "do sensors near the teeth line / alveolar ridge alone come close to the full set?"**
Not answerable from the 2025 paper. The closest published subset is midsagittal-only, which is
**4.92% relative below** the full set in single-speaker and **15.81% relative below** in LOSO. An
alveolar-only subset could be better or worse; no one has published it. This is the single most
useful experiment the group has not run.

---

## 3. Open vowels and non-contact sounds that contact EPG misses

### 3.1 Why OPG sees them

EPG gives a binary contact/no-contact map. OPG gives a distance from reflected light intensity, so
it works precisely where there is no contact. The 2012 design paper puts it plainly: EPG "provides
no indication about the position of the tongue when it is not touching the palate. Therefore, it is
not suitable for the analysis of phones with little or no tongue-palate contact, for example mid and
open vowels." The 2015 calibration paper repeats that EPG is "intrinsically 'blind' to all tongue
movements that do not contain palate contact (such as the movements necessary to produce open or
back vowels)". The 2011 paper gives the concrete example: "there is virtually no information about
the articulation of /E/ and /a/ in the EPG patterns, but the tongue profiles properly reflect the
different vertical tongue positions of the shown vowels."

The earliest statement of the same limit is Wrench, McIntosh and Hardcastle (1996), who introduced
the optical-fibre optopalatograph: with EPG, "If the tongue is not touching the palate there is no
indication of how far it is from the palate. Consequently, it is best at providing feedback for
obstruent, lateral, and high front vowel articulations." That is the design brief for OPG in one
sentence: EPG does not mislabel open vowels, it records nothing about them.

That is a statement about the *signal*, not about classifier accuracy. When the same group actually
classified vowels, EPG did surprisingly well on /a:/ because the EPG pattern still carries indirect
information and the classifier had context.

### 3.2 Per-vowel numbers: contact vs optical vs both (2012)

Six German long vowels, 97 tokens from a read passage, four-fold cross-validated feed-forward
networks, 4 EPG indices vs 5 optical distances (Table 1 of the 2012 Interspeech paper):

| Vowel | Items | Contact sensors | Optical sensors | Both |
|---|---|---|---|---|
| [a:] | 30 | 96.7% | **100.0%** | 100.0% |
| [e:] | 11 | **18.2%** | 9.1% | 36.4% |
| [i:] | 29 | 86.2% | **89.7%** | 79.3% |
| [o:] | 15 | **46.7%** | 40.0% | 53.3% |
| [u:] | 8 | 0.0% | 0.0% | **25.0%** |
| [y:] | 4 | 0.0% | 0.0% | 0.0% |
| **All** | **97** | **64.9%** | **64.9%** | **69.1%** |

This is the cleanest per-sound evidence in the literature, and it is sobering:

- Optical alone is **not** a superset of contact. It wins on [a:] (+3.3 pp) and [i:] (+3.5 pp),
  loses on [e:] (−9.1 pp) and [o:] (−6.7 pp), and is identical at 0% on [u:]/[y:].
- Fusion is the only condition that beats both single modalities overall (69.1% vs 64.9%).
- The rare vowels are data-starved (4–11 tokens), so the 0% cells are not evidence that OPG cannot
  represent [u:]; they are evidence that a 97-token corpus cannot train six classes.

### 3.3 Per-class numbers on 26 phonemes (2025, OPG alone and fused with radar)

Three native German male speakers, 26 phonemes, 10 repetitions in multiple consonant/vowel
contexts, RBF-SVM with 50 repeats of nested cross-validation (Table 4 of the 2025 radar+OPG paper):

| Input | Tense vowels | Lax vowels | Consonants |
|---|---|---|---|
| Radar alone | 83.36% | 84.02% | 88.04% |
| OPG alone | 63.07% | **71.25%** | 67.50% |
| Radar + OPG | **83.39%** | **84.89%** | **90.08%** |

OPG's best class is **lax vowels**, not tense/open vowels, and its weakest is consonants. The paper's
interpretation is that OPG's low-dimensional, interpretable distance signal is complementary to
radar, not a replacement for contact sensing. On the full 26-class task OPG reached 70.61%
single-speaker mean and 66.99% multi-speaker, against radar's 88.48% and 85.40%.

### 3.4 Net answer

OPG supplies the missing physical variable for open vowels, and the 2012 table shows it can beat
contact sensing on [a:] and [i:]. But the measured gain is small and class-dependent: optical alone
ties contact at 64.9% overall, and neither modality handles the rare rounded vowels. For a
palate-free design, distance sensing is necessary but not sufficient; the published evidence supports
**distance plus a second channel**, not distance alone.

---

## 4. Fusion with lips, EPG and other channels; models other than HMMs

### 4.1 Lip sensing is already inside OPG, and it is not optional

The 2011 prototype added "one forward-directed sensor in front of the upper incisors" and found it
"very effective for the discrimination of unrounded vowels, rounded vowels, and bilabial closures";
even the context vowel of a bilabial closure could be distinguished. The 2012 palate made this
sensor S0 on the same flexible circuit. The 2015 EOS palate has a sixth optical sensor in front of
the incisors with **two** phototransistors, "to determine both degrees of freedom of lip movement,
i.e., protrusion and opening". The 2020 EOS system uses **two** separate lip sensors (one facing the
lower lip for opening, one on the incisors for protrusion), and its feature vector is "the ADC data
of the 2 lip sensors, 5 distance sensor values, and 3 factors describing the contact pattern for a
total of 10 features per vector."

The 2025 ablation quantifies the loss: **−2.25 pp multi-speaker (−2.49% relative), −5.25 pp
single-speaker, −8.13 pp LOSO**. This is the strongest argument in the literature for keeping at
least one lip sensor on any reduced layout.

The 2013 real-time system explains why one lip sensor is not enough, in a passage that anticipates
the 2015 redesign: with a single forward sensor the lips have "two degrees of freedom (protrusion and
opening)", and "The transitions between the described extremes are non-unique using a single lip
sensor and cannot be reconstructed accurately and the visualization must be limited to the opening."
A palate-free design that substitutes lip imaging for a lip sensor has to resolve both degrees of
freedom, or it inherits exactly this ambiguity.

### 4.2 EPG + OPG = EOS: the original fusion

EOS is the same pseudopalate carrying both electrical contact sensors and optical distance sensors.
Configuration changed across generations:

| System | Contact sensors | Optical tongue | Optical lip | Result |
|---|---|---|---|---|
| 2011 prototype | 62 (Articulate) | 3 | 1 (+1 velum) | Qualitative; lip sensor effective, velum sensor failed |
| 2012 Interspeech | EPG strip | 4 (S1–S4) | 1 (S0) | Vowel classification 64.9% contact, 64.9% optical, **69.1% both** |
| 2015 EOS | 124 | 5 laser | 1 (2 detectors) | Calibration; median position error "close to 1 mm" |
| 2016 Show & Tell | 124 | 5 laser | 1 (2 detectors) | Viterbi + Mahalanobis, 30-word demo |
| 2020 ICASSP | 32 | 5 laser | 2 | BLSTM: **97–99.5%** single-speaker; **56.17–61.75%** LOSO |

The 2020 study is the best EOS accuracy reference: two corpora (10 digits, 30 frequent German
words), four male speakers aged 30–41, 10 repetitions each, BLSTM with 10 features. Speaker-dependent
accuracy was "up to the state-of-the-art with average word accuracies of 97% to 99.5%"; LOSO was
"approx. 56% to 62%". That is the same pattern as the 2025 OPG-only study: near-ceiling within a
speaker, roughly halved across speakers.

### 4.3 OPG + radar: the only non-palatal fusion with numbers

The 2025 Interspeech paper recorded radar (one emitter on the left cheek, two receivers on the
right) and OPG simultaneously from three native German male speakers, 26 phonemes, 10 repetitions.
RBF-SVM, 50 repeats of nested cross-validation:

| Input | Single-speaker mean | Multi-speaker |
|---|---|---|
| Radar | 88.48% | 85.40% |
| OPG | 70.61% | 66.99% |
| Radar + OPG | **90.06%** | **86.55%** |

The fusion gain is small but statistically significant: **+1.15 pp absolute / +1.35% relative**
multi-speaker, +1.58 pp single-speaker. The useful part is where the gain lands: for the alveolar
/t/ and post-alveolar /S/, "the mean accuracy for these phonemes increased from 77.60% to 85.40%,
while the confusion between each other decreased from 12.75% to 5.80%." That is exactly the
alveolar/post-alveolar distinction a reduced palate is most at risk of losing.

### 4.4 Models: BLSTM, DTW, SVM, Viterbi — no CNN, transformer or CTC found

| Paper | Task | Model |
|---|---|---|
| Stone & Birkholz 2016 | 30-word EOS command recognition | Viterbi + Mahalanobis distance (HMM-style) |
| Stone & Birkholz 2020 | 10/30-word EOS | 1-layer BLSTM + FC |
| Possamai de Menezes et al. 2024 | 40-word OPG | DTW pattern matching |
| Fietkau et al. 2025 | 100-word OPG, ablation | 1-layer BLSTM + FC + log-softmax |
| Menezes et al. 2025 | 26-phoneme radar+OPG | RBF-SVM |

I found **no OPG or EOS paper using a CNN, transformer or CTC loss**. Searches by the permitted
author names and the terms "optopalatography" / "electro-optical stomatography" returned the papers
above and no deep convolutional or attention-based OPG classifier. The line has stayed on small
recurrent models, DTW and SVMs because the datasets are tiny (97 tokens in 2012; 4,000 utterances
in 2025) and the input is 15 or fewer channels. Any claim that a transformer/CTC OPG result exists
should be treated as unverified until a citation is produced.

### 4.5 The channel neither OPG nor EPG has: velum state

Both palatographic modalities are blind to the velum, which is why the same group built a separate
sensor for it. Birkholz, Bakardjiev, Kürbis and Petrick (2016) describe "a portable minimally
invasive system to determine the state of the velum (raised or lowered) at a sampling rate of
40 Hz that works both during normal and silent speech": a capsule inserted "into one nostril by
about 10 mm" whose loudspeaker emits "chirps with a power band from 12-24 kHz" while a microphone
records the reflection. The motivation is stated against the alternatives: EMG and
ultrasound-plus-lip-video silent-speech systems "provide no reliable information about the velar
state, making a distinction of nasalized and non-nasalized speech sounds difficult."

This is the only extra channel in the line that adds an articulator rather than another view of the
tongue, and there is **no published fusion of it with OPG** — the 2016 paper is a design study with
no recognition accuracy. The in-mouth alternative was already tried and failed: the 2011 prototype
included one velum-directed optical sensor, and the table in §4.2 records it as "velum sensor
failed". For a palate-free layout the velum is therefore the one articulator that no amount of
extra tongue-distance sensing can recover; treat nasal/non-nasal contrast as unsolved unless a
dedicated velum channel is added.

---

## 5. Hardware facts

Values below are from the papers that built the devices; where a generation differs, the range is
given. The 2025 study uses the OPG2023 device, i.e. the last row group.

| Parameter | Value | Source |
|---|---|---|
| Sensing principle | Reflected infrared intensity → distance; light source + photodetector side by side on the lingual side of the palate | 2023 review §1.1 |
| Emitter, early | LED VSMY2850G (lensed, 2.3 × 2.3 × 2.8 mm) or TCND5000 (integrated LED + photodiode) | 2012 ESSV; 2023 review |
| Emitter, late | Laser diode / VCSEL **VC850M-SMD** (1.6 × 0.8 × 0.6 mm); OPG2023 uses "a VCSEL" | 2023 review; 2024 |
| Wavelength | **850 nm typical, 840–860 nm range** (VC850M family) | VC850M datasheet |
| Optical power | **10 mW cw** rated, 20 mA operating current, 1.4–2.2 V forward | VC850M datasheet |
| Detector | Phototransistor TEMT7100X01 (2 × 1.25 × 0.85 mm) early; photodiode SFH 2704 (2 × 1.8 × 0.6 mm) in Model 6; OPG2023 phototransistor | 2023 review; 2024 |
| Range | **25 mm minimum requirement** (2011); calibration at 0, 5, 10, 15, 20, 25, 30 mm; "distances larger than 30 mm are generally irrelevant" | 2011; 2015 |
| Sample rate | **100 Hz** for every generation (contact and optical) | 2011–2025, all |
| ADC | 10-bit (2012), 12-bit (2015 EOS), **18-bit (OPG2023)** | 2012; 2015; 2025 |
| Multiplexing | Optical sensors switched in sequence to avoid optical crosstalk; 4 × 32:1 analog mux for contact sensors | 2011; 2013; 2015 |
| Power | 9 V battery → 3.3 V (2015 EOS); 16 × 10 cm control board; early LEDs driven at ~165–166 mA pulses; laser "requires substantially less electrical power"; VCSEL 20 mA | 2013; 2015; 2023 review |
| Pseudopalate thickness | 0.5 mm thermoformed acrylic/foil base (2011, 2012, Model 6); two 0.5 mm layers in the 2012 EOS prototype; 1 mm transparent sheets in Model 5; optical components 0.6–2.8 mm high; early sensors protruded "about 2 mm"; 1980s glossometry palates "up to 4 mm"; fibre-optic OPG palates 1–2 mm | 2011; 2012; 2012 ESSV; 2023 review |
| Wired or wireless | **Wired.** 2015 EOS: "22 lines ... exit the mouth" to a 16 × 10 cm board, then RS232 to a PC. 2024 OPG2023: "USB interfaces used to connect the OPG device to a computer." No wireless OPG/EOS version appears in the reviewed papers. | 2015 ESSV; 2024 |
| Fitting | Individual impression → plaster model → 0.5 mm foil thermoformed → flexible PCB glued → foil removed from molars/premolars → Adams clasps + silicone cable conduit. "A skilled dental technican needs about two hours" given a populated board; material cost "about 50 Euros" at 5–10 units. 2025: every speaker had "their own individually manufactured OPG pseudo palate." | 2012 ESSV; 2025 |
| Fitting, non-personalized | The one alternative in the literature: 9 sensors, no dental retainer, held "against the hard palate with a specifically developed palatal adhesive" (adhesive instead of clasps); inter-speaker accuracy 61.4% vs 97.9% within-speaker, and the paper does not report self-placement | 2022 TBME |
| Crosstalk / error budget | Fibre-optic OPG with all halogen channels lit simultaneously: "worst case error of 10% in estimated distance values below 5mm"; later designs switch optical sensors in sequence instead | 1997; 2011–2015 |
| Calibration | In-vitro distance function with tube spacers, or single in-vivo 0 mm contact + multi-linear regression to 0–30 mm; "maximum median position errors close to 1 mm" | 2012 ESSV; 2015 |

Two hardware qualifications:

1. **The 850 nm figure is from the VC850M datasheet, not from a speech paper.** The papers say only
   "infrared" and give the part number. The VC850M-Z-TO18FW datasheet I opened is the TO-18 package
   variant; the palate uses the SMD variant. Same emitter family and wavelength class, different
   package. Treat 850 nm as the design value, not a measured in-mouth value.
2. **Thickness is local, not uniform.** The carrier sheet is 0.5 mm, but the sensors stand 0.6–2.8 mm
   above it; the 2011 paper says they "protruded about 2 mm from the pseudopalate surface into the
   mouth." A "0.5 mm palate" claim would be misleading.

---

## 6. What this means for a palate-free layout

1. **A midline-only strip is viable for one user, not for many.** Midsagittal-only scores 77.25%
   single-speaker (95.1% of the 81.25% full-set result) but 40.35% LOSO (84.2% of 47.93%), and the
   multi-speaker midsagittal-only result is 80.75% vs 90.25% full (−10.53% relative). A palate-free
   device that covers only the midline should be sold as a per-user trained device, not a
   speaker-independent one.
2. **Keep two lip sensors if the form factor allows it.** They cost little space (two apertures at
   the incisors) and removing them costs 2.25 pp multi-speaker, 5.25 pp single-speaker and 8.13 pp
   LOSO. In the multi-speaker model they are the most informative single group (2.49% relative vs
   1.94% for all lateral sensors).
3. **Do not drop lateral coverage without testing cross-speaker generalisation.** The lateral group
   is only 1.75 pp in the multi-speaker pool, but 23.15 pp in LOSO — even allowing for the paper's
   admitted underfitting, the direction is consistent with lateral geometry helping
   speaker-to-speaker mapping. A palate-free layout with no side coverage is the riskiest cut.
4. **The alveolar/post-alveolar zone is where fusion pays.** Radar+OPG raised /t/ and /S/ from
   77.60% to 85.40% and halved their mutual confusion from 12.75% to 5.80%. If a palate-free design
   loses the anterior contact row, a second channel that resolves alveolar vs post-alveolar is worth
   more than more midline distance sensors.
5. **Distance sensing is necessary but not sufficient for open vowels.** OPG beats contact on [a:]
   (100.0% vs 96.7%) and [i:] (89.7% vs 86.2%), but loses on [e:] (9.1% vs 18.2%) and [o:] (40.0% vs
   46.7%), and both are 0% on [u:]/[y:] with 4–8 tokens. Plan for fusion, not a single modality.
6. **"Silent" is unproven in this literature.** The 2020 EOS words were "produced ... with
   phonation"; the 2025 paper's "silent" means no acoustic input, not inaudible articulation. A
   palate-free silent device must run its own mouthed/whispered validation; no OPG paper reports a
   mouthed-only accuracy.
7. **The electronics are still wired and bench-bound.** 22 wires exit the mouth in the 2015 EOS
   system; OPG2023 connects by USB to a portable control unit. No wireless OPG exists in this line.
   A palate-free layout inherits the wiring/retention problem, not just the sensor-placement problem.
8. **Budget for per-user training and a small vocabulary.** The best OPG numbers are 98.38% on 40
   words for one speaker (DTW) and 90.25% on 100 words with four speakers (BLSTM); LOSO falls to
   47.93%. The one non-personalized device reported 97.9% within-speaker but **61.4% inter-speaker**
   on just eight gestures with nine sensors. A palate-free device with fewer sensors should not
   promise open-vocabulary ASR from the published evidence.

---

## 7. Limits of this review

- **Group ablation only.** The 2025 paper's four input sets are all/lip/lateral/midsagittal. No
  leave-one-sensor-out table, no alveolar-only table, no per-sensor information gain. The per-position
  table in §2.3 is a list of named positions, not a list of measured contributions.
- **Four speakers, one corpus, one device generation.** S4 is an outlier (57.00% single-speaker),
  and the authors themselves flag model underfitting for the "no lateral" condition. The 2025 paper
  calls its own multi-speaker result "comparable to the state-of-the-art" but with "considerably less
  speakers than most of these studies."
- **No silent-production validation.** "Silent" = acoustic-free recognition. The 2020 paper is
  explicit that words were phonated; the 2025 paper is silent about production mode.
- **No DOI for the key paper.** ESSV 2025 is a proceedings volume without DOIs. The publisher PDF is
  the authoritative version; the title on the TU Dresden publication list omits "silent" ("Evaluating
  optopalatography sensor positions for command word recognition"), while the PDF title includes it.
- **Access note.** The ESSV host resets direct connections and serves a JavaScript challenge, so
  the 2025 ESSV paper was read through a text-rendering reader proxy of the publisher PDF. The three
  earlier ESSV papers are also mirrored on the TU Dresden publication server and were downloaded from
  there directly, together with the ISCA, PubMed and vocaltractlab.de PDFs. The extracted PDF text is
  what the quotes and numbers come from. No paywalled paper is cited for a number.
- **Search bounds.** Searches used only the permitted author names and terms
  ("optopalatography", "optical palatography", "electro-optical stomatography", "pseudopalate") plus
  citation chaining. A CNN/transformer/CTC OPG paper could exist outside that net; none was found
  inside it.

## Sources

Numbered as in `sources-opg-ablation.jsonl`; each was opened and read.

1. Fietkau, Possamai de Menezes, Birkholz (2025), *Evaluating optopalatography sensor positions for
   silent command word recognition*, ESSV 2025, pp. 69–76.
2. Possamai de Menezes, Fietkau, Diener, Kürbis, Birkholz (2024), *A demonstrator for
   articulation-based command word recognition*, Interspeech 2024, pp. 2042–2043.
3. Menezes, Mouras, Fietkau, Kazzy, Birkholz (2025), *Multimodal silent recognition of phonemes
   using radar and optopalatographic silent speech interfaces*, Interspeech 2025, pp. 5058–5062.
4. Birkholz, Neuschaefer-Rube (2011), *Combined optical distance sensing and electropalatography to
   measure articulation*, Interspeech 2011, pp. 285–288.
5. Birkholz, Dächert, Neuschaefer-Rube (2012), *Advances in combined electro-optical palatography*,
   Interspeech 2012, pp. 703–706.
6. Birkholz, Neuschaefer-Rube (2012), *A new artificial palate design for the optical measurement of
   tongue and lip movements*, ESSV 2012, pp. 89–95.
7. Preuß, Neuschaefer-Rube, Birkholz (2013), *Prospects of EPG and OPG sensor fusion in pursuit of a
   3D real-time representation of the oral cavity*, ESSV 2013, pp. 144–151.
8. Preuß, Birkholz (2015), *Optical sensor calibration for electro-optical stomatography*,
   Interspeech 2015, pp. 618–622.
9. Preuß, Birkholz (2015), *Fortschritte in der Elektro-Optischen Stomatographie*, ESSV 2015,
   pp. 248–255.
10. Stone, Birkholz (2016), *Silent-speech command word recognition using electro-optical
    stomatography*, Interspeech 2016 Show & Tell, pp. 2350–2351.
11. Stone, Birkholz (2020), *Cross-speaker silent-speech command word recognition using
    electro-optical stomatography*, ICASSP 2020, pp. 7849–7853.
12. Birkholz, Stone, Wagner, Kürbis, Wilbrandt, Bosshammer (2023), *A review of palatographic
    measurement devices developed at the TU Dresden from 2011 to 2022*, ICPhS 2023, pp. 883–887.
13. Roithner Lasertechnik (2022), *VC850M-Z-TO18FW 850 nm VCSEL datasheet* (component document, not
    a speech paper).
14. Preuß, Neuschaefer-Rube, Birkholz (2013), *Real-time control of a 2D animation model of the vocal
    tract using optopalatography*, Interspeech 2013, pp. 997–1001.
15. Preuß, Eckers, Birkholz, Neuschaefer-Rube (2014), *Ein OPG-gesteuertes Serious Game zur
    Unterstützung von mundmotorischen Übungen*, ESSV 2014.
16. Birkholz, Bakardjiev, Kürbis, Petrick (2016), *Towards minimally invasive velar state detection in
    normal and silent speech*, Interspeech 2016, pp. 1780–1784.
17. Wagner, Stappenbeck, Wenzel, Steiner, Lehnert, Birkholz (2022), *Evaluation of a
    non-personalized optopalatographic device for prospective use in functional post-stroke dysphagia
    therapy*, IEEE Trans. Biomed. Eng. 69(1):356–365, doi:10.1109/TBME.2021.3094415, PMID 34214033.
18. Wrench, McIntosh, Hardcastle (1996), *Optopalatograph (OPG): a new apparatus for speech
    production analysis*, ICSLP 1996, doi:10.21437/ICSLP.1996-408.
19. Wrench, McIntosh, Hardcastle (1997), *Optopalatograph: development of a device for measuring
    tongue movement in 3D*, Eurospeech 1997, doi:10.21437/Eurospeech.1997-366.
20. Birkholz, Schutte, Preuß, Neuschaefer-Rube (2014), *Towards non-invasive velum state detection
    during speaking using high-frequency acoustic chirps*, ESSV 2014.
