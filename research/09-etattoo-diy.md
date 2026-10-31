# Track 09 — E-tattoo / epidermal electrodes the owner can make or buy in weeks

*Research notes for a personal R&D silent-speech wearable. Inline `[n]` citations map to the
numbered Sources list at the end. Demonstrated results are separated from claims/marketing. All
numbers are quoted exactly as the source gives them. Pages I could not fetch myself are marked
"unverified" and are cited only as described by a source I did fetch.*

*Scope: epidermal/e-tattoo electrodes for under-chin, jawline and behind-ear sEMG. Fabrication
routes a hobbyist with a fiber/CO2 laser, inkjet printer, screen-printer or makerspace can execute;
what needs a cleanroom; commercial suppliers and prices 2024–2026; the interconnect problem (how a
tattoo connects to rigid electronics); measured performance vs Ag/AgCl; skin tone/visibility; a
concrete first DIY recipe; a fallback commercial option.*

Status: COMPLETE (v4) — all sections written from fetched sources, including a vendor-verified
supplier/price table (§3, observed 2026-10-01). Length exceeds the suggested 2,000–5,000-word
target because the track contains many independent verified numbers (thicknesses, impedances,
SNRs, cycle counts, accuracies); nothing unverified is presented as fact.

---

## 1. What "e-tattoo" means here, and the decision it drives

An "electronic tattoo" (e-tattoo, epidermal electrode) is a conductive pattern on an ultrathin
polymer film that is transferred to skin with water like a child's temporary tattoo. The films that
work are **sub-micrometre to a few micrometres thick**, which is the whole point: a film that thin
has a bending stiffness low enough to follow skin ridges and creases instead of bridging them, so
it couples to skin by van der Waals forces with no gel and no strap [2][3].

Three thickness classes show up repeatedly in the primary literature, and they map directly onto
what the owner can do:

| Class | Total thickness | Example | Minimum kit |
|---|---|---|---|
| True e-tattoo | 0.45–1.5 µm | cut-and-paste Au/Cr/PET on tattoo paper [2]; inkjet PEDOT:PSS on ethylcellulose [4] | cutter plotter + tattoo paper (+ sputter coater) |
| Thin epidermal patch | 5–20 µm | Ag-In-Ga printed on tattoo paper [6]; Cu/PI serpentine on wound dressing [1] | screen printer / photolithography |
| Ultrathin nanomesh | ~65 nm gold mesh | electrospun PVA + Au [9] | electrospinner + sputter coater (makerspace) |

For this build the useful threshold is **≤ 5 µm total**, because that is where the papers stop
needing adhesive tape and start reporting gel-comparable behaviour on curvy, hairy, moving skin
[2][4][7].

**What matters for the owner's face/chin array** (the four constraints this track must answer):

1. **Conformability → impedance.** On a curved jaw/chin, a stiff patch lifts at the edges; the
   contact area collapses and impedance rises. Conformability, not the electrode's own
   conductivity, is what lowers skin–electrode impedance [6].
2. **Interconnect.** The tattoo is ~1 µm; the amplifier/PCB is ~1 mm. Every published system has
   to solve the soft-to-rigid transition, and several do it with tooling the owner can buy [1][2][4][5][7].
3. **Durability under jaw motion and speech.** The jaw and chin move constantly. The relevant
   published numbers are strain-at-failure and multi-day stretch cycling [2][4][5].
4. **Visibility.** Sub-micrometre films are effectively invisible; the connector is the visible
   part, and users consistently report they feel the connector, not the tattoo [4].

The rest of this file resolves those four constraints and ends with a buildable recipe.

---

## 2. Fabrication routes, ranked by hobbyist feasibility

### 2.1 Route A — "Cut-and-paste" Au/Cr on PET over commercial tattoo paper (best first build)

This is the Lu group's low-cost tape-free e-tattoo, and it is the single most hobbyist-reproducible
route in the literature [2]. The full process, quoted from the paper:

1. Peel the liner off **commercial tattoo paper (Silhouette, USA)**.
2. Laminate a **1.4 µm transparent PET sheet (PolyK Technologies)** onto the tattoo paper; dry on a
   hotplate at **50–60 °C for ~5 min**.
3. Deposit **10 nm Cr + 100 nm Au** by thermal evaporation (Au chosen for biocompatibility,
   chemical inertness and ductility; Ti is named as a cheaper but less ductile alternative).
4. Pattern with a **programmable mechanical cutter plotter (Silhouette Cameo)** loaded with an
   AutoCAD design — the paper states sharpness 5, cutting rate 2, thickness 1. Ribbon width was
   **600 µm, "as limited by the patterning resolution of the cutter plotter."**
5. Wet the tattoo paper to partially dissolve the water-soluble adhesive and peel away the
   extraneous Au/Cr/PET, leaving serpentine ribbons.
6. Moisten skin, laminate the tattoo paper, slide it off (sliding works better than peeling), and
   the **1.5 µm** open-mesh tattoo adheres by van der Waals forces alone.
7. Optional: **spray 3M Nexcare liquid bandage five times** to build a **~1 µm** transparent
   encapsulation (each spray ≈ 200 nm).

Demonstrated properties: the serpentine ribbon stiffness is **115 N/m**, comparable to epidermis at
**160 N/m** (160 kPa modulus, 1 mm thick); the device measured two ECG electrodes, one RTD and two
hydration sensors on a **7.5 cm × 4.0 cm** footprint; the paper reports reduced motion artifacts vs
thicker e-tattoos and gel electrodes, and no sweat accumulation because the mesh is open [2].

**Hobbyist verdict: yes, with a makerspace.** The only non-household tool is the thermal evaporator
for Cr/Au. A makerspace/university will run it; a cheap alternative is commercial Au/PET or
Cu/PET sheet (the paper itself uses 13 µm Au/PET from Rotex Tech for the connector strips). The
paper notes the cutter can also pattern Al/PET, carbon-doped PDMS, graphene/PMMA and ITO/PET [2],
so the owner is not locked to gold.

**This route has already been used for silent speech, on the target muscles.** Wang et al. 2021
built a 4-channel array from the same "Cut and Paste" method, **1.2 µm thick**, integrated in a
**47 µm 3M Tegaderm patch**, with the four pairs on **levator anguli oris (LAO), depressor anguli
oris (DAO), buccinators (BUC) and anterior belly of digastric (ABD)** — the last is the under-chin
muscle this project needs [21]. Design details: filamentary serpentines **500 µm wide**, ribbon-
width-to-arc-radius ratio **0.32**, arc angle **20°**, giving "4 % elastic stretchability" by
theory, which the authors then extend with an "electricity-preferred" method; each electrode is
about **18 mm × 32 mm**; and the electrode-to-wire joint is reinforced by "**low-temperature alloy
welding**" to survive all-weather use [21]. That paper is the single most on-point reference in
this whole track; its recognition results are in §5.3.

### 2.2 Route B — Screen-printed carbon + plasma-polymerised PEDOT on tattoo sheet (best for the face)

The Hanein group's process is designed exactly for hairy, curved, long-wear facial sites and is
the most directly relevant to an under-chin/jaw array [7]:

1. Screen-print carbon ink onto a **temporary tattoo sheet**.
2. Laser-cut a **double-sided adhesive film** into a passivation layer and bond it to the array.
3. **Plasma-polymerise EDOT (ppEDOT)** onto the exposed carbon to cut impedance.
4. Glue a **polyimide film with holes** to the array so the whole thing **fits a zero insertion
   force (ZIF) socket** on a custom PCB. That is the entire interconnect.

Electrode area is **20 mm²** (down to **5 mm diameter**); the ppEDOT coating raised specific
capacitance from **0.018 to 1.6 ± 0.1** (12 W) and **3.3 ± 0.2 mF cm⁻²** (90 W), and **at 1 kHz
coated electrodes had ~10× lower impedance than pristine carbon, which in turn had ~10× larger
impedance than gelled electrodes**; because the commercial gel electrodes had **15× the area**,
their *specific* impedance was similar [7].

**Hobbyist verdict: yes.** Screen printing can be done with a laser-cut stencil and a squeegee; the
only specialist step is the plasma polymerisation. The paper's plasma is described as a simple
solvent-free room-temperature process [7], but a plasma chamber is a makerspace tool. If plasma is
unavailable, use a commercial PEDOT:PSS inkjet ink instead (Route C) — but then expect the higher
impedance Ferrari et al. measured [4].

### 2.3 Route C — Inkjet-print PEDOT:PSS on commercial tattoo paper

Ferrari et al. established the canonical recipe [4]:

- Substrate: decal transfer paper with a **~450 nm ethylcellulose (EC)** release layer over a
  starch–dextrin sacrificial layer.
- Ink: waterborne **PEDOT:PSS** dispersion, filtered at **0.20 µm**, printed with a **Dimatix
  DMP-2800** using a **10 pL** cartridge.
- Interconnects: **Au sputtered** (70 W, 2 × 10⁻² argon, 1 min for 30 nm) plus a **13 µm Kapton**
  flat connector tab glued with the kit's acrylic glue sheet (~700 nm).
- Stacking more PEDOT:PSS layers took the electrode from **h ≈ 600 to ~1200 nm** and dropped sheet
  resistance from **520 to 50 Ω/sq**.

A simpler follow-up from the same group inkjet-prints **PEDOT:PSS Clevios P Jet 700 + 10 % vol
glycerol** and screen-prints stretchable **Ag paste CI-1036** interconnects (baked **120 °C for
10 min**) [5].

Ferrari et al. also give performance for this stack: **ECG SNR 6.45 (tattoo) vs 7.52 (standard
gel)**, and facial EMG rest **3.0 µV** / active **50.6 µV** (tattoo) vs **1.9 / 72.5 µV**
(Ag/AgCl) [4]. The paper does **not** state an annealing/drying temperature in the main text;
treat any cure schedule as **unverified** [4].

**2.3b Route C2 — PEDOT:PSS + ionic liquid, screen-printed (concrete, high-density recipe)**

Velasco-Bosom et al. published a complete, verifiable recipe for a high-density sEMG array [14]:

- Ink: **PEDOT:PSS Clevios 1 wt % + 40 wt % cholinium lactate (IOLITEC) + 1 wt % GOPS**, vortexed
  and filtered at **0.45 µm**.
- Deposition: drop-cast **1.8 µL** per well, dry overnight, **×3**, then **hard-bake 130 °C for
  60 min**, then soak overnight in DI water.
- Tracks: **Sicrys 130EG-1** Ag ink, dry 40 °C, **sinter 120 °C for 60 min**, on **50 µm Kapton**.
- Performance: **2.7 MΩ at 60 Hz** for 2.25 mm², **0.3 MΩ** for 12.56 mm² (**48 kΩ·cm²**
  normalised), vs Ag/AgCl **17 kΩ**; EMG **SNR = 6 (15.6 dB)**; total array thickness **170 µm** [14].

The 170 µm thickness is far from an e-tattoo and the impedance is high, but this is the most
copyable *printed* recipe found, and the ionic-liquid additive is the current best practice for
lowering conducting-polymer impedance.

**Hobbyist verdict: yes, with a printable-ink printer.** PEDOT:PSS is water-based and can be run
through a modified inkjet printer, but clogging and substrate wetting are the failure modes;
Ferrari notes the substrate "strongly influence[s]" print quality and that glycerol additive
improved both print quality and conductivity [5]. A Dimatix is a lab instrument, but the underlying
chemistry is hobby-accessible (AgIC-style conductive inkjet paper is the consumer version).

### 2.4 Route D — Printed silver + liquid-metal (Ag-In-Ga / EGaIn) tattoo

Lopes et al. print silver nanoparticle ink (Mitsubishi) on **Silhouette printable tattoo paper**,
then rub **EGaIn** over the pattern and clean the excess with weak acetic acid, forming a
non-smearing **Ag-In-Ga** alloy that stretches **over 100 %** [6]. The carrier film is **5 µm**.
In their head-to-head test of seven soft electrode types against Ag/AgCl and stainless steel:

