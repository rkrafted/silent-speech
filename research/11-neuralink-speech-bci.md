# Track 11 — Neuralink and invasive speech BCIs: what they proved and what transfers

*Research report for the silent-speech wearable project. Status: COMPLETE.*

Conventions (from `BRIEF.md`): inline `[n]` citations map to the numbered Sources list at the end.
Numbers are quoted exactly as the source gives them. **Demonstrated** results (peer-reviewed, with
participant count / vocabulary / open vs closed vocabulary / silent vs mouthed vs voiced) are kept
strictly separate from **claims/marketing** (livestreams, tweets, press releases, company pages).
Anything I could not verify against a page I fetched is marked **(unverified)**.

**Anatomy warning up front, because this track exists to answer it.** Neuralink's N1 sits in
**motor cortex (brain)**. This project's sensors read **facial and neck muscles (surface EMG)**.
They are different tissues, different signal physics, different failure modes. "Similar
positioning" is true for neither the hardware nor the signal:

- A microelectrode array records **action potentials of individual neurons** (spikes, ~µV–mV,
  sampled at ~20–30 kHz, 1,000+ channels) **inside** cortex. Facial sEMG records the **summed
  motor-unit action potentials of whole muscles** (µV–mV, 250 Hz–5 kHz, 8–32 channels) **through
  skin**. One is a population of digital-ish event trains; the other is a continuous, low-pass,
  cross-talk-heavy mixture.
- Neuralink's electrode **penetrates** the cortical surface; this build's electrodes sit on the
  face or behind the ear and do not break the skin.
- Motor cortex encodes **articulatory plans**; facial muscles are one **downstream actuator** of
  those plans. Decoding the actuator is a strictly harder and lossier inverse problem.

What *can* transfer is **algorithmic and protocol-level**: output units, language-model decoding,
streaming architectures, calibration protocol, and the attempted-vs-inner-speech distinction. This
report is organised to extract exactly those, and to say plainly where the analogy stops.

---

## 1. Neuralink: the full record, 2019–2026

**Headline verdict:** Neuralink has produced **no peer-reviewed speech-decoding result**. Its
public record is a 2019 methods white paper plus company blog/livestream/press announcements. Its
2025 "speech" milestone is **cursor typing plus text-to-speech**, not neural decoding of speech.
Everything below is labelled by evidence class.

### 1.1 The 2019 platform paper

The only journal publication describing the implant is E. Musk and Neuralink, *An Integrated
Brain-Machine Interface Platform With Thousands of Channels*, J Med Internet Res 2019;21(10):e16194
`[13]`. I could not render the JMIR HTML (HTTP 202, empty body), but I downloaded and text-extracted
the **white-paper PDF itself** and read it, so the following are **primary-source figures** (the
paper uses ";" for the decimal point in the PDF text, e.g. "3;072"):

- "arrays of small and flexible electrode 'threads', with as many as **3,072 electrodes per array
  distributed across 96 threads**" `[13]`.
- Each array has "48 or 96 threads, each of those containing **32 independent electrodes**"; "96
  polymer threads, each thread with 32 electrodes, in a (4 × 7) mm² area of brain for a total of
  3,072 electrodes" `[13]`.
- Thread geometry: widths **5–50 µm**, thickness "nominally **4 to 6 µm**", typical length
  "approximately **20 mm**" `[13]`.
- Electrode impedance: "**36.97 ± 4.68 kΩ** (n = 257 electrodes)" for PEDOT:PSS and "**56.46 ± 7.10 kΩ**
  (n = 588)" `[13]`.
- Surgical robot: "capable of inserting **six threads (192 electrodes) per minute**"; chronic
  implant recordings "averaged 45 min" per surgery with "an approximate insertion rate of **29.6
  electrodes per minute**" `[13]`.
- Electronics: a neural processing ASIC "capable of processing **256 channels** of data"; "this
  particular packaged device contains **12 of these chips for a total of 3,072 channels**". The
  3,072-channel package "occupies less than (23 × 18.5 × 2) mm³". Recording bandwidth
  "**3 Hz–27 kHz**". A single USB-C cable provides "full-bandwidth data streaming … recording from
  all channels simultaneously" `[13]`.
- Yield: "a spiking yield of up to **85.5%** in chronically implanted electrodes"; on the
  chronically implanted array described, the spiking yield was **53.4%** of "all 1,280 implanted
  channels", with a maximum of 85.5% `[13]`.
- The paper itself cites prior speech work "using no more than 256 electrodes" as motivation `[13]`.

The *shipped human* N1 (as opposed to the 2019 rodent research platform) is described in
Neuralink's own materials as **1,024 electrodes on 64 threads**, fully implantable and wireless with
inductive charging, targeting the **precentral gyrus ("hand-knob" motor cortex)**; the company says
it transmits spike counts over Bluetooth and, in the 2021 MindPong demo, "1 count every 25 ms × 1024
channels" `[14][44]`. These are **company-published, not peer-reviewed**. The human N1's electrode
contact diameter and wireless bandwidth are **(unverified)**.

### 1.2 The human timeline (all company-announced unless noted)

- **2020–2023 (regulatory):** FDA breakthrough designation for N1 announced Aug 2020; the company's
  first trial application was reportedly rejected in early 2022 over battery and wire-migration
  concerns **(secondary)** `[58]`; FDA granted the PRIME IDE in **May 2023** `[14]`. **PRIME**
  (NCT06429735) is registered with a start date of **9 Jan 2024**, estimated enrolment **15**, ages
  22–75, and primary endpoints of **device- and procedure-related adverse events** `[54]`.
- **Participants (company-announced):** 1 **Noland Arbaugh** (Jan 2024; reported cursor rate rising
  from **4.6 to 8.0 bits/s**); 2 "**Alex**" (Jul 2024); 3 **Bradford G. Smith** (Nov 2024, ALS,
  first non-verbal); 4 **Mike** (Feb 2025); 5 **RJ** (Apr 2025); 6 **Rob Greiner** (Jun 2025); 7
  undisclosed; 8 **Nick Wray** (CONVOY, Oct 2025). Neuralink reported **12** cumulative participants
  by Sept 2025 and **21** by late Jan 2026 with "zero serious device-related adverse events"
  **(press)** `[57][59]`.
- **Thread retraction:** Neuralink's own wording is a "net decrease in the number of effective
  electrodes" with performance recovered by an **algorithm change**; the widely repeated "**85% of
  threads**" figure is **WSJ-sourced via secondary press**, not a Neuralink statement `[57][58]`.
- **2 May 2025:** FDA **breakthrough device designation** for "restoring communication in patients
  with severe speech impairment" `[11]`. This is a regulatory fast-track tag, **not** a working
  decoder.
- **Apr–May 2025:** third participant **Bradford G. Smith** ("Brad"), ALS and non-verbal, stated "I
  am typing this with my brain. It is my primary communication." The "speech" was **AI narration
  with a synthesised version of his former voice** driven by cursor-selected text — i.e.
  **text-to-speech + voice cloning, not neural speech decoding** `[11]`. The press framing
  ("regains speech") overstates the technical claim.
- **June 2025:** Neuralink open-sourced a `datarepo` toolkit, but its blog states "**This is not a
  release of any Neuralink data**"; the GitHub org has no datasets `[57]`.
- **13 June 2025 (Blindsight):** an engineer presented a monkey result at the Neural Interfaces
  conference — the animal moved its eyes toward an implant-induced percept "**at least
  two-thirds of the time**"; no peer-reviewed paper `[60]`.
- **3 Oct 2025 (VOICE):** a **speech-restoration** early-feasibility study registered
  (NCT07224256), estimated enrolment **6**, ages 22–75, primary endpoints device/procedure AEs
  `[56]`. No results are posted.
- **CONVOY:** registered **25 Nov 2024** (NCT06710626), estimated enrolment **3**, primary outcome
  "ability of participants to modulate brain activity for controlling an assistive device via the
  N1 Implant" `[55]`. Eighth participant **Nick Wray** (ALS) used a robotic arm over "three
  eight-hour sessions" to drink from a cup, put on a hat, microwave food, open a refrigerator, move
  "39 cylinders across a table in five minutes" and flip five pegs, plus first wheelchair control
  `[12]`.
- **Credibility caveats:** USDA OIG probe (Dec 2022), a DOT investigation into transport of
  drug-resistant bacteria and Herpes B (Feb 2023), and an FDA June 2023 inspection that cited
  "objectionable conditions or practices" in documentation while stating it "did not find evidence
  of any violations that would undermine the device's safety" `[58]`.
