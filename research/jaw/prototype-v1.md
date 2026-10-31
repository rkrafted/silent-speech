# Hidden jaw-integrated silent-speech prototype — v1 design

This is the design that turns the three research sweeps (Baltic, patents, PubMed site evidence)
into one buildable thing: a surface-EMG silent-speech device whose electrodes are **not on the
front of the face**. It answers five questions: which shape hides the electrodes, what to buy,
what already failed, how to measure the hidden-set cost during the borrowed-EMG week, and the
week-by-week route to a first wearable by 2026-12-31.

Status: v1, written 2026-10-06. Nothing here has been built yet; every accuracy number is
quoted from a source, not measured on our device.

## How to read the citations

- `[pubmed-<PMID>]` — a paper in `sources-pubmed.jsonl`, keyed by its PubMed id.
- `[baltic-<PMID>]` — a paper in `sources-baltic.jsonl`; `[baltic-<row>]` — a non-paper row
  (lab page, tender, device page) by its 1-based line number.
- `[patents-<number>]` — a patent in `sources-patents.jsonl`, keyed by the numeric part of the
  patent number in its title (e.g. `[patents-10621973]` = US10621973B1).
- `[research/NN §x]` — a section of the repo's own earlier track notes under `research/`.

Companion machine-readable lists: `research/jaw/sources-baltic.jsonl`,
`research/jaw/sources-patents.jsonl`, `research/jaw/sources-pubmed.jsonl`.

## Reuse check (repo finder + local tools first)

The repo finder (`prior_art check`) returned only weak, unrelated textual hits for this idea
(a speech-wearable repo, "factors"/"jaw" keyword matches); no reusable hidden-jaw design exists
in public code. The reusable assets are local and are used directly:

- `silent-speech-ml` — the recording prompter (`tools/prompter.py`), external-import
  (`tools/import_external.py`), whole-model fine-tune curve (`scripts/finetune_curve.py`) and the
  decoder (`scripts/decode_full.py`, `scripts/eval_repro.py`). Section 4 drives all of these.
- `research/04` §3 and §5 — the concealed-layout survey (Layouts A–D) this document narrows to one.
- `research/jaw/site-evidence.md` — the site ranking and the paired 16-channel experiment.

Gaddy's montage is the anchor for all of it: 8 monopolar channels, gold electrodes + Ten20 paste,
shared reference behind one ear, bias behind the other [research/04 §1.2]. The eight sites are
1 left cheek above mouth, 2 left chin corner, 3 below chin back 3 cm, 4 throat 3 cm left of the
Adam's apple, 5 mid-jaw right, 6 right cheek below mouth, 7 right cheek 2 cm from nose, 8 back of
right cheek 4 cm in front of the ear.

---

## 1. Three form factors that hide the electrodes

The hidden/visible split comes from `site-evidence.md` §3–4. One line to keep in mind throughout:
the **visible cheek and mid-jaw channels are the cheap ones to drop**, and the **hidden
under-chin (site 3) and throat (site 4) channels are two of the most valuable** [pubmed-33181497]
[pubmed-29552581] [pubmed-19304494]. The one genuinely expensive loss is Gaddy site 2, the front
of the chin, which the same re-analysis ranks second-most important [research/04 §1.2].

### Option A — Behind-ear pod with a jaw-line arm (and a short neck stem) — "the ear hook"

- **Sites covered.** Retroauricular/mastoid pod (site 8's neighbourhood, plus the reference/bias
  sites both AlterEgo and Gaddy already put behind the ears); a thin arm under the mandible from
  the jaw angle forward to the submental floor (sites 3 and 2's territory: mylohyoid, anterior
  digastric, geniohyoid); optional short stem to the superior ventral neck (site 4). This is the
  concrete hybrid already written up in `research/08` §7: a BTE/RIC pod + a thin flex strip behind
  the jaw angle to 1–2 submental sites [research/08 §7].
