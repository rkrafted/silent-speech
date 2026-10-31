# Track 06 — The implant option: is a small subdermal implant worth it?

*Research report for the silent-speech wearable project. Status: COMPLETE (all sections written; 77 sources).*
*Inline `[n]` citations map to the numbered Sources list at the end. Demonstrated results are separated
from claims/marketing. All numbers are quoted as the source gives them. Items I could not verify are
marked "unverified".*

Scope: the owner accepts a SMALL SUBDERMAL implant (skin-level — not brain, not nerve cuff) if it buys
invisibility. This track asks honestly what exists, what the real risks are, whether an implant actually
improves signal over good surface electrodes for speech muscles, and what is legal in Latvia/EU. It ends
with a verdict. Current date at time of writing: late 2026.

---

## 0. Bottom line up front

1. **Not worth it.** No implant route is justified to buy invisibility, because the implant that would
   help most (EMG in the speech muscles) has never been demonstrated in a human face and the implant that
   is easiest to get (an NFC/RFID chip or magnet) measures nothing useful for speech.
2. **The one modality with real silent-speech performance uses *glued* magnets, not implants** — >90%
   on 57 words with a 12-channel magnetic sensor array [7][11]. Implantation is a *retention* solution
   for those magnets, not a signal solution. Try glue first.
3. **Implanted EMG has been proven only in limb prosthetics** — first-in-human 2015 (arm), a new
   10-person trial started April 2026 (arm) [4][1]. In limbs, newer human data show real SNR and
   cross-talk gains (max SNR 304 vs 35 in one subject [61]), but older head-to-head studies found no
   *classification-accuracy* advantage [59][60]. **No published human facial/laryngeal/speech-muscle
   implant exists, and no implant-vs-surface comparison has ever been run in speech muscles** [14][15][17].
4. **The face is the worst possible implant site** — the marginal mandibular and buccal branches of the
   facial nerve run just under the SMAS through exactly the submental/cheek/upper-lip region a speech
   electrode would occupy [30][31]. A complication is a permanently visible facial asymmetry, which
   directly defeats the "barely different from normal face" requirement.
5. **Legal reality in Latvia/EU:** a subdermal speech sensor is a medical device. The EU MDR custom-made
   and "in-house" routes are designed for clinician–patient care inside a health institution, not for a
   private individual's non-medical project [47]–[55]. A body-mod artist is not a lawful route to
   a medical device implant, and a surgeon implanting a non-CE-marked device for a non-medical purpose is
   in a very exposed position.

If the owner still wants an implant, the only defensible version is **glued magnets first, and only then a
clinician-supervised magnet placement in the mouth (not the face)** — see §12.

---

## 1. What "implant" would even mean — five distinct strategies

The word "implant" hides five unrelated engineering choices with completely different risk profiles.

| # | Strategy | What goes under the skin | Where | Maturity |
|---|----------|--------------------------|-------|----------|
| A | Implanted EMG sensor capsule (IMES-class) | ASIC + electrodes + inductive coil, ~2.5 mm × 16 mm | In/near the muscle | First-in-human 2015 (arm) [4]; new trial 2026 [1] |
| B | Subdermal wire / needle EMG electrode | Insulated wire, bare tip; sometimes percutaneous | Muscle | Routine clinical for minutes–hours; chronic only in research |
| C | Magnet on tongue/lip | Nothing (glued) — *or* a magnet under the oral mucosa | Mouth/lips | Glued: real results, >90% on 57 words [7][11]; implanted: no human trial found |
| D | Subdermal magnet | NdFeB cylinder in a shell | Finger (biohacking), hand (Tongue Drive) | Thousands of biohacking implants; documented harms (§5) |
| E | Subdermal NFC/RFID chip or LED | 2.1 × 12 mm glass capsule | Hand | Commodity body modification; case-report complications [22] |

Only A and B record **electrical muscle activity** for speech. C and D are **kinematic** (movement)
sensors. E records nothing useful for speech and appears here only because "implant" in the
body-modification world means an RFID capsule — it is the realistic precedent for what a body-mod artist
would actually install, and the only one with a mass-market safety record.

The structural problem: every route that measures the speech muscles (A, B, C-implanted) puts a foreign
body into the face, mouth, tongue or submental region — the most nerve-dense, most mobile, most
infection-prone, most visible part of the body. Every route that avoids the face (E) gives no speech
signal. There is no implant location that is both useful for speech and low-risk.

---

## 2. Implantable EMG sensors (IMES, Phantom Neuro, Ripple, MyoPlant)

### 2.1 IMES — the reference design (Alfred E. Mann Foundation)

IMES is the only fully implanted EMG sensor with a long publication history. The primary IEEE paper
describes a system that receives and processes signals from **up to 32 implanted myoelectric sensors**;
each implant is a custom ASIC "packaged into a biocompatible RF BION capsule from the Alfred E. Mann
Foundation", powered and read over a **transcutaneous magnetic link**, and "designed for permanent
long-term implantation with no servicing requirements" [2]. The trial registry describes the device as
"**Tiny (2.5 mm by 16 mm) Implantable Myoelectric Sensors**" [5]; the primary development paper gives
the first-in-human proof of principle where the subject "was able to intuitively and simultaneously
control two DOF in a hand and wrist prosthesis" [3].

Animal state at publication: "Implants have been chronically implanted in the legs of three cats and are
still completely operational four months after implantation" [2]. (A secondary student summary claims
nine months and "8-bit resolution ... sample rate roughly 1000 samples/s/channel" [**unverified** — not in
the [2] abstract]; the [2] full text is reported to give Band-2 raw-EMG rates up to 15 kS/s with one
implant [2, full text].)

**Human use — arm prosthetics, not speech.** The first FDA-approved IMES trial (NCT01901081,
"Feasibility of Implantable Myoelectric Sensors to Control Upper Limb Prostheses") was sponsored by the
Alfred E. Mann Foundation, ran May 2013–Dec 2016, **actual enrollment 3**, completed. Inclusion required
residual anatomy supporting "at least six IMES", and subjects did six months of prosthetic training.
Primary purpose: DEVICE_FEASIBILITY [5]. The 2015 publication is explicitly "interim results" from
**one subject**, who could do a greater variety of tasks than with his previous myoelectric prosthesis [4].

The stated rationale for implants is the key sentence for this track: surface recordings are "often
inconsistent and unreliable", limited by "poor skin contact, socket rotation, residual limb sweating, and
their ability to only record signals from superficial muscles" [4]. That rationale is about a prosthetic
socket rubbing a sweaty residual limb and about reaching deep forearm muscle groups. Neither mechanism
applies to a bare face, and the facial muscles that matter most for speech (orbicularis oris, mentalis,
depressor anguli oris) are superficial.

### 2.2 Phantom Neuro / Phantom X — the 2024–2026 commercial attempt

The trial registry entry (primary source) is specific [1]:

- Title: "Evaluation of the Phantom X Implantable EMG Sensor System for Myoelectric Prosthesis Control"; acronym **CYBORG**.
- "first-in-human clinical investigation evaluating the safety and performance of the Phantom X System, an implantable electromyography (EMG) sensor array".
- System: "an implanted EMG sensor array, an implanted telemetry module, and an external wearable interface".
- Population: unilateral **transradial amputation and wrist disarticulation**; **estimated enrollment 10**; single-arm, open-label; primary purpose **DEVICE_FEASIBILITY**.
- **Actual start 2026-04-17**; estimated primary completion 2026-12; overall 2027-06. Status: RECRUITING. Sites: Cabrini Health, Malvern, and ProMotion Prosthetics, Moorabbin, Victoria, Australia. PI Michael Lo.
- Registry flags: `isUnapprovedDevice: true`, `isFdaRegulatedDevice: true`.
- Exclusion criterion 7: "Patient may require an MRI during the study duration" — i.e. the implant is incompatible with the possibility of an MRI [1].

So as of late 2026 Phantom X is a **10-person safety/feasibility study in amputees' arms**, started April
2026, with no published signal-quality data. It is not a speech device, has never been implanted in a
face, and no result exists yet. Phantom Neuro raised a $19M Series A led by Ottobock (announced April
2025) [company news, unverified against a filing]. Citing it as evidence that "implanted EMG for speech
works" is citing a pipeline, not data.