- **Peer-reviewed output:** only the 2019 white paper `[13]` and a 2026 *J Neural Eng* BCI-society
  workshop summary co-authored by a Neuralink employee `[61]`. A first-in-human manuscript was
  reported **submitted to NEJM** around Oct 2025 with no published version found **(unverified)**.
- No published speech-BCI accuracy, WER, vocabulary or words-per-minute figure from Neuralink was
  found. Its claimed cursor records appear only in press and X posts `[12]`.

### 1.3 Peer-reviewed vs claimed — the verdict table

| Item | Evidence class | Ref |
|---|---|---|
| 2019 platform: 3,072 electrodes / 96 threads / robotic inserter / 85.5% max spiking yield | **Peer-reviewed white paper** (JMIR) | `[13]` |
| PRIME (NCT06429735), CONVOY (NCT06710626), VOICE (NCT07224256) | Trial **registrations** only; no results posted | `[54][55][56]` |
| First human implant → 8 reported participants (2024–25); 12 → 21 cumulative | Company livestream/X/press only; cursor rate 4.6→8.0 bits/s is unpublished | `[12][57][59]` |
| Thread retraction and software recovery | Neuralink confirms a "net decrease in effective electrodes"; the "85% of threads" figure is **secondary press** | `[57][58]` |
| FDA breakthrough designation for speech restoration (May 2025) | Regulatory tag; **not a result** | `[11]` |
| Brad Smith "regains speech" | Press/X; technically cursor typing + **AI voice cloning**, not speech decoding | `[11]` |
| Blindsight monkey (June 2025) | Conference talk/poster; no paper | `[60]` |
| CONVOY robotic-arm tasks (Nick Wray, Oct 2025) | Company/X demonstration; no paper | `[12]` |
| Any Neuralink speech WER / vocabulary / words-per-minute | **None found** | — |
| Any Neuralink dataset, code or model release | `datarepo` toolkit only; blog says "not a release of any Neuralink data" | `[57]` |
| Peer-reviewed Neuralink output, 2019–2026 | 2019 white paper + 2026 BCI-society workshop summary only | `[13][61]` |

### 1.4 Why this matters for the build

- Neuralink is the **worst-documented** of the invasive players. For a personal R&D project the
  useful lessons come from Stanford/UC Davis/UCSF (below), not from Neuralink.
- Its one clearly relevant engineering signal is the **thread-retraction/software-recovery** story:
  a signal-loss event was handled by **recalibrating the decoder**, not by replacing hardware `[12]`.
  The surface-EMG analogue is real and central: when contact changes (electrode re-donning, sweat,
  beard, neck position), the **decoder must adapt**, because the hardware cannot be re-implanted
  every session.
- Neuralink publishes essentially nothing that can be reused: no dataset, no code, no model
  weights, no WER tables. **Do not plan any part of this build around Neuralink data.**

---

## 2. The invasive speech-BCI leaders, with real numbers

These are the numbers that matter. All are peer-reviewed. "Vocab" = output vocabulary; "WER" =
word error rate; "wpm" = words per minute.

### 2.1 Stanford — Willett et al., Nature 2023 (speech-to-text from spikes)

Demonstrated, participant with ALS who "can no longer speak intelligibly" `[1]`:
- **9.1% WER on a 50-word vocabulary** and **23.8% WER on a 125,000-word vocabulary** — described
  as "the first successful demonstration of large-vocabulary decoding". The paper's table gives
  125k vocalized **23.8% WER / 19.7% phoneme error (PER)** and silent **24.7% WER / 20.9% PER**;
  50-word vocalized **9.1% WER / 21.4% PER**, silent **11.2% / 22.1%** `[1]`.
- **62 words per minute**, "3.4 times faster than the prior record for any kind of BCI" and
  approaching the ~160 wpm of natural conversation; online with an 80-ms RNN step `[1]`.
- **Anatomy correction:** the arrays were **not in primary motor cortex**. T12 had four 64-electrode
  Utah arrays (256 electrodes) — "two in area 6v (ventral premotor cortex) and two in area 44 (part
  of Broca's area)"; area 44 carried little production information, so decoding used area 6v `[1]`.
- Training data: 260–480 sentences/day (~41 min), **10,850 sentences by the final day**, over
  5 vocalized and 3 silent evaluation days; "140 min per day on average" `[1]`.
- Two mechanism findings that transfer: "spatially intermixed tuning to speech articulators that
  makes accurate decoding possible from only a small region of cortex", and "a detailed
  articulatory representation of phonemes that persists years after paralysis" `[1]`.
- Note the venue split: the *preprint* is what I fetched; the peer-reviewed version is Nature 620,
  1031–1036 (2023).

### 2.2 UC Davis — Card et al., NEJM 2024 (the fastest calibration on record)

Demonstrated, one 45-year-old man with ALS, tetraparesis and severe dysarthria `[2]`:
- **Four microelectrode arrays** in the **left ventral precentral gyrus**, recording from **256
  intracortical electrodes** `[2]`.
- **Day 1 of use (25 days after surgery): 99.6% accuracy on a 50-word vocabulary**, after
  **30 minutes** of cortical recordings while the participant attempted to speak, plus subsequent
  processing `[2]`.
- **Day 2: 90.2% accuracy on a 125,000-word vocabulary**, after **1.4 additional hours** of system
  training `[2]`.
- With further training data, **97.5% accuracy sustained over 8.4 months**, used in self-paced
  conversation at ~**32 words per minute** for **>248 cumulative hours** `[2]`.
- This is the single best existence proof that **calibration cost can be tiny** and that a decoder
  can remain stable for months. It is also the strongest evidence that **an LLM-scale output
  vocabulary is feasible** once the acoustic/articulatory decoder is good enough.

### 2.3 UCSF — Metzger et al., Nature 2023 (multimodal: text + voice + avatar)

Demonstrated using **high-density surface recordings of speech cortex** (ECoG) in a participant with
severe limb and vocal paralysis, trained on **attempted silent speech** `[3]`:
- Implant: **253-channel high-density ECoG** over speech sensorimotor cortex and superior temporal
  gyrus; participant: a 47-year-old woman with anarthria/quadriplegia from a brainstem stroke
  18 years earlier `[3]`.
- Text: **median 78 words per minute, median word error rate 25%** (full text: median **78.3 wpm**,
  **25.5% WER**, **18.5% PER**, **19.9% CER**) on a 1,024-word "General" set of **9,655 sentences**;
  offline scaling to a **39,378-word** vocabulary reached **27.6% median WER** `[3]`.
- Small closed sets were far better: **50-phrase set 4.92% WER at 101 wpm; 529-phrase set 17.1% WER
  at 89.9 wpm** `[3]`.
- Also synthesised intelligible speech audio personalised to the participant's pre-injury voice, and
  animated a facial avatar for speech and non-speech gestures `[3]`.
- "The decoders reached high performance with **less than two weeks of training**"; 13 days of
  collection at ~1.6 h of training data per day `[3]`.

### 2.4 UCSF/Berkeley — Littlejohn et al., Nature Neuroscience 2025 (streaming)

Demonstrated with high-density ECoG in a participant with severe paralysis and anarthria `[4][7]`:
- A **recurrent neural network transducer (RNN-T)** model, the same family used in streaming ASR,
  doing **online** large-vocabulary speech synthesis personalised to the participant's pre-injury
  voice, with **neural decoding in 80-ms increments** `[4]`.
- **First sound out within 1 second** of the detected speech-attempt intent, versus "about an
  8-second delay for a single sentence" in the 2023 system `[7]`; the device "can continuously
  decode speech" without interruption `[4][7]`.
- Accuracy was reported as **the same high level as the previous non-streaming approach**, and the
  model generalised to **26 unseen rare words** (NATO phonetic alphabet) `[7]`.
- **The most transferable single result in this whole report:** the framework "also successfully
  generalized to other silent-speech interfaces, including single-unit recordings and
  **electromyography**" `[4]`. The press release states the same algorithm worked on "non-invasive
  recordings (sEMG) that use sensors on the face" `[7]`. An RNN-T streaming decoder is therefore
  directly reusable for this build.

### 2.5 Stanford — Kunz et al., Cell 2025 (inner speech — the privacy question)

Demonstrated with microelectrode arrays along the **precentral gyrus** of **four participants**
(T12, T15, T16, T17; T12/T15/T17 anarthric or severely dysarthric from ALS, T16 from a pontine
stroke), spanning areas 6v, 4, PEF, 55b, 6d `[5][6]`:
- Inner, perceived and read speech are **all represented in the same precentral regions** as
  attempted speech. T16's *listening* decoded at **92.1% (95% CI 86.4–96.0)** versus **80.0%** for
  attempted vocalized speech; T12's *motoric inner speech* decoded at **72.6% (95% CI 65.7–78.8)**
  versus **97.9%** for attempted vocalized speech (7-word task, Gaussian Naive Bayes, 500 ms) `[5]`.