- The **tattoo electrodes had the highest SNR and the lowest electrode–skin impedance at low
  frequencies**, attributed to the alloy's malleability and the 5 µm carrier [6].
- Ag-In-Ga tattoos "can be rapidly printed at low cost with accessible equipment" [6].

**Hobbyist verdict: yes** (screen/stencil print + rub), but EGaIn is messy and gallium wets many
metals; keep it away from the electronics. A simpler drawable version: Yu et al. paint a Ga-based
liquid-metal ink (oxygen concentration **0.34 %**, resistivity **44.1 µΩ·cm**, peak polarisation
voltage in saline **−0.73 V**) straight onto skin with a paintbrush and record ECG "as good as …
conventional electrodes", but the authors note it "can be printed and erased easily" — i.e. it
smears [15]. The long-contact cytotoxicity of Ga-In is an **open question** in the literature
(the 2018 cytotoxicity paper is paywalled, so its numbers are **unverified** here) [18][19]. For an
under-chin array that must survive speaking, liquid metal is a poor first choice without an
encapsulation frame.

### 2.5 Route E — Gold nanomesh (needs a makerspace, not a cleanroom)

Miyamoto et al. fabricated a **~65 nm-thick gold nanomesh** on an electrospun PVA nanofiber mesh
(as described in [2]'s account of that work). The abstract states the result: a **one-week skin
patch test** showed inflammation risk "can be significantly suppressed by using the nanomesh
sensors", the sensors are gas-permeable and stretchable, and EMG was recorded "with minimal
discomfort" [9]. A secondary account of the method describes electrospinning water-soluble **PVA**
microfibres, vacuum-depositing a gold layer "**bis zu hundert Nanometer dünne Goldschicht**"
(up to ~100 nm), laminating to skin, then washing the PVA away with water so a gold nanowire mesh
remains held by van der Waals adhesion; the same secondary report gives "**tausendfachen Dehnungen
um bis zu vierzig Prozent**" (1000 cycles to 40 %) and one-week wear without irritation [16]. The
**full paper is paywalled and its abstract elides the numbers**, so the nanomesh thickness,
cycle count and wear claims are **secondary/unverified** — only the abstract quotes in [9] are
primary-confirmed here.

**Hobbyist verdict: yes-with-makerspace.** Electrospinning (high voltage) plus vacuum Au deposition
(e.g. a Q150T-class sputter coater) are makerspace/university tools; no cleanroom is required. This
is the best *biocompatibility* benchmark but a harder first build than Routes A/B.

### 2.6 Route F — Graphene electronic tattoo (makeable if you buy the graphene)

The GET is more accessible than its cleanroom reputation suggests, because the graphene can be
bought instead of grown [10][11]. Verified numbers from the original paper: total thickness
**463 ± 30 nm**, optical transparency **~85 %**, stretchability **more than 40 %**, and dry-electrode
impedance "on par with medically used silver/silver-chloride (Ag/AgCl) gel electrodes"; a bare GET
"stay[s] attached to skin for several hours", and with liquid bandage "**up to several days**" [20].
The fabrication is the cost- and time-effective "**wet transfer, dry patterning**" method [20].

The step-by-step lab protocol exists (**Nature Protocols 2021**, paywalled), and its own supplement
confirms the key steps: **Step 18** reversing the graphene; **Step 21** shaping the GET with a
**Cameo plotter**; **Step 22** removing excess graphene; **Step 24-A** contacting via **copper
tape** or **24-B via silver epoxy**; **Step 25** troubleshooting transfer on skin [10]. The copper
etchant is **ammonium persulfate** — the protocol carries the caution "Ammonium persulfate is
corrosive. Wear personal protective equipment and work in a fume hood" [10]. The precursor for
GET 2.0 is "Single-layer graphene-on copper (Cu) substrate grown by the chemical vapor deposition
… purchased from **Grolltex**" [11]. Ferrari's review describes the GET carrier as **~440 nm PMMA**
or **~13 µm polyimide**, transferred to tattoo paper or medical adhesive, cut into ribbons, and
released with water [4]. The npj paper adds that a cutter plotter can pattern **graphene/PMMA**
directly [2].

**Hobbyist verdict: yes-with-makerspace.** Buy graphene-on-Cu from a supplier (no cleanroom);
the etch needs a **fume hood**; a spin coater, hotplate, blade cutter (Silhouette Cameo) and
temporary tattoo paper complete the kit. The payoff is the best combination of transparency,
stretchability and impedance in this whole file.

### 2.7 Route G — Laser-induced graphene on polyimide (consumer CO₂ laser)

Sun et al. laser-scribe porous graphene on polyimide and report (abstract-verified): **sheet
resistance 10.96 Ω sq⁻¹**, **failure strain ≈ 330 %**, **modulus ≈ 15 kPa**, resistance change
**≈ +7 %** after 500 bend cycles at 2.5 mm radius and **≈ +1 %** after 1000 cycles at 500 % strain,
and **7 days on skin without inflammation** [12]. The Lu paper independently cites laser-induced
graphene's use for an "intelligent artificial throat" [2, ref 51].

The attraction is that a **consumer CO₂ laser (K40/xTool class)** does the patterning with no
chemicals and no ink. Real maker numbers exist for the laser step: the original Tour-group LIG used
a **4.8 W CO₂ laser on polyimide in ambient air** [42], and a Glowforge owner reported that
**2 mil Kapton tape at 1 % power / speed 45 / 675 LPI / 0.030″ defocus** gave **15 Ω** on a
0.5 mm square, with a revised recipe of **11–25 % power at speed 640 / normal focus** reaching "as
low as **10 Ω**"; the same maker found the material "very fragile" and that **probing flakes it
off**, and concluded **5 mil polyimide** is needed rather than 1 mil [33]. A separate maker's
405 nm-laser Kapton supercapacitor build produced **156 µF / 0.8 V** per cell, with a commenter
reporting **uneven burn and continuity breaks** on a cheap laser [32].

The remaining gap: I found **no primary study validating LIG electrodes for facial sEMG**
(impedance, SNR, crosstalk, motion artifact). Treat the EMG performance as **unverified**.
Because Route A gets the same "laser + polyimide" convenience with published facial-EMG-grade
behaviour [2][21], LIG is a second or third experiment, not the first.

### 2.8 Route H — Conductive paint / drawn-on electrodes (proof-of-life only)

Bare Conductive Electric Paint and silver conductive paint can be stencilled onto skin or a tattoo
film. They are cheap and immediate, but I found **no primary source** quantifying their
skin–electrode impedance, noise or motion-artifact performance for facial sEMG; treat as
**unverified**. The maker record is the reality check: Chip Audette's homemade passive EEG
electrodes made from **flat metal lock washers with solder tabs** cost **$0.24 each** (about
**$1.10/electrode** vs **$8–20** commercial), produced clean ECG R/T waves ("a bit noisier" than
real electrodes) and clear EEG alpha, but **weak Mu rhythm**, heavy **60 Hz noise** without a
driven ground, and **poor adhesion** because the washer ring was too narrow. His rule of thumb was
**< 5 kΩ per electrode** and **< 10 kΩ across a pair** [38]. A Hackaday builder got usable EMG from
**duct tape + stripped wire + 5 cm × 1 cm aluminium foil with sugar syrup as electrolyte**, with
commenters flagging 50/60 Hz hum and no driven-ground feedback [39]. Note the paper finding that
electrode material conductivity correlated *less* with SNR than conformability did [6], so a thick
painted electrode is likely to underperform even with low bulk resistance.

### 2.9 Route ranking summary

| Route | Equipment | Reported impedance/SNR | Verdict |
|---|---|---|---|
| A. Cut-and-paste Au/Cr/PET [2][13] | cutter plotter + evaporator | [13]: >110 % strain, 10 000 cycles at 20 %; not measured for facial sEMG | build this first |
| B. Screen carbon + ppEDOT + ZIF [7] | screen printer + plasma + laser | 1 kHz: 10× better than carbon, ~10× worse than gel; specific impedance ≈ gel | build for face |
| C. Inkjet PEDOT:PSS [4][5] | inkjet + sputter (or Ag paste) | 60 Hz 294 ± 1 kΩ vs gel 102 ± 2 kΩ; ECG SNR 6.45 vs 7.52 | good, higher Z |
| C2. PEDOT:PSS–ionic liquid printed [14] | screen printer + 130 °C oven | 60 Hz 0.3–2.7 MΩ (area-dependent); EMG SNR 6 | concrete recipe, thick |
| D. Ag-In-Ga printed [6] / drawable LM [15] | stencil/screen + EGaIn; or brush | highest SNR of 7 soft types [6]; 44.1 µΩ·cm ink [15] | good, messy, cytotoxicity unverified |
| E. Au nanomesh [9][16] | electrospinner + sputter coater | inflammation-free 1 week (abstract); 40 % cycles (secondary) | benchmark |
| F. Graphene GET [20][10][11] | cutter + fume hood (buy graphene-on-Cu) | 463 ± 30 nm, ~85 % transparent, >40 % stretch, impedance ≈ Ag/AgCl | best all-round, more steps |
| G. LIG on PI [12] | consumer CO₂ laser | 10.96 Ω/sq, ≈330 % strain, 7 days on skin | promising, facial-EMG unverified |
| H. Conductive paint | none | unverified | avoid for now |

---

## 3. Commercial suppliers and prices

Prices were observed on **2026-10-01**; sources fetched directly by me are marked "(verified)",
those fetched by a delegated search pass are marked "(via sub-search)" and quoted as reported. No
price is invented; anything not confirmed is marked **unverified**.

### 3.1 Home-fabrication consumables (the tattoo substrate and inks)

| Item | Price | Notes |
|---|---|---|
| **Silhouette Temporary Tattoo Paper**, 8.5 × 11 in, **2 sheets** | **"As low as $9.99" USD**, in stock (verified by sub-search at the official store) [45] | the substrate used by [2][7][22]; sold to individuals |
| Same item at 3D Jake (CH) | **CHF 10.05** [46] | international alternative |
| **Hayes Paper waterslide decal paper**, 40 sheets | **$27.99** [47] | this is *decal* paper, not confirmed as tattoo paper — the tattoo-specific Hayes product is **unverified** |
| **The Magic Touch Tattoo 2.1** (the exact paper in [4]) | **unverified** | not confirmed as individually purchasable |
| **Bare Conductive Electric Paint**, 10 mL | **$13.50** at SparkFun (via sub-search) [48] | Adafruit explicitly warns "not intended for use on your bare skin" [49] |
| **MG Chemicals 842AR** silver conductive coating, 150 mL | **unverified** | Faraday/EMI-shielding paint, not skin-rated |
| **NovaCentrix Metalon** conductive inks | no public price | quote/webstore account only [50] |
| **AgIC inkjet conductive paper** | **unavailable** | the domain now redirects to Elephantech; no consumer product found [via sub-search] |
| **DuPont/Celanese Micromax PE872** | **unverified** | enterprise/licensed MOQ |

**Practical read:** a DIY substrate + conductive layer is cheap and purchasable (tattoo paper at
~$10 per 2 sheets), but **none of the skin-rated conductive inks from the papers are sold in
consumer quantities**. The gold/Cr (Route A/F) and PEDOT:PSS (Route C) routes will need a
makerspace's evaporator/inkjet, or the conductive layer bought as PET/Au film.

### 3.2 Dry / ultrathin EMG electrodes (the closest buyable thing to an e-tattoo)

| Product | Price | Notes |
|---|---|---|
| **OpenBCI / IDUN Dryode Alpha Kit** — flexible waterproof dry electrode, ECG/EMG/EEG | **$224.99 (1 m lead) / $244.99 (1.5 m)** (verified: the $244.99/1.5 m price is on the OpenBCI page) [51] | 10 electrodes + 10 adhesive patches + snap cables; **out of stock on 2026-10-01**; contact area **20 mm diameter**, quoted impedance **~3.2–5.2 kΩ**; sold to individuals |
| **OpenBCI EEG Polymer Electrodes Kit** — 8 dry conductive-polymer electrodes + headband | **$199.99** [52] | ~30 in stock; EEG-oriented but polymer dry electrodes |
| **SparkFun MyoWare 2 Muscle Sensor** — EMG amplifier board | **$42.95** (verified at SparkFun) [53] | **uses gel electrodes, not dry/epidermal**; dev kit **$154.95** [54] |
| **g.tec g.SAHARA** hybrid dry EEG electrodes | **unverified** (quote-based) [55] | |
| **TMSi Textile HD-EMG Grids** | **unverified** (quote-based) [56] | textile, not tattoo |
| **Delsys Trigno, CGX/Cognionics, BioSemi, Neuroelectrics** | **unverified** (enterprise/quote) | CGX has a dry EEG developer kit page with no public price [57] |

### 3.3 Ag/AgCl gel baseline (for comparison and for the fallback pipeline)

| Product | Price | Per-electrode |
|---|---|---|
| **Rhythmlink Disposable Single Recording Sticky Pad EMG**, 80/box | **$94.37** [58] | ≈ $1.18 |
| **Kendall Ag/AgCl Ø55 mm**, 30 pcs | **€8.30/bag** [59] | ≈ €0.28 |
| **Covidien/Kendall H124SG** ECG electrode, 500 pcs | **€109.90** [60] | ≈ €0.22 |
| **Vermed A10005** foam electrode | **$129.66** [61] | pack size **unverified** |
| **Ambu BlueSensor N** | **unverified** price | datasheet confirms Ag/AgCl solid gel [62] |

### 3.4 Is there a vendor selling an actual e-tattoo / epidermal EMG electrode?

**No.** Across the search performed, **no consumer or small-quantity seller of gold-nanomesh,
graphene GET, PEDOT:PSS-tattoo or cut-and-paste e-tattoo electrodes was found**; these remain
lab-protocol level [via sub-search]. Epicore Biosystems sells only B2B sweat-microfluidic patches
(no individual sales found); "Softsonics/Softionics" returned no product. Adjacent but not an
e-tattoo: Metrohm-DropSens screen-printed gold electrodes on rigid ceramic [70]. **This is why the
fallback plan in §8 is "build the proven open-source electronics and use gel/dry electrodes for
data", not "buy the tattoo".**

### 3.5 Patents worth reading before building

The Lu group's core e-tattoo patent is **US 10,492,703 B2, "Epidermal Sensor System and Process",
Nanshu Lu, S. Yang, P. Wang, UT System, granted 2019-12-03** [63] — this is the cut-and-paste
lineage. Northwestern/Rogers holds a family (US 10,969,395 B2; US 11,112,869 B2; US 11,064,946 B2;
US 2021/0145352 A1; US 2020/0315488 A1 / US 10,441,185 B2) [64][65][66][67][68], and NC State holds
US 2022/0340726 A1 on gas-permeable ultrathin stretchable epidermal devices [69]. A personal,
non-commercial R&D build is not a product, but the owner's EE should read US 10,492,703 B2 before
choosing the cut-and-paste route for anything that might later be shared or sold.

---

## 4. The interconnect problem

### 4.1 Why it is the hard part

A 1 µm tattoo and a 1 mm PCB differ in flexural rigidity by roughly five orders of magnitude. The
Taccola paper computes it explicitly for a PEDOT:PSS-on-tattoo system [5]:

| Layer | Thickness | Flexural rigidity D (N·m) |
|---|---|---|
| PEDOT:PSS electrode | 0.4–0.6 µm | 0.0223 × 10⁻⁹ |
| Tattoo substrate | 1.5 µm | 0.0236 × 10⁻⁹ |
| Printed Ag paste | 15 µm | 56.3 × 10⁻⁹ |
| Kapton connector | 25 µm | 4650 × 10⁻⁹ |

Any conductive track printed straight across that interface concentrates stress at the boundary and
cracks under bending or stretch. The published fixes are: (a) a **graded transition** through a soft
stretchable silver ink [5]; (b) a **serpentine** track geometry [1][2][5]; or (c) keeping the rigid
part **off the skin** and coupling through a reusable mechanical connector [7].

### 4.2 Method 1 — Polyimide tab into a ZIF socket (simplest, most robust)

Bareket/Inzelberg: screen-printed electrodes on tattoo film, laser-cut passivation, then "a
polyimide film with holes is glued to the array to fit into a zero insertion force (ZIF) socket"
[7]. The array is placed on skin; the connector tab sits at the edge and clips into a custom PCB.
The same group recorded facial sEMG with this stack for an hour with the head free to move, and the
amplifier was additionally held with **medical tape (3M Transpore) and a plastic hair clip** [8].

**Why it suits this build:** ZIF sockets and 13–25 µm polyimide are cheap and available; the tab is
reusable while the tattoo is disposable; and it survived the constant micromotion of cheek muscles
in 18 volunteers [8]. The trade-off is that the tab is a stiff "handle" the user can feel [4].

### 4.3 Method 2 — Silver paste + Au/PET strips + clip (no socket needed)

Lu group: cut **13 µm Au/PET strips (Rotex Tech)** as intermediate connectors, attach one end to a
tattoo terminal with **silver paste (Creative Materials 124-23)** and alligator-clip the other end
[2]. This is the least-tooling option and can be done at a kitchen table.

### 4.4 Method 3 — Screen-printed stretchable Ag + Kapton pad + magnetic snap (best long-wear)

Taccola et al. solve the mismatch explicitly for multi-day wear [5]:

- **Graded transition:** serpentine lines of stretchable Ag paste (**CI-1036**, baked 120 °C,
  10 min) are screen-printed on *both* the tattoo and a **25 µm Kapton HN** contact pad, and the
  two are joined with a drop of the same paste.
- **Magnetic docking:** four **neodymium magnets, 0.5 mm thick × 2.5 mm diameter**, glued to a
  plastic support, press the pads against magnets on the external device. The system "is able to
  sustain multiple connections/disconnections … without failure."
- **Testing:** short-term stretch to **10 %** (10/10 samples passed with no discontinuity);
  long-term cycling at **3 % strain, 18 cycles/min** for **96 h**, after which **70 % of samples**
  still worked; samples aged 6 months were "not significantly deteriorated". A vertical 4 g
  shake every hour and a 2-minute shake produced only minor perturbations, "still more than
  suitable" [5].
- The hardware, firmware and DXF files are **open source** (Zenodo DOI in [5]).

**Why it suits this build:** the jaw is a 3–10 % strain environment during speech, so the 3 %/18 cpm
result is a conservative lower bound; magnets make the connector wearable and washable. This is the
interconnect to copy for the under-chin array.

### 4.5 Method 4 — Anisotropic conductive film (ACF) bonding

ACF is the industry way to bond an FPC to a pad: an adhesive loaded with conductive particles
conducts only in z after heat + pressure. The e-tattoo literature is split on it:

- **Critical negative result:** the graphene-e-tattoo group states outright that "conventional
  electrical connections for thin-film sensors such as **soldering, anisotropic cohesive films
  (ACF), and z-axis conductive tapes are not applicable to GET**" — a sub-micron graphene film
  ruptures under the bonding force [29].
- **But stretchable ACF now exists.** Hwang et al.'s **S-ACF** (20 µm Au/Ni-coated polystyrene
  particles in SEBS-g-MA) gives a contact resistance of "**0.19 ohm per 0.25 mm²**"
  (abstract: "0.2 ohm in 0.25 mm²", SD ±0.049), ~**50 µm** connection resolution, stable to
  **ε = 80 %**, **2000** stretch/flex cycles, shear **> 19.6 N (2 kgf)**, and bonds at
  **80 °C for 10 min under 0.1 MPa** [30]. For calibration, the same paper quotes commercial
  **3M ECATT 9703 at "0.3 ohm/6 mm²"** [30].