### 2.3 Ripple and MyoPlant

- **Ripple Neuro MIRA** is a 32-channel intramuscular recording array plus a subcutaneous package; a
  2022 animal/cadaver study (4 rabbits, 6 dogs + 3 sheep) reported electrode impedance **<5 kΩ** and
  average SNR **22.2 ± 6.2 dB**, with **2 sheep implants dislocated**, and a fibrous capsule of
  **19.00 ± 8.76 µm** at 3 months vs **29.00 ± 23.31 µm** for inert controls (no significant
  difference) [18]. Telemetry figures on the company site ("10.2 Mb/s or greater", "50%" coupling
  efficiency) are **company claims** [19].
- **MyoPlant** (German BMBF project, €3.8M, 2008–2014) used a central implant with distributed bipolar
  epimysial electrodes. In **2 rhesus macaques** a decoder trained on one day stayed accurate for months
  while concurrent surface EMG did not — no dB values given [20]; the project page claims "up to seven
  simultaneous arm movements" [21]. No human data found.

### 2.4 Verdict on the IMES-class route for speech

- Real, works for gross limb muscles, inside a human since ~2015 [3][4].
- **Never** applied to speech in a published human study. The closest work is animal: epimysial electrode
  arrays on rat face (10 Wistar rats; tolerated >40 days without infection; EMG→whisker model
  variance accounted for >96%) [14], and canine laryngeal EMG (8 canines up to 41 weeks) [15][16].
- Its selling points (deep-muscle access, sweat immunity, no socket) are largely irrelevant to a face
  except motion artifact and glue reliability.
- The cost is surgery, anaesthesia, a permanently powered inductive link, MRI exclusion [1], and a device
  approved for nothing — let alone for a face.

---

## 3. Subdermal wire/needle and epimysial electrodes

Needle EMG is a **diagnostic, minutes-long** procedure, not a chronic interface. Intraoperative subdermal
needle electrodes are placed under anaesthesia and "removed before you leave the operating room"
[46]. Complications are rare: in a study of **101 warfarin patients (INR ≥1.5)** there were
**2 small subclinical hematomas**, in **57 on clopidogrel/aspirin** there was **1**, and in **51
controls 0**; a survey of electrodiagnostic labs found that **4 of 60 (9%)** reported at least one
hemorrhagic complication requiring intervention in an anticoagulated patient and **none** with
antiplatelets [46].

Reusable **subdermal EEG electrodes** were implicated in a hepatitis B outbreak — **75 HBV infections
1991–1996, peak 18.2 cases per 1000 person-EEGs (1995)** — attributed to inadequate infection control
[46]. This is the cautionary tale for any percutaneous (through-the-skin) speech electrode:
the skin breach, not the electrode, is the risk.

Chronic **epimysial vs intramuscular** electrodes were compared directly in six users of a
neuromusculoskeletal arm prosthesis [6]: intramuscular electrodes had significantly greater
cross-channel impedance (better isolation) but this "did not translate to significantly improved
signal-to-noise ratio, separability, or repeatability". Epimysial SNR during hand movements was
**17.63 [14.43, 26.62] dB**. The practical lesson: even *among implant types*, the signal does not
automatically get better — and these were arm muscles, not face.

---

## 4. Permanent-magnet articulography (implanted vs glued magnets)

This is the one branch developed **specifically for silent speech / laryngectomy patients**, so it
deserves close reading.

### 4.1 What was actually demonstrated

The REdRESS interface (Hofe et al., Interspeech 2010) used **seven magnets** — "four on the lips, one on
the tongue tip and two on the sides of the tongue" — with the explicit design intent "to capture
sufficient data from important articulators while deploying a small number of magnets in an arrangement
which might realistically be implanted permanently in users in a practical system" [7]. In the prototype,
"the magnetic pellets are **glued** onto the skin and the tongue surface, respectively" [7]. Sensor side:
**six magnetic-field sensors measuring two components each = 12 data channels**, sampled at **500 Hz**
(16 kHz audio), using Honeywell HMC1022 sensors and a 12-bit ADC [7]. Magnet geometry: "cylinders with a
length and a diameter of 5mm and 1mm for the lips, 5mm and 2mm for the tongue sides and 4mm and 2mm for
the tongue tip" [7].

Task: **57 isolated words** including minimal pairs; **1,138 utterances** from one male speaker; whole-word
HMMs; forced choice. Results [7]:

| Condition | Errors / 1,138 | Word accuracy |
|---|---|---|
| Sensor (raw, 12 ch) | 131 | **88.5%** |
| SensorD (+ velocity) | 37 | **96.8%** |
| SensorDD (+ acceleration) | 37 | **96.8%** |
| SensorDex (velocity only) | 15 | **98.7%** |
| Audio (MFCC reference) | 3 | **99.7%** |

A three-speaker follow-up (MVOCA, Interspeech 2013) used **5 sensors × 3 components = 15 channels** at
500 Hz downsampled to 100 Hz and 71 CVC words. Word accuracy / segmentation accuracy were: **M1
90.97 / 86.76%**, **M2 82.72 / 76.72%**, **M3 84.91 / 74.89%**. Confusions were concentrated in voicing
and nasality pairs (b/p 15.8%, d/t 3.8%, f/v 17.7%, s/z 11.9%, b/m 20.0%) [8].

The later phonetic analysis (Gonzalez et al., Interspeech 2014) explains why. Using six magnets (lips
1 mm diameter × 5 mm, tongue tip 2 mm × 4 mm, tongue middle 5 mm × 1 mm), four triaxial sensors (three
signal + one Earth-field reference = **9 channels**), PMA oversampled from **100 Hz to 200 Hz**, and 420
CMU Arctic sentences, they found PMA "achieves comparable accuracy to using the audio signal for
discriminating the **place of articulation** of consonants, but it provides **little information regarding
the voicing and manner of articulation**" [9]. The measured symmetric-KL divergence between voiced and
unvoiced classes was **0.90 for MFCC vs 0.20 for PMA** [9]. Earlier reported results cited in [9]: 57-word
isolated recognition **98.80% PMA vs 99.70% audio**, connected digits **95.90% vs 96.30%**.

The journal version (Gilbert et al. 2010) states "recognition rates of **over 90%** are achievable for
vocabularies of at least 57 isolated words: sufficient to drive command-and-control applications", using
**500–1000 utterances** for speaker-dependent training/testing and DTW [11].

The magnet size and attachment are confirmed again in the 2016 Computer Speech & Language paper: magnets
"1mm (diameter) × 5mm (length) for magnets 1–4, 2mm × 4mm for magnet 5 and 5mm × 1mm for magnet 6", and
"These magnets are currently attached using **Histoacryl surgical tissue adhesive** (Braun, Melsungen,
Germany), but **would be surgically implanted for long term** [use]" — an aspiration, not a result. That
system was "sampled at 100Hz" [10].

**Scope of the evidence.** The 2018 project report records parallel MRI + PMA + speech recordings for
**4 subjects**, CV/VCV material [12]. Critically:
- Every human PMA trial used **glued**, not implanted, magnets [7][8][9][10].
- All participants had an **intact larynx**; the target laryngectomy population had not been tested in
  the cited work [7][12].
- The corpora were **voiced and simultaneously audio-recorded** (needed to learn the PMA→audio mapping),
  not silent-only.
- No human surgical implantation of speech magnets was found — no trial, no adverse-event series, no
  regulatory filing. University of Hull patent **US10283120B2** claims surgical implantation, but a
  patent is a claim, not evidence [13].

### 4.2 Tongue Drive System — the closest thing to a real implant precedent

The Tongue Drive System (TDS) is a **control** (not speech) interface using a magnetic tracer on the
tongue. In the clinical version, 8 participants with C3–C5 spinal cord injury used a "∅4.8 mm × 1.5 mm"
magnet held by Cyanodent adhesive; ~80% correct commands at 1 s, ~85 bits/min [42]. A tongue-**piercing**
variant was tested in humans: 10 screened, 3 ineligible (ankyloglossia), **7 pierced**, 1 exited at 48 h
for swelling/discomfort, **6 completed**; pain 5.8/4.0/2.9 on days 1–3; and — the important long-term
finding — "**Calculus developed ... in all participants by week 4**". The magnet was encased in a titanium
barbell [43]. A rat study implanted a 0.5 mm steel pellet for 24–28 days with no migration and a capsule
of **17.8 ± 10.2 µm** [44].