- Inner speech is "a more weakly modulated version of attempted speech": in the example array,
  "T12-i6v motoric inner speech is about **52%** of attempted speech" in neural distance, while the
  two are separable along a "motor-intent" dimension `[5]`.
- Real-time decoding: an RNN emitting probabilities for **39 phonemes + a silence token every
  80 ms**, trained on **up to 1 hour of cued inner speech combined with previously collected
  attempted-speech data** `[5]`. Online WERs on a **50-word** vocabulary: **24%, 14%, 33%** for
  T12, T15, T16. Online WERs on a **125,000-word** vocabulary (T15, T16): **26% to 54%** `[5]`.
  (The press-release "as high as 74% accuracy" `[6]` is the complement of the best 125k WER, 26% —
  not a separate result. The paper's own "72.6%" is the 7-word T12 figure. Do not quote them as
  the same number.)
- A decoder **trained solely on attempted speech decoded inner speech above chance for all
  participants** `[5]` — i.e. an attempted-speech BCI must actively suppress inner speech.
- Some **uninstructed, free-form inner speech** was decodable during a serial-recall task
  (T12, area i6v), and a **verbal-memory instruction** significantly increased sequence-position
  decoding in all positions `[5]`.
- Defences: attempted vs inner speech are "different enough to be reliably distinguished", so an
  attempted-speech BCI can be trained to ignore inner speech; and an internally spoken **keyword**
  can lock/unlock the decoder, recognised with **>98% accuracy** in the press account `[6]`.
- Author-stated caveat: current systems "are unable to decode free-form inner speech without making
  substantial errors" `[6]`.

### 2.6 Cross-subject transfer — Singh et al., Nature Communications 2025

Using minimally invasive **stereo-EEG (SEEG)** in a large cohort doing a speech motor task, a
sequence-to-sequence model decoded **variable-length phonemic sequences** before and during
articulation. A **cross-subject transfer-learning framework** isolating shared latent manifolds
"significantly outperformed models trained on individual data alone", enabling robustness despite
variable electrode coverage `[8]`. This is the cleanest peer-reviewed evidence that **pretraining
across people/sessions helps**, which matters for one-user data efficiency.

### 2.7 The other companies (verified status)

- **Synchron.** Endovascular **Stentrode** (~**16 electrodes**) in the superior sagittal sinus,
  implanted via the jugular vein. Peer-reviewed first-in-human (2 ALS participants): click-selection
  accuracy **92.63%** and **93.18%** at **13.81** and **20.10 correct characters per minute**,
  unsupervised home use from days 86/71 `[10]`. **SWITCH** (JAMA Neurology 2023, 4 patients,
  12 months): "no serious adverse events and no vessel occlusion or device migration. Mean (SD)
  signal bandwidth was 233 (16) Hz" `[39]`. **COMMAND** results were presented as a CNS 2024
  late-breaking abstract (not NEJM): six participants, "all six patients successfully met the
  primary endpoint of no device-related serious adverse events", median deployment time 20 minutes
  `[40]`. **No Synchron speech-decoding result exists**; it is motor/point-and-click control.
- **Paradromics.** Official Connexus specs: "**421 microelectrodes**, each smaller than a human
  hair, reach **1.5 mm below the brain's surface**"; pre-clinical information transfer rate
  "exceeding **200 bits per second**" `[41]`. FDA **IDE approved November 2025** (Connect-One,
  NCT07357428) `[42]`. First-in-human was a **temporary** implant during epilepsy surgery (2 June
  2025); the first **long-term** implant was announced 17 June 2026, and on 14 Sept 2026 the company
  announced real-time speech/text with that participant `[41][43]`. These are **company
  announcements, not peer-reviewed**; no Paradromics paper was found.
- **Precision Neuroscience.** Layer 7 is a **1,024-channel thin-film cortical array** delivered
  through a micro-slit rather than a craniotomy; a **five-patient pilot** paper was published in
  *Nature Biomedical Engineering* (2026; Epub Oct 2025) `[44]`. FDA **510(k) clearance dated
  17 April 2025** (K242618) covers recording/monitoring/stimulation for "implantation durations of
  up to 30 days", and the company reported testing in **37 patients** at that point `[45]`. No
  published speech-BCI decoding in a chronically paralyzed user; a secondary report of ~80%
  attempted-speech detection with 4 min of training is **(unverified)**.
- **Blackrock Neurotech.** Utah array = **96 channels** (10×10 grid minus corners, 4×4 mm, 1.0–1.5 mm
  long); MoveAgain is the wireless 96-channel system with FDA breakthrough designation (Dec 2021)
  `[46]`. Blackrock arrays are the hardware behind Willett 2023 and Card 2024/2026 `[1][2][52]`.
- **Neuralink.** As above: no peer-reviewed speech result `[11][13][14]`.

### 2.8 Other 2025–2026 peer-reviewed results worth knowing

- **Instantaneous voice synthesis (UC Davis, Nature 2025).** 256 microelectrodes in the ventral
  precentral gyrus of a man with ALS and severe dysarthria; a brain-to-voice prosthesis that
  "instantaneously synthesizes voice with closed-loop audio feedback", including decoded
  paralinguistic features so the participant could change intonation and sing short melodies `[47]`.
  The companion Brain2voice 2.0 preprint attributes **25 ms latency** and a **43.75% perceptual
  WER** to the prior system — **(unverified against the primary paper)** `[48]`.
- **Long-term independent home use (UC Davis, Nature Medicine 2026).** One participant with ALS
  used the 256-electrode BCI "for more than **3,800 h at home** with no researchers present" over
  nearly 2 years; he "communicated **183,060 sentences** — totaling **1,960,163 words** — at an
  average rate of **56 words per minute**", labelled **92%** of sentences "at least mostly
  correctly", and reached "**more than 99% word accuracy (125,000 word vocabulary)**" on formal
  word-reading tests `[52]`. This is the strongest evidence yet that a speech BCI can be a daily
  tool — and that **home use, not lab accuracy, is the right success metric**.
- **Seven-year BCI longevity (UMC Utrecht, NEJM 2024).** A woman with advanced ALS used an implanted
  subdural ECoG BCI at home for **7 years** until "control of the BCI became unreliable… the
  amplitude of neural signals declined, and CT imaging revealed progressive atrophy" `[49]`. A
  click/spelling interface, not speech — but the key warning that **implanted signal quality can
  decay over years**.
- **Mandarin syllable decoding (NeuroXess/Huashan, Science Advances 2025).** 256-channel µECoG;
  "**394 distinct syllables**… median syllable identification accuracy of **71.2%** in a
  single-character reading task", with real-time sentence decoding `[50]`. Evidence that the
  phoneme/syllable-unit approach is language-general, including tonal languages.
- **Click-based ECoG spelling (Johns Hopkins, Communications Medicine 2024).** Median **10.2
  characters/min** with a click detector trained on **<44 min** of data and used **90 days without
  retraining** `[51]`. Relevant as a low-channel fallback and as a calibration-stability datapoint.

**Comparison table (demonstrated only):**

| Group / system | Sensors | Task | Vocab | WER / accuracy | Speed | Calibration | Ref |
|---|---|---|---|---|---|---|---|
| Stanford, 2023 (spiking) | 4×64 Utah, areas 6v + 44 | attempted speech → text | 50 words / 125,000 words | 9.1% / 23.8% WER (vocalized); 11.2% / 24.7% silent | 62 wpm | 10,850 sentences over ~8 days | `[1]` |
| UC Davis, 2024 (spiking) | 256 electrodes, L ventral precentral | attempted speech → text | 50 / 125,000 words | **99.6%** (50 w, day 1); **90.2%** (125k, day 2); **97.5%** over 8.4 months | ~32 wpm self-paced | **30 min** + 1.4 h | `[2]` |
| UC Davis, 2026 (spiking) | same | speech + cursor, **at home** | 125,000 words | **>99%** formal; 92% of sentences "mostly correct" | **56 wpm** avg; 3,800 h | near-daily, unsupervised | `[52]` |
| UC Davis, 2025 (spiking) | 256 µelectrodes, ventral precentral | attempted speech → **voice** | n/r | 43.75% perceptual WER (companion preprint) | 25 ms latency (companion preprint) | — | `[47][48]` |
| UCSF, 2023 (ECoG) | 253-ch high-density surface | attempted silent speech → text/audio/avatar | 1,024-word General; offline 39,378 | **25.5% WER**, 18.5% PER, 19.9% CER | **78.3 wpm** | <2 weeks (~13 days) | `[3]` |
| UCSF, 2025 (ECoG) | 253-ch high-density surface | streaming speech synthesis | 1,024 words | same accuracy as non-streaming | **80-ms increments, <1 s** | — | `[4][7]` |
| Stanford, 2025 (spiking) | 2/4/4/6 Utah, precentral gyrus | **inner** speech → text | 50 words; 125,000 words | 50-w WER **24 / 14 / 33%**; 125k WER **26–54%** | — | up to 1 h inner + prior attempted data | `[5]` |
| UTH/UT Austin, 2025 (SEEG) | stereo-EEG, large cohort | phonemic sequences | open phonemes | cross-subject transfer beats single-subject | — | — | `[8]` |
| Synchron, 2021/2023 | endovascular Stentrode (~16 ch) | click/typing | click commands | 92.63% / 93.18% click accuracy; SWITCH 233 Hz bandwidth | 13.81 / 20.10 correct chars/min | home use day 71–86 | `[10][39]` |
| NeuroXess, 2025 | 256-ch µECoG | Mandarin reading → syllables | 394 syllables | **71.2%** median syllable ID | — | — | `[50]` |
| Utrecht, 2024 | subdural ECoG | click/spelling, at home | letters | — | ~2 letters/min (2016 case) | 7 years of use | `[49]` |

