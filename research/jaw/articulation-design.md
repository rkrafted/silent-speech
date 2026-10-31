# Articulation → sensor layout: what is already published

Research note, 2026-10-20. Scope: public papers, dataset cards and repository READMEs only.
Nothing was downloaded, registered for or installed; sizes below are from HTTP `Content-Length`
headers, package metadata or line counts, not from pulling the files. The question behind it:
**how much does each articulator channel (lips, tongue tip, tongue sides, tongue back, jaw)
reduce word collisions, and has anyone already measured that?**

Short answer up front: the *lip* channel has been measured to death (a 40–60 % claim, and a
34.42 % token collision figure on a 979-word set). The per-articulator version — "if I add a
tongue-back channel, how many words stop colliding?" — has **not** been published. Section 7
says what a 150-line computation would need.

## 1. Viseme and homophene studies: how much English collapses

A **viseme** is a set of phonemes with the same visible mouth shape; two words with the same
viseme string but different phonemes are **homophenous** ("bat", "pat", "mat"). The count depends
entirely on which phoneme→viseme map is used, so every number below is map-specific.

### 1.1 The headline percentages

| Measure | Value | What it is |
|---|---|---|
| Literature claim, quoted | "**as many as 40%–60% of English spoken words could be homophenous**" | Bear & Harvey cite earlier estimates (their ref. 2, Berger, *Visemes and homophenous words*) |
| Word types in their own 979-word set, Fisher map | **106 of 979 = 10.83 %** | "Of the 979 different words spoken in our database, 106 (10.83%) are homophenous when the Fisher phoneme-to-viseme mapping … is used" |
| Word **tokens** in the same set | **8,988 of 26,114 = 34.42 %** | "these homophenous words account for 8988 (34.42%) of all word tokens" |
| Ceiling on word accuracy from collisions alone | **65.58 %** | "even with perfect viseme recognition, the recogniser's performance could be as low as 65.58% if it were always to make the wrong choice between a group of homophenous words" |

The gap between 10.83 % of types and 34.42 % of tokens is the useful part: collisions concentrate
in frequent words (`the`, `a`, `to`, `and`, `you` all collapse into high-frequency viseme
strings), so a lip-only recogniser is worse than the type count suggests.

### 1.2 Which classes were used — the Fisher (1968) map

Bear & Harvey's Table 2 gives the whole map, so it can be reproduced without the 1968 paper:

| Class | Phonemes merged | Collision risk |
|---|---|---|
| V1 | /b/ /p/ /m/ | all bilabials; the classic "bat/pat/mat" |
| V2 | /f/ /v/ | labiodental |
| V3 | /t/ /d/ /s/ /z/ /th/ /dh/ | **six** phonemes — the widest consonant class |
| V4 | /w/ /r/ | |
| V5 | /k/ /g/ /n/ /l/ /ng/ /hh/ /y/ | **seven** phonemes — velars, nasal, lateral, /h/, /j/ |
| V6 | /ch/ /jh/ /sh/ /zh/ | postalveolars |
| V7 | /eh/ /ey/ /ae/ /aw/ /er/ /ea/ | vowels |
| V8 | /uh/ /uw/ | |
| V9 | /iy/ /ih/ /ia/ | |
| V10 | /ah/ /ax/ /ay/ | |

(Labels are quoted verbatim from Bear & Harvey's Table 2, which uses BEEP/ARPAbet-style phone
names; they are not IPA.)

Two things follow. (a) The classes are **not articulator-pure**: V5 mixes a velar stop, a nasal,
a lateral, a glottal and a palatal, because from the *lips* all of them are "nothing visible".
(b) V3 and V5 are where a non-lip channel would pay: any sensor that separates /t/ from /s/ or
/k/ from /ŋ/ removes 6- and 7-way ambiguities at once.

### 1.3 Word lists and dictionaries used

- **BEEP** (British English pronunciation dictionary, Cambridge) is the dictionary used to turn
  orthography into phonemes before mapping to visemes in Bear & Harvey 2017. It is *not* free —
  see §5, and do not redistribute it.
- The 979-word count above is the set of words actually spoken in their AVL2/RMAV recording,
  not a general vocabulary.
- Bear & Harvey 2017 then compare **"eight vowel- and fifteen consonant-maps … paired with each
  other to provide 120 P2V maps to test"**, i.e. there is no canonical viseme set; the choice of
  map is itself a 120-way design decision that changes recogniser accuracy.

## 2. Electropalatography: which phonemes touch the palate

