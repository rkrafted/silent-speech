# Intraoral silent-speech appliance — confidential prior-art check (patents and papers)

Scope: patents and papers on an in-mouth appliance that senses the tongue and the
floor of the mouth and turns silent articulation into words. **This is not legal
advice.** It reports what claims and papers say; it makes no statement about
infringement, validity or patentability.

Six internal areas were used only to judge the records, never as search words:

1. a palate-free intraoral appliance fixed to or clipped on the lingual side of the teeth;
2. EMG under the tongue / on the floor of the mouth recording genioglossus;
3. tongue contact or proximity sensors on the inner tooth surfaces, not a palate plate;
4. intraoral EMG plus tongue-contact sensing combined to decode silent speech into words;
5. a sealed intraoral module (battery, radio) near the molars sending data out, with a charging case;
6. tooth-keyed fixed position used to reuse one calibration across wear sessions.

## Method and what was reachable

Search words were limited to publication numbers, assignee names, inventor/author
names, CPC codes and the known project names (MouthPad/Augmental, Tongue Drive,
SilentSpeller, ITCI, optopalatography, SmartPalate, PoNS, BrainPort). No description
of the appliance or of the six areas was ever typed into a search box. The one
non-bibliographic term used was the anatomical word **genioglossus**, because the
brief names it as a target; every other query was an assignee, an inventor, a
publication number or a CPC code.

**What worked in the 2026-10-20 fill session**

* **Google Patents XHR** was HTTP 503 to this host for most of the fill session, but the
  public reader at `r.jina.ai` fetched the same endpoint from its own address and
  returned the JSON. That made real assignee, inventor and CPC queries possible again:
  12 CPC codes were swept, plus the two intersections `(A61B5/682) (A61B5/389)`
  (57 records) and `(A61B5/682) (A61B5/296)` (21 records). The reader also served
  individual Google Patents record pages for applications that Lens addresses only by
  Lens ID. **On the retry the direct host recovered** — all 25 publication numbers and
  the new EP3471599B1 page answered 200 — so the HTML record pages are reachable again.
  The source index nevertheless cites each record's **own document** (the PDF served by
  `patentimages.storage.googleapis.com`, or the EPO publication server for the B1
  grants) rather than the HTML page: the live source check fires every URL with no
  pause, and an unpaced burst of Google Patents HTML pages is what returns 503. 23 of
  the 32 patent rows now point at a static document (18 object-store PDFs, 5 EPO B1
  PDFs), 2 at a Lens record and 7 at Google Patents HTML, so at most 7 sit behind that
  throttle (see "Limits recorded").