---

## 3. Public datasets, benchmarks and code

The speech-BCI field has released **two clean, permissively licensed single-participant datasets**
and essentially nothing else. Everything from UCSF's Chang lab is request-gated, and most decoder
code has **no licence file**, which legally means all rights reserved.

| Dataset | Year | Modality | Contents | Access | Licence |
|---|---|---|---|---|---|
| Willett T12, *Data for: A high-performance speech neuroprosthesis* | 2023 | Intracortical spikes (Utah arrays) | 1 participant, **12,100 sentences**, 256 electrodes; ~**80.44 GB**; includes an example RNN decoder and language models | Dryad `10.5061/dryad.x69p8czpq` `[26]` | **CC0-1.0** (Dryad API licence field) `[26]` |
| Card T15, *Data for: An accurate and rapidly calibrating speech neuroprosthesis* | 2025 | Intracortical spikes | 1 participant, **10,948 sentences**, 256 electrodes, 45 sessions over 20 months, 512 features at 20-ms bins; ~**11.59 GB** | Dryad `10.5061/dryad.dncjsxm85` `[27]` | **CC0-1.0** (Dryad API licence field) `[27]` |
| Metzger 2023 avatar ECoG | 2023 | ECoG (253 ch) | 1 participant, silent attempted speech; ~82.6 GB | Zenodo `10.5281/zenodo.8200781` `[31]` | **restricted, request access; no open licence stated** `[31]` |
| Littlejohn 2025 streaming | 2025 | ECoG | 1 participant; up to 58.4 h | Harvard Dataverse `10.7910/DVN/8TQKC8` `[32]` | **restricted / request access** `[32]` |
| Gaddy Silent Speech EMG | 2020 | Facial sEMG (8 ch, 1 kHz) | 1 participant, silent + vocalized, open 9,828-word vocab; ~3.9 GB | Zenodo `10.5281/zenodo.4064409` `[19]` | CC-BY-4.0 (per Track 05's Zenodo check) |
| emg2qwerty | 2024 | Wrist sEMG | 108 users, 346 h, 1,135 sessions (typing, not speech) `[21]` | GitHub + Meta `[21]` | **CC-BY-NC-SA-4.0** (Track 05 verified the LICENSE file; the README is wrong) `[21]` |

**Brain-to-Text benchmark.** The '24 edition was organised by Willett/Stanford with the T12 dataset
and hosted the associated competition; the top three entrants **all ensembled decoders and merged
them with a fine-tuned LLM**, and architecture changes (state-space models, transformers) did not
beat the RNN baseline `[9][28]`. The '25 edition moved to the **Card/UC Davis T15 dataset** and was
hosted on Kaggle (CC0-1.0 data); per the delegated sub-search, the '25 baseline was **6.70% WER** on
a held-out test set, and the competitive lessons repeated (fine-tuned LLM rescoring wins)
`[9][27][29]`. **Organiser attribution matters if you cite the benchmark** — B2T '24 is Stanford,
B2T '25 is UC Davis/BrainGate, not Willett and not Bern `[28][29]`.

**Code licences are the trap.** The Stanford baseline (`fwillett/speechBCI`) and the UC Davis
baseline (`Neuroprosthetics-Lab/nejm-brain-to-text`) have **no LICENSE file** at the paths checked,
so they are **not** open-source for reuse by default `[30][33]`. The clean one among the speech
decoders is `dgaddy/silent_speech`, which is **MIT** `[34]`. If you want to
reuse an invasive decoder baseline, read the licence first; absence of a licence is not permission.

**Can BCI/neural data pretrain an sEMG phoneme decoder? No published evidence, and no paired data.**
The full argument and its one supportive-but-upper-limb counterexample (Rizzoglio et al. `[38]`) are
in 4.2. In short: no paired spike + sEMG speech corpus exists; the two signals are different
processes (population spikes vs tissue-filtered motor-unit interference that must be decomposed
`[35]`); and the existing EMG foundation models pretrain on EMG or audio, never spikes
`[18][20][23]`. The natural bridge is a **shared label space, not shared weights**: 39 ARPAbet-style
phones + silence `[1][5]`, plus articulatory-kinematics corpora — **USC-TIMIT** (rtMRI + EMA + audio,
10 rtMRI speakers / 4 EMA, 460 sentences, CC-BY-4.0) and **CMUdict** (unrestricted commercial use)
`[36][37]`.

**Verdict for the build:** use the T12/T15 CC0 datasets to **learn decoder architectures and LM
stacking**, and USC-TIMIT/CMUdict/phoneme inventories to define the shared output space. Do not
attempt to transfer spike weights to sEMG.

---

## 4. What actually transfers to a surface-EMG silent-speech build

The dividing line: **decoder topology, output units, LM stack, calibration/drift protocol and UX
transfer; anatomy, front-end signal and pretrained weights do not.**

### 4.1 Transfer that is real (algorithmic and protocol-level)

1. **Streaming RNN-T decoders, already validated on sEMG.** The 2025 UCSF streaming model used a
   recurrent neural network transducer with **80-ms decode increments**, produced first sound within
   **1 second**, could "continuously decode speech indefinitely", and "also successfully generalized
   to other silent-speech interfaces, including single-unit recordings and **electromyography**"
   `[4][7]`. This is the strongest direct transfer in the report: a causal, chunked, autoregressive
   decoder with an explicit **speech-attempt detector** that gates output is the default real-time
   architecture to copy.
2. **Decode sub-word units, not words.** Every high-data-efficiency invasive system decodes
   **phonemes**: Willett's RNN "converts a time series of this neural activity into a time series of
   probabilities for each phoneme (plus … 'silence' … and 'blank')", at 80-ms steps `[1]`; Card
   predicts "the most likely English phoneme being attempted" every 80 ms `[2]`; the inner-speech
   model outputs "probabilities for **39 phonemes and a silence token every 80 ms**" `[5]`. Willett's
   phoneme error was **19.7% vocalized vs 20.9% silent**, and the paper reports a preserved
   articulatory code ("the correlation between electromagnetic articulography (EMA) and neural data
   was 0.61") `[1]`. For one user, a **phoneme/articulatory-feature CTC head plus a language model**
   is the defensible choice; words belong to the LM.
3. **Use an LLM to rescore an ensemble — this is where the last WER points came from.** All three
   top Brain-to-Text '24 entrants merged multiple decoder outputs with a **fine-tuned LLM** `[9]`.
   On the non-invasive side, MONA LISA took silent-EMG WER from **28.8% → 12.2%** (vocal EMG
   **23.3% → 3.7%**) using cross-modal alignment plus "LLM Integrated Scoring Adjustment", and also
   improved the Brain-to-Text 2024 top WER "from 9.8% to 8.9%" `[20]`. Card et al. applied "two
   further open-source language models" after the word decoder, reaching **9.8% WER on day 2** and
   **2.5% (95% CI 1.0–4.5) by session 15** `[2]`. Willett reports that "an improved language model
   could decrease word error rates from 23.8 to 17.4%, and … testing on more proximal sentences
   further decreased word error rates to 11.8%" `[1]`. Budget an LM/LLM stage from day one.
4. **The language model is what buys vocabulary size.** UC Davis went from a 50-word to a
   125,000-word vocabulary between day 1 and day 2 on **1.4 h** more data `[2]`; the acoustic model
   barely changed. Plan "phonemes first, words via LM".
5. **Calibration can be 30 minutes; personalisation can be 3.** Card et al. reached 99.6% on 50
   words "following 30 minutes of collection of cortical recordings and processing" (213 sentences),
   then 9.8% WER on 125k after 1.4 h more (260 sentences) `[2]`. On sEMG, **3 minutes** of
   target-subject calibration reached 20.5% CER / 31.7% WER with no significant difference from a
   ~13-minute pool `[18]`. Bootstrap with a standard prompt set, then keep the calibration short.
6. **Plan for drift at three timescales, and prefer target inference over distribution matching.**
   Willett used "unique input layers for each day … and rolling feature adaptation to account for
   within-day changes" `[1]`; Card combined "data from multiple days … to continuously calibrate the
   decoder", sustained **97.5% accuracy through session 84 (>8 months)**, and fed "correctly decoded
   sentences … to fine-tune the neural decoder online" `[2]`. Wilson et al. (2026) use a **hidden
   Markov model to infer intended targets** and retrain on them, beating distribution-alignment
   methods in 2-month simulations, a 1-month human closed loop, and a 5-year offline dataset; the
   distribution-matching baselines "appear to accumulate compounding errors over time" `[22]`. The
   sEMG analogue of "target inference" is **confidence-gated self-training on the user's own
   accepted output**.
7. **Inner speech is a weaker copy of attempted speech, and must be gated.** Kunz et al. show the
   two share a subspace with inner speech at ~**52%** modulation, that a merely-attempted-speech
   decoder already reads inner speech above chance, and that a **keyword lock/unlock** plus a
   motor-intent dimension can suppress it `[5][6]`. Transfer the *design*: an always-on silent
   interface needs an explicit **arm/unlock gesture** and a **null/ignore class**, not just a
   classifier.
8. **Cross-subject pretraining works — within a modality.** Singh et al. (SEEG) show a group-derived
   decoder "significantly outperformed models trained on individual data alone" `[8]`; sEMG
   multi-subject pretraining + target fine-tuning reached **21.7% CER** versus **44.9% CER** from
   random init, and **74.4% → 21.7%** macro CER going from 1 to 26 pretraining participants `[18]`.
   For a one-user project this is the highest-leverage trick: accumulate **your own** data, but
   initialise from public multi-user checkpoints.
9. **Attempted/mouthed speech is nearly as good as vocalized.** Willett: 50-word WER **9.1%
   vocalized vs 11.2% silent**, 125k **23.8% vs 24.7%**, phoneme error **19.7% vs 20.9%** `[1]`.
   This is the single most important scoping result for the owner: build a **mouthed/attempted**
   interface first; do not start with pure inner speech.
10. **Copy the error-correction UX verbatim.** Card et al.'s participant used on-screen
    correctness buttons ("100% correct", "mostly correct", "incorrect"), a **letter-by-letter
    spelling mode for out-of-vocabulary words** (proper nouns), a **6-second inactivity
    auto-finalizer**, and an optional manual finalize button `[2]`. For character-level sEMG,
    backspace-aware beam search is mandatory because deleting characters corrupts LM state `[21]`.
11. **sEMG is pre-emptive, so the latency budget is generous.** sEMG "precedes the onset of the
    corresponding motion by tens of milliseconds", giving "the potential to detect activity with
    negative latency" `[21][24]`. A few hundred ms of algorithmic latency is therefore invisible to
    the wearer if the attempt detector fires early.
12. **On-device inference is already demonstrated for sEMG commands.** SilentWear runs a
    15k-parameter CNN on a multi-core MCU at **63.9 µJ/inference, 2.47 ms latency, 20.5 mW** total
    and >**27 h** of continuous operation `[23]`. The open-vocabulary decoder stays off-device.

### 4.2 Transfer that is fake or unproven

- **Anatomy and signal — the "similar positioning" claim is false.** N1 threads sit **inside motor
  cortex** and record single-neuron spikes over a 3 Hz–27 kHz band across 1,000+ channels `[13]`;
  this build's electrodes sit **on the skin over facial/neck muscles** and record summed motor-unit
  action potentials. The channel count, sampling rate, noise model, units and tissue interface are
  all different. You cannot import a spiking-cortex decoder into sEMG; only the *decoder topology
  around* the front end transfers.
- **The Neuralink "speech" milestone is not speech decoding.** The third participant's restoration
  was cursor typing plus an AI-synthesised copy of his pre-illness voice `[11]`. It says nothing
  about decoding attempted or silent speech, and Neuralink has published no WER, vocabulary or wpm
  figure of any kind.
- **125,000-word vocabularies do not read across to sEMG.** The large open vocabularies were
  reached with intracortical/ECoG signals at far higher information rates. The best demonstrated
  **non-invasive silent-EMG open-vocabulary** figure found is MONA LISA's **12.2% WER** (vocal EMG
  3.7%), and it depends on LLM rescoring plus cross-modal training `[20]`. Do not transfer the BCI
  vocabulary numbers.
- **Zero-shot cross-user sEMG models are unusable.** The 108-user emg2qwerty model has "over 50%
  character error rate" on a new user without personalisation `[21]`; the multi-subject 2026 study
  is the first to make a *closed 50-sentence* corpus work at ~22% CER `[18]`. Personal data is not
  optional.
- **Cross-modal alignment is not free.** MONA LISA's contrastive losses only helped with parallel
  EMG/audio data plus DTW targets; its attempt at an unsupervised EMG↔LibriSpeech contrastive loss
  (supTcon) produced "a modest performance degradation in all models" `[20]`. Treat cross-modal
  pretraining as an ablation, not a default.
- **Can BCI/neural data pretrain an EMG phoneme decoder?** The evidence says **no direct weight
  transfer, and the useful bridge is elsewhere**. (a) Spikes and sEMG have incompatible statistics:
  one is a set of single/multi-unit action-potential event trains sampled at tens of kHz from inside
  cortex `[13]`; the other is tissue-filtered interference of many motor-unit action potentials with
  crosstalk, from which recovering motor-unit spike trains requires **decomposition** `[35]`.
  (b) The peer-reviewed cross-modal results point from **sEMG toward speech/audio models**, not
  toward spikes: Gowda et al. show self-supervised speech (S3) representations are "strongly
  linearly related to the electrical power of muscle activity" (**r = 0.85**) and that EMG power
  vectors for different articulatory gestures form "structured, separable clusters", letting them
  map EMG into S3 space and synthesise speech for a participant with ALS who silently articulated
  `[16]`; Gowda & Miller decode **silent** sEMG to text "at the phonemic level" with a
  sequence-to-sequence model that needs no time-aligned audio `[17]`. (c) Cross-subject transfer
  *within* a neural modality is proven (`[8]`), and cross-subject transfer *within* sEMG is proven
  (`[18]`), but I found **no paper in which a model pretrained on intracortical data improved a
  surface-EMG decoder**. The one supportive-looking result runs the other way and is not speech:
  human intracortical spikes were used to **predict monkey EMG** (EMG as decoder *output*), with a
  monkey-trained EMG decoder transferred to a human after CCA alignment of latent signals `[38]`.
  The defensible move is therefore to pretrain on **audio speech representations, other users'
  sEMG, and synthetic/self-supervised targets** — not on BCI recordings. This is a negative result
  from a deliberate search, not proof that it is impossible; the shared thing that *could* work is a
  common **phoneme/articulatory label space**, which is a data-alignment project, not a
  weight-transfer project.

### 4.3 The target-side numbers to beat (sEMG, not BCI)

Read these as the realistic envelope for this build, and do not confuse them with the BCI table in
Section 2:
- Multi-subject sEMG pretraining, **27 participants**, each with "less than 0.5 h of data (21.3 min
  on average)" of Aloud + Mimed speech, closed 50-sentence corpus: **21.7% CER / 31.9% WER** after
  target fine-tuning, versus **49.3% CER** with no target calibration and **68.0% CER** for direct
  checkpoint fine-tuning `[18]`.
