# Track 02 — Sensing modalities for a nearly-invisible silent-speech interface

Working report. Status: complete (sections 0–9, 102 sources). All numbers are quoted from the cited source; **demonstrated**
results and **claims/marketing** are kept separate per BRIEF.md.

Scope: which sensing modality can (a) decode *silent* or near-silent speech and (b) stay nearly
invisible on the face/head. Candidate modalities: surface EMG (face/submental/neck), ultrasound
tongue imaging (UTI), permanent-magnet articulography (PMA) and EMA, in-ear sensing (ear-canal
deformation, in-ear EMG, in-ear microphones for non-audible murmur), NAM microphones and throat/skin
accelerometers, radar/RF/mm-wave/Wi-Fi, strain/e-skin sensors on the throat, camera-based visual
speech recognition (lip reading), EEG/fNIRS/MEG.

## 0. How modalities are judged here

The owner's constraints (from BRIEF.md) turn "best accuracy" into a constrained optimisation:

| Criterion | Why it matters for this owner |
|---|---|
| Silence | Must work when the user produces *no audible sound* and ideally *no visible articulation* (used in public, in conversation). |
| Visibility on the face | "Barely different from normal face" is a hard constraint; a headset with visible tentacles fails it. A small subdermal implant is the fallback. |
| Per-user calibration | Long calibration is explicitly allowed, so a modality that is weak zero-shot but strong per-user is acceptable. |
| DIY feasibility | One hired EE + one user. No clean-room fab, no surgical suite except possibly a small subdermal implant. |
| Output path | Bone-conduction / in-ear audio is in scope, so an ear-mounted sensor that shares the audio path is attractive. |

Two definitions recur and are easy to conflate. **Silent speech** = speech intent with no audible
sound; in practice it splits into *subvocal* (some muscle/vocal-fold activity, no sound), *mouthed*
(articulators move, no sound) and *whispered* (audible but quiet, no voicing). Meltzner et al. (2008)
name exactly three modes: "1) vocalized ... 2) mouthed – with articulation but no vocal tract
excitation (no voice), and 3) mentally rehearsed – ... without articulator movement or voice
production" [76]. Wand et al. (2014) warn that whispered speech is "of course, also audible" and
define silent speech as "the speaker performs normal articulatory movements while suppressing the
glottal airstream" [70]; Rosello et al. define subvocalization as "silent internal speech produced
while reading... characterized by small movements in facial and laryngeal muscles measurable by
surface electromyography" [71]. **Terminology warning:** in most silent-speech-interface papers
"silent speech" means what this brief calls *mouthed*; the brief's stricter "no articulator
movement" matches Meltzner's *mentally rehearsed*, and EEG is the only modality aimed at that. The
phrase "voiced-but-inaudible" was not defined in any source fetched [unverified].

A 2025 review of silent-speech sensing distinguishes off-body, on-body and in-body sensing and
argues that "on-body systems currently offer the best balance between accuracy and deployability,
whereas in-body approaches provide unmatched neural access for individuals with complete loss of
articulation" [1]. This track follows that off/on/in-body split. A 2026 systematic review adds that
SSIs have "for the first time, approached the Word Error Rate usability threshold required for
real-world deployment", mostly via multimodal sensing + large models [74].

A second framing: the modality determines how much of the speech-production chain you observe.
Acoustic and NAM/accelerometer sensors observe *air or tissue vibration* (needs some sound or
vibration); sEMG observes *muscle activation* (works when mouthed/subvocal, not when purely
imagined); UTI/EMA/PMA observe *articulator position* (works when mouthed); camera observes
*visible articulation*; EEG observes *cortical intent* (works when nothing moves, but with poor
SNR). The more downstream the sensor, the more silent the user can be and the harder the decoding.

## 1. Surface EMG (face / submental / neck)

**How it works.** Electrodes on the skin pick up the electrical activity of the speech muscles
(laryngeal, hyoid, digastric, orbicularis oris, levator anguli oris, platysma, mentalis). It is a
*muscle* signal: it requires the user to send motor commands to the articulators, so it covers
mouthed and subvocal speech but not pure "thinking". Signals are small (tens to hundreds of µV) and
need good skin contact.

**AlterEgo (the reference point in the brief).** Kapur, Kapur & Maes, IUI 2018 (the brief says
"Kapur et al., 2018" — correct; note it is IUI, not UIST). The abstract reports "92% median word
accuracy levels" [2]. Details from the paper: **7 channels**, sourced from "the laryngeal region,
hyoid region, levator anguli oris, orbicularis oris, platysma, anterior belly of the digastric,
mentum"; signals "sampled at 250 Hz and differentially amplified at 24× gain (Texas Instruments,
OpenBCI)"; "gold plated silver electrodes (1.45 mm diameter conductive area), in combination with
Ten20 ... or passive dry Ag/AgCl electrodes (4 mm diameter)"; recognition ran **off-device**
("wirelessly sent to an external computing device") [2]. Mode was **silent internal speech** — users
were told to "read the number to themselves, without producing a sound and moving their lips" — with
a **closed vocabulary** of digits and operators [2]. The 10-user study reports "The average accuracy
over all runs for all the users is 92.01%" with "0.427 seconds" latency, from "~31 hours of silently
spoken text" [2]. MIT News adds the hardware story: a 16-electrode search over facial locations,
with 7 chosen, mounted on a neck-wrapping headset with "tentacle-like curved appendages that touch
the face at seven locations on either side of the mouth and along the jaws"; "about 20 words each"
vocabulary [3]. A follow-up in multiple sclerosis used "8 signal electrodes - 4 on the face and 4 on
the neck" with 3 patients, 15 sentences, "mean accuracy of 0.81" [6]. **Demonstrated but closed
vocabulary, per-user.**

**sEMG at larger vocabularies.**
- Wand, Toth, Jou & Schultz (2009) is the cautionary result: 78 speakers, 8-channel Varioport at
  600 Hz, silent = "voicelessly mouthed"; for most speakers silent-mode "word error rates (WER)
  exceed 80%", best "30.10%" for one speaker with prior silent practice [7]. (The commonly cited
  "Toth 2009 SVM" paper could not be verified on the author's publication list; the real Toth 2009
  paper does EMG-to-speech synthesis, 5 channels, 15.7–19.2% WER on generated audio [8].)