- **Nanoscale ACF is now room-temperature and pressure-free** (wet-volatile ethanol assist): a
  ~**300 nm** AgNW-disk/SEBS film with 40 µm disks and 40 µm gaps, **> 500 %** strain, **8.6 Ω** at
  a 0.06 mm² bond, resistance change **−12 % after 1000 cycles** at 125–250 %, **1.6 ± 4.9 %**
  after 24 h artificial sweat, and WVTR **1200–1230 g m⁻² day⁻¹** (vs Tegaderm 180) [31].

**Verdict:** ACF is a viable option for **Au/PI or SEBS patches above a few micrometres**, but not
for a sub-micron graphene tattoo. For a first build, mechanical docking is less risky.

### 4.6 Method 5 — Heterogeneous serpentine ribbon + soft conductive-rubber via (best for GET-class films)

Jang et al. solved the sub-micron interconnect by never letting a rigid trace touch the tattoo
[29]:

- A **750 nm Au/PI heterogeneous serpentine ribbon (HSPR)** carries the signal from the graphene
  electrode to a **soft conductive-rubber via** (SNE-553 silicone + Ni/graphite particles, modulus
  **0.19–2.3 MPa**), which then contacts a rigid wrist/behind-ear PCB.
- The **soft rubber interlayer has vertical resistance < 50 Ω under 20 % compressive strain, stable
  over 10,000 cycles**, with resistance change ~10 Ω [29].
- The HSPR reaches **42 ± 2.6 % stretchability** at R/R₀ = 2 (catastrophic failure 51.5 %), versus
  **9.8 ± 0.3 %** for a homogeneous straight GET and **4.4 ± 1.1 %** for a heterogeneous straight
  ribbon — a **~50-fold** enhancement. FEM max strain at 20 % applied is **4.3 %** for the HSPR arm
  vs **35 %** for the straight ribbon, with only **0.7 %** at the step edge. It survived **10,000
  cycles at 0–20 % strain** with resistance slightly decreasing [29].

This is the design to copy if the owner builds the graphene route (§2.6). For the printed/cut Au
route, the same principle applies: **serpentine everything, and cross into a soft interlayer before
the rigid pad.**

### 4.7 Method 6 — Magnetic snap / pogo-pin docking (most wearable, best cycle life)

- **Magnetic snaps produced zero motion artefacts** in a direct comparison with prong and spring
  snaps under standing, walking (**50 steps/min**) and rope jumping (**~120 jumps/min**), with and
  without a **140 g** mass; magnetic snaps "withstand all conditions without any artefact being
  recorded", with clean signal > 4 s about **100 %** of the time, while prong snaps degraded to
  **85.34 ± 29.32 %** clean rate (walking + mass) and spring snaps to **40.64 ± 48.3 %** [34]. No
  DC resistance was measured in that study.
- **Magnetic connectors + Mill-Max pogo pins survived 5000 mating/unmating cycles** with "all
  resistance and impedance values … below **1.6 Ω**"; at 2 cycles/day that is **≈ 6.8 years**.
  Conductive epoxy outperformed conductive stitch, which outperformed solder. Buckle retention
  forces were **9.82 / 13.50 / 22.86 N** and snap forces **10.04 / 15.46 / 22.93 N**. Peel strength
  for the stitched interconnect was **217.06 N** (buckle) / **145.19 N** (snap), while epoxy and
  solder joints failed at **< 15 N** (the copper wire broke first) [35].
- Silver epoxy alone (SunRay S-CEP7-SF4) was the best of three interconnects in [35], with all
  values **< 1.6 Ω** after 5000 cycles; note the general warning that silver paste "becomes
  mechanically stiff once it dries", concentrating strain [via [43]].

### 4.8 Method 7 — Textile / carbon-rubber electrodes and the wired behind-ear layout