- **Three minutes** of target-subject calibration reached **20.5% CER / 31.7% WER**, with "no
  statistically significant difference from the full approximately 13-min pool" `[18]`.
- Macro-averaged CER fell from **74.4%** with 1 pretraining participant to **21.7%** with 26 `[18]`.
- **Leakage warning:** excluding the five evaluation sentences from all sEMG training data raised
  CER/ WER to **78.6% / 99.9%** in that study `[18]`. Any single-user pipeline must report this.

---

## 4b. What to copy from speech BCIs — concrete design/ML decisions

Each line names the invasive result it comes from; details and caveats are in 4.1.

1. **Output: 39 phonemes + silence + CTC blank, 80-ms steps** `[1][2][5]`. No word classifier.
2. **Front end:** 8-ms frames / 32-ms log-spectral features → temporal-depthwise-separable ConvNet,
   ~1 s receptive field, CTC; a 15k-parameter version already runs on an MCU `[21][23]`.
3. **Streaming: causal RNN-T or chunked causal CTC**, trained with ~900 ms past / ~100 ms future
   context, deployed causal-only; an RNN-T is the one decoder already validated on sEMG `[4][7][21]`.
4. **A separate speech-attempt detector gates the decoder**, as in the streaming neuroprosthesis
   `[4]`; this is what suppresses chewing, swallowing and inner monologue `[5]`.