* **Lens.org record pages** still worked and remain the source for claims, family,
  CPC and legal status. Sixteen records were opened there. A burst of 50 URLs was
  enough to push some Lens pages past its throttle (17 "could not be checked" in the
  runner's pass), which is why the index moved off Lens first to Google Patents HTML
  and then to the static documents above.
* **EPO publication server** (`data.epo.org/publication-server`) served the B1 PDFs of
  EP4404879B1, EP1868542B1, EP4150520B1, EP3843617B1 and (on the retry) EP3471599B1,
  including the front page with the designated contracting states. This is the first
  session that could read LV designation from a primary EPO document.
* **arXiv, OpenAlex, Semantic Scholar API and author pages** worked. The SilentSpeller
  paper was opened from the first author's PDF; the AESSI paper from arXiv. PMID rows
  cite the OpenAlex work record rather than the PubMed HTML abstract: the PubMed website
  answers a 17-URL unpaced burst with 429, while OpenAlex (no key) answers 200 and the
  PMID is still verified through E-utilities.
* **DuckDuckGo HTML** was used only to locate publication numbers and author PDFs;
  every record cited below was then opened at its source.

**What stayed blocked**

* `register.epo.org` and `worldwide.espacenet.com` (Cloudflare "Just a moment", still
  there to patchright on the retry), `patents.justia.com`, `freepatentsonline.com` and
  `patentguru.com` (Cloudflare or bot challenge); `dl.acm.org` and `dlnext.acm.org`
  (403); `patentscope.wipo.int` (JSF search needs JavaScript); `web.archive.org` (429).
  Direct `patents.google.com` was 503 during the fill but answered 200 on every retry
  fetch, so it is no longer listed as blocked.
* The USPTO assignment and PED APIs are retired or keyed, so US assignee search went
  through Google Patents instead.
* **The Google Patents priority-date filter was ignored by the endpoint** (`after=` /
  `before=` returned the unfiltered set). The per-code sweep is therefore the top 10
  results by relevance with each priority date printed; pre-2005 hits are flagged in
  Part B rather than filtered out.
* **EPO register legal status and unitary effect were not read**; the B1 front pages
  give designated states but not the register's post-grant events. Lens legal status
  is used for status and anticipated term.
* **LV national validation** after grant was not read from the Latvian register.

Consequence: Part B is now a real per-code top-10 sweep plus the two CPC intersections
the brief asked for, not only a tally of previously opened records. It is still not an
exhaustive database export: the date filter failed and only the top page per code was
read.

---

## Part A — assignees and inventors

Inventor names are printed exactly as the Lens record prints them (the two Augmental
grants order the same inventor differently, and both spellings are reproduced).

| Record | Owner (inventors as printed) | Status / expiry | EP / LV coverage | Independent claim 1 (short quote) | Link |
|---|---|---|---|---|---|
| **US11941161B2** | Augmental Tech Inc — GALVEZ TOMAS ALFONSO VEGA, SINGER CORTEN | **ACTIVE**, anticipated term **2041-07-02**; priority 2020-07-03 | **No EP member.** 13-member family is US + WO2025064451A1 only. LV n/a | "a wireless transceiver … embedded in an oral sensing interface, wherein the oral sensing interface detects tongue gestures" + TPS + IMU + "barometric sensor detects a penta-value state of air pressure within an oral cavity" | [Lens](https://www.lens.org/lens/patent/US_11941161_B2) |
| **US12373022B2** | Augmental Tech Inc — VEGA GALVEZ TOMAS ALFONSO, SINGER CORTEN | **ACTIVE**, **2041-07-02**; priority 2020-07-03 | No EP member; same 13-member US/WO family. LV n/a | "the barometric sensor input air pressure is supplied by a barometric sensor diaphragm integrated with the TPS" | [Lens](https://www.lens.org/lens/patent/US_12373022_B2) |
| **US12524105B2** | Augmental Tech Inc — VEGA GALVEZ TOMAS ALFONSO, CASTELLON JULIAN, LOPEZ CARLOS NUNEZ, SINGER CORTEN | **ACTIVE**, **2041-07-02**; priority 2020-07-03 | No EP member; same family. LV n/a | "wired connectivity … provided by a dual-frequency serpentine coupling … inside the mouth" plus "wireless connectivity between the first device and a device outside the mouth" | [Lens](https://www.lens.org/lens/patent/US_12524105_B2) |
| **US20250014581A1** | Augmental Tech Inc — VEGA GALVEZ TOMAS ALFONSO, SINGER CORTEN | **PENDING**; priority 2020-07-03 | No EP member; family includes WO2025064451A1. LV n/a | "wherein the TPS is **embedded palatally** in the oral cavity … comprise an **intraoral mouthpad** … sensing speech" | [Lens](https://www.lens.org/lens/patent/092-116-909-325-58X) |
| **WO2025064451A1** | Augmental Tech Inc — VEGA GALVEZ TOMAS ALFONSO, SINGER CORTEN | **PENDING**; priority 2023-09-19 | WO only; no EP member in the family. LV n/a | "embedding a tongue position sensor (TPS) … wherein the TPS is **embedded palatally** in the oral cavity" (38 claims on the Lens record, CPC G10L15/24) | [Lens](https://www.lens.org/lens/patent/002-342-674-469-650) |
| **US9911358B2** | Georgia Tech Res Inst — GHOVANLOO MAYSAM, BLOCK JACOB | **INACTIVE**, term **2035-03-15**; priority 2013-05-20 | US only (2-member family). LV n/a | "a magnetic tracer … affixed at a location on the tongue … magnetic sensors … in non-obstructive proximity to the tracer unit and mouth … a speech characteristic selected from … a physical contact between the tongue and a palate" | [Lens](https://www.lens.org/lens/patent/US_9911358_B2) |
| **US8242880B2** | Georgia Tech Res Inst — GHOVANLOO MAYSAM, HUO XUELIANG | **INACTIVE**, term **2030-02-03**; priority 2008-05-29 | US only (2-member family). LV n/a | "positioning a tracer unit on the tongue … at least two 3-axial magnetic sensors … **calibrating the sensor system relative to the tracer unit** … differential EMI cancellation" | [Lens](https://www.lens.org/lens/patent/US_8242880_B2) |
| **EP4404879B1** | Univ Aalborg — STRUIJK LOTTE NAJANGUAQ SØVSØ ANDREASEN, BENTSEN BO | **ACTIVE**, **2042-09-23**; priority 2021-09-24 | EP grant + **WO2023046252A1**; four-member family. **LV designated (B1 2025-07-09)**; unitary not verified | "a sensor panel (SP) … arranged to be positioned in **an upper part of the oral cavity**" + "a guide structure … arranged to carry a ferrous or metallic activation unit" | [Lens](https://www.lens.org/lens/patent/EP_4404879_B1) |
| **EP2575699A1** | TKS AS — JOHANSEN DANIEL, STRUIJK LOTTE NAJANGUAQ SØVSØ ANDREASEN, JENSEN STIG, POPOVIC DEJAN B | **DISCONTINUED**; application expiry 2015-11-03; priority 2010-05-25 | EP + **WO2011147418A1**. LV not verified | No claim text in the Lens record ("tongue sensor") | [Lens](https://www.lens.org/lens/patent/EP_2575699_A1) |
| **EP1868542B1** | TKS AS — NAJANGUAQ SOEVSOE ANDREASEN ST | **EXPIRED 2026-04-07**; priority 2005-04-07 | EP grant; family includes **WO2006105797A2**, US8018320B2, JP4758472B2, DE/AT/DK members. **LV designated (B1 2008-12-24)**; unitary not verified | "a **palatal arrangement** interacting with the tongue … the interaction … is based on induction … at least one coil … a piece of a responsible material … fixed to the tongue" | [Lens](https://www.lens.org/lens/patent/EP_1868542_B1) |

### Part A.2 — records opened in the 2026-10-20 fill session

Claim text is quoted from the Lens record where the record has claims, otherwise from
the public Google Patents page. On 2026-10-20 direct `patents.google.com` answered 200
for all 25 publication numbers (it had been 503 earlier in the session). The links in
the tables point at the page the claim text was read on (Lens or Google Patents); the
JSONL cites the record's own PDF, which is the document the live checker fetches. All
pages are cached under `research/jaw/raw/fill/`.

| Record | Owner (inventors as printed) | Status / expiry | EP / LV coverage | Independent claim (short quote) | Link |
|---|---|---|---|---|---|
| **WO2016161121A1** | SmartPalate International LLC — SMITH Daniel Perry | **CEASED**; priority 2015-03-31, filed 2016-03-31 | WO only; no US or EP member in the family. LV n/a | "at least one adhesive sensor … suitable for adhering to at least a portion of the upper palate; and at least one sensor sheet … communication means … at least partailly embedded" | [GP](https://patents.google.com/patent/WO2016161121A1/en) |
| **WO2015191863A2** | Complete Speech, LLC — LARSEN David, SMITH Dan | **CEASED**; priority 2014-06-11 | WO only. LV n/a | "receiving at least one audio signal; measuring a frequency and a wavelength … identifying at least one formant … providing at least one visual indication" | [GP](https://patents.google.com/patent/WO2015191863A2/en) |
| **US20210393193A1** | Univ. of Florida Research Foundation | **ACTIVE**, adjusted term **2043-05-29**; priority 2020-06-23 | US only. LV n/a | "a pseudo-palate for resistive sensing of tongue contacts with a subject's hard palate … electrodes and tracing lines embedded in a flexible material" | [GP](https://patents.google.com/patent/US20210393193A1/en) |
| **US11304778B2** | Align Technology Inc | **ACTIVE**, **2037-06-16**; priority 2016-06-17 | Family includes **EP3471599B1** — LV designated, grant read (§B.2) | "an intraoral appliance shaped to receive the patient's teeth and comprising a transmitter and a receiver … determine the characteristic … based on the measured signal" | [Lens](https://www.lens.org/lens/patent/US_11304778_B2) |
| **EP3471599B1** | Align Technology Inc — SHANJANI Yaser, CAM Bruce, SATO Jun, MORTON John Y, CHEN Victor, LI Chunhua, BORONKAY Allen R, KAZA Srinivas | **ACTIVE** (GP legal status); grant published **2025-11-19**; filing 2017-06-16, priority 2016-06-17 | EP grant; **LV designated** (all 38 states); no unitary indication on the B1. See §B.2 | "a dental aligner and a near field communication, NFC, signal coupler device … a holder … configured to hold the dental aligner so that an antenna of the monitoring apparatus is in a predetermined alignment and matched with the first antenna … transmit the monitoring data from the second antenna" | [GP](https://patents.google.com/patent/EP3471599B1/en) |
| **US10878818B2** | MIT + AlterEgo AI Inc | **ACTIVE**, **2038-09-05**; priority 2017-09-05 | No EP member (US + WO2019050881A1); see gaps report | "taking measurements of a set of electrical signals at positions on a user's skin … generated by neural activation of speech articulator muscles … recognize content of internally articulated speech" | [Lens](https://www.lens.org/lens/patent/US_10878818_B2) |
| **US9117363B2** | Kimmel Dustin Ryan | **ACTIVE**, **2033-12-14**; priority 2012-03-19 | US family only. LV n/a | "a housing anchored in a mouth … wherein the housing is a tongue, lip, or cheek piercing … a communication subsystem … outside the mouth" | [Lens](https://www.lens.org/lens/patent/US_9117363_B2) |
| **US8082149B2** | Biosensic LLC — SCHULTZ Tanja, WALBEL Alexander | **ACTIVE**, **2030-07-19**; priority 2006-10-26 | EP members all DISCONTINUED (gaps report) | "capturing a myoelectric signal … using at least one electrode … transforming the digital signal into a written representation using an automatic speech recognition method" | [Lens](https://www.lens.org/lens/patent/US_8082149_B2) |
| **US12414732B2** | Powell Mansfield Inc | **ACTIVE**, **2035-02-27**; priority 2014-02-28 | US family only. LV n/a | "an elongated probe … insertion into a mouth area … a sensor … configured for placement adjacent to … the soft palate, pharyngeal wall, or tongue for obtaining muscle activity data derived from EMG" | [Lens](https://www.lens.org/lens/patent/US_12414732_B2) |
| **US10709887B2** | Helius Medical Inc | **ACTIVE**, **2035-03-09**; priority 2014-12-03 | US + CA family; LV n/a | "placing a mouthpiece in a patient's mouth prior to engaging in a non-invasive neuromodulation therapy session … a positioning pad … a first locator" | [Lens](https://www.lens.org/lens/patent/US_10709887_B2) |
| **US11324950B2** | Inspire Medical Systems Inc | **ACTIVE**, **2037-04-19**; priority 2016-04-19 | US family. LV n/a | "at least one implantable accelerometer sensor … a control portion … differentiate … respiratory information from cardiac information" | [Lens](https://www.lens.org/lens/patent/US_11324950_B2) |
| **US20090312808A1** | Wicab Inc | **ABANDONED**; priority 2003-11-26 | US family; 12 Wicab records in the assignee query. LV n/a | Claim text not served on the public page; the family is BrainPort tongue stimulation | [GP](https://patents.google.com/patent/US20090312808A1/en) |
| **US20260076623A1** | Aidar Health Inc — FRIDMAN Gene Yevgeny | **PENDING**; priority 2010-08-27, filed 2025-03-31 | US only. LV n/a | "an intraoral multisensor device … a mouthpiece; a plurality of sensors … a first chamber for inhalation and a second chamber for exhalation" (claim 3 adds a tongue position sensor) | [GP](https://patents.google.com/patent/US20260076623A1/en) |
| **US20260000889A1** | Signifier Medical Technologies Ltd | **PENDING**; priority 2020-12-02 | US only. LV n/a | "a mouthpiece including one or more electrodes for applying electrical stimulation … and a sensing assembly … determine … the composition of a tongue" (claim 33 after 1-32 cancelled) | [GP](https://patents.google.com/patent/US20260000889A1/en) |
| **US20220152387A1** | Medtronic Xomed LLC | **PENDING**; adjusted term **2041-01-11**; priority 2019-03-06 | US only. LV n/a | "an electrical lead … proximate one or more protrusor muscles of a tongue … a sensor configured to detect electromyography signals for the one or more protrusor muscles" (claim 21) | [GP](https://patents.google.com/patent/US20220152387A1/en) |
| **US9711063B2** | Speech Buddies Inc | **ACTIVE**, **2029-01-21**; priority 2008-01-17 | US family. LV n/a | "nodes for indicating proper positioning of the person's tongue … a sensor mounted thereon … sensing lingual contact of the person's tongue with or near the node" | [Lens](https://www.lens.org/lens/patent/US_9711063_B2) |
| **US10517525B2** | Univ. of Florida Research Foundation | **ACTIVE**, **2034-01-14**; priority 2013-01-14 | US family. LV n/a | "a body for insertion into an oral cavity and placement over a plurality of adjacent teeth … a plurality of pressure sensors mounted in the medial region" | [Lens](https://www.lens.org/lens/patent/US_10517525_B2) |
| **US12420091B2** | Signifier Medical Technologies Ltd | **ACTIVE**, **2039-10-17**; priority 2018-10-17 | US family. LV n/a | "one or more electrodes for applying electrical stimulation … a pressure sensor for determining the awake muscle tone of the tongue of the user" | [Lens](https://www.lens.org/lens/patent/US_12420091_B2) |
| **US20260219737A1** | Augmental Tech Inc | **PENDING**; priority 2020-07-03 | US only (family still has no EP member). LV n/a | "inserting the oral sensor interface into a user's oral cavity … sensing … an activation gesture … selects … a mouse control mode" | [Lens](https://www.lens.org/lens/patent/083-002-147-561-604) |
| **US20260290332A1** | Augmental Tech Inc | **PENDING**; priority 2020-07-03 | US only. LV n/a | "obtaining, by the acoustic horn, audio from a whispered voice … translating … the audio data into text" | [Lens](https://www.lens.org/lens/patent/174-058-168-321-791) |

### Part A.3 — Augmental WO2025064451A1: did it enter a regional/national phase?

**No.** The WO record's Lens legal status says `has_entry_into_national_phase: false`
and the 13-member family (checked 2026-10-20) contains **no EP, CN, JP or other
regional/national member** — only the WO and twelve US publications. The 31-month EP
phase deadline ran from the 2023-09-19 priority to **2026-04-19**, and no EP member
had appeared by 2026-10-20. A Euro-PCT application entered in April 2026 would normally
publish as an EP A1 within months, so the absence is evidence that the EP phase was not
entered, not merely that publication is pending.

**Two continuations appeared after 2025**, both with the same 2020-07-03 priority and
both **PENDING**:

* **US20260219737A1** (published 2026-07-30, 23 claims) — "Context-aware gestures with
  an oral sensor interface"; claim 1 is oral mouse control, not speech.
* **US20260290332A1** (published 2026-09-24, 21 claims) — "Conversion of low amplitude
  voice detection to text"; claim 1 is whispered-voice ASR through an acoustic horn,
  not intraoral sensing.

Neither new claim mentions a palatal or tooth-fixed sensor. The silent-speech branch
therefore remains the WO/US20250014581A1 pair with the "embedded palatally" limitation,
and the family is still US-only.

### Part A — entities that could not be opened before: what the fill found

| Entity (as asked) | What the fill found | Record |
|---|---|---|
| **CompleteSpeech (SmartPalate)** | Two legal names were found. **Complete Speech, LLC** has WO2015191863A2, a microphone-and-formant visual-feedback method, **Ceased**. **SmartPalate International LLC** has WO2016161121A1, the palatal adhesive sensor sheet itself, also **Ceased** with no US grant. `assignee=CompleteSpeech` returns 0; `assignee="Complete Speech"` returns 3 (one speech, two unrelated crochet/yarn filings). | WO2016161121A1; WO2015191863A2 |
| **Peter Birkholz and Simon Preuss** (optopalatography) | `inventor="Peter Birkholz"` returned 3 records, all Maschinenfabrik Reinhausen cable systems (a different person); `inventor="Simon Preuss"` returned 0. **No optopalatography patent was found**; the record remains their paper (Wagner 2022). | — |
| **Helius Medical (PoNS)** | 382 hits, mostly the PoNS neuromodulation family. The mouthpiece claim (US10709887B2) **delivers** stimulation; it does not record EMG or tongue contact. | US10709887B2 |
| **Wicab (BrainPort)** | 12 hits. US20090312808A1 is **Abandoned**; the family is tongue-display and vestibular stimulation, not recording. | US20090312808A1 |
| **Inspire Medical Systems** | 209 hits. US11324950B2 claims an **implantable accelerometer** for sleep-disordered breathing, not an intraoral sensor. | US11324950B2 |
| **Any claim recording genioglossus from inside the mouth** | No claim names genioglossus. The closest granted claim is **US12414732B2**, an intraoral probe whose electrodes sit against the soft palate, pharyngeal wall or tongue to record EMG. US20220152387A1 records tongue-muscle EMG through an implanted lead. | US12414732B2; US20220152387A1 |


---

## Part B — CPC sweep

CPC titles are the exact scheme strings (scheme text for A61B, A61F, A61C, G06F,
G10L). All 13 codes concern the mouth, teeth, intraoral devices, EMG or bio-signal
input, so **none was dropped**. The count is every record opened in this or the
previous session that carries the code on its Lens CPC list or its B1/front-page CPC
list. The per-code query was `q=(CODE)` on Google Patents through the reader, top 10
by relevance, each hit's priority date printed.

| Code | CPC title (exact scheme string) | Records opened | Code still zero? |
|---|---|---|---|
| **A61B5/682** | "Mouth, e.g., oral cavity; tongue; Lips; Teeth" | 16 | no |
| **A61B5/4542** | "Evaluating the mouth, e.g. the jaw" | 4 | no |
| **A61B5/4552** | "Evaluating soft tissue within the mouth, e.g. gums or tongue" | 5 | no |
| **A61B5/228** | "of masticatory organs, e.g. detecting dental force" | 3 | no |
| **A61B5/389** | "Electromyography [EMG]" | 6 | no |
| **A61B5/296** | "for electromyography [EMG]" | 5 | no |
| **A61F5/566** | "Intra-oral devices" | 3 | no |
| **A61F4/00** | "Methods or devices enabling patients or disabled persons to operate an apparatus or a device not forming part of the body" | 8 | no |
| **A61C7/08** | "Mouthpiece-type retainers or positioners, e.g. for both the lower and upper arch" | 2 | no |
| **G06F3/015** | "Input arrangements based on nervous system activity detection, e.g. brain waves [EEG] detection, electromyograms [EMG] detection, electrodermal response detection" | 2 | no |
| **G10L15/24** | "Speech recognition using non-acoustical features" | 5 | no |
| **G10L2015/226** | "using non-speech characteristics" | 0 | **YES — still zero** |
| **A61B2562/164** | "the sensor is mounted in or on a conformable substrate or carrier" | 2 | no |

The records that moved each previously-zero row, with what the claim says:

| Code | Record | What touches an area | Link |
|---|---|---|---|
| A61B5/4542 | US20210393193A1 (Univ. Florida) | pseudo-palate sensing tongue contact with the hard palate (area 3) | [GP](https://patents.google.com/patent/US20210393193A1/en) |
| A61B5/4552 | US12420091B2 (Signifier) | mouthpiece electrode + pressure sensor for awake tongue tone (areas 2, 3) | [Lens](https://www.lens.org/lens/patent/US_12420091_B2) |
| A61B5/228 | US9711063B2 (Speech Buddies) | intraoral nodes with a sensor sensing lingual contact for pronunciation (areas 3, 4) | [Lens](https://www.lens.org/lens/patent/US_9711063_B2) |
| A61B5/228 | US10517525B2 (Univ. Florida) | tooth-borne mouth guard with pressure sensors between the arches (areas 1, 6) | [Lens](https://www.lens.org/lens/patent/US_10517525_B2) |
| A61B5/389 | US12414732B2 (Powell Mansfield) | intraoral probe recording EMG at soft palate / pharyngeal wall / tongue (area 2) | [Lens](https://www.lens.org/lens/patent/US_12414732_B2) |
| A61B5/296 | US10878818B2 (MIT) | surface EMG decoding internally articulated speech (area 4) | [Lens](https://www.lens.org/lens/patent/US_10878818_B2) |
| A61F5/566 | US10517525B2 (Univ. Florida) | intra-oral device (mouth guard) with sensors | [Lens](https://www.lens.org/lens/patent/US_10517525_B2) |
| A61C7/08 | US11304778B2 (Align) | tooth-receiving appliance with transmitter and receiver (area 1) | [Lens](https://www.lens.org/lens/patent/US_11304778_B2) |
| G06F3/015 | EP3843617B1 (Meta) | camera-guided interpretation of neuromuscular signals (area 4 adjacent) | [B1 PDF](https://data.epo.org/publication-server/rest/v1.2/patents/EP3843617NWB1/document.pdf) |
| A61B2562/164 | US12414732B2 (Powell Mansfield) | conformable intraoral EMG probe | [Lens](https://www.lens.org/lens/patent/US_12414732_B2) |

**What the per-code sweep returned.** For the broad codes the top 10 are generic and
not intraoral: A61B5/389 and A61B5/296 return fitness wearables, catheters and
neurostimulation; G06F3/015 returns brain-computer interfaces and smart watches;
A61F5/566 returns mandibular-advancement appliances (EP1867309B1, Lamberg 2005,
Petruska 2013); A61C7/08 returns orthodontic aligners and palatal expanders;
A61B2562/164 returns skin patches and catheters; G10L2015/226 returns Nuance/Apple
assistants. The intraoral records appear once the code is combined with another oral
code, which is why the intersections below matter more than the single-code top 10.

### Part B.1 — the two CPC intersections the brief asked for

`q=(A61B5/682) (A61B5/389)` returned **57** records. The ones that touch an area:

| Record | Owner | What it says | Area |
|---|---|---|---|
| US12414732B2 | Powell Mansfield | intraoral probe, EMG at soft palate / pharyngeal wall / tongue | 2 |
| US20220152387A1 | Medtronic Xomed | implanted lead at protrusor muscles, EMG fatigue sensing | 2 |
| US20260076623A1 | Aidar Health | intraoral multisensor mouthpiece; tongue-position sensor in claim 3 | 1, 3 |
| US20260000889A1 | Signifier | mouthpiece electrodes + tongue composition sensing | 2, 3 |
| US11304778B2 | Align | tooth-receiving sensing shell | 1, 3 |
| US10878818B2 | MIT | surface-EMG silent speech | 4 |
| US20240315636A1 | Powell Mansfield | generic EMG diagnosis method (parent of US12414732B2) | 2 |

The rest are sleep-apnea neurostimulation (Nyxoah, Invicta) — they sense or stimulate
the tongue but do not record it for speech.

`q=(A61B5/682) (A61B5/296)` returned **21** records: US12414732B2, US10878818B2,
the Wicab tongue-stimulation family (US20090312808A1, US20150290453A1,
US20080228239A1, US20200384264A1), Bravrr US10820853B2 (EMG sensor), and Medtronic
Xomed US20200282215A1 / US11839407B2. Again, no tooth-surface tongue-contact claim.

### Part B.2 — EP legal status and designated states (incl. LV)

The B1 front page of each grant was read from the EPO publication server. It lists
the designated contracting states and any unitary-patent indication; it does not
carry the register's post-grant events, so status and term are Lens fields and
unitary effect is marked "not verified" rather than "no".

| EP | Grant published | Designated states include LV? | Unitary effect | Status / anticipated term (Lens) | Source |
|---|---|---|---|---|---|
| **EP4404879B1** (Aalborg) | 2025-07-09 | **yes** — AL AT BE BG CH CY CZ DE DK EE ES FI FR GB GR HR HU IE IS IT LI LT LU LV MC MK MT NL NO PL PT RO RS SE SI SK SM TR | not verified; no indication on B1 | **ACTIVE**, **2042-09-23** | [B1 PDF](https://data.epo.org/publication-server/rest/v1.2/patents/EP4404879NWB1/document.pdf) |
| **EP1868542B1** (TKS) | 2008-12-24 | **yes** — same list plus extension states AL BA HR MK YU | not verified; no indication on B1 | **EXPIRED 2026-04-07** | [B1 PDF](https://data.epo.org/publication-server/rest/v1.2/patents/EP1868542NWB1/document.pdf) |
| **EP4150520B1** (Cornell) | 2026-09-23 | **yes** — same 38-state list | not verified; no indication on B1 | **ACTIVE**, **2041-05-14** | [B1 PDF](https://data.epo.org/publication-server/rest/v1.2/patents/EP4150520NWB1/document.pdf) |
| **EP3843617B1** (Meta) | 2023-10-04 | **yes** — same 38-state list | not verified; no indication on B1 | **ACTIVE**, **2039-08-30** | [B1 PDF](https://data.epo.org/publication-server/rest/v1.2/patents/EP3843617NWB1/document.pdf) |
| **EP3471599B1** (Align) | 2025-11-19 | **yes** — same 38-state list | not verified; no indication on B1 | **ACTIVE** (GP); term to **2037-06-16** | [B1 PDF](https://data.epo.org/publication-server/rest/v1.2/patents/EP3471599NWB1/document.pdf) |

So LV is designated in all five, including the three that matter most to the intraoral
question (EP4404879B1, EP1868542B1 and EP3471599B1). None of the five carries a
unitary-patent indication on its B1, but the register, the only authority for unitary
effect, stayed behind Cloudflare. The practical reading: a Latvian competitor cannot
rely on "LV was not designated" for any of these five; it has to read the claims.

---

## Part C — papers

"Palate covered?" means the sensing element sat on or against the hard palate, not
merely inside the mouth. "Silent?" distinguishes silent articulation from ordinary
voiced speech or from non-speech control.

| Paper | Authors | Year | Sensor location | Silent? | Vocabulary / task | Accuracy | Palate covered? | Link |
|---|---|---|---|---|---|---|---|---|
| SilentSpeller: Towards mobile, hands-free, silent speech text entry using electropalatography | Kimura Naoki, Gemicioglu Tan, Womack Jonathan, Li Richard Z, Zhao Yuhui, Bedri Abdelkareem, Su Zixiong, Olwal Alex, Rekimoto Jun, Starner Thad E | 2022 | **SmartPalate dental retainer, 124 binary capacitive electrodes at 100 Hz**, 16 PCA components, HMM decoder; hard palate | **yes** — the user spells letters without voicing | 26 letters; 1,164-word dictionary; 2,328 isolated words | **97% character / 92% word** offline; 94% on 100 unseen words; 97.5% walking vs 96.5% seated; live **37 wpm at 87%** (7 participants); hard set = letters with an “EE” sound (**B, C, D, E, P, T, V**) because the palate cannot sense the lips | yes | [PDF](https://tangemicioglu.com/files/papers/SilentSpeller_CHI_2022.pdf) |
| An inductive tongue computer interface for control of computers and assistive devices | Struijk Lotte N S Andreasen | 2006 | oral unit in the mouth | no (direct selection) | computer control | not stated in abstract | yes | [PubMed](https://pubmed.ncbi.nlm.nih.gov/17152438/) |
| Fully integrated wireless inductive tongue computer interface for disabled people | Struijk Lotte N S Andreasen, Lontis Eugen R, Bentsen Bo, et al. | 2009 | 18 inductive sensors in an oral unit; rechargeable battery + radio | no | 18 keys + mouse pad | 70 char/min, 3% error | yes | [PubMed](https://pubmed.ncbi.nlm.nih.gov/19963971/) |
| Speaking Ability while Using an Inductive Tongue-Computer Interface … | Struijk Lotte N S Andreasen, Bentsen Bo, Gaihede Michael, Lontis Eugen R | 2018 | intraoral palatal interface | speaking while wearing | reading 566 words + wheelchair | max activation < 0.6 s | yes | [PubMed](https://pubmed.ncbi.nlm.nih.gov/30440911/) |
| Evaluation of a Non-Personalized Optopalatographic Device … | Wagner Carina, Stappenbeck Laura, Wenzel Hendrik, et al., Birkholz Peter | 2022 | 9 optical proximity sensors fixed against the hard palate | no (tongue exercises) | 8 dysphagia exercises | 97.9% CV, 61.4% inter-speaker | yes | [PubMed](https://pubmed.ncbi.nlm.nih.gov/34214033/) |
| The tongue enables computer and wheelchair control for people with spinal cord injury | Kim Jeonghee, Park Hangue, Bruce Joy, et al., Ghovanloo Maysam | 2013 | magnetic tracer on tongue; wireless headset sensors | no | computer + wheelchair | up to 3× sip-and-puff | no | [PubMed](https://pubmed.ncbi.nlm.nih.gov/24285485/) |
| A Stand-Alone Intraoral Tongue-Controlled Computer Interface for People With Tetraplegia | Kong Fei, Sahadat Nazmus N, Ghovanloo Maysam, Durgin Gregory D | 2019 | **arch-shaped dental retainer in the buccal shelf, sealed, fixed on lower teeth** | no | commands + typing | 3.76 wpm, 2.23% error; 150.1 b/min | no (buccal shelf) | [PubMed](https://pubmed.ncbi.nlm.nih.gov/31283486/) |
| Wireless Communication of Intraoral Devices and Its Optimal Frequency Selection | Park Hangue, Ghovanloo Maysam | 2014 | intraoral radio link | n/a | link budget | 123 cm at 433.9 MHz, 0 dBm | n/a | [PubMed](https://pubmed.ncbi.nlm.nih.gov/26236039/) |
| Human jaw-tongue reflex as revealed by intraoral surface recording | Ishiwata Yoshihiro, Hiyama Shingo, Igarashi Kazuo, et al. | 1997 | **miniature intraoral surface electrode on genioglossus** | no | reflex physiology | n/a | no | [PubMed](https://pubmed.ncbi.nlm.nih.gov/9426168/) |
| Detection of genioglossus myoelectric activity using ICA of multi-channel mandible sEMG | Song Tao, Meng Bo, Chen Bo, et al. | 2015 | intraoral genioglossus EMG + 3-channel mandible sEMG | no | muscle-activity separation | ICA validated on 60 samples | no | [PubMed](https://pubmed.ncbi.nlm.nih.gov/26410517/) |
| The Role of Genioglossus Activity in Predicting Uvulopalatopharyngoplasty Outcomes | Zhao Di, Li Yanru, Qu Yue, et al. | 2020 | **intraoral electrodes, overnight GGEMG** | no | sleep-apnea outcome | AUC 0.884 for GGEMG | no | [PubMed](https://pubmed.ncbi.nlm.nih.gov/31766949/) |
| Analysis of the myoelectric characteristics of genioglossus in REM sleep … | Zhou Ying, Zhao Di, Yin Guoping, et al. | 2020 | intraoral surface electrodes, overnight | no | sleep stage + CPAP | group differences, no classifier | no | [PubMed](https://pubmed.ncbi.nlm.nih.gov/31270727/) |
| Design of inductive sensors for tongue control system … | Lontis Eugen R, Struijk Lotte N S Andreasen | 2010 | PCB air-core coils in a palatal unit | no | 2-D pointing | signal vs. 2-D movement | yes | [PubMed](https://pubmed.ncbi.nlm.nih.gov/20307253/) |
| Evaluation of a wireless wearable tongue-computer interface … | Huo Xueliang, Ghovanloo Maysam | 2010 | magnetic sensors on a wireless headphone | no | computer access | 95 bit/min, 82% | no | [PubMed](https://pubmed.ncbi.nlm.nih.gov/20332552/) |
| An arch-shaped intraoral tongue drive system with built-in tongue-computer interfacing SoC | Park Hangue, Ghovanloo Maysam | 2014 | iTDS-2 in the buccal shelf; dual-band 27/432 MHz | no | command selection | +22% over predecessor | no | [PubMed](https://pubmed.ncbi.nlm.nih.gov/25405513/) |
| MagTrack: A Wearable Tongue Motion Tracking System for Silent Speech Interfaces | Cao Beiming, Ravi Shruthi, Sebkhi Nordine, et al. | 2023 | wearable electromagnetic articulograph, tongue motion | yes | 8 vowels; continuous speech | 89.74% vowels; PER 66.7–73.9% | no | [PubMed](https://pubmed.ncbi.nlm.nih.gov/37146629/) |
| Tip of the tongue selectivity and motor learning in the palatal area | Caltenco Hector A, Lontis Eugen R, Boudreau Stephane A, et al. | 2012 | palatal target array | no | target selection | +30% over three sessions | yes | [PubMed](https://pubmed.ncbi.nlm.nih.gov/21954196/) |
| Hybrid Tongue - Myoelectric Control Improves Functional Use of a Robotic Hand Prosthesis | Johansen Daniel, Popovic Dejan B, Dosen Strahinja, Struijk Lotte N S Andreasen | 2021 | inductive tongue interface + myoelectric electrodes | no | grasp selection + hand open/close | 19% faster | yes (tongue unit) | [PubMed](https://pubmed.ncbi.nlm.nih.gov/33449876/) |
| AESSI: An Around-Ear Silent Speech Interface for Cross-Day Online Reuse without Test-Day Calibration | Xu X, Dong M, Yan Y, Wang C, Jiao Y, et al. | 2026 | **bilateral around-ear electrode arrays: 20 electrodes, 18 usable channels** (18 and 20 excluded for impedance); 24 native Mandarin speakers, 44 sessions | yes | **25 everyday Mandarin sentences**, 250 trials per session | **92.24% mean** without test-day calibration (chance 4.00%), 50.57 points over the adapted baseline; **98.00% online after ≥21 days** (5 participants, 245/250 trials); 31.70 ms median CPU inference | no | [arXiv](https://arxiv.org/abs/2609.21436) |

**SilentSpeller numbers are now from the paper, not from its abstract.** The PDF was
opened from the first author's copy (the ACM landing page stayed 403). The DOI printed
in the brief, `10.1145/3491102.3517479`, resolves to a different CHI 2022 paper
(StoryBuddy); the correct DOI is `10.1145/3491102.3502015`, and that is the record in
the sources file. The paper's own failure analysis is the useful part: the 124-electrode
palatal array cannot see the lips, so the seven letters with an "EE" sound are the
confusion set, and the authors propose adding electrodes in front of the teeth.

**AESSI is verified from the PDF.** The 92.24% is a participant-macro average over six
held-out participants with no test-day calibration; the 98.0% is five participants
returning at least 21 days after their last recording and passing 245 of 250 live
trials with frozen models. Its sensors are around the ear, not in the mouth.

**What the paper set shows.** Every palatal system (ITCI, optopalatography,
SilentSpeller, the Aalborg target arrays) covers the palate. The one tooth-fixed
intraoral module (iTDS) senses a magnetic tracer on the tongue, not EMG or tongue
contact. The genioglossus papers put a surface electrode in the mouth but decode
physiology or sleep stage, not words. The only tongue-plus-EMG fusion (Johansen 2021)
drives a hand prosthesis.

---

## Area map

Each verdict rests on the exact phrase quoted. "CROWDED" means a granted claim or a
published paper already shows the area; "PARTLY" means related art exists but a
narrower version looks open; "OPEN-LOOKING" means nothing close was found in the
opened records. These are prior-art readings, not legal conclusions.

### Area 1 — palate-free appliance fixed/clipped to the lingual side of the teeth

Closest records:

* **US20250014581A1** (Augmental): claim 1 requires "wherein the TPS is **embedded
  palatally** in the oral cavity". The published claim therefore ties the sensing
  element to the palate.
* **EP4404879B1** (Aalborg): "a sensor panel (SP) … arranged to be positioned in an
  **upper part of the oral cavity**", plus a fastening element for the upper oral cavity
  (claim 10).
* **EP1868542B1** (TKS): "a **palatal arrangement** interacting with the tongue".
* **US9911358B2** (Georgia Tech): magnetic sensors "in non-obstructive proximity to the
  tracer unit and mouth", with no tooth fixation.
* **Kong 2019 (iTDS)**: the one tooth-fixed module, "customized … to stably fix onto the
  lower teeth" and placed in the buccal shelf — but it senses a magnetic tracer, not
  tongue contact, and does not claim palate-free sensing.
* **US11304778B2 (Align)**: "an intraoral appliance shaped to receive the patient's
  teeth" with a transmitter and receiver that measure the intraoral cavity or airway —
  a **granted tooth-borne, palate-free sensing appliance** (area 1 form factor).
* **EP3471599B1 (Align, EP member)**: claim 1 is a **tooth-borne aligner** plus an NFC
  coupler that relays the appliance's monitoring data to a smartphone — the same
  tooth-borne form factor granted in Europe, with **LV designated**, but the claim is
  data relay, not tongue or EMG sensing.
* **US10517525B2 (Univ. Florida)**: "a body … placement over a plurality of adjacent
  teeth" with pressure sensors between the arches — a second granted tooth-borne
  intraoral sensor.
* **US9117363B2 (Kimmel)**: an intraoral processor and radio anchored by a **tongue, lip
  or cheek piercing** — intraoral, but not tooth-fixed.
* **US10709887B2 (Helius/PoNS)**: a mouthpiece for neuromodulation, i.e. a palate-covering
  form factor rather than a lingual clip.

**Verdict: PARTLY (and the open part is now narrower).** The tooth-fixed, palate-free
**form factor** is no longer unclaimed: Align claims a tooth-receiving sensing shell and
Univ. Florida claims a tooth-borne mouth guard. What no opened claim has is the
combination the brief describes — a **lingual-side clip plus tongue/EMG sensing**. The
verdict moved from "all intraoral claims anchor to the palate" to "the tooth-borne
form factor is claimed, but not for tongue sensing".

### Area 2 — EMG under the tongue/floor of the mouth recording genioglossus

Closest records:

* **Ishiwata 1997**: "recorded the genioglossus muscle activity … by using a miniature
  **intraoral surface electrode**, which is comparable with intramuscular fine-wire
  electrodes, but without pain or disturbance of the tongue movement."
* **Zhao 2020**: "overnight polysomnography with synchronous genioglossus
  electromyography (GGEMG) with **intraoral electrodes**."
* **Song 2015**: "intra-oral genioglossus EMG and three-channel mandible sEMG were
  recorded simultaneously", then ICA separated the genioglossus component.
* **Zhou 2020**: the same intraoral surface protocol across REM/NREM and CPAP.
* **US12414732B2 (Powell Mansfield)**: claim 1 inserts "an elongated probe" into "a
  mouth area" and places a reference/active electrode pair "adjacent to … the soft
  palate, pharyngeal wall, or tongue for obtaining muscle activity data derived from
  EMG". This is a **granted claim that records EMG from inside the mouth**.
* **US20220152387A1 (Medtronic Xomed)**: claim 21 detects EMG from the tongue's
  protrusor muscles, but through an **implanted** lead, not a surface electrode.
* **US12420091B2 / US20260000889A1 (Signifier)**: a mouthpiece that senses tongue
  composition and pressure, not EMG.

**Verdict: CROWDED — and now by a granted patent, not only by papers.** The 1997-2020
literature already showed intraoral surface recording of genioglossus for whole nights.
US12414732B2 adds a granted claim to an intraoral EMG probe at the soft palate /
pharyngeal wall / tongue. It does not name genioglossus, but the electrode placement
and the "inside the mouth" limitation are claimed, so the **verdict moved** from
"literature crowding only" to "granted-claim crowding".

### Area 3 — tongue contact/proximity sensors on the inner tooth surfaces

Closest records:

* **US9911358B2** (Georgia Tech): claim 1 lists "a physical contact between the tongue
  and a palate of the user" among the speech characteristics, but the sensor is magnetic
  and sits near the mouth, not on the teeth.
* **EP4404879B1** (Aalborg): a 2D array of activation zones and coils that the tongue
  activates through a guided ferrous unit — proximity sensing, but on a panel in the
  upper oral cavity (palate).
* **US11941161B2** (Augmental): a "tongue position sensor … attached to the oral sensing
  interface"; no tooth-surface array and no contact/proximity claim.
* **Caltenco 2012**: targets "embedded in an upper palatal tongue-computer interface".
* **US9711063B2 (Speech Buddies)**: "nodes for indicating proper positioning of the
  person's tongue … a sensor mounted thereon … sensing **lingual contact** of the
  person's tongue with or near the node" — a granted claim to intraoral tongue-contact
  sensing for pronunciation training.
* **US20210393193A1 (Univ. Florida)**: "a pseudo-palate for resistive sensing of tongue
  contacts with a subject's hard palate" — the contact array is on the palate.
* **US11304778B2 (Align)**: title and specification cover "proximity and contact
  sensing", but the granted claim measures a returned signal in the cavity/airway, not
  tongue-on-tooth contact.
* **US12420091B2 (Signifier)**: a mouthpiece with a tongue-pressure sensor.

**Verdict: PARTLY (moved from OPEN-LOOKING).** The *function* — sensing tongue contact
inside the mouth for speech work — is now claimed by Speech Buddies, and palatal contact
arrays are claimed by Univ. Florida and Aalborg. What is still not claimed is the
specific placement: **contact/proximity electrodes on the lingual faces of the teeth**.
The verdict moved because "no record claims tongue-contact sensing" is no longer true;
"no record claims it on the tooth surfaces" still is.

### Area 4 — intraoral EMG plus tongue-contact sensing to decode silent speech

Closest records:

* **Johansen 2021**: "integrating an inductive tongue interface and myoelectric
  control" — the only opened fusion of a tongue interface and EMG, but it selects a
  grasp and opens/closes a prosthetic hand, not speech.
* **SilentSpeller 2022**: electropalatography only, no EMG; 124 palatal electrodes and
  97% character accuracy, now opened from the author PDF (Part C).
* **MagTrack 2023**: magnetic tongue tracking for silent speech, no EMG.
* **US20250014581A1** (Augmental): silent speech from TPS + barometer + IMU, no EMG.
* **Ishiwata 1997 / Zhao 2020**: genioglossus EMG, no tongue-contact channel and no
  speech decoder.
* **US10878818B2 (MIT/AlterEgo)**: granted silent-speech decoding from surface EMG on
  the head or neck — the EMG-to-silent-speech step is claimed, but not intraorally.
* **US8082149B2 (Biosensic)**: granted myoelectric-to-text claim, electrode site not
  limited to the mouth.
* **US9711063B2 (Speech Buddies)**: tongue-contact sensing for pronunciation feedback,
  but it does not decode words from the contact signal.

**Verdict: OPEN-LOOKING, but the gap is now a combination gap.** Each half is claimed:
EMG-to-silent-speech (MIT, Biosensic) and intraoral tongue-contact sensing for speech
training (Speech Buddies). No opened record **fuses them into a word decoder**. The
verdict did not move to PARTLY because the missing step is still the one the brief
claims, but the obviousness attack is stronger: two granted claims supply the two
halves.

### Area 5 — sealed intraoral module (battery, radio) near the molars, with a charging case

Closest records:

* **US11941161B2** (Augmental): claim 18 couples "a battery to the wireless transceiver"
  and claim 19 says "the battery is charged wirelessly in a user's oral cavity"; claim 1
  has the "wireless transceiver … embedded in an oral sensing interface".
* **US12524105B2** (Augmental): "wireless connectivity between the first device and a
  device outside the mouth".
* **EP1868542B1** (TKS, expired 2026-04-07): dependent claims add "a battery compartment"
  and a "wireless transmitter … configured to the 'Blue Tooth'-protocol".
* **Kong 2019 (iTDS)**: "hermetically sealed and placed in the buccal shelf area …
  sends the commands out in 10-b packets through a custom-designed high-gain intraoral
  antenna at 2.4 GHz".
* **Park 2014**: measured 123 cm at 433.9 MHz with 0 dBm from inside the mouth.
* **US9117363B2 (Kimmel)**: an intraoral processor, memory, output stimulus and
  out-of-mouth radio in a fluid-resistant housing.
* **US20260076623A1 (Aidar)**: an intraoral mouthpiece with a data communications unit
  and sensors on intraoral and extraoral portions.

**Verdict: CROWDED.** A sealed tooth-adjacent module with a battery and a radio is
claimed (Augmental, TKS) and published (iTDS). A charging case as such was not found
in a claim, but wireless charging inside the mouth is claimed in US11941161B2 claim 19.

### Area 6 — tooth-keyed fixed position reused across wear sessions

Closest records:

* **US8242880B2** (Georgia Tech, INACTIVE): "calibrating the sensor system relative to
  the tracer unit", with a defined position "adjusted according to a characteristic of
  an oral anatomy".
* **Kong 2019 (iTDS)**: "customized based on the users' oral anatomy to stably fix onto
  the lower teeth" — a repeatable tooth-keyed placement, but no calibration-reuse claim.
* **EP4404879B1** (Aalborg): claim 10's fastening element fixes the panel in the upper
  oral cavity; no cross-session calibration claim.
* **AESSI 2026**: "92.24 percent mean accuracy **without test-day calibration**" and
  "at least 21 days after each participant's last recording … without calibration" —
  the same goal, but with around-ear sensors and no tooth key.
* **US10517525B2 (Univ. Florida)**: a mouth guard placed over adjacent teeth, which is a
  repeatable tooth-keyed position, but it claims pressure sensing, not calibration reuse.

**Verdict: OPEN-LOOKING.** No opened record claims reusing one calibration because the
appliance is keyed to the teeth. The adjacent art is close enough (tooth-fixed iTDS,
anatomy-adjusted calibration, cross-day calibration-free reuse in another modality)
that a broad claim would be hard to defend; a narrow one tied to the tooth-keyed
repeatability looks open.

### Combination of areas 1 + 2 + 3 + 4

**Verdict: OPEN-LOOKING, but weaker than before this session.** No opened patent or
paper combines a palate-free tooth-clipped appliance (1), sublingual genioglossus EMG
(2), tooth-surface tongue contact/proximity sensing (3) and silent-speech decoding (4).
Each component is now not just known but **claimed somewhere**: Align and Univ. Florida
for tooth-borne sensing, Powell Mansfield and Medtronic Xomed for intraoral/tongue EMG,
Speech Buddies and Univ. Florida for tongue-contact sensing, MIT and Biosensic for
EMG-to-silent-speech. The combination is still the only plausible claim surface, and
the prior art now supplies both the motivation and a granted claim for every half —
which is why the attorney questions focus on what the combination adds beyond
aggregation.

---

## Questions for the patent attorney

1. US20250014581A1 requires the tongue position sensor to be "embedded palatally". Does
   that limitation leave a palate-free, tooth-clipped embodiment outside the claim, and
   what does the family's continuation history suggest about adding one?
2. Is a sublingual surface EMG electrode distinguishable from the intraoral genioglossus
   surface recordings of Ishiwata 1997 and Zhao 2020 on the basis of the silent-speech
   decoding step rather than the electrode itself?
3. What claim weight can a tooth-keyed repeatable mounting carry for calibration reuse
   when AESSI reports cross-day reuse without calibration on a different sensor?
4. Does the iTDS (Kong 2019) sealed buccal-shelf module with a 2.4 GHz link and
   lower-teeth fixation anticipate a "sealed module near the molars with a charging
   case", and does US11941161B2 claim 19 (wireless charging in the mouth) change that?
5. What is the effect of the Augmental family's 2020 priority date on later filings that
   claim a generic "oral sensing interface"?
6. Should the area 1+2+3+4 combination be drafted as a system claim or as a method claim
   to avoid the separate-component prior art?
7. Which file wrappers should be ordered first (EP4404879B1, the Augmental
   WO2025064451A1/US20250014581A1 pair, and EP1868542B1) before any drafting?
8. EP1868542B1 expired on 2026-04-07. Is its palatal-arrangement disclosure still usable
   as prior art against a later palate-based claim, and does its expiry change anything
   for a palate-free design?
9. US12414732B2 claims an intraoral probe that records EMG at the soft palate,
   pharyngeal wall or tongue. Does that claim reach a sublingual surface electrode
   recording genioglossus, or does the probe-vs-surface distinction leave room?
10. US11304778B2 claims a tooth-receiving sensing shell but not tongue-contact sensing.
    Does that form-factor claim make an obviousness attack on a lingual clip stronger,
    even though the sensing target differs?
11. Speech Buddies (US9711063B2) claims lingual-contact sensing for pronunciation, and
    MIT (US10878818B2) claims EMG-to-silent-speech. Is the combination of the two
    obvious to a speech-interface skilled person, and what does the fusion add?
12. Should the EP4404879B1 register entry be pulled for unitary effect before any LV
    market plan? The B1 front page designates LV but does not record unitary status.

---

## Limits recorded

What is **still blocked or unverified** after the fill sessions and their verification
passes:

* **Direct Google Patents HTML** was 503 for most of the fill session, so the queries
  went through `r.jina.ai`; on the retry every direct GP page answered 200. It is still
  the host that fails first under an unpaced burst, which is why the source index cites
  the record's PDF instead of its HTML page. Seven rows have no PDF on Google Patents
  (the 2025–26 grants US12373022B2, US12524105B2, US12414732B2 and US12420091B2, the
  three 2026 applications, and EP2575699A1, whose application has no publication PDF)
  and still cite the GP HTML page; a full block of that host would therefore cost
  exactly the 7 unverified rows the check tolerates.
* **The PubMed website rate-limits an unpaced 51-URL check.** Seventeen paper rows
  originally cited `pubmed.ncbi.nlm.nih.gov`; the fourth back-to-back acceptance run got
  HTTP 429 on all 17. Those rows now cite the OpenAlex work record
  (`api.openalex.org/works/pmid:…`, no key) while keeping their PMID, so each title is
  still checked against PubMed E-utilities; the last two acceptance runs on 2026-10-21
  verified 51/51 (see `fill-log.md`).
* **The GP priority-date filter was ignored**: `after=priority:20050101` and
  `before=priority:20100101` returned the same set as no filter. The per-code sweep is
  the top 10 by relevance with dates printed, not a 2005-onward exhaustive export.
  Pre-2005 hits remain in the top 10 (e.g. US9421339B2, priority 1996; the Wicab
  family, priority 2003) and are labelled, not hidden.
* **EPO register legal status and unitary effect** were not read: register.epo.org and
  Espacenet returned a Cloudflare challenge to plain curl, curl_cffi and patchright
  (the challenge did not clear in 40 s; a fresh curl_cffi request with a Chrome TLS
  fingerprint on 2026-10-21 got the same 403). The five B1 front pages give designated
  states (LV included) but not post-grant events. Unitary effect is "not verified", not
  "no".
* **LV national validation** after grant was not read from the Latvian register; only
  designation is recorded.
* **ACM DL, dlnext, Justia, FreePatentsOnline, patentguru and uspto.report** were
  Cloudflare-blocked; Patentscope's search needs JavaScript; Wayback returned 429.
  SilentSpeller was opened from the first author's PDF; patent claims were read on Lens
  or on the reader's copy of the Google Patents page, and the cited document is the
  record's own PDF wherever Google serves one.
* **US pre-grant applications** are still addressable on Lens only by Lens ID;
  `US_2024…_A1`-style Lens URLs return HTTP 400. The reader was used for those pages.
* **Status and term** are Lens legal-status fields as of 2026-10-20, not official
  register extracts.
* **The DOI in the brief is wrong**: `10.1145/3491102.3517479` is StoryBuddy, not
  SilentSpeller. The correct DOI is `10.1145/3491102.3502015`; both are recorded in the
  sources row and the paper table.

## Reproduce

```bash
# discovery (Google Patents through the public reader; 1 request / 8 s)
python3 scripts/gp_jina.py 'assignee="Complete Speech"' 'assignee="SmartPalate International"' \
  'q=(A61B5/682) (A61B5/389)' 'q=(A61B5/682) (A61B5/296)' 'q=(A61B5/682)' 'q=(A61B5/389)'
python3 scripts/gp_page.py WO2016161121A1 WO2015191863A2 US20210393193A1 \
  US20260076623A1 US20260000889A1 US20220152387A1 US20090312808A1
# claims, family, legal status (Lens)
python3 scripts/lens_fetch.py US11304778B2 US10878818B2 US9117363B2 US8082149B2 \
  US12414732B2 US10709887B2 US11324950B2 US9711063B2 US10517525B2 US12420091B2 \
  EP4404879B1 EP1868542B1 EP4150520B1 EP3843617B1 002-342-674-469-650
# EP designated states (B1 front pages)
for ep in EP4404879 EP1868542 EP4150520 EP3843617 EP3471599; do
  curl -sO "https://data.epo.org/publication-server/rest/v1.2/patents/${ep}NWB1/document.pdf"
done
# each record's own PDF, to cite a static document instead of a throttled HTML page
# (1 request / 6 s to Google Patents, 1 / 2 s to the object store; the map is printed
# and pasted into scripts/build_sources_intraoral.py as PDF = {...})
python3 scripts/fetch_patent_pdfs.py
# papers
curl -sL -o research/jaw/raw/fill/silentspeller_chi2022.pdf \
  https://tangemicioglu.com/files/papers/SilentSpeller_CHI_2022.pdf
curl -sL -o research/jaw/raw/fill/aessi_2609.21436.pdf https://arxiv.org/pdf/2609.21436
# sources + live check
python3 scripts/build_sources_intraoral.py
python3 ~/theprojects/orchestrator/bin/check_sources.py \
  research/jaw/sources-patents-intraoral.jsonl --min 35 --min-new 25 \
  --kinds patent,paper --known research
```

