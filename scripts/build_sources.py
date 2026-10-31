#!/usr/bin/env python3
"""Build research/jaw/sources-patents.jsonl from the facts we read.

Patents follow the ss-research-baltic convention: the publication number goes in
the title, `patent_no` is null, and `url` is the page actually opened (Lens.org
public patent page, which serves the whole record as JSON). Papers carry the
PubMed id when one exists and a URL that returns HTTP < 400.

Run: python3 scripts/build_sources.py
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "research" / "jaw" / "raw"
OUT = REPO / "research" / "jaw" / "sources-patents.jsonl"


def lens(no: str) -> str:
    import re
    m = re.match(r"^([A-Z]{2})(\d+)([A-Z]\d?)$", no)
    cc, num, kind = m.groups()
    return f"https://www.lens.org/lens/patent/{cc}_{num}_{kind}"


# (publication number, title, people, year, what_they_did, useful_for_us)
PATENTS: list[tuple[str, str, list[str], str, str, str]] = [
    ("US10621973B1", "Sub-vocal speech recognition apparatus and method", ["McVicker Ryan", "Eigenbrode Brett"], "2017",
     "A headset worn over the ear carries EMG electrodes and an IMU in contact with the skin over the neck, under the chin and behind the ear; sub-vocal speech is recorded, amplified, filtered and windowed into multi-millisecond frames for recognition.",
     "The closest claimed combination of chin plus neck EMG with a jaw IMU; active to 2038, so our hidden-jaw device needs a different site set or a design-around rather than the same chin/neck/behind-ear triad."),
    ("US8082149B2", "Methods and apparatuses for myoelectric-based speech processing", ["Schultz Tanja", "Waibel Alexander"], "2006",
     "Captures a myoelectric signal from a user with at least one electrode, amplifies, filters and digitises it, then processes the signal for speech; assigned to Biosensic LLC with Tanja Schultz as inventor.",
     "The foundational EMG-speech patent by the field's best-known group; its 45-member family includes continuations US11222185B2 and US11972227B2, so the basic electrode-plus-processing claim stays alive across many years."),
    ("US12505842B2", "Devices, systems, and methods for personal speech recognition and replacement", ["Rameau Anais", "Dunham Simon", "Wang Fei"], "2019",
     "A personal device with a cutaneous sensor unit detects surface EMG from articulatory muscles and wirelessly sends it to a computing device that recognises silent speech, aimed at laryngectomy and voice-rest patients.",
     "Clinical sEMG silent-speech claim naming articulatory muscles and a wearable cutaneous unit; useful evidence that chin/neck sEMG can be framed as voice restoration and that a small sensor unit is patentable."),
    ("US12400473B2", "Wearable facial movement tracking devices", ["Zhang Cheng", "Chen Tuochao", "Steeper Benjamin", "Guimbretiere Francois", "Li Ke", "Zhang Ruidong", "Lim Hyunchul"], "2020",
     "Head-mounted or neck-mounted wearables with cameras or acoustic sensors learn skin-deformation and facial-feature patterns to reconstruct facial expressions and movements.",
     "The optical/acoustic competitor route to EMG: it proves facial tracking from a head-worn device but needs camera line of sight and raises the occlusion and privacy problems our hidden EMG device avoids."),
    ("US11216069B2", "Systems and methods for improved speech recognition using neuromuscular information", ["Berenzweig Adam", "Kaifosh Patrick", "Du Alan Huan", "Seely Jeffrey Scott"], "2018",
     "Multiple neuromuscular sensors on one or more wearables continuously record neuromuscular signals, and a trained inference model takes audio plus the neuromuscular signals (or signals derived from them) and determines text.",
     "The core Meta/CTRL-labs claim combining neuromuscular sensing with audio for speech recognition; broad and active to 2038, so it belongs at the top of any freedom-to-operate watch list for a neuromuscular wearable."),
    ("US11036302B1", "Wearable devices and methods for improved speech recognition", ["Berenzweig Adam", "Kaifosh Patrick", "Du Alan Huan", "Seely Jeffrey Scott"], "2018",
     "Wearable-device variants of the Meta neuromuscular speech system: sensors record neuromuscular signals, models determine text, with embodiments covering the wearable housing and sensor arrangement.",
     "Shows Meta claimed the wearable hardware separately from the signal-processing method; a reminder that both the sensor housing and the decoding pipeline can be separately claimed."),
    ("US12579768B2", "Wearable electronic devices, extended reality systems including neuromuscular sensors, and methods for generating text from speech input", ["Wetmore Daniel"], "2018",
     "Neuromuscular sensors on a wearable sense signals, and processors generate text and XR interactions from the sensed neuromuscular data.",
     "A late Meta grant in the same family that extends the claims into extended-reality use; shows how a single neuromotor portfolio is kept alive with continuation grants."),
    ("US12154572B2", "Identifying silent speech using recorded speech", ["Wexler Yonatan"], "2022",
     "Signals representing pre-vocalisation facial skin micromovements are received in a first time period and signals representing sounds in a succeeding period, and the micromovements are interpreted using the recorded speech.",
     "The Q (Cue) optical-micromovement approach that self-supervises on recorded speech to decode silent speech; a 101-member family and the technology behind Apple's acquisition, so it is a major adjacent claim space."),
    ("US12482449B2", "Systems and methods for using silent speech in a user interaction system", ["Garg Sahaj", "Kothari Tanay", "Leonardo Anthony"], "2023",
     "A speech input device wearable on the user receives an electronic signal indicative of the user's speech-muscle activation patterns, including EMG data, and uses it in a user-interaction system with a knowledge system.",
     "Wispr AI's granted claim explicitly covers a wearable that reads speech-muscle activation EMG; the 15-member family is active, so check it before claiming an EMG silent-speech wearable."),
    ("US10678502B2", "Systems and methods for in-ear control of remote devices", ["Sheynblat Leonid"], "2016",
     "An in-ear device microphone receives audio, a speech-recognition technique determines a command, and a voice-recognition technique identifies the wearer before controlling remote devices.",
     "In-ear form-factor precedent for command input; it is acoustic rather than silent, so it does not block ear-canal deformation or EMG sensing but shows the earbud interaction claim pattern."),
    ("US11683632B2", "Automatic speech recognition triggering system", ["Dusan Sorin V", "Lindahl Aram M", "Watson Robert D"], "2017",
     "An ASR triggering system uses a microphone plus an accelerometer worn in the ear canal to generate a non-acoustic bone-conduction signal that triggers speech recognition.",
     "Apple's ear-canal accelerometer claim, with a three-grant family (US10313782B2, US11102568B2, US11683632B2); relevant to any in-ear or behind-ear vibration sensor on our device."),
    ("US9779758B2", "Augmenting speech segmentation and recognition using head-mounted vibration and/or motion sensors", ["Johnson Michael Patrick", "Dong Jianchun", "Balez Mat"], "2012",
     "Audio in the speech band from a microphone is combined with vibration data from a non-microphone sensor on a head-mountable device to decide whether and when the speaker is speaking.",
     "Head-mounted vibration and motion sensing for speech segmentation; a Google claim that covers using a second, non-acoustic sensor to gate speech, which is how a jaw-mounted sensor is likely to be used."),
    ("US10679644B2", "Production of speech based on whispered speech and silent speech", ["Rakshit Sarbajit K", "Keen Martin G", "Bostick James E", "Ganci Jr John M"], "2017",
     "Multiple sensors capture low-amplitude whispered or silent speech, computing devices analyse the sensor data, map it to speech, and transmit amplified speech to a remote communication device.",
     "IBM claims a multi-sensor silent/whispered speech pipeline end to end; its continuation US10529355B2 shows the sensor-fusion claim was filed twice, so the concept is well covered."),
    ("US11397799B2", "User authentication by subvocalization of melody singing", ["Lawrenson Matthew John", "Andersson Lars", "Burkert Till", "Strom Jacob", "van den Berg Jan Jasper"], "2016",
     "A computing device acquires a representation of a melody subvocalised by the user and authenticates the user when it matches a reference melody closely enough.",
     "An authentication use of subvocalisation rather than speech decoding; useful as a secondary claim target if our jaw device also supports an unlock gesture, and it shows subvocal signals are treated as biometrics."),
    ("US11154232B2", "Mechano-acoustic sensing devices and methods", ["Jeong Jae-Woong", "Rogers John", "Liu Yu Hao"], "2017",
     "A soft, conformal device records mechano-acoustic signals from skin almost anywhere on the body and can add electrophysiological recording for multimodal operation.",
     "The soft-conformal materials route (Rogers group) for picking up throat and jaw vibration; useful if the hidden device records mechano-acoustic rather than purely electrical signals."),
    ("US8242880B2", "Tongue operated magnetic sensor systems and methods", ["Ghovanloo Maysam", "Huo Xueliang"], "2008",
     "A magnetic tracer unit is placed on the tongue and a sensor system near the mouth tracks the tracer's position, enabling assistive control.",
     "Intraoral magnetic tracking is a fully different sensing modality from EMG and is now INACTIVE, so the concept is relatively free to use, but it needs a tracer on the tongue, which is not hidden."),
    ("US9911358B2", "Wireless real-time tongue tracking for speech impairment diagnosis, speech therapy with audiovisual biofeedback, and silent speech interface", ["Ghovanloo Maysam", "Block Jacob"], "2013",
     "A small magnetic tracer on the tongue plus an array of magnetic sensors around the mouth localises the tongue with sub-millimetre precision and fuses that with acoustic, video and airflow data in a silent-speech interface.",
     "Georgia Tech explicitly claimed a silent-speech-interface use of tongue tracking; now INACTIVE, which makes it useful prior art and a design dead-end requiring a tongue tracer rather than hidden jaw sensing."),
    ("US7082395B2", "Signal injection coupling into the human vocal tract for robust audible and inaudible voice recognition", ["Tosaya Carol A", "Sliwa Jr John W"], "1999",
     "Artificial excitation is injected into the human vocal tract to enhance or replace natural excitation, adding spectral, temporal or phase data so that audible or inaudible mouthed/whispered speech is recognised more robustly.",
     "An early subvocal approach that is now EXPIRED; it is direct evidence that external excitation of the vocal tract was tried and did not become a product, which is a dead-end warning for hardware-heavy silent-speech schemes."),
    ("CN113288183B", "Silent speech recognition based on facial-neck surface electromyography", ["Zhang Xu", "Deng Zhihang", "Chen Xi", "Chen Xiang", "Chen Xun"], "2021",
     "Surface EMG from a high-density electrode array and from sparse discrete electrodes is preprocessed and turned into high-density and channel-sparse sEMG image sets; a source-domain network is trained and transfer learning calibrates it on the target domain so discrete-electrode silent words can be classified.",
     "This is essentially our problem statement from USTC: high-density arrays are used to train, few discrete electrodes are used to wear, and transfer learning handles electrode shift and cross-user variation; active to 2041."),
    ("CN114863912A", "Silent voice decoding method based on surface electromyogram signals", ["Zhang Xu", "Song Rui", "Chen Xi", "Chen Xiang", "Chen Xun"], "2022",
     "Silent-speech sEMG data is collected and featurised into a training set, a Transformer-based decoding network is built and trained, and the optimised network decodes silent speech.",
     "The same USTC group moved from a CNN-style classifier to a Transformer decoder, which is the architecture direction we should copy for small sEMG vocabularies."),
    ("CN114822541A", "Silent speech recognition method and system based on back translation", ["Yin Erwei", "Zhang Jing", "Cao Yidan", "Zhang Yakun", "Ai Yongbao", "Wang Kai", "Zhang Haoyang", "Yan Ye"], "2022",
     "Silent-state surface EMG is collected, preprocessed and featurised, fed to an SAEM model, and back-translation is used to expand or regularise the silent-speech recognition.",
     "A concrete data-augmentation recipe (back-translation) from the Chinese defence lab for the small-corpus problem that will also limit our one-user jaw dataset."),
    ("CN112151030B", "Multimodal speech recognition method and apparatus for complex scenes", ["Yin Erwei", "Wu Jinghan", "Yan Huijiong", "Xie Liang", "Deng Baosong", "Fan Xiaoli", "Luo Zhiguo", "Yan Ye"], "2020",
     "When a change in the captured lip image is detected, audio, lip-image and facial-EMG signals are captured synchronously, multi-source features are encoded by a speech model, and a language model synthesises text.",
     "Confirms the Chinese defence lab claims lip image plus facial EMG plus audio fusion for noisy, private or vocal-cord-damaged scenarios; active, and a broad multimodal claim to check."),
    ("CN111190484B", "Multimodal interaction system and method", ["Yan Ye", "Wang Yijing", "Pei Yu", "Ming Dong", "Xu Minpeng", "Yin Erwei"], "2019",
     "An acquisition module collects EEG, EMG, lip images, eye images and physiological parameters; machine learning recognises commands, language and emotion, and an interaction module dispatches them.",
     "A very broad multimodal claim that sweeps in EEG plus EMG plus lip and eye images; even though we do not plan EEG, the breadth shows how much of the multimodal space this lab has claimed."),
    ("CN111899713A", "Silent communication method, device and equipment and storage medium", ["Yan Ye", "Zhao Tao", "Yin Erwei", "Deng Baosong", "Huo Xiaokai", "Xu Mengfei", "Fan Xiaoli", "Xie Liang"], "2020",
     "Facial EMG, lip optical images and oral-cavity ultrasound images are acquired synchronously, preprocessed and feature-extracted for silent communication.",
     "A sensor-fusion dead-end to note: it needs an intraoral ultrasound probe, which cannot be hidden like a jaw patch, but it shows the lab explored ultrasound as an alternative to EMG."),
    ("CN113887339A", "Silent speech recognition system and method fusing surface electromyogram signal and lip image", ["Tao Wenyuan", "Fu Linhui", "Xu Minpeng", "Meng Jiayuan"], "2021",
     "A surface-EMG acquisition and recognition pipeline is fused with a lip-image acquisition and preprocessing pipeline to recognise silent speech.",
     "Tianjin University's EMG-plus-lip fusion; the application is marked DISCONTINUED, which is useful evidence that fusing a camera with sEMG did not pay off and that pure sEMG is the leaner route."),
    ("CN111723717A", "Silent speech recognition method and system", ["Zhao Tao", "Tao Wenyuan", "Yan Ye", "Yin Erwei", "Ma Quanzhi", "Liu Xuanheng", "Xie Liang"], "2020",
     "Facial EMG data and vocal-cord vibration data are acquired during speaking, preprocessed, feature-fused, and trained and recognised with deep learning to output a command result.",
     "Adds vocal-cord vibration to facial EMG; DISCONTINUED, so the two-sensor combination was tried and dropped, another signal that more sensors do not automatically help."),
    ("CN109745045A", "Myoelectric electrode patch and silent voice recognition equipment", ["Zhang Hongmiao", "Liu Huicong", "Dong Wei", "Sun Lining"], "2019",
     "The patch stacks a flexible substrate, a first insulating layer, a flexible electrode layer with multiple electrode probes and interconnect wires, and a second insulating layer, and the probes collect myoelectric signals for silent-voice recognition equipment.",
     "A concrete flexible dry-electrode patch design from Soochow University; the application is DISCONTINUED, so the layered patch geometry itself is relatively free to reuse."),
    ("CN110996782B", "In-ear potential sensor", ["Iyer T M", "Lin L", "Kierszenblat R", "Joffe M", "McElhone D", "Pecher C R", "Reed J E", "Farrell A"], "2017",
     "An audio product has at least two electrodes, a processor and an electroacoustic transducer; a signal obtained through an electrode and affected by the user's action leads the processor to take an action controlling another device.",
     "Bose's in-ear biopotential electrode claim, active with a seven-member family (EP3668392, US10575777B2, WO2019036114A1); a direct watch-out for an earbud that senses electrical signals from the ear canal."),
    ("CN112424859B", "Systems and methods for improved speech recognition using neuromuscular information", ["Berenzweig Adam", "Kaifosh Patrick", "Du Alan Huan", "Seely Jeffrey Scott", "Wetmore Daniel"], "2018",
     "The Chinese counterpart of the Meta claim: multiple neuromuscular sensors on wearable devices record neuromuscular signals, and a trained inference model determines text from audio and the neuromuscular signals.",
     "Meta filed the same neuromuscular-plus-audio claim in China and it is active, so any China-based jaw EMG product faces the same claim there as in the US."),
    ("CN115705841A", "Speech recognition using accelerometer sensing for bone conduction", ["Alessi Enrico Rosario", "Passaniti Fabio", "Guarneri Nunziata Ivana"], "2021",
     "An accelerometer senses vibrations of one or more bones and no audio input is used, yet voice-command and natural-language recognition are performed from the bone-conduction signal alone.",
     "STMicroelectronics claims accelerometer-only speech recognition with no microphone; its family (EP4131256A1, US12603087B2, US20230045064A1) is a direct watch-out for a jaw- or ear-mounted accelerometer picking up bone conduction."),
    ("JP7149492B2", "EMG-assisted communication device with context-sensitive user interface", ["Shorley James E", "Ford Peter S", "Wong Robert W"], "2017",
     "An EMG-assisted communication device presents a context-sensitive user interface, using muscle signals to drive communication for users who cannot speak.",
     "Control Bionics' assistive EMG communication device, active with continuations US11284844B2 and US12455623B2; relevant prior art for the user-interface side of an EMG speech device rather than the sensor itself."),
    ("KR20250142168A", "System and method for silent speech communication using the attachable optical sensor", ["Lim Seong Jae", "Park Chang Joon"], "2024",
     "An attachable optical sensor has an optical-fibre layer in a lattice structure, a support member and an optical receiver, and the system uses it for silent speech communication.",
     "ETRI's optical-fibre deformation route to silent speech, pending with a JP grant (JP7714768B1) and a US application; a non-EMG Korean competitor worth monitoring and a possible alternative sensing modality."),
    ("KR102270653B1", "Speech production and facial expression mapping system using articulatory physical properties", ["Lee Woo Gi", "Sim Bong Seop", "Kwon Heon Do", "Kim Deok Hwan", "Shin Jin Ho"], "2017",
     "A sensor unit adjacent to one side of the speaker's head or neck measures the physical properties of the articulatory organs, including an oral-tongue sensor, and the system maps them to speech and facial expression data.",
     "Inha University claims articulatory (including tongue) sensing rather than EMG, inside a 34-member Korean family; shows Korean universities were building the same speech-production sensing space with different modalities."),
    ("DE102020110901B4", "Method for generating an artificial voice", ["Altavo GmbH"], "2020",
     "Acoustic signals of healthy speakers reading a known text are recorded together with at least one vocal-tract signal of a patient articulating the same text, and an artificial voice is generated from the pairing.",
     "Altavo's vocal-tract sensing plus voice-synthesis claim, active with EP4139917 and US20230154450A1; the closest thing to a radar/ultrasound jaw-neck competitor and a strong watch-out in Europe."),
    ("JP6960189B2", "Vocalization device", ["Chen Xiaoming", "Wu Zhe"], "2017",
     "A vocalisation device assigned to Suzhou Yichuan Electronic Technology, with an 11-member family spanning CN107820178B, EP3637797B1 and US11223897B2.",
     "A Chinese hardware company hold on a vocalisation device; less about decoding silent speech than about producing sound, but it shows the adjacent speaker/vocaliser patent thicket around the mouth and throat."),
]

# (title, url, pmid|None, people, year, what_they_did, useful_for_us)
PAPERS: list[tuple[str, str, str | None, list[str], str, str, str]] = [
    ("Development of sEMG sensors and algorithms for silent speech recognition",
     "https://pmc.ncbi.nlm.nih.gov/articles/PMC6168082/", "29855428",
     ["Meltzner Geoffrey S", "Heaton James T", "Deng Yunbin"], "2018",
     "Builds surface-EMG sensors and recognition algorithms specifically for silent speech, reporting on electrode placement and classification of silently mouthed words.",
     "The clearest sensor-and-algorithm paper for our exact task, and the source of the electrode-placement practice we should copy before buying an amplifier."),
    ("Evaluation of a wireless wearable tongue-computer interface by individuals with high-level spinal cord injuries",
     "https://pmc.ncbi.nlm.nih.gov/articles/PMC2952279/", "20332552",
     ["Huo Xueliang", "Ghovanloo Maysam"], "2010",
     "Evaluates a wireless wearable tongue-computer interface with magnetic tracer tracking in users with high-level spinal cord injuries, reporting usability and performance.",
     "Demonstrates that an intraoral magnetic interface is wearable and clinically usable, so it is a serious alternative if our jaw EMG proves too noisy, but it needs a tongue tracer."),
    ("An arch-shaped intraoral tongue drive system with built-in tongue-computer interfacing electronics",
     "https://pmc.ncbi.nlm.nih.gov/articles/PMC4279550/", "25405513",
     ["Park Hangue", "Ghovanloo Maysam"], "2014",
     "Presents an arch-shaped intraoral device with built-in interfacing electronics for a tongue drive system, integrating the sensor array into a dental retainer form factor.",
     "A complete intraoral integration example; useful mainly as a contrast to the behind-ear/jaw form factor we want, since a retainer is not hidden from the wearer's own mouth feel."),
    ("Computerised system translates 'subvocal speech' into action",
     "https://pubmed.ncbi.nlm.nih.gov/15132141/", "15132141",
     ["Larkin Marilynn"], "2004",
     "A short news report on NASA Ames' subvocal speech system, which used throat surface EMG to classify silently spoken words into control commands.",
     "The historical origin of subvocal EMG control; its date shows the idea is over twenty years old, which is useful for prior-art arguments even though it never became a product."),
    ("Can we decode phonetic features in inner speech using surface electromyography?",
     "https://pmc.ncbi.nlm.nih.gov/articles/PMC7252628/", "32459800",
     ["Nalborczyk Ladislas", "Grandchamp Romain", "Koster Ernst H W"], "2020",
     "Tests whether phonetic features of inner speech can be decoded from surface EMG of the orofacial muscles, finding that some but not all articulatory features are recoverable.",
     "A careful negative-ish result that tells us exactly which phonetic dimensions survive in inner speech EMG and which do not, so we do not promise phoneme accuracy we cannot get."),
    ("Towards optimizing electrode configurations for silent speech recognition",
     "https://pubmed.ncbi.nlm.nih.gov/33181497/", "33181497",
     ["Zhu Mingxing", "Zhang Haoshi", "Wang Xiaochen"], "2020",
     "Searches over surface-EMG electrode configurations for silent speech recognition and reports which channel placements and densities carry the most decoding information.",
     "Gives a starting electrode layout from the Chinese high-density sEMG group, saving us a full hardware search before we build the jaw patch."),
    ("Biosignal sensors and deep learning-based speech recognition: a review",
     "https://pmc.ncbi.nlm.nih.gov/articles/PMC7922488/", "33671282",
     ["Lee Wookey", "Seong Jessica Jiwon", "Ozlu Busra"], "2021",
     "Reviews biosignal sensors and deep-learning speech recognition, covering EMG, EEG and related modalities with their electrode types and reported accuracies.",
     "A single citation to compare sensor modalities and electrode types before committing to EMG, and a source of accuracy numbers to benchmark our own prototype against."),
    ("Prosodic preferences of surface electromyography-based subvocal speech for communication",
     "https://pmc.ncbi.nlm.nih.gov/articles/PMC12137685/", "39643558",
     ["Raiff Laura", "Turashvili Dea M", "Heaton James T"], "2024",
     "Studies which prosodic patterns users can reliably produce and which the sEMG system can recover in subvocal speech for communication.",
     "Shows prosody is recoverable from subvocal sEMG, which matters if we want natural-sounding output rather than just command words."),
    ("Noninvasive speech restoration after total laryngectomy using surface electromyography",
     "https://pmc.ncbi.nlm.nih.gov/articles/PMC13537912/", "42694022",
     ["Kaushal Naresh K", "Comstock Daniel C", "Belafsky Peter Charles"], "2026",
     "Applies surface EMG of the residual articulatory muscles to restore speech for total-laryngectomy patients, reporting a clinical restoration pipeline.",
     "Confirms the clinical pull for silent sEMG speech and gives the assessment protocol we could borrow when validating our own device on one user."),
    ("CochlearMotion: head gesture recognition leveraging ear canal deformation",
     "https://scholarspace.manoa.hawaii.edu/bitstreams/cb7fa89c-fa37-4e5b-9e8c-51c6a6bee12f/download", None,
     ["Lee Youngone", "Tan Sheng", "Wang Zi"], "2025",
     "Uses ear-canal deformation measured inside an earbud to recognise head gestures, showing the deformation signal is informative enough for machine learning.",
     "Direct evidence that in-ear deformation sensing works, so an earbud lead for our jaw device can double as a motion channel without adding a visible sensor."),
    ("Can LLMs understand unvoiced speech? Exploring EMG-to-text conversion with LLMs",
     "https://aclanthology.org/2025.acl-short.56.pdf", None,
     ["Mohapatra Payal", "Pandey Akash", "Zhang Xiaoyuan", "Zhu Qi Xin"], "2025",
     "Explores using large language models for EMG-to-text conversion of unvoiced speech, testing whether a language model can clean up noisy EMG decoding.",
     "Shows the current frontier is EMG-to-text with an LLM decoder, which is the cheapest way for us to get usable text out of a small personal sEMG corpus."),
    ("Digital voicing of silent speech",
     "https://www.aclweb.org/anthology/2020.emnlp-main.445.pdf", None,
     ["Gaddy David", "Klein Dan"], "2020",
     "Voices silent speech by decoding surface EMG of the face during silently mouthed speech, with an accompanying public code release.",
     "A verified silent-EMG-to-speech result with released code, so it is both a baseline method and a reusable implementation to test on our own recordings."),
    ("emg2speech: synthesizing speech from electromyography using self-supervised learning",
     "https://aclanthology.org/2026.acl-long.750.pdf", None,
     ["Gowda Harshavardhana T", "Comstock Daniel C", "Miller Lee M"], "2026",
     "Synthesises speech from orofacial EMG using self-supervised learning, reducing the labelled-data requirement for EMG-to-speech.",
     "Self-supervision is exactly what a one-user project needs because labelled silent-speech data is expensive to record; this is the method to try first."),
]

CODE: list[tuple[str, str, list[str], str, str, str]] = [
    ("dgaddy/silent_speech: code for voicing silent speech from EMG",
     "https://github.com/dgaddy/silent_speech", ["Gaddy David", "Klein Dan"], "2020",
     "Official repository for the Digital Voicing of Silent Speech paper, containing the EMG-to-speech models and training code.",
     "Ready-to-run EMG-to-speech code we can adapt to our own jaw recordings instead of writing a decoder from scratch."),
    ("HarshavardhanaTG/emg2speech: converting orofacial surface EMG to speech",
     "https://github.com/HarshavardhanaTG/emg2speech", ["Gowda Harshavardhana T"], "2026",
     "Public code release for the emg2speech self-supervised orofacial-EMG-to-speech work.",
     "A second reusable decoder, specifically self-supervised, which fits the small labelled dataset we will have as one user."),
    ("MAILAB-Yonsei/Silent-Speech-Interfaces",
     "https://github.com/MAILAB-Yonsei/Silent-Speech-Interfaces", ["MAILAB Yonsei"], "2023",
     "Yonsei University lab repository collecting silent-speech-interface code and experiments.",
     "A Korean lab's working code and configs, useful to compare preprocessing choices against the Chinese and US pipelines."),
]

DATASETS: list[tuple[str, str, str | None, list[str], str, str, str]] = [
    ("Surface EMG Dataset for Silent Speech Recognition",
     "https://doi.org/10.6084/m9.figshare.33335820", None,
     ["Jeon Hyeseong", "Sohn Jangjay", "Jung Sungmin"], "2026",
     "A public surface-EMG dataset recorded for silent speech recognition and released on figshare.",
     "A ready public sEMG corpus for silent speech, so we can pretrain or sanity-check our decoder before collecting our own jaw data."),
]


def main() -> int:
    rows: list[dict] = []
    for no, title, people, year, what, useful in PATENTS:
        rows.append({
            "kind": "patent",
            "title": f"{no} — {title}",
            "url": lens(no),
            "patent_no": None,
            "people": people,
            "year": year,
            "what_they_did": what,
            "useful_for_us": useful,
        })
    for title, url, pmid, people, year, what, useful in PAPERS:
        rows.append({
            "kind": "paper", "title": title, "url": url, "pmid": pmid,
            "people": people, "year": year, "what_they_did": what, "useful_for_us": useful,
        })
    for title, url, people, year, what, useful in CODE:
        rows.append({
            "kind": "code", "title": title, "url": url,
            "people": people, "year": year, "what_they_did": what, "useful_for_us": useful,
        })
    for title, url, pmid, people, year, what, useful in DATASETS:
        rows.append({
            "kind": "dataset", "title": title, "url": url, "pmid": pmid,
            "people": people, "year": year, "what_they_did": what, "useful_for_us": useful,
        })
    OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    print(f"wrote {len(rows)} sources -> {OUT}")
    from collections import Counter
    print(Counter(r["kind"] for r in rows))
    bad = [r["title"] for r in rows if len(r["what_they_did"]) < 40 or len(r["useful_for_us"]) < 40]
    print("too-short:", bad)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