5. **LM from day one, LLM rescoring of an ensemble as soon as there is a beam** `[9][20]`.
6. **Backspace-aware beam search** so deletions do not corrupt LM state `[21]`.
7. **v1 decodes attempted/mouthed speech, not pure inner speech**: mouthed costs ~2 WER points
   versus vocalized, inner speech ~25 accuracy points `[1][5]`.
8. **Explicit lock/unlock** (keyword or distinct motor act) plus a null class `[5][6]`.
9. **Initialise from a multi-subject checkpoint**, then fine-tune on the owner (21.7% vs 44.9% CER;
   5/27 folds failed from random init) `[18]`.
10. **≤3-minute per-session calibration, ~30-minute bootstrap** `[2][18]`.
11. **Continuous adaptation:** day-specific input layers + rolling within-day adaptation `[1]`,
    online fine-tuning on accepted output `[2]`, target-inference rather than distribution matching
    for long-term drift `[22]`.
12. **Re-donning robustness as a feature:** rotation augmentation (electrode permute ±1),
    rotation-invariance module, ~60 ms temporal jitter `[21]`; without it silent accuracy fell
    **77.5% → 59.3%** across sessions `[23]`.
13. **Explicit correction UX** — self-report buttons, letter-spelling OOV fallback, 6-s inactivity
    finalizer, online fine-tune on correct sentences `[2]`.
14. **Leakage-controlled evaluation.** Removing evaluation sentences from training changed
    21.7%/31.9% CER/WER to **78.6%/99.9%** `[18]`; a one-user project is maximally exposed to this.

## 4c. Latency, correction UX, and privacy

- **Latency.** The invasive budget is an **80-ms decode increment**, first sound **<1 s**, continuous
  streaming `[4][7]`. sEMG is **pre-emptive** — muscle activity "precedes the onset of the
  corresponding motion by tens of milliseconds", permitting "negative latency" `[21][24]` — and
  on-device command inference is already at **2.47 ms**, **63.9 µJ**, **20.5 mW** for a 15k-parameter
  CNN `[23]`. Run the CTC decoder causally on-device at 80-ms cadence; let LM/LLM rescoring lag on a
  phone/PC and patch the displayed sentence when it arrives.
- **Correction UX.** Copy Card et al. `[2]`: "**100% correct / mostly correct / incorrect**"
  self-report buttons; a **letter-by-letter spelling fallback** for out-of-vocabulary items; a
  **6-second inactivity auto-finaliser**; and online fine-tuning on accepted sentences. Add
  **backspace-aware** LM state updates `[21]`, a visible beam/alternatives list, and an LLM repair
  pass `[20]`. Track the **uncorrected error rate** (mobile-typing anchor: **2.3%**) `[21]`.
- **Privacy.** A decoder trained **only on attempted speech** still reads inner speech above chance
  in every participant tested `[5]`, so suppression is an active requirement: an **internally spoken
  keyword** lock (>98%) `[6]`, a motor-intent dimension that separates attempted from inner speech
  `[5]`, and a hard gate requiring an attempted-articulation signal. On sEMG the risk is smaller but
  real — residual muscle activity during imagined two-syllable speech is decodable above chance `[25]`.

---

## Sources

*(Numbered list. All URLs below were fetched in this session — by me or by a delegated
sub-search — and the numbers quoted are from the fetched page unless marked unverified.)*

1. F. R. Willett et al., *A high-performance speech neuroprosthesis*, bioRxiv preprint (2023),
   https://www.biorxiv.org/content/10.1101/2023.01.21.524489v2 (peer-reviewed version: Nature 620,
   1031–1036, 2023).
2. N. S. Card et al., *An Accurate and Rapidly Calibrating Speech Neuroprosthesis*, N Engl J Med
   2024;391(7):609–618, https://doi.org/10.1056/NEJMoa2314132 (abstract fetched via Europe PMC,
   PMID 39141853).
3. S. L. Metzger et al., *A high-performance neuroprosthesis for speech decoding and avatar
   control*, Nature 620, 1037–1046 (2023), https://doi.org/10.1038/s41586-023-06443-4 (abstract
   fetched via Europe PMC, PMID 37612505).
4. K. T. Littlejohn et al., *A streaming brain-to-voice neuroprosthesis to restore naturalistic
   communication*, Nature Neuroscience 28, 902–912 (2025),
   https://doi.org/10.1038/s41593-025-01905-6 (abstract fetched via Europe PMC, PMID 40164740).
5. E. M. Kunz et al., *Inner speech in motor cortex and implications for speech neuroprostheses*,
   Cell (2025), https://doi.org/10.1016/j.cell.2025.06.015 (metadata fetched via Europe PMC,
   PMID 40816265).
6. Cell Press / EurekAlert, *Brain-computer interface could decode inner speech in real time*,
   14 Aug 2025, https://www.eurekalert.org/news-releases/1093888.
7. UC Berkeley / EurekAlert, *Brain-to-voice neuroprosthesis restores naturalistic speech*,
   31 Mar 2025, https://www.eurekalert.org/news-releases/1078701.
8. A. Singh et al., *Transfer learning via distributed brain recordings enables reliable speech
   decoding*, Nature Communications 16, 8749 (2025),
   https://doi.org/10.1038/s41467-025-63825-0 (abstract fetched via Europe PMC, PMID 41034198).
9. F. R. Willett et al., *Brain-to-Text Benchmark '24: Lessons Learned*, arXiv:2412.17227 (2024),
   https://arxiv.org/abs/2412.17227.
10. T. J. Oxley et al., *Motor neuroprosthesis implanted with neurointerventional surgery improves
    capacity for activities of daily living tasks in severe paralysis: first in-human experience*,
    J NeuroIntervent Surg 13(2):102–108 (2021), https://doi.org/10.1136/neurintsurg-2020-016862
    (abstract fetched via Europe PMC, PMID 33115813).
11. Teslarati, *Neuralink device gets FDA recognition for speech restoration*, 2 May 2025,
    https://www.teslarati.com/neuralink-speech-restoration-fda-breakthrough/.
12. Interesting Engineering, *Mind over machine: Neuralink's breakthrough lets patient control
    robot with thoughts*, 11 Oct 2025,
    https://interestingengineering.com/innovation/neuralinks-patient-control-robot-with-thoughts.
13. E. Musk and Neuralink, *An Integrated Brain-Machine Interface Platform With Thousands of
    Channels*, J Med Internet Res 2019;21(10):e16194, https://www.jmir.org/2019/10/E16194/ ;
    PDF read via mirror: https://tweakers.net/files/upload/Neuralink-White-Paper.pdf
    (JMIR HTML returned HTTP 202 with an empty body; the PDF was downloaded and text-extracted, so
    the specs quoted above are from the white paper itself).
14. Neuralink, *PRIME Study Brochure* (PDF),
    https://neuralink.com/pdfs/PRIME-Study-Brochure.pdf.
15. The Next Web, *Neuralink finally has a real rival: Paradromics just put a brain chip in its
    first patient*, https://thenextweb.com/news/paradromics-first-clinical-brain-chip-implant-speech
    (article body truncated on fetch).
16. H. T. Gowda, D. C. Comstock, L. M. Miller, *emg2speech: Synthesizing speech from
    electromyography using self-supervised speech models*, arXiv:2510.23969 (v2, 2026),
    https://arxiv.org/abs/2510.23969.
17. H. T. Gowda, L. M. Miller, *Non-invasive electromyographic speech neuroprosthesis: a geometric
    perspective*, arXiv:2502.05762 (v3, 2026), https://arxiv.org/abs/2502.05762.
18. C. Le, B. Fumagalli, Y. Esmaeili, X. Chen, T. He, N. Emami, A. Flinker, Y. Wang,
    *Multi-Subject Pretraining Enables Short-Calibration Personalization for Closed-Corpus Surface
    EMG Speech Decoding*, arXiv:2609.21288 (2026), https://arxiv.org/abs/2609.21288.