That calculus rate is a warning for any intra-oral magnet: the mouth coats foreign bodies in biofilm and
calculus, which is why a glued or implanted oral magnet needs constant maintenance.

### 4.3 What this means for the owner

- Kinematic magnet sensing is the **only** implant-adjacent silent-speech modality with real published
  performance (>90% on 57 words) [7][11].
- Those results came from **glued** magnets on an intact speaker.
- A glued magnet is the removable, zero-surgery version. Surgery adds risk without adding signal — the
  magnet's job is just to stay put. **Try glued magnets first.**
- PMA's fundamental weakness (no voicing / no manner of articulation) [9] is not fixed by implantation.
  Moving a magnet deeper under the mucosa changes retention, not information content.

---

## 5. Magnet implants in the body: migration, coating failure, MRI

### 5.1 Biohacker finger magnets — documented harms

The vendor of the xG3 injectable biomagnet describes it as a "**3mm x 15mm bioglass encased neodymium
magnet**", N52+, and warns that "nothing has been certified by any government regulatory agency for
implantation" and that "**all magnetic products are incompatible with MRI machines**" [45].

Peer-reviewed and case-level evidence:
- A **15-year-old ferrous foreign body** in the hand caused "intense right middle finger pain during
  MRI"; it was found incidentally and removed. The same case discussion cites intraocular-foreign-body
  blindness, fatal aneurysm-clip torquing, and five pacemaker deaths as MRI magnet/ferrous hazards [33].
- A radiology case documents an incidental **subdermal middle-finger magnet** in a 30-year-old man, and
  notes such implants are "often inserted in less than ideal sterile conditions" [34].
- First-person reporting: a magnet implanted in 2012 gave "about four years of peak performance", after
  which sensation faded [35]. Community history records coatings failing, migration, and MRI causing
  anything from "powerful vibration to slight pain" [37]. Forum self-reports describe a parylene rod
  "slowly moving its way down the open wound" [36] and a "**FDA2T-coated**" magnet becoming "extremely
  corroded" at ~8 months, removed in ~10 minutes of self-surgery, leaving **residual numbness** [36].

These are self-reported and not clinically adjudicated. I found **no peer-reviewed case report of MRI
injury caused specifically by a finger magnet**; the strongest MRI evidence involves generic ferrous
foreign bodies. The vendor's own MRI-incompatibility warning [45] is the operative fact.

### 5.2 MRI rules

FDA's 2023 guidance recognizes **ASTM F2052** (displacement force), **F2213** (torque), **F2503**
(marking), **F2182** (heating), **F2119** (artifact). "A maximum magnetically induced displacement force
of less than or equal to the gravitational force ... is often used as a conservative acceptance
criterion for implants." Devices are assessed per field strength: **0.25 T, 1.2 T, 1.5 T, 3.0 T, 7.0 T**;
a device safe at 1.5 T may be unsafe at other strengths. **MR Safe** means nonconductive, nonmetallic and
nonmagnetic; ferromagnetic devices cannot be labelled "Safety in MRI Not Evaluated" [32].

Practical consequence for a facial magnet: it permanently rules out or complicates MRI of the head and
neck — including the MRI that might one day be needed to investigate exactly the region you implanted.

---

## 6. Subdermal electronics / biohacking implants (NFC/RFID, Northstar)

**Dangerous Things xNT** (the commodity "chip implant") is documented by the manufacturer as an
"NTAG216 13.56MHz ISO14443A & NFC Type 2 chip" in a "**2.1x12mm cylindrical sterile bioglass implant**",
installed by injection. The manufacturer's own warning: "they have **not been certified by any government
regulatory agency for implantation or use inside the human body. Use of this device is strictly at your
own risk. These devices are MR conditional**" [23]. The recommended site is "between the metacarpal bones
of the index finger and thumb", at least 5 mm from bone [23]. I found **no published failure, expulsion
or rejection rate** for these devices — neither the company nor the medical literature reports one
[unverified gap].

The **Northstar V1** subdermal LED (Grindhouse Wetware, 2014–2015) was a circular implant with five red
LEDs, a processor and a battery, magnet-activated; five core members had it implanted in the hand in
2015, and documented removals happened "around eight months" and "two years" later [41]. No complication
rate is reported. Northstar V2 added gesture recognition and Bluetooth; the company later "found that
there wasn't a market" [41].

**VeriChip** is the one such device ever FDA-classified: an "Implantable Radiofrequency Transponder System
for Patient Identification and Health Information" (product code NRV, 21 CFR 880.6300), Class II via De
Novo **DEN040007**, applicant Digital Angel Corporation, decision date **12 October 2004** [38].

None of these measures speech. Their relevance is only as a risk baseline for "what a body-mod artist
actually installs" — and that baseline is far below a medical device.

---

## 7. Infection, rejection, extrusion, scarring — the numbers

There is no good body-modification complication dataset. The APP (Association of Professional Piercers)
explicitly scopes itself to piercing and "does not directly regulate, perform outreach, or offer
procedural guidelines on practices other than body piercing" [40], so the implant industry has no
self-regulatory statistics at all. Regulators treat the act as surgery: the NSW Health Care Complaints
Commission states subdermal implant insertion "involves surgery" (scalpel incision, tissue pocket,
suturing) and lists risks including infection — "in some cases may result in sepsis ... can be fatal" —
nerve damage, allergic reaction/rejection, and "scar tissue or other permanent damage" [39]. The best
available proxies:

**Case report (single case).** A 26-year-old man developed an **infected RFID/NFC chip in the middle
finger**; the chip was removed, soft tissue debrided, and "a pan-sensitive staphylococcus aureus was
detected by sonication of the RFID/NFC chip". Treatment was amoxicillin/clavulanic acid "24 hours iv,
total 11 days" plus splinting, with complete recovery [22]. No cohort infection rate exists.

**Contraceptive subdermal implant — a well-powered baseline for a small subdermal foreign body.** A
manufacturer-sponsored prospective cohort followed **7,364 Nexplanon insertions and 5,159 removals by 428
trained healthcare professionals** [24]:
- deep insertion **0.9% (95% CI 0.7–1.1%)**; partial **0.4% (0.2–0.5%)**;
- "severe pain" in the implant arm **2.4% (2.0–2.8%)**; pins/needles/numbness **2.8% (2.4–3.2%)**;
  altered strength/movement **1% (0.8–1.3%)**;
- multiple removal attempts **0.3%**; implant "too deep" **0.25%**; local migration **0.14%**;
  post-removal sensory disturbance **0.7%**, severe pain **0.3%**, motor disturbance **0.23%**;
- implant-site pain "around 3%–5%", local haematoma "about 2%" [24].
- Migration: "one case of intravascular migration for every 1.3 million implants sold"; a French survey
  found **12 pulmonary-migration cases Jan 2012–Jul 2017 against 1.2 million implants**, i.e. ~**1 in
  100,000** [24].

Caveat: Nexplanon is placed on the relatively immobile inner upper arm by trained clinicians under an FDA
REMS [25]. It is a **floor**, not a face-equivalent.

**Facial implants (silicone, chin/jaw).** A prospective study of **58 patients / 116 solid silicone
implants** with ≥6 months follow-up found **5 implants infected (4.3%)** and **16 displaced (13.8%)**;
patient satisfaction was **94%** (only 3 of 58 dissatisfied) [26]. A systematic review found silicone had
higher infection and displacement rates while porous polyethylene (Medpor) had more prominence problems;
exposure/extrusion rates were low for both, but the authors warn follow-up was "deficient" [27]. Biofilm
was found in **5 of 7** explanted facial implants; all 3 porous polyethylene samples had severe areas,
and the only 2 biofilm-free implants were silicone [28].

**Chronic subcutaneous electrodes (the closest structural analogue).** A prospective series of **38
subcutaneous EEG implant procedures** (epilepsy and healthy adults; ~15-minute procedure) reported
**6 cases where adverse events led to explant/discontinuation** — 4 implant pain/headache, **1
post-operative local infection**, and **1 superficial lead placement causing skin perforation a few weeks
after implantation**; 2 further events involved the implant fixating in the introducing needle and 2
silicone-sheath damages at explantation [29]. That is ~3% infection/skin-breakdown in the best-run
clinical hands, in the scalp — not the mobile, expressive face.

