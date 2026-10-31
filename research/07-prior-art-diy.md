# Track 07 — Prior art: DIY / open-source silent-speech devices, and what is reusable

*Status: complete as of this pass. Created early per BRIEF.md and extended as sources were fetched.
Every claim carries an inline `[n]`; anything that could not be verified against a fetched page is
labelled **unverified** in place.*

## Scope and method

This track answers: **who already built a DIY / open AlterEgo-style silent-speech device, and what
can be reused?** Coverage targets, per the track brief:

- GitHub (stars + recency), Hackaday.io, Hackster.io, OpenBCI community/forum, Reddit
  (r/BCI, r/OpenBCI, r/biohackers), YouTube ("I built AlterEgo", "silent speech EMG"), theses and
  student projects 2018–2026.
- For each project: link, hardware, channel count, electrode sites, vocabulary, reported accuracy,
  code/license, and what went wrong.
- Commercial dev kits that lower the barrier (OpenBCI, BioAmp, MindRove, MyoWare 2.0, Delsys) and
  their limits.
- Closing: the best 3 things to fork or buy for a first working closed-vocabulary prototype.

Everything factual below carries an inline `[n]` mapping to the numbered **Sources** list at the end.
Numbers are quoted exactly as the source gives them. Where a claim could not be verified against a
fetched page, it is marked **unverified**.

---

## 1. What "AlterEgo-class" actually means, from MIT's own pages

Useful grounding before judging DIY claims, because almost every DIY project compares itself to
AlterEgo and most of them overshoot.

- MIT's own project description: the system "reads electrical impulses from the surface of the skin
  in the lower face and neck that occur when a user is internally vocalizing words or phrases –
  without actual speech, voice, or discernible movements" [1]. Feedback is by bone conduction [1].
- Claimed performance, in MIT's words: "a working prototype that, after training with user-specific
  example data, demonstrates **over 90% accuracy on an application-specific vocabulary**. The system
  is currently user-dependent and requires individual training." [2]. Note this is a *claim* on a FAQ
  page, not a peer-reviewed number, and "application-specific vocabulary" is unspecified — no
  vocabulary size, no open/closed-vocab statement, no dataset size.
- Form factor: "We have not prioritized the form factor" [2]. So MIT itself never demonstrated the
  barely-visible version the owner wants.
- The **demonstrated, peer-reviewed** AlterEgo-line result is the MS/dysphonia study: 3 multiple
  sclerosis patients, **10 trials of 15 sentences each**, personalized CNN, "mean overall test
  accuracy of 0.81 at a mean information transfer rate of 203.73 bits per minute" [4]. Vocab = 15
  closed-set sentences per patient, silent articulation, single-user training. That is the honest
  bar: ~0.8 accuracy on a *tiny* closed sentence set, per user.
- Publication trail: IUI 2018 paper (pp. 43–53) [3] and the ML4H 2020 paper [4]. The project
  "originated at the MIT Media Lab in 2018 and spun off as a for-profit company in early 2025" [1] —
  i.e. as of 2026 the lab page points to alterego.io, and there is no open hardware or dataset to
  fork from MIT.

**Takeaway:** nothing from MIT is forkable (no code, no dataset, no hardware files on those pages).
The DIY world has to rebuild the sensing stack from scratch, which is exactly why the projects below
matter.

---

## 2. The fullest DIY paper trail: Cerebro Voice (2018, Hackaday Prize)

The single best-documented open DIY attempt is **Cerebro Voice**, a 2018 Hackaday Prize entry by
Annie Ho, Taylor Yang, Dan Goncharov, Mikhail Filipchuk and Juan Casian (team name "42 Robotics")
[5][6].

| Item | Detail (as documented) |
|---|---|
| Links | https://hackaday.io/project/160715-cerebro-voice [5]; code https://github.com/WesleyTo/subvocalization_stream [6] |
| Hardware evolution | Started with the **MyoWare** board ("2 channels for EMG signal + ground"), then moved "from MyoWare to **OpenBCI** as our biosensing unit to increase the number of channels from a 2-channel board to a 4-channel board" [5] |
| Channels | 2 → 4 (OpenBCI 4-channel board), 7 electrodes listed in the component list, plus a Behringer UMC1820 audio/MIDI interface used as the pre-amp rig and a KY038 mic amp [5] |
| Electrode sites | Throat: "Concentrate around the throat area and Adam's apple but do not put pressure directly on Adam's apple" [5] |
| Electrodes | Disposable "Red Dot" monitoring electrodes (wet gel, snap) [5] |
| Task | Subvocalisation — the training script prompts a word on screen and the user "vocalize[s] or subvocalize[s]" it [6] |
| Vocabulary | Configurable via `configuration.json`, "defaults to a basic set of control words" [6] |
| Reported accuracy | **None published.** The logs only claim "some predictive power" and "predictive power" from more channels [5]. A 2020 commenter asked directly "Is this actually working?" and got no answer [5] |
| Code | Python + Arduino (`main.ino`, `record_raw_data.py`, `flash_new.py`, `process_audio.py`, `check_audio.py`, `upload_audio.py`) [6] |
| License | The README does not state a license (no LICENSE text reproduced there) — **unverified / no explicit license** [6] |
| Outcome | README: "This project is no longer being maintained on this repo… All contributors… left the organization (42 Robotics) in late 2018. This project has not been, and will not be, updated by us, anymore." [6] |

What went wrong / lessons:
- The team tried **EMG Click** first and failed: "Unfortunately we did not have any luck with this.
  Perhaps we did not put enough time into exploring this." [5]
- They tried to convert a **KY038 microphone amplifier into an EMG amplifier** and reported
  "results were not great" [5].
- They iterated on **active sensors** and **flexible PCB** form factor but never got to a
  closed-vocabulary accuracy number [5].
- The signal chain described in the code is telling: **audio capture** (WAV files through a USB
  audio interface) rather than a research-grade biosignal front-end [6]. That is cheap but the
  sample rate/bandwidth is set by an audio interface, and the repo's own to-do list admits the
  Arduino timer timing "may be slightly off due to the imprecise nature of the Arduino crystal clock
  and prescalers" [6].

This is the most reusable *pipeline skeleton* in the DIY space (prompt → label → segmented
per-channel WAV/EMG → dataset → upload), and it is abandoned. It reports **no accuracy**, so treat
it as scaffolding, not as evidence that the approach works with this hardware.

---

## 3. Maker press and adjacent DIY builds

- Hackaday's `subvocal-recognition` tag carries only **two** articles (as fetched) [7], which is
  itself a finding: maker coverage of this topic is thin.
  1. *"Speech Recognition Without A Voice"* (Sept 2018) — coverage of Cerebro Voice; describes it as
     "in the early stages of prototyping" [7].
  2. *"You Won't Hear This Word On The Street"* (Jan 2019) — **Microsoft SilentVoice** by Masaaki
     Fukumoto, demoed at UIST. This is *not* EMG and not subvocalisation: it uses a microphone
     "less than two millimeters from the mouth, usually against the lips" and **ingressive speech**
     (whispering while inhaling) so no air pops the mic [7]. Low-tech and cheap, but it requires
     mouth contact and audible (if quiet) airflow — the opposite of invisible, and it will not work
     in a truly silent setting.
- Cerebro Voice public comments capture the community's scepticism, worth recording as prior-art
  opinion rather than fact:
  - A sEMG-wristband builder: "I always thought it is not possible to record the vocal chords
    controlling muscles without invasive electrodes. Are you sure?" [5]
  - Carl Bugeja: "Had a similar idea once but gave up on trying to filter out the human
    thoughts/inner-voice.. you should try to combine it with a bone conduction speaker" [5] —
    independently arriving at the AlterEgo bone-conduction loop.
  - Shervin Emami: "only if it's done reliably and fairly conveniently… Have you made comparisons of
    how reliable or accurate your system is compared to traditional audio based speech recognition?"
    [5] — again, no answer.
- **jarvisMonke/inner-voice-emg** (created 2024-03-20) is the most recent "DIY AlterEgo" repo found
  that explicitly claims to be one: "An open-source, low-cost EMG system to classify subvocalized
  commands using custom hardware and machine learning" and "a fully open-source, DIY alternative to
  MIT's AlterEgo" [8]. Read the status table carefully: PCB design "In Progress", hardware assembly
  "Not Started", ML pipeline "In Progress", model training "Not Started", demo video "Not Started"
  [8]. Planned hardware: ESP32 + "Custom ADS1299 Breakout PCB", snap electrodes, **up to 6 sensor
  channels**, 1.5 s windows, SVM/LSTM, "Trainable on 4–10+ silent speech commands" [8]. **No
  results, no accuracy, no hardware.** This is a plan, not prior art, and should not be counted as
  a working device.

### 3.1 Student / science-fair builds — the only DIY projects with actual accuracy numbers

These were found via the parallel sub-search and their PDFs were fetched; Hackster itself blocks
automated fetches (HTTP 403) [47][48][49][50].