- Meltzner et al. 2018 is the strongest classic number: 11 sEMG sensors ("7 sensors were placed on
  the neck and chin (#1-7 submental) and 4 sensors were placed on the face (#8-11)"), 19 subjects,
  "2,200-word" vocabulary, "more than 1,200 continuous phrases", **"8.9%-word error rate (91.1%
  recognition rate)"**, mode "subvocal"/"silently mouthed", sessions "4-6 hours" [9]. This is
  **open vocabulary** (phoneme models), speaker-dependent.
- Gaddy & Klein (EMNLP 2020) trained on silent EMG by transferring audio targets from vocalized
  speech: "Eight channels ... at a sample rate of 1000 Hz"; closed 67-word vocabulary WER fell
  "from 64% to 4%" and open 9,828-word vocabulary "88% to 68%" [10]. This is EMG→voice conversion,
  not sensor fusion.
- MONA LISA (2024) reports open-vocabulary silent sEMG WER improved "from 28.8% to 12.2%" on the
  Gaddy benchmark, calling it the "first instance where noninvasive silent speech recognition on an
  open vocabulary has cleared the threshold of 15% WER" (vocal EMG: "23.3% to 3.7%") [11].
- emg2speech (2025): "31" electrodes at 5000 Hz, ~9 h, "over 6,800 unique words"; human-transcription
  WER of synthesized speech "62.55±2.40%" healthy and "50.82±1.59%" ALS [12].
- Janke & Diener (2017) generate speech directly from facial sEMG (specific WER not verified;
  abstract only) [15]; Scheck et al. (2025) report silent 8-channel EMG character error rate "46.0"
  [16].

**Form factor / invisibility.** Face electrodes are the accuracy leader but are visible. The
necklace study (Wu, Kaveh et al., Interspeech 2024) moved them: "dry electrodes are placed around
the neck instead", and an "11-word, multi-speaker **voiced** EMG" classifier reached "92.7%
accuracy"; ablations show "the importance of having more than two electrodes on the neck" [4]. A
neck band or a jawline-mounted strip is compatible with "barely different from normal face"; pasted
electrodes on the mouth are not. Adjacent non-invasive neuromotor work (Meta/CTRL-labs wristband,
Nature 2025) reaches "0.66 target acquisitions per second" and "handwriting at 20.9 words per
minute", but decodes hand movement, not speech [69]. Gel beats dry on signal quality [2]; Meltzner's protocol required
"shave coarse facial hair and remove excessively dry skin by repeated hypoallergenic tape peels" [9]
— a real daily-life problem for a 1-user build.

**DIY feasibility.** One user could start today: OpenBCI Cyton (8 ch, "250Hz", "$1,249.00",
"0.298 microvolt/bit") [13], OpenBCI Ganglion (4 ch, "200Hz", "$624.99") [13], MyoWare 2.0 muscle
sensor ("$43.50"), Backyard Brains Human SpikerBox ("$299.99"), or research-grade Delsys Trigno (used
by Meltzner) [9]. Gaddy's full pipeline and "nearly 20 hours" single-speaker dataset are open
(CC-BY-4.0) [10][72], and EMG-UKA (8 speakers, 7:32 h) is partly free [70]. A 3-minute calibration
was enough for one 2026 8-channel montage to reach "20.5% character error rate (CER) and 31.7% word
error rate (WER)" on a 50-sentence closed set, not significantly better with ~13 min [75].

**Commercial claim.** In September 2025 a startup also called AlterEgo launched a headset that
"hooks around the ear and runs along the jawline", reading subvocalisation and replying over bone
conduction; Kapur is CEO, Max Newlon COO [5]. The company site says "the first near-telepathic
interface", shows a "pre-production prototype", and publishes **no accuracy number** — marketing,
not evidence [14].

## 2. In-ear sensing, NAM microphones, throat/neck vibration and strain

This family is attractive because the sensor disappears into an earbud or under a collar. The catch
is that most of it senses *sound or vibration produced somewhere*, so it spans the line from
"inaudible" to "whispered" rather than genuinely silent.

**Non-audible murmur (NAM).** Nakajima et al. (2003) defined NAM recognition as "recognition of
inaudible speech produced without vibration of the vocal folds", using a stethoscope-principle
microphone adhering to the skin [17]. Heracleous et al. (2004) attached a stethoscopic NAM mic
"behind the talker's ear" that "cannot be heared by listeners near the talker", reaching **93.5% word
accuracy** with MAP adaptation on a 20k-vocabulary Japanese dictation task (one male speaker, 1,800
NAM training utterances, 24 test utterances) [18]. Heracleous et al. (2005) report "stethoscope NAM
88.9%", "silicon NAM 93.9%" vs "normal speech 96.2%" (350 train / 48 test NAM utterances), and a
25-keyword spotter at "88.2% detection ... allowing 4 false alarms per keyword" [19]. Nakajima et al.
(2005) redefined NAM as "flesh conducted soft whisper" picked up "low behind the earlobe"; body
tissue is a low-pass filter (5 kHz attenuated "by almost 36dB compared with 1kHz"), and a listening
test found meaningless-word NAM intelligibility "extremely low" [20]. A 2024 successor (StethoSpeech)
turns "flesh-conducted vibrations behind the ear into speech" with an off-the-shelf clinical
stethoscope [33]. **So NAM is genuinely inaudible-to-bystanders, ear-mounted and invisible — but the
demonstrated recognition numbers come from small test sets and a 20k dictation vocabulary is not the
same as open conversational speech.**

**Ear-canal deformation.** EarSSR (IEEE TMC 2024) uses the earphone's own microphone and speaker to
sense "sub-millimeter" ear-canal deformation from jaw motion (canal volume changes by "almost
20 mm³"); for **silent** speech it reports "82% for single alphabetic letter recognition and ... 93%
for word recognition" over "26 alphabets" and "50 words and phrases" with "50 volunteers" [21].
EarCommand (IMWUT 2022) reports WER "10.02% for word-level recognition and 12.33% for sentence-level
recognition" with "32 word-level commands and 25 sentence-level commands" [22]. Both are earbud-only,
therefore invisible. JawSense (2021) classifies "nine phonemes" from "unvoiced jaw movement" at "92%
phoneme classification rate" with six subjects [23].

**In-ear EMG.** A promising but unproven branch: OpenEarable ExG is an open platform with "up to 7
sensing channels" in and around the ear, validated on EOG and EEG, **not** a silent-speech demo [24].
A textile-electrode earmuff study (around-ear, not canal) reports "96% accuracy on 10 commonly used
voice-free control words" with "4 subjects" [34]. The frequently cited names "EarEMG", "EarFSR",
"Oreo" and a CMU/Lopez "in-ear" system could not be verified and should be treated as misnamed or
non-existent [24].

**Throat/skin vibration and strain.** A throat microphone on soft whisper (audible) improved WER
"from 99.3% to 32.9%" with adaptation (Jou et al. 2004) [28] — note "soft whisper", not silent.
Textile strain sensors are the strongest recent throat result: a graphene-flake choker with a "gauge
factor [that] exceeds existing state-of-the-art strain sensors by 420%" and "100% unresponsive to
environmental sound noise" reached "95.25% for a lexicon of 20 words from 3 participants", still 90%
with "as few as 30 samples per class" [25]; a follow-up with carotid pulse reports "4.2% word error
rate, 2.9% sentence error rate" after fine-tuning on stroke patients (preprint) [26]. Kim et al.
(Nature Communications 2022) placed "four strain sensors near the subject's mouths" and classified
100 words at "87.53%", versus "42.60%" for a same-size sEMG comparison [27]. Jaw-motion IMUs work
too: "Unvoiced" (SenSys 2024) uses a "twin-IMU earable" to reach ">94% task completion rate and <9%
word error rate for over 90% of phrases" across "19 users" [29]; QuietSync (ICMI 2024) combines
headphone IMU + contact ExG for "12 commands with an accuracy of 94.2%" (no unimodal ablation, so
the fusion gain is unverified) [30]. In-ear magnetosensing (EarMag 2025) is only at "76% accuracy
for five exercises" and is gesture, not speech [31]. **Correction worth recording: NeckFace (IMWUT
2021) is an infrared-camera facial-expression neckband, not a silent-speech sensor [32].**

## 3. Articulator tracking: ultrasound tongue imaging (UTI), EMA, PMA

These measure *where the tongue/lips are*, which is the most physically informative signal for
mouthed speech — but they require hardware on or in the vocal tract.

**UTI.** Florescu et al. (Interspeech 2010) is the canonical portable silent UTI result: a Terason
T3000 with an "8MC4 140° micro-convex transducer" plus lip camera, "60 fps" ultrasound at
"320x240", mounted via an "ultrasound probe stabilization helmet"; **50 French words**, silent
("maintain a glottal closure ... so that no sound is produced"). Silent→silent word recognition was
**"64.5% ± 6.5%"** (fixed rig 65.3%), vocalized→vocalized 75.3%, and cross-mode only ~42–46%;
tongue-only silent 57.3%, lips-only 34.7% [35]. Hueber's 2009 thesis gives continuous-speech phone
accuracy of "70.8" (ultrasound-only "70.8" vs video-only "43.6") with a constrained "3000 mots"
lexicon [36]. Newer synthesis work is blunt about silence: Gosztolya et al. (SSW 2025) report
phonetic error rate rising from "18.8%...21.6%" (original) to "51.5%...64.9%" (audible) to
"86.0%...91.7%" (whispered) to "96.0%...96.9%" (silent normal articulation) [51]. Hardware is bulky:
the Articulate Instruments stabilising helmet + probe weighs "1.3 kg" total with "1.5Hrs" battery
[41], and even the small Interson USB probe is "15.5 cm by 3.5 cm", 100 g and only "15 fps" [41].
UltraSuite/TaL provide large open corpora (TaL80: "81" speakers, "16639" utterances; ~13.5 h of
speech) [39][40][73]. **Verdict: real silent-speech capability, but the under-chin probe on a
headset is a visible, bulky accessory — the opposite of the owner's constraint — and no cheap probe
price was verified [41].**

**EMA.** Coils are glued to the lips and tongue; the Carstens AG501 offers "8/16/24 channels" at
"1250Hz" with "RMS of 0.3mm" [42]. The cleanest silent demonstration is Wang, Samal & Green (2014):
participants "mouthed (silently articulated) phrases" with an NDI Wave at "100 Hz" and "0.5 mm"
accuracy; closed-vocabulary phrase accuracy was "100%", "96.67", "96.67" for three speakers with
latencies of 1.4–3.1 s [43]. Datasets exist (MNGU0: 6 coils, "1,354 utterances", ~67 min [52];
EMA-MAE: 40 speakers, "400 Hz" [53]). **Verdict: excellent mouthed accuracy on tiny phrase sets,
but glue-on coils in the mouth are not a wearable the owner can use in public.**

**PMA (permanent-magnet articulography).** Small magnets on lips and tongue tracked by magnetometers
on a headset. Fagan et al. (2008) report **"97% for words and 94% for phonemes"** with 6 dual-axis
sensors in "a pair of special glasses", mouthed speech, small vocabulary [44]. Gilbert et al. (2010,
MVOCA) report "over 90% ... for vocabularies of at least 57 isolated words" with magnets "on the
tongue and lips" [45]. Hofe et al. (2010) used "seven magnets, four on the lips, one on the tongue
tip and two on the sides of the tongue" plus "six magnetic field sensors ... 12 data channels",
reaching "98.7%" on 57 words — but words were **read aloud**, i.e. voiced recording with
sensor-only recognition [46]; the 2013 multi-speaker follow-up used "five magnetic field sensors ...
15 channels" and was also voiced [47]. Cheah et al. (2018) quantifies the fatal weakness of
on-the-body magnets: with head motion and no cancellation, recognition "deteriorates significantly
(down to about 2%)" [48]. A 2023 alternative avoids oral magnets entirely: a "single soft magnetic
skin placed behind the ear" tracking the temporomandibular joint gives "93.2% accuracy for phonemes,
and 87.3% for a list of words from the same viseme groups" [50]. Gonzalez et al. (2016) give the
direct-synthesis counterpart on TIDigits with 3 speakers ("5.54"/"10.50"/"8.46" minutes of data,
MCD "4.8"–"6.4" dB) [49]. Magnets were fixed with
"Histoacryl surgical tissue adhesive", and the authors suggest a biocompatible coating would allow
permanent implantation [48]; a dedicated long-term tongue-magnet safety study was not found
[unverified].

## 4. Intraoral sensors (EPG / optopalatography) and hidden jaw sensors

If invisibility is the top priority, the sensor can go inside the mouth. **SilentSpeller** (CHI
2022) uses a dental retainer with "124 electrodes ... at 100 Hz": "97% character accuracy (93% word
accuracy)" offline, live "37 words per minute at 87% accuracy" over seven participants, and "94%
accuracy (86% word)" on 100 unseen words — silent "unvoiced spelling" against a 1164-word dictionary
[54]; a 2021 demo claimed "up to 53 words per minute and 90% accuracy" [55]. The commercial
CompleteSpeech SmartPalate is the same idea ("a customized retainer equipped with 124 sensors") with
no public list price [56][57]. Optopalatography (optical distance sensors embedded in a pseudopalate)
reported "98.38% accuracy on a single speaker 40-word corpus" for silent articulation [61]; Birkholz
& Neuschaefer-Rube describe the "thin acrylic pseudopalate with embedded contact sensors ... and
optical distance sensors" [62]. A completely hidden optical option is glasses with IR distance
sensors at cheek/jaw joint/jaw: 10 participants, 5 commands, silent-speech F-score "0.90" vs "0.86"
for voiced [60]. The Augmental MouthPad ("$1,400" / "$1,900", "~10 g", "7+ hours") is the same
form-factor family and is *invisible and shipping*, but it is a tongue/head pointer, not speech
decoding [58]. **Verdict: unmatched invisibility and the best demonstrated silent accuracy-per-word
for a small dictionary, but it needs a custom dental appliance (a maker/dentist dependency the owner
must accept) and it is closed-vocabulary spelling, not open speech.**