19. D. Gaddy, D. Klein, *Digital Voicing of Silent Speech*, Proceedings of EMNLP 2020, pp.
    5521–5530, https://aclanthology.org/2020.emnlp-main.445/.
20. T. Benster, G. Wilson, R. Elisha, F. R. Willett, S. Druckmann, *A Cross-Modal Approach to
    Silent Speech with LLM-Enhanced Recognition* (MONA LISA), arXiv:2403.05583 (2024),
    https://arxiv.org/abs/2403.05583 (abstract fetched directly; the full WER ladder was read from
    https://ar5iv.labs.arxiv.org/html/2403.05583 via the delegated sub-search).
21. V. Sivakumar et al., *emg2qwerty: A Large Dataset with Baselines for Touch Typing using Surface
    Electromyography*, NeurIPS 2024 Datasets and Benchmarks, arXiv:2410.20081,
    https://arxiv.org/abs/2410.20081 (abstract fetched directly; full-text details such as the
    900 ms/100 ms context split, backspace-aware decoder, rotation augmentation and the 2.3%
    uncorrected-error anchor were read from https://ar5iv.labs.arxiv.org/html/2410.20081 via the
    delegated sub-search).
22. G. H. Wilson et al., *Long-term unsupervised recalibration of cursor-based intracortical
    brain-computer interfaces using a hidden Markov model*, Nature Biomedical Engineering 10,
    1466–1484 (2026), https://doi.org/10.1038/s41551-025-01536-z (abstract fetched via Europe PMC,
    PMID 41361599).
23. G. Spacone et al., *SilentWear: an Ultra-Low Power Wearable System for EMG-based Silent Speech
    Recognition*, arXiv:2603.02847 (2026), https://arxiv.org/abs/2603.02847.
24. K. Xu et al., *Silent Speech Interfaces in the Era of Large Language Models: A Comprehensive
    Taxonomy and Systematic Review*, arXiv:2603.11877 (2026), https://arxiv.org/abs/2603.11877
    (abstract fetched directly; the 60 ms electromechanical-delay quote came from
    https://ar5iv.labs.arxiv.org/html/2603.11877 via the delegated sub-search).
25. K. Bhadra, A.-L. Giraud, S. Marchesotti, *Learning to operate an imagined speech Brain-Computer
    Interface involves the spatial and frequency tuning of neural activity*, Communications Biology
    8, 271 (2025), https://doi.org/10.1038/s42003-025-07464-7 (PDF fetched via HAL).
26. Dryad, F. Willett et al., *Data for: A high-performance speech neuroprosthesis* (2023),
    https://doi.org/10.5061/dryad.x69p8czpq (Dryad API fetched: licence **CC0-1.0**, storage
    80,440,635,830 bytes, version 9, 12,100 sentences).
27. Dryad, N. Card et al., *Data for: An accurate and rapidly calibrating speech neuroprosthesis*
    (2025), https://doi.org/10.5061/dryad.dncjsxm85 (Dryad API fetched: licence **CC0-1.0**, storage
    11,594,901,567 bytes, version 5).
28. EvalAI, *Brain-to-Text Benchmark '24* challenge page 2099,
    https://eval.ai/web/challenges/challenge-page/2099/overview (fetched by the delegated
    sub-search).
29. Kaggle, *Brain-to-text '25* competition, https://www.kaggle.com/competitions/brain-to-text-25/
    (fetched by the delegated sub-search; data terms CC0-1.0).
30. GitHub, fwillett/speechBCI, https://github.com/fwillett/speechBCI (checked by the delegated
    sub-search: **no LICENSE file**).
31. Zenodo, *Dataset for "A high-performance neuroprosthesis for speech decoding and avatar
    control"* (2023), https://doi.org/10.5281/zenodo.8200781 (restricted, request access; checked by
    the delegated sub-search).
32. Harvard Dataverse, K. T. Littlejohn et al. (2025), https://doi.org/10.7910/DVN/8TQKC8
    (restricted, request access; checked by the delegated sub-search).
33. GitHub, Neuroprosthetics-Lab/nejm-brain-to-text,
    https://github.com/Neuroprosthetics-Lab/nejm-brain-to-text (checked by the delegated
    sub-search: **no LICENSE file**).
34. GitHub, dgaddy/silent_speech, https://github.com/dgaddy/silent_speech (checked by the delegated
    sub-search: **MIT**).
35. D. Farina, R. Merletti, R. M. Enoka, *The extraction of neural strategies from the surface EMG:
    2004–2024*, J Appl Physiol 138:121–135 (2025), https://doi.org/10.1152/japplphysiol.00453.2024
    (fetched by the delegated sub-search).
36. USC SAIL, *USC-TIMIT* (rtMRI + EMA + audio), Zenodo (2026),
    https://doi.org/10.5281/zenodo.19422914 (licence CC-BY-4.0 per the Zenodo API, fetched by the
    delegated sub-search).
37. CMU Sphinx, *cmudict* (ARPAbet pronouncing dictionary), https://github.com/cmusphinx/cmudict
    (LICENSE + README checked by the delegated sub-search: "any research or commercial purpose is
    completely unrestricted").
38. F. Rizzoglio et al., *From monkeys to humans: observation-based EMG brain-computer interface
    decoders for humans with paralysis*, J Neural Eng 20:056020 (2023),
    https://doi.org/10.1088/1741-2552/ad038e (abstract fetched via Europe PMC, PMID 37844567).
39. P. Mitchell et al., *Assessment of Safety of a Fully Implanted Endovascular Brain-Computer
    Interface for Severe Paralysis in 4 Patients: The SWITCH Study*, JAMA Neurology
    80(3):270–278 (2023), https://doi.org/10.1001/jamaneurol.2022.4847 (abstract fetched by the
    delegated sub-search, PMID 36622685).
40. Synchron / Business Wire, *Synchron Announces Positive Results from U.S. COMMAND Study of
    Endovascular BCI*, 30 Sept 2024 (CNS 2024 abstract LB009),
    https://cardiacvascularnews.com/synchron-announces-positive-results-from-u-s-command-study-of-endovascular-brain-computer-interface/
    (fetched by the delegated sub-search).
41. Paradromics, *Connexus* product page, https://paradromics.com/connexus/ (fetched by the
    delegated sub-search).
42. ClinicalTrials.gov, *Connect-One* EFS, NCT07357428, https://clinicaltrials.gov/study/NCT07357428
    (fetched by the delegated sub-search).
43. Paradromics, *Paradromics Achieves Real-Time Speech with Connexus BCI*, 14 Sept 2026,
    https://paradromics.com/news/paradromics-achieves-real-time-speech-connexus-brain-computer-interface/
    (fetched by the delegated sub-search).
44. M. Hettick et al., *Minimally invasive implantation of scalable high-density cortical
    microelectrode arrays for multimodal neural decoding and stimulation*, Nature Biomedical
    Engineering 10(6):1206–1221 (2026), https://doi.org/10.1038/s41551-025-01501-w (fetched by the
    delegated sub-search, PMID 41039113).
45. Precision Neuroscience, *Precision Neuroscience Receives FDA Clearance for High-Resolution
    Cortical Electrode Array*, 17 Apr 2025 (K242618),
    https://www.precisionneuro.io/articles/company-news/precision-neuroscience-receives-fda-clearance-for-high-resolution-cortical-electrode-array
    (fetched by the delegated sub-search).
46. BCI.INTEL device database, *Utah Array (NeuroPort Electrode 96)* and *MoveAgain*,
    https://bciintel.com/devices/blackrock-utah-array/ and
    https://bciintel.com/devices/blackrock-moveagain/ (secondary database; fetched by the delegated
    sub-search).
47. M. Wairagkar et al., *An instantaneous voice-synthesis neuroprosthesis*, Nature
    644(8075):145–152 (2025), https://doi.org/10.1038/s41586-025-09127-3 (abstract fetched via
    Europe PMC).
48. M. Wairagkar et al., *Brain2voice 2.0: High-performance voice synthesis brain-computer
    interface*, bioRxiv preprint (2026), https://doi.org/10.64898/2026.06.30.735633 (source of the
    25 ms latency and 43.75% perceptual WER; fetched by the delegated sub-search — **unverified
    against the primary Nature paper**).
49. M. J. Vansteensel et al., *Longevity of a Brain-Computer Interface for Amyotrophic Lateral
    Sclerosis*, N Engl J Med 391(7):619–626 (2024), https://doi.org/10.1056/NEJMoa2314598 (fetched
    by the delegated sub-search, PMID 39141854).
50. Y. Qian et al., *Real-time decoding of full-spectrum Chinese using brain-computer interface*,
    Science Advances 11(45):eadz9968 (2025), https://doi.org/10.1126/sciadv.adz9968 (abstract
    fetched via Europe PMC).