- **Gaddy sites lost.** 1, 5, 6, 7 (visible cheeks and mid-jaw); site 2 only if the arm does not
  reach the front of the chin; site 4 unless the neck stem is fitted. Sites 3 and 8 and both ear
  references stay [pubmed-19304494].
- **Expected accuracy cost.** Hidden-only on a **closed command set** roughly **+3 to +6 WER
  points**: Meltzner lost only 3.3 points going 8 sensors → 4 [pubmed-29552581], and the 2026
  laryngectomy study kept 95% of a 20-channel signal with ~9 electrodes [pubmed-42694022]. On
  **open vocabulary** the cost is larger, **+8 to +15 points**, because Gaddy's best 4-electrode
  models were 45–54% WER, 9–18 points worse than all 8 electrodes in the same dissertation (the 68.0% figure is a different, audio-based metric), as the sweep reports it [site-evidence §5]
[research/04 §1.2]. A behind-ear single magnetic
  sensor alone reached 87.3% on a same-viseme word list [pubmed-37751158].
- **Comfort.** The pod is a 9–17 g behind-the-ear object, the weight class of a bone-conduction
  hearing aid [research/08 §6]. The arm moves with the jaw, so it must be sprung or soft; contact
  pressure should be the least that holds the pads (capillary-closure pressure at the mastoid is
  ~3.7 kPa and hearing-aid headbands measured 11–17 kPa) [research/03 §10]. No adhesive if the
  arm is sprung; dry pads can run for hours [research/04 §4.6].
- **How visible.** Pod: normal-hearing-aid visible, hidden by hair. Arm: a thin skin-toned strip
  along the jaw line, visible in profile, invisible from the front. Nothing on the mouth or cheeks.
- **Key parts.** One ADS1299 (8 ch, TQFP-64, 10×10 mm) or an Intan RHD headstage; nRF5340; 150 mAh
  LiPo; Formlabs BioMed Clear shell; dry/textile pads or an e-tattoo strip on the arm.

### Option B — Headphone or earbud + a submental strip

- **Sites covered.** Around-ear ring or earmuff electrodes (retroauricular/mastoid and the jaw
  musculature that leaks to the ear: masseter) plus 2 submental channels under the chin. This is
  the two-piece hybrid of `research/04` Layout A/C: headphone-earmuff textile EMG reached **96% on
  10 silent words** with 4 channels [research/04 §3.1], and bilateral around-ear cEEGrid arrays
  (AESSI) reached **92.24% cross-day on a fixed 25-sentence set**, 98.00% online after ≥21 days
  [research/04 §3.1]. Pure ear-EEG is much weaker: around-ear **56.6%** on 64 words and **−16 to
  −22 points** versus scalp [pubmed-41855656] [pubmed-41286316].
- **Gaddy sites lost.** 1, 2, 5, 6, 7, and 3 unless the strip actually reaches the submental
  floor. Ear channels do not see the tongue, lips or the digastric complex well [research/08 §7].
- **Expected accuracy cost.** Best-in-class for **closed commands** (96% / 92% cited above);
  poor for **open vocabulary** — a 64-word closed set is the current ceiling for around-ear
  [research/08 §8.1]. Versus the full face set, expect the hidden-only +3 to +6 closed / +8 to +15
  open gap plus the ear-EEG penalty on anything only the ear can see.
- **Comfort.** A headphone is an object the owner already wears — no adhesive on the face. The
  submental strip does need adhesive or a chin strap and can pull on jaw motion.
- **How visible.** The headphone is normal. The strip is hidden under the chin unless the head
  tips back. Best concealment of the three if the strip can be dropped.
- **Key parts.** Graphene/PEDOT:PSS textile pads in the earmuff, or a cEEGrid-style flex array
  (gel + fresh adhesive per session); 2-electrode submental flex strip; same ADS1299 pod; ESP32-S3
  for the headphone build.

### Option C — Collar / neckband