---

## 8. Facial-specific anatomy and risk

The face is not a generic implant site. Clinical teaching on "facial danger zones" identifies the motor
branches of the facial nerve (CN VII) that a facial implant can injure [30]:

- **Temporal branch** — beneath the superficial temporal fascia; landmark "line from 0.5 cm below tragus
  to 2.0 cm above lateral eyebrow", second line on zygoma to lateral orbital rim. The modern description
  is **Pitanguy's line**: from 0.5 cm inferior to the tragus to 1.5 cm superolateral to the lateral
  eyebrow; it "passes over the zygomatic arch ... approximately 5 cm anterior to the tragus" and is "most
  vulnerable where it crosses the zygomatic arch". Injury causes brow palsy, asymmetry and incomplete eye
  closure, risking exposure keratitis [31].
- **Zygomatic and buccal branches** — lie below the SMAS, resting on masseter and the buccal fat pad.
  The stated danger zone is "anterior to parotid, superior to mandible, posterior to z. major muscle,
  superior to masseter & buccal fat pad". These branches supply **orbicularis oris, buccinator, levator
  labii superioris, nasalis, risorius and levator anguli oris** — the exact speech muscles a
  silent-speech implant would sit next to [30].
- **Marginal mandibular nerve** — "beneath SMAS", "**very superficial**", paresis of the lip depressors.
  Landmark: "Draw line 2.0 cm lateral to oral commissure / Drop line from this point to mid-mandible /
  Draw circle 2 cm around this point" [30].

In other words, the submental/cheek/upper-lip region where a speech-muscle electrode would go contains the
marginal mandibular and buccal branches running immediately under the SMAS. Threading a subdermal implant
through that region means threading it through the facial nerve's territory, in the most visible real
estate on the body. Injury means a permanent, visible facial asymmetry — the exact opposite of the
owner's requirement that the device look "barely different from the owner's normal face".

---

## 9. Does the implant actually improve the signal? (implant vs surface evidence)

**Short answer: for limbs the evidence is mixed and metric-dependent; for speech muscles the comparison
has never been made in any species.**

### 9.1 The limb evidence — implants win on SNR, classification was already saturated

Two older head-to-head studies found surface EMG competitive on *classification accuracy*. Hargrove,
Englehart & Hudgins (2007) collected surface and intramuscular MES **simultaneously** for 10 classes of
isometric contraction and compared six pattern-recognition controllers. Result: "There was **no
significant difference in classification accuracy** as a result of using the intramuscular MES measurement
technique when compared to the surface MES measurement technique", and "**97%**" accuracy "could be
achieved by optimally selecting only **three channels of surface MES**" [59]. Farrell & Weir (2008)
extended this to **11 subjects**: with amplitude-only features, targeted surface, targeted intramuscular
and untargeted surface electrodes "produced **similar classification accuracies**" (untargeted
intramuscular was significantly worse); with richer features, "**no statistical differences were observed
between any of the electrode conditions**". Their conclusion: "the choice of electrode should be driven by
**clinical factors, such as signal robustness/stability, cost, etc., instead of by classification
accuracy**" [60].

Newer human data reverses the picture on *signal-quality* metrics. Wallace et al. (2026) compared
implanted electrodes (via regenerative peripheral nerve interfaces) against dry-domed surface electrodes
in **2 participants**: implanted signals had **389% higher median, 236% higher mean and 148% higher max
active-movement amplitude**; unitless max SNR was **304 (24.8 dB) vs 35 (15.4 dB)** for S1 and **537
(54.6 dB) vs 348 (50.8 dB)** for S2 (p<0.0005, stable over 3 monthly collections); average absolute
cross-correlation during pinch was **0.06 vs 0.33** (S1) and **0.07 vs 0.18** (S2) [61]. Salminger et al.
(2019) report **3 above-elbow amputees** with a **2.5-year** implant and "substantial functional
improvements" versus surface [62]. In animals, MIRA's 32 intramuscular electrodes stayed functional for
5–6 months with impedance **<5 kΩ** (plateau <1 kΩ) and mean SNR **22.2 ± 6.2 dB** [18].

So the honest framing is not "implants do not help" — in limbs they clearly improve amplitude, SNR and
cross-talk, and they add inter-day repeatability [61][62]. They simply did not improve *classification
accuracy* in the earlier studies because surface EMG had already saturated those tasks [59][60].

### 9.2 For the face, the depth advantage is physically small

Measured facial muscle depths from ultrasound:
- orbicularis oculi (inferior orbital) **1.69 mm** (range 1.00–3.90); superior palpebral **1.10 mm**;
  corrugator supercilii **3.82 mm** [63];
- depressor anguli oris — an actual silent-speech target — mean depth **3.1 ± 0.8 mm**
  (range 2.2–5.4 mm) in 290 Caucasian patients, 2.1 ± 0.4 mm in an Asian cohort [64].

Speech muscles therefore sit **~1–4 mm** under the skin, behind a thin SMAS layer [63][64]. The quantitative
fat-attenuation model — where adding **3 / 9 / 18 mm** of fat cut surface EMG RMS amplitude directly over
the active muscle by **31.3 / 80.2 / 90.0%** and raised crosstalk — is a *limb* model (Kuiken et al.
2003) [65][66]; the face does not have 9–18 mm of fat over orbicularis oris. In other words, the
"closer to source" advantage that makes implants compelling in the forearm is largely absent in the face.
The one place surface EMG genuinely cannot reach is the **genioglossus and other deep tongue muscles**
[67] — but the tongue is inside the mouth, so the relevant interface is intra-oral, not subdermal.

### 9.3 Surface EMG for speech works, and its failures are mechanical

- A 2025 pilot tested **14 face/neck muscles** and settled on an **8-channel bipolar setup** (digastric,
  depressor anguli oris, risorius, levator labii superioris, masseter, zygomaticus major, depressor labii
  inferioris, stylohyoid), sampled at **2048 Hz** with a −3 dB bandwidth constrained under **73.01 Hz**.
  Highest phone-classification test accuracy was **48.42%**. Reported failures: mouth electrodes "did not
  stick as well"; the orbicularis oris channel was "affected by sweat and condensation of air coming from
  the nose"; one channel degraded across rounds; and facial muscles are "long and narrow and close to each
  other", so arrays "increase the risk of cross-talk" [68].
- The ReSSInt project used **8 channels at 2048 Hz** with a **3D-printed face mask** to reposition
  electrodes; sessions <1 h; it was "very common for the electrodes to come off" (invalidating data), with
  ≥1 week between sessions and ~2 h of preparation each [69].
- A total-laryngectomy pilot used **20 surface electrodes** (face/jaw/neck) at **5000 Hz** with full skin
  prep and produced intelligible own-voice speech at mean human-listener **WER 20.16% (95% CI
  10.97–31.48)** for the patient and **14.88% (6.83–24.87)** for a healthy reference; only 9/20 (patient)
  and 11/18 (reference) channels were needed for 95% of the signal. Single session; longitudinal stability
  untested [70].
- Physics: surface EMG spectral content is **5–500 Hz**; "the thicker the fat layer or the deeper the MUs,
  the smoother the EMG signal and the narrower its bandwidth", while intramuscular EMG bandwidth extends
  beyond surface "at least until **1500 Hz**" [71].

The practical surface problems are real — but they are **adhesion, positioning and sweat** problems. Those
are exactly what a mechanically well-designed concealed epidermal array (mask/headset/frame) can fix
without surgery, and they are what the PMA headset already solves for magnets.

### 9.4 No speech-muscle implant comparison exists

