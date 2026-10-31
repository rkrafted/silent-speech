# LCSC / JLCPCB part numbers — the four open sensor-pod parts

Scope: the four still-open parts on the sensor-pod order (0402 ferrite bead, 128 Mbit
QSPI flash, MAX17048 fuel gauge, SMD pogo pin) plus the 2x5 and 1x2 SMD headers, the USB-C
receptacle and 5 V TVS for the small USB charging board, a shorter pogo pin, and JLCPCB's
6-layer capability. Every part number below was read from the public LCSC product page
(and/or LCSC's own domestic store `item.szlcsc.com`) and cross-checked against the public
JLCPCB parts-library search API; every mechanical value comes from the manufacturer
datasheet drawing named in the row. Prices are USD, from the JLCPCB assembly parts library
unless the column says "LCSC 1-off". "JLC lib" is the JLCPCB library class: `Basic`,
`Extended` (JLCPCB can place both, at different handling fees) or `not assemblable`.

Method note: the JLCPCB parts library was queried through its public search endpoint
(`https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList`);
LCSC stock was read from the LCSC product page when reachable and otherwise from the
equivalent LCSC domestic product page (`item.szlcsc.com/<id>.html`), whose `stockNumber`
field is the LCSC stock. The LCSC English product pages intermittently serve a
"Challenge Validation" bot wall; that is why some stock figures are attributed to the
LCSC domestic store.

---

## 1. 0402 ferrite bead, BLM15HD182SN1D or 0402 equivalent with Z >= 1 kOhm at 2.4 GHz

Datasheet: Murata "GHz Noise Suppression Chip Ferrite Bead BLM15H____SN1_" reference
specification, Reference Spec. No. JENF243A-0024K-01
(https://datasheet.lcsc.com/datasheet/pdf/d3c74377b0928ed60229ef4bb9f3feac.pdf?productCode=C76888).
For BLM15HD182SN1D the spec table states **1800 Ohm +/-25 % at 100 MHz**, **2700 Ohm
+/-40 % at 1 GHz**, DC resistance 2.2 Ohm max, rated current 200 mA.

That reference specification stops at 1 GHz, so the 2.4 GHz value was taken from Murata's
published impedance data for the part. Murata's official BLM15 series S-parameter archive
(https://www.murata.com/-/media/webrenewal/tool/sparameter/ferritebeads/v22/blm15-s-v22.ashx?la=en)
contains the measured 2-port S-parameters of BLM15HD182SN1D from 1 MHz to 3 GHz in
`BLM15HD182SN1.s2p` (`# Hz S RI R 50`), which is the measured data behind Murata's
SimSurfing impedance-frequency curve. Converting the series S21 to impedance,
Z = 2 x 50 x (1 - S21)/S21, gives |Z| = 1871 Ohm at 100 MHz (checks against the 1800 Ohm
+/-25 % rating), 2531 Ohm at 1 GHz (inside the 2700 Ohm +/-40 % rating) and
**1009 Ohm at 2.4 GHz** (the nearest measured point, 2407.1 MHz, is 1005.5 Ohm; the curve
crosses 1 kOhm at about 2.43 GHz and is 985 Ohm at 2456 MHz). So the BLM15HD182SN1D itself
clears the >= 1 kOhm-at-2.4-GHz requirement, with only about a 1 % margin.

| # | LCSC | Mfr + MPN | Package | JLC lib | LCSC stock | JLC stock | 1-off / 10-off | Z @ 2.4 GHz (source) |
|---|------|-----------|---------|---------|-----------|-----------|----------------|----------------------|
| 1 | **C76888** | Murata **BLM15HD182SN1D** | 0402 (1.0 x 0.5 x 0.5 mm) | Extended | 458,058 | 458,058 | $0.0155 / $0.0155 | **1009 Ohm at 2.4 GHz** (Murata S-parameter data) |
| 2 | C21516 | Murata **BLM15HD102SN1D** | 0402 | Extended | 62,173 | 62,173 | $0.0191 / $0.0191 | 2000 Ohm at 1 GHz; 2.4 GHz not verified |
| 3 | C32472 | Sunlord **GZ1005D102TF** | 0402 | Extended | 18,351 | 18,351 | $0.0038 / $0.0038 | 1 kOhm at 100 MHz; 2.4 GHz curve not located |

pick: C76888 (Murata BLM15HD182SN1D) because Murata's own measured S-parameter data gives
1009 Ohm at 2.4 GHz, which clears the >= 1 kOhm requirement, and the part is in stock at
LCSC (458,058) and in the JLCPCB library (458,058) as an Extended part. The margin is thin
(about 1 %), so if the 2.4 GHz impedance must be comfortable rather than marginal, ask
Murata for a curve for a higher-impedance 0402 part or keep this bead as a series element
with the radio's matching network checked; the two alternatives listed are drop-in 0402
footprints but their 2.4 GHz values were not verified from a curve.

---

## 2. 128 Mbit QSPI NOR flash, WSON-8 6 x 5 mm, 3.3 V

| # | LCSC | Mfr + MPN | Package | JLC lib | LCSC stock | JLC stock | 1-off / 10-off | Notes |
|---|------|-----------|---------|---------|-----------|-----------|----------------|-------|
| 1 | **C190862** | Winbond **W25Q128JVPIQ** | WSON-8-EP(5x6) | Extended | 15,313 | 16,146 | $3.6756 / $3.1846 | the exact requested part; in stock |
| 2 | C2441427 | Winbond **W25Q128JVPIM(-TR)** | WSON-8-EP(5x6) | Extended | 24,626 | 24,630 | $2.8240 / $2.8240 | same 128 Mbit 3.3 V QSPI die and pinout, cheaper |
| 3 | C3001859 | ISSI **IS25LP128-JKLE** | WSON-8-EP(5x6) | Extended | 189 | 189 | $2.6315 / $2.2335 | different vendor, same WSON-8 6x5 128 Mbit 3.3 V QSPI function |

pick: C190862 (W25Q128JVPIQ) because it is the exact part requested, it is in stock at LCSC
(15,313) and in the JLCPCB library (16,146), and JLCPCB lists it as an Extended part it can
place. The W25Q128JVPIM (C2441427) is the drop-in fallback if the exact ordering code goes
short; the ISSI part is a second-source fallback. All three are 3.3 V, 128 Mbit, QSPI, in
the 5 x 6 mm WSON-8 with the same industry-standard 8-pad land pattern.

---

## 3. 2 x 5 pin header, 2.54 mm, surface-mount, vertical (KiCad `PinHeader_2x05_P2.54mm_Vertical_SMD`)

KiCad footprint geometry (read from `/usr/share/kicad/footprints/Connector_PinHeader_2.54mm.pretty/PinHeader_2x05_P2.54mm_Vertical_SMD.kicad_mod`):
pads on both sides of the body at x = +/-2.525 mm, i.e. the two pad rows are **5.05 mm**
apart, with five pads per row on a 2.54 mm pitch and a 3.15 x 1.0 mm pad.

Note: the XFCN `PZ254V-11-*` / `PZ254V-12-*` family is **through-hole**, not SMD — its
datasheet has a "P.C.B Hole Layout" with 1.02 mm holes and a 3.0 mm pin below the plastic —
so it cannot match this footprint.

| # | LCSC | Mfr + MPN | Mounting | JLC lib | LCSC stock | JLC stock | 1-off / 10-off | Pin above plastic | Plastic height |
|---|------|-----------|----------|---------|-----------|-----------|----------------|-------------------|----------------|
| 1 | **C32713285** | hanxia **HX PZ2.54-2x5P TP** | SMD, P=2.54 mm, vertical, 2x5 = 10 pos | Extended | 19,253 | 20,147 | $0.0934 / $0.0934 | 6.00 +/-0.2 mm | 2.50 mm |
| 2 | C5378168 | ZHOURI **PZ2.54-2*5-SMT** | SMD, P=2.54 mm, vertical, 2x5 = 10 pos | Extended | 393 | 393 | $0.0748 / $0.0748 | 6.0 +/-0.1 mm | 2.54 mm |
| 3 | C3294463 | HCTL **PZ254-2-05-S** | SMD, P=2.54 mm, vertical, 2x5 = 10 pos, locating post | Extended | 10,126 | 13,301 | $0.1281 / $0.1281 | not stated in the drawing | 2.5 mm |

Datasheet drawings: C32713285 —
https://datasheet.lcsc.com/datasheet/pdf/05dd0cad90f18fe26f11856a6b05a3f2.pdf?productCode=C32713285 ;
C5378168 — ZHOURI drawing; C3294463 — HCTL drawing. The hanxia recommended SMD pad field
measures 8.60 mm outer-to-outer across the two rows with 3.20 x 1.02 mm pads and a 2.54 mm
pitch (pad-row centres about 5.4 mm), which overlaps the KiCad 5.05 mm/3.15 mm pads within
the 3.2 mm pad length.

pick: C32713285 because it is a genuine surface-mount vertical 2x5 header whose datasheet
states both requested dimensions (pin length above plastic 6.00 +/-0.2 mm, plastic height
2.50 mm), it has the deepest JLCPCB stock of the three (20,147) and it is the cheapest
well-documented option at $0.0934.

---

## 4. Tall SMD pogo pin (working height about 5.0-6.0 mm, free height about 6-7 mm)

| # | LCSC | Mfr + MPN | Mount | JLC lib | LCSC stock | JLC stock | 1-off / 10-off |
|---|------|-----------|-------|---------|-----------|-----------|----------------|
| 1 | **C20826701** | Harwin **P70-1100045R** | SMT (tape and reel) | Extended | 100 | 100 | $1.4292 / $1.1942 |
| 2 | C7464877 | Harwin **P70-2300045R** | SMT (tape and reel) | Extended | 18 | 18 | $1.4569 / $1.4243 |
| 3 | C5221294 | YIYUAN **YTC1P-4520-01** | SMD, D=2 mm | Extended | 2,295 | 2,295 | $0.1717 / 50-off $0.1371 |

Datasheet values (Harwin customer information sheet P70-1XX0045R, page 1):

| Value | P70-1100045R | P70-2300045R |
|-------|--------------|--------------|
| Free height (dim A) | 6.30 +/-0.15 mm | 6.20 +/-0.15 mm |
| Max working height | 5.30 mm | 5.20 mm |
| Normal working height | 5.00 mm | 4.90 mm |
| Min working height / max allowed travel | 4.70 mm (stroke 1.60 mm) | 4.60 mm (stroke 1.60 mm) |
| Plunger/barrel diameter | 1.54 +/-0.03 mm (plunger tip 0.90 mm) | 1.50 +/-0.03 mm (plunger tip 0.90 mm) |
| Spring force at normal height | 1.22 N +/-0.34 N | 0.83 N +/-0.25 N |
| Current rating | 2.0 A | 2.0 A |
| Contact resistance | 30 mOhm max | 30 mOhm max |
| Plating (body) | 0.1 um gold over 1.4 um nickel | 0.1 um gold over 1.4 um nickel |
| Plating (plunger) | 0.4 um gold over 1.4 um nickel | 0.4 um gold over 1.4 um nickel |
| Durability | 10,000 cycles | 10,000 cycles |
| Recommended PCB pad | Ø2.00 +/-0.05 mm SMD pad | Ø1.80 mm solder pad (Ø0.85 mm hole) |
| Packing | 650 per reel | 580 per reel |
| Operating temperature | -40 to +85 C | -40 to +85 C |

YIYUAN YTC1P-4520-01 (shared series datasheet, part row 4520): free height 6.5 mm
(A = 4.5 mm barrel + B = 2.0 mm plunger), working height 5.10 mm, stroke 1.4 mm, plunger
Ø0.90 mm / barrel Ø1.50 mm / base Ø2.00 mm, current rating DC 12 V 1.5 A max, spring force
100 gf +/-20 gf at normal working height, 10,000-cycle minimum durability, plunger and
barrel gold plated over nickel.

pick: C20826701 (Harwin P70-1100045R) because it is the only candidate whose datasheet
states every requested value, its free height 6.30 mm sits in the 6-7 mm band and its
normal working height 5.00 mm (max 5.30, min 4.70) sits in the 5-6 mm band, its 2.0 A
rating clears the 1 A requirement, and its recommended pad is 2.00 mm (within the 2.0 mm
limit). The P70-2300045R is a near-identical second choice but only 18 units are in the
JLCPCB library. The YIYUAN YTC1P-4520-01 (C5221294) is the cheaper, deeper-stock third
option (free 6.5 mm, working 5.10 mm, 1.5 A, 10,000 cycles, about $0.17, 2,295 in stock).

---

## 5. MAX17048 1-cell fuel gauge (TDFN-8 2 x 2 mm) and pin-compatible equivalents

| # | LCSC | Mfr + MPN | Package | JLC lib | LCSC stock | JLC stock | 1-off / 10-off |
|---|------|-----------|---------|---------|-----------|-----------|----------------|
| 1 | **C2682616** | Analog Devices / Maxim **MAX17048G+T10** | DFN-8-EP(2x2) | Extended | 24,543 | 24,964 | $2.1486 / $1.8958 |
| 2 | C7497002 | Analog Devices / Maxim **MAX17048X+T10** | WLP-8 (0.9 x 1.7 mm; LCSC says 0.9 x 1.8) | Extended | 1,687 | 0 | $2.3216 / $2.2742 |
| 3 | C18185545 | Analog Devices / Maxim **MAX17049G+T10** | TDFN-8-EP(2x2) | Extended | 6 | 6 | $11.1524 / $9.6385 |

Quiescent current, from the MAX17048/MAX17049 datasheet page 2: Sleep mode (TA <= +50 C)
0.5 uA typ / 2 uA max; Hibernate mode with the reset comparator disabled (VRESET.Dis = 1)
**3 uA typ / 5 uA max**; Hibernate with the reset comparator enabled (VRESET.Dis = 0) 4 uA
max; Active mode 23 uA typ / 40 uA max.

Datasheet TDFN-8 pin table, copied exactly (MAX17048/MAX17049 datasheet, "Pin/Bump
Descriptions", page 6; the datasheet's own header is "PIN/BUMP | NAME | FUNCTION" over the
TDFN / WLP / NAME / FUNCTION columns):

| TDFN | WLP | NAME | FUNCTION |
|------|-----|------|----------|
| 1 | A1 | CTG | Connect to Ground |
| 2 | A2 | CELL | Connect to the Positive Battery Terminal. MAX17048: Not internally connected. MAX17049: Voltage sense input. |
| 3 | A3 | VDD | Power-Supply Input. Bypass with 0.1uF to GND. MAX17048: Voltage sense input. Connect to positive battery terminal. MAX17049: Connect to regulated power-supply voltage. |
| 4 | A4 | GND | Ground. Connect to negative battery terminal. |
| 5 | B4 | ALRT | Open-Drain, Active-Low Alert Output. Optionally connect to interrupt input of the system microcontroller. |
| 6 | B3 | QSTRT | Quick-Start Input. Allows reset of the device through hardware. Connect to GND if not used. |
| 7 | B2 | SCL | I2C Clock Input. SCL has an internal pulldown (IPD) for sensing disconnection. |
| 8 | B1 | SDA | Open-Drain I2C Data Input/Output. SDA has an internal pulldown (IPD) for sensing disconnection. |
| - | - | EP | Exposed Pad (TDFN Only). Connect to GND. |

Datasheet URL: https://datasheet.lcsc.com/datasheet/pdf/6ea2434b9fcbd476e93afe7bcb1f53c0.pdf?productCode=C2682616
(the identical official Maxim document is 19-6171 Rev 7; the canonical adi.com URL could not
be opened from this sandbox, so the same official PDF mirrored on the LCSC datasheet host
was used). Pin table on page 6.

What the datasheet says to do with CTG, QSTRT and ALRT when unused:
- CTG (pin 1), page 6: "Connect to Ground". The datasheet gives no conditional text; CTG is
  always grounded (there is no "if unused" note for it).
- QSTRT (pin 6), page 6: "Quick-Start Input. Allows reset of the device through hardware.
  **Connect to GND if not used.**" Page 14 repeats: "The QSTRT pin is unused in this
  application and is connected to GND." Table 3 (page 15) also lists QSTRT = "Connect to
  GND".
- ALRT (pin 5), page 6: "Open-Drain, Active-Low Alert Output. Optionally connect to
  interrupt input of the system microcontroller." Table 3 (page 15, 1S rows) lists ALRT =
  "Leave unconnected". Page 14 adds: "In all cases, the system must provide pullup circuits
  for ALRT (if used), SDA, and SDL." (the datasheet prints SDL, a typo for SCL).

pick: C2682616 (MAX17048G+T10) because it is the only in-stock, JLCPCB-placeable MAX17048
(24,543 at LCSC / 24,964 at JLCPCB), and it is the 1-cell member of the shared 2 x 2 mm
TDFN-8 pinout. The WLP version (C7497002) has 1,687 at LCSC but is zero-stock in the JLCPCB library, and the
MAX17049G+T10 (C18185545) shares the pinout but is the 2-cell part, so it is not a
functional 1-cell drop-in.

---

## 6. 1 x 2 pin header, 2.54 mm, surface-mount, vertical, pads alternating left/right (KiCad `PinHeader_1x02_P2.54mm_Vertical_SMD_Pin1Left`)

KiCad footprint geometry (read from the footprint file): pad 1 at x = -1.655 mm, pad 2 at
x = +1.655 mm, i.e. the pad rows are **3.31 mm** apart, with 2.51 x 1.0 mm pads; the part
is a staggered-pad 1x2 SMD header (the two pads sit on opposite sides of the body).

| # | LCSC | Mfr + MPN | Mounting | JLC lib | LCSC stock | JLC stock | 1-off / 10-off | Pin above plastic | Plastic height |
|---|------|-----------|----------|---------|-----------|-----------|----------------|-------------------|----------------|
| 1 | **C41417359** | hanxia **HX PZ2.54-1x2P TP-YQ** | SMD, P=2.54 mm, vertical, 1x2, staggered pins (Type A / Type B) | Extended | 50,994 | 50,994 | $0.0281 / $0.0281 | 6.00 +/-0.2 mm | 2.50 mm |
| 2 | C2883759 | XKB **X6511WVS-02H-C60D48R2** | SMD, P=2.54 mm, vertical, 1x2, staggered (R1/R2) | Extended | 2,200 | 4,219 | $0.0593 / $0.0593 | C = 6.0 mm | H = 2.5 mm |

Datasheet drawing for C41417359:
https://datasheet.lcsc.com/datasheet/pdf/1b0c7ceb9cbed233d19ca44ae115b638.pdf?productCode=C41417359
The hanxia recommended SMD pad field measures 6.40 mm outer with 3.20 x 1.02 mm pads and a
2.54 mm pitch (pad-row centres about 3.20 mm, versus KiCad's 3.31 mm), and the drawing
defines the mirror-image Type A ("right front, left back") and Type B layouts that
correspond to KiCad's Pin1Left and Pin1Right footprints.

pick: C41417359 because it is the closest dimensional match to the KiCad
`PinHeader_1x02_P2.54mm_Vertical_SMD_Pin1Left` footprint (pad-row centres 3.20 mm versus
3.31 mm), its datasheet states both pin-style values (pin above plastic 6.00 +/-0.2 mm,
plastic height 2.50 mm), it uses the same pin style as item 3, and it has the deepest stock
(about 51,000) at the lowest price ($0.0281).

---

## 7. USB-C 2.0 receptacle and 5 V TVS for the small charging board

USB-C receptacle:

| # | LCSC | Mfr + MPN | Pins / mounting | JLC lib | LCSC stock | JLC stock | 1-off / 10-off |
|---|------|-----------|-----------------|---------|-----------|-----------|----------------|
| 1 | **C165948** | Korean Hroparts **TYPE-C-31-M-12** | 16-pin, SMD top-mount, 7.35 mm long | Extended | 351,036 | 367,652 | $0.1864 / $0.1864 |
| 2 | C393939 | SHOU HAN **TYPE-C16PIN** | 16-pin, SMD right-angle | Extended | 335,641 | 349,817 | $0.0689 / $0.0689 |
| 3 | C456012 | SHOU HAN **TYPE-C 6P** | 6-pin, SMD right-angle, 5 V 3 A | Extended | 572,900 | 580,426 | $0.0389 / $0.0389 |

The TYPE-C-31-M-12 drawing (https://datasheet.lcsc.com/datasheet/pdf/9e56b777c022540fcce7c7f67825f55e.pdf?productCode=C165948)
shows the full USB 2.0 pinout with VBUS, GND, CC1 and CC2 broken out. The 6-pin SHOU HAN
part is the power-only option (VBUS/GND only; no CC pins documented), which means it cannot
negotiate a USB-C-to-C charger. The mid-mount alternative is C223907 (Korean Hroparts
TYPE-C-31-M-14, 16-pin recessed/mid-mount, JLCPCB stock 3,101) but it needs a board cutout
and a different footprint.

5 V unidirectional TVS:

| # | LCSC | Mfr + MPN | Package | JLC lib | LCSC stock | JLC stock | 1-off / 10-off | Vrwm / Vbr / Vc | Ppp |
|---|------|-----------|---------|---------|-----------|-----------|----------------|-----------------|-----|
| 1 | **C113952** | MDD **SMAJ5.0A** | DO-214AC (SMA) | Extended | 515,333 | 524,956 | $0.0412 / $0.0412 | 5 V / 7 V / 9.2 V | 400 W (10/1000 us) |
| 2 | C169426 | Shandong Jingdao **SMF5.0A** | SOD-123FL | Extended | 51,900 | 51,916 | $0.0229 / $0.0229 | 5 V / 7 V / 9.2 V | 200 W (10/1000 us) |
| 3 | C78401 | Brightking **SMAJ5.0A/TR13** | SMA (DO-214AC) | Extended | 63,790 | 74,277 | $0.0536 / $0.0441 | 5 V / 6.4 V / 9.2 V | 400 W (10/1000 us) |

There is **no Basic-library** USB-C or 5 V unidirectional TVS in the JLCPCB library (checked
by scanning the JLCPCB parts API for TVS/ESD, SMAJ, SMF and Type-C results); every viable
part is Extended, so the JLCPCB Extended-part handling fee applies.

pick: C165948 (USB-C) and C113952 (SMAJ5.0A TVS) because the 16-pin TYPE-C-31-M-12 gives
CC1/CC2 for USB-C-to-C charging negotiation with the deepest JLCPCB stock (367,652), and
the MDD SMAJ5.0A is the cheapest standard SMAJ5.0A with the deepest stock (524,956). If
only an A-to-C charger is needed, the 6-pin C456012 saves about $0.15 per board.

---

## 8. Shorter SMD pogo pin (free height 2.0-2.8 mm, working height 1.6-2.4 mm)

The part to replace is Harwin P70-1000045R: its datasheet master table gives dim A (free
height) = 3.50 +/-0.20 mm, max working height 3.00 mm, normal working height 2.90 mm, min
working height / max allowed travel 2.70 mm, recommended PCB pad Ø2.20 +/-0.05 mm, 2.0 A,
0.88 N +/-0.29 N, 10,000 cycles, body 0.1 um gold over 1.4 um nickel and plunger 0.4 um
gold over 1.4 um nickel.

| # | LCSC | Mfr + MPN | Mount | JLC lib | LCSC stock | JLC stock | 1-off / 10-off |
|---|------|-----------|-------|---------|-----------|-----------|----------------|
| 1 | **C42419351** | YIYUAN **YTC1P-1807-01** | SMD, D=2 mm | Extended | 3,844 | 4,071 | $0.1111 / 50-off $0.0877 |
| 2 | C20612445 | Xinyangze **YZ50315020R-03** | SMD, D=2 mm | Extended | 617 | 1,038 | $0.3417 / 50-off $0.2678 |
| 3 | C5157371 | Xinyangze **YZ153915020R-01** | SMD, D=2 mm | Extended | 287 | 287 | $0.3337 / 50-off $0.2639 |

Datasheet values (YIYUAN drawing YTC1P-1807-01; Xinyangze drawings YZ50315020R-03 and
YZ153915020R-01):

| Value | YTC1P-1807-01 | YZ50315020R-03 | YZ153915020R-01 |
|-------|---------------|----------------|-----------------|
| Free height | 2.50 +/-0.15 mm | 2.00 +/-0.10 mm | 2.00 +/-0.15 mm |
| Working height | 2.00 mm | 1.60 mm | 1.60 mm |
| Max compression / stroke | 1.80 +/-0.10 mm (max travel 0.70 mm) | 1.55 mm limit (0.45 mm) | 1.50 mm limit (0.50 mm) |
| Plunger / barrel / base | Ø0.90 / Ø1.50 / Ø2.00 mm | Ø1.00 +/-0.03 / Ø1.50 / Ø2.00 | Ø1.00 / Ø1.50 / Ø2.00 mm |
| Spring force | 40-50 gf at normal working height | 130 gf +/-20 % | 40 gf +/-20 % |
| Current rating | DC 12 V, 1.0 A max; 50 mOhm | 12 V, 1.0 A; 50 mOhm | 12 V, 1.0 A; 50 mOhm |
| Plating | 1 micro-inch min Au over 50-120 micro-inch Ni | 3 micro-inch Au over 50-80 micro-inch Ni | 3 micro-inch Au over 50-80 micro-inch Ni |
| Durability | 20,000 cycles min | 10,000 cycles | 10,000 cycles |
| Recommended pad | not stated (base flange Ø2.00 mm) | not stated (base Ø2.00 mm) | not stated (base Ø2.00 mm) |

All three are inside the free-height 2.0-2.8 mm and working-height 1.6-2.4 mm windows, clear
the 0.5 A current requirement and the 10,000-cycle requirement, and have a Ø2.00 mm base
(within the 2.2 mm pad limit). None of their drawings state a recommended PCB pad size, only
the base diameter, so budget a pad of about Ø2.0-2.2 mm. The Xinyangze parts have thicker
gold (3 micro-inch) but a much lower stock position; the YIYUAN part has the best stock and
the lowest price, and its 20,000-cycle rating is double the requirement.

pick: C42419351 (YIYUAN YTC1P-1807-01) because it exactly meets the target (free 2.50 mm,
working 2.00 mm, 1.0 A, 20,000 cycles, Ø2.00 mm base, SMD tape-and-reel), it is Extended and
JLCPCB-stocked (4,071), and it is the cheapest of the three at $0.1111. The Xinyangze
YZ50315020R-03 (C20612445) is the fallback for a 2.00 mm free height with thicker gold, and
the Xinyangze YZ153915020R-01 (C5157371) is the third option.

---

## 9. JLCPCB 6-layer PCB capabilities: 1.2 mm and 1.0 mm, price, and design rules

Capabilities page: https://jlcpcb.com/capabilities/pcb-capabilities (the same tables are
served at https://jlcpcb.com/capabilities/Capabilities). Verbatim wording:

- "Thickness | 0.4 - 4.5 mm | Thickness for FR4 are: 0.4/0.6/0.8/1.0/1.2/1.6/2.0 mm
  (2.5 mm and above are for 12+ layer PCBs only)"
- "Thickness Tolerance (Thickness>=1.0mm) | +/- 10% | e.g. For the 1.6mm board thickness,
  the finished board thickness ranges from 1.44mm(T-1.6x10%) to 1.76mm(T+1.6x10%)"
- "Drill Diameter | ... Multilayer: 0.15 - 6.3 mm (0.1mm microvias only available for board
  thickness <=1mm; ENIG/OSP surface finish required)"
- "Min. Via hole size/diameter | 0.15/0.25mm (0.1mm/0.2mm only available for board thickness
  <=1mm; ENIG/OSP surface finish required)"
- "Min. track width and spacing (1 oz) | 0.10 / 0.10 mm (4 / 4 mil)" with description
  "1- and 2-layer: 0.10 / 0.10 mm (4 / 4 mil) Multilayer: 0.09 / 0.09 mm (3.5 / 3.5 mil).
  3 mil is acceptable in BGA fan-outs."

**1.2 mm and 1.0 mm for 6 layers:** the capabilities page has no per-layer thickness row,
but the public JLCPCB quote page (https://jlcpcb.com/quote) embeds its own per-layer
configuration; for FR-4 batch, 6 layers, the selectable thicknesses are exactly
**0.8 / 1.0 / 1.2 / 1.6 / 2.0 mm** (0.4 and 0.6 mm are shown but not selectable for 6
layers). So both 1.2 mm and 1.0 mm are offered for 6 layers.

**Price difference, 6 layers, 5 boards, 24 x 30 mm, ENIG-RoHS** (JLCPCB's own public quote
endpoint `POST https://jlcpcb.com/api/overseas-core-platform/shoppingCart/calculationGoodsCostsNew`,
the endpoint the quote page calls; total is the quote page's `orderCountTolls.dummyMoney`,
excluding shipping):

| 6L, 24x30 mm, 5 pcs, ENIG | Board base | ENIG surcharge | Total USD |
|---------------------------|-----------|----------------|-----------|
| 1.2 mm | $32.00 | $16.70 | **$48.70** |
| 1.6 mm | $32.00 | $16.70 | **$48.70** |
| Difference (1.2 vs 1.6) | $0.00 | $0.00 | **$0.00** |

A quantity-25 sanity check on the same endpoint: 1.2 mm and 1.6 mm both give base $33.00 +
ENIG $17.00 + stencil $2.40 = $52.40, while 1.0 mm gives base $66.00 ($85.40 total) and
2.0 mm gives base $99.00. So 1.2 mm and 1.6 mm are genuinely price-identical for this
6-layer order, and dropping to 1.0 mm roughly doubles the board base price.

**Do the design rules change with thickness?** Between 1.2 mm and 1.6 mm, no: both are
greater than 1 mm, so the minimum via is 0.15 mm hole / 0.25 mm via and the minimum
track/space is 0.09 / 0.09 mm (multilayer, 1 oz). Thickness only matters across the 1 mm
boundary: at 1.0 mm the 0.1 mm hole / 0.2 mm via microvia becomes available (with ENIG/OSP
surface finish required). ENIG is the finish this order already uses.

pick: stay at 1.6 mm (or move to 1.2 mm at no cost) because JLCPCB charges the same
$48.70 for 5 boards of 24 x 30 mm 6-layer ENIG at either 1.2 mm or 1.6 mm, and neither
thickness changes the minimum via or track rules; 1.0 mm is offered but costs more and is
only worth it if the 0.1 mm microvia capability is needed.