- **Sites covered.** 14 differential dry channels around the neck (SilentWear layout) or a smaller
  necklace montage; the superior ventral neck/larynx area (site 4) is strongly covered, the
  submental complex (site 3) only partially, and the ear reference moves to an earhook.
- **Gaddy sites lost.** 1, 2, 5, 6, 7, 8; site 3 is partly lost because a band below the jaw
  cannot reliably reach the floor of the mouth — the worst channel to lose [site-evidence §4].
- **Expected accuracy cost.** Silent within-session **77.5 ± 6.6%**, leave-one-session-out
  **59.3 ± 2.2%** after re-donning [research/04 §3.4]; voiced 11-word necklace 92.7% [research/04
  §3.4]. Zhu's optimiser independently put most of its 10 selected electrodes on the neck
  [pubmed-33181497]. Versus the full face set this is the largest cross-session drop of the three.
- **Comfort.** No adhesive, no face contact; hidden by a collar, scarf or hoodie. Skin prep is
  minimal.
- **How visible.** Hidden by clothing — but that makes it wardrobe-dependent (no collar in
  summer, formal shirts, sportswear) and it is the least "barely different from normal" in a
  T-shirt.
- **Key parts.** Textile neckband, soft dry electrodes (Datwyler SoftPulse-class or a conductive
  textile), two ADS1298/ADS1299 AFEs, nRF53 BLE; 20.5 mW total for >27 h [research/04 §3.4].

### The pick: **Option A**, the behind-ear pod with a jaw-line arm

1. It is the only shape that keeps **both** best-evidenced hidden signals — submental/complex
   (site 3) and laryngeal/neck (site 4) — while also putting the reference and bias where the
   anatomy already wants them [site-evidence §3] [pubmed-19304494].
2. It has the best **accuracy-per-visibility** for silent EMG: a skin-toned jaw strip plus a
   hearing-aid pod reads as a hearing aid, not as face electrodes, and the submental patch alone
   reached 80.9% on 5 silent words (89.6–92.7% for a 3-channel patch) [research/04 §3.2].
3. It leaves the mouth free for the minimal real articulation the decoder needs, and it is the
   one constrained layout that can carry an optional invisible second modality — an in-ear
   deformation sensor (91.7% TMJ classification) or a behind-ear contact mic [pubmed-42394395]
   [research/08 §8.1].
4. It has a **patent route around** the closest claims: the Vocasso claim is the specific
   chin + neck + behind-ear EMG + chin-IMU triad [patents-10621973], and Wispr's ear-hook claim
   pairs a preauricular downstem with a postauricular reference [patents-12482449]. A pod with a
   submental arm, no chin IMU and a mastoid (not postauricular-downstem) reference is a different
   combination — this is a design observation, not a legal opinion.

Plan: build Option A first. Keep Option B's headphone-cushion pads as the no-adhesive daily mode
and Option C's neckband as the fallback if the jaw strip will not stay put.

---

## 2. Bill of materials

Prices are the ones actually observed in the research; anything the research could not confirm is
marked **unverified** and should be re-checked in an EU logged-in browser before ordering. EU
listings from outside the EU add roughly import VAT and duty (OpenBCI states ~+25% for the EU
[research/10 §A.2]).

### Stage 0 — the borrowed-EMG week (near zero cost)

| Item | Part | Qty | Price | Where |
|---|---|---|---|---|
| Gel electrodes | Kendall H124SG (Medtronic/Covidien) Ag/AgCl | ~100 | ~€0.22 each [CALL-PREP] | EU medical distributors (Mediq, HOSPIMED-class) |
| Conductive paste | Ten20 (Weaver) | 1 | ~€10–15 (**unverified**) | EU medical/online |
| Skin prep | alcohol wipes, medical tape, gauze | — | ~€10 | pharmacy |
| **Stage-0 total** | | | **≈€35–50** | |