## 5. Acoustic eyewear and wearable ultrasound

**EchoSpeech (CHI 2023)** is the strongest "invisible" result that is not in the mouth: active
acoustic/FMCW sonar from "two speakers ... and two microphones on either sides of the frame" of
ordinary eyewear. It recognises "31 isolated commands" and 3–6-figure connected digits at
**"4.5% (std 3.5%) and 6.1% (std 4.2%) Word Error Rate"**, with a small amount of new-user data
("1-6 minutes" in the abstract, "6-7 minutes" in the introduction [38]) giving "9.5% and 14.4% WER"
for new users; 12 participants, "23808 valid silent utterances"; power
"73.3mW" [38]. Participants were told to "mouth the word silently". It is **not** ultrasound tongue
imaging (echo sonar, 18–24.5 kHz) [38]. Caveats: closed vocabulary (31 commands; digits), short
range, and it needs glasses with speakers/mics — but that is a normal-looking object.

**SottoVoce (CHI 2019)** is the opposite trade-off: a real "3.5-MHz convex-type ultrasonic imaging
probe under the jaw" at "30 frames per second" with a lab display; ~500 commands, silent, and the
best smart-speaker success rate was "65.0%" vs "90.0%" ground truth, with "WER ... 41.03%" for one
network [59]. Not wearable.

## 6. Fusion

Reviews are consistent that no single on-body modality wins on every axis and that fusion is the
intended path. Denby et al.'s 2010 review (the field's founding survey, covering EMA,
ultrasound+optical imaging, NAM, glottal sensors, sEMG, EEG and implants, each scored 1–5 on six
axes) concluded "no SSI technology today proposes a device responding fully to all six axes" and
recommended "combine technologies in a multi-sensor device and perform data fusion" [37]. The 2025
Nature Sensors review reaches the same conclusion, e.g. "EMG signals capture neuromuscular intent but
are motion-sensitive, while strain sensors track tissue deformation... Fusing the two allows decoding
models to contextualize signal quality" [1]. Earlier surveys by Schultz et al. (2017) [63] and the Freitas et al. (2017) book, which has a
"Combining Modalities: Multimodal SSI" chapter [77], cover the same ground. Gonzalez-Lopez et al.
(2020) add the reality check: "most present-day SSIs have only been validated in laboratory
settings for healthy users" [64]. Point-tracking fusion on the same ultrasound+lip data improved
WER "by 23.06%" over the image-based system, with the silent subset reaching "47.15%" [67].

Measured fusion gains (each on its own dataset, so not a fair head-to-head):
| Fusion | Single-modality | Fused | Source |
|---|---|---|---|
| sEMG + lipreading | sEMG 94.1% WER, lips 57.2% WER | 40.5% WER (phone acc 76.3%) | [75] |
| EEG + sEMG | sEMG 10.52% CER, EEG 38.85% CER | 7.22% CER | [68] |
| Ultrasound + lip video | — | 17.4% → 6.4% WER (2010 rig vs deep-learning update, same pair) | [65] |
| EMG + IMU (QuietSync) | no unimodal baseline published | 94.2% on 12 commands | [30] |
| Modulation-only baseline | silent ultrasound ~39.34% vs 77.79% modal | adaptation recovers a lot of the silent gap | [66] |