No implant-vs-surface EMG comparison in facial, submental or laryngeal muscles was found **in any
species**, and no **long-term (>1 year) impedance/signal trajectory** exists for intramuscular
speech-muscle electrodes (gap). No silent-speech system uses an implanted speech-muscle EMG electrode:
the only invasive SSI route in the reviews is **intracranial** recording (ECoG, stereo-EEG,
microelectrode arrays) [72][73][74], and MIT AlterEgo is surface-only — it "reads electrical signals from
the surface of the skin in the lower face and neck" [75]. Denby et al. (2010) rated surface EMG
non-invasive 4/5 and ready-for-market 3/5, noting only that "surface electrodes need to be firmly
attached to the skin"; the only implant class they assessed was cortical BCI ("Brain surgery is
required") [73]. Gonzalez-Lopez et al. (2020) state that intramuscular needles are "problematic when the
aim is to measure the characteristics and behaviour of whole muscle signals, as is the case with SSIs"
[72]. The one human facial-EMG study found uses **needle EMG plus external ball electrodes** (10
patients; selective response within 4.5 cm horizontal and 3 cm vertical of the mouth corner) [17].

### 9.5 Electrode–tissue interface

Intramuscular leads in animals stayed at **<5 kΩ** for 5–6 months with only a **19 µm** fibrous capsule
[18]. By contrast, cortical microelectrodes form a tight cellular sheath at **6–12 weeks** that
"eventually increases the impedance of the electrode ... preventing it from registering electrical
activity" [76]. For intramuscular muscle electrodes the capsule does not appear to kill the signal in the
first months [18], but no facial/laryngeal long-term data exists. The non-medical risk/benefit question
is also unaddressed in the literature; the closest work is a 2025 proposal for a moratorium on
implantable **non-medical** neurotech, arguing that "at present, there are no compelling applications or
interesting use-cases for them" in people without disabilities, and that such implants are "nowhere
subject to clear, specific, and appropriate regulation" [77].

**Synthesis:** for a limb in a sweaty socket, implants buy robustness (and, in recent data, real SNR and
cross-talk gains) at the cost of surgery. For a face with 1–4 mm of soft tissue, they buy little of that
advantage and cost a facial nerve. Surface EMG already produces intelligible continuous speech [70]; the
remaining problems are adhesion and placement, not depth. That is why the recommendation is
surface/glued first, not implant.

---

## 10. Regulatory reality: EU MDR, Latvia, surgeon vs body-mod artist

*(MDR article text verified against the EUR-Lex-derived adopted text on legislation.gov.uk [47][48][49];
EUR-Lex itself returned HTTP 202/empty to this session's fetches, so numbers below are cross-checked
against MDCG guidance [51][52].)*

### 10.1 Is it a medical device? Yes, if its intended purpose is assistive communication.

MDR Art 2(1) defines a medical device as "any instrument, apparatus, appliance, software, implant,
reagent, material or other article intended by the manufacturer to be used ... for one or more of the
following specific medical purposes: — diagnosis, prevention, monitoring, prediction, prognosis,
treatment or alleviation of disease, — ... — investigation, replacement or modification of the anatomy
or of a physiological or pathological process or state ..." [47]. A sensor whose documented intended
purpose is to restore communication (a "compensation for a disability") is a medical device. A purely
non-medical novelty interface may escape that, but MDR **Annex XVI item 2** then potentially catches
"products intended to be totally or partially introduced into the human body through surgically invasive
means for the purpose of modifying the anatomy" [50] — a subdermal implant is not a "piercing". The
classification therefore turns on the intended purpose the owner documents — which is itself a risk,
because documenting "silent-speech communication aid" makes it a device.

Art 2(5): an **implantable device** is one "intended ... to be totally introduced into the human body
... **by clinical intervention** and ... to remain in place after the procedure" (partial introduction
for ≥30 days also counts) [47]. The MDR's own framing is that implantation *is* a clinical intervention —
not a body-mod service.

### 10.2 The custom-made and in-house routes are both closed to a private owner.

**Custom-made** (Art 2(3)) requires the device to be "specifically made in accordance with a written
prescription of any person authorised by national law by virtue of that person's professional
qualifications ... intended for the sole use of a particular patient" [47]. So the *prescriber* must be
a nationally authorised professional; the owner cannot self-prescribe. Custom-made devices are **not
CE-marked** (Art 20(1)), but they may be placed on the market only if Art 52(8) and Annex XIII are met,
and "manufacturers of **class III custom-made implantable devices shall be subject to the conformity
assessment as specified in Chapter I of Annex IX**" — i.e. a **notified body** is involved [49]. That is
a heavy, expensive, formal process, not a favour from a surgeon.

**In-house** (Art 5(5)) exempts devices "manufactured and used only within health institutions
established in the Union", provided conditions (a)–(h) are met, including "the devices are not
transferred to another legal entity" and the institution justifies that the patient group's needs cannot
be met by a market device; the exemption "shall not apply to devices that are manufactured on an
industrial scale" [48]. MDCG 2023-1 (non-binding guidance) states plainly: "**Article 5(5) is only
applicable to health institutions within the Union**"; "**Custom-made devices are out of scope of
Article 5(5)**"; and "**Self-tests cannot fall under Article 5(5) if used outside the health
institution's legal entity**" [51]. A private individual is not a health institution (Art 2(36): "an
organisation the primary purpose of which is the care or treatment of patients or the promotion of
public health" [47]).

**Research route:** a systematic self-experiment is most plausibly an Art 82 clinical investigation
("Clinical investigations, not performed pursuant to any of the purposes listed in Article 62(1)"),
which still requires compliance with parts of Art 62 and additional national requirements [51][49]. It
is not a loophole; it is a regulated pathway with ethics review.

### 10.3 Latvia specifically

- There is **no Latvian statute expressly regulating "body modification" or subdermal implants**.
  Cabinet Regulation No. 693 (8 Dec 2015, in force 1 Jan 2016) is a **notification/hygiene regime** to
  the Veselības inspekcija for "skaistumkopšanas ... kā arī tetovēšanas, skarifikācijas, permanentā
  grima, mikropigmentācijas un pīrsinga pakalpojumu sniegšanu" — tattooing, scarification,
  micropigmentation, piercing. **Implants are absent from the list** [54]. This is consumer/hygiene
  registration, not authorisation to implant a device.
- The **Ārstniecības likums** (Medical Treatment Law) reserves independent practice to registered
  medical persons (Art 26(1)); Art 12 makes unqualified independent treatment, and assisting it, liable
  [53]. Implantation as such is not named, and whether a cosmetic implant is "ārstniecība" is unsettled —
  which is precisely the legal grey zone. Art 36 makes the medical person responsible for "the use of the
  chosen medical technology and its consequences" [53].
- At EU level there is no single "reserved medical act" list: MDR Art 1(15) preserves national law on
  who may use certain devices [49]. A **body-mod artist is not a legitimate route** to a medical-device
  implant: their own products are explicitly uncertified "at your own risk" items [23], and the piercing
  industry's standards body does not cover implants [40]. The Veselības inspekcija (Latvian Health
  Inspectorate) is the body responsible for medical-device and beauty/hygiene-service oversight, but its
  published material covers devices and hygiene, not implantation of custom implants [58].
- The clearest EU regulatory-gap evidence found is a **Dutch government-commissioned evaluation (2011)**,
  which states that "het plaatsen van body implants" (placing body implants) and scarification are
  "momenteel niet wettelijk geregeld" — currently not legally regulated — and notes uncertainty over
  whether a piercer may lawfully make the incision required [55].

### 10.4 Product liability, insurance, and the surgeon's position

- MDR Art 10(16) lets persons "claim compensation for damage caused by a defective device"; manufacturers
  must hold financial coverage for product liability [49]. A self-manufacturer who never places the
  device on the market is unlikely to be a "manufacturer" for these purposes — so a DIY/self-implant
  leaves the owner with **little product-liability recourse**.
- Latvian **Ārstniecības likums Art 34(4)–(6)**: the sponsor of a clinical investigation of medical
  devices must insure its and the investigator's civil liability for harm to the subject, with cover in
  force for the whole investigation and minimum limits set by Cabinet [53]. A surgeon asked to implant a
  non-CE-marked device outside the custom-made or investigational routes is personally exposed under
  Art 36 and professional discipline.
- **AI Act:** an AI decoder that is a safety component of, or itself part of, an MDR device is likely
  **high-risk** — AI Act (EU) 2024/1689 Art 6(1) covers an AI system used as a safety component of a
  product under the harmonisation legislation listed in Annex I, where that product needs third-party
  conformity assessment; MDR 2017/745 is in Annex I Section A [57].
