#!/usr/bin/env python3
"""Build research/jaw/sources-patents-gaps.jsonl from the records actually opened.

Every sentence below was written from the claim text in research/jaw/raw/lens/<id>.json
or, for the two Google Patents records, from the fetched page. The INDEX table holds the
metadata exactly as the opened record printed it (title, URL, inventors, priority year),
so this script regenerates the citation index offline; the gitignored raw cache is only
the provenance. The output file is gitignored because the repo's raw-data gate treats
every committed .jsonl as a downloaded dump.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPACT = ROOT / "research" / "jaw" / "raw" / "lens" / "_compact.jsonl"
OUT = ROOT / "research" / "jaw" / "sources-patents-gaps.jsonl"

# (lens_id or "GOOGLE:<no>", what_they_did, useful_for_us)
ROWS = [
    ("US_10878818_B2",
     "Claim 1 is a method of taking electrical measurements at positions on the skin of the head or neck, where the signals come from neural activation of speech-articulator muscles, and analysing them to recognise internally articulated speech, at least part of which happens while the user is not exhaling.",
     "This is the AlterEgo foundation patent and the closest single claim to a silent jaw/neck wearable; it is active to 2038 and is now held by AlterEgo AI together with MIT, so the claim text sets the baseline every other record is measured against."),
    ("045-073-728-605-863",
     "The WO publication of the MIT silent-speech family claims a method of measuring electrical signals at head or neck skin positions and recognising internally articulated speech, with dependent claims on low-voltage windows, 8-20 microvolt RMS against an ear reference, and audio feedback by earphone or bone conduction.",
     "It is the international member of US10878818 and therefore the file that would have entered national/regional phases, so it is the right document to check before assuming the MIT family is US-only."),
    ("124-274-805-307-259",
     "Claim 1 claims a wearable device with a plurality of electrodes, a subset of which measure electrical signals at a face, head, or neck of a user that indicate speech activation patterns while the user silently speaks or whispers, plus a processing module and a communication module coupled to an external device.",
     "This Wispr application is the most direct competitor wording to a face/head/neck electrode patch that sends data to another device; Lens records it as discontinued but the same specification produced granted US12482449B2."),
    ("168-823-659-596-990",
     "Claim 1 claims a communication system in which a speech system measures speech-muscle activation patterns of a first user, determines speech data from a silent utterance, and transmits it to a second user's communication device with low-latency feedback.",
     "It shows Wispr claiming the end-to-end silent call path rather than only the sensor, which matters if our neck unit is described as sending recognised speech to a phone call or app."),
    ("045-871-880-751-474",
     "Claim 1 claims a training method that receives a model output, receives an input signal from a speech input device worn by the user captured while the user makes a facial expression, gesture, or speech in response to the output, derives a feedback signal, and retrains the model with it.",
     "This is a per-session retraining claim driven by user feedback, close to fast calibration loops, and it shows Wispr also protects the feedback-training mechanism rather than only the hardware."),
    ("US_12505842_B2",
     "Claim 1 claims a system that detects surface EMG from a face and/or neck using a personal device with a cutaneous sensor unit whose electrodes detect sEMG from a corresponding set of articulatory muscles during silent utterances, a control module connected by a set of electrical pathways, a signal acquisition circuit, and a wireless communication circuit that transmits the data to a computing device.",
     "This granted Cornell claim combines the electrode set, the wiring to the electronics, and the wireless link in one independent claim, which is the closest granted match to our areas 1, 2 and 6."),
    ("US_12400473_B2",
     "Claim 1 claims a wearable system with at least one imaging sensor capturing a facial feature of the wearer, a processor that compares the image data to a model, assigns a contour with a predetermined degree of correspondence, and communicates the result.",
     "Cornell's camera/acoustic route is the non-EMG alternative for the same silent-speech problem, and its EP member is granted, so it is the family to watch if our design ever uses a camera for placement or calibration."),
    ("US_10621973_B1",
     "Claim 1 claims a sub-vocal speech recognition apparatus with a chin electrode, a neck electrode, a chin inertial measurement unit, a chin housing holding the electrode and IMU, a first bend-and-stay wire from the headset to the chin housing, a second bend-and-stay wire to the neck electrode, and a processor receiving the signals.",
     "This is the only granted claim found that recites the mechanical routing of chin and neck electrodes back to a headset, so it is the closest prior art for concealment geometry and electrode-to-electronics connection."),
    ("US_8082149_B2",
     "Claim 1 claims capturing a myoelectric signal with at least one electrode that converts ionic current from muscle contraction into electric current, amplifying, filtering and digitising it, transmitting it to a digital device, transforming it into a written representation with automatic speech recognition, and synthesising audible output.",
     "The Biosensic/Schultz patent is the broad foundational myoelectric-speech claim and its family was kept alive for over a decade, so any claim that starts from one electrode plus signal processing has to be read against it."),
    ("066-659-600-047-268",
     "Claim 1 claims a computer-implemented method that records an EMG signal from facial muscles, extracts features, and classifies the signal into speech units for a user interface.",
     "This second Schultz-family application is recorded as discontinued, which is useful because it shows a narrower facial-EMG classification claim that did not survive, while the broader parent did."),
    ("US_11216069_B2",
     "Claim 1 claims a system that captures speech data, uses neuromuscular sensors worn on the wrist to detect signals corresponding to arm, wrist or hand movement, and applies a trained statistical model to output information about muscle activation for improving speech recognition.",
     "Meta's claim is wrist-based rather than face/neck, so it is not a direct match, but its very large family and its EP grants make it the main obstacle to any generic neuromuscular-plus-speech-model wording."),
    ("EP_3843617_B1",
     "Claim 1 claims a system with a camera that captures images and neuromuscular sensors on wearable devices, where the processor calibrates inference models used to generate a musculoskeletal representation from the camera information.",
     "This granted Meta EP claim covers camera-assisted calibration of a neuromuscular model, which is the closest granted claim to calibration using an external reference rather than per-user labelled data."),
    ("US_12482449_B2",
     "Claim 1 claims a user interaction system with a wearable speech input device measuring a signal indicative of speech-muscle activation patterns and a processor that uses a speech model and the signal to generate an output and a knowledge system to take an action or generate a response.",
     "Wispr's granted claim is broad at the level of sensor plus speech model plus action, and dependent claim 16 recites a large language model, so the language-model part of the pipeline is already inside this family."),
    ("168-072-859-365-199",
     "Claim 1 of this Q (Cue) application is directed to silent voice control from facial skin micromovements, with dependent claims on training and on distinguishing pre-vocalisation movement from other facial movement.",
     "Q (Cue) is the camera/micromovement alternative and its 101-member family is the broadest non-EMG block, useful as the fallback comparison when arguing that an EMG patch senses a different signal."),
    ("US_12154572_B2",
     "Claim 1 claims a non-transitory medium that trains on first signals representing prevocalisation facial skin micromovements, second signals representing sounds in a later period, correlates the recognised words with the earlier micromovements, and stores the correlation.",
     "The granted Q (Cue) claim is a training method rather than a sensor geometry, so it constrains any calibration approach that pairs an earlier silent signal with later audible speech."),
    ("US_12525240_B1",
     "Claim 1 claims accessing an ML model trained to detect inner speech on a general-population dataset, collecting a user's EMG signals, under-sampling negative-label samples and over-sampling positive-label samples, updating the model parameters, and detecting the user's inner speech with the updated model.",
     "This granted Snap claim is a direct hit on fast per-user calibration of a silent-speech decoder from a general model, which makes area 3 the most crowded part of the landscape."),
    ("US_12346500_B1",
     "Claim 1 claims collecting a first set of EMG signals over a time interval, generating features, generating a probability of inner-speech presence with an ML model, comparing that probability to a specified threshold, and detecting inner speech when the threshold is transgressed.",
     "Snap's threshold-on-probability claim is the functional equivalent of a null/activation decision, so it is the closest granted claim to gating a decoder on detected inner speech."),
    ("US_12367784_B1",
     "Claim 1 claims presenting a prompt on a display with instructions for a user to imagine speaking a specified word without vocalising, storing EMG blocks, processing them with a model to compute informative features, detecting inner speech, and presenting an indication in response.",
     "This is a guided-training claim that tells the user what to imagine, which is the closest granted claim to any app-guided session, although it guides the utterance rather than the electrode position."),
    ("US_12670910_B2",
     "Claim 1 claims presenting an instruction to produce inner speech, collecting EMG, classifying it to predict a word or phrase, and concurrently generating and displaying numerical measures of prediction accuracy in a graphical user interface.",
     "Snap claims the live accuracy readout during calibration, which overlaps any per-session progress or quality indicator we might show the user."),
    ("US_12586568_B2",
     "Claim 1 claims establishing a relationship between EMG for overt speech, EMG for inner speech and rest data, transforming overt speech signals into inner-speech training data using that relationship, and training a decoder on the transformed data.",
     "This is the synthetic-training-data route to avoiding a long per-user recording session, and it is granted, so it narrows the obvious data-augmentation answer to small user datasets."),
    ("US_12444406_B2",
     "Claim 1 claims an iterative loop in which EMG for inner speech of specified words is decoded into predictions, the predictions are presented to the user, and a training set is formed from the predictions, the EMG and the specified words as ground truth with weights applied to portions of the EMG.",
     "Snap's iterative learning loop claims user-in-the-loop correction as training data, which is the closest granted claim to a calibration session that improves while the user watches the guesses."),
    ("US_12632112_B1",
     "Claim 1 claims detecting inner speech in EMG data, adjusting a progress indicator in response, determining that the indicator transgressed a threshold, and triggering an operation when it does.",
     "The claim turns a detected inner-speech event into a trigger for an action, which is the nearest granted wording to an activation gesture that fires a command, but it does not recite a jaw clench or a null class."),
    ("US_12567417_B1",
     "Claim 1 claims accessing EMG blocks from multiple channels generated by subthreshold activity of speech muscles, computing a metric per block, determining that a channel's metric transgresses a detection threshold, and generating audible or visual feedback that the threshold was transgressed.",
     "This individual filing claims per-channel threshold feedback, which is close to telling the user that an electrode is or is not picking up usable signal during a session."),
    ("US_12198698_B1",
     "Claim 1 claims a device with transmitting and receiving antennas whose radio-frequency radiation patterns overlap speech articulators, where reflected RF data modulated by articulator movement is processed to detect non-audible speech, and the device is coupled to the exterior of the head.",
     "Reflex Technologies claims a non-EMG, head-mounted silent-speech sensor, which matters because it is a granted alternative that could be cited against broad 'head-worn silent speech' wording."),
    ("US_12469488_B2",
     "Claim 1 claims a method using an RF sensing device worn externally on a head or neck, with transmit and receive antennas, collecting RF data modulated by speech articulators and outputting the determined non-audible speech.",
     "The method claim expressly recites a head-or-neck worn unit, so it is the closest granted non-EMG claim to our neck-worn form factor and must be distinguished by the sensing modality."),
    ("US_11045137_B2",
     "Claim 1 claims a wearable bioelectrical sensing device with four electrodes, a first housing containing portions of the first two, and an angled portion that guides corresponding angled electrode portions into a starting position while the electrodes remain free to translate in X, Y and Z.",
     "This Meta grant claims a mechanical housing that self-aligns electrodes, which is the closest claim to how electrodes are held and connected in a concealed wearable, and it is relevant to re-donning and electrode shift."),
    ("US_10842403_B2",
     "Claim 1 claims a method of increasing signal quality from electrodes of a headset while maintaining the electrodes in the same physical location, by evaluating a property of a first and then a second neurological signal against a quality threshold.",
     "The claim addresses keeping electrodes in place and checking signal quality, which is the closest granted wording to detecting electrode shift after re-donning."),
    ("US_10548500_B2",
     "Claim 1 claims a sensor electrode with a tapering portion and a flexible protruding portion that contacts a body part, an electrode supporter, a sensor support maintaining contact, and a wearable main body, with a defined gradient of the protruding portion's longitudinal section.",
     "Samsung's claim is about the electrode's own shape for reliable skin contact, so it is prior art for the electrode-to-skin interface rather than for the interconnect or the electronics."),
    ("US_11317867_B2",
     "Claim 1 claims a flexible top housing, a flexible lower housing with a sensor bore, and an electrical subsystem between them including a flexible printed circuit board with a sensor contact pad, a sensor and an electrically conductive adhesive patch.",
     "This Medtronic grant claims a flexible PCB plus conductive adhesive stack in a flexible housing, which is the closest granted claim to a thin flexible electrode-and-interconnect assembly."),
    ("US_11154232_B2",
     "Claim 1 claims a conformal sensing device with a mechano-acoustic sensor, a wireless transmitter, and a flexible housing with an elastomeric core between upper and lower insulating layers, the core having a lower modulus than the layers.",
     "The Rogers-group claim covers a soft conformal wireless sensing stack, which is the reference point for a skin-like patch and for the mechanical argument that a thin laminated electrode is different from a rigid device."),
    ("EP_2356680_B1",
     "Claim 1 claims an apparatus with discrete electronic islands and at least one stretchable electrical interconnect connecting them, arranged boustrophedonically as parallel rungs with a length-to-displacement ratio of at least 10:1, where the interconnect is formed of a rigid semiconductor material.",
     "This granted MC10 claim is the core stretchable-interconnect geometry and is active to 2029, so it is the closest granted claim to thin meandering conductors between rigid islands on skin."),
    ("EP_2902293_B1",
     "Claim 1 claims a method of assembling a stretchable device by attaching components to an elastomeric substrate, arranging a boustrophedonic semiconductor interconnect with a rung length-to-displacement ratio of at least 10:1, interconnecting the components, and stretching the substrate.",
     "The method claim covers making the same stretchable interconnect, so both the product and the process of a meander-on-elastomer interconnect are already granted to MC10."),
    ("EP_4434456_A1",
     "Claim 1 claims a neckband to be worn on a shoulder, with a sensor acquiring sensor data and a processor determining a state of the user wearing the neckband on the shoulder and performing an action according to the state.",
     "Sony's pending neckband claim is the closest claim to a neck-worn electronics unit, but it claims state detection and an action, not streaming biosignals to a phone or glasses for speech decoding."),
    ("US_11683632_B2",
     "Claim 1 claims a microphone producing an acoustic signal for a key-phrase and other vocalisations, an accelerometer producing a signal for the key-phrase, and a processor that sends the acoustic payload and generates an ASR trigger from the combination of the acoustic and accelerometer signals.",
     "Apple's granted trigger claim is the closest granted wording to an activation event that starts speech recognition, but it requires a spoken key-phrase plus an accelerometer, not a jaw clench or a null class."),
    ("US_10679644_B2",
     "Claim 1 claims receiving sensor data from multiple sensors associated with low-amplitude speech including biometric data, receiving video of the face, mapping the sensor data to syllables to form a string, and transmitting amplified speech.",
     "IBM's multi-sensor claim shows a granted combination of facial sensors with video for silent/whispered speech, which is useful prior art for arguing that a single-modality EMG patch is a different combination."),
    ('US20230088533A1',
     'Claim 1 claims a biopotential-based gesture-control system with a plurality of electrode pairs, a motion sensor, a controller and a classifier, and a monitoring state in which data that does not satisfy one or more action criteria is returned without being transmitted to the classifier, while data that satisfies the criteria is classified into a gesture and turned into a machine instruction.',
     "Pison's abandoned application is the closest claim wording found to an activation gate plus a null class before the classifier, but it claims gesture control rather than silent speech and it is not in force, so it narrows the obvious wording without blocking it."),
    ('US20210390167A1',
     'Claim 1 claims a computing device that displays a first text, acquires a camera video sequence of the user subvocalizing it, magnifies the correlated body-part motions, derives a phrasing signature and authenticates the user when that signature matches a reference.',
     "Ericsson's application is a camera-based subvocal authentication claim, useful because it shows that 'subvocal' wording is already claimed in a non-EMG modality, so our EMG claim has to be distinguished by the sensed signal rather than by the word."),
    ('WO2018223388A1',
     "Claim 1 claims an apparatus with a microphone positioned near the user's mouth that detects a silent voice from ingressive air flow through the gap between the apparatus and the mouth.",
     "Microsoft's ceased WO is an airflow-and-microphone route to silent voice, not a biosignal route, and it is useful only to show how broad the phrase 'silent voice input' has been made."),
    ('WO2025038844A1',
     "The page serves no claim text for this WO (the indexed WIPO text carries none), so only the record data is stated: title 'Use of non-audible silent speech commands for automated assistants', applicant Google LLC, priority 2023-08-17, CPC G10L15/24 and G10L2015/223.",
     "It is the nearest title-level hit for feeding silent-speech commands to an assistant, but without claim text it cannot be quoted or mapped, and Google's status field says Ceased."),
    ('WO2025014394A1',
     'The page serves no claim text for this WO; the record shows Xpanceo Research on Natural Science LLC, priority 2023-07-10, CPC G06F3/015 and G02C7/04, and a title about an augmented-reality interface control system.',
     'It is the only opened AR-glasses control filing that carries the nervous-system-input code G06F3/015, the code family a glasses link would sit in, but the claims were unavailable so no mapping is claimed.'),
    ('WO2023088083A1',
     "The page serves no claim text for this WO; the record is Evoco Labs' speech-enhancement filing, priority 2021-11-18, with CPC codes only in G10L21 and G10L25 (speech enhancement and feature extraction).",
     'It is a speech-processing filing with no wearable, electrode or placement claim, so it is recorded as opened and is not relevant to any of the seven areas.'),
    ('US20100131268A1',
     'Claim 1 claims a voice-estimation interface adapted to probe a vocal tract and a signal-converter module that processes the probe signals to estimate voice.',
     "Alcatel-Lucent's abandoned vocal-tract probing claim is a non-EMG, non-wearable route, useful only as background showing that 'voice estimation' wording predates the current silent-speech filings."),
    ('US20120136660A1',
     'Claim 1 claims a speaker that directs an excitation signal into a vocal tract, a microphone that detects the vocal-tract response, and a processor that derives formant frequencies from the response and identifies a phoneme from them.',
     'It is the later Alcatel-Lucent vocal-tract probe claim, abandoned, and it does not touch a skin electrode, a wearable housing or a decoder calibration, so it is background only.'),
    ('US20130090931A1',
     'Claim 1 claims a multi-modal communication system whose primary modality is a tongue-tracking unit with a tracer on the tongue and a sensing unit, combined with a secondary modality.',
     "Georgia Tech's abandoned tongue-tracking claim is an alternative silent-input modality, useful to show that non-EMG silent interfaces were claimed early, not as a close hit on any of the seven areas."),
    ('US20150370320A1',
     'Claim 1 claims a touch-based and/or gesture-based human-to-computer textile interface with an article of clothing and an array or mesh of electromagnetic sensors woven into the fabric that transduce touch or gestures into computer inputs.',
     "Medibotics' abandoned claim is a fabric-integrated sensor array, the closest opened wording to a textile electrode garment, but it claims touch and gesture sensing rather than biopotentials on the face or neck."),
    ('US20180233140A1',
     'Claim 1 claims an intelligent digital assistant that trains two voice models on two sub-fragments of one speech fragment, cross-scores each fragment against the other model, and determines from the two confidence values whether the same speaker produced both.',
     'It is the only opened record that carries CPC G10L2015/226, and its claim is speaker-change detection, not silent articulation, a wearable or a placement aid, so it fills the code without touching any of the seven areas.'),
]


INDEX = {
    'US_10878818_B2': {
        "title": 'US10878818B2 — Methods and apparatus for silent speech interface',
        "url": 'https://www.lens.org/lens/patent/US_10878818_B2',
        "people": [
            'Arnav Kapur',
            'Shreyas Kapur',
            'Patricia Maes',
        ],
        "year": '2017',
    },
    '045-073-728-605-863': {
        "title": 'WO2019050881A1 — METHODS AND APPARATUS FOR SILENT SPEECH INTERFACE',
        "url": 'https://www.lens.org/lens/patent/045-073-728-605-863',
        "people": [
            'Arnav Kapur',
            'Shreyas Kapur',
            'Patricia Maes',
        ],
        "year": '2017',
    },
    '124-274-805-307-259': {
        "title": 'US20240221751A1 — WEARABLE SILENT SPEECH DEVICE, SYSTEMS, AND METHODS',
        "url": 'https://www.lens.org/lens/patent/124-274-805-307-259',
        "people": [
            'Sahaj Garg',
            'Tanay Kothari',
            'Anthony Leonardo',
            'Lucas Marsh',
            'Dawid Bodgal',
            'Jeff Talbot',
        ],
        "year": '2023',
    },
    '168-823-659-596-990': {
        "title": 'US20240221719A1 — SYSTEMS AND METHODS FOR PROVIDING LOW LATENCY USER FEEDBACK ASSOCIATED WITH A USER SPEAKING SILENTLY',
        "url": 'https://www.lens.org/lens/patent/168-823-659-596-990',
        "people": [
            'Tanay Kothari',
            'Anthony Leonardo',
            'Sahaj Garg',
        ],
        "year": '2023',
    },
    '045-871-880-751-474': {
        "title": 'US20240220811A1 — SYSTEM AND METHOD FOR USING GESTURES AND EXPRESSIONS FOR CONTROLLING SPEECH APPLICATIONS',
        "url": 'https://www.lens.org/lens/patent/045-871-880-751-474',
        "people": [
            'Sahaj Garg',
            'Tanay Kothari',
            'Anthony Leonardo',
        ],
        "year": '2023',
    },
    'US_12505842_B2': {
        "title": 'US12505842B2 — Devices, systems, and methods for personal speech recognition and replacement',
        "url": 'https://www.lens.org/lens/patent/US_12505842_B2',
        "people": [
            'Anaïs Rameau',
            'Simon Dunham',
            'Fei Wang',
        ],
        "year": '2019',
    },
    'US_12400473_B2': {
        "title": 'US12400473B2 — Wearable facial movement tracking devices',
        "url": 'https://www.lens.org/lens/patent/US_12400473_B2',
        "people": [
            'Cheng Zhang',
            'Tuochao Chen',
            'Benjamin Steeper',
            'Francois Guimbretiere',
            'Ke Li',
            'Ruidong Zhang',
            'Hyunchul Lim',
        ],
        "year": '2020',
    },
    'US_10621973_B1': {
        "title": 'US10621973B1 — Sub-vocal speech recognition apparatus and method',
        "url": 'https://www.lens.org/lens/patent/US_10621973_B1',
        "people": [
            'Ryan Mcvicker',
            'Brett Eigenbrode',
        ],
        "year": '2017',
    },
    'US_8082149_B2': {
        "title": 'US8082149B2 — Methods and apparatuses for myoelectric-based speech processing',
        "url": 'https://www.lens.org/lens/patent/US_8082149_B2',
        "people": [
            'Tanja Schultz',
            'Alexander Walbel',
        ],
        "year": '2006',
    },
    '066-659-600-047-268': {
        "title": 'US20160314781A1 — COMPUTER-IMPLEMENTED METHOD, COMPUTER SYSTEM AND COMPUTER PROGRAM PRODUCT FOR AUTOMATIC TRANSFORMATION OF MYOELECTRIC SIGNALS INTO AUDIBLE SPEECH',
        "url": 'https://www.lens.org/lens/patent/066-659-600-047-268',
        "people": [
            'Tanja Schultz',
            'Michael Wand',
            'Matthias Janke',
        ],
        "year": '2013',
    },
    'US_11216069_B2': {
        "title": 'US11216069B2 — Systems and methods for improved speech recognition using neuromuscular information',
        "url": 'https://www.lens.org/lens/patent/US_11216069_B2',
        "people": [
            'Adam Berenzweig',
            'Patrick Kaifosh',
            'Alan Huan Du',
            'Jeffrey Scott Seely',
        ],
        "year": '2018',
    },
    'EP_3843617_B1': {
        "title": 'EP3843617B1 — KAMERAGEFÜHRTE INTERPRETATION VON NEUROMUSKULÄREN SIGNALEN',
        "url": 'https://www.lens.org/lens/patent/EP_3843617_B1',
        "people": [
            'Adam Berenzweig',
            'Thomas Reardon',
            'Christopher Osborn',
            'Patrick Kaifosh',
            'Brett Jurman',
            'Daniel Wetmore',
        ],
        "year": '2018',
    },
    'US_12482449_B2': {
        "title": 'US12482449B2 — Systems and methods for using silent speech in a user interaction system',
        "url": 'https://www.lens.org/lens/patent/US_12482449_B2',
        "people": [
            'Sahaj Garg',
            'Tanay Kothari',
            'Anthony Leonardo',
        ],
        "year": '2023',
    },
    '168-072-859-365-199': {
        "title": 'US20250028804A1 — SILENT VOICE CONTROL BASED ON FACIAL SKIN MICROMOVEMENTS',
        "url": 'https://www.lens.org/lens/patent/168-072-859-365-199',
        "people": [
            'Yonatan Wexler',
            'Avi Barliya',
        ],
        "year": '2021',
    },
    'US_12154572_B2': {
        "title": 'US12154572B2 — Identifying silent speech using recorded speech',
        "url": 'https://www.lens.org/lens/patent/US_12154572_B2',
        "people": [
            'Yonatan Wexler',
        ],
        "year": '2022',
    },
    'US_12525240_B1': {
        "title": 'US12525240B1 — User calibration of EMG speech signal detection',
        "url": 'https://www.lens.org/lens/patent/US_12525240_B1',
        "people": [
            'Mark Kliger',
            'Yaron Laufer',
            'Meir Meshulam',
            'Assif Ziv',
        ],
        "year": '2023',
    },
    'US_12346500_B1': {
        "title": 'US12346500B1 — EMG speech signal detection',
        "url": 'https://www.lens.org/lens/patent/US_12346500_B1',
        "people": [
            'Mark Kliger',
            'Meir Meshulam',
            'Assif Ziv',
        ],
        "year": '2023',
    },
    'US_12367784_B1': {
        "title": 'US12367784B1 — Training users to produce inner speech',
        "url": 'https://www.lens.org/lens/patent/US_12367784_B1',
        "people": [
            'Elizabeth Izakson',
            'Meir Meshulam',
            'Assif Ziv',
        ],
        "year": '2023',
    },
    'US_12670910_B2': {
        "title": 'US12670910B2 — Inner speech production performance measurement and quantification',
        "url": 'https://www.lens.org/lens/patent/US_12670910_B2',
        "people": [
            'Elizabeth Izakson',
            'Meir Meshulam',
            'Hagar Yamin',
            'Assif Ziv',
        ],
        "year": '2023',
    },
    'US_12586568_B2': {
        "title": 'US12586568B2 — Synthetically generating inner speech training data',
        "url": 'https://www.lens.org/lens/patent/US_12586568_B2',
        "people": [
            'Yaron Laufer',
            'Meir Meshulam',
            'Assif Ziv',
        ],
        "year": '2023',
    },
    'US_12444406_B2': {
        "title": 'US12444406B2 — Inner speech iterative learning loop',
        "url": 'https://www.lens.org/lens/patent/US_12444406_B2',
        "people": [
            'Marcos Jimenez',
            'Meir Meshulam',
            'Assif Ziv',
        ],
        "year": '2023',
    },
    'US_12632112_B1': {
        "title": 'US12632112B1 — Human-machine interaction using EMG speech signals',
        "url": 'https://www.lens.org/lens/patent/US_12632112_B1',
        "people": [
            'Tal Pais',
            'Mark Kliger',
            'Meir Meshulam',
            'Assif Ziv',
        ],
        "year": '2023',
    },
    'US_12567417_B1': {
        "title": 'US12567417B1 — EMG speech signal detection with feedback',
        "url": 'https://www.lens.org/lens/patent/US_12567417_B1',
        "people": [
            'Mark Kliger',
            'Yaron Laufer',
            'Meir Meshulam',
            'Assif Ziv',
        ],
        "year": '2022',
    },
    'US_12198698_B1': {
        "title": 'US12198698B1 — Devices for non-audible speech detection',
        "url": 'https://www.lens.org/lens/patent/US_12198698_B1',
        "people": [
            'Tyler Stephen Benster',
            'Reshef Haim Elisha',
            'Guy Halleck Wilson',
            'Kaveh Moussakhani',
        ],
        "year": '2023',
    },
    'US_12469488_B2': {
        "title": 'US12469488B2 — Methods for non-audible speech detection',
        "url": 'https://www.lens.org/lens/patent/US_12469488_B2',
        "people": [
            'Tyler Stephen Benster',
            'Reshef Haim Elisha',
            'Guy Halleck Wilson',
            'Kaveh Moussakhani',
        ],
        "year": '2023',
    },
    'US_11045137_B2': {
        "title": 'US11045137B2 — Methods and apparatus for improved signal robustness for a wearable neuromuscular recording device',
        "url": 'https://www.lens.org/lens/patent/US_11045137_B2',
        "people": [
            'Curtis Barbre',
            'Jonathan Reid',
            'Ning Guo',
            'Brandon Pool',
        ],
        "year": '2018',
    },
    'US_10842403_B2': {
        "title": 'US10842403B2 — Systems and methods to gather and analyze electroencephalographic data',
        "url": 'https://www.lens.org/lens/patent/US_10842403_B2',
        "people": [
            'Yakob Badower',
            'Ramachandran Gurumoorthy',
            'A K Pradeep',
            'Robert T Knight',
        ],
        "year": '2012',
    },
    'US_10548500_B2': {
        "title": 'US10548500B2 — Apparatus for measuring bioelectrical signals',
        "url": 'https://www.lens.org/lens/patent/US_10548500_B2',
        "people": [
            'Se-Hoon Lim',
            'Jun-Hyung Park',
            'Hee-Jae Jo',
            'Jang-Beom Yang',
            'Jae-Min Jung',
            'Eun-Mi Oh',
            'Jong-Ho Choi',
            'Jun-Ho Koh',
            'Chang-Hyun Lee',
            'Yong-Hyun Lim',
            'Hae-In Chun',
        ],
        "year": '2014',
    },
    'US_11317867_B2': {
        "title": 'US11317867B2 — Flexible physiological characteristic sensor assembly',
        "url": 'https://www.lens.org/lens/patent/US_11317867_B2',
        "people": [
            'Ellis Garai',
            'David Choy',
            'David C Antonio',
            'Robert C Mucic',
        ],
        "year": '2019',
    },
    'US_11154232_B2': {
        "title": 'US11154232B2 — Mechano-acoustic sensing devices and methods',
        "url": 'https://www.lens.org/lens/patent/US_11154232_B2',
        "people": [
            'Jae-Woong Jeong',
            'John Rogers',
            'Yu Hao Liu',
        ],
        "year": '2017',
    },
    'EP_2356680_B1': {
        "title": 'EP2356680B1 — EXTREM DEHNBARE ELEKTRONIK',
        "url": 'https://www.lens.org/lens/patent/EP_2356680_B1',
        "people": [
            'William J Arora',
            'Roozbeh Ghaffari',
        ],
        "year": '2008',
    },
    'EP_2902293_B1': {
        "title": 'EP2902293B1 — HERSTELLUNG EXTREM DEHNBARER ELEKTRONIK',
        "url": 'https://www.lens.org/lens/patent/EP_2902293_B1',
        "people": [
            'William Arora',
            'Roozbeth Ghaffari',
        ],
        "year": '2008',
    },
    'EP_4434456_A1': {
        "title": 'EP4434456A1 — HALSBAND',
        "url": 'https://www.lens.org/lens/patent/EP_4434456_A1',
        "people": [
            'Justinas Miseikis',
        ],
        "year": '2023',
    },
    'US_11683632_B2': {
        "title": 'US11683632B2 — Automatic speech recognition triggering system',
        "url": 'https://www.lens.org/lens/patent/US_11683632_B2',
        "people": [
            'Sorin V Dusan',
            'Aram M Lindahl',
            'Robert D Watson',
        ],
        "year": '2017',
    },
    'US_10679644_B2': {
        "title": 'US10679644B2 — Production of speech based on whispered speech and silent speech',
        "url": 'https://www.lens.org/lens/patent/US_10679644_B2',
        "people": [
            'Sarbajit K Rakshit',
            'Martin G Keen',
            'James E Bostick',
            'Jr John M Ganci',
        ],
        "year": '2017',
    },
    'US20230088533A1': {
        "title": 'US20230088533A1 — Detecting and Using Body Tissue Electrical Signals',
        "url": 'https://patents.google.com/patent/US20230088533A1/en',
        "people": [
            'Dexter W. Ang',
            'David O. Cipoletta',
        ],
        "year": '2016',
    },
    'US20210390167A1': {
        "title": 'US20210390167A1 — Authenticating a user subvocalizing a displayed text',
        "url": 'https://patents.google.com/patent/US20210390167A1/en',
        "people": [
            'Matthew John LAWRENSON',
            'Lars Andersson',
            'Till BURKERT',
            'Harm Stefan CRONIE',
            'Jacob Ström',
            'Jan Jasper Van Den Berg',
        ],
        "year": '2016',
    },
    'WO2018223388A1': {
        "title": 'WO2018223388A1 — Silent voice input',
        "url": 'https://patents.google.com/patent/WO2018223388A1/en',
        "people": [
            'Masaaki Fukumoto',
        ],
        "year": '2017',
    },
    'WO2025038844A1': {
        "title": 'WO2025038844A1 — Use of non-audible silent speech commands for automated assistants',
        "url": 'https://patents.google.com/patent/WO2025038844A1/en',
        "people": [
            'Glen Shires',
        ],
        "year": '2023',
    },
    'WO2025014394A1': {
        "title": 'WO2025014394A1 — Augmented reality interface control system and method',
        "url": 'https://patents.google.com/patent/WO2025014394A1/en',
        "people": [
            'Aleksey Vladimirovich ARSENIN',
            'Vyacheslav Sergeevich BRUNOV',
            'Valentin Sergeevich VOLKOV',
            'Yuliya Yuryevna NEKRASOVA',
            'Aleksey Evgenievich OSADCHIY',
            'Valentin Romanovich SOLOVEI',
            'Alexander Vyacheslavovich SYUY',
            'Marina Mikhailovna CHUGUNOVA',
        ],
        "year": '2023',
    },
    'WO2023088083A1': {
        "title": 'WO2023088083A1 — Speech enhancement method and apparatus',
        "url": 'https://patents.google.com/patent/WO2023088083A1/en',
        "people": [
            '陆丛希',
            '李林锴',
            '周昊帅',
            '袁宇帆',
            '孙鸿程',
        ],
        "year": '2021',
    },
    'US20100131268A1': {
        "title": 'US20100131268A1 — Voice-estimation interface and communication system',
        "url": 'https://patents.google.com/patent/US20100131268A1/en',
        "people": [
            'Lothar Benedikt Moeller',
        ],
        "year": '2008',
    },
    'US20120136660A1': {
        "title": 'US20120136660A1 — Voice-estimation based on real-time probing of the vocal tract',
        "url": 'https://patents.google.com/patent/US20120136660A1/en',
        "people": [
            'Dale D. Harman',
            'Lothar Benedikt Moeller',
        ],
        "year": '2010',
    },
    'US20130090931A1': {
        "title": 'US20130090931A1 — Multimodal communication system',
        "url": 'https://patents.google.com/patent/US20130090931A1/en',
        "people": [
            'Maysam Ghovanloo',
            'Xueliang Huo',
        ],
        "year": '2011',
    },
    'US20150370320A1': {
        "title": 'US20150370320A1 — Smart Clothing with Human-to-Computer Textile Interface',
        "url": 'https://patents.google.com/patent/US20150370320A1/en',
        "people": [
            'Robert A. Connor',
        ],
        "year": '2014',
    },
    'US20180233140A1': {
        "title": 'US20180233140A1 — Determining speaker changes in audio input',
        "url": 'https://patents.google.com/patent/US20180233140A1/en',
        "people": [
            'Kazuhito Koishida',
            'Uros Batricevic',
        ],
        "year": '2017',
    },
}


def render() -> str:
    keys = {key for key, _, _ in ROWS}
    assert keys == set(INDEX), f"ROWS/INDEX mismatch: {keys ^ set(INDEX)}"
    out = []
    for key, what, useful in ROWS:
        meta = INDEX[key]
        assert len(what) >= 40 and len(useful) >= 40, key
        out.append({
            "kind": "patent",
            "title": meta["title"],
            "url": meta["url"],
            "people": meta["people"],
            "year": meta["year"],
            "what_they_did": what,
            "useful_for_us": useful,
        })
    return "\n".join(json.dumps(r, ensure_ascii=False) for r in out) + "\n"


def main(argv: list[str]) -> int:
    text = render()
    n = text.count("\n")
    if "--check" in argv:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        print(f"{OUT}: {n} rows, {'up to date' if current == text else 'STALE'}")
        return 0 if current == text else 1
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {n} rows -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