The practical pattern: **fusion buys most where modalities fail differently** — sEMG is good at
phoneme identity but motion-sensitive [1][75], strain/IMU is good at jaw/tissue motion but has poor
spectral detail [25][29], and a microphone/NAM is cheap but only captures audible murmur. Also
important: two "fusion" claims in the brief are weak. Gaddy & Klein 2020 is not sensor fusion but
EMG→voice target transfer [10], and the very large reported UTI+lip numbers [65] are a
pre-2018 lab TIMIT result, not a wearable.

## 7. Radar / RF / Wi-Fi and camera lip reading

**RF/radar.** These sense lip/jaw motion remotely, so on the face they are literally invisible —
the sensor is a device elsewhere (a room, a phone, a tag). But that also means the user is tethered
to infrastructure rather than wearing the sensor.
- **WiHear** (2.4 GHz Wi-Fi CSI) reads mouth motion while the user *speaks*: "detection accuracy of
  91% on average for single individual speaking no more than 6 words and up to 74% for no more than
  3 people talking simultaneously", with a pre-defined ~14-syllable vocabulary; it works through
  walls but is voiced, not silent [78].
- **mSilent** (mmWave radar, IMWUT 2023) is the strongest silent result here: "speak to the device
  without making a sound", "1,000 daily conversation sentences", "a 9.5% average word error rate
  (WER) at a distance of 1.5m" [83]. Abstract-only; needs a radar unit aimed at the face.
- **Lip-Siri** (2026) uses Wi-Fi backscatter tags and **silent** lip-reading: 15 participants, 340
  sentences / 3,398 words, "85.61% accuracy on word prediction and a WER of 36.87% on continuous
  sentence recognition", but only "within 50 cm of the backscatter tags" [79].
- **HearMe** (RFID, 20-word vocabulary, "accuracy higher than 0.88") [80] and an **RFID face tattoo**
  (mouthed gestures; "86% accuracy in reconstructing the top-100 words") [81] are tag-based and
  hideable; RF-Mic (RFID on the glasses bridge) eavesdrops on *live voice* [82].
- **RaSSpeR** (contactless radar, 13 words, 3 speakers) reached "an average accuracy of 0.826" [85];
  through-wall TWLip variants claim mask penetration but published WERs are not in their abstracts
  [84]. **Google ATAP Soli** is a 60 GHz gesture/vital-sign sensor; no Soli speech or lip-reading
  demo was found [86] — absence of evidence, not proof of absence.

**Camera-based visual speech recognition (VSR).** LipNet (2016) is the demo everyone quotes: on the
constrained GRID corpus ("64000 possible sentences", 51-word vocabulary) it reached "95.2% accuracy
in sentence-level, overlapped speaker split task" with WER 4.8% overlapped / 11.4% unseen; the
comparison is hearing-impaired lipreaders at 47.7% WER [87]. On open, natural vocabularies the
numbers collapse: on LRS (118,116 utterances, 17,428-word vocabulary) lips-only was "CER 39.5% /
WER 50.2% / BLEU 54.9" versus "17.7% WER" audio-only [88]; video-only LRS2-BBC WER 48.3% and
LRS3-TED 58.9% in 2018 [89], improved by AV-HuBERT to lip-reading WER "32.5%" (30 h labels),
"28.6%" (433 h) and "26.9%" (433 h + self-training) on LRS3 (AV-HuBERT uses audio in *pre-training*
only) [90]. Whisper is audio-only and reports no visual LRS numbers [91]. Robustness is the real
blocker: frontal WER 56.4% degrades to 62.8% in profile, and a frontal-only model falls to 82.6%
WER in profile [92]; low light and masks break it [79]. **Glasses- or ear-mounted VSR** is exactly
the invisible form factor the owner wants, but only weak, number-less records were found
[unverified].

## 8. EEG, fNIRS and MEG — why this fails for this build