- **Precedent:** no EU prosecution or regulator action specifically about a self-used, subdermal
  silent-speech sensor was found. The nearest persuasive authority is the UK Court of Appeal decision
  *R v Crimi-Appleby* (2025), which upheld convictions over extreme non-medical body modifications and
  held that the victims' consent was no defence to offences of wounding and at most a sentencing factor
  [56]. The facts concerned castration, not implants, but the principle — consent does not legalise a
  non-medical invasive act — is directly relevant.

**Net legal position:** the legal risk is less "you will be prosecuted" than "no legitimate professional
can lawfully do this for you outside a formal notified-body/investigation process, and nobody is insured
if it goes wrong." A DIY or body-mod route is a legal grey zone and, more importantly, an uninsured one.

---

## 11. Cost and practicalities

- **Glued magnets / surface electrodes:** €0–low hundreds, reversible, no recovery, no scar.
- **NFC/RFID implant (if it were useful):** ~$25 for the xNT chip plus artist fee [23]; irrelevant to
  speech.
- **IMES-class implant:** not purchasable; clinical-trial-only, surgery plus anaesthesia, MRI exclusion
  [1], and approved for no indication.
- **Custom implanted magnet done properly (clinician):** would require a custom-made-device regulatory
  path, a willing surgeon, an oral/maxillofacial specialist, and a sterile magnet — no established
  supply chain or price exists.

---

## 12. Verdict

**No implant route is worth it over concealed epidermal electrodes for this project.** The reasoning, in
order of weight:

1. **Signal:** the one modality that has demonstrated silent-speech performance uses *glued* magnets, and
   implantation does not add information [7][9][11]. Implanted EMG improves mechanical reliability and
   (in limbs) SNR and cross-talk, but it has never been tested on a human face and the face's 1–4 mm
   soft-tissue depth removes most of its advantage [61][14][17].
2. **Risk:** the useful implant sites are exactly the facial-nerve danger zones [30][31]. A visible palsy
   is a worse outcome than a slightly visible electrode patch, given the owner's own "barely different"
   requirement.
3. **Regulatory:** no lawful, insured route exists in Latvia/EU for a private non-medical active implant;
   a body-mod artist is not a legitimate path and a surgeon has no device authorisation to rely on.
4. **MRI:** a facial magnet permanently complicates head/neck MRI [32][45].
5. **Reversibility:** glued/epidermal approaches can be iterated in a weekend; an implant cannot.

**If the owner insists on one implant, the least-bad ranking is:**

1. **Glued magnets on tongue/lips with a 12–15-channel magnetic sensor array** (no surgery at all;
   demonstrated >90% on 57 words [7][11]). This is the recommended first build.
2. If retention is the blocker, a **clinician-placed magnet under the oral mucosa** (inside the mouth,
   not the face), supervised by an oral/maxillofacial surgeon, on a named-patient custom-made-device
   basis. Accept the calculus/biofilm maintenance burden [43].
3. Nothing in the face. Not an NFC chip (useless for speech), not a subdermal magnet (MRI-incompatible,
   migrates, corrodes [36][45]), not an IMES-class device (no speech evidence, no approval [1][4]).

**With which professional:** for route 2, an **oral and maxillofacial surgeon** (or a dentist with
surgical privileges) in Latvia, working through the MDR custom-made-device route; not a piercer and not a
body-modification artist. For route 1, no clinician is needed.

---

## Sources

