#!/usr/bin/env python3
"""The citation index for research/jaw/articulation-design.md.

Every record below was opened by hand in the session that wrote the note: the paper PDF or
abstract, the dataset card, or the repository page.  This script is the source of truth; it
renders research/jaw/sources-articulation-design.jsonl so the file can be regenerated and
checked offline.

    python3 scripts/build_sources_articulation.py           # write the .jsonl
    python3 scripts/build_sources_articulation.py --check   # exit 0 if the .jsonl is current
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "research" / "jaw" / "sources-articulation-design.jsonl"

RECORDS = [
    {
        "kind": "paper",
        "title": "Visual units and confusion modelling for automatic lip-reading",
        "url": "http://www2.cmp.uea.ac.uk/~sjc/Image-and-vision-computing-2015.pdf",
        "people": ["Helen L. Bear", "Richard W. Harvey"],
        "year": 2016,
        "what_they_did": "Compared modelling visemes against modelling phonemes for automatic lip-reading, and counted homophenous words in their 979-word recording set under the Fisher phoneme-to-viseme map: 106 words (10.83%) but 8988 of 26114 word tokens (34.42%), giving a 65.58% ceiling on word accuracy from collisions alone.",
        "useful_for_us": "This is the only source that puts real numbers on how much English collapses when phonemes are merged into visual classes, and it defines the exact type-versus-token distinction our collision calculation must reproduce.",
    },
    {
        "kind": "paper",
        "title": "Phoneme-to-viseme mappings: the good, the bad, and the ugly",
        "url": "https://arxiv.org/abs/1805.02934",
        "people": ["Helen L. Bear", "Richard W. Harvey"],
        "year": 2017,
        "what_they_did": "Collected eight vowel and fifteen consonant phoneme-to-viseme maps from the literature and paired them into 120 maps, then compared recognition with HMM classifiers on AVL2 and RMAV, using the BEEP British English dictionary for viseme transcriptions, and derived new data-driven Bear visemes.",
        "useful_for_us": "It shows that the choice of phoneme-to-viseme map is itself a large design space and that no map is canonical, which is why our per-articulator channel map cannot simply reuse an existing viseme set.",
    },
    {
        "kind": "paper",
        "title": "An Optimal Set of Flesh Points on Tongue and Lips for Speech-Movement Classification",
        "url": "https://pubmed.ncbi.nlm.nih.gov/26564030/",
        "people": ["Jun Wang", "Ashok Samal", "Panying Rong", "Jordan R. Green"],
        "year": 2016,
        "what_they_did": "Recorded tongue and lip movement from 13 talkers with Carstens AG500 and NDI Wave electromagnetic articulographs and compared SVM classification of 8 vowels, 11 consonants, words and phrases for different flesh-point combinations, finding that T1, T4, UL and LL reach 91%-95% and are equivalent to all six sensors.",
        "useful_for_us": "This is the closest published sensor-reduction result for articulation and shows that tongue tip, tongue back and the two lips each carry information while the front tongue body does not.",
    },
    {
        "kind": "paper",
        "title": "Articulatory Feature Prediction from Surface EMG during Speech Production",
        "url": "https://arxiv.org/abs/2505.13814",
        "people": ["Jihwan Lee", "Kevin Huang", "Kleanthis Avramidis", "Simon Pistrosch", "Monica Gonzalez-Machorro", "Yoonjeong Lee", "Bjorn Schuller", "Louis Goldstein", "Shrikanth Narayanan"],
        "year": 2025,
        "what_they_did": "Predicted articulatory features from eight surface EMG electrodes with a convolutional plus Transformer model, then analysed which electrode contributes to which EMA sensor and measured subsets of four, three and two electrodes against phoneme error rate, word error rate and SpeechBERTScore.",
        "useful_for_us": "It gives the per-electrode to per-articulator mapping and the accuracy cost of dropping channels, and it states plainly that lips are better captured than the tongue by surface EMG.",
    },
    {
        "kind": "paper",
        "title": "SilentSpeller: Towards mobile, hands-free, silent speech text entry using electropalatography",
        "url": "https://tangemicioglu.com/files/papers/SilentSpeller_CHI_2022.pdf",
        "people": ["Naoki Kimura", "Tan Gemicioglu", "Jonathan Womack", "Yuhang Zhao", "Abdelkareem Bedri", "Richard Li", "Alex Su", "Alex Olwal", "Jun Rekimoto", "Thad Starner"],
        "year": 2022,
        "what_they_did": "Built a silent text-entry system on a 124-electrode electropalatography retainer sampled at 100 Hz, recognised the 26 letters of the alphabet rather than phonemes, and reported 97% character and 93% word accuracy offline on 1164 words, 94% on 100 unseen words, and 37 words per minute at 87% accuracy live.",
        "useful_for_us": "It is the concrete example of how a tongue-contact channel copes with phonemes that produce no palatal contact, by switching the unit from phoneme to letter name and letting word models resolve similar palatograms such as B/P and D/T/Z.",
    },
    {
        "kind": "paper",
        "title": "Speech-language pathologists' knowledge of tongue/palate contact for consonants",
        "url": "https://pubmed.ncbi.nlm.nih.gov/22106891/",
        "people": ["Sharynne McLeod"],
        "year": 2011,
        "what_they_did": "Asked 175 speech-language pathologists to draw tongue/palate contact for 24 English consonants and compared their drawings with electropalatography-established adult contact, finding best accuracy for the no-contact consonants h, p and f, then the velars g, k and ng, and poor awareness of lateral bracing and grooving.",
        "useful_for_us": "It names the consonants that produce no palatal contact and the ones whose contact is lateral or grooved, which is exactly the per-phoneme contact classification a tongue channel has to be designed around.",
    },
    {
        "kind": "paper",
        "title": "Allophonic variation in English coronal stops: An EPG corpus study",
        "url": "https://twpl.library.utoronto.ca/index.php/twpl/article/download/29221/21935",
        "people": ["Katherine Sung", "Alexei Kochetov"],
        "year": 2018,
        "what_they_did": "Analysed electropalatographic recordings of Canadian English coronal stops and quantified linguopalatal contact with whole-total and centre-of-gravity measures, showing complete alveolar closure over the first two to four rows with side contact for /t/ and last-row closure with substantial side contact for /k/, while the bilabial /p/ shows no linguopalatal contact at all.",
        "useful_for_us": "It provides the actual contact geometry per place of articulation, including the side contact that a tongue-sides channel would have to capture and the zero-contact case that any contact sensor misses.",
    },
    {
        "kind": "paper",
        "title": "Distinguishing Homophenes Using Multi-Head Visual-Audio Memory for Lip Reading",
        "url": "https://ojs.aaai.org/index.php/AAAI/article/download/20003/19762",
        "people": ["Minsu Kim", "Jeong Hun Yeo", "Yong Man Ro"],
        "year": 2022,
        "what_they_did": "Proposed a multi-head visual-audio memory that stores audio-visual features during training so a lip-reading model can separate homophenous words at test time, and evaluated word accuracy on LRW, LRW-1000 and LRS2.",
        "useful_for_us": "It confirms that homophene collisions are a recognised failure mode of visual-only recognition and that the published remedy is extra audio supervision, not a better sensor layout.",
    },
    {
        "kind": "paper",
        "title": "Articulation-to-speech using electro-optical stomatography and articulatory synthesis",
        "url": "https://issp2020.yale.edu/S05/stone_05_02_016_abstract.pdf",
        "people": ["Simon Stone", "Peter Birkholz"],
        "year": 2020,
        "what_they_did": "Combined electro-optical stomatography, which measures palatal contact plus tongue-palate distance and lip opening, with a parametric articulatory synthesiser to map articulation directly to speech parameters instead of vocoder features.",
        "useful_for_us": "It is the fusion case that shows how to cover the no-contact phonemes, by adding distance and lip measurements to a binary contact grid.",
    },
    {
        "kind": "paper",
        "title": "Confusions among visually perceived consonants",
        "url": "https://pubs.asha.org/doi/abs/10.1044/jshr.1104.796",
        "people": ["Cletus G. Fisher"],
        "year": 1968,
        "what_they_did": "Measured how often consonants are confused with each other when perceived visually, producing the consonant confusion matrix that later became the ten-class Fisher viseme set used by most lip-reading homophene analyses.",
        "useful_for_us": "This is the origin of the viseme classes whose word-level collision rate Bear and Harvey quantify, so the class table in our note is attributable to a primary perceptual study rather than to a blog.",
    },
    {
        "kind": "paper",
        "title": "An Improved Model for Voicing Silent Speech",
        "url": "https://aclanthology.org/2021.acl-short.23/",
        "people": ["David Gaddy", "Dan Klein"],
        "year": 2021,
        "what_they_did": "Improved silent-speech-to-audio synthesis from eight facial EMG electrodes and reported per-phoneme confusion and forced-choice articulatory-feature accuracy, including place 96.6%, oral manner 92.9%, nasality 89.1% and voicing 88.1% with only a 2.8-point gain over phoneme context.",
        "useful_for_us": "Its feature table tells us which articulatory dimensions a face and neck channel genuinely carries and which are recovered from language context, which bounds what any added channel can contribute.",
    },
    {
        "kind": "dataset",
        "title": "PanPhon: IPA segments to articulatory feature vectors",
        "url": "https://github.com/dmort27/panphon",
        "people": ["David R. Mortensen", "Patrick Littell", "Akash Bharadwaj", "Kartik Goyal", "Chris Dyer", "Lori Levin"],
        "year": 2016,
        "what_they_did": "Packages a CSV of 6367 IPA segments described by 24 articulatory feature columns (356,894 bytes) together with Python code to map segments to feature vectors, under the MIT-Modern-Variant licence declared in pyproject.toml.",
        "useful_for_us": "It is the licence-clean, 349 KB way to build channel-partition maps from features such as labial, coronal, dorsal, lateral and nasal instead of hand-writing a phoneme table.",
    },
    {
        "kind": "dataset",
        "title": "PHOIBLE: phonological inventories and distinctive features",
        "url": "https://github.com/phoible/dev",
        "people": ["Steven Moran", "Daniel McCloy"],
        "year": 2019,
        "what_they_did": "Maintains a database of more than 3000 phonological inventories covering more than 2100 ISO 639-3 codes with distinctive-feature rows per segment, distributed as data/phoible.csv at 26,455,818 bytes under an MIT repository licence.",
        "useful_for_us": "It is the cross-linguistic check on whether a feature contrast used in a channel map exists in other languages, although it is inventory-shaped rather than English-shaped and much larger than PanPhon.",
    },
    {
        "kind": "dataset",
        "title": "CMUdict: the Carnegie Mellon Pronouncing Dictionary",
        "url": "https://github.com/cmusphinx/cmudict",
        "people": ["Carnegie Mellon University Speech Group"],
        "year": 2015,
        "what_they_did": "Distributes cmudict.dict, 3,618,488 bytes and 84162 entry lines of ARPAbet phoneme strings with stress marks and alternate pronunciations, with a licence stating that use for any research or commercial purpose is completely unrestricted.",
        "useful_for_us": "It is the smallest licence-clean English word-to-phoneme file and therefore the first of the two inputs our offline collision calculation needs.",
    },
    {
        "kind": "dataset",
        "title": "wordfreq: word frequencies for many languages",
        "url": "https://github.com/rspeer/wordfreq",
        "people": ["Robyn Speer"],
        "year": 2025,
        "what_they_did": "Provides per-word frequency estimates for more than 40 languages from many corpora, as a snapshot of usage through about 2021, shipped as a 56,834,549-byte wheel under the Apache-2.0 licence.",
        "useful_for_us": "It is what turns a raw count of colliding word types into a token-weighted estimate, which the 10.83% versus 34.42% gap shows can change the answer by a factor of three.",
    },
    {
        "kind": "dataset",
        "title": "SUBTLEX-US: subtitle-based American English word frequencies",
        "url": "https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexus",
        "people": ["Marc Brysbaert", "Boris New"],
        "year": 2009,
        "what_they_did": "Compiled word form frequency and contextual diversity from a 51-million-word corpus of American subtitles, distributing a 74,286-word list and a 282,170-letter-string raw file as zipped Excel and text downloads.",
        "useful_for_us": "It is an alternative token weighting to wordfreq, but the distribution page states no explicit licence, so it cannot be shipped without asking the authors first.",
    },
    {
        "kind": "dataset",
        "title": "Silent Speech EMG dataset",
        "url": "https://zenodo.org/records/4064409",
        "people": ["David Gaddy", "David Klein", "Dan Klein"],
        "year": 2020,
        "what_they_did": "Publishes facial electromyography recordings during both silent and vocalized speech as a single 3,919,507,637-byte emg_data.tar.gz under CC-BY-4.0, with force-aligned phoneme labels produced through the Montreal Forced Aligner.",
        "useful_for_us": "It is the only large openly licensed silent-speech articulation dataset found, so it is the reference corpus if the collision question is later extended from text to measured signals.",
    },
    {
        "kind": "dataset",
        "title": "The IPA Chart (2020 revision)",
        "url": "https://www.internationalphoneticassociation.org/node/1061",
        "people": ["International Phonetic Association"],
        "year": 2020,
        "what_they_did": "Publishes the International Phonetic Alphabet chart as a place-by-manner-by-voicing grid and a vowel quadrilateral, and states that since July 2012 the charts are freely available under a Creative Commons Attribution-Sharealike 4.0 International licence.",
        "useful_for_us": "It is a licence-clean human-readable reference for articulator rows and columns, but it is a PDF image, not a machine-readable feature table.",
    },
    {
        "kind": "repo",
        "title": "SilentSpeller code repository",
        "url": "https://github.com/supernaiter/SilentSpeller",
        "people": ["Naoki Kimura", "Tan Gemicioglu", "Thad Starner"],
        "year": 2022,
        "what_they_did": "Releases one participant's electropalatography dataset and a formatting script for the SilentSpeller pipeline under Apache-2.0, while stating that the repository is still under construction and that the full GT2K recognition pipeline is not yet published.",
        "useful_for_us": "It is the only open data from an EPG silent-speech system, but it contains no code that scores phoneme classes or vocabulary collisions.",
    },
    {
        "kind": "repo",
        "title": "OpenFaceFX lip-sync pipeline",
        "url": "https://github.com/OpenFaceFX/OpenFaceFX",
        "people": ["OpenFaceFX contributors"],
        "year": 2026,
        "what_they_did": "Implements deterministic phoneme-to-viseme-to-curve animation from audio plus transcript with a phoneme timeline and a configurable viseme stage, under the MIT licence and with numpy as its only runtime dependency.",
        "useful_for_us": "It is the closest maintained code that already takes a custom phoneme-to-viseme mapping, but it renders animation and never counts how many words share a mapped string.",
    },
    {
        "kind": "repo",
        "title": "Multi-head Visual-Audio Memory for lip reading",
        "url": "https://github.com/ms-dot-k/Multi-head-Visual-Audio-Memory",
        "people": ["Minsu Kim", "Jeong Hun Yeo", "Yong Man Ro"],
        "year": 2022,
        "what_they_did": "Releases a PyTorch implementation of the AAAI homophene-disambiguation model under a non-commercial Creative Commons Attribution-NonCommercial 4.0 licence, last pushed in March 2024.",
        "useful_for_us": "It is the only repository found by a GitHub search for homophene that is not a viseme animation tool, and its non-commercial licence rules it out as a dependency.",
    },
    {
        "kind": "repo",
        "title": "Voicing Silent Speech (dgaddy/silent_speech)",
        "url": "https://github.com/dgaddy/silent_speech",
        "people": ["David Gaddy"],
        "year": 2022,
        "what_they_did": "Releases EMG to speech and EMG to text code for the EMNLP 2020 and ACL 2021 silent-speech papers under the MIT licence, with the matching dataset hosted separately on Zenodo and force-aligned phonemes as a git submodule.",
        "useful_for_us": "It is the reference implementation for the eight-electrode EMG setup whose per-feature accuracies bound what a face and neck channel can recover.",
    },
]


def render() -> str:
    lines = []
    for r in RECORDS:
        assert r["kind"] in ("paper", "dataset", "repo"), r["title"]
        for k in ("what_they_did", "useful_for_us"):
            assert len(r[k]) >= 40, (r["title"], k)
        lines.append(json.dumps(r, ensure_ascii=False, sort_keys=True))
    return "\n".join(lines) + "\n"


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        cur = OUT.read_text() if OUT.exists() else ""
        if cur == text:
            print(f"{OUT.name}: {len(RECORDS)} rows, up to date")
            return 0
        print(f"{OUT.name}: STALE — run without --check")
        return 1
    OUT.write_text(text)
    print(f"{OUT.name}: {len(RECORDS)} rows written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