| Project | Year / author | Hardware | Electrode sites | Vocab | Reported result | Cost |
|---|---|---|---|---|---|---|
| **WAV: A Novel Subvocalization Interpretation Device** (ISEF) | Anjan Sesetty | "Microcontroller + EMG/EEG electrodes"; trained on public EMG + the **EEG-UKA** dataset | not stated in the fetched PDF | not stated | **96.7% accuracy**; **1.92 seconds per translated word** | **< $50** |
| **SpeakUp** (Regeneron STS / Hackster) | Varun Chandrashekhar | **MyoWare** + Arduino + radio, SVM, Streamlit UI | **submental triangle (under the chin)** | not stated | **80.1% accuracy** | **< $100** |
| **MindScribe** (YIS 2025 semi-finalist, Canada) | Krivan Mirok | **OpenBCI Cyton, 8 ch @ 250 Hz**; homemade **3-electrode cheek patch** (silicon tape) | muscles **ZYG, RIS, LLS, DAO, DLI, MAS, ABD, SLH** | **8 words** | **≈0.90 accuracy on a 5-word held-out-day test; 74.60% on the full 8-word** task | not stated |

Source PDFs: WAV ISEF abstract [47], SpeakUp presentation [48], MindScribe report [49]. Caveats: the
ISEF and STS entries are competition abstracts, not peer-reviewed; the numbers are self-reported and
the methods/vocab are thin, so treat WAV's 96.7% and SpeakUp's 80.1% as claims until code/data
appear. MindScribe is the most useful of the three because it names the **exact 8 muscles and the
exact board/rate**, and it shows the day-to-day generalisation drop (≈0.90 → 74.60%) that every
single-user build must expect [49].

### 3.2 NASA Ames "subvocal speech" (2004) — the origin story, and a 92% claim

The project brief's lineage starts before AlterEgo. NASA Ames (Chuck Jorgensen) demonstrated
subvocal speech recognition using button sensors placed **under the chin and on either side of the
Adam's apple**, reporting **"92 percent accuracy" on six words and ten numbers** [50]. Two warnings:
the original NASA URL is dead, and the figure survives in a news reprint, so this is a **secondary
source claim** [50]. The technique is the direct ancestor of the neck/throat electrode placements
every later DIY project uses [5][17][49].

### 3.3 Video/DIY builds found, mostly without numbers

- **Riddlecraft Engineer, "Detecting Facial Muscle Signals Using EMG and Arduino Uno" (2025)** —
  MyoWare + Arduino Uno + AD620 instrumentation amp + MATLAB; sites are cheeks/jaw/throat; **no
  accuracy reported**, and the author explicitly notes weak facial EMG and noise/motion artifacts
  [51]. This is the clearest video documentation of the cheap-front-end failure mode in §8.
- **Endong Sun (Imperial College MSc), "Silent Speech Interface" (2022)** — Arduino + sEMG + ML/DL
  with a UI; **no numbers** in the video description [52].
- **`joaocarvalhoopen/Partial_DSP_implement_of_AlterEgo_Paper` (MIT license)** — a software-only
  simulation of AlterEgo's DSP chain (band-pass, notch, FastICA); **no hardware, no accuracy** [53].
- **PiEEG "Octopus 16"** — a $70 kit ($90 with neckband), 16 channels, 24-bit, advertised with
  "Whisper (Silent Speech) … via throat EMG"; the Indiegogo campaign page returned 403, so the
  specs/claims are **unverified** [54]. Worth tracking as a cheap neckband option.
- **Reddit:** no threads in r/BCI, r/OpenBCI, r/biohackers or r/AskElectronics were found on this
  topic. The only relevant finds are (a) a post confirming the Berkeley "Digital Voicing" dataset was
  recorded with an **OpenBCI Cyton** [55], and (b) the PiEEG Octopus claim above [54]. Reddit direct
  access was blocked; results came via a mirror.
- **Could not open (unverified):** Hackster.io (403) pages including "Sound of Silence" [48];
  openbci.com/community (503) pages "Synthetic Telepathy with Subvocal Recognition | NeuroTechSC"
  and "Subvocal Phoneme Recognition using Facial EMGs"; NYU ITP "Speaking to the Subconscious using
  Subvocal Speech" (410, suspended); a Moratuwa "Silent Speech Decoder" video (EEG/fNIRS, not EMG);
  and **SpeeChin** (neck-mounted IR camera, 54 English / 44 Chinese commands), which is a different
  modality.

### 3.4 The form-factor result the owner should care about: headphone-integrated textile EMG

**Tang et al., "Wireless Silent Speech Interface Using Multi-Channel Textile EMG Sensors Integrated
into Headphones" (arXiv:2504.13921, April 2025; IEEE TIM 2025)** [56]. Four
**graphene/PEDOT:PSS-coated textile electrodes** are sewn into **headphone earmuffs** (so there is
nothing on the face), read by a **compact ESP32-S3 wireless module**, and decoded by a **1D SE-ResNet**
with per-channel squeeze-and-excitation attention to tolerate motion-induced skin-electrode
impedance changes. Reported: **96% accuracy on 10 commonly used voice-free control words**,
outperforming single-channel and non-adaptive baselines [56]. Limits: 10-word closed vocabulary,
accuracy is on the paper's own dataset, and earmuffs are a real wearable but still a visible
accessory. This is the strongest published evidence that the "barely different from normal" goal is
best served by moving the electrodes *off the face* into headphones, rather than by shrinking face
electrodes.

---

## 4. GitHub / open-code landscape (first pass)

The GitHub signal is weaker than for most hardware topics: the flagship DIY project is archived
(Cerebro Voice) and the other "AlterEgo clone" repo never built hardware. The genuinely reusable
code is *research* code:

| Repo / artifact | What it is | Task | Hardware | License / result |
|---|---|---|---|---|
| `dgaddy/silent_speech` ★182 [24] | Official code for EMNLP 2020, ACL 2021 "An Improved Model…", and the 2022 Berkeley dissertation; both **speech synthesis** and **direct silent→text** | **silently mouthed + voiced** | **OpenBCI Cyton, 8 ch, 1000 Hz**, gold electrodes + Ten20 paste, ref behind ear; sites cheek/chin/neck | **MIT code; data CC-BY-4.0** [24][25] |
| `MateusAquino/subvocalization-emg` ★23 [17] | Full capture→label→train→evaluate app | subvocal + articulated | OpenBCI Cyton, 8 ch | **BSD-3**; 4 words, 10 participants |
| `facebookresearch/emg2qwerty` ★142 [57] | Meta's dataset + baselines | **wrist typing**, not speech | Meta sEMG-RD, 32 ch, 2 kHz | **CC-BY-NC-4.0 (non-commercial)**; test CER 6.95% personalised, 51.78% generic |
| `facebookresearch/emg2pose` [58] | Hand-pose regression dataset/models | wrist pose | sEMG-RD, 16 ch/wrist, 2 kHz | CC-BY-NC-SA-4.0; 193 users, 370 h |
| `payalmohapatra/SilentSpeechLLM` ★11 [59] | EMG adaptor + **Llama-3.2-3B** | unvoiced closed-vocab EMG→text | uses dgaddy Zenodo data | MIT; "average word error rate of 0.49" |
| `bigdatasciencegroup/AlterEgo` ★16 [60] | Phoneme biLSTM encoder-decoder + attention; MEng thesis | silent/subvocal | 8 ch, `sample_rate=250`, serial | **no license**; Fluent Speech Commands 248 cmds + 27 phrases; **no accuracy quoted** |
| `luffy101-hash/silent-speak-emg` [61] | 4× Grove EMG in **earmuffs**, 1D CNN | silently mouthed, 10 commands | ESP32-S3, 1000 Hz, 20–450 Hz; masseter/temporalis | MIT; **no accuracy stated** |
| `joaocarvalhoopen/Partial_DSP_implement_of_AlterEgo_Paper` [53] | Software-only DSP simulation (band-pass, notch, FastICA) | — | none | MIT; no hardware/accuracy |
| `Elesdes/EMG2Speech-LiquidNet` [62] | Liquid neural net for EMG→speech | silent | not stated in README | Apache-2.0 |
| `WesleyTo/subvocalization_stream` [6] | Cerebro Voice capture + labelling pipeline | subvocal vs vocal | MyoWare 2ch / OpenBCI 4ch | no license stated; archived |
| `jarvismonke/inner-voice-emg` ★7 [8] | Planned ESP32 + ADS1299 classifier | subvocal, 4–10+ | not built | no license; no results |

**Tooling SDKs worth using:** `brainflow-dev/brainflow` ★1,768 **MIT** — one unified EEG/EMG/ECG
acquisition library across OpenBCI, Muse, Ganglion, etc. [63]; `upsidedownlabs/BioAmp-EXG-Pill`
★427 open hardware [64]; `MindRove/MindRoveSDK` ★16 **Apache-2.0** [37]; `NiklasRosenstein/myo-python`
★283 **MIT** (wraps the proprietary Thalmic SDK) [39]; `BITalinoWorld/revolution-python-api` ★25
**GPL-3.0** [65]. **Community derivatives of emg2qwerty** are where the fast iteration is happening:
`shivk-1/emg2qwerty` reports CER going 46.4% (greedy) → **56.6% (adding an LLM made it worse)** →
39.3% (beam) → **24.8% (full 2 kHz + beam)**, best user 22.2%, and cites a "MyoText" result of 5.4%
CER / 6.5% WER; `KunwooLeeKay/emg2qwerty`, `LLeon360/emg2qwerty`, and `vishar0/emg-tokenizer` (RVQ
tokenizer, 400× compression with no CER loss) are further CNN/Transformer swaps [66]. Two lessons:
(i) the emg2qwerty ecosystem is the fastest-moving sEMG codebase to borrow from; (ii) a language
model on top of a weak acoustic model can *hurt* (56.6% vs 46.4% CER).