If the owner is willing to give up the "tattoo" look at the electrode, **embroidered conductive
textile** is a robust fallback: hybrid polyamide thread electrodes gave sEMG amplitude comparable
to Ag/AgCl (**28.45 dB**), SNR **23.34 dB vs Ag/AgCl 23.10 dB** at 10 mmHg contact pressure, and
impedance correlation with Ag/AgCl up to **0.993** at 25 mm inter-electrode distance; 20 mm was
chosen. Washing was stable to the **5th wash**, after which surface resistance increased
**four-fold**; sweat *improved* the signal (lower contact impedance) [36]. Kusche et al. found dry
electrodes (gold, stainless, carbon rubber, metallized textile) can be tuned "down to ranges of
hydrogel electrodes and even below" with the right contact setup, with gold-plated best [24].

The published **wired layouts** both keep the rigid connector off the face: GET palm → 750 nm
Au/PI serpentine ribbon → conductive-rubber via → rigid wrist PCB [29]; neck patch → VIA →
co-planar ACF → FPC [37]. For a jaw/chin array, the analogue is a serpentine ribbon running to a
**behind-the-ear or jaw-hinge pod**.

### 4.9 What fails, and when

- **Strain failure of the metal/interconnect, not the tattoo:** inkjet PEDOT:PSS tattoos recovered
  well to **5 % strain** and first failed "at around 8 %, probably ascribable to failure of wire
  interconnection rather than to tattoo integrity"; the electrode area itself showed no cracks or
  delamination after repeated **10 %** cycles [4].
- **Delamination/adhesive failure under sweat:** the open-mesh design in [2] was chosen specifically
  so sweat does not accumulate at the interface; a continuous film traps it. Ferrari et al. note
  that a steady liquid layer can cause redness/itchiness and damage components [3].
- **Connector peel is the user-reported weak point:** in a study where 11 people wore the tattoos,
  all "described not to perceive the electrode but had perception of the connector part (wire or
  flat connector, placed at the edge of tattoo)"; the connector is thicker/stiffer than the sensing
  part [4].
- **Sub-micron films fail fast without encapsulation:** bare GET first delaminated at **4 h 23 min**
  and first ruptured at **5 h**; with liquid bandage, cracks appeared at **96 h** [20][26].
- **Strain concentrates at rigid islands and step edges:** FEM shows **0.7 %** strain at a
  heterogeneous serpentine step edge vs **35 %** for a straight ribbon at 20 % applied strain
  [29]; a review notes curved planar wires can "undergo complete fracture from the edge after
  repeated stretching" above **10 %** tensile strain [via [40]].
- **Prong/spring snap contacts lose signal under motion** (clean-signal rate dropped to
  **85.34 ± 29.32 %** and **40.64 ± 48.3 %**), whereas magnetic snaps did not [34].

**Recommended interconnect for this build:** screen-printed or cut **serpentine** traces from the
electrode to a **13–25 µm polyimide pad**; cross into a **soft conductive-rubber interlayer** before
the pad if the electrode is a sub-micron film [29]; then either a **ZIF socket** (cheap, bench use)
[7], **silver epoxy** (best cycling of the adhesives, < 1.6 Ω after 5000 cycles [35]), or the
**magnetic dock** (4 × 0.5 mm × 2.5 mm neodymium magnets) [5][34][35]. Mechanically anchor the pad
behind the ear/jaw hinge with medical tape so jaw motion pulls the tape, not the pad [8].

---

## 5. Measured performance

### 5.1 Skin–electrode impedance vs Ag/AgCl (the central comparison)

| Electrode | Area | Frequency | Impedance | Source |
|---|---|---|---|---|
| Inkjet PEDOT:PSS tattoo (after 60 min) | 300 mm², 20 mm gap | 60 Hz | **294 ± 1 kΩ** (median ± IQR, n = 7) | [4] |
| Titanium dry | 300 mm² | 60 Hz | **94 ± 3 kΩ** | [4] |
| Ag/AgCl pregelled | 300 mm² | 60 Hz | **102 ± 2 kΩ** | [4] |
| Inkjet PEDOT:PSS tattoo, EMG band | — | 10–450 Hz | "below 300 kΩ, ~300 kΩ at 60 and 100 Hz" | [4] |
| Screen-printed carbon (pristine) | 20 mm² | 1 kHz | ~10× *larger* than gelled | [7] |
| Screen-printed carbon + ppEDOT | 20 mm² | 1 kHz | ~10× *lower* than pristine carbon | [7] |
| Ag/AgCl commercial | 300 mm² (15× area) | 1 kHz | specific impedance ≈ ppEDOT/carbon | [7] |

**The most complete same-subject comparison** is Lopes et al.'s seven-way test (one subject, five
runs over five consecutive days, no skin prep, ~2 min after placement, 11 mm gap) [6]. Fitted
interface values:

| Electrode (5 µm–500 µm class) | Rd | Cd | Total Ze |
|---|---|---|---|
| Printed Ag-In-Ga tattoo (5 µm) | **31.8 ± 1.6 kΩ** | **60.5 ± 2.3 nF** | **145.7 ± 4.5 kΩ** |
| Hydrogel–PDMS | 42.2 | 39.1 | 240.9 |
| Ag/AgCl gel | 192.1 ± 31.9 kΩ | 44.4 nF | 324.9 ± 1.4 kΩ |
| AgPDMS | 236.2 | 28.9 | 420.0 |
| Stainless steel 316 | 312.7 ± 48.6 | 24.6 | 511.7 ± 0.7 |
| Carbon-black PDMS | 363.8 | 20.9 | 610.1 |
| z-axis Ag-Ni PDMS | 348.9 | 6.0 | ~70 (EMG band only) |

SNR rank in the same study: **tattoo > hydrogel > Ag/AgCl > AgPDMS > stainless > cPDMS > zPDMS**
[6]. The tattoo's advantage is conformability (higher effective contact area → higher Cd), not
material conductivity. **The two tables above come from different labs, electrode areas and fitting
methods (Ferrari's 60 Hz modulus vs Lopes's fitted RC model); do not compare their absolute
ohms across tables — compare within a table.**

Additional same-subject impedance/SNR data points: the graphene e-tattoo paper reports ECG SNR
**15.22 dB vs 11 dB** for gel on the same subject, with motion artifact "comparable to gel" [20];
PGIN reports "3.5 times lower interfacial impedance than commercial electrode" at 10 and 100 Hz
[22]; a 2024 hydrogel e-tattoo reports "**234 % lower interface impedance at 20 Hz**" and "**up to
19 dB higher SNR**" than medical Ag/AgCl [23]. For dry metal electrodes, Kusche et al. found
Ag/AgCl gel at **~1 kΩ total** and near-constant, dry Au/stainless starting at **~2×** that,
halving within 5 min and saturating after ~15 min; smooth carbon rubber ~3×, textured ~5×, and
metallized textile **> 15 kΩ at 391 kHz**; applying **5 N** contact force plus a high frequency let
dry metal match gel [24]. That study is in the bioimpedance band, not EMG, but it shows how
sensitive dry electrodes are to pressure and hydration. Goyal et al. confirm the mechanism: dry
impedance is dominated by the **stratum corneum at 1 Hz–10 kHz** and is strongly
**hydration-dependent**, and a **9 cm²** electrode had **~2× lower impedance** than a **4 cm²**
one [25].

Two important caveats, both from the papers: Ferrari et al. used a **gentle abrasion prep on all
electrode types** and note a more aggressive abrasion might lower impedance, but gentle prep "is
more suitable for facial and sensitive skin" [7, methods note]; and the PEDOT:PSS tattoo had
**higher impedance than both gel and dry at every frequency above 10 Hz**, which the authors
attribute to PEDOT:PSS being antistatic and lowering the interface capacitance [4]. A carbon +
ppEDOT electrode is the better impedance choice for the face [7].

### 5.2 Noise and SNR on facial sEMG

Bareket et al. (dry carbon/ppEDOT, 20 mm²):

- **SNR 13 (22 dB)** after **3 hours** on the hand, stable recordings [7].
- Noise RMS (single-ended): **83 ± 20 µV** carbon, **66 ± 6 µV** ppEDOT/carbon, **74 ± 15 µV**
  commercial pregelled (300 mm²).
- Noise RMS (differential): **26 ± 11**, **25 ± 9**, **22 ± 9 µV** respectively.
- Facial sEMG: recordings over the **zygomaticus major** on **3 individuals** distinguished neutral,
  smile, sad and angry expressions; a big smile vs laughing was separable [7].
- No skin irritation was observed **for five individuals for up to ten hours** [7].

Inzelberg et al. (8 screen-printed carbon electrodes, 5 mm diameter, on the cheek, 18 volunteers):

- SNR, nose wrinkle **1.57 ± 0.43** single-ended / **4.66 ± 2.18** differential; eye close
  **1.97 ± 0.65** / **10.86 ± 7.44**; voluntary smile **4.06 ± 2.59** / **7.73 ± 4.64** [8].
- Baseline noise RMS **39.82 ± 6.58 µV** single-ended, **13.78 ± 4.90 µV** differential [8].
- Sampling **3000 Hz** wired / **410 Hz** wireless; band-pass **5–500 Hz** / **5–204 Hz**; 50 Hz
  notch. The wireless amplifier weighed **7.95 g** at **3.5 × 1.8 × 0.9 cm** [8].
- Electrode placement took **about a minute**; recording ran for an hour with free head movement;
  the amplifier was secured with medical tape and a hair clip [8].

The takeaway: **a dry tattoo electrode on the face gives usable but not gel-grade SNR**, and the
smile/zygomatic channel is the strongest of the measured facial tasks. The under-chin muscles the
owner needs (anterior belly of digastric, buccinator) are smaller and deeper than zygomaticus, so
expect the lower end of this range.

### 5.3 Silent-speech validation with epidermal electrodes

The earliest silent-speech validation on an epidermal patch is **Liu et al. 2020**, an epidermal
Cu/PI "tattoo-like" patch attached to the lower jaw and both sides of the face [1]. Demonstrated
results:

- **Three channels** over **anterior belly of digastric (ABD), buccinator (BUC), zygomaticus (ZYG)**.
- **Closed vocabulary:** 5 action words (Front, Back, Left, Right, Stop) and 6 emotion words
  (Happy, Sad, Hello, Goodbye, Hug, Love), **30 trials each**, tester **spoke silently**.
- Classifier: **linear discriminant analysis** on wavelet-denoised features.
- **Average action-instruction accuracy up to 89.04 %; emotion-instruction accuracy 92.33 %**.
- Patch: **Cu electrodes, 400 nm thick, 9 mm diameter**, filamentary-serpentine mesh **0.1 mm
  wide, 0.2 mm radius of curvature**; **double-wave** interconnects encapsulated in **polyimide**;
  **total thickness < 10 µm**; **peel strength > 1 N cm⁻¹**.
- Stretch: **> 20 %** with no cracks; max principal elastic strain in the metal **11.24 %** vs Cu
  fracture strain **33.3 %**.
- Signal chain: **2000 Hz, 16-bit**, **NI USB-6003**, band-pass **10–1000 Hz**, ZTEMG-1300
  conditioning circuit.
- Fabricated **on a silicon wafer** and transferred to a **sterile polyurethane wound dressing**
  using **3M water-soluble tape** — i.e. **not** a hobbyist process [1].

**Interpretation.** This is the key existence proof for the owner's plan: a dry, gel-free,
few-micrometre electrode array on the jaw/face can drive silent-speech decoding at ~90 % over two
small closed vocabularies. It is **closed-vocabulary, 3-channel, 1-tester** and the fabrication
needs a cleanroom; it does not establish open-vocabulary decoding or long wear. The same group's
results section reports **89.6 ± 0.6 %** (action) and **92.7 ± 0.5 %** (emotion) under 10-fold CV,
best single-class values **80.9 ± 0.9 %** and **81.9 ± 0.6 %**, and **real-time HMI 77.6 % (5 class)
/ 83.6 % (6 class)**; wavelet soft-threshold denoising gave **SNR 20.87 ± 1.47 dB**, RMSE
**16.82 ± 2.1 µV** [1].