The lab's own amplifier is the sensor; we supply electrodes and the recording software. If the lab
is RSU/LASE, confirm whether the BTS FREE-EMG is **8 or 16 channels** — the public equipment list
says 8, and BTS FREE-EMG is 16 ch / 1 kHz / 13 g wireless sensors [baltic-39] [baltic-38]. If the
lab is Turiba, the borrowed OpenBCI Cyton+Daisy is 16 channels but **Daisy degrades to ~125 Hz**,
so it is an electrode/cable source and a pilot host, not the main recorder [baltic-29] [baltic-33]
[research/10 §A.2].

### Stage 1 — cheapest working bench recorder (own hardware)

| Item | Part number / name | Qty | Price | EU source |
|---|---|---|---|---|
| Main board | **PiEEG-16** (2× ADS1299, 16 ch, 250 SPS–16 kSPS, MIT) | 1 | **$390** [research/10 §A.3] | pieeg.com; Elecrow (ships EU) |
| Host | **Raspberry Pi 5 4 GB** (SC1111) | 1 | ~€60–80 | Botland (PL), BerryBase (DE), Kubii (FR) |
| Power | USB power bank 5 V/2 A, ≥10 000 mAh | 1 | ~€20 | any EU retailer |
| **EU-vendor alternative** | **Cerelog ESP-EEG** (8-ch ADS1299 + ESP32, 250 SPS default) | 1 | **$389.99** [research/10 §A.4] | Cerelog, Spain (EU) |
| **Single-channel trial** | **MyoWare 2.0** DEV-18977 | 1 | **$42.95** [research/03 §8] | SparkFun; Mouser/Farnell EU |
| **Stage-1 total** | | | **≈€420–520** | |

Do **not** buy an OpenBCI Cyton for this: over Bluetooth it is fixed at 250 Hz, Cyton+Daisy to the
PC degrades toward 125 Hz, and used units sell near the new price ($1,249 / $2,499) [research/10
§A.2]. PiEEG-16 has the same ADS1299 silicon as the AlterEgo/Gaddy chain at a quarter of the
price. Battery-only while worn — never a wall adapter [research/03 §9].

### Stage 2 — wearable v1 (the behind-ear pod + jaw arm)

| Item | Part number / name | Qty | Price | Notes / source |
|---|---|---|---|---|
| AFE | **ADS1299IPAG** (TI, TQFP-64), or ADS1298IPAG | 1–2 | **unverified** (TI store out of stock) [research/03 §11b] | 8 ch each; 2 gives 16 |
| MCU + BLE | **nRF5340** (dev: nRF5340-DK) | 1 | ~€6–12 (**unverified**) [research/03 §11b] | 2 Mbps PHY |
| Power mgmt | MCP73831 charger + TPS62840 buck + TPS7A02 LDO + MAX17048 gauge | 1 set | ~€5–8 (**unverified**) [research/03 §11b] | |
| Battery | 150 mAh LiPo | 1 | ~€6 (**unverified**) [research/03 §11b] | 27 h at 20.5 mW |
| Audio out (optional) | MAX98357A breakout + Adafruit 1674 / C2049 8 Ω bone-conduction shaker | 1 each | **$5.95 + $8.95** [research/03 §10, §11a] | bench audio only |
| Shell | **Formlabs BioMed Clear** resin (ISO 10993-5/-10/-23, USP VI) | 1 cartridge | quote | Formlabs EU / 3D Jake |
| Dry pads | Datwyler SoftPulse-class dry electrodes, or OpenBCI/IDUN Dryode Alpha Kit | 4–10 | **$224.99–$244.99** kit [research/09 §3.2] | Dryode was out of stock 2026-10-01 |
| **Stage-2 total** | | | **≈€150–400 + NRE** | custom board, excl. PCB assembly (~€100–300) |

### Stage 3 — hidden electrodes and the e-tattoo arm (optional, later)

