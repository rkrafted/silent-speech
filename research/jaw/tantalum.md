# 22 µF low-profile tantalum / polymer capacitor for the ADS1298 VCAP1

Research date: 2026-10-19. Read from the TI datasheet, public LCSC product pages, the public
JLCPCB parts-library search, the manufacturer datasheets and the KiCad footprint library.
No account was created and no part was ordered.

**pick: C215879 because it is the only 22 µF part here that combines a 0.90 mm maximum body height, 15,700+ pieces in stock at both LCSC and JLCPCB, Extended-library assembly, and a 6.3 V rating that Vishay derates to 5.0 V — still above the 4 V maximum VCAP1 reference voltage.**

## 1. What the ADS1298 datasheet says about VCAP1

The VCAP1 pin is the output of the internal reference amplifier, not a 1.1 V digital rail. The
22 µF capacitor is the reference bypass to AVSS.

- **Pin name and value.** SBAS459K, page 10 (TQFP pin table): “28 VCAP1 — Analog bypass
  capacitor; connect 22-µF capacitor to AVSS”. The NFBGA pin table on page 8 says the same for
  pin 5H.
- **DC voltage, typical.** SBAS459K, page 33, §9.3.1.6 and Figure 31 (Internal Reference):
  “When using a 3-V analog supply, set the internal reference to 2.4 V. For a 5-V analog supply,
  set the internal reference to 4 V by setting the VREF_4V bit in the CONFIG2 register.” The
  same figure labels the VCAP1/VREFP output node “2.4V or 4V”.
- **DC voltage, maximum.** The datasheet gives no steady-state VCAP1 voltage above **4 V**. The
  only other VCAP1 voltage in the document is the power-on-reset threshold, page 96, §11.1:
  “Issue the reset after tPOR or after the VCAP1 voltage is greater than 1.1 V, whichever time
  is longer.” The 1.1 V in Figure 105 is the POR trip point, not the operating reference.
- **Leakage and ESR.** SBAS459K states **no** ESR limit and **no** leakage limit for the VCAP1
  capacitor. The only guidance is electrical/mechanical: page 96 says “In most cases, the VCAP1
  capacitor is also a multilayer ceramic; however, in systems where the board is subjected to
  high- or low-frequency vibration, install a nonferroelectric capacitor, such as a tantalum or
  class 1 capacitor (C0G or NPO)”, and “When using internal reference, noise on the VCAP1 node
  results in performance degradation.” Page 33 also asks for external band-limiting capacitors
  that limit the reference noise bandwidth to below 10 Hz. Low leakage and low ESR are therefore
  sensible design choices, but they are not datasheet pass/fail limits.
- There is **no 3.86 V specification** in SBAS459K; the 4 V figure above is the highest normal
  VCAP1 voltage in the document.

## 2. Qualifying parts (22 µF, ≥ 4 V, body height ≤ 1.25 mm, JLCPCB-assemblable, in stock)

| # | LCSC | Manufacturer / MPN | Type | Case (EIA); L × W × H max | V | Tol | Leakage | ESR | Polarity marking | JLCPCB class | Stock LCSC / JLC | 1-off LCSC / JLC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **C215879** | Vishay **T58MM226M6R3C0300** | Polymer tantalum (vPolyTan T58) | MM / 1608-09; 1.60 ± 0.20 × 0.85 ± 0.20 × **0.90 mm** | 6.3 V (derated 5.0 V) | ±20 % | 14 µA max at +25 °C (at 6.3 V) | 300 mΩ max at 100 kHz | Anode polarity bar (bar = +), cathode at the opposite end | Extended | **15,706 / 15,708** | **$0.5663 / $1.0467** |
| 2 | **C19941081** | KEMET **T597S226M010APE100** | Polymer tantalum (KO-CAP T597) | S / 3216-12; 3.20 ± 0.20 × 1.60 ± 0.20 × **1.20 mm** (1.1 ± 0.1) | 10 V | ±20 % | 66 µA max at rated 10 V after 5 min (0.3 CV) | 100 mΩ max at 100 kHz | Anode (+) end and cathode (−) end marked; polarity bar | Extended | **40 / 40** | **$0.8413 / $0.9144** |

Sources for the numbers: Vishay T58 datasheet Doc. 40189 (case table, standard ratings, marking);
KEMET T59X datasheet T2073_T59X (case table, ratings table, leakage note); LCSC product pages
(stock, tolerance, 1-off price); JLCPCB parts library (Extended class, JLC stock, JLC price).

### Why this order

1. **C215879 (best).** 0.90 mm maximum height is the lowest of any stocked 22 µF tantalum/polymer
   part found; 15,706 LCSC and 15,708 JLCPCB pieces mean it will not run out during a prototype
   or a small production run; the 14 µA maximum leakage is the lowest of the two; and the 6.3 V
   rating is derated by Vishay to 5.0 V continuous, which still clears the 4 V maximum VCAP1
   voltage by 1.0 V. It is a 1608-09 (0603-ish) case, so JLCPCB's placement and reflow are routine.
   Note: LCSC and JLCPCB label this case “CASE-MM-1608-10”; Vishay's own case table says MM =
   **1608-09** with H max 0.90 mm, so the datasheet value is used here.