1. ClinicalTrials.gov, "Evaluation of the Phantom X Implantable EMG Sensor System for Myoelectric Prosthesis Control (CYBORG)", NCT07325708 — https://clinicaltrials.gov/api/v2/studies/NCT07325708 (registry entry; start 2026) 
2. Weir RF, Troyk PR, DeMichele GA, Kerns DA, Schorsch JF, Maas H. "Implantable myoelectric sensors (IMESs) for intramuscular electromyogram recording." IEEE Trans Biomed Eng. 2009;56(1):159–71 — https://pubmed.ncbi.nlm.nih.gov/19224729/ (2009)
3. Merrill DR, Lockhart J, Troyk PR, Weir RF, Hankin DL. "Development of an implantable myoelectric sensor for advanced prosthesis control." Artif Organs. 2011;35(3):249–52 — https://pubmed.ncbi.nlm.nih.gov/21371058/ (2011)
4. Pasquina PF et al. "First-in-man demonstration of a fully implanted myoelectric sensors system to control an advanced electromechanical prosthetic hand." J Neurosci Methods. 2015;244:85–93 — https://pubmed.ncbi.nlm.nih.gov/25102286/ (2015)
5. ClinicalTrials.gov, "Feasibility of Implantable Myoelectric Sensors to Control Upper Limb Prostheses", NCT01901081 — https://clinicaltrials.gov/api/v2/studies/NCT01901081 (2013–2016)
6. Earley EJ, Kristoffersen MB, Ortiz-Catalan M. "Comparing implantable epimysial and intramuscular electrodes for prosthetic control." Front Neurosci. 2025;19:1568212 — https://research.chalmers.se/publication/547425/file/547425_Fulltext.pdf (2025)
7. Hofe R, Ell SR, Fagan MJ, Gilbert JM, Green PD, Moore RK, Rybchenko SI. "Evaluation of a Silent Speech Interface Based on Magnetic Sensing." Interspeech 2010:246–249 — https://www.isca-archive.org/interspeech_2010/hofe10_interspeech.pdf (2010)
8. Hofe R et al. "Performance of the MVOCA Silent Speech Interface Across Multiple Speakers." Interspeech 2013:1140–1143 — https://www.isca-archive.org/interspeech_2013/hofe13_interspeech.pdf (2013)
9. Gonzalez JA, Cheah LA, Bai J, Ell SR, Gilbert JM, Moore RK, Green PD. "Analysis of Phonetic Similarity in a Silent Speech Interface based on Permanent Magnetic Articulography." Interspeech 2014:1018–1022 — https://www.isca-archive.org/interspeech_2014/gonzalez14_interspeech.pdf (2014)
10. Gonzalez JA et al. "A silent speech system based on permanent magnet articulography and direct synthesis." Computer Speech & Language. 2016;39:67–87 — https://eprints.whiterose.ac.uk/112036/1/csl2016.pdf (2016)
11. Gilbert JM, Rybchenko SI, Hofe R, Ell SR, Fagan MJ, Moore RK, Green P. "Isolated word recognition of silent speech using magnetic implants and sensors." Med Eng Phys. 2010;32(10):1189–97 — https://pubmed.ncbi.nlm.nih.gov/20863739/ (2010)
12. Gonzalez JA, Green PD, Murphy D, Gully A, Gilbert JM. "Silent Speech: Restoring the Power of Speech to People whose Larynx has been Removed." IberSPEECH 2018:163–167 — https://www.isca-archive.org/iberspeech_2018/gonzalezlopez18_iberspeech.pdf (2018)
13. US Patent US10283120B2, University of Hull — https://patents.google.com/patent/US10283120B2/en (2019)
14. Jowett N, Kearney RE, Knox CJ, Hadlock TA. "Toward the bionic face: a novel neuroprosthetic device for facial reanimation." Plast Reconstr Surg. 2019 — https://pmc.ncbi.nlm.nih.gov/articles/PMC6311722/ (2019)
15. Li Y, Huang S, Zealear D. "An implantable system for in vivo chronic electromyographic study in the larynx." Muscle Nerve. 2017;55(5):706–714 — https://pubmed.ncbi.nlm.nih.gov/27543847/ (2017)
16. Zealear D, Li Y, Huang S. "An Implantable System For Chronic In Vivo Electromyography." J Vis Exp. 2020 — https://pubmed.ncbi.nlm.nih.gov/32391811/ (2020)
17. Arnold D et al. "Selective zygomaticus muscle activation by ball electrodes in synkinetically reinnervated patients after facial paralysis." Front Rehabil Sci. 2023 — https://pubmed.ncbi.nlm.nih.gov/ (2023)
18. Gstoettner C et al. "Feasibility of a Wireless Implantable Multi-electrode System ...: Animal and Cadaver Study." Clin Orthop Relat Res. 2022 — https://pubmed.ncbi.nlm.nih.gov/ (2022)
19. Ripple Neuro, "Clinical Projects" — https://rippleneuro.com/clinical-projects/ (accessed 2026)
20. Morel P et al. "Long-term decoding of movement force and direction with a wireless myoelectric implant." J Neural Eng. 2016 — https://pubmed.ncbi.nlm.nih.gov/26643959/ (2016)
21. Bundesministerium für Bildung und Forschung, "MyoPlant" project page — https://www.interaktive-technologien.de/projekte/myoplant (2008–2014)
22. Schiffmann A, Clauss M, Honigmann P. "Biohackers and Self-Made Problems: Infection of an Implanted RFID/NFC Chip: A Case Report." JBJS Case Connect. 2020;10(2):e0399 — https://pubmed.ncbi.nlm.nih.gov/32649126/ (2020)
23. Dangerous Things, "xNT Chip Implant" product page — https://dangerousthings.com/product/xnt/ (accessed 2026)
24. FSRH, "Progestogen-only Implants" clinical guideline — https://www.fsrh.org/Common/Uploaded%20files/documents/fsrh-guideline-progestogen-only-implants.pdf (Feb 2021)
25. DailyMed, NEXPLANON (etonogestrel implant) label — https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=487f8a62-e142-457c-97cc-2e398fde7594 (accessed 2026)
26. Al-Jandan B, Marei HF. "Mandibular angle augmentation using solid silicone implants." Dent Med Probl. 2018;55(4):367–370 — https://dmp.umw.edu.pl/pdf/2018/55/4/issue.pdf (2018)
27. Rojas YA et al. "Facial Implants: Controversies and Criticism. A Comprehensive Review." Plast Reconstr Surg. 2018;142(4):991–999 — https://pubmed.ncbi.nlm.nih.gov/29994843/ (2018)
28. Walker TJ, Toriumi DM. "Analysis of Facial Implants for Bacterial Biofilm Formation Using Scanning Electron Microscopy." JAMA Facial Plast Surg. 2016;18(4):299–304 — https://pubmed.ncbi.nlm.nih.gov/27149574/ (2016)
29. Djurhuus BD et al. "Minimally invasive surgery for placement of a subcutaneous EEG implant." Front Surg. 2023;10:1304343 — https://www.frontiersin.org/journals/surgery/articles/10.3389/fsurg.2023.1304343 (2023)
30. Steinman H. "Facial Danger Zones in Mohs Surgery & Reconstruction." American Society for Mohs Surgery — https://asms.mohssurgery.org/files/papers/2017%20FMS/Facial%20Danger%20Zones%20Mohs%20course%20final%20revised%202017.pdf (2017)
31. Wedlich et al. "Cut with caution in cutaneous surgery." J Cutan Aesthet Surg (Article in Press) — https://jcasonline.com/content/173/2026/0/1/pdf/JCAS-276-2025.pdf (2026)
32. US FDA, "Testing and Labeling Medical Devices for Safety in the Magnetic Resonance (MR) Environment" — https://www.fda.gov/media/74201/download (2023)
33. El Sayed Omar et al. "MRI-induced soft tissue pain: incidental finding of a 15-year-old foreign body." BMJ Case Rep. 2013:bcr2012008275 — https://pmc.ncbi.nlm.nih.gov/articles/PMC3604481/ (2013)
34. Hacking C. "Subdermal magnet implant in finger." Radiopaedia case 67990 — https://radiopaedia.org/cases/subdermal-magnet-implant-in-finger (2019)
35. Robertson A. "I hacked my body for a future that never came." The Verge — https://www.theverge.com/2017/7/21/15999544/biohacking-finger-magnet-human-augmentation-loss (2017)
36. biohack.me forum, "Had to have my magnet removed" (2012) and "Brutal Magnet Removal" (2017) — https://forum.biohack.me/discussions/326 and https://forum.biohack.me/discussions/2038 (self-reported)
37. HumanAug Wiki, "A History of Magnet Implantation" — https://wiki.biohack.me/doku.php?id=a_history_of_magnet_implantation (2024)
38. US FDA De Novo DEN040007, Implantable Radiofrequency Transponder System (VeriChip / Digital Angel) — https://fda.innolitics.com/device/DEN040007 (decision 12 Oct 2004)
39. NSW Health Care Complaints Commission, Annual Report 2017–18 — http://www.hccc.nsw.gov.au/ArticleDocuments/75/Annual%20Report%202017-18%20Chapters.pdf.aspx (2018)
40. Association of Professional Piercers, Procedure Manual, 2013 Edition — https://safepiercing.org/wp-content/uploads/2020/10/APP_Procedures_2013_A_Web.pdf (2013)
41. Powerhouse Collection, "'Northstar V1' and 'Grindhouse V1 P2' subdermal LED light implants", object 2019/27/2 — https://collection.powerhouse.com.au/object/562945 (2019)
42. Huo X, Cheng J, Ghovanloo M. "Evaluation of the Tongue Drive System by Individuals with High-Level Spinal Cord Injury." IEEE EMBC 2009:555–558 — https://pmc.ncbi.nlm.nih.gov/articles/PMC4467691/ (2009)
43. Minocha JS et al. "Development of a Tongue-Piercing Method for Use With Assistive Technology." JAMA Dermatol. 2014;150(4):453–454 — https://pmc.ncbi.nlm.nih.gov/articles/PMC4445083/ (2014)
44. Mimche S et al. "Tongue implant for assistive technologies." Arch Oral Biol. 2016;71:1–9 — https://open.library.emory.edu/downloads/ae939d08-656f-4301-8277-4804eb64d532 (2016)
45. Dangerous Things, "xG3 Injectable Biomagnet" product page — https://dangerousthings.com/product/xG3/ (accessed 2026)
46. Composite source for needle/subdermal EMG practice and complications: IMES technical details (Weir et al.); Caldwell CW, Reswick JB, "A percutaneous wire electrode for chronic research use", IEEE TBME 1975; intraoperative needle-EMG practice (IntraNerve IONM FAQ, https://www.intranerve.com/solutions/ionm-faq/); Lynch SL et al., "Complications of needle electromyography: hematoma risk", Muscle Nerve 2008; Gruis KL et al., "Survey of electrodiagnostic laboratories regarding hemorrhagic complications from needle EMG", Muscle Nerve 2006; CMAJ 2000, "An outbreak of hepatitis B associated with reusable subdermal electroencephalogram electrodes" (1975–2008)
47. Regulation (EU) 2017/745 (MDR), Article 2 (definitions), adopted text — https://www.legislation.gov.uk/eur/2017/745/article/2/adopted (2017)
48. Regulation (EU) 2017/745 (MDR), Article 5 (in-house exemption), adopted text — https://www.legislation.gov.uk/eur/2017/745/article/5/adopted (2017)
49. Regulation (EU) 2017/745 (MDR), Articles 1, 10, 20, 21, 52, 62, 82 — https://www.legislation.gov.uk/eur/2017/745/article/52/adopted and https://meddeviceguide.com/regulations/eu-mdr/clinical (2017)
50. Regulation (EU) 2017/745 (MDR), Annex XVI (products without an intended medical purpose), adopted text — https://www.legislation.gov.uk/eur/2017/745/annex/XVI/adopted (2017)
51. MDCG 2023-1, "Guidance on the health institution exemption under Article 5(5) of Regulation (EU) 2017/745 and 2017/746" — https://health.ec.europa.eu/system/files/2023-01/mdcg_2023-1_en.pdf (Jan 2023)
52. MDCG 2021-24, "Guidance on classification of medical devices" — https://health.ec.europa.eu/system/files/2021-10/mdcg_2021-24_en_0.pdf (Oct 2021)
53. Ārstniecības likums (Latvian Medical Treatment Law), Arts 1, 12, 26, 34–36 — https://likumi.lv/ta/id/44108-arstniecibas-likums (1997, as amended 2025)
54. Ministru kabineta noteikumi Nr. 693, "Kārtība, kādā skaistumkopšanas un tetovēšanas pakalpojumu sniedzēji paziņo par saimnieciskās darbības uzsākšanu" — https://likumi.lv/ta/id/278396 (8 Dec 2015)
55. "Evaluatie Warenwetbesluit tatoeëren en piercen", Research voor Beleid for the Dutch Ministry of Health — https://zoek.officielebekendmakingen.nl/blg-170769.pdf (2011)
56. R v Crimi-Appleby and others, Court of Appeal (Criminal Division), England and Wales — https://www.judiciary.uk/wp-content/uploads/2025/04/FINAL-JUDGMENT-REX-V-CRIMI-APPLEBY-AND-OTHS-202400381-A1.pdf (2025)
57. Regulation (EU) 2024/1689 (AI Act), Article 6 and Annex I — https://artificialintelligenceact.eu/article/6/ and https://artificialintelligenceact.eu/annex/1/ (2024)
58. Veselības inspekcija (Latvian Health Inspectorate), "Medicīnas ierīces" and hygiene requirements pages — https://www.vi.gov.lv/lv/medicinas-ierices (accessed 2026)
59. Hargrove LJ, Englehart K, Hudgins B. "A comparison of surface and intramuscular myoelectric signal classification." IEEE Trans Biomed Eng. 2007;54(5):847–53 — https://pubmed.ncbi.nlm.nih.gov/17518281/ (2007)
60. Farrell TR, Weir RF. "A comparison of the effects of electrode implantation and targeting on pattern classification accuracy for prosthesis control." IEEE Trans Biomed Eng. 2008;55(9):2198–211 — https://pubmed.ncbi.nlm.nih.gov/18713689/ (2008)
61. Wallace DM et al. "Regenerative peripheral nerve interfaces (RPNIs) and implanted electrodes improve online control of prostheses for hand and wrist." J Neural Eng. 2026;23:016020 — https://doi.org/10.1088/1741-2552/ae36d2 (2026)
62. Salminger S et al. "Long-term implant of intramuscular sensors and nerve transfers for wireless control of robotic arms in above-elbow amputees." Sci Robot. 2019;4(32):eaaw6306 — https://doi.org/10.1126/scirobotics.aaw6306 (2019)
63. Jaguś D, Pawłowska A, Mlosek RK. "Ultrasound Evaluation of Upper Facial Muscles to Guide Botulinum Toxin Application." Toxins. 2025;17(12):595 — https://doi.org/10.3390/toxins17120595 (2025)
64. Urso SU et al. "Determining the Position, Morphology, and Location of the Depressor Anguli Muscle Through Ultrasound in the Caucasian Population." Aesthet Surg J Open Forum (2026) — https://doi.org/10.1093/asjof/ojag091 (2026)
65. Kuiken TA, Lowery MM, Stoykov NS. "The effect of subcutaneous fat on myoelectric signal amplitude and cross-talk." Prosthet Orthot Int. 2003;27(1):48–54 — https://doi.org/10.3109/03093640309167976 (2003)
66. Nordander C et al. "Influence of the subcutaneous fat layer, as measured by ultrasound, skinfold calipers and BMI, on the EMG amplitude." Eur J Appl Physiol. 2003;89(6):514–519 — https://doi.org/10.1007/s00421-003-0819-1 (2003)
67. Wu WT et al. "Ultrasound Imaging of the Facial Muscles and Relevance with Botulinum Toxin Injections: A Pictorial Essay and Narrative Review." Toxins. 2022;14(2):101 — https://doi.org/10.3390/toxins14020101 (2022)
68. Salomons I, del Blanco E, Navas E, Hernáez I. "Electrode Setup for Electromyography-Based Silent Speech Interfaces: A Pilot Study." Sensors. 2025;25(3):781 — https://doi.org/10.3390/s25030781 (2025)
69. Hernáez I et al. "ReSSInt project: Voice Restoration using Silent Speech Interfaces." IberSPEECH 2022 — https://www.isca-archive.org/iberspeech_2022/hernaez22_iberspeech.pdf (2022)
70. Kaushal NK et al. "Noninvasive Speech Restoration After Total Laryngectomy Using Surface Electromyography: Pilot Study." Laryngoscope Investig Otolaryngol (2026) — https://doi.org/10.1002/lio2.70559 (2026)
71. Muceli S, Merletti R. "Tutorial. Frequency analysis of the surface EMG signal: Best practices." J Electromyogr Kinesiol. 2024;79:102937 — https://doi.org/10.1016/j.jelekin.2024.102937 (2024)
72. Gonzalez-Lopez JA et al. "Silent Speech Interfaces for Speech Restoration: A Review." arXiv:2009.02110 — https://arxiv.org/abs/2009.02110 (2020)
73. Denby B et al. "Silent Speech Interfaces." Speech Communication. 2010;52(4):270–287 — https://www.neurones.espci.fr/Articles_PS/SPEECH_COM_VERSION_WEB.pdf (2010)
74. Tang C et al. "Sensing technologies for silent speech interfaces." Nature Sensors. 2026;1:16–26 — https://doi.org/10.1038/s44460-025-00010-2 (2026)
75. MIT Media Lab, "AlterEgo: Frequently Asked Questions" — https://www.media.mit.edu/projects/alterego/frequently-asked-questions/ (accessed 2026)
76. Cui J et al. "Acute to long-term characteristics of impedance recordings during neurostimulation in humans." J Neural Eng (2024) — https://doi.org/10.1088/1741-2552/ad3416 (2024)
77. Bublitz C et al. "A Moratorium on Implantable Non-Medical Neurotech Until Effects on the Mind are Properly Understood." Neuroethics. 2025;18(3):46 — https://doi.org/10.1007/s12152-025-09612-6 (2025)

## Key takeaways for the build

1. **Do not implant anything yet.** No implant route beats concealed epidermal/glued electrodes for
   signal, and every useful site adds facial-nerve and MRI risk [6][9][30][45].
2. **Build the glued-magnet PMA path first** (4 lip magnets + 2–3 tongue magnets, 12–15 magnetic
   channels): it is the only silent-speech modality with >90% on a 57-word vocabulary, and it needs no
   surgery [7][8][11].
3. **Expect PMA's information ceiling:** it nails place of articulation but loses voicing and manner of
   articulation (voiced/unvoiced KL divergence 0.90 audio vs 0.20 PMA) [9]. Fuse it with a second
   modality (surface EMG submental, or audio of the whisper) rather than expecting PMA alone to scale.
4. **If an implant is ever considered, the mouth — not the face — is the only defensible site**, placed
   by an oral/maxillofacial surgeon under the MDR custom-made-device route, because the face contains
   the marginal mandibular and buccal nerve branches [30][31].
5. **Implanted EMG is a limb technology.** IMES/Phantom X are transradial-amputation devices; Phantom X
   is a 10-person first-in-human arm study that only began 2026-04-17 and excludes anyone who may need an
   MRI [1][4][5].
6. **Any intra-oral magnet will demand maintenance** — calculus formed in all 6 completed tongue-piercing
   subjects by week 4 [43].
7. **Never put a permanent magnet in the body without accepting MRI loss**: vendor warnings and FDA rules
   are explicit that magnets are MRI-incompatible [32][45].
8. **Body-mod artists are not a lawful implant route for a medical device**; the industry's own devices
   are uncertified "at your own risk" products and its standards body excludes implants [23][40].
9. **Budget the alternative:** the entire implant question exists to hide an electrode. A concealed
   epidermal array costs a few hundred euros and a weekend; an implant costs surgery, an MRI exclusion,
   and a regulatory dead end.
10. **Revisit only if glued magnets prove unworkable** (retention failure, not accuracy failure) — then
    and only then is a clinician-placed oral magnet worth a conversation.

## Open questions

1. Is there any 2024–2026 registered trial of an implantable EMG device for **facial or speech** muscles?
   (Searched; none found as of late 2026.)
2. What are the real, quantified long-term complication rates of body-modification NFC/RFID implants at
   5–10 years? No published cohort exists.
3. Can a magnet under the **oral mucosa** be imaged/retained safely without calculus, and does it change
   PMA accuracy at all? No data found.
4. What is the exact Latvian legal status of a *non-medical* active implant, and could a named-patient
   custom-made device be obtained for a personal R&D project? The MDR route exists (Art 52(8),
   Annex XIII, notified body for a class III custom implantable) [47][49][51], but no Latvian guidance or
   precedent was found — this remains open.
5. Would a submental **high-density surface EMG** array plus PMA match an implanted system closely enough
   that the implant question disappears? Needs a head-to-head experiment, which this project can run.
6. Is there any evidence that fibrous encapsulation changes EMG frequency content (not just amplitude)
   in a way that affects speech decoding? Not found.