| Item | Part number / name | Qty | Price | Source |
|---|---|---|---|---|
| Tattoo substrate | **Silhouette Temporary Tattoo Paper** 8.5×11 in (2 sheets) | 1 | **$9.99** | [research/09 §3.1] (3D Jake CH: CHF 10.05) |
| Thin PET | PolyK Technologies 1.4 µm PET | 1 sheet | unverified | Route A [research/09 §2.1] |
| Au/PET film | Rotex Tech 13 µm Au/PET (connector strips) | 1 | unverified | [research/09 §2.1] |
| Conductive ink | Heraeus **Clevios P Jet 700** PEDOT:PSS | small | unverified | Route C [research/09 §2.3] |
| Silver ink | **Sicrys 130EG-1** Ag, on 50 µm Kapton | small | unverified | Route C2 [research/09 §2.3b] |
| Interconnect | Kapton tab into a **ZIF socket** or magnetic pogo dock, **behind the ear** | 1 | ~€5 | [research/09 §2.2] |

Fabrication routes, cheapest first: (A) cut-and-paste Au/Cr on 1.4 µm PET over tattoo paper with a
Silhouette Cameo plotter plus one thermal-evaporator run at a makerspace; (B) screen-printed carbon
+ plasma-polymerised PEDOT with a ZIF interconnect; (C) inkjet PEDOT:PSS. Route A is the stated
first build [research/09 §2.1]; the only non-household tool is the evaporator [research/09 §2.1].

### 3D-print files to adapt

There is **no open behind-ear silent-speech shell** to download. The files that exist and are
worth adapting: AlterEgo's published form factor is a 3D-printed photopolymer-resin band with
brass structural rods and face extensions [research/04 §1.1]; OpenBCI publishes KiCad/gerber design
files for its boards [research/03 §8]; and the BTE/RIC split (electronics in the behind-ear case,
only electrodes into the canal/jaw) is the realistic host for a stock-package ADS1299 (12×12 mm)
[research/08 §6]. Concretely: model the pod around the ADS1299 + nRF5340 + 150 mAh cell, print in
BioMed Clear, and treat the jaw arm as a separate sprung flex/PLA piece so the pod does not move
when the jaw opens.

---

## 3. What others tried and dropped — and how we avoid it

The patents sweep is a list of dead ends; the papers add the physiological ones.

| Dead end | Who tried it | Status / evidence | How v1 avoids it |
|---|---|---|---|
| Injecting excitation into the vocal tract | Tosaya/Sliwa [patents-7082395] | **EXPIRED** 2021, never a product | No output transducer in the sensing path |
| Magnetic tracer on the tongue + mouth sensor array | Georgia Tech [patents-8242880] [patents-9911358] | Both **INACTIVE**; needs an intraoral tracer | No intraoral parts |
| sEMG fused with a lip camera | Tianjin [patents-113887339]; defence lab [patents-111899713] | Both **DISCONTINUED**; occlusion + privacy | Pure sEMG, no line-of-sight sensor |
| Adding vocal-cord vibration to facial EMG | Tianjin [patents-111723717] | **DISCONTINUED** | One modality, hidden sites only |
| Oral-cavity ultrasound probe | Defence lab [patents-111899713] | **DISCONTINUED**; cannot be hidden, uncomfortable | No intraoral probe |
| Kitchen-sink multimodal fusion (EEG+EMG+lip+eye) | Defence lab [patents-111190484] | Claim ACTIVE but heavy; siblings discontinued | Deliberately one modality + one hidden non-EMG gate |
| Optical facial-micromovement decoding | Q (Cue) [patents-12154572] | ACTIVE, Apple-acquired; camera/lighting dependent | Electrodes, not optics |
| In-ear microphone command input | Qualcomm [patents-10678502] | ACTIVE, but acoustic — not silent | In-ear sensor is deformation only, not audio |
| Cross-user generic EMG model, no calibration | Meta/CTRL-labs [patents-11216069] | Claims need a trained model but still per-user data | Per-user fine-tune is the plan (curve, §4) |
| Extra modalities generally | USTC/discontinued siblings | Pure sEMG is the lean surviving route | Keep channel count small |
| **Pure inner speech** | Meltzner 2008 (cited in [research/04 §Key takeaways 8]) | "Recognition impossible" from mentally rehearsed speech | Train **minimal but real articulation**, lips closed |
| Wet gel as a daily electrode | [research/04 §Key takeaways 4] | Gel dries in ~1 h, Ag/AgCl signal gone by ~3 h | Dry/textile for wear, gel only for the borrowed-week recording |
| 2–4 channels for open speech | Gaddy/Meltzner ablations [research/04 §Key takeaways 2] | 9–18 WER points worse than a full montage | 7–14 ch for open vocab; 2–4 only for commands |