2. **C19941081 (second).** The safer 10 V rating (2.5× the 4 V maximum VCAP1 voltage), a larger
   3216 case and 100 mΩ ESR, at 1.2 mm maximum height. Its weakness is stock: only 40 pieces at
   LCSC and JLCPCB. That is enough for a handful of prototype boards but not for a production
   run, and it costs about 50 % more than C215879 at LCSC.

### Near misses (not in the table because they fail the hard 1.25 mm maximum)

- **C3202863** — Zhenhua XinYun CA45A-P-6.3V-22UF-K, MnO2 tantalum, case P / 2012-12, 22 µF
  ±10 %, 6.3 V, 1.4 µA leakage, 240 in stock, $0.0747. The datasheet gives the case as
  2.0 ± 0.2 × 1.25 ± 0.2 × **1.2 ± 0.2 mm**, so the maximum height is **1.4 mm**, not 1.25 mm.
  It is the cheapest option and would fit a 1.4 mm envelope, but not this rule.
- **C11383** — KEMET TAJP226M006RNJ, MnO2 tantalum, case P / 2012-15, 22 µF 6.3 V, 3.3 Ω,
  **1.5 mm** nominal height, 14 in stock, $0.3369. Fails the height rule.
- **C11366** — KEMET TAJA226K010RNJ, MnO2 tantalum, case A / 3216-18, 22 µF 10 V ±10 %, 3 Ω,
  **1.8 mm** height, 472,486 in stock, $0.185. The high-stock, low-cost fallback if the
  low-profile rule is relaxed to 1.8 mm.
- **C132274** — KEMET TAJR106K006RNJ, MnO2 tantalum, case R / 2012-12, **10 µF** 6.3 V ±10 %,
  6 Ω, **1.2 mm** height, 6,311 in stock, $0.2954. The closest 10 µF part at 1.2 mm if 22 µF
  cannot be sourced; it is half the datasheet's 22 µF value.
- **C215860** — Vishay 298D226X0010M2T, 22 µF 10 V, case M / 1608-09, **0.9 mm** maximum height,
  but only **1 piece** in stock at LCSC/JLC. Not assemblable in practice.
- **C340707** — Kyocera-AVX F920J226MPA, 22 µF 6.3 V, case P / 2012-12, **1.2 mm** nominal,
  but **0** LCSC stock (4 in the JLC library). Not usable.

## 3. KiCad footprint for the best pick

The KiCad standard library `Capacitor_Tantalum_SMD` has no 1608-09 footprint: its 1608 family is
`CP_EIA-1608-08_AVX-J` (0.8 mm body) and **`CP_EIA-1608-10_AVX-L`** (1.0 mm body). The T58
datasheet's pad table gives **identical pad dimensions for the MM (1608-09) and M0 (1608-10)**
cases, and both KiCad footprints use the same pads (at ±0.715 mm, 1.09 × 1.13 mm), so the land
pattern is the same. The 0.8 mm `AVX-J` body envelope is too tight for the 0.9 mm MM part; the
1.0 mm `CP_EIA-1608-10_AVX-L` envelope clears it and is the library's T58 footprint. Its
description field reads:

> “Tantalum Capacitor SMD AVX-L (1608-10 Metric), IPC-7352 nominal, (Body size from:
> https://www.vishay.com/docs/48064/_t58_vmn_pt0471_1601.pdf)”

So the matching standard footprint is **`Capacitor_Tantalum_SMD:CP_EIA-1608-10_AVX-L`**, used with
the understanding that it is the 1.0 mm (M0) envelope for a 0.9 mm (MM) body; the pads are
identical, and the extra 0.1 mm is in the fab/courtyard, not the copper. For the second part,
KEMET case S / 3216-12 is **`CP_EIA-3216-12_Kemet-S`** in the same library.

## 4. Caveats and method

- Prices and stock move daily. The figures above were read on 2026-10-19 from the public LCSC
  product pages and the public JLCPCB parts search; re-check before releasing a BOM.
- The LCSC 1-off price is the retail single-piece price. The JLCPCB price is the parts-library
  price returned for quantity 1 and can differ; the Extended-library loading/feeder fee is
  additional and is not included.
- “JLCPCB class: Extended” means the part is in the Extended (not Basic) assembly library. Both
  picks are Extended, so either one incurs the usual Extended-part handling.
- The ADS1298 datasheet does not require a tantalum part; it recommends a nonferroelectric
  capacitor (tantalum or C0G/NPO) when the board is exposed to vibration. These parts are chosen
  for that nonferroelectric requirement, not because the datasheet mandates tantalum.
- The 22 µF value is the datasheet's pin-table value. A 10 µF part (C132274) is listed only as a
  fallback; it is outside the datasheet's stated value.