EEG is the only non-invasive modality that could in principle read *mentally rehearsed* speech (the
brief's strictest silence), so it matters. The evidence is that it cannot decode words.
- **KaraOne** (14 participants, EEG + face + audio) reports "up to 90% accuracy in classifying
  imagined consonants from imagined vowels and up to 95% ... stimulus from active imagination
  states" — these are **binary** discriminations, not word decoding [93].
- The **Inner Speech** dataset (10 participants, 136 channels, inner-speech commands) is a data
  descriptor; the authors do not demonstrate above-chance word decoding [94].
- **Défossez et al. (2023)** decode *perceived* (listened) speech from non-invasive recordings: MEG
  "up to 41% accuracy out of more than 1,000 distinct possibilities ... more than 80% in the very
  best participants", but EEG only "up to 19.1% top-10 accuracy (out of 2,604 segments)" [95] —
  and this is perception, not silent production. (The commonly cited "Broderick MEG" result is
  labelled EEG in that paper's Table 1 and concerns perception [95].)
- **Reviews** put imagined-speech EEG in context: subject-dependent accuracies "50.0% to 94.0%
  (average 71.9%)" and subject-independent "53.1% to 76.7% (average 68.0%)" on KaraOne, with
  cross-subject accuracy dropping "markedly" [97]; complex multiclass tasks perform "as low as
  26.7%", and EEGNet/SPDNet "often underperformed (24.79–66.93%)" [96]. Hybrid EEG-fNIRS improves to
  "53% ... to 70.45±19.19%" [96]; fNIRS-only thought-to-LLM work publishes no accuracy in its
  abstract [102]. Stated causes: low spatial resolution, skull/scalp attenuation and volume
  conduction, low SNR, non-stationarity, inter-subject variability, small datasets [96][97].
- **Contrast — invasive works.** Intracortical/ECoG systems decode attempted or mimed speech:
  50-word vocabulary at "15.2 words per minute, with a median word error rate of 25.6%" (Moses 2021)
  [99]; "9.1% word error rate on a 50-word vocabulary ... 23.8% ... on a 125,000-word vocabulary",
  "62 words per minute" (Willett 2023) [100]; ECoG synthesis during silently mimed sentences
  (Anumanchipalli 2019) [98]. fMRI can reconstruct perceived *and* imagined speech semantics but
  "subject cooperation is required both to train and to apply the decoder" [101].
- **Form factor.** EEG caps/electrodes are visible and gel-dependent; ear-EEG hides the electrodes
  but worsens an already marginal SNR [24]. **Verdict: EEG cannot carry this build; it is slower,
  less accurate and more visible than sEMG for the same "silent" use case.**

## 9. Ranked recommendation for this owner

Scoring the owner's constraints (silence, face-invisibility, per-user calibration allowed, DIY by
one EE, one user) against the demonstrated numbers:

| Rank | Modality | Best demonstrated (silent/mouthed) | Face visibility | DIY difficulty | Why this rank |
|---|---|---|---|---|---|
| 1 | **sEMG, neck/jawline first, face optional** | AlterEgo 92.01% closed ~20-word [2]; Meltzner 8.9% WER open 2,200-word [9]; MONA LISA 12.2% open WER [11] | Neck band or jawline strip ≈ invisible; face electrodes visible | Low (OpenBCI $625–1,249 [13], open dataset [10][72]) | Only modality with both large-vocabulary silent evidence and a hidden form factor; dry electrodes + per-user training fit the brief |
| 2 | **Active acoustic eyewear (EchoSpeech-style)** | 4.5%/6.1% WER, 31 commands + digits, mouthed, 12 participants [38] | Normal glasses; fully invisible as "speech tech" | Medium (COTS frame + 2 speakers + 2 mics) | Best invisibility-per-accuracy; pairs naturally with bone-conduction output; closed vocabulary is the limit |
| 3 | **In-ear (ear-canal deformation / in-ear EMG / NAM)** | EarSSR 82% letters / 93% 50 words silent [21]; EarCommand 10.02% word WER [22]; NAM 93.5% on 20k dictation (small test) [18] | Earbud; fully invisible; shares audio path | Low–medium (earbud + DSP) | Fits the audio-output requirement and is invisible, but vocabularies are small and speech quality degrades in noise |
| 4 | **Intraoral EPG / optopalatography** | SilentSpeller 97% char / 37 wpm [54]; optopalatography 98.38% on 40 words [61]; hidden IR glasses F 0.90 [60] | Completely hidden | High (custom dental retainer / dentist) | Highest silent accuracy per word, but needs a retainer and is closed-vocabulary spelling, not open speech |
| 5 | **UTI / EMA / PMA (articulator tracking)** | UTI 64.5% on 50 words silent [35]; EMA 96.7–100% on closed phrases [43]; PMA 97%/94% [44], 88.5–98.7% on 57 words [46] | Visible under-chin probe/helmet (1.3 kg [41]); coils glued in mouth; magnets on tongue/lips | High; magnets ≈ implant path (see track 06) | Rich signal but fails "barely different from normal face"; PMA's magnet option is the only articulatory route compatible with the brief, and head-motion can drop it to "about 2%" [48] |
| 6 | **Radar / Wi-Fi / RFID** | mSilent 9.5% WER, silent, 1.5 m, abstract-only [83]; Lip-Siri WER 36.87% silent [79] | Sensor is off-body → face invisible; but not a personal wearable | High (SDR/radar + external setup) | Compelling numbers, but the owner would be tied to a rig in the room; no wearable path demonstrated |
| 7 | **Camera VSR** | LipNet 95.2% on GRID [87]; open-vocab WER 26.9–50.2% [88][90] | Glasses/ear camera can be invisible; downward camera is conspicuous | Medium | Open-vocabulary WER too high, plus lighting/pose/mask/privacy; good as an *auxiliary* stream only |
| 8 | **EEG / fNIRS / MEG** | Binary imagined-vowel ~90% [93]; perceived-speech EEG top-10 19.1% [95] | Visible cap or low-SNR ear-EEG | Medium–high (research-grade amps) | Cannot decode words non-invasively; fails the accuracy requirement outright |

**Recommended build path.**
1. **Primary: per-user sEMG.** Start with an 8-channel OpenBCI Cyton [13] and a neck/jawline montage
   (dry electrodes under a collar), because the necklace study shows the neck alone carries speech
   information (92.7% on 11 voiced words with >2 electrodes) [4] and Meltzner shows 11 submental +
   facial sensors reach 8.9% WER on a 2,200-word open vocabulary [9]. Pre-train on the open Gaddy
   and EMG-UKA corpora [10][70][72], then fine-tune on the owner, since 3 minutes of per-user data
   was enough for a 2026 montage to reach "20.5% CER / 31.7% WER" [75] and MONA LISA shows 12.2%
   open-vocab silent WER is now achievable [11].
2. **Primary-hiding option: acoustic eyewear.** If face/neck electrodes prove socially unacceptable,
   EchoSpeech-style sonar eyewear is the only demonstrated near-invisible verbal interface (4.5–6.1%
   WER, 1–6 min training) [38], at the cost of a 31-command closed vocabulary.
3. **Fuse sEMG with a second stream for robustness.** The strongest measured pairing is sEMG +
   lipreading (94.1% → 40.5% WER) [75], but a camera is the most conspicuous input; an
   invisible equivalent is sEMG + acoustic eyewear, or sEMG + jaw/ear IMU, since jaw IMUs reach
   <9% WER on >90% of phrases on their own [29] and EMG+IMU is already used in earbud prototypes
   [30]. Reviews explicitly recommend this complementary fusion [1][37], and the sEMG+strain logic
   ("EMG captures intent but is motion-sensitive; motion sensors track tissue deformation") is the
   design rationale [1]. Use the differential-IMU trick (a reference IMU on the forehead/ear) to
   cancel head motion, which is the dominant failure mode for both sEMG and PMA [1][48].
4. **Do not pursue as the main sensor:** UTI (bulky helmet probe [41]), EMA (glued coils [43]),
   EEG/fNIRS (cannot decode words [95][96][97]). Keep PMA magnets as a fallback only if the owner
   later accepts a tongue magnet implant; treat it as a track-06 question, not a track-02 one.

## Sources

Fetch status is noted where it matters: "abstract only" = only the abstract/landing page was read;
everything else had full text extracted or an HTML page fetched. All URLs were accessed 1 Oct 2026.

1. Tang, C., Qi, L., Gao, S., Zhang, Z., Yi, W. et al. "Sensing technologies for silent speech interfaces." *Nature Sensors* (2025). DOI 10.1038/s44460-025-00010-2. https://www.nature.com/articles/s44460-025-00010-2 (abstract verified via Cambridge Apollo record; accepted full text also read there: https://www.repository.cam.ac.uk/items/a166e44d-3d76-44c5-94e0-08f73b2fa00d)
2. Kapur, A., Kapur, S., Maes, P. "AlterEgo: A Personalized Wearable Silent Speech Interface." IUI 2018, pp. 43–53. DOI 10.1145/3172944.3172977. https://www.media.mit.edu/publications/alterego-IUI/
3. MIT News. "Computer system transcribes words users 'speak silently'." 4 April 2018. https://news.mit.edu/2018/computer-system-transcribes-words-users-speak-silently-0404
4. Wu, P., Kaveh, R., Nautiyal, R., Zhang, C., Guo, A., Kachinthaya, A., Mishra, T., Yu, B., Black, A.W., Muller, R., Anumanchipalli, G.K. "Towards EMG-to-Speech with Necklace Form Factor." Interspeech 2024. https://www.isca-archive.org/interspeech_2024/wu24k_interspeech.html
5. Fast Company (SA). "AlterEgo launches world's first near-telepathic wearable — This is how it works." 11 September 2025. https://fastcompany.co.za/tech/2025-09-11-alterego-launches-worlds-first-near-telepathic-wearable-this-is-how-it-works/
6. Kapur, A., et al. "Non-Invasive Silent Speech Recognition in Multiple Sclerosis with Dysphonia." ML4H/NeurIPS 2019, PMLR v116. https://proceedings.mlr.press/v116/kapur20a.html
7. Wand, M., Toth, A., Jou, S.-C., Schultz, T. "Impact of Different Speaking Modes on EMG-based Speech Recognition." Interspeech 2009. https://www.cs.cmu.edu/~atoth/papers/IS090482.pdf
8. Toth, A., et al. "Synthesizing Speech from Electromyography using Voice Transformation Techniques." Interspeech 2009. https://www.isca-archive.org/interspeech_2009/toth09_interspeech.pdf
9. Meltzner, G.S., et al. "Development of sEMG sensors and algorithms for silent speech recognition." *J. Neural Engineering* 15(4):046031, 2018. DOI 10.1088/1741-2552/aac965
10. Gaddy, D., Klein, D. "Digital Voicing of Silent Speech." EMNLP 2020, pp. 5521–5530. https://aclanthology.org/2020.emnlp-main.445/
11. Benster, T., et al. "MONA LISA: A multimodal deep learning approach for silent speech recognition." 2024. arXiv:2403.05583. https://arxiv.org/abs/2403.05583
12. Gowda, D., Comstock, L., Miller, K. "emg2speech: Speech synthesis from surface EMG." 2025. arXiv:2510.23969. https://arxiv.org/abs/2510.23969
13. OpenBCI. "Cyton Biosensing Board (8-channel)" ($1,249.00; 250 Hz) https://shop.openbci.com/products/cyton-biosensing-board-8-channel and "Ganglion Board" ($624.99; 200 Hz) https://shop.openbci.com/products/ganglion-board ; specs https://docs.openbci.com/Cyton/CytonSpecs/
14. AlterEgo (company). Official site, 2025. https://www.alterego.io/
15. Janke, M., Diener, L. "EMG-to-Speech: Direct Generation of Speech From Facial Electromyographic Signals." IEEE/ACM TASLP 25(12):2375–2385, 2017. DOI 10.1109/TASLP.2017.2738568 (abstract only)
16. Scheck, K., et al. "DiffMV-ETS: Diffusion-based EMG-to-Speech." Interspeech 2025. https://www.isca-archive.org/interspeech_2025/scheck25_interspeech.pdf
17. Nakajima, Y., Kashioka, H., Shikano, K., Campbell, N. "Non-audible murmur recognition." Eurospeech 2003. https://www.isca-archive.org/eurospeech_2003/nakajima03_eurospeech.html (abstract only)
18. Heracleous, P., et al. "Non-Audible Murmur (NAM) Speech Recognition Using a Stethoscopic NAM Microphone." Interspeech 2004. https://www.isca-archive.org/interspeech_2004/heracleous04_interspeech.pdf
19. Heracleous, P., et al. "Applications of NAM Microphones in Speech Recognition." Interspeech 2005. https://www.isca-archive.org/interspeech_2005/heracleous05_interspeech.pdf
20. Nakajima, Y., et al. "Remodeling of the Sensor for Non-Audible Murmur (NAM)." Interspeech 2005. https://www.isca-archive.org/interspeech_2005/nakajima05_interspeech.pdf
21. Sun, C., et al. "EarSSR: Silent Speech Recognition via Ear Canal Deformation Sensing." IEEE TMC, 2024. DOI 10.1109/TMC.2024.3356719. PDF https://chaof94.github.io/Papers/EarSSR.pdf
22. Jin, Y., et al. "EarCommand: 'Hearing' Your Voice Commands by Listening to the Ear Canal." IMWUT 2022. DOI 10.1145/3534613 (abstract only)
23. Khanna, P., et al. "JawSense: Recognizing Unvoiced Sound using a Low-cost Ear-worn System." HotMobile 2021. DOI 10.1145/3446382.3448363 (abstract only)
24. Lepold, N., et al. "OpenEarable ExG: Open-Source Hardware for Ear-Based Biopotential Sensing." 2024. arXiv:2410.06533. https://arxiv.org/abs/2410.06533
25. Tang, Y., et al. "Ultrasensitive Textile Strain Sensors Redefine Wearable Silent Speech Interfaces." 2024. arXiv:2311.15683. https://arxiv.org/abs/2311.15683
26. Tang, Y., et al. "Wearable intelligent throat enables natural speech in stroke patients." 2024. arXiv:2411.18266. https://arxiv.org/abs/2411.18266 (preprint)
27. Kim, T., et al. "Wearable, ultra-light strain sensors for silent speech recognition." *Nature Communications* 13:5815, 2022. DOI 10.1038/s41467-022-33457-9
28. Jou, S.-C., Schultz, T., Waibel, A. "Adaptation for soft whisper recognition using a throat microphone." Interspeech 2004. https://www.isca-archive.org/interspeech_2004/jou04_interspeech.html (abstract only)
29. Srivastava, A., et al. "Unvoiced: Designing an LLM-Assisted Silent Speech Interface using Twin-IMU Earable." SenSys 2024. DOI 10.1145/3666025.3699374. PDF https://people.cs.umass.edu/~phuc/papers/Unvoiced_SenSys24.pdf
30. Srivastava, A., et al. "Whispering Wearables (QuietSync): Silent Speech with IMU + ExG." ICMI 2024. DOI 10.1145/3678957.3685720 (abstract only)
31. van Oort, T., et al. "EarMag: In-Ear Magnetosensing for Orofacial Activity." UbiComp Companion 2025. DOI 10.1145/3714394.3757254 (abstract only)
32. Chen, T., et al. "NeckFace: Continuously Tracking Face and Neck Movements with a Neck-Worn Camera." IMWUT 2021. DOI 10.1145/3463511 (abstract only; included as a correction)
33. "StethoSpeech: Recognizing Speech from Flesh-Conducted Vibrations Behind the Ear." IMWUT 2024. DOI 10.1145/3678515 (abstract only)
34. Tang, Y., et al. "Textile EMG electrodes in earmuffs for voice-free control." IEEE TIM preprint. Cambridge repository: https://www.repository.cam.ac.uk/bitstreams/0d87f867-5edb-4c1a-a0fa-99387d485d30/download
35. Florescu, V.-M., Crevier-Buchman, L., Denby, B., Hueber, T., et al. "Silent vs vocalized articulation for a portable ultrasound-based silent speech interface." Interspeech 2010, pp. 450–453. https://www.isca-archive.org/interspeech_2010/florescu10_interspeech.pdf
36. Hueber, T. "Reconstitution de la parole par imagerie ultrasonore et vidéo de l'appareil vocal." PhD thesis, Université Pierre et Marie Curie, 2009. https://pastel.hal.science/pastel-00005707/file/hueber_phd.pdf
37. Denby, B., Schultz, T., Honda, K., Hueber, T., Gilbert, J., Brumberg, J. "Silent speech interfaces." *Speech Communication* 52(4):270–287, 2010. DOI 10.1016/j.specom.2009.08.002
38. Zhang, R., Li, K., Hao, Y., Wang, Y., Lai, Z., Guimbretière, F., Zhang, C. "EchoSpeech: Continuous Silent Speech Recognition on Minimally-obtrusive Eyewear Powered by Acoustic Sensing." CHI 2023. DOI 10.1145/3544548.3580801. PDF https://czhang.org/assets/pdf/EchoSpeech.pdf
39. Eshky, A., Ribeiro, M.S., Cleland, J., Richmond, K., et al. "UltraSuite: A Repository of Ultrasound and Acoustic Data from Child Speech Therapy Sessions." Interspeech 2018. https://ultrasuite.github.io/papers/ultrasuite_IS18.pdf
40. Ribeiro, M.S., et al. "TaL: a synchronised multi-speaker corpus of ultrasound tongue imaging, audio, and lip videos." IEEE SLT 2021. https://ultrasuite.github.io/papers/tal_corpus_SLT2021.pdf
41. Articulate Instruments "SonoSpeech" brochure (2017) http://www.articulateinstruments.com/SonoSpeech%20Brochure.pdf and Interson USB probe datasheet https://interson.com/wp-content/uploads/2017/09/99-5903.pdf
42. Rebernik, T., Jacobi, J., Tiede, M., Wieling, M. "Accuracy Assessment of Two Electromagnetic Articulographs: NDI Wave and NDI Vox." *JSLHR* 64(7), 2021. https://pure.rug.nl/ws/files/199230911/2021_JSLHR_20_00394.pdf
43. Wang, J., Samal, A., Green, J.R. "Preliminary Test of a Real-Time, Interactive Silent Speech Interface Based on Electromagnetic Articulograph." SPLAT 2014, pp. 38–45. https://aclanthology.org/W14-1906.pdf
44. Fagan, M.J., et al. "Development of a (silent) speech recognition system for patients following laryngectomy." *Medical Engineering & Physics*, 2008. DOI 10.1016/j.medengphy.2007.05.003 (abstract only)
45. Gilbert, J.M., et al. "Isolated word recognition of silent speech using magnetic implants and sensors." *Medical Engineering & Physics*, 2010. DOI 10.1016/j.medengphy.2010.08.011 (abstract only)
46. Hofe, R., et al. "Evaluation of a Silent Speech Interface Based on Magnetic Sensing." Interspeech 2010. https://www.isca-archive.org/interspeech_2010/hofe10_interspeech.pdf
47. Hofe, R., et al. "Performance of the MVOCA Silent Speech Interface Across Multiple Speakers." Interspeech 2013. https://www.isca-archive.org/interspeech_2013/hofe13_interspeech.pdf
48. Cheah, L.-A., et al. "A Wearable Silent Speech Interface based on Magnetic Sensors with Motion-Artefact Removal." BIODEVICES 2018. https://www.scitepress.org/PublishedPapers/2018/65732/65732.pdf
49. Gonzalez, J.A., et al. "A silent speech system based on permanent magnet articulography and direct synthesis." *Computer Speech & Language* 39:67–87, 2016. https://eprints.whiterose.ac.uk/112036/1/csl2016.pdf
50. Dong, X., et al. "Decoding silent speech commands from articulatory movements through soft magnetic skin and machine learning." *Materials Horizons* 10(12):5607–5620, 2023. https://par.nsf.gov/biblio/10491496 (abstract only)
51. Gosztolya, G., Ibrahimov, R., Zainkó, C. "How Silent Are Silent Speech Interfaces? Speech Reconstruction From Whispered and Silent Ultrasound Tongue Images." SSW 2025. https://www.isca-archive.org/ssw_2025/gosztolya25_ssw.pdf
52. Richmond, K., Hoole, P., King, S. "Announcing the Electromagnetic Articulography (Day 1) Subset of the mngu0 Articulatory Corpus." Interspeech 2011. https://www.pure.ed.ac.uk/ws/files/15322641/Announcing_the_electromagnetic_articulography.pdf
53. Ji, A., Berry, J., Johnson, M. "The Electromagnetic Articulography Mandarin Accented English (EMA-MAE) Corpus." ICASSP 2014. https://speechlab.eece.mu.edu/johnson/papers/Ji_Icassp2014.pdf
54. Kimura, N., Gemicioglu, T., Womack, J., Li, R., Zhao, Y., Bedri, A., Su, A., Olwal, A., Rekimoto, J., Starner, T. "SilentSpeller: Towards mobile, hands-free, silent speech text entry using electropalatography." CHI 2022, Art. 288. DOI 10.1145/3491102.3502015. PDF https://tangemicioglu.com/files/papers/SilentSpeller_CHI_2022.pdf
55. Kimura, N., et al. "Mobile, Hands-free, Silent Speech Texting Using SilentSpeller." CHI EA 2021. DOI 10.1145/3411763.3451552 (abstract only)
56. Mat Zin, N.A., et al. "The technology of tongue and hard palate contact detection: a review." *BioMedical Engineering OnLine* 20:17, 2021. https://pmc.ncbi.nlm.nih.gov/articles/PMC7866712/
57. CompleteSpeech. SmartPalate official site. https://completespeech.com/
58. Augmental. MouthPad official site (prices, specs). https://www.augmental.tech/ ; MIT Media Lab article "Forget the mouse: Augmental's MouthPad..." https://www.media.mit.edu/articles/forget-the-mouse-augmental-s-mouthpad-lets-the-tongue-control-the-cursor/
59. Kimura, N., Kono, M., Rekimoto, J. "SottoVoce: An Ultrasound Imaging-Based Silent Speech Interaction Using Deep Neural Networks." CHI 2019. arXiv:2303.01758. https://arxiv.org/abs/2303.01758
60. Igarashi, K., Futami, K., Murao, K. "Silent Speech Recognition Using Eyewear-Mounted Infrared Distance Sensors." *Sensors* 24(22):7368, 2024. https://pmc.ncbi.nlm.nih.gov/articles/PMC11598394/
61. Possamai de Menezes, M., et al. "A demonstrator for articulation-based command word recognition." Interspeech 2024. https://www.isca-archive.org/interspeech_2024/possamaidemenezes24_interspeech.html
62. Birkholz, P., Neuschaefer-Rube, C. "Combined Optical and Contact Palatography." Interspeech 2011. https://www.isca-archive.org/interspeech_2011/birkholz11_interspeech.html
63. Schultz, T., Hueber, T., Wand, M., Krusienski, D.J., Herff, C., Brumberg, J.S. "Biosignal-Based Spoken Communication: A Survey." IEEE/ACM TASLP 25(12):2257–2271, 2017. https://hal.science/hal-01652757v1 (abstract only)
64. Gonzalez-Lopez, J.A., Gomez-Alanis, A., Martín-Doñas, J.M., Pérez-Córdoba, J.L., Gomez, A.M. "Silent Speech Interfaces for Speech Restoration: A Review." IEEE Access, 2020. arXiv:2009.02110. https://arxiv.org/abs/2009.02110 (abstract only)
65. Ji, Y., et al. "Updating the Silent Speech Challenge Benchmark with Deep Learning." 2017. arXiv:1709.06818. https://arxiv.org/abs/1709.06818
66. Ribeiro, M.S., Eshky, A., Richmond, K., Renals, S. "Silent vs vocalised speech recognition with ultrasound and lip video." Interspeech 2021. https://www.isca-archive.org/interspeech_2021/ribeiro21_interspeech.pdf
67. Beeson, R., Richmond, K. "Improved Ultrasound and Lip Point Tracking for Silent Speech Recognition." Interspeech 2023. https://www.isca-archive.org/interspeech_2023/beeson23_interspeech.pdf
68. Li, Z., et al. "EEG-based Silent Speech Decoding with the Assistance of sEMG." Interspeech 2023. https://www.isca-archive.org/interspeech_2023/li23l_interspeech.pdf
69. Kaifosh, P., et al. "A generic non-invasive neuromotor interface for human-computer interaction." *Nature*, 2025. DOI 10.1038/s41586-025-09255-w. https://www.nature.com/articles/s41586-025-09255-w (abstract only)
70. Wand, M., Janke, M., Schultz, T. "The EMG-UKA Corpus for Electromyographic Speech Processing." Interspeech 2014. https://www.isca-archive.org/interspeech_2014/wand14b_interspeech.pdf
71. Rosello, E., Toman, P., Agarwala, S. "Subvocal Speech Recognition." 2017. https://pamelatoman.net/materials/papers/2017-subvocal_speech_recognition_paper.pdf
72. Gaddy, D., Klein, D. "Silent Speech EMG" dataset (CC-BY-4.0, ~20 h, single speaker). Zenodo, 2020. https://zenodo.org/records/4064409 ; code https://github.com/dgaddy/silent_speech
73. UltraSuite. Data download page. https://ultrasuite.github.io/download/
74. Xu, et al. "Silent Speech Interfaces in the Era of Large Language Models: A Comprehensive Taxonomy and Systematic Review." 2026. arXiv:2603.11877. https://arxiv.org/abs/2603.11877
75. del Blanco, et al. "sEMG + lipreading fusion for silent speech." 2026. arXiv:2606.09667. https://arxiv.org/abs/2606.09667
76. Meltzner, G.S., et al. "Speech Recognition for Vocalized and Subvocal Modes of Production using Surface EMG Sensors." Interspeech 2008. https://www.isca-archive.org/interspeech_2008/meltzner08_interspeech.pdf
77. Freitas, J., Teixeira, A., Dias, M.S., Silva, S. *An Introduction to Silent Speech Interfaces.* Springer, 2017. DOI 10.1007/978-3-319-40174-4. https://link.springer.com/book/10.1007/978-3-319-40174-4 (abstract/landing page only)
78. Wang, G., Zou, Y., Zhou, Z., Wu, K., Ni, L.M. "We Can Hear You with Wi-Fi!" MobiCom 2014 / IEEE TMC 2016. DOI 10.1109/TMC.2016.2517630. PDF https://yongpanzou.github.io/documents/WiHearMobicom.pdf
79. Tian, et al. "Lip-Siri: Wi-Fi Backscatter Silent Speech Recognition." January 2026. arXiv:2601.18177. https://arxiv.org/abs/2601.18177
80. Zhang, et al. "HearMe: Accurate and Real-time Lip Reading based on Commercial RFID Devices." IEEE TMC, 2022. DOI 10.1109/TMC.2022.3208019 (abstract only)
81. Wang, et al. "RFID Tattoo: A wireless platform for speech recognition." IMWUT 3(4), 2019. DOI 10.1145/3369812 (abstract only)
82. "RF-Mic: Live Voice Eavesdropping via a Contactless RFID Tag on Glasses." IMWUT 2023. DOI 10.1145/3596259 (abstract only)
83. Zeng, Y., et al. "mSilent: Towards Silent Speech Recognition with mmWave Radar." IMWUT 2023. DOI 10.1145/3580838 (abstract only)
84. "TWLip: Through-Wall Silent Speech/Lip Reading with Radar." IEEE IoT Journal 2024, DOI 10.1109/JIOT.2024.3427329; "TWLip-Seq" IEEE Sensors Journal 2025, DOI 10.1109/JSEN.2025.3601532 (abstracts only)
85. Ferreira, et al. "RaSSpeR: Radar-based Silent Speech Recognition." Interspeech 2021. DOI 10.21437/Interspeech.2021-1413 (abstract only)
86. Lien, J., et al. "Soli: Ubiquitous Gesture Sensing with Millimeter Wave Radar." ACM TOG 35(4), 2016. DOI 10.1145/2897824.2925953; hardware detail in Xu et al. 2024, arXiv:2407.06458
87. Assael, Y., Shillingford, B., Whiteson, S., de Freitas, N. "LipNet: End-to-End Sentence-level Lipreading." 2016. arXiv:1611.01599. https://arxiv.org/abs/1611.01599
88. Chung, J.S., Senior, A., Vinyals, O., Zisserman, A. "Lip Reading Sentences in the Wild." CVPR 2017. arXiv:1611.05358. https://arxiv.org/abs/1611.05358
89. Afouras, T., Chung, J.S., Zisserman, A. "LRS2-BBC / LRS3-TED datasets." 2018. arXiv:1809.02108, arXiv:1809.00496
90. Shi, B., Hsu, W.-N., Lakhotia, K., Mohamed, A. "Learning Audio-Visual Speech Representation by Masked Multimodal Cluster Prediction (AV-HuBERT)." ICLR 2022. arXiv:2201.02184. https://arxiv.org/abs/2201.02184
91. Radford, A., et al. "Robust Speech Recognition via Large-Scale Weak Supervision (Whisper)." 2022. arXiv:2212.04356. https://arxiv.org/abs/2212.04356
92. Chung, J.S., Zisserman, A. "Lip Reading in Profile." BMVC 2017. http://robots.ox.ac.uk/~vgg/publications/2017/Chung17a/chung17a.pdf
93. Zhao, S., Rudzicz, F. "KaraOne: Imagined and inner speech EEG dataset." ICASSP 2015. DOI 10.1109/ICASSP.2015.7178118; data http://www.cs.toronto.edu/~complingweb/data/karaOne/karaOne.html
94. Nieto, N., et al. "Inner Speech: A ten-participant, 136-channel inner-speech EEG dataset." *Scientific Data* 9, 2022. DOI 10.1038/s41597-022-01147-2
95. Défossez, A., et al. "Decoding speech perception from non-invasive brain recordings." *Nature Machine Intelligence*, 2023. arXiv:2208.12266. https://arxiv.org/abs/2208.12266
96. Motaqi, M., et al. "A Comprehensive Review of Imagined Speech Decoding in Brain-computer Interfaces." *Basic and Clinical Neuroscience* 17(2), 2026. https://bcn.iums.ac.ir/files/site1/user_files_c424bc/majid-A-10-8254-1-f2fc3f5.pdf
97. Keerthana, et al. "Imagined Speech Decoding: A Systematic Review." *IEEE Access* 14, 2026. DOI 10.1109/ACCESS.2026.3708197
98. Anumanchipalli, G.K., Chartier, J., Chang, E.F. "Speech synthesis from neural decoding of spoken sentences." *Nature* 568, 2019. DOI 10.1038/s41586-019-1119-1
99. Moses, D.A., et al. "Neuroprosthesis for Decoding Speech in a Paralyzed Person with Anarthria." *NEJM* 385, 2021. DOI 10.1056/NEJMoa2027540
100. Willett, F.R., et al. "A high-performance speech neuroprosthesis." *Nature* 620, 2023. https://stanfordhealthcare.org/publications/886/886506.html
101. Tang, J., et al. "Semantic reconstruction of continuous language from non-invasive brain recordings." *Nature Neuroscience* 26, 2023. DOI 10.1038/s41593-023-01304-9
102. "MindGPT: Thought-to-LLM with fNIRS." 2024. arXiv:2408.05361. https://arxiv.org/abs/2408.05361 (abstract only)

## Key takeaways for the build

- **sEMG is the only modality that already combines large-vocabulary silent decoding with a hidden
  form factor.** Meltzner et al. reached 8.9% WER on a 2,200-word open vocabulary with 11 sensors
  [9]; MONA LISA reached 12.2% open-vocabulary silent WER [11]; AlterEgo's 92.01% is a closed
  ~20-word result [2]. A neck/jawline montage is barely visible and the necklace study proves the
  neck alone carries speech information (>2 electrodes needed; 92.7% on 11 voiced words) [4].
- **Per-user calibration is a feature, not a cost, for this owner.** 3 minutes gave 20.5% CER /
  31.7% WER on an 8-channel lower-face/neck montage [75], and Gaddy's open dataset plus ~30 min
  sessions is enough to bootstrap [10][72].
- **Active acoustic eyewear (EchoSpeech) is the best fully-invisible back-up** — 4.5%/6.1% WER on
  31 commands and connected digits, 1–6 min of training, ~73 mW, mouthed not voiced [38]. Closed
  vocabulary is the price.
- **In-ear sensing is the natural companion to the bone-conduction output** and is invisible:
  EarSSR 82% letters / 93% on 50 words [21], EarCommand ~10–12% WER on 32/25 commands [22], NAM
  mics 88.9–93.9% on small test sets [18][19]. Vocabularies are small and noise is the enemy.
- **Intraoral EPG is the accuracy winner but needs a dentist**: SilentSpeller hit 97% char / 37 wpm
  on a 1164-word dictionary [54] and optopalatography 98.38% on 40 words [61]; the device is
  completely hidden but is closed-vocabulary spelling, not open speech.
- **Articulator tracking (UTI/EMA/PMA) is ruled out by visibility**, not accuracy: UTI needs a
  1.3 kg under-chin probe/helmet [41], EMA glues coils to the tongue/lips [43], and PMA's on-body
  magnets collapse to "about 2%" under head motion without cancellation [48].
- **Radar/mmWave is the surprise contender** (mSilent 9.5% WER, silent, 1.5 m [83]; Lip-Siri WER
  36.87% silent at 50 cm [79]) but requires infrastructure around the user, not a wearable.
- **Camera lip reading is auxiliary only**: 95.2% on GRID [87] becomes 26.9–50.2% WER on open
  vocabularies [88][90] and degrades sharply with pose, light and masks [79][92].
- **EEG cannot carry this build**: non-invasive EEG decodes perceived-speech segments at 19.1%
  top-10 [95], imagined-speech reviews average ~68–72% on binary/small tasks with cross-subject
  collapse [96][97]; invasive arrays reach 9.1% WER on 50 words [100] but are out of scope.
- **Fusion should be sEMG + an invisible second stream** (acoustic eyewear, ear-canal deformation,
  or a jaw IMU with a forehead/ear reference IMU). The measured fusion gains are real (sEMG+lip
  94.1% → 40.5% WER [75]; EEG+sEMG 10.52% → 7.22% CER [68]) and both 2010 and 2025 reviews
  recommend complementary sensing [1][37].

## Open questions

1. **Can a neck-only dry-electrode montage reach open-vocabulary silent accuracy on one user?**
   The necklace result is voiced and 11 words [4]; Meltzner's 8.9% used 7 submental + 4 facial
   sensors [9]. Nobody has published neck-only silent open-vocabulary WER.
2. **How stable is a dry-electrode neck/jaw montage over a full day** (sweat, beard, collar
   movement, speech vs swallowing), and what is the re-donning calibration cost? No source found.
3. **Does sEMG + EchoSpeech-style acoustic eyewear actually fuse well**, or do both sense the same
   articulatory information (making the gain small)? Only sEMG+lipreading and sEMG+IMU have measured
   gains [75][30].
4. **Is a hidden ear-canal/ear-EMG channel good enough to be the second stream**, given EarSSR and
   EarCommand report 50-command-scale vocabularies only [21][22]?
5. **What is the real long-term safety of tongue magnets** if the owner ever wanted the PMA path?
   Sources only speculate about permanent implantation [48]; no dedicated study was found.
6. **Cost and availability of a wearable ultrasound front end** — no verified price for any UTI
   probe; if a cheap 60+ fps submental probe emerges, UTI's silent-speech ceiling changes.
7. **Radar at wearable scale** — no mmWave silent-speech system has been shown on body/battery;
   mSilent is abstract-only and lab-mounted [83].