Two more things the sweeps teach us to copy rather than fight:

- **Train dense, deploy sparse.** USTC's granted CN113288183B builds a source network from a
  high-density sEMG set and a target network from a channel-sparse set, then transfers
  [patents-113288183]. That is exactly the §4 plan: record 16 channels, deploy the winning 4–6.
- **Transformer/LLM decoder, not a bigger sensor.** CN114863912A claims a Transformer decoder for
  silent sEMG [patents-114863912], and LLM rescoring is already the biggest lever on our own
  numbers (`silent-speech-ml` decode item). This is software, so it does not raise the visible
  electrode count.

Watch-out claims to read before any filing (not legal advice): Wispr US12482449B2 (wearable
speech-muscle activation, incl. EMG) [patents-12482449]; Cornell US12505842B2 (cutaneous
articulatory sEMG for silent speech) [patents-12505842]; Vocasso US10621973B1 (chin + neck +
behind-ear EMG + chin IMU) [patents-10621973]; Biosensic/Schultz US8082149B2 and its 45-member
family [patents-8082149]; and Apple US11683632B2 / Bose CN110996782B for any in-ear part
[patents-11683632] [patents-110996782].

---

## 4. Borrowed-EMG week plan

Goal: **one speaker, one electrode map, one session set** that records Gaddy's 8 sites and the
hidden candidates **at the same time**, so every channel subset is scored on the *same* signals.
The paired design is what removes session and skin as confounders (`site-evidence.md` §5).

### 4.1 The 16-channel electrode map

Monopolar interpretation (Gaddy-style shared reference + bias), 16 electrodes:

| Ch | Site | Tag | Role |
|---|---|---|---|
| 1 | left cheek just above mouth | VISIBLE | Gaddy 1 |
| 2 | left corner of chin | VISIBLE | Gaddy 2 (top-2) |
| 3 | below chin, back 3 cm | HIDDEN | Gaddy 3 (top-2, submental complex) |
| 4 | throat, 3 cm left of Adam's apple | HIDDEN | Gaddy 4 (paralaryngeal) |
| 5 | mid-jaw right | VISIBLE | Gaddy 5 |
| 6 | right cheek just below mouth | VISIBLE | Gaddy 6 |
| 7 | right cheek 2 cm from nose | VISIBLE | Gaddy 7 |
| 8 | back of right cheek, 4 cm in front of ear | SEMI | Gaddy 8 (jaw hinge) |
| 9 | second submental, paramedian right | HIDDEN | anterior digastric/mylohyoid |
| 10 | second paralaryngeal, right of Adam's apple | HIDDEN | superior ventral neck |
| 11 | lateral neck below the collar line | HIDDEN | sternohyoid/SCM edge |
| 12 | posterior digastric, under the mandible between jaw angle and chin | HIDDEN | jaw-line arm |
| 13 | mastoid/retroauricular behind the right ear | HIDDEN | the pod's home site |
| 14 | masseter over the jaw angle (or in-ear deformation placeholder) | HIDDEN | ear-region / second modality |
| 15 | REF below left ear | HIDDEN | Gaddy reference |
| 16 | BIAS below right ear | HIDDEN | Gaddy bias |