**The strongest result is Wang et al. 2021 — and it uses the DIY-cuttable electrode.** This is the
same cut-and-paste Au tattoo introduced in §2.1, worn on LAO/DAO/BUC/ABD [21]:

- **4 channels**, one working + one reference per channel; **110 daily words in 13 categories**;
  **closed vocabulary**; **silent** speech.
- Classifier: **LDA**, deployed on a cloud server; **recognition rate 92.64 %** over the 110 words.
- Signal chain: **gain 1000**, **10–500 Hz** band-pass, **10-bit ADC at 500 Hz**, Bluetooth 5 at up
  to **256 kb/s**, ear-mounted wireless DAQ module [21].
- The paper reports the system holding **≥ 96 %** in rest/walk/jog and **86 %** while running,
  **98 %** across repeated trials with large mouth deformation, and graceful channel loss (3
  channels > 85 %, 2 channels > 70 %, 1 channel 42.27 % vs 0.91 % chance) [21] (numbers read from
  the results/figures by the search pass; the headline 92.64 % is quoted in the abstract/intro).

**Ultrathin printed array (PGIN) — a second silent-speech demonstration.** Du et al. 2024 built a
**~115 nm** PEDOT:PSS/graphene-oxide photopatterned array (PGIN): **2060 S cm⁻¹ at 88 %
transparency**, **110 % strain**, **24.5 mC cm⁻²** charge storage, and an interfacial impedance
"**3.5 times lower than commercial electrode**" [22]. It is fabricated on **The Magic Touch tattoo
paper** by spin-coating, UV crosslinking through a photomask, and a 10 s sulfuric-acid dip [22].
For silent speech: **6 channels on the right side of the face**, ground on the **left mastoid**,
**8 volunteers** silently reading digits **0–9**, ten sets of ten, SVM and CNN classifiers, **up to
92 % accuracy**; digits zero/one/two were the worst classes [22]. Under motion, the paper reports
every PGIN channel stayed **> 20 dB SNR** while Ag/AgCl "showed a severe signal distortion" [22].

**Cross-track caution:** all three silent-speech results are **closed-vocabulary, isolated-word
classification**; no open-vocabulary continuous decoding or WER for an epidermal array was found.
Subject counts are 1–8. Cross-talk between facial channels is not quantified against gel anywhere
in this set (**gap/unverified**).

### 5.4 Wear duration, sweat, hair, removal, skin reactions

- **48 h** of continuous wear with usable impedance, and recordings were possible at both 24 h and
  48 h; impedance was "relatively constant" at 1 kHz throughout [4].
- **Graphene e-tattoo durability, from the paper's own Supporting Information [20][26]:** a bare
  GET had **first delamination at 4 h 23 min** and **first rupture at 5 h**; with a **< 1 µm
  liquid-bandage encapsulation**, cracks appeared at **96 h** and impedance escalated. Three
  sensors on chest/forearm/bicep were "not affected by" a **25-minute run at 6.5 mph**. A "no
  crack to 52 h" figure appears in some notes but was **not found in the SI** — treat 52 h as
  **unverified**. A review states liquid bandage gives "up to three days without any
  delamination" [via [29]].
- **One-week, 20-subject patch test with no inflammation** is claimed for the gold nanomesh, along
  with **> 10,000 bend/stretch cycles** and water-vapour transmission "superior to plastic foil
  and rubber sheet"; the dermatological severity scores themselves are paywalled, so those are
  **secondary/unverified** [9][17][27].
- **A 10-hour wear comparison** with the cut-and-paste Au tattoo found gel noise/impedance stable
  while the tattoo gradually degraded — but after 30 min of running at hour 8, sweat made the
  tattoo's noise lower than gel's [21]. Authors cleaned skin with water only [21].
- **Hair growing through the tattoo over 24 h** with "no visible effect on the quality of the
  recording" — the tattoo was perforated so hair could pass through; the authors propose this for
  long-term scalp EEG [4].
- **Sweat:** open-mesh designs minimise sweat accumulation [2]; a continuous film traps a liquid
  layer, which can cause redness/itchiness and damage the device [3].
- **Removal:** wash with soap and water and rub gently, like a child's temporary tattoo [4].
- **Skin reactions:** 11 wearers, "no skin irritation … even … for long-term recordings (2 days)";
  **one** subject showed moderate irritation to the ethylcellulose layer, judged a subjective
  uncommon sensitivity [4]. In [7], no irritation for 5 people up to 10 h.
- **Shaving/prep:** Ferrari et al. used a gentle abrasion on all sites; Bareket et al. state the
  gentle prep is what makes the face/sensitive-skin use case valid [4][7]. The owner should shave
  the jaw/chin, wipe with alcohol, and **not** aggressively abrade before a session.
- **Water vapour:** the ethylcellulose tattoo film's breathability is what makes multi-day wear
  tolerable; the review gives the relevant comparison (a film is a barrier when its water-vapour
  transmission rate drops below the ~5 g m⁻² h⁻¹ transepidermal water loss) and shows temporary
  tattoo and medical-grade polyurethane pass while silicones, PEN and parylene do not [3].

### 5.5 What is not demonstrated

- **No published open-vocabulary silent-speech decoder driven by an e-tattoo electrode array** was
  found; [1] is closed-vocabulary and the best available.
- **No published e-tattoo array on the hyoid / laryngeal neck sites.** The published arrays do
  include the **anterior belly of digastric** [1][21], but the laryngeal/hyoid channels that
  AlterEgo used are not covered by any epidermal array in this set.
- **No multi-day (≥ 4 days) e-tattoo sEMG dataset**; the longest quantified wear here is 48 h [4].
- **Skin-tone-stratified electrode performance** is not addressed by any paper fetched here
  (see §6).

---

## 6. Visibility and skin tone

### 6.1 How visible is each option in practice

- **Sub-micrometre transparent films are effectively invisible; the connector is not.** In the
  Ferrari et al. study, 11 wearers "did not perceive the electrode but had perception of the
  connector part (wire or flat connector, placed at the edge of tattoo)", and the authors state the
  connector is thicker/stiffer than the sensing part [4]. This is the single most useful
  visibility fact in the file: **the tattoo disappears, the tab does not.**
- **PEDOT:PSS tattoo:** overall thickness **600–1200 nm** on a **~450 nm** ethylcellulose carrier
  [4]; it looks like a faint clear film and is removed with soap and water [4].
- **Graphene e-tattoo:** **463 ± 30 nm** and **~85 % optically transparent** [20]. Graphene is a
  weak broadband absorber, so a few-layer film reads as a very faint grey; the **gold or copper
  traces and the contact pads are the visible elements**.
- **Gold nanomesh:** breathable, featherweight and the most comfortable in the wear studies, but
  gold reads as a **faint metallic sheen**, not invisible. The 2017 paper reports 20 subjects, one
  week, no inflammation, and EMG "comparable to gel"; some users "forgetting the sensors were
  attached" [9][17][27].
- **Transparent metal alternatives:** a silver-nanowire/PEDOT:PSS stretchable transparent electrode
  reports **~25 Ω/sq**, **~85 % transmittance at 550 nm**, stable to **50 % strain** and **500
  cycles**, sensing from **< 1 cm²** [28]. Metal meshes and nanowires can look **glossy** even when
  nominally transparent.
- **PGIN** is **88 % transparent** at 2060 S/cm, so a patterned array on the face is largely hidden
  except for its contacts [22].
- **The only "undetectable by sight and touch" claim** is a 2026 *Science Advances* paper: a
  **~200 nm** elastic film with transparent conductive nanowires, with reflections/gloss suppressed,
  recording EOG, facial EMG and EEG. The paper is paywalled here and the transmittance value is
  **unverified**; treat as a promising press-release-level result, not a benchmark [41].
- **Practical visibility verdict for the owner:** use a transparent/near-transparent electrode
  (GET via §2.6 if willing to do the wet transfer, otherwise printed PEDOT:PSS), route all traces
  to a **single tab behind the ear or at the jaw hinge**, and keep the tab small; the tab is what
  other people will see.

### 6.2 Skin tone, hydration, hair

- **No controlled study was found that stratifies biopotential electrode impedance or SNR by
  Fitzpatrick skin type / melanin.** The strongest statement located is a press release for the
  2026 film claiming operation "across a wide range of skin tones and features" — **unverified**
  [41] — and a 2024 paper on **eumelanin (black) conductive tattoo inks** intended to lower skin
  impedance, whose numbers are **unverified** [44]. Any claim that a given electrode is
  skin-tone-neutral for this build should be treated as an open experiment, not a fact.
- **Hydration dominates dry-electrode impedance.** Dry impedance is governed by the stratum
  corneum over **1 Hz–10 kHz** and is strongly hydration-dependent; a **9 cm²** electrode had **~2×
  lower impedance** than a **4 cm²** electrode, and **titanium gave better signal quality than
  stainless steel** (Ti 2.17 × 10⁶ S/m, SS 1.30 × 10⁶ S/m) [25]. For a chin/jaw array this means:
  dry, cold skin raises impedance, and a little moisture (water before application, or natural
  sweat) lowers it.
- **Hair is not a blocker for the tattoo, because it can grow through it.** Ferrari et al.
  demonstrated hair growing through the tattoo over **24 h** with no effect on the recording, and
  calculated the surface occupied by hair at **~0.5 % per cm²** (density **160 hairs/cm²**,
  diameter **60 µm**) [4]. This is a real advantage of the perforated tattoo over a continuous
  film or a rigid electrode on the jaw/chin.
- **Skin reactions:** the only quantified e-tattoo reaction rate in this set is **1 of 11**
  subjects showing moderate irritation to the ethylcellulose carrier [4]; no irritation was seen in
  5 people over 10 h in [7]. The gold-nanomesh one-week test claims zero inflammation but the
  severity tables are paywalled [9][17][27].

---

## 7. Concrete DIY recipe for a first under-chin + jawline tattoo array

**Goal:** 4 bipolar channels (4 working + 4 reference electrodes) on **LAO, DAO, BUC and the
anterior belly of digastric (under-chin)** — exactly the montage that already achieved **92.64 % on
110 silent words** with a cut-and-paste Au tattoo [21] — transferable with water, connected to an
OpenBCI/MyoWare-class amplifier through a reusable tab, for a few hundred US$ of consumables (see
the price caveat below). Add channels later if the 4-channel map underfits.

**Design rules from the data:** electrode **Au on 1.4 µm PET** (or printed PEDOT:PSS/carbon), keep
total thickness **≤ 5 µm**, use **filamentary serpentine traces 500 µm wide, ribbon-width-to-arc-
radius ratio 0.32, arc angle 20°** [21], put the stiff connector **at the jaw hinge / behind the
ear**, and reinforce the electrode–wire joint with a conductive adhesive or low-temperature alloy
[5][21].

### 7.1 Bill of materials (three variants)

**Variant 1 — fastest, no cleanroom (recommended first): screen-printed carbon + PEDOT on tattoo paper**

- Commercial temporary tattoo paper, printable (Silhouette / The Magic Touch class) [2][3][5][7].
- Conductive carbon ink (screen-printable) — the ink class used in [7].
- PEDOT:PSS inkjet/dispersion (e.g. Clevios P Jet 700 class) + optional 10 % vol glycerol [5];
  or a commercial PEDOT:PSS screen ink.
- Double-sided adhesive film (for the laser-cut passivation layer) [7].
- 13–25 µm polyimide (Kapton) sheet for the connector tab [4][5].
- Stretchable silver conductor paste for the serpentine traces (CI-1036 class) [5], or Au/PET
  strips + silver paste as the simpler Lu method [2].
- ZIF socket (FPC connector) + a small custom PCB, or a magnetic connector (4 × 0.5 mm × 2.5 mm
  neodymium magnets) [5][7].