51. D. N. Candrea et al., *A click-based electrocorticographic brain-computer interface enables
    long-term high-performance switch scan spelling*, Communications Medicine 4(1):207 (2024),
    https://doi.org/10.1038/s43856-024-00635-3 (fetched by the delegated sub-search,
    PMID 39433597).
52. N. S. Card et al., *Long-term independent use of an intracortical brain-computer interface for
    speech and cursor control*, Nature Medicine 32(7):2504–2510 (2026),
    https://doi.org/10.1038/s41591-026-04414-6 (abstract fetched via Europe PMC, PMID 42297978).
53. S. D. Stavisky, *Restoring Speech Using Brain-Computer Interfaces*, Annual Review of Biomedical
    Engineering 27(1):29–54 (2025), https://doi.org/10.1146/annurev-bioeng-110122-012818 (fetched by
    the delegated sub-search, PMID 39745941).
54. ClinicalTrials.gov, *PRIME* (Precise Robotically IMplanted Brain-Computer InterfacE),
    NCT06429735, https://clinicaltrials.gov/study/NCT06429735 (fetched via the ClinicalTrials.gov
    API v2: start 2024-01-09, estimated enrolment 15, ages 22–75, primary endpoints device- and
    procedure-related adverse events).
55. ClinicalTrials.gov, *Control of Assistive Devices Via Brain-Computer Interface Technology*
    (CONVOY), NCT06710626, https://clinicaltrials.gov/study/NCT06710626 (fetched via the API v2:
    start 2024-11-25, estimated enrolment 3).
56. ClinicalTrials.gov, *VOICE: An Early Feasibility Study of a Precise Robotically Implanted
    Brain-Computer Interface for Communication Restoration*, NCT07224256,
    https://clinicaltrials.gov/study/NCT07224256 (fetched via the API v2: start 2025-10-03,
    estimated enrolment 6, ages 22–75).
57. Neuralink, *Updates* (company blog: PRIME progress updates, MindPong, datarepo),
    https://neuralink.com/updates/ (fetched by the delegated sub-search; the public page is
    JavaScript-rendered so I could retrieve only the title directly).
58. WIRED, *Elon Musk's Neuralink has a monkey-death problem* (investigation),
    https://www.wired.com/story/elon-musk-pcrm-neuralink-monkey-deaths/ (fetched by the delegated
    sub-search; the DOT-probe reporting used was Ars Technica,
    https://arstechnica.com/science/2023/02/feds-probing-neuralink-for-allegedly-transporting-pathogens-on-brain-hardware/).
59. Reuters via The Star, *Elon Musk's Neuralink says it has 21 participants enrolled in trials*,
    29 Jan 2026, https://www.thestar.com.my/tech/tech-news/2026/01/29/elon-musk039s-neuralink-says-it-has-21-participants-enrolled-in-trials
    (fetched by the delegated sub-search).
60. The Star, *Neuralink device helps monkey see something that's not there*, 16 June 2025,
    https://www.thestar.com.my/tech/tech-news/2025/06/16/neuralink-device-helps-monkey-see-something-thats-not-there
    (fetched by the delegated sub-search).
61. A. Sawyer et al., BCI-society workshop summary, J Neural Eng (2026),
    https://doi.org/10.1088/1741-2552/ae9eee (co-authored by a Neuralink employee; fetched by the
    delegated sub-search).

## Key takeaways for the build

1. **Anatomy, not similarity.** N1 is in motor cortex and reads spikes; this build reads facial/neck
   muscle sEMG through skin. "Similar positioning" is false for both electrode and signal `[13]`.
   Only decoder topology, output units, protocol and UX transfer.
2. **Neuralink has no peer-reviewed speech result.** Its 2025 "speech" milestone is cursor typing +
   AI voice cloning `[11]`; it publishes no dataset, code or WER. Plan around zero Neuralink
   dependency.
3. **The speech-BCI numbers to know:** Willett 2023 — **62 wpm, 9.1% WER (50 words), 23.8% WER
   (125k words)** from spikes in areas 6v/44 `[1]`; Card 2024 — **99.6% on 50 words after 30 min,
   90.2% on 125k after 1.4 h, 97.5% sustained 8.4 months, ~32 wpm** `[2]`; Card 2026 — **56 wpm
   average, 3,800 h of unsupervised home use, >99% word accuracy (125k)** `[52]`; Metzger 2023 —
   **78.3 wpm, 25.5% median WER** from ECoG `[3]`; Wairagkar 2025 — **instantaneous voice synthesis,
   25 ms latency** (companion preprint) `[47][48]`; Littlejohn 2025 — **80-ms streaming, <1 s
   latency, and the same model worked on sEMG** `[4][7]`; Kunz 2025 — inner speech decodeable but
   weaker (**72.6% vs 97.9%** on a 7-word set; **26–54% WER** on 125k) `[5]`.
4. **Copy the streaming RNN-T plus an attempt detector.** It is the one architecture already
   validated across ECoG, single units and sEMG `[4][7]`, and it gives the build its latency budget.
5. **Output phonemes (≈39 + silence + blank) at 80 ms, and let an LM/LLM supply the words.**
   Sub-word units plus LM is the shared data-efficient design across invasive and sEMG systems
   `[1][2][5][21]`; LLM rescoring/ensembling bought 28.8%→12.2% on silent sEMG `[20]`.
6. **Build attempted/mouthed speech first, not inner speech.** Mouthed costs only ~2 WER points vs
   vocalized `[1]`; inner speech is a ~52%-magnitude signal and much worse `[5]`. The owner's
   "barely different" face constraint is compatible with mouthed micro-articulation; strict
   thought-only is not where to start.
7. **One user can be data-efficient with pretraining + 3-minute calibration.** Multi-subject
   checkpoint init + target fine-tune gave 21.7% CER vs 44.9% from scratch `[18]`; 3 min matched
   ~13 min of calibration `[18]`; 30 min bootstrapped a 50-word 99.6% decoder in the invasive case
   `[2]`.
8. **Plan for drift and re-donning as the main engineering risk.** Day-specific input layers and
   rolling adaptation `[1]`, online fine-tune on accepted output `[2]`, and target-inference
   adaptation rather than distribution matching `[22]`. Silent inter-session accuracy can drop from
   77.5% to 59.3% without rotation augmentation/invariance `[23]`.
9. **An always-on silent interface needs an explicit lock.** A decoder trained only on attempted
   speech still reads inner speech above chance `[5]`; use a keyword/motor-act unlock and a
   null class `[5][6]`.
10. **Do not plan to pretrain an EMG decoder on BCI data.** No such transfer was found; the proven
    cross-modal bridges go **sEMG → self-supervised speech/audio spaces** (EMG power vs S3 features
    r = 0.85 `[16]`; MONA LISA/LibriSpeech `[20]`) and **sEMG → other users' sEMG** `[18]`.
    Behavioural/articulatory label spaces are shared; spike weights are not.

## Open questions

1. **What is the real inner-speech ceiling for surface sEMG?** The BCI result (72.6% on 7 words,
   26–54% WER on 125k) is motor-cortex data `[5]`. The closest sEMG evidence is indirect: residual
   EMG during imagined two-syllable imagery was above chance but only 2 channels `[25]`, and no
   sEMG imagined-vs-mouthed accuracy table was found.
2. **Does any neural/intracortical pretraining actually help an sEMG decoder?** A deliberate search
   found none. The testable version: train on a shared **phoneme/articulatory label space** rather
   than transferring weights.
3. **What is the real wall-clock latency of the streaming neuroprosthesis?** The verified budget is
   the 80-ms decode increment; the <1 s figure is from the press release, not the paper `[4][7]`.
4. **How much of the invasive calibration advantage is signal quality vs protocol?** 30 minutes to
   99.6% `[2]` may not reproduce on dry facial sEMG; no dry-skin equivalent exists at that
   performance level.
5. **Do Neuralink's later PRIME/CONVOY/Blindsight results ever reach peer review?** As of this
   search, no Neuralink paper reports human speech, cursor bits-per-second, or vision outcomes.
6. **Can the 3-minute calibration result hold for an open vocabulary?** It was demonstrated on a
   closed 50-sentence corpus `[18]`.
7. **What is the right lock mechanism for sEMG?** The invasive keyword result `[6]` has no published
   sEMG analogue; whether a covert motor act can be both reliable and invisible is unresolved.
8. **How much does the language model hide sensing failures?** The leakage result (21.7% → 78.6% CER
   when evaluation sentences are removed from training data) `[18]` suggests single-user numbers are
   easy to inflate; no standard leakage-controlled protocol exists for one-user wearables.