If the borrowed rig is the **BTS FREE-EMG** (16 bipolar channels, 13 g sensors [baltic-39]), each
sensor is a two-pad bipolar pair: place channels 1–14 at the sites above with the second pad ~2 cm
along the muscle, channel 15 as a cross-ear mastoid pair, channel 16 as the in-ear deformation
sensor or a spare. Log for every channel: wet gel vs dry, exact distance from the landmark, and
which muscle it overlies. Record a **hard clench at the start of every block** for sync [CALL-PREP
must-get 3]. If the rig is only **8 channels**, split into two sessions (Gaddy set first, hidden
set second) and accept that the comparison is unpaired; schedule a third short session to repeat
the hidden set after re-donning.

### 4.2 Session schedule

| Day | Time | What | Output |
|---|---|---|---|
| −1 | 1 h | Write the raw-format converter from the lab's 1-minute sample; dry-run `tools/prompter.py --dry-run` | converter + prompt JSONL |
| 1 | 6 h | Block 1 setup + baseline (30); block 2 Harvard voiced **and** silent (90); block 3 ARCTIC prose (45); block 4 minimal pairs p/b t/d k/g m/b (45); block 5 real commands + 4 wheel choices (60); block 6 re-record errors (45); block 7 held-out calibration (30) | raw day-1 + `prompter.jsonl` |
| 2 | 2 h, ≥48 h later | Re-don the **same** map; repeat the 67-word closed set and the held-out set only | re-donning delta |
| 3 | 1 h (optional) | In-ear deformation sensor + mastoid contact-mic side test; unlock-gesture (double clench) test | second-modality go/no-go |
| 4 | — | Import + fine-tune + subset scoring | the WER-per-subset table |

Break 5 minutes every 30; skin and focus give out after ~3–4 h [CALL-PREP]. The
prompter already emits a CLENCH NOW marker at each block start and logs wall-clock timestamps, so
alignment is post-hoc from `--start-ms` (`silent-speech-ml/docs/READY.md` §1–2).

### 4.3 The analysis that scores WER per subset with our own pipeline

All code already exists in `silent-speech-ml`; nothing new is trained from scratch.

1. Import each day/condition:
   `python3 tools/import_external.py --input raw/day1.csv --format auto --jsonl .../prompter.jsonl --out data/owner_recordings --session day1 --condition silent --src-rate 1000 --start-ms <epoch-ms>`
   (`silent-speech-ml/docs/READY.md` §4).
2. Fine-tune the whole released checkpoint and get the minutes-vs-WER curve:
   `python3 scripts/finetune_curve.py --condition <imported session> --minutes 5,10,15,20,30,60`
   On the public closed session this curve is **1.3913 WER at 0 min → 0.3986 at 5 → 0.1884 at 10
   → 0.0797 at 15 → 0.0870 at 20 min** (same speaker, word-LM beam)
   (`silent-speech-ml/state/finetune_curve.json`; `DONE.md` §2). That is why 15–20 minutes of the
   owner's own recording is the target, not hours.
3. Score every subset with the same decoder — word-LM prefix beam (`scripts/decode_full.py`) plus
   greedy (`scripts/eval_repro.py`) and the grammar trie:
   - (a) all 16 channels; (b) Gaddy 8; (c) hidden-only {3, 4, 8, refs, 9, 10, 11, 12, 13};
   - (d) leave-one-channel-out for all 16; (e) visible-only {1, 2, 5, 6, 7};
   - (f) the proposed 4-channel wearable set {3, 4, 9, 13}.
   Subsets are channel masks over the same imported session — no re-recording.
4. Report the WER gap (a→c) and the per-channel importance order, then compare it with Gaddy's
   order {2, 3, 1, 7, 4, 6, 8, 5} and Hwang's re-analysis {3, 2, 7, 1, 5, 4, 8, 6}
   [site-evidence §4].

### 4.4 The decision rule (fixed before recording, so the result cannot be argued away)

- Hidden-only gap on the **closed** set **≤5 WER points** → build the hidden montage, spend the
  data budget on per-user fine-tuning [site-evidence §5].
- Gap **≥10 points** → re-include the front-of-chin channel (site 2) with a skin-tone-matched
  e-tattoo, and make the ear/earbud sensor the primary concealment play [site-evidence §5].