Key point for reuse: Meta's emg2qwerty is the biggest open sEMG dataset and the cleanest code
pipeline, but it is **wrist typing on proprietary hardware**, not face/jaw silent speech. Gaddy &
Klein is the closest open *facial EMG* dataset (silent + vocalized), and its headline result is a
demonstrated transition from 64% → 4% WER in one data condition and 88% → 68% in another when
training on silent speech via transfer from vocalized audio [12].

### 4.1 `mateusaquino/subvocalization-emg` — the best open OpenBCI facial montage found

A Brazilian bachelor's final project (Mateus de Aquino Batista, Univap) that is the closest thing to
a **forkable, OpenBCI-based silent-speech app** in the DIY space [17]:

- Hardware: **OpenBCI Cyton (8 channels)**, "read muscle activity data from the face" [17].
- Montage — explicitly adapted from the AlterEgo IUI 2018 pilot's "top muscle regions": **Earlobe →
  BIAS**, **Mental → N3P (upper)**, **Inner laryngeal → N1P (upper)**, **Outer laryngeal → N1P
  (lower)**, **Hyoid → N3P (lower)**, **Inner infra-orbital → N2P (upper)**, **Outer infra-orbital →
  N4P**, **Buccal → N2P (lower)** [17]. This is the single most concrete electrode-placement recipe
  in the open DIY corpus and it should be the starting montage for the build.
- Software: Python 3.10.9 + TensorFlow/Keras 2.11.0; a browser app (`localhost:8000`) with EMG
  streaming, a recording tab (word + repeat setup), neural-network training tab, and an evaluation
  tab; PoC notebooks including one that runs on a public EMG hand-gesture dataset [17].
- Dataset: **10 participants**, 4 words — **"Sim" (Yes), "Não" (No), "Talvez" (Maybe), Silence** —
  each recorded in three speech styles: **F = normal speech, A = lip articulation, S =
  subvocalization**, grouped `participant → speech style → word`; ethics approval CAAE
  65587722.5.0000.5503 [17].
- Reported results: the README states the *expectation* "A hit rate between 90 and 95% is expected
  from the general validation", but the **conclusion is the honest part**: "The results demonstrate
  that this processing and training method is effective for detecting strong gestures, such as
  speech and articulation. However, for more subtle muscle movements, such as subvocalization,
  further improvements in noise reduction and data augmentation are necessary." Also: "the same
  methods, montage, and algorithm yielded varying results across different participants. Some
  exhibited lower accuracy in detecting easily recognizable speech, while others achieved higher
  accuracy in identifying less discernible subvocalizations." [17]
- License: **BSD 3-clause** on the source code; article content reserved [17]. This is the only
  facial-EMG DIY project found with an explicit permissive license.
- Status caveat: README says "This study is currently underway… preliminary and subject to change"
  [17]. **No final per-word accuracy table was on the README** — the notebooks (`Subvocalization.ipynb`)
  are where the numbers would be; treat any headline accuracy as unverified until those are run.

This repo alone justifies the track: it gives an 8-channel montage, a working capture/train/evaluate
app, a 10-person 4-word × 3-style dataset, a permissive license, and a clear statement of where the
method breaks (subvocalization ≪ articulation ≪ voiced speech).

### 4.2 Biohacker-community prior art for the subdermal variant