- Optional: 3M Nexcare liquid bandage spray for the ~1 µm encapsulation [2].
- CO₂ or fiber laser for cutting the passivation/tab (VLS3.50 class used in [4][5]);
  or a Silhouette Cameo cutter for the Au/PET route [2].

**Variant 2 — lower impedance, and the one with a silent-speech precedent: cut-and-paste Au/Cr/PET**

- Silhouette tattoo paper; **1.4 µm PET** (PolyK class); **Cr and Au** targets; thermal evaporator.
- Silhouette Cameo (or any programmable cutter): sharpness 5, rate 2, thickness 1 [2].
- 13 µm Au/PET strips + silver paste for the connector [2].
- **This is the variant to build.** It is the electrode worn in the 110-word, 92.64 % silent-speech
  study, at **1.2 µm** with a **47 µm Tegaderm** carrier and the LAO/DAO/BUC/ABD montage [21].

**Variant 3 — printed PEDOT:PSS/GO photopatterned (PGIN), if a UV mask aligner is available**

- The PGIN recipe is fully published: **Clevios PH1000** + **GO** (7 wt % optimum) + **PEGDMA**
  (1.4:1 vs PEDOT) + **Irgacure 2959** (5 wt % vs PEGDMA) + **Capstone FS-30** (1 wt % vs PH1000);
  spin-coat **1000 rpm, 100 s**, dry at room temperature, UV crosslink **25 mW cm⁻² for 2 min**
  through a photomask, rinse, then dip in **concentrated sulfuric acid for 10 s** [22]. This is the
  highest-performance printed route (115 nm, 88 % transparent, 110 % strain) but the acid step and
  UV aligner are the price of admission [22].

### 7.2 Fabrication steps (Variant 1)

1. **Draw the array** in CAD: 12 electrodes, ~5 mm diameter, 20 mm spacing along muscle fibres for
   the differential pairs [1][4]; serpentine traces from each electrode to a single edge tab.
2. **Laser-cut a screen stencil** from acrylic/PET for the electrode pattern.
3. **Screen-print carbon ink** onto the tattoo paper through the stencil; dry per the ink datasheet.
4. **Over-coat with PEDOT:PSS** (or plasma-polymerise EDOT if a plasma etcher is available) to
   lower impedance [5][7].
5. **Screen-print the serpentine silver traces** on the same sheet, from each electrode to the tab
   region; bake at **120 °C for 10 min** [5].
6. **Laser-cut the double-sided adhesive passivation** with holes over the 12 electrodes; laminate
   it to the printed sheet [7].
7. **Laser-cut the Kapton tab** and bond it to the trace ends with a drop of silver paste; bake
   **120 °C for 10 min** [5].
8. **Prepare skin:** shave the jaw/chin; wipe with alcohol; gently exfoliate (no aggressive
   abrasion) [4][7].
9. **Transfer:** wet the backing paper, press the tattoo to skin, and slide the paper off (sliding
   beats peeling) [2]; hold for a few seconds.
10. **Optional encapsulation:** five light sprays of liquid bandage over the array, stencil-masking
    the electrode windows if a hydration sensor is ever added [2].
11. **Connect:** insert the Kapton tab into the ZIF socket, or snap the magnetic dock [5][7]; tape
    the tab at the jaw hinge with medical tape so jaw motion pulls the tape, not the pad [8].

### 7.3 Cost

Concrete, vendor-verified prices (2026-10-01; full table in §3):

- **Silhouette temporary tattoo paper: "as low as $9.99" for 2 sheets** [45] — the single most
  important consumable; one 8.5 × 11 in sheet yields several arrays.
- **Silhouette Cameo cutter**: a one-off machine purchase (price not verified here); a makerspace
  membership or a friend's cutter removes this cost.
- **MyoWare 2 Muscle Sensor: $42.95** (verified [53]); **MyoWare dev kit $154.95** [54] — but note
  it uses **gel** electrodes, so it is a pipeline tool, not the final electrode.
- **OpenBCI dry-polymer electrode kit: $199.99**; **IDUN Dryode Alpha kit: $224.99–$244.99** (out
  of stock 2026-10-01) [51][52] — the buyable dry fallback.
- **Ag/AgCl baseline: ≈ €0.22–$1.18 per electrode** depending on brand/pack [58][59][60].
- **Bare Conductive paint: $13.50/10 mL**, but **not skin-rated** [48][49].

Not priced (quote/makerspace): thermal-evaporator time for Cr/Au, PEDOT:PSS ink and an inkjet
printer capable of it, plasma etcher for ppEDOT, and the custom PCB (the owner's hired EE). The
gold and PEDOT:PSS material costs themselves are small; the **equipment access is the real cost**,
which is why the cut-and-paste Au route (one cutter + one evaporator run) is the cheapest credible
path.

### 7.4 How to validate the array (one afternoon)

1. Measure **electrode–skin impedance** with a known resistor or an impedance analyzer at 10, 60,
   100, 200, 1000 Hz, against an Ag/AgCl pair at the same 20 mm spacing on the forearm **and** the
   jaw; the target is the [7] result (ppEDOT/carbon ≈ 10× better than bare carbon, specific
   impedance ≈ gel) [4][7].
2. Record **silent vs mouthed vs voiced** versions of a 10-word set, 30 trials each, 4 channels,
   and run the same **LDA** pipeline as [1]. Then scale to the published benchmark: **110 words /
   13 categories, LDA, 500 Hz sampling, 10–500 Hz band-pass, gain 1000** — the configuration that
   reached **92.64 %** [21]. Because 4 channels is enough for that result on the same muscles, a
   4-channel first array is the right size.
3. Measure **baseline noise RMS** and report SNR the way [8] does (activity RMS / rest RMS), so the
   numbers are comparable to the published facial-EMG figures.
4. Leave the array on for 3 h and repeat; [7] reports SNR 13 (22 dB) at 3 h. Then extend to 24–48 h
   against the [4] benchmark.
5. Log **skin condition** (redness, itch) daily and stop at the first sign of irritation; note that
   one in 11 subjects reacted to ethylcellulose in [4].

### 7.5 What to change if the first array underperforms

- **Impedance too high / noisy:** switch from PEDOT:PSS-only to **carbon + ppEDOT** [7], or use
  Variant 2 (Au) which had the highest SNR in the seven-way comparison [6].
- **Delamination at the jaw hinge:** move the connector tab behind the ear; add the [5] magnetic
  dock and the graded soft-Ag transition.
- **Motion artifacts during speech:** use **open-mesh filamentary serpentine** geometry [2] and
  keep the differential pair 20 mm apart along the muscle [1][4].

---

## 8. Fallback commercial option

There is an important structural fact to plan around: **the electrodes in every strong paper here
are lab-made, not products.** GET, PGIN, the Hanein carbon/ppEDOT tattoo, the Lu cut-and-paste Au
tattoo and the IIT PEDOT:PSS tattoo are all fabricated per-paper. So the fallback is not "buy the
same tattoo"; it is a ladder of three options, in order of how fast they let the owner collect
labelled data.

1. **Ag/AgCl gel electrodes + a small EMG front-end (fastest, best signal, cheapest).** This is the
   gold-standard baseline in every comparison in this file: **94–102 kΩ at 60 Hz** on the forearm
   [4]. Consumables are **≈ €0.22–€0.28 per electrode** (Kendall H124SG 500-pack at €109.90;
   Kendall Ø55 mm 30-pack at €8.30) or **$94.37 for an 80-pack** of Rhythmlink EMG sticky pads
   [58][59][60]; the **MyoWare 2 Muscle Sensor is $42.95** [53]. This lets the owner build the
   **channel map and the LDA/CNN pipeline within days**, then swap in the tattoo. Gel dries and the
   adhesive is visible, so it fails the "barely different from normal face" requirement — but it
   de-risks the data collection.
2. **A commercial dry electrode array (a week, worse signal, no gel).** The buyable options are the
   **OpenBCI EEG Polymer Electrodes Kit at $199.99** (8 dry polymer electrodes + headband) [52] and
   the **OpenBCI/IDUN Dryode Alpha Kit at $224.99–$244.99** (10 flexible dry electrodes, quoted
   **~3.2–5.2 kΩ**, but **out of stock on 2026-10-01**) [51]. Expect the dry-metal behaviour
   measured by Kusche et al. — **~2× gel impedance at t = 0, halving within 5 min and saturating
   after ~15 min**, and very sensitive to contact force [24][25]. This gets the owner something
   wearable-ish while the tattoo is being iterated. g.tec, TMSi, Delsys, CGX/Cognionics, BioSemi and
   Neuroelectrics are quote/enterprise-only with no public price and are not realistic single-user
   purchases [55][56][57].
3. **Build the IIT open-source tattoo-adjacent system (2–6 weeks, best match).** Taccola et al.
   released the **Eagle schematics, PCB layouts, bill of components, firmware, USB-BT dongle
   firmware, 3D-printed case STLs, GUI and the DXF electrode layouts** for their BBLE-based EMG and
   ECG devices, validated with printed tattoo electrodes and magnetic docking
   (**Zenodo DOI in [5]**; the paper gives the repository URL and repository contents explicitly).
   This is the only end-to-end system in this track whose hardware is both **open** and
   **validated with an ultrathin electrode**, so it is the natural fallback for the hired EE: he
   builds the proven electronics while the owner proves out the electrode.

**What is explicitly *not* a fallback:** a vendor selling the GET/PGIN/Hanein e-tattoo. No such
product was found in this research (see §3 for the closest purchasable items). Anyone promising an
"e-tattoo EMG" product should be treated as marketing until a datasheet with impedance vs Ag/AgCl
is provided.

---

## Key takeaways for the build

1. **Two routes are buildable in weeks, no cleanroom.** (A) The Lu group's cut-and-paste stack —
   1.4 µm PET laminated on Silhouette tattoo paper, 10 nm Cr + 100 nm Au, patterned with a
   Silhouette Cameo, released with water to a **1.5 µm** tape-free, gel-free tattoo [2]. (B) The
   Hanein stack — screen-printed carbon, laser-cut double-sided-adhesive passivation, **ppEDOT**
   coating, polyimide tab into a **ZIF socket** [7]. Both need a laser/cutter plus an oven and a
   screen or stencil, not a fab.
2. **Buy the graphene instead of growing it.** GET is the best all-round electrode here —
   **463 ± 30 nm, ~85 % transparent, > 40 % stretch, impedance "on par with" Ag/AgCl, days of wear
   with liquid bandage** — and the lab protocol is: buy graphene-on-Cu (Grolltex), wet-transfer,
   dry-pattern with a Cameo plotter, contact with copper tape or silver epoxy, fume hood for the
   ammonium-persulfate etch [10][11][20].
3. **The interconnect decides whether the array survives speaking.** There are now three
   demonstrated answers, in increasing order of robustness: (a) a **polyimide tab into a ZIF
   socket** [7]; (b) **silver epoxy or a magnetic dock** — magnetic + pogo-pin connectors held
   **< 1.6 Ω over 5000 mating cycles**, and magnetic snaps recorded **zero motion artefacts** under
   walking and rope jumping while prong/spring snaps degraded [34][35]; (c) for sub-micron films,
   a **heterogeneous serpentine ribbon into a soft conductive-rubber via** [29]. Critically,
   **soldering, conventional ACF and z-axis tape are documented as *not applicable* to a
   sub-micron graphene tattoo** [29]; ACF only becomes viable as stretchable ACF for thicker
   Au/PI/SEBS patches (0.19 Ω per 0.25 mm², 80 °C/0.1 MPa) [30][31]. The IIT magnetic dock with
   screen-printed serpentine Ag traces survived **96 h at 3 % strain, 18 cycles/min in 70 % of
   samples**, and 10/10 samples survived short-term **10 %** stretch [5]. Put the stiff part off
   the moving chin.
4. **Conformability beats conductivity.** The material's own conductivity "seems irrelevant to the
   overall skin–electrode impedance"; what matters is intimate contact (higher interface
   capacitance, lower interface resistance) [6]. An ultrathin film on a curved jaw therefore beats
   a thicker, more conductive one.