EPG measures **where the tongue contacts the hard palate** with a fixed grid of electrodes
(SilentSpeller's retainer: "124 electrodes … at 100 Hz"). It is a *tongue* channel, so it sees
exactly the classes lips cannot — and misses exactly the classes lips see.

### 2.1 Per-class contact, from EPG data

| Class | Contact pattern | Source (quoted) |
|---|---|---|
| /p/ (bilabial) | **none** — "does not have an active lingual constriction, and thus the palate shows no linguopalatal contact"; /b/ and /m/ are the same place, so expect the same, but the paper only shows /p/ | Sung & Kochetov (2018), EPG corpus of Canadian English coronal stops |
| /h/ /p/ /f/ | the three consonants EPG practitioners classify as **"no contact"** | McLeod 2011: "SLPs were most accurate for consonants with no contact (h, p, f)" |
| /t/ /d/ | complete closure at the alveolar ridge, "the first 2–4 rows of the palate, accompanied by some side contact" | same EPG corpus study (Sung & Kochetov 2018) |
| /k/ /g/ /ŋ/ | closure "in the last row of the palate (the velar region), also with a substantial side contact" — and this class is *easy* for humans to draw | same; McLeod: after the no-contact set, "then velar consonants (g, k, ng)" |
| /s/ /z/ /ʃ/ /ʒ/ | a central **groove**, not a closure; "/s, z, sh, zh/" groove | McLeod 2011 |
| /t/ /d/ /n/ /s/ /z/ | **lateral bracing** ("horseshoe" contact) on the side margins | McLeod 2011 |
| /l/ | lateral contact with an open midline | McLeod 2011 (lateral margins named as the weak spot of clinical knowledge) |

The important negative result for design: **/h/, /p/, /f/ are the consonants EPG practitioners
classify as no-contact**, so a binary tongue-contact channel is blind to them by construction.
Note that /b/ and /m/ are *not* in that set even though they share /p/'s place of articulation, so
an EPG-only design must not assume all bilabials are contact-free.

### 2.2 How EPG recognisers handle the no-contact sounds

- **SilentSpeller (CHI 2022)** does not recognise phonemes at all. "SilentSpeller focuses on
  recognizing the 26 letters of the alphabet, silently mouthed in the context of spelling a
  word." The user spells: "instead of saying 'rapidly' (ra·puhd·lee), the user spells each letter
  'a:r ei pi: di: el wai'". Letter *names* are syllables, so a /p/ is never an isolated
  no-contact segment — it arrives inside /piː/, which has tongue contact and a vowel.
  Residual letter collisions are handled by word-level HMMs over a 1,164-word dictionary:
  "Some similar sounding letters, such as B/P and D/T/Z, have similar palatograms." Reported:
  97 % character / 93 % word accuracy offline, 94 % on 100 unseen words, live 37 wpm at 87 %.
- **Electro-optical stomatography (EOS)** adds optical distance sensors to the contact grid, i.e.
  it measures tongue-palate *distance* where contact is absent — "97% user dependent accuracy
  across four users on a 30-word command vocabulary … User independent recognition averaged
  56%" (as reported in SilentSpeller's related work).
- **TongueBoard** (Li et al.) used 15 common words / 17 choices, "3.78 bits per decision …
  accuracy = 97.1%" — again a closed command vocabulary, not spelling.
- **Dimensionality**: SilentSpeller keeps "the top 16 components ('eigen-palates')" out of 124
  electrodes, so 124 sensors is not a requirement — 16 numbers at 100 Hz carried the recogniser.

## 3. Sensor selection: which channels separate which phonemes

Four studies actually measured "drop sensors, measure the loss". None measured word collisions;
they measured phoneme/word accuracy or correlation with articulator trajectories.

### 3.1 EMA: 6 sensors → 4 sensors is free (Wang et al. 2016)

13 talkers, Carstens AG500 + NDI Wave, 8 vowels + 11 consonants + words + phrases; SVM
classification of flesh-point combinations.

| Sensor set | Result |
|---|---|
| all 6 (T1 tip/blade, T2–T3 tongue-body front, T4 tongue-body back, UL, LL) | reference |
| **T1 + T4 + UL + LL (4)** | "**91%–95%**" and "equivalent to that using all 6 sensors" |

So the tongue *front* (T2/T3) is redundant for phoneme/word classification, while tongue tip,
tongue back, upper lip and lower lip each carry something. This is the closest published thing
to a per-channel ablation — but it stops at accuracy, not at vocabulary collisions.

### 3.2 sEMG: 8 electrodes → 4, and lips beat tongue (Lee et al. 2025)

8 face/neck electrodes predicting EMA trajectories, then speech. Table 3 of the paper:

| Electrode set | EMA correlation | PER % | WER % | SpeechBERTScore |
|---|---|---|---|---|
| all 8 (full model) | — | — | **15.5** | 84.4 |
| **{2,3,4,6}** | **0.882** | 39.7 | **22.9** | 83.2 |
| {2,4,6} | 0.859 | 46.1 | 31.6 | 82.1 |
| {2,4} | 0.816 | 52.1 | 46.9 | 79.9 |

Findings that matter for channel choice:

- "we observe **stronger association in the lips compared to the tongue** … the tongue, being
  internally located, poses greater challenges for accurate movement measurement using external
  skin surface EMG sensors."
- Electrode 2 (chin corner, superficial genioglossus) is strongest for **tongue tip**; electrode 3
  (posterior submental) also tracks the tongue; electrodes 2 and 6 track **lower lip and jaw**.
- Electrode 4 (paralaryngeal) alone gives loudness r = **0.73** and pitch r = **0.32**, "the
  highest among all EMG electrodes" — because it is nearest the larynx.

So sEMG's *best* channels are lips and larynx; tongue-tip comes through weakly and tongue-back
barely at all. Dropping 4 of 8 electrodes costs 7.4 points of WER (15.5 → 22.9).

### 3.3 Articulatory features: what a channel can and cannot recover (Gaddy & Klein 2021)

Forced-choice accuracy (majority / phoneme context only / full EMG), from the project's own
track-12 note:

| Feature | Context | EMG | Gain over context |
|---|---|---|---|
| Place | 80.4 | **96.6** | +16.2 |
| Oral manner | 79.6 | **92.9** | +13.3 |
| Nasality | 84.3 | 89.1 | +4.8 |
| **Voicing** | 85.3 | 88.1 | **+2.8** |

Place and manner are genuinely in the face/neck signal; voicing and nasality are ~recovered from
language context. A layout that claims to separate /p/ from /b/ from the same channels is claiming
the +2.8 column.

### 3.4 Fusion, and what won

| Comparison | Winner | Number |
|---|---|---|
| 6 EMA sensors vs 4 | **4 is enough** | 91–95 %, "equivalent" |
| 8 sEMG vs 4 vs 2 | **4** | WER 15.5 → 22.9 → 46.9 |
| Contact-only EPG vs contact + optical distance | **fusion** (EOS) | 97 % user-dependent, 56 % cross-user |
| Lip-only viseme recognition | **nothing** — capped by collisions | 65.58 % ceiling |

The pattern is consistent: **a small, well-chosen set of complementary places wins; adding more
sensors of the same place does not.** What no paper does is score a sensor *set* by how many
English words it keeps distinct.

## 4. Articulatory-feature tables

These let you code each phoneme by articulator instead of hand-writing a viseme map.

| Name | URL | Licence | Size | Format / contents |
|---|---|---|---|---|
| **PanPhon** (Mortensen et al. 2016) | https://github.com/dmort27/panphon | **MIT-Modern-Variant** (`license = {text = "MIT-Modern-Variant"}` in `pyproject.toml`) | wheel **78,888 B**; `panphon/data/ipa_all.csv` **356,894 B** | CSV, **24 feature columns**, **6,367 segments**; IPA segment → ±feature vectors |
| **PHOIBLE** (Moran & McCloy) | https://github.com/phoible/dev | **MIT** (repo licence; data described as CC-usable, verify before redistribution) | `data/phoible.csv` **26,455,818 B**; repo checkout **65,041 KB** | CSV; 3,000+ inventories, 2,100+ ISO 639-3 codes, distinctive-feature rows per segment |
| **IPA chart (2020 revision)** | https://www.internationalphoneticassociation.org/node/1061 | **CC BY-SA 4.0** — "As of July 2012, they are made freely available under a Creative Commons Attribution-Sharealike 4.0 International Deed" | chart PDF, a few hundred KB | human-readable chart: place × manner × voicing, vowel quadrilateral; not machine-readable |

PanPhon is the practical one: 349 KB of CSV, permissive licence, one row per IPA segment, and the
feature set includes exactly the articulators in question (labial, coronal, dorsal, high/low/back,
round, lateral, nasal, voice). PHOIBLE is the cross-linguistic check (does a feature contrast
exist in other languages) but is 26 MB and inventory-shaped, not English-shaped. The IPA chart is
a licence-safe reference image, not a data source.

## 5. Pronunciation dictionaries and word-frequency lists

| Name | URL | Licence | Size | What it contains |
|---|---|---|---|---|
| **CMUdict** | https://github.com/cmusphinx/cmudict | BSD-style: "Use of this dictionary for any research or commercial purpose is **completely unrestricted**" | `cmudict.dict` **3,618,488 B**, **84,162 entries** | ARPAbet phoneme strings per word, stress marks, alternate pronunciations |
| **wordfreq** 3.1.1 | https://github.com/rspeer/wordfreq | **Apache-2.0** | wheel **56,834,549 B** | per-word frequencies, 40+ languages, "snapshot of language usage through about 2021"; small and large lists |
| **SUBTLEX-US** | https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexus | **no explicit licence on the distribution page** — cite Brysbaert & New (2009), ask before redistributing | zipped xlsx/text; **74,286 words**, corpus **51 million words**, **282,170 letter strings** | subtitle-based word form frequency (WF) and contextual diversity (CD), per million words |
| **BEEP** (British English) | cited via Bear & Harvey 2017 | not free; distributed by Cambridge | not checked | British English pronunciations; used by the viseme papers, **not** a candidate for us |
| **Silent Speech EMG** (Gaddy et al.) | https://zenodo.org/records/4064409 | **CC-BY-4.0** | **3,919,507,637 B** (one `emg_data.tar.gz`) | "Facial electromyography recordings during both silent and vocalized speech"; 8 EMG + audio, force-aligned phonemes via MFA |

For the collision computation, CMUdict alone is enough: 3.6 MB, unrestricted, ARPAbet, already
the dictionary every US speech paper uses. wordfreq is the right second file if collisions must
be weighted by how often a word is actually said — which §1.1 shows changes the answer by 3×.

## 6. Existing code that counts "how many words collide after merging classes"

There is **no maintained tool** that takes a custom phoneme→class map and a dictionary and
returns the collision count. What exists is adjacent:

| Repo | Licence | Last activity | Custom class map? | Counts word collisions? |
|---|---|---|---|---|
| https://github.com/supernaiter/SilentSpeller | Apache-2.0 | pushed 2026-08-24, 19 stars | no (HMM letter models) | no — README: "repository is still under construction"; only one participant's dataset + formatting script released |
| https://github.com/OpenFaceFX/OpenFaceFX | MIT | pushed 2026-09-05 | yes, in effect — "deterministic phoneme→viseme→curve math" with a phoneme timeline | no — it animates; it does not measure ambiguity |
| https://github.com/ms-dot-k/Multi-head-Visual-Audio-Memory | **CC BY-NC 4.0** (non-commercial) | pushed 2024-03-09, 27 stars | no | no — it *disambiguates* homophenes with audio memory on LRW/LRS2 |
| https://github.com/dgaddy/silent_speech | MIT | pushed 2024-04-30 | no | no — EMG → speech/text |

A GitHub repository search for `homophene` returns **2 repositories total**, both of them the
lip-reading model above and a viseme-aware Swin transformer. Searching `viseme phoneme` returns
46, all of them animation or recognition pipelines. The published homophene analysis (Bear &
Harvey) is a *method described in a paper*, not released code: their definition is one line —
"we define a set of words to be homophenous if they all have the same viseme transcription in
whatever phoneme/viseme mapping we are using" — and re-implementing it is ~30 lines over CMUdict.

## 7. Verdict: does published work already answer the per-articulator question?

**No. Our own computation is needed, and it is small.**

What is published:

1. **Lips**: collision rates for several hand-made viseme maps (40–60 % claim; 10.83 % of types,
   34.42 % of tokens, 65.58 % ceiling).
2. **Single articulators**: how well a *set of flesh points* classifies phonemes/words — EMA
   6→4 (91–95 %), sEMG 8→4 (WER 22.9 %), EPG contact patterns per phoneme.
3. **Feature recoverability**: place +16.2, manner +13.3, nasality +4.8, voicing +2.8 points over
   context.

What is **not** published anywhere found: a table of "channel X reduces English word collisions
by Y %", i.e. the marginal value of tongue tip vs tongue sides vs tongue back vs jaw. Every study
stops at phoneme/word accuracy on a closed vocabulary, and none uses a dictionary-wide homophene
count as the metric. Bear & Harvey explicitly note the choice of map is unresolved ("the practical
reality is that many systems use visemes and there is need to resolve which choice of visemes
works best"), and their analysis is lips-only.

To compute it, exactly **two files** are needed:

| File | Size | Licence | Role |
|---|---|---|---|
| `cmudict.dict` (https://github.com/cmusphinx/cmudict) | **3,618,488 B** | unrestricted / BSD-style | 84,162 words → ARPAbet phoneme strings |
| `panphon/data/ipa_all.csv` (https://github.com/dmort27/panphon) — **optional** | **356,894 B** | MIT-Modern-Variant | build channel-partition maps from ±features instead of hand-writing them |

The code is a ~150-line stdlib script: load CMUdict, map each ARPAbet phone to a channel-partition
label, hash the mapped string per word, count colliding groups weighted by wordfreq (optional,
Apache-2.0, 56.8 MB wheel). No training, no GPU, no download beyond those files. It can run
entirely offline and its output is a table of the form *channel set → % word types colliding →
% tokens colliding*.

## What this means for the sensor layout

- **Lips alone cannot be the plan.** Under the Fisher map, 34.42 % of word tokens in a 979-word
  set are homophenous and the perfect-viseme ceiling is 65.58 %; a lip channel is necessary but
  capped before any sensor noise.
- **One non-lip place buys the most.** The widest classes are V3 (/t d s z θ ð/, six phonemes)
  and V5 (/k g n l ŋ h j/, seven). A channel that separates within V5 — velar vs nasal vs
  lateral — breaks a 7-way ambiguity for the price of one place.
- **Tongue tip and tongue back are the two EMA points that survive ablation.** The 4-sensor set
  T1 (tip/blade) + T4 (back) + upper lip + lower lip keeps "91%–95%", "equivalent to that using
  all 6 sensors"; front tongue-body sensors T2/T3 are redundant.
- **Tongue sides are the least redundant and least understood channel.** Lateral bracing is
  required for /t d n s z/ and the groove for /s z ʃ ʒ/, and clinicians are documented as poor at
  lateral margins; nothing in the literature scores side contact for word distinctness.
- **Jaw is a lip/larynx proxy, not a place channel.** Electrodes 2 and 6 carry lower lip and jaw
  and the 4-electrode sEMG set reaches WER 22.9 % vs 15.5 % for all 8 — jaw adds mouth opening,
  not place.
- **Do not expect sEMG to deliver tongue back.** "Stronger association in the lips compared to
  the tongue"; the best tongue electrode reaches tongue tip only, and 2 electrodes cost WER 46.9 %.
- **Voicing needs its own channel or the LM.** Voicing accuracy is 88.1 % with only +2.8 over
  phoneme context, and the paralaryngeal electrode gives pitch r = 0.32 — a voicing contrast
  (/p/ vs /b/) is a language-model decision unless a laryngeal sensor is added.
- **/h/, /p/, /f/ are invisible to a contact channel** (the EPG "no contact" set). Either accept
  context recovery, or use a distance/optical measure (EOS: 97 % user-dependent) instead of
  binary contact.
- **Sparsity is fine.** SilentSpeller reduced 124 electrodes to 16 principal components at 100 Hz
  and still got 97 % character accuracy; the channel count that matters is the number of
  *distinct places*, not electrodes.
- **The layout decision can be made offline for ~4 MB of downloads.** CMUdict (3.6 MB,
  unrestricted) plus a channel map answers "which set of places minimises collisions" before any
  hardware is built.

## Open questions

1. Which viseme/class map corresponds to a *sensor* channel rather than to lips? Fisher's map is
   a lip map; no published map is parameterised by articulator, which is exactly the gap.
2. Does the type/token ratio (10.83 % vs 34.42 %) hold for CMUdict-sized vocabularies, or is it
   an artefact of a 979-word recording set? Cheap to check with CMUdict + wordfreq.
3. Are vowels worth a channel? Fisher merges six vowels in V7 and three in V9/V10, but EPG vowel
   contact is variable and was not quantified in the sources opened here.
4. What is the real cross-user penalty of a sparse layout? EOS drops 97 % → 56 % user-independent;
   no equivalent number exists for a 4-place layout.
5. SilentSpeller's per-letter confusion matrix (B/P, D/T/Z) is shown as palatograms but not
   published as numbers — the exact letter-pair collision rate is unknown.
6. Is there a licence-clean British-English pronunciation dictionary? BEEP is not free, and the
   viseme papers all use it, so their exact numbers cannot be reproduced without it.

## Sources

1. Bear, H. L., & Harvey, R. W. (2016). *Visual units and confusion modelling for automatic
   lip-reading.* Image and Vision Computing. PDF: http://www2.cmp.uea.ac.uk/~sjc/Image-and-vision-computing-2015.pdf
2. Bear, H. L., & Harvey, R. W. (2017). *Phoneme-to-viseme mappings: the good, the bad, and the
   ugly.* Speech Communication. https://arxiv.org/abs/1805.02934
3. Wang, J., Samal, A., Rong, P., & Green, J. R. (2016). *An Optimal Set of Flesh Points on Tongue
   and Lips for Speech-Movement Classification.* JSLHR 59(1):15–26. https://pubmed.ncbi.nlm.nih.gov/26564030/
4. Lee, J., Huang, K., Avramidis, K., Pistrosch, S., Gonzalez-Machorro, M., Lee, Y., Schuller, B.,
   Goldstein, L., & Narayanan, S. (2025). *Articulatory Feature Prediction from Surface EMG during
   Speech Production.* Interspeech 2025. https://arxiv.org/abs/2505.13814
5. Kimura, N., Gemicioglu, T., Womack, J., Zhao, Y., Bedri, A., Li, R., Su, A., Olwal, A.,
   Rekimoto, J., & Starner, T. (2022). *SilentSpeller: Towards mobile, hands-free, silent speech
   text entry using electropalatography.* CHI 2022. https://tangemicioglu.com/files/papers/SilentSpeller_CHI_2022.pdf
6. McLeod, S. (2011). *Speech-language pathologists' knowledge of tongue/palate contact for
   consonants.* Clinical Linguistics & Phonetics 25(11–12):1004–1013. https://pubmed.ncbi.nlm.nih.gov/22106891/
7. Sung, K., & Kochetov, A. (2018). *Allophonic variation in English coronal stops: An EPG corpus
   study.* Toronto Working Papers in Linguistics 40.
   https://twpl.library.utoronto.ca/index.php/twpl/article/download/29221/21935
8. Kim, M., Yeo, J. H., & Ro, Y. M. (2022). *Distinguishing Homophenes Using Multi-Head
   Visual-Audio Memory for Lip Reading.* AAAI 2022. https://ojs.aaai.org/index.php/AAAI/article/download/20003/19762
9. Stone, S., & Birkholz, P. (2020). *Articulation-to-speech using electro-optical stomatography
   and articulatory synthesis.* ISSP 2020. https://issp2020.yale.edu/S05/stone_05_02_016_abstract.pdf
10. Fisher, C. G. (1968). *Confusions among visually perceived consonants.* JSHR 11(4):796–804.
    https://pubs.asha.org/doi/abs/10.1044/jshr.1104.796 (abstract page only — paywalled)
11. Gaddy, D., & Klein, D. (2021). *An Improved Model for Voicing Silent Speech.* ACL-IJCNLP 2021.
    https://aclanthology.org/2021.acl-short.23/
12. Mortensen, D. R., Littell, P., Bharadwaj, A., Goyal, K., Dyer, C., & Levin, L. (2016).
    *PanPhon: A Resource for Mapping IPA Segments to Articulatory Feature Vectors.* COLING 2016.
    https://github.com/dmort27/panphon
13. Moran, S., & McCloy, D. (eds.). *PHOIBLE.* https://github.com/phoible/dev
14. *CMUdict (Carnegie Mellon Pronouncing Dictionary).* https://github.com/cmusphinx/cmudict
15. Speer, R. *wordfreq.* https://github.com/rspeer/wordfreq
16. Brysbaert, M., & New, B. (2009). *Moving beyond Kučera and Francis …* Behavior Research
    Methods 41:977–990. Distribution: https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexus
17. Gaddy, D., et al. *Silent Speech EMG* dataset (2020). https://zenodo.org/records/4064409
18. International Phonetic Association. *The IPA Chart* (2020 revision).
    https://www.internationalphoneticassociation.org/node/1061
19. *SilentSpeller* code repository. https://github.com/supernaiter/SilentSpeller
20. *OpenFaceFX* lip-sync pipeline. https://github.com/OpenFaceFX/OpenFaceFX
21. *Multi-head Visual-Audio Memory* code repository. https://github.com/ms-dot-k/Multi-head-Visual-Audio-Memory
22. *Voicing Silent Speech* (dgaddy/silent_speech) code repository. https://github.com/dgaddy/silent_speech