- Between 5 and 10 → keep the site-2 e-tattoo as a removable add-on and re-measure on the second
  day.
- If an in-ear deformation sensor adds nothing over channel 3 → drop it from the v1 wearable
  [site-evidence §6].

A short "Electrode plan" section is appended to `CALL-PREP.md` pointing at this section.

---

## 5. Fastest path to a first wearable (week by week to 2026-12-31)

Today is 2026-10-06; the deadline is ~12.5 weeks away. One owner and one hired EE.

| Week | Dates | Steps | Gate |
|---|---|---|---|
| 1 | Oct 6–12 | Fix the borrowed-rig date (RSU/LASE BTS or Turiba); order PiEEG-16 + Pi 5; write the converter; prompter dry run | raw sample file in hand |
| 2 | Oct 13–19 | Recording week (§4.2): day 1 (6 h), day 2 re-don, optional day 3 ear test | day-1 raw imported |
| 3 | Oct 20–26 | Import + fine-tune + subset scoring (§4.3); freeze the hidden set and channel mask | WER-per-subset table + decision §4.4 |
| 4 | Oct 27–Nov 2 | CAD the pod + jaw arm; print v0 in BioMed Clear; mount dry pads; bench-test on PiEEG | pod fits, all channels alive |
| 5 | Nov 3–9 | Wearable v0 on a power bank; 3× don/doff; measure cross-session WER | re-donning within the §4.4 budget |
| 6 | Nov 10–16 | 30 min/day closed-vocab recording; per-user fine-tune; grow to ~200 phrases | closed-vocab WER at the `silent-speech-ml` level |
| 7 | Nov 17–23 | Reliability layer: double-clench unlock + null class + confidence gate; constrained LLM corrector (3090/Ollama or phone) | no transcription without the unlock |
| 8 | Nov 24–30 | PCB v1 schematic (2× ADS1299 + nRF5340), EDI or hired-EE review, order fab | design review signed off |
| 9 | Dec 1–7 | Android app + BLE; on-phone TFLite/ONNX decoder prototype | phone receives EMG and types text |
| 10 | Dec 8–14 | Assemble PCB; integrate into the pod; measure SNR, runtime, comfort | ≥6 h on battery, no dropout |
| 11 | Dec 15–21 | End-to-end demo: silent command → text + TTS; fix the top 3 failures | demo runs 3 days in a row |
| 12 | Dec 22–31 | Freeze v1, document, DONE; buffer for slips | tagged v1 |

Fallbacks, pre-decided: 8-channel rig → two sessions; jaw strip will not hold → headphone-cushion
mode from Option B; PCB slips → the PiEEG + Pi 5 in a pouch is the v1 "wearable"; e-tattoo slips →
dry Ag/AgCl on the jaw arm; ear-only doesn't beat chance on tongue/lip tasks → the jaw strip is
mandatory, not optional.

## 6. Risks and open questions

- **Site 2 (front of chin) is the expensive loss** [site-evidence §3–4]. The whole hidden-only bet
  is that the submental complex (site 3) plus the jaw arm carries enough of it.
- **Subvocalisation is not free**: intrinsic laryngeal activity during subvocalisation was small
  and idiosyncratic (only the right cricothyroid reached significance) [pubmed-33612369]. The
  protocol must be minimal real articulation [research/04 §Key takeaways 8].
- **Wet vs dry is under-reported** in the high-accuracy studies, and the materials evidence is
  mostly limb, not face [site-evidence §6].
- **Wear duration and re-application** are the neckband's known failure and the mouth/chin is
  worse; the e-tattoo arm is the mitigation but only 48–52 h is quantified
  [research/04 §Key takeaways 5].
- **Freedom to operate is unresolved** — the sweeps found active claims close to an ear-hook EMG
  wearable [patents-12482449] [patents-12505842] [patents-10621973]; this document is not legal
  advice.