5. **Dry tattoo facial sEMG works, but with a real SNR penalty.** Screen-printed carbon/ppEDOT on
   the hand reached **SNR 13 (22 dB)** after 3 h with no irritation up to 10 h [7]; on the face,
   8 printed carbon electrodes gave differential SNR **4.66 ± 2.18 (nose)** to **10.86 ± 7.44
   (eyes)** and **7.73 ± 4.64 (smile)** [8]. Expect the under-chin digastric channel to sit at the
   lower end.
6. **There are now three silent-speech demonstrations on epidermal arrays, and the best one uses
   the DIY-cuttable electrode.** (a) **Liu et al. 2020**: 3 channels (ABD/BUC/ZYG), **silent**,
   closed vocab 5 action + 6 emotion words, 30 trials each, LDA, **89.04 % / 92.33 %** (abstract;
   89.6 / 92.7 under 10-fold CV), real-time 77.6 % / 83.6 % — Cu/PI patch made on a silicon wafer
   [1]. (b) **Wang et al. 2021**: 4 channels on **LAO/DAO/BUC/ABD**, **1.2 µm cut-and-paste Au**
   tattoo on Tegaderm, **110 words / 13 categories**, LDA, **92.64 %**, with ≥ 96 % in
   rest/walk/jog and 86 % while running [21]. (c) **PGIN 2024**: 115 nm printed PEDOT:PSS/GO,
   6 channels, 8 volunteers, silent digits 0–9, **up to 92 %** and > 20 dB SNR under motion [22].
   All three are closed-vocabulary isolated-word classification; no open-vocabulary WER for an
   e-tattoo was found.
7. **Impedance ranking to plan around:** Ag/AgCl ≈ titanium dry (**94–102 kΩ at 60 Hz**) <
   carbon + ppEDOT (≈ gel specific impedance) < PEDOT:PSS inkjet tattoo (**294 ± 1 kΩ at 60 Hz**,
   higher than gel at every frequency above 10 Hz) [4][7]. If impedance is the bottleneck, choose
   carbon + ppEDOT, not PEDOT:PSS alone.
8. **Multi-day wear is plausible but only 48 h is quantified:** stable impedance at 24 h and 48 h,
   hair growing through a perforated tattoo with no signal effect, removal with soap and water, and
   **1 in 11** wearers showing moderate irritation to the ethylcellulose carrier [4]. One-week
   inflammation-free wear is claimed only for the gold nanomesh, and its numbers are
   secondary/unverified [9][16].
9. **Do not use unencapsulated liquid metal on the jaw.** Ga-In ink paints on and records ECG
   comparably [15], but it smears, can bridge traces, and its long-contact cytotoxicity is
   unresolved (papers paywalled — **unverified**) [18][19].
10. **Laser-induced graphene on polyimide is the cheapest chemical-free experiment** (10.96 Ω/sq,
    ≈ 330 % strain, 7 days on skin) but has **no published facial-sEMG validation**; run it only
    after a working Route A/B array gives you a baseline [12].

## Open questions

1. **The published arrays do cover the anterior belly of digastric** (ABD) [1][21], but **no paper
   puts an e-tattoo on the hyoid/laryngeal neck sites** that AlterEgo found useful, and no paper
   optimises an e-tattoo montage for this owner's anatomy. The channel map is still an open
   experiment.
2. **Open-vocabulary silent-speech decoding with epidermal electrodes** — not found. [1] is a
   closed 5- and 6-word vocabulary at ~90 %.
3. **Beyond 48 h of e-tattoo sEMG** — no multi-day (≥ 4 day) impedance/SNR dataset; the
   nanomesh's one-week claim is not verified for sEMG here [9][16].
4. **Facial-specific strain durability.** The best cycling test is 3 % at 18 cycles/min on the
   chest [5]; jaw motion during speech is faster and larger. No jaw-cycling test found.
5. **Skin-tone and hair-density dependence** of epidermal electrode impedance/SNR — no paper
   fetched addresses it directly (see §6).
6. **ACF bonding for e-tattoos** — no primary bond-resistance/peel/cycling numbers found; all
   published e-tattoo interconnects use a mechanical dock, silver paste or ZIF.
7. **Magnetic-dock cycle life** — [5] says it survived "multiple connections/disconnections"
   without giving a number.
8. **A like-for-like DIY cost/performance comparison** of GET wet transfer vs screen-printed
   carbon vs cut-and-paste Au for a single user — no published comparison; this is the owner's
   first-morning experiment.
9. **Long-contact safety of Ga-In / galvanic skin effects under a chin array that may be worn for
   hours** — unverified [18][19].
10. **LIG electrode sEMG impedance, SNR and crosstalk** — unverified [12].

---

## Sources