The owner's "small subdermal implant" idea is not new. On biohack.me (August 2015) user
garethnelsonuk proposed exactly this: "a set of **subdermal EMG electrodes near the throat for
subvocal recognition** — with training over time and with the electrodes being in the same position
every time this should become more and more accurate and has the advantage of silent input of
complex data", with output via an eyetap and/or **bone-conduction earphone** [18]. The thread is
70 comments of design debate, not a build; the only hardware claim is second-hand ("logistic
regression based binary classification for EEG analysis in real-time on an arduino at up to 512 Hz
over four channels") [18]. Useful as prior art and as a warning: an 11-year-old subdermal-throat-EMG
plan never produced a device [18]. Another commenter in the same thread cites a 2014 paper that
"sampled at 20 kHz over 5 channels on the face and neck" for "semi-complete subvocal recognition"
[18] — a sample-rate target worth noting (see §9).

---

## 5. OpenBCI community: one real student project, one dead-end thread

- **MUSE** (OpenBCI community case study, published 2025-12-14): a student team ("Ignitious" plus
  Mohamed and Lakshmi) built a system on the **OpenBCI Cyton 8-channel board** with "medical-grade
  amplifiers placed on specific facial muscles" to detect millivolt-level activation during imagined
  speech [10]. Stated target: "correctly classify **over 100 common words** from facial EMG data
  with **over 90% accuracy**", and to share the dataset publicly [10]. As of the case study there is
  **no reported accuracy and no released dataset** — only the block diagram, an example raw EMG
  trace, and an electrode-placement figure. This is the closest open *facial* EMG student effort on
  OpenBCI hardware and worth contacting through the case-study page [10]; note the page is the
  Chinese OpenBCI distributor's site reposting an OpenBCI community story.
- **OpenBCI forum** (July 2019): user JMCooper asked about using the **Ganglion** board + gold cup
  electrodes to detect throat EMG for subvocalisation, to build biofeedback (audio or vibration) to
  *suppress* subvocalisation while reading, portable on a Raspberry Pi [9]. The only substantive
  reply is about electrode choice: for sEMG the common choice is "foam pre gelled adhesive type
  (silver chloride buttons)" with snap connectors, not gold cups [9]. **No follow-up results in the
  thread** — another example of a project announced and not finished.

---

## 6. Academic / student projects 2018–2026 that a DIY builder can actually reuse

These are not "maker" builds, but they are the prior art closest to buildable, with published
numbers and sometimes open data:

1. **PULP / ETH Zürich — fully-dry EMG neckband (Sensors 2025 / arXiv 2509.21964)** [16]. Textile
   neckband, **14 fully-differential EMG channels**, BioGAP-Ultra platform, **22 mW**. Evaluated on
   **8 speech commands**: vocalized **87 ± 3%**, silent articulation **68 ± 3%** with 5-fold CV;
   when the band is **repositioned between sessions** (leave-one-session-out), accuracy drops to
   **64 ± 18%** (vocalized) and **54 ± 7%** (silent). Single-site, 8-word closed vocabulary, fully
   dry electrodes. This is the most honest published "small closed vocabulary, silent, dry
   electrodes" number set found, and it quantifies the session-repositioning penalty that every DIY
   build will hit.
2. **Arduino + ensemble learning sEMG SSI** (Springer chapter, copyright 2026, Deveza, Ibarra,
   Sejera) [15]. Explicitly uses **Arduino** and **sEMG**, compares **ResNet50V2, VGG16, CNN-LSTM,
   MLP** and ensembles (soft voting, stacking with NN/SVM meta-learners). Abstract claim: "the
   proposed SSI can achieve an **F1-Score of at least 90%**" [15]. Caveats: paywalled; the abstract
   is AI-summarised by the publisher; vocabulary, channel count, electrode sites and subject count
   are **not stated in the abstract — unverified**. Treat the 90% F1 as a claim until the methods
   are read.
3. **Soft active EMG interface, worn on the hand** (Advanced Intelligent Systems 2026, e70440;
   arXiv 2608.27048, Aug 2026) [19]. This is the highest reported closed-vocabulary accuracy found
   and it deliberately avoids permanent facial attachment: the device is "worn on the hand… a
   fingertip electrode that can be positioned near the lips to acquire EMG signals **only when
   needed**", built from liquid-metal interconnects, transparent flexible printed-circuit
   electrodes, and elastomer encapsulation [19]. A DNN classified a **30-word vocabulary at a mean
   accuracy of 97.2 ± 1.3% across three subjects**, and the authors demonstrate **real-time drone
   control** [19]. Limits to note: 30 words, 3 subjects, and the "silent" mode involves bringing the
   hand/finger to the lips — discreet, but not invisible and not hands-free. This is the design to
   study if the owner wants a high-accuracy first prototype without wearing anything on the face.
4. **Myovox** (arXiv 2609.17548, July 2026) [11] — see §7; the single most relevant *reusable
   pipeline* for open-vocabulary face EMG.
5. **NTNU master's thesis, "Silent Speech Communication Using Facial Electromyography"**
   (Backsæther, NTNU Open handle 11250/2784241) — found, landing page redirects through
   `hdl.handle.net` → `nva.sikt.no`; **not fetched/verified in this pass**.
6. **WPI project, "Analysis into the use of EMG & AI to unlock a voice for the speech-impaired"**
   (Steyn, Savoie; WPI Digital Commons) — surfaced in search and on Semantic Scholar; the
   repository download is a PDF and the landing page did not render, so **unverified**. Title
   indicates the same face/neck EMG → speech goal.
7. **"Subvocal Speech Recognition via Close-Talk Microphone and Surface Electromyogram Using Deep
   Learning"** — surfaced in search (Wanfang conference record); **unverified**. Interesting as a
   *sensor-fusion* framing (microphone + sEMG), which is what the Cerebro Voice team also attempted
   with a KY038 mic amp [5].
8. **Canadian science-fair project MindScribe** (YIS 2025 semi-finalist report, "MindScribe:
   Innovation Report") — surfaced in search, PDF not fetched; **unverified**.
9. **"WAV: A Novel Subvocalization Interpretation Device"** and **"SpeakUp"** (Varun
   Chandrashekhar, Regeneron STS/Hackster) — both surfaced in search; Hackster returned HTTP 403
   (Cloudflare) and the STS abstracts are PDF-only, so both are **unverified** in this pass. SpeakUp
   is described elsewhere as "A Machine Learning-Based Speech Aid to Enable Real-Time Silent
   Communication for the Paralyzed by Translating Neuromuscular…" [search result].

---

## 7. The reusable research core: emg2speech, emg2qwerty, Myovox

If the owner is one user who can collect a lot of calibration data, the practical question is *which
published pipeline to copy*. The candidates below are ordered by how directly they serve a
face/neck silent-speech build.

**A. Meta `emg2qwerty` (2024) — best code/data hygiene, wrong body part** [13]. 108 users, 1,135
sessions, 346.4 h, 5,262,671 keystrokes; two wristbands × 16 differential dry-gold pairs = 32 ch,
2 kHz, 12-bit, 6.6 mV max, 20–850 Hz, Bluetooth [13]. Time-Depth-Separable ConvNet + CTC + 6-gram
char LM. Test CER: generic **51.78 ± 4.61%** (unusable), personalised random-init **9.55 ± 5.16%**,
personalised fine-tuned **6.95 ± 3.61%**, best user **3.16%**; authors say models become "usable at a
CER of approximately 10% or less". Fatal limit: the `sEMG-RD` wristband is proprietary, and the paper
itself lists "lack of broader access to the proprietary research-grade sEMG hardware" as a limitation.
Code/data are forkable, the sensing is not. License **CC-BY-NC-4.0 (non-commercial)** [57].

**B. Gaddy & Klein `silent_speech` (EMNLP 2020 Best Paper; ACL 2021; 2022 dissertation) — the best
documented silent *facial* EMG corpus, recorded on buyable hardware** [12][24][25].
- Hardware (per the repo/paper): **OpenBCI Cyton, 8 channels, 1000 Hz**, gold electrodes with Ten20
  paste, monopolar, reference behind the ear; sites on **cheek, chin and neck**, in a single speaker
  over **~20 hours** [24]. Note the 1000 Hz rate: this is the *same board* the dev-kit section lists
  at a 250 Hz default, so the Cyton must be driven faster than the default streaming mode (see §9.1).
- Vocabulary: a **closed set of 67 words** (≈26 min silent + 30 min voiced, ~500 utterances) and an
  **open ~9,828-word** condition [24].
- Results, quoted: transcription WER "improves from **64% to just 4%**" on the closed set (human
  evaluation); on the open condition **88% → 68%** (automatic) and **95% → 75%** (human); the repo
  README states the latest model reaches "a WER of approximately **36%**" on an ASR-based
  open-vocabulary evaluation, and the direct silent→text CTC model "approximately **28%**" [24].
- Releases "our new dataset of silent and vocalized facial EMG measurements" [12]: **CC-BY-4.0**,
  3.9 GB, 8-channel numpy arrays [25]. Code is **MIT** [24].
- A 2025 community model, `SilentSpeechLLM` (MIT), trains an EMG adaptor + **Llama-3.2-3B** on this
  dataset and reports "average word error rate of 0.49" — i.e. an LLM layer on top of the same
  open data is still far from the closed-set 4% [59].

This is the fork with the *fewest unknowns*: 8-channel data you can download, code you can run,
MIT/CC-BY licensing, and hardware you can buy (an OpenBCI Cyton). Its weakness is that the source
data is **silently mouthed** (lips move) rather than zero-movement subvocalisation, and it is one
speaker [24].

**C. Myovox (2026) — single-author replication of an open-vocab face-EMG model** [11]. **31-channel
facial sEMG**, single subject, **vocalized** speech, open-vocabulary English; starts from the public
**emg2speech "General Corpus"** and takes it from a published **51.17% WER** to **18.53% WER** in
three measured steps: (1) recover missing decode settings → **40.63% WER / 39.02% PER** faithful
baseline; (2) bidirectional Conformer + cross-modal distillation from WavLM-Large layer-9 features →
**26.14% WER / 22.34% PER**; (3) two-model ensemble + n-best union + QLoRA 7B LM reranker → **18.53%
WER**. The negative result matters most: reranking saturates because the binding constraint is the
**acoustic phone error rate (~20.9%)**, and the 9.30% n-best oracle is unreachable — no LM can fix the
sensing gap. Test set **400 held-out sentences** of the **8,500 / 760 / 400** split; single subject.
Scope warning: **vocalized**, not silent, and one person [11].

**D. emg2speech / Gowda & Miller — open code, open data, direct *silent* EMG-to-text** [20][21][22][23].
The strongest silent-articulation fork: `HarshavardhanaTG/emg2speech` decodes sEMG "from the face and
neck" to phonemes, with manifold/Euclidean RNN code, `largeVocab*`, **`smallVocabEuclidean/Manifold`**,
**`natoWords`**, `checkGrandfather`/`checkrainbow` notebooks, and an `emg2qwerty/` replication dir
[20]. Data + checkpoints on OSF (`osf.io/bgh7t/`, unzip to `DATA/`): large/small-vocab arrays and
labels, trained checkpoints + LM/WFST graphs, and **NATO-words data for Subjects 1–4** [20]; the OSF
page is JS-only to the fetcher, so treat the file list as described-by-README (**unverified**) [23].
Papers: "Non-invasive electromyographic speech neuroprosthesis: a geometric perspective"
(arXiv 2502.05762) — sEMG from "multiple articulatory sites on the face and neck as participants
silently articulate speech", **direct sequence-to-sequence EMG-to-text at the phoneme level without
time-aligned audio** [22]; and "emg2speech" (arXiv 2510.23969) — maps EMG into self-supervised speech
(S3) space, "a simple linear mapping predicts EMG power from S3 representations with a correlation of
**r = 0.85**", demonstrated on a participant with **ALS** silently articulating [21]. License **not
verified** (`.../main/LICENSE` → HTTP 404) [20].

**E. Field review:** "Silent Speech Interfaces in the Era of Large Language Models" (arXiv 2603.11877,
March 2026, 20 pages) [14] — taxonomy across neural, neuromuscular, articulatory-kinematic and
acoustic/RF modalities, LLM-as-prior, and the "user-dependency paradox". Cite it as the frame.

**F. Open facial-EMG corpora and pretrained weights — the actual download list** [24][25][26].

| Asset | Access | Size / shape | License | Notes |
|---|---|---|---|---|
| Gaddy "Silent Speech EMG" (EMNLP 2020 dataset) | Zenodo DOI 10.5281/zenodo.4064409 [25]; code `dgaddy/silent_speech` [24] | `emg_data.tar.gz` = **3.9 GB**; each sample `{i}_emg.npy` shape **(T, 8)**, plus `_audio.flac`, `_audio_clean.flac`, `_info.json` (text prompt), `_button.npy` [25] | **CC-BY-4.0** [25] | Facial EMG during **both silent and vocalized speech**; recorded with an **OpenBCI Cyton, 8 ch, 1000 Hz**, ref behind ear, cheek/chin/neck sites; closed 67-word set + open ~9,828-word condition, ~20 h, single speaker [24][25]. Samples with `sentence_index: -1` are reference signals, not data [25] |
| `dgaddy/silent_speech` code + pretrained models | GitHub [24]; vocoder+transduction weights Zenodo 6747411, recognition weights Zenodo 7183877 (per README) [24] | — | code **MIT**; data CC-BY-4.0 [24][25] | Official repo for EMNLP 2020, ACL 2021 "An Improved Model for Voicing Silent Speech", and the 2022 Berkeley dissertation. Latest model **~36% WER** on ASR-based open-vocab voicing; direct silent→text CTC model **~28% WER** [24]. Needs DeepSpeech 0.7.0 model files + KenLM + ctcdecode [24] |
| CSL-EMG_Array (Uni Bremen, INTERSPEECH 2020) | uni-bremen.de corpus page, email-gated download [26] | **4×8 + 1×8 array sEMG** (i.e. 32 + 8 electrodes); **12 sessions, 8 speakers** (8 audible, 4 silent); **~9.7 hours**; **8.8 GB**; NumPy v3 + JSON; marker channel for sync [26] | **CC-BY-4.0** [26] | Parallel facial sEMG **and** audio for audible *and* silent speech; the best public *array* corpus for pretraining a face montage [26] |
| emg2speech (Gowda & Miller) | GitHub + OSF `osf.io/bgh7t/` [20][23] | large-vocab pkl, small-vocab npy, NATO-words per subject 1–4, checkpoints | not verified (no LICENSE file found) [20] | Silent articulation, face+neck, direct EMG→text and EMG→audio [21][22] |
| emg2qwerty (Meta) | GitHub `facebookresearch/emg2qwerty` [13] | 108 users / 1,135 sessions / 346.4 h | not verified here | **Wrist** typing, not face; hardware proprietary [13] |

Practical order of operations for one user: (1) run `dgaddy/silent_speech` inference on the public
8-channel silent corpus to get the toolchain working; (2) pretrain or fine-tune on CSL-EMG_Array
(40-electrode array, audible+silent) or emg2speech's small-vocab/NATO data; (3) only then record
your own 8-channel Cyton data with the mateusaquino montage [17] and fine-tune per-user, because
every result above shows personalisation is where the accuracy comes from (6.95% vs 51.78% CER
[13]).

---

## 8. What consistently goes wrong (failure modes extracted from the prior art)

These recur across every project above; they are the build's risk register.

1. **Projects die at exactly the "collect lots of labelled data" step.** Cerebro Voice archived
   after the capture pipeline worked and before any classifier accuracy was reported [5][6]; the
   OpenBCI Ganglion throat-EMG thread stops after one electrode-advice reply [9]; `inner-voice-emg`
   (2024) never assembled hardware [8]; the 2015 subdermal-throat-EMG proposal produced 70 comments
   and no device [18]. Only academic labs (PULP, Meta, Gaddy) got past this, because they had
   participants and time.
2. **Subvocalisation is much weaker than articulation or voiced speech.** PULP: 87 ± 3% voiced vs
   68 ± 3% silent, 5-fold CV [16]. mateusaquino: method "effective for detecting strong gestures,
   such as speech and articulation… for more subtle muscle movements, such as subvocalization,
   further improvements in noise reduction and data augmentation are necessary" [17]. Design
   consequence: a first prototype should train on *lip articulation* as well as subvocalisation and
   treat voiced speech as the upper bound.
3. **Session-to-session electrode repositioning is the dominant error source.** PULP:
   87 → 64 ± 18% (voiced) and 68 → 54 ± 7% (silent) under leave-one-session-out with band
   repositioning [16]. `emg2qwerty`: generic cross-user model is unusable at **51.78% CER** and
   personalization is what fixes it (6.95% CER) [13]. Design consequence: fix the montage
   mechanically (a jig or a fixed band) *before* spending time on models; budget labelled data per
   session; use rotation/channel-shift augmentation as Meta did [13].
4. **Cheap front-ends and wrong electrodes silently cap accuracy.** Cerebro Voice failed with the
   EMG Click and with a KY038 mic amp repurposed as an EMG amp [5]; an OpenBCI thread documents that
   for sEMG the standard is gel adhesive silver-chloride snap electrodes, not gold cups [9]. The
   Myo armband is a documented example of a consumer device that "only measures 8 channels of sEMG
   and has a low sampling rate (200 Hz) after the signal has been rectified and smoothed" [13] —
   rectification/smoothing before the ADC destroys the information a speech model needs.
5. **Under-sampling and clock jitter.** The 2014 work cited in the biohack thread sampled **20 kHz
   over 5 face/neck channels** [18]; the Arduino in Cerebro Voice was admitted to have imprecise
   timer timing [6]. Decide a sample rate and get a real clock/timestamp source before collecting
   the dataset; you cannot fix aliasing later.
6. **There is a hard acoustic-model ceiling; an LLM cannot rescue a bad signal.** Myovox shows
   reranking saturates at 18.53% WER because the EMG acoustic phone error rate is ~20.9% and the
   n-best oracle is 9.30% [11]. Spend effort on channels/montage/electrodes, not on a bigger LM.
7. **Accuracy scales inversely with vocabulary and with how silent you are.** The honest published
   points: 8 silent words → 68% (dry neckband, [16]); 30 words → 97.2% but with a fingertip brought
   to the lips ([19]); 3 MS patients × 15 sentences → 0.81 ([4]); 4 words × 3 speech styles → method
   works for voiced/articulated, subvocal needs work ([17]). MIT's "over 90% on an
   application-specific vocabulary" [2] has no published vocabulary size and must not be used as a
   planning number.
8. **The best hardware is not for sale.** Meta's `sEMG-RD` (the source of the best open dataset) is
   proprietary and the authors list lack of access as a limitation [13]. Expect to build or buy the
   front-end, not to copy one.

---

## 9. Commercial dev kits that lower the barrier

All specs below were read from the vendor pages listed in Sources [28]–[46]; prices are as displayed
at fetch time and are not converted. "Not published" means the vendor page does not state it.

### 9.1 OpenBCI — the established research baseline

| Board | Channels | Sample rate | ADC | Range / gain | Electrodes | Price |
|---|---|---|---|---|---|---|
| Cyton | 8 | **250 Hz** default ("Faster rates are supported by the ADS1299, but the RFDuino wireless link and the serial limits might not be able to keep up") | 24-bit (ADS1299) | +2.5 to −2.5 V; default gain 24× (config 24/12/8/6/4/2/1); scale 0.02235 µV/count; SNR 121 dB; resolution 0.298 µV/bit | not included; gold-cup wet, EMG/ECG snap cables | **$1,249.00** |
| Cyton + Daisy | 16 | 250 SPS, but it alternates board/Daisy samples and sends a **2-sample average** | 24-bit | as Cyton | as Cyton | **$2,499.00** |
| Ganglion | 4 | **200 Hz** streaming | 24-bit MCP3912, but BLE sends only **19-bit** default (18-bit with accel) | −15,686 µV to +15,686 µV; scale 0.001869917138805 µV/count; gain not published | any via 16-pin header; dongle sold separately | **$624.99** |
| Galea | not published | not published | not published | not published | not published | **$42,980.00** |

Sources [27][28][29][30]. Limits for this project: Cyton's default 250 Hz is *just* enough for
surface EMG (~20–450 Hz) but is Nyquist-limited and has no active electrodes, so expect motion
artifact on a jaw that moves when you talk; the Cyton+Daisy **averages two samples**, which further
degrades high-frequency EMG; the Ganglion's 200 Hz gives ~100 Hz Nyquist, which is **too low for the
full EMG band** and its BLE path drops LSBs [27][28][29]. This is consistent with the independent
report that the discontinued Myo armband "only measures 8 channels of sEMG and has a low sampling
rate (200 Hz) after the signal has been rectified and smoothed" [13]. **However:** the best open
facial silent-speech dataset (`dgaddy/silent_speech`) was recorded on this same Cyton board at
**1000 Hz** [24], which means the 250 Hz streaming figure is a *wireless/serial default*, not the
ADS1299's ceiling (the Cyton specs page itself says faster rates are supported by the ADS1299 but the
RFDuino link and serial may not keep up [28]). A cabled or SD-card / custom-firmware Cyton can
therefore reach the rates the face-EMG literature uses; budget the EE's time for that.

### 9.2 Cheap analog front-ends (buy several, build the ADC yourself)

| Item | Channels | ADC / sample rate | Gain / bandwidth | Electrodes | Price | Open source |
|---|---|---|---|---|---|---|
| BioAmp EXG Pill | 1 | **no ADC on board** — needs host MCU/ADC (docs recommend Arduino UNO R4, 14-bit; or ADS1115/ADS131M0x) | gain set by R6; bandpass set by R12/C5; **default gain/BW not published**; default configured EEG/EOG, solder jumper for EMG/ECG; input impedance 10^12 Ω | 2 or 3, 1.5 mm wire or gel | **₹2,599** (1), **₹5,199** (2-pack), **₹19,999** (8-pack) | yes, HW+SW |
| Muscle BioAmp Shield | 1 | no ADC — Arduino UNO shield | fixed gain **×2420**, bandpass **72–720 Hz**, input impedance 10^11 Ω | 3 (pos/neg/ref), gel or Muscle BioAmp Band | store price not captured | yes, HW+SW |
| Muscle BioAmp Band | 1 (passive band) | n/a | n/a | dry snap | **₹199** | n/a |
| MyoWare 2.0 Muscle Sensor (DEV-27924) | 1 analog | no ADC, no sample rate | gain RAW/rectified/envelope = 200; HPF fc 20.8 Hz; LPF fc 498.4 Hz; envelope fc 3.6 Hz; CMRR 140 dB; 2.27–5.47 V | snap disposable wet | **$42.95** | not open (SparkFun) |
| MyoWare Link / Power / Cable / Arduino shields | up to 6 sensors per Link Shield | — | — | — | $13.50 / $15.95 / $5.95 / $10.25 | — |

Sources [31][32][33][34]. Important: Up**side** Down Labs publishes no multi-channel "BioAmp ADC"
board — the documented multi-channel path is **combining 2× EXG Pill + an Arduino UNO R4** for a
2-channel rig [31]. MyoWare 1.0 is **retired** and its gain/bandwidth were never on the tutorial
page [34]. Both are 1-channel-per-board designs, so an 8-channel face montage means 8 front-ends, 8
ADC inputs, and careful common-reference wiring — which is exactly the gap a custom PCB (the hired
EE's job) should fill.

### 9.3 Mid-tier dry-electrode bands with SDKs

| Item | Channels | Sample rate | ADC | Gain / BW | Electrodes | Price | SDK / license |
|---|---|---|---|---|---|---|---|
| MindRove Armband 2 | 8 EMG (+2) | **500 SPS** | 24-bit | gain 12; 0–250 Hz | 8+2 stainless steel **dry** | **$799.00** (reg $899) | C++, C#, Python, MATLAB, LSL; docs list an **MIT License** page |
| MindRove Armband (prev) | 8 EMG (+2) | 500 SPS | 24-bit | gain 12; 0–250 Hz | 8+2 dry | **$679.00** | same |
| MindRove **Sense XR Face + Brain** | 8 total = 2 forehead EEG + 2 central EEG + 2 occipital EEG + **2 facial EMG** | 500 SPS | 24-bit | not published | integrated dry VR-face interface | **$949–$1,049** | same |

Sources [35][36][37]. This is the only off-the-shelf option found that ships **facial EMG** channels
with raw access and a documented SDK [36][37]. 500 SPS / 24-bit beats Cyton on rate; only 2 facial
channels, and both vendors' 16/32-channel EMG+EEG boards were **not found on the current store**
(unverified) [37].

### 9.4 Research/clinical tier (quote-only, not first-prototype friendly)

- **Delsys Trigno**: Trigno Centro "Capture up to **128 EMG channels**", 32 sensors, 40 m+ range,
  0 ms inter-sensor latency; sensors include Avanti (EMG+IMU), Quattro (4-ch), Galileo (HDsEMG /
  motor-unit decomposition). Noise baseline 5 µV pk-pk; signals 20 µV–2 mV; full-scale SNR 65 dB.
  **Sample rate and ADC bits are not published on the website; price is not published — "Request a
  Quote"** [38].
- **OYMotion gForcePro+ / gForceOct**: 8 differential EMG + 9-axis IMU, dry electrodes, 8-bit max
  1 kHz or 12-bit max 500 Hz, ARM Cortex-M4, BLE; **price not published** (sales@) [40].
- **BITalino (PLUX)**: EMG sensor **€60.00**, Board **€195.00**, Plugged **€225.00**, MuscleBIT
  (**4 EMG**) **€395.00**; sample rate/ADC not published on the fetched pages [41].
- **Brain Products** (LiveAmp/actiCHamp) and **g.tec** (g.Nautilus/g.HIamp): pages JS-rendered, no
  price, distributor/quote only — **unverified** [44][45].

### 9.5 Consumer EEG/EMG headsets — mostly the wrong tool

- **NeuroSky MindWave Mobile 2**: 1 EEG at **FP1**, **512 Hz**, 12-bit raw, free dev tools; price not
  shown on the fetched page; forehead-only, no EMG-grade front-end [42].
- **Muse S / Muse 2**, **Emotiv Insight** (5-channel per page title), **Emotiv EPOC X** (14-channel
  per page title): sensor pages are JS-rendered or behind the developer portal, so channels/sample
  rate are **unverified** here; the Cortex API docs page is reachable [43][46]. None has a facial/jaw
  EMG front-end or documented facial electrode sites.
- **Thalmic Myo**: discontinued — myo-python README: "[Oct 15, 2018] Thalmic Labs have announced the
  discontinuation of the Myo armband." Community SDK **myo-python** is MIT-licensed but wraps the
  proprietary Thalmic Myo SDK. Sample rate 200 Hz is widely cited but official pages are defunct
  (**unverified**). Secondhand only; forearm form factor [39].

**For this project the honest ranking is:** OpenBCI Cyton (because the best open *facial silent*
dataset was recorded on it, at 1 kHz, with 8 channels — see item 1 below) or MindRove Sense XR (if
you want facial channels out of the box at 500 SPS) > BioAmp EXG Pill × N + a good ADC (if the hired
EE is going to design the real PCB anyway). Avoid Ganglion, Myo, MyoWare-for-accuracy, and consumer
EEG headsets for the silent-speech path.

---

## Best 3 things to fork or buy to get a first working closed-vocabulary prototype fast

**1. FORK `dgaddy/silent_speech` + its Zenodo dataset — fewest unknowns, buyable hardware, best
licensing.** [24][25] This is the strongest single fork: official code for EMNLP 2020 / ACL 2021 /
the 2022 Berkeley dissertation, **MIT code**, a **CC-BY-4.0** 3.9 GB dataset of **8-channel** facial
EMG recorded on an **OpenBCI Cyton at 1000 Hz** (cheek/chin/neck, ref behind ear, single speaker,
~20 h), a **closed 67-word** condition with a reported **64% → 4% WER** (human eval) and an open
~9,828-word condition at **~36% WER**, plus *pretrained weights* for both speech synthesis and direct
silent→text. Start here: download the data, run inference with the released recognition model, then
fine-tune on your own 8-channel recordings using the same montage [24][25]. Caveat: "silently
mouthed" (lips move) and one speaker.

**2. FORK `HarshavardhanaTG/emg2speech` (code) + its OSF data bundle — the *zero-movement*
silent-articulation companion.** [20][21][22][23] Where dgaddy is silently *mouthed*, emg2speech
targets **silently articulated** face/neck EMG and does direct EMG→text and EMG→audio, with code,
data (large-vocab pkl, small-vocab npy, NATO-words for 4 subjects) and pretrained checkpoints, plus
**`smallVocab*`** and **`natoWords`** notebooks to run on day one. Use it to pretrain and as your
regression test (`checkGrandfather.ipynb` / `checkrainbow.ipynb`). Caveat: no LICENSE file found at
the README's path — confirm licensing before shipping anything derived from it [20].

**3. FORK the montage, then BUY one front-end now (custom PCB later).**
- Montage: `MateusAquino/subvocalization-emg` (BSD-3) gives the **8-site facial montage** adapted
  from AlterEgo — Earlobe/BIAS, Mental, Inner laryngeal, Outer laryngeal, Hyoid, Inner
  infra-orbital, Outer infra-orbital, Buccal — plus a working capture→label→train→evaluate app and a
  10-participant, 4-word, 3-speech-style dataset layout [17]. Keep this even if you change boards.
- Buy: **OpenBCI Cyton** — 8 ch, 24-bit, **$1,249**, the board both dgaddy [24] and mateusaquino
  [17] used; plan to run it cabled/SD at **1 kHz**, not the 250 Hz wireless default [28].
  *Alternative:* **MindRove Sense XR Face + Brain** — 8 total channels including **2 facial EMG**,
  **500 SPS**, 24-bit, dry, documented SDK, **$949–$1,049** [36][37].
  *Budget:* **2–8× BioAmp EXG Pill** (₹2,599 each) + Arduino UNO R4 (14-bit ADC) or ADS131M0x, for
  the EE-designed PCB path [31][32].

For the "barely different from normal" requirement, also prototype **headphone-integrated textile
EMG**: 4 graphene/PEDOT:PSS electrodes in earmuffs + ESP32-S3 reached **96% on 10 voice-free control
words** in Tang et al. 2025 [56], and removes face electrodes entirely.

Do **not** start with: Ganglion (200 Hz), Thalmic Myo (discontinued, 200 Hz, forearm), consumer EEG
headsets (no EMG front-end, correct positions unavailable), or MyoWare as the accuracy path (1
channel, no ADC, retired 1.0) [29][33][34][39][42][43].

---

## Key takeaways for the build

- **Nobody has publicly shipped a working, invisible, verified DIY AlterEgo.** The fullest maker
  attempt, Cerebro Voice (2018), is archived with no published accuracy [5][6]; the only DIY builds
  that *claim* strong numbers are science-fair abstracts (WAV: 96.7%, < $50 [47]; SpeakUp: 80.1%,
  < $100 [48]) and are self-reported/unverified. Plan for a hard, multi-month build, not a kit.
- **MIT's "over 90% accuracy" is a FAQ claim with no vocabulary size, no dataset size and no
  open/closed-vocab statement; the peer-reviewed number is 0.81 mean accuracy on 15 closed sentences
  for each of 3 MS patients, after per-user training** [2][4]. Use 0.81/15-sentence closed-vocab as
  the honest anchor, not 90%.
- **Accuracy ordering is voiced > articulated > silent.** PULP's dry neckband: 87 ± 3% voiced vs
  68 ± 3% silent on 8 words; 64 ± 18% vs 54 ± 7% after the band is repositioned between sessions
  [16]. A one-user prototype that allows **near-silent lip articulation** will be far easier than
  true zero-movement subvocalisation, which multiple projects flag as the weak case [5][17].
- **Session-to-session electrode placement is the dominant error term, above model choice.**
  68% → 54% (silent, PULP) [16]; 51.78% → 6.95% CER from generic to personalised (emg2qwerty) [13].
  Fix the montage mechanically and budget per-session labelled data before buying a bigger GPU.
- **Fork the decoder, don't write it. Best single fork: `dgaddy/silent_speech`** — MIT code, a
  CC-BY-4.0 8-channel facial EMG dataset (3.9 GB), an OpenBCI Cyton recording rig at 1 kHz, a closed
  67-word result of **64% → 4% WER** (human eval) and open-vocab ~36%, plus pretrained weights
  [24][25]. Add `emg2speech` for **silent articulation** (open code + OSF data + checkpoints)
  [20][21][22][23] and CSL-EMG_Array (40-electrode array, ~9.7 h, audible+silent, CC-BY-4.0) as the
  public array corpus [26]. Note Meta's emg2qwerty is **CC-BY-NC-4.0 — non-commercial** [57].
- **Copy the montage from `mateusaquino/subvocalization-emg`** (8 facial/neck sites, BSD-3, Cyton pin
  map) rather than inventing electrode positions [17].
- **An LLM cannot rescue a weak signal — and can make it worse.** Myovox: reranking saturates at
  18.53% WER because the EMG acoustic phone error rate is ~20.9% and the n-best oracle is 9.30% [11].
  On emg2qwerty, adding an LLM raised CER from 46.4% (greedy) to **56.6%** in one community
  reproduction [66]. Spend the effort on electrodes, channels, sample rate and mounting.
- **Hardware: pay for sample rate and channel count, not brand.** The OpenBCI Cyton runs at **1 kHz**
  in the best open facial dataset [24] even though its wireless default is 250 Hz [28]; MindRove
  Sense XR gives 2 facial EMG at 500 SPS/24-bit dry [36]; avoid 200 Hz-class devices entirely
  [29][39]. The generic dev-kit gap (1-channel analog boards vs 8+ channel facial arrays) is exactly
  what the hired EE's custom PCB should close [31][33].
- **The "barely different from normal" answer may be headphones, not face electrodes.** Four
  graphene/PEDOT:PSS textile EMG electrodes sewn into headphone earmuffs + an ESP32-S3 reached **96%
  on 10 voice-free control words** [56]; a 4-electrode earbud/earmuff build (ESP32-S3, 1 kHz) is
  already on GitHub without published accuracy [61]. Test this form factor early.
- **The subdermal-implant variant has 11-year-old prior art and still no device**: a 2015
  biohack.me proposal for "subdermal EMG electrodes near the throat for subvocal recognition" with
  bone-conduction output [18]. Treat it as a later-stage option, not the first prototype.
- **Every successful result in this space is per-user calibrated and closed-vocabulary.** 8 words
  [16], 4 words [17], 30 words [19], 10 words [56], 15 sentences [4], closed 67 words [24], 8 words
  at ~90%/74.6% [49], 6 words + 10 numbers back in 2004 [50], 100+ words *claimed* but unreported
  [10]. A realistic first milestone for one user is **20–30 closed commands at high accuracy on
  articulated/near-silent speech, then push toward true subvocalisation**.

## Open questions

1. Can this owner produce usable sEMG with **zero visible movement** (true subvocalisation), or
   must the prototype permit near-silent lip/jaw articulation? Every dataset that separates the two
   shows a large gap [16][17]; a same-day A/B recording of both on the owner would settle it.
2. What is the **minimum channel count** for the owner's target vocabulary? Open results use 8
   channels [17][25], 14 [16], and 31 [11]; nobody has published a channel-count ablation on face
   EMG for a *single* user.
3. Can **dry electrodes** hold position on the jaw/neck well enough to skip per-session recalibration
   (the 68→54% drop) [16]? Does a fixed elastic jig or adhesive patch close that gap?
4. Is the **emg2speech / OSF bundle** actually downloadable and under what license? The OSF page is
   JavaScript-only to the fetcher and the repo has no LICENSE file at the README's path [20][23].
5. What closed-vocabulary size is achievable at ≥90% for one user with unlimited calibration data —
   10, 30, 100? MUSE claims "over 100 common words … over 90% accuracy" but has published no
   results [10]; Myovox's open-vocab 18.53% WER is the only open-vocab datum [11].
6. How much does **electrode-site choice on the face/neck** matter versus channel count? The
   AlterEgo-derived montage and PULP's neckband cover different sites; no head-to-head exists in the
   open literature [16][17].
7. Is a **small subdermal implant** actually necessary for an invisible form factor, or is a
   neckband/collar with dry electrodes sufficient? No maker or paper found has built the subdermal
   version [18].
8. Does a **phoneme-level language prior** help at a 30-word closed vocabulary, or is it only useful
   at open vocabulary? Myovox's ceiling result suggests minimal headroom [11].
9. What end-to-end **latency** is acceptable for the bone-conduction assistant loop, and does the
   chosen front-end (MindRove WiFi Direct, OpenBCI BLE) meet it? No latency numbers were published
   on the fetched product pages [28][36].
10. Do the **headphone-earmuff textile EMG** results [56] reproduce outside the authors' setup, and
    will the owner actually wear earmuffs/headphones all day? If yes, this sidesteps the
    face-electrode invisibility problem entirely. Related: can the 4-electrode earmuff build [61]
    be made to report a real accuracy?
11. Are the **science-fair numbers** (WAV 96.7% for < $50 [47]; SpeakUp 80.1% for < $100 [48])
    reproducible, or artifacts of a tiny/leaky dataset? Neither released data or code that was found.

## Sources

1. MIT Media Lab, "AlterEgo — Overview", https://www.media.mit.edu/projects/alterego/overview/ (fetched 2026).
2. MIT Media Lab, "AlterEgo: Frequently Asked Questions", https://www.media.mit.edu/projects/alterego/frequently-asked-questions/ (fetched 2026).
3. MIT Media Lab, "AlterEgo — Publications", https://www.media.mit.edu/projects/alterego/publications/ (fetched 2026).
4. A. Kapur, U. Sarawgi, E. Wadkins, M. Wu, N. Hollenstein, P. Maes, "Non-Invasive Silent Speech Recognition in Multiple Sclerosis with Dysphonia", PMLR 116:25–38, 2020. https://proceedings.mlr.press/v116/kapur20a.html
5. A. Ho et al. (42 Robotics), "Cerebro Voice", Hackaday.io, 2018. https://hackaday.io/project/160715-cerebro-voice
6. W. To, "subvocalization_stream" (Cerebro Voice code) README, GitHub. https://github.com/WesleyTo/subvocalization_stream
7. Hackaday, "subvocal recognition" tag (2 articles: Cerebro Voice 2018; Microsoft SilentVoice 2019), https://hackaday.com/tag/subvocal-recognition/
8. jarvisMonke, "Inner Voice EMG Interface" README, GitHub, 2024. https://github.com/jarvismonke/inner-voice-emg
9. OpenBCI Forum, "Using the ganglion board to read EMG detecting subvocalizations for biofeedback to train suppression", July 2019. https://openbci.com/forum/index.php?p=/discussion/2226/
10. OpenBCI (China), "OpenBCI探索项目：MUSE（基于无声发音的语音解码项目）" (OpenBCI community case study), 2025. https://openbci-cn.com/146.html
11. V. Madishetty, "Myovox: Reading Speech from the Muscles of the Face", arXiv:2609.17548, 2026. https://arxiv.org/abs/2609.17548
12. D. Gaddy, D. Klein, "Digital Voicing of Silent Speech", EMNLP 2020 (Best Paper). https://aclanthology.org/2020.emnlp-main.445/
13. V. Sivakumar et al., "emg2qwerty: A Large Dataset with Baselines for Touch Typing using Surface Electromyography", arXiv:2410.20081, 2024. https://ar5iv.labs.arxiv.org/html/2410.20081
14. K. Xu et al., "Silent Speech Interfaces in the Era of Large Language Models: A Comprehensive Taxonomy and Systematic Review", arXiv:2603.11877, 2026. https://arxiv.org/abs/2603.11877
15. W. K. Deveza, J. B. Ibarra, M. Sejera, "Silent Speech Interface Based on Surface Electromyography Using Arduino and Ensemble Learning", Springer Nature Switzerland, 2026. https://www.springerprofessional.de/en/silent-speech-interface-based-on-surface-electromyography-using-/51520734
16. F. Meier, G. Spacone, S. Frey, L. Benini, A. Cossettini, "A Parallel Ultra-Low Power Silent Speech Interface based on a Wearable, Fully-dry EMG Neckband", arXiv:2509.21964, 2025. https://arxiv.org/abs/2509.21964
17. M. de A. Batista, "subvocalization-emg" (OpenBCI Cyton, BSD 3-clause) README, GitHub. https://github.com/mateusaquino/subvocalization-emg
18. biohack.me forum archive, "A theoretical approach to a pseudo-exocortex", Aug 2015. https://forum.biohack.me/discussions/1037
19. Y. Kurotaki et al., "Soft Active Electromyography Interface for Machine Learning-Enabled Silent Speech Recognition", arXiv:2608.27048 / Advanced Intelligent Systems 2026, e70440. https://arxiv.org/abs/2608.27048
20. H. T. Gowda, "emg2speech" README, GitHub. https://github.com/HarshavardhanaTG/emg2speech
21. H. T. Gowda, D. C. Comstock, L. M. Miller, "emg2speech: Synthesizing speech from electromyography using self-supervised speech models", arXiv:2510.23969. https://arxiv.org/abs/2510.23969
22. H. T. Gowda, L. M. Miller, "Non-invasive electromyographic speech neuroprosthesis: a geometric perspective", arXiv:2502.05762 (v3 2026). https://arxiv.org/abs/2502.05762
23. OSF, emg2speech data project, https://osf.io/bgh7t/ (fetched; page renders JavaScript-only, file list not verifiable).
24. D. Gaddy, "silent_speech" code repository README, GitHub. https://github.com/dgaddy/silent_speech
25. D. Gaddy, "Silent Speech EMG" dataset, Zenodo, DOI 10.5281/zenodo.4064409, 2020 (CC-BY-4.0). https://zenodo.org/records/4064409
26. L. Diener, M. Roustay Vishkasougheh, T. Schultz, "CSL-EMG_Array: An Open Access Corpus for EMG-to-Speech Conversion", INTERSPEECH 2020; corpus page https://www.uni-bremen.de/en/csl/research/silent-speech-communication/csl-emg-array-corpus
27. OpenBCI Docs, "Cyton Data Format". https://docs.openbci.com/Cyton/CytonDataFormat/
28. OpenBCI Docs, "Cyton Specifications". https://docs.openbci.com/Cyton/CytonSpecs/
29. OpenBCI Docs, "Ganglion Specifications". https://docs.openbci.com/Ganglion/GanglionSpecs/
30. OpenBCI Shop product data (Cyton, Cyton+Daisy, Ganglion, Galea). https://shop.openbci.com/products/cyton-biosensing-board-8-channel.json ; https://shop.openbci.com/products/ganglion-board.json ; https://shop.openbci.com/products/cyton-daisy-biosensing-boards-16-channel.json ; https://shop.openbci.com/products/galea.json
31. Upside Down Labs Docs, "BioAmp EXG Pill" and "Muscle BioAmp Shield". https://docs.upsidedownlabs.tech/hardware/bioamp/bioamp-exg-pill/index.html ; https://docs.upsidedownlabs.tech/hardware/bioamp/muscle-bioamp-shield/index.html
32. Upside Down Labs Store, "BioAmp EXG Pill" and "Muscle BioAmp Band". https://store.upsidedownlabs.tech/product/bioamp-exg-pill/ ; https://store.upsidedownlabs.tech/product/muscle-bioamp-band/
33. SparkFun, "Getting Started with the MyoWare 2.0 Muscle Sensor Ecosystem". https://learn.sparkfun.com/tutorials/getting-started-with-the-myoware-20-muscle-sensor-ecosystem/all
34. SparkFun, "MyoWare Muscle Sensor Kit" (MyoWare 1.0, retired). https://learn.sparkfun.com/tutorials/myoware-muscle-sensor-kit/all
35. MindRove, "EMG Armband 2". https://mindrove.com/product/emg-armband-2/
36. MindRove, "Sense XR Face + Brain — EEG/EMG interface for Meta Quest 2/3/3S". https://mindrove.com/product/sense-xr-face-brain-eeg-emg-interface-for-meta-quest-2-3-3s-vr-headsets/
37. MindRove Docs (SDK, license, API). https://docs.mindrove.com/
38. Delsys, Trigno product family (Centro, Avanti, Galileo). https://delsys.com/products/ ; https://delsys.com/product/trigno-centro/ ; https://delsys.com/trigno-galileo/
39. N. Rosenstein, "myo-python" (Thalmic/North Myo, discontinued 2018; MIT license) README. https://github.com/NiklasRosenstein/myo-python
40. OYMotion, gForcePro+ / gForceOct product pages. https://oymotion.com/en/product32/149 ; https://oymotion.com/en/product32/148
41. PLUX Biosignals, BITalino EMG sensor and product list. https://www.pluxbiosignals.com/products/electromyography-emg-for-bitalino.json
42. NeuroSky Store, "MindWave". https://store.neurosky.com/pages/mindwave
43. Emotiv, Cortex API documentation. https://emotiv.gitbook.io/cortex-api/
44. g.tec, g.Nautilus Research wireless EEG system. https://www.gtec.at/product/gnautilus-research-wireless-eeg-system/
45. Brain Products, LiveAmp. https://www.brainproducts.com/solutions/liveamp/
46. Muse, Developer portal. https://developer.choosemuse.com/ (redirected; specs/pricing **unverified**)
47. A. Sesetty, "WAV: A Novel Subvocalization Interpretation Device", Regeneron ISEF abstract, Society for Science. https://abstracts.societyforscience.org/Home/PrintPdf?projectId=21187 (PDF fetched by the research pass; competition abstract, self-reported)
48. V. Chandrashekhar, "SpeakUp: A Machine Learning-Based Speech Aid to Enable Real-Time Silent Communication for the Paralyzed…", Regeneron STS presentation PDF. https://mms.kyscience.org//members/publication/docs/PROP32491437-SpeakUp-Science_Fair_Presentation-Varun_Chandrashekhar.pdf (PDF fetched; the Hackster page https://www.hackster.io/Varun_Chandrashekhar/speakup-ml-based-speech-aid-to-enable-silent-communication-ffd9f8 returned HTTP 403 — **unverified**)
49. K. Mirok, "MindScribe: Innovation Report", Youth Science Summit / sciencefairs.ca, 2025. https://sciencefairs.ca/wp-content/uploads/2025/10/YIS2025_Semi_Mirok_Report.pdf (PDF fetched by the research pass)
50. C. Jorgensen (NASA Ames), subvocal speech, 2004 — reported via a news reprint and the Stanford HCI seminar abstract (original NASA URL dead). https://hci.stanford.edu/seminar/abstracts/05-06/060217-jorgensen.html (secondary source; "92 percent accuracy six words and 10 numbers" — **unverified primary**)
51. Riddlecraft Engineer, "Detecting Facial Muscle Signals Using EMG and Arduino Uno", YouTube, 2025. https://youtu.be/-20ZNmy9XG8 (metadata/description only; no accuracy reported)
52. E. Sun, "Silent Speech Interface", Imperial College MSc project video, 2022. https://youtu.be/sPrt58o1qEI (metadata/description only)
53. J. Carvalho, "Partial_DSP_implement_of_AlterEgo_Paper" (MIT license), GitHub. https://github.com/joaocarvalhoopen/Partial_DSP_implement_of_AlterEgo_Paper
54. PiEEG, "Octopus 16" (16-ch, 24-bit kit, $70 / $90 with neckband; "Whisper (Silent Speech) … throat EMG" claim), Indiegogo campaign — page returned HTTP 403 to the fetcher — **unverified**
55. Reddit, r/TargetedEnergyWeapons post (id `kowzpc`) reporting that the Berkeley "Digital Voicing" dataset used an OpenBCI Cyton; accessed via a Reddit mirror — **secondary/unverified**
56. C. Tang, J. Mallah, D. Kazieczko, W. Yi, T. R. Kandukuri, E. Occhipinti, B. Mishra, S. Mehta, L. G. Occhipinti, "Wireless Silent Speech Interface Using Multi-Channel Textile EMG Sensors Integrated into Headphones", arXiv:2504.13921, 2025 (IEEE TIM 2025). https://arxiv.org/abs/2504.13921
57. Meta Reality Labs, `facebookresearch/emg2qwerty` GitHub repository. https://github.com/facebookresearch/emg2qwerty
58. Meta Reality Labs, `facebookresearch/emg2pose` GitHub repository. https://github.com/facebookresearch/emg2pose
59. P. Mohapatra, `payalmohapatra/SilentSpeechLLM` (MIT license), GitHub, 2025. https://github.com/payalmohapatra/SilentSpeechLLM
60. `bigdatasciencegroup/AlterEgo` GitHub repository (no license), 2019. https://github.com/bigdatasciencegroup/AlterEgo
61. `luffy101-hash/silent-speak-emg` (MIT license), GitHub, 2026. https://github.com/luffy101-hash/silent-speak-emg
62. `Elesdes/EMG2Speech-LiquidNet` (Apache-2.0), GitHub. https://github.com/Elesdes/EMG2Speech-LiquidNet
63. `brainflow-dev/brainflow` (MIT license), GitHub — unified biosignal acquisition SDK. https://github.com/brainflow-dev/brainflow
64. `upsidedownlabs/BioAmp-EXG-Pill` open-hardware repository, GitHub. https://github.com/upsidedownlabs/BioAmp-EXG-Pill
65. `BITalinoWorld/revolution-python-api` (GPL-3.0), GitHub. https://github.com/BITalinoWorld/revolution-python-api
66. emg2qwerty community derivatives with reported CER: `shivk-1/emg2qwerty` https://github.com/shivk-1/emg2qwerty ; `KunwooLeeKay/emg2qwerty` https://github.com/KunwooLeeKay/emg2qwerty ; `LLeon360/emg2qwerty` https://github.com/LLeon360/emg2qwerty ; `vishar0/emg-tokenizer` https://github.com/vishar0/emg-tokenizer (READMEs fetched by the research pass)

---

*Track file complete for the sources verified above. Items explicitly marked **unverified** were not
fetchable (Cloudflare 403, PDF-only, JS-only, or redirect-blocked) and are flagged as such in-line.*