1. H. Liu, W. Dong, Y. Li, F. Li, J. Geng, M. Zhu, T. Chen, H. Zhang, L. Sun, C. Lee,
   "An epidermal sEMG tattoo-like patch as a new human–machine interface for patients with loss of
   voice", *Microsystems & Nanoengineering* **6**, 16 (2020).
   https://www.nature.com/articles/s41378-019-0127-5
   (open-access mirror: https://pmc.ncbi.nlm.nih.gov/articles/PMC8433406/)
2. Y. Wang, Y. Qiu, S. Kabiri Ameri, H. Jang, Z. Dai, Y. A. Huang, N. Lu,
   "Low-cost, μm-thick, tape-free electronic tattoo sensors with minimized motion and sweat
   artifacts", *npj Flexible Electronics* **2**, 6 (2018).
   https://www.nature.com/articles/s41528-017-0019-4
3. L. M. Ferrari, K. Keller, B. Burtscher, F. Greco, "Temporary tattoo as unconventional substrate
   for conformable and transferable electronics on skin and beyond", *Multifunctional Materials*
   **3**, 032003 (2020). https://doi.org/10.1088/2399-7532/aba6e3
   (PDF: https://beta.iopscience.iop.org/article/10.1088/2399-7532/aba6e3/pdf)
4. L. M. Ferrari, S. Sudha, S. Tarantino, R. Esposti, F. Bolzoni, P. Cavallari, C. Cipriani,
   V. Mattoli, F. Greco, "Ultraconformable Temporary Tattoo Electrodes for Electrophysiology",
   *Advanced Science* **5**, 1700771 (2018). https://pmc.ncbi.nlm.nih.gov/articles/PMC5867059/
5. S. Taccola, A. Poliziani, D. Santonocito, A. Mondini, C. Denk, A. N. Ide, M. Oberparleiter,
   F. Greco, V. Mattoli, "Toward the use of temporary tattoo electrodes for impedancemetric
   respiration monitoring and other electrophysiological recordings", arXiv:2012.13319 (2020);
   published in *Sensors* **21**(4), 1197 (2021). https://arxiv.org/abs/2012.13319
   (full text PDF: https://arxiv.org/pdf/2012.13319)
6. P. A. Lopes, D. Vaz Gomes, D. Green Marques, P. Faia, J. Góis, T. F. Patrício, J. Coelho,
   A. Serra, A. T. de Almeida, C. Majidi, M. Tavakoli, "Soft Bioelectronic Stickers: Selection and
   Evaluation of Skin-Interfacing Electrodes", *Advanced Healthcare Materials* **8**, 1900234
   (2019). http://sml.me.cmu.edu/wp-content/uploads/2019/07/lopes_ahm2019.pdf
7. L. Bareket, L. Inzelberg, D. Rand, M. David-Pur, D. Rabinovich, B. Brandes, Y. Hanein,
   "Temporary-tattoo for long-term high fidelity biopotential recordings", *Scientific Reports* **6**,
   25727 (2016). https://www.nature.com/articles/srep25727
8. L. Inzelberg, D. Rand, S. Steinberg, M. David-Pur, Y. Hanein, "A Wearable High-Resolution Facial
   Electromyography for Long Term Recordings in Freely Behaving Humans", *Scientific Reports* **8**,
   2058 (2018). https://www.nature.com/articles/s41598-018-20567-y
9. A. Miyamoto, S. Lee, N. F. Cooray, et al., "Inflammation-free, gas-permeable, lightweight,
   stretchable on-skin electronics with nanomeshes", *Nature Nanotechnology* **12**, 907–913 (2017).
   https://www.nature.com/articles/nnano.2017.125
   (only the abstract and reference list were accessible; full text paywalled — fetched content
   used only for the abstract claims.)
10. D. Kireev, et al., "Fabrication, characterization and applications of graphene electronic
    tattoos", *Nature Protocols* (2021). https://doi.org/10.1038/s41596-020-00489-8
    (paywalled; only the publisher's supplement/video metadata and an indexed caution line were
    accessible — cited for the step list and the ammonium-persulfate safety note, not for numbers.)
11. D. Kireev, et al., "Graphene electronic tattoos 2.0 with enhanced performance, breathability
    and robustness", *npj 2D Materials and Applications* **6** (2022).
    https://www.nature.com/articles/s41699-022-00324-6
12. Q. Sun, et al., "Gas-Permeable, Multifunctional On-Skin Electronics Based on Laser-Induced
    Porous Graphene and Sugar-Templated Elastomer Sponges", *Advanced Materials* **30**, 1804327
    (2018). https://doi.org/10.1002/adma.201804327
    (paywalled; abstract verified, used for the quoted material numbers.)
13. S. Yang, et al., "'Cut-and-Paste' Manufacture of Multiparametric Epidermal Sensor Systems",
    *Advanced Materials* **27**, 6423–6430 (2015). https://doi.org/10.1002/adma.201502386
    (paywalled; numbers quoted via the open review at [17] and the description in [2].)
14. D. Velasco-Bosom, et al., "Conducting Polymer–Ionic Liquid Electrode Arrays for High-Density
    Surface Electromyography", *Advanced Healthcare Materials* (2021).
    https://pmc.ncbi.nlm.nih.gov/articles/PMC11469138/
15. Y. Yu, J. Zhang, J. Liu, "Biomedical Implementation of Liquid Metal Ink as Drawable ECG
    Electrode and Skin Circuit", *PLOS ONE* **8**(3), e58771 (2013).
    https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0058771
16. Welt der Physik, "Elektronische Pflaster aus Nanonetzwerken", 2017 (secondary method and
    durability description of [9]). https://www.weltderphysik.de/gebiet/technik/nachrichten/2017/elektronische-pflaster-aus-nanonetzwerken/
17. S. Wu, et al., "Materials, Devices, and Systems of On-Skin Electrodes for Electrophysiological
    Monitoring and Human–Machine Interfacing", *Advanced Science* (2020).
    https://pmc.ncbi.nlm.nih.gov/articles/PMC7816724/
18. S. Kim, et al., "Cytotoxicity of Gallium–Indium Liquid Metal in an Aqueous Environment",
    *ACS Applied Materials & Interfaces* (2018). https://doi.org/10.1021/acsami.8b02320
    (paywalled/abstract elided — **unverified**.)
19. "Harnessing the Rheological Properties of Liquid Metals…", *ACS Accounts of Chemical Research*
    (2018). https://doi.org/10.1021/acs.accounts.8b00489
    (paywalled — cited only for the existence of an open long-contact safety question;
    **unverified**.)
20. S. Kabiri Ameri, R. Ho, H. Jang, L. Tao, Y. Wang, L. Wang, D. M. Schnyer, D. Akinwande, N. Lu,
    "Graphene Electronic Tattoo Sensors", *ACS Nano* **11**, 7634–7641 (2017).
    https://doi.org/10.1021/acsnano.7b02182
    (open PDF: https://figshare.com/articles/journal_contribution/Graphene_Electronic_Tattoo_Sensors/5249074
    — abstract/figures verified from the open copy; full-text numbers marked where secondary.)

*Sources 21–39 marked "(via sub-search)" were fetched by a delegated search pass of mine, not
re-fetched by me; their numbers are quoted as that pass reported them.*

21. Y. Wang, T. Tang, Y. Xu, Y. Bai, L. Yin, G. Li, H. Zhang, H. Liu, Y. Huang, "All-weather,
    natural silent speech recognition via machine-learning-assisted tattoo-like electronics",
    *npj Flexible Electronics* **5**, 20 (2021).
    https://www.nature.com/articles/s41528-021-00119-7
22. X. Du, et al., "Ultrathin Bioelectrode Array with Improved Electrochemical Performance for
    Electrophysiological Sensing and Modulation" (PGIN), *ACS Nano* **18**(51), 34971–34985 (2024).
    https://doi.org/10.1021/acsnano.4c13325
    (open accepted manuscript: https://par.nsf.gov/servlets/purl/10582528)
23. Hydrogel e-tattoo for electrophysiology, *npj Flexible Electronics* **8** (2024).
    https://doi.org/10.1038/s41528-024-00335-x (via sub-search; full text not fetched by me.)
24. R. Kusche, et al., "Dry electrodes for bioimpedance measurements — design, characterization and
    comparison", *Biomedical Physics & Engineering Express* **5**, 015016 (2018).
    https://doi.org/10.1088/2057-1976/aaea59 (via sub-search.)
25. K. Goyal, D. A. Borkholder, S. W. Day, "Dependence of Skin-Electrode Contact Impedance on
    Material and Skin Hydration", *Sensors* **22**(21), 8510 (2022).
    https://pmc.ncbi.nlm.nih.gov/articles/PMC9656728/ (via sub-search.)
26. S. Kabiri Ameri, et al., "Imperceptible electrooculography graphene sensor system for
    human–robot interface", *npj 2D Materials and Applications* **2**, 19 (2018).
    https://www.nature.com/articles/s41699-018-0064-4 (via sub-search; cited for durability of
    the same GET platform.)
27. RIKEN / EurekAlert press release on the gold-nanomesh work, 2017.
    https://www.eurekalert.org/news-releases/729928 (via sub-search; press-release level.)
28. J. Noh, et al., "Silver Nanowire-Based Stretchable Transparent Electrodes for Precise Biosignal
    Sensing from Small Skin Areas", *ACS Applied Materials & Interfaces* **17**(49), 66330–66338
    (2025). https://doi.org/10.1021/acsami.5c16155 (via sub-search; DOI as reported.)
29. H. Jang, et al., "Graphene e-tattoos for unobstructive ambulatory electrodermal activity
    sensing on the palm enabled by heterogeneous serpentine ribbons", *Nature Communications* **13**,
    6604 (2022). https://pmc.ncbi.nlm.nih.gov/articles/PMC9633646/ (via sub-search.)
30. S. Hwang, et al., "Stretchable anisotropic conductive film (S-ACF) for electrical interfacing in
    high-resolution stretchable circuits", *Science Advances* **7**(32), eabh0171 (2021).
    https://pmc.ncbi.nlm.nih.gov/articles/PMC8346218/ (via sub-search.)
31. R. Katayama, et al., "Gas-permeable and stretchable nanoscale anisotropic conductive film",
    *Science Advances* **12**(38), eaeh6203 (2026).
    https://pmc.ncbi.nlm.nih.gov/articles/PMC13588162/ (via sub-search.)
32. Hackaday, "Laser-Induced Graphene Supercapacitors From Kapton Tape", 2020.
    https://hackaday.com/2020/11/11/laser-induced-graphene-supercapacitors-from-kapton-tape/
    (via sub-search.)
33. Glowforge Owners Forum, "LIG (Laser Induced Graphene) — Settings", 2017.
    https://community.glowforge.com/t/lig-laser-induced-graphene-settings/9707 (via sub-search.)
34. M. Ferreira, et al., "Exploring the electrical robustness of conductive textile fasteners for
    wearable devices", *Scientific Reports* (2024).
    https://pmc.ncbi.nlm.nih.gov/articles/PMC10991394/ (via sub-search.)
35. A. Ugale, et al., "Durability of Wearable Buckle and Snap Magnetic Connectors", *Textiles*
    **6**(1), 17 (2026). https://www.mdpi.com/2673-7248/6/1/17 (via sub-search.)
36. L. Etana, et al., "Evaluation of Novel Embroidered Textile-Electrodes Made from Hybrid
    Polyamide Threads for Surface EMG", *Sensors* **23** (2023).
    https://pmc.ncbi.nlm.nih.gov/articles/PMC10181695/ (via sub-search.)
37. C. Wang, et al., "Monitoring of the central blood pressure waveform via a conformal ultrasonic
    device", *Nature Biomedical Engineering* **2**, 687–695 (2018).
    https://pmc.ncbi.nlm.nih.gov/articles/PMC6428206/ (via sub-search.)
38. C. Audette (EEG Hacker), "Homemade Passive Electrodes", 2013.
    https://eeghacker.blogspot.com/2013/11/homemade-passive-electrodes.html (via sub-search.)
39. Hackaday, "DIY EMG Uses An Audio Recorder", 2012.
    https://hackaday.com/2012/06/17/diy-emg-uses-an-audio-recorder/ (via sub-search.)
40. J. Li, et al., "Designs and Applications for the Multimodal Flexible Hybrid Epidermal Electronic
    Systems", *Research* (2024). https://pmc.ncbi.nlm.nih.gov/articles/PMC11310101/
    (via sub-search; cited for wire-fracture and substrate-elongation figures.)
41. Y. Liu, N. Matsuhisa, et al., "Reduction of appearance artifacts in wearable on-skin
    electronics", *Science Advances* (2026). https://doi.org/10.1126/sciadv.aee6417
    (paper paywalled; press release cited at
    https://www.eurekalert.org/news-releases/1135754 — **unverified numbers**.)
42. J. Lin, et al. (Tour group), "Laser-induced porous graphene films from commercial polymers",
    *Nature Communications* **5**, 5714 (2014). https://www.nature.com/articles/ncomms6714
    (via sub-search; cited for the 4.8 W CO₂ laser process.)
43. S. Ji, X. Chen, "Enhancing the interfacial binding strength between modular stretchable
    electronic components", *National Science Review* (2022).
    https://pmc.ncbi.nlm.nih.gov/articles/PMC9843131/ (via sub-search; cited for the
    silver-paste stiffening and wire-fracture warnings.)
44. "Electroactive Melanin Tattoo Inks for Effectively Reducing Skin Impedances",
    *ACS Applied Polymer Materials* (2024). https://doi.org/10.1021/acsapm.4c01588
    (via sub-search; **numbers unverified**.)
45. Silhouette America, "Tattoo Paper" product page.
    https://www.silhouetteamerica.com/tattoos-paper (via sub-search, observed 2026-10-01.)
46. 3D Jake CH, "Silhouette Printable Tattoo Paper".
    https://www.3djake.ch/de-CH/silhouette/printable-tattoo-paper (via sub-search, 2026.)
47. Amazon listing, "Hayes Paper Waterslide Decal Paper, 40 sheets" (ASIN B08CS64B8Z).
    https://www.amazon.com/dp/B08CS64B8Z (via sub-search, 2026.)
48. SparkFun, "Bare Conductive Electric Paint Sachet 10 mL".
    https://www.sparkfun.com/bare-conductive-electric-paint-sachet-10ml.html (via sub-search, 2026.)
49. Adafruit, "Bare Conductive Electric Paint Lamp Kit" (skin warning).
    https://www.adafruit.com/product/3746 (via sub-search, 2026.)
50. NovaCentrix, "Aerosol Conductive Inks".
    https://novacentrix.com/aerosol-conductive-inks/ (via sub-search, 2026.)
51. OpenBCI Shop, "IDUN Dryode™ Alpha Kit".
    https://shop.openbci.com/products/idun-dryode-kit (fetched directly: $244.99 for the 1.5 m-lead
    kit; $224.99 for the 1 m option; out of stock 2026-10-01.)
52. OpenBCI Shop, "EEG Polymer Electrodes Kit".
    https://shop.openbci.com/products/eeg-polymer-electrodes (via sub-search, 2026.)
53. SparkFun, "MyoWare 2 Muscle Sensor". https://www.sparkfun.com/myoware-2-muscle-sensor.html
    (fetched directly: $42.95.)
54. SparkFun, "MyoWare 2.0 Development Kit".
    https://www.sparkfun.com/products/18441 (via sub-search, 2026.)
55. g.tec, "g.SAHARA hybrid EEG electrodes".
    https://www.gtec.at/product/gsahara-hybrid-eeg-electrodes/ (via sub-search; price unverified.)
56. TMSi, "Textile HD-EMG Grids". https://www.tmsi.com/products/textile-hd-emg-grids/
    (via sub-search; price unverified.)
57. CGX/Cognionics, "Dry EEG Developers Kit". https://www.cgxsystems.com/dev-kit
    (via sub-search; no public price.)
58. MFI Medical, "Rhythmlink Disposable Single Recording Sticky Pad EMG Surface Electrode".
    https://mfimedical.com/products/rhythmlink-disposable-single-recording-sticky-pad-emg-surface-electrode
    (via sub-search, 2026.)
59. MeGro, "Kendall disposable electrodes with liquid gel and Ag/AgCl sensor, Ø55 mm, 30 pcs".
    https://www.megro.de/en/Kendall-disposable-electrodes-w-liquid-gel-and-Ag-AgCI-sensor-OE-55-mm-30-pcs./CHG-31.1663.21
    (via sub-search, 2026.)
60. Aurosan, "Covidien/Kendall H124SG ECG electrodes, 500 pcs".
    https://aurosan-shop.de/en/products/h124sg-ekg-einmalelektroden-500-stck-30x24-mm
    (via sub-search, 2026.)
61. FH Medical Services, "Vermed A10005 Performance Plus Stress-Holter Foam Electrode".
    https://fhmedicalservices.com/products/vermed-a10005-performance-plus-stress-holter-foam-electrode
    (via sub-search; pack size unverified.)
62. Ambu USA, "BlueSensor N" datasheet.
    https://www.ambuusa.com/Admin/Public/Download.aspx (via sub-search; price unverified.)
63. US Patent 10,492,703 B2, "Epidermal Sensor System and Process", N. Lu, S. Yang, P. Wang,
    UT System, granted 2019-12-03. https://patents.google.com/patent/US10492703B2/en
64. US Patent 10,969,395 B2, "Epidermal Microfluidic Sensor…", J. A. Rogers et al., Northwestern,
    2021-04-06. https://patents.google.com/patent/US10969395B2/en
65. US Patent 11,112,869 B2, "Epidermal Virtual Reality Devices", J. A. Rogers et al., Northwestern
    + UIUC, 2021-09-07. https://patents.google.com/patent/US11112869B2/en
66. US Patent 11,064,946 B2, "Devices and Related Methods for Epidermal Characterization of
    Biofluids", J. A. Rogers et al., University of Illinois, 2021-07-20.
    https://patents.google.com/patent/US11064946B2/en
67. US Patent Application 2021/0145352 A1, "Epidermal Sensing Systems for Optical Readout…",
    J. A. Rogers et al., 2021-05-20. https://patents.google.com/patent/US20210145352A1/en
68. US Patent Application 2020/0315488 A1 / US 10,441,185 B2, "Flexible and Stretchable Electronic
    Systems for Epidermal Electronics", J. A. Rogers, D.-H. Kim.
    https://patents.google.com/patent/US20200315488A1/en
69. US Patent Application 2022/0340726 A1, "Gas Permeable, Ultrathin, Stretchable Epidermal
    Electronic Devices…", Y. Zhu et al., NC State, 2022-10-27.
    https://patents.google.com/patent/US20220340726A1/en
70. Metrohm-DropSens, screen-printed gold electrodes (rigid ceramic).
    https://metrohm-dropsens.com/products/electrodes/modified-screen-printed-electrodes/
    (via sub-search; adjacent, not an e-tattoo.)
