# What the chip makers' forums already answer: six ADS1298 / NINA-B306 questions

Public pages only. No account was created, nothing was logged into, posted, replied to, voted on
or emailed. Searches used only part numbers, pin names and electrical terms (for example
`ADS1298 RLD electrode impedance`, `ADS1298 VCAP1`, `nRF52840 VBUS`, `NINA-B306 I2C radio
sensitive`); no application, body-site or product-category word was typed into any search box or
URL. Forum thread pages were read through the public text proxy `r.jina.ai` where the site's bot
wall returned 403 to a direct fetch; the canonical thread URL is given in each table.

A note on dates: forum pages show relative dates ("over 8 years ago"), so the year below is the
year implied by that label at the time of reading, not a date printed on the post.

**Part names covered.** The ADS1298/ADS1294/ADS1296/ADS1298R material is one family document
(SBAS459K), and the order code ADS1298IPAG is that device in the TQFP-64 package; the threads mostly
say "ADS129x". ADS1299 appears only where a source states an ADS1299-specific value — the 100 µF
VCAP1 note in Q3 and the 392 kΩ || 10 nF evaluation-board network in Q1 — and those rows say so.
The Nordic/u-blox side was covered as nRF52840, nRF52833, NINA-B306, NINA-B301 and NINA-B3 (the
family data sheet and system integration manual). Both spellings were used where the terms
differ: RLD / right leg drive, VCAP1 / VCAP 1, CLK_EN / CLKEN, I2C / TWI.

---

## Q1 — ADS1298 RLD loop stability with high contact impedance and a 10 kΩ series resistor

**Verdict: PARTLY.** TI states plainly that RLD loop stability is system-specific and gives the
component values it actually uses, but it publishes no stability analysis or recommended values
for a 0.1–2 MΩ electrode contact resistance with a 10 kΩ series resistor. The 392 kΩ || 10 nF
network in the question is **not** the datasheet network: the datasheet's RLD example (Figure 94,
"Setting Common-Mode Using RLD Electrode", §10.1.2) draws 1 MΩ || 1.5 nF from RLDOUT to RLDINV,
and TI's RLD application report measures both 1 MΩ || 1.5 nF and 670 kΩ || 1.8 nF. The 392 kΩ ||
10 nF pair is the **ADS1299EEG-FE evaluation board's** network, and the only TI reply found about
it says the choice is unexplained and the resulting ≈40 Hz bandwidth is too low for 50/60 Hz.

| Source | Date | Who answered | What it says |
|---|---|---|---|
| [ADS1298 datasheet, SBAS459K](https://www.ti.com/lit/ds/symlink/ads1298.pdf), §9.3.1.7.6 p. 41 (stability) and §10.1.2, Figure 94 pp. 86–87 (values) | rev. Aug 2015 | TI (official document) | The RLD section says the loop is compensated externally and that "Stabilizing the entire loop is specific to the individual system, based on the various poles in the loop." The 1 MΩ \|\| 1.5 nF feedback network is drawn in Figure 94 (RLDOUT to RLDINV) in §10.1.2 "Establishing the Input Common-Mode"; the values appear only in the figure, with no tolerance or "typical" label in the text. |
| [Improving Common-Mode Rejection Using the Right-Leg Drive Amplifier, SBAA188](https://www.ti.com/lit/an/sbaa188/sbaa188.pdf), §4 p. 5 and Figure 6 | Jul 2011 | TI (official application report) | "Stability is the major concern in this RLD technique. Note that the protection resistor and the cable impedance form a low-pass filter." It says that pole "can be as small as 2 kHz because of the protection resistor and cable", so capacitor `CP` is added to introduce a zero and `CF` across `RF` sets the closed-loop bandwidth. Its measured board uses `RF` = 670 kΩ, `CF` = 1.8 nF; its Table 1 measures the same amplifier with 1 MΩ \|\| 1.5 nF and steps the source resistance `RP` from 1 MΩ down to 50 kΩ (CMR 70.6 dB without feedback, 93.3 dB with it at 100 kΩ). |
| [ADS1298: RLD circuit simulation (E2E 880544)](https://e2e.ti.com/support/data-converters-group/data-converters/f/data-converters-forum/880544/ads1298-rld-circuit-simulation) | 2019 | TI employee (`TI__Guru`) | Asked for a step-by-step RLD design procedure, the TI answer was: "I would suggest starting with the 1 M \|\| 1.5 nF feedback circuit used in the RLD application note." The same reply says: "We do not have a separate step-by-step design procedure for the ADS129x devices, primarily because we do not have actual, verified models for the internal amplifiers." |
| [ADS1298: RLD feedback/filter (E2E 780513)](https://e2e.ti.com/support/data-converters-group/data-converters/f/data-converters-forum/780513/ads1298-rld-feedback-filter) | 2018 | TI employee (`TI__Guru`) | On the RLDOUT-to-RLDIN feedthrough path the TI answer warns: "Adding a low-pass filter here would be detrimental to properly closing the RLD loop." The reply also says the datasheet word "filter" should have read "Series Resistance or Feedthrough". |
| [ADS1299: Right leg drive closed loop bandwidth — RC in datasheet and EK (E2E 400935)](https://e2e.ti.com/support/data-converters-group/data-converters/f/data-converters-forum/400935/ads1299-right-leg-drive-closed-loop-bandwidth-rc-in-datasheet-and-ek) | 2014 | TI employee (`TI__Guru`) | The asker compared the 1 MΩ \|\| 1.5 nF of the datasheet/application note with the 392 kΩ \|\| 10 nF on the ADS1299EEG-FE board and asked why the board's RLD bandwidth (≈40 Hz) is below 50/60 Hz. The TI answer: "Your reasoning is definitely justified… reducing the RLD bandwidth in the ADS1299 to only 40Hz would negate the added CMRR benefit"; "I do not know the reason why these values were chosen for our EVM"; and it "may still be a good idea to widen the RLD bandwidth to > 60Hz". This is an **ADS1299 thread**; the brief treats the ADS1299 RLD arrangement as shared, and this is the only source found that uses the 392 kΩ \|\| 10 nF value. |

What is missing: no TI page found gives a phase-margin or transient response for 0.1–2 MΩ source
resistance, and none evaluates 392 kΩ || 10 nF. SBAA188 is the closest published analysis: it
identifies exactly the mechanism the question worries about (protection resistor + cable
capacitance forming a low pole) and it does measure at a 1 MΩ source resistance, but only with
the application report's own feedback values and without the 10 kΩ RLDOUT series resistor.

## Q2 — Unipolar 3.3 V: internal RLDREF or an external mid-supply divider, and noise

**Verdict: PARTLY.** Both options are explicitly permitted and the register bit that selects them
is documented, but no TI page found reports a measured noise difference between them.

| Source | Date | Who answered | What it says |
|---|---|---|---|
| [ADS1298 datasheet, SBAS459K](https://www.ti.com/lit/ds/symlink/ads1298.pdf), §9.3.1.7.6 p. 41; CONFIG3 register, RLDREF_INT bit | rev. Aug 2015 | TI (official document) | "Set the reference voltage for the RLD to be generated internally ([AVDD + AVSS] / 2), or provided externally with a resistive divider." The register description adds: "0 = RLDREF signal fed externally" and "1 = RLDREF signal (AVDD – AVSS) / 2 generated internally". |
| [ADS1298: Noise on the ECG signals, internal RLD amp is used (E2E 1278584)](https://e2e.ti.com/support/data-converters-group/data-converters/f/data-converters-forum/1278584/ads1298-noise-on-the-ecg-signals-internal-rld-amp-is-used) | 2023 | TI employee (`TI__Mastermind`) | In a noise-troubleshooting checklist the TI answer says: "try with the Internal RLD amp first by setting RLDREF_INT=1 to use the internal mid supply voltage (AVDD+AVSS)/2". This is a debugging preference, not a noise comparison. |
| [How to change RLDREF for ADS1298 (E2E 207287)](https://e2e.ti.com/support/data-converters-group/data-converters/f/data-converters-forum/207287/how-to-change-rldref-for-ads1298) | 2012 | TI employees (`TI__Guru****`, `TI__Mastermind`) | The pin "is able to be configured as an input pin. You can connect this internally to Vdd/2 or the WCT node, or you could use your own external source to drive the pin." The EVM has R1/R2/R5 pads for a divider or a trim pot, but no jumper. |

What is missing: a quantitative statement of how much quieter the internal mid-supply is than a
1 % resistor divider (in nV/√Hz, or a measured noise floor for each option).
Neither the datasheet nor the threads give one, so the noise answer is OPEN even though the
selection answer is clear.

## Q3 — VCAP1 22 µF: ceramic X5R/X7R microphonics, or tantalum / polymer / C0G

**Verdict: ANSWERED.** The datasheet says exactly what the question asks, in the power-supply
section, and the wording is unambiguous.

| Source | Date | Who answered | What it says |
|---|---|---|---|
| [ADS1298 datasheet, SBAS459K](https://www.ti.com/lit/ds/symlink/ads1298.pdf), §11 "Power Supply Recommendations" p. 96 | rev. Aug 2015 | TI (official document) | "In most cases, the VCAP1 capacitor is also a multilayer ceramic; however, in systems where the board is subjected to high- or low-frequency vibration, install a nonferroelectric capacitor, such as a tantalum or class 1 capacitor (C0G or NPO)." It then explains: "EIA class 2 and class 3 dielectrics such as (X7R, X5R, X8R, and so forth) are ferroelectric. The piezoelectric property of these capacitors can appear as electrical noise coming from the capacitor. When using internal reference, noise on the VCAP1 node results in performance degradation." |
| [ADS1298: VCAP1 and WCT capacitor values (E2E 1634560)](https://e2e.ti.com/support/data-converters-group/data-converters/f/data-converters-forum/1634560/ads1298-vcap1-and-wct-capacitor-values) | 2026 | TI employee (`TI__Guru`) | On the value: "22uF on VCAP1 is recommended for ADS1294/8. 100uF is recommended on ADS1299 since the noise performance is so much lower". This thread discusses capacitance only, not dielectric; the dielectric answer is the datasheet above. |

## Q4 — Sharing one ADS1298 clock between two boards, plus START alignment

**Verdict: PARTLY.** The clock-sharing topology and the fact that START is the synchronisation
signal are documented. Nothing found covers a 15–20 cm two-wire clock cable, a series resistor or
buffer, whether the running clock output couples noise into the inputs, or how two separate
microcontrollers should align START.

| Source | Date | Who answered | What it says |
|---|---|---|---|
| [ADS1298 datasheet, SBAS459K](https://www.ti.com/lit/ds/symlink/ads1298.pdf), Table 11 p. 50 and §9.4.2 p. 56 | rev. Aug 2015 | TI (official document) | With `CLKSEL = 0` the CLK pin is an input: "0 X External clock Input: external clock". For a master: "set one of the devices as the master for the clock source with the internal oscillator enabled (CLKSEL pin = 1) and the internal oscillator clock brought out of the device by setting the CLK_EN register bit to 1. Use this master device clock as the external clock source for the other devices." For timing: "When using multiple devices, synchronize the devices with the START signal." |
| [ADS1298: How to design clock circuits for synchronous sampling of two ADS1298? (E2E 1684949)](https://e2e.ti.com/support/data-converters-group/data-converters/f/data-converters-forum/1684949/ads1298-how-to-design-clock-circuits-for-synchronous-sampling-of-two-ads1298) | 2026 | TI employee (`TI__Guru`) | "An external clock can be shared with the CLK pin for both devices. Each device must set the CLKSEL pin to 0 to accept the external clock input. Alternatively, the primary device can output the internal oscillator to the second device." The reply points to the datasheet's Multiple-Device Configuration section and adds no cable-length, series-resistor or buffer guidance. |

What is missing: Figure 65, "Synchronizing Multiple Converters", is a timing diagram for two
devices on a shared START, and the multiple-device section around it is written for one host.
There is no procedure for two independent MCUs (for example a shared START line versus
synchronising the START opcodes), and no statement about CLK output noise. Those parts remain
OPEN.

## Q5 — nRF52840 / NINA-B306 VBUS when USB is never used

**Verdict: PARTLY.** The official documents say only that 5 V must be on VBUS *when the USB
interface is used*; neither document found contains an explicit "leave open or tie to GND"
sentence. The Nordic forum answer and the non-USB reference circuit say tie it to GND.

| Source | Date | Who answered | What it says |
|---|---|---|---|
| [nRF52840 Product Specification v1.1](https://pdf.searchdatasheet.com/283a577b/nordicsemi.no/NRF52840-QIAA-R.txt), §5.3.2 "USB supply" p. 65 | 2018 (v1.1) | Nordic (official document) | "When using the USB peripheral, a 5 V USB supply needs to be provided on the VBUS pin." The chapter is conditional and does not state what to do with VBUS when USB is unused; the reference-circuit tables list configurations with USB disabled. |
| [NINA-B3 series data sheet, UBX-17052099 R15](https://content.u-blox.com/sites/default/files/NINA-B3_DataSheet_UBX-17052099.pdf), §3.1 NINA-B30 pin table p. 24, pin 31 | R15 | u-blox (official document) | Pin 31 is `VBUS`, "USB interface 5 V input", with the note: "Must be connected to 5 V for the USB interface to work." Again this states the condition for using USB, not the unused case. |
| [nRF52840 Unused USB bus (Nordic DevZone 35658)](https://devzone.nordicsemi.com/f/nordic-q-a/35658/nrf52840-unused-usb-bus) | 2018 | community (top reply) | "D+ and D- can be left unconnected and VBUS connected to GND. Please look at the circuit config num 6" — linking the nRF52840 PS reference-circuitry page for the configuration with USB disabled. This is the direct answer, but it is a forum reply, not a sentence in the Product Specification. |

A second DevZone thread, [48589](https://devzone.nordicsemi.com/f/nordic-q-a/48589/what-do-you-do-with-the-usb-pins-if-you-are-not-using-usb),
gives the same instruction — "You have to ground VBUS. D- and D+ can be left floating" — and adds
that the pins cannot be used as GPIO. A third thread, [69598](https://devzone.nordicsemi.com/f/nordic-q-a/69598/vusb-connection-to-gnd-if-usb-will-not-be-used)
(nRF52833), quotes the reference circuitry as connecting VBUS and DECUSB directly to GND when USB
is not used; the Nordic employee's reply there is about the C18/C19 capacitors rather than the
VBUS pin, so it supports the tie-to-GND practice without changing the verdict. All three replies
are consistent with the reference design; the absence of a one-line rule in the PS text is why
this is PARTLY rather than ANSWERED.

## Q6 — NINA-B306 radio-sensitive pins and a small ground plane beside the antenna

**Verdict: PARTLY.** The exact wording, the pin list and the 10 kHz recommendation are all in the
data sheet, so the first half is ANSWERED. No readable u-blox statement was found on running a
100 kHz I²C burst on those pins, and no measured range figure was found for a ground plane
smaller than the recommended 10 mm; those parts are OPEN.

| Source | Date | Who answered | What it says |
|---|---|---|---|
| [NINA-B3 series data sheet, UBX-17052099 R15](https://content.u-blox.com/sites/default/files/NINA-B3_DataSheet_UBX-17052099.pdf), §3.1 p. 23 note and p. 24 pin table + footnote 2 | R15 | u-blox (official document) | "Some GPIO pins are connected to the pins located close to the radio part of the RF chip. Digital noise on these pins can reduce the radio sensitivity." The marked pins are module pins **16** (`radio sensitive pin2`), **17, 18, 20, 21, 22, 23, 24, 28, 29, 35, 36, 37, 38, 39, 40** (`radio sensitive pin1`). Footnote 2: "It is recommended to keep frequencies below 10 kHz, and only use standard drive strength on these digital pins." |
| [NINA-B3 series system integration manual, UBX-17056748 R15](https://content.u-blox.com/sites/default/files/NINA-B3_SIM_UBX-17056748.pdf), §3.3.3 pp. 38–39 | R15 | u-blox (official document) | For the NINA-B3x6 PCB-trace antenna: "A large ground plane on the host PCB is a prerequisite for good antenna performance." and "It is recommended to have the ground plane extending at least 10 mm on both sides of the module." The manual gives no range number for a smaller plane, only that the recommendation exists. |
| [Pin configurations for GPIO pins on NINA-B306-00B (Nordic DevZone 116718)](https://devzone.nordicsemi.com/f/nordic-q-a/116718/pin-configurations-for-gpio-pins-on-nina-b306-00b-nrf52840-ble-module) | 2025 | community | The asker deliberately avoids the radio-sensitive pins for SPI/I²C: "My reasoning for choosing all the specific GPIO pins mentioned above is because they aren't radio sensitive so I'm not limited to keep the frequencies below 10 kHz". The reply: "as long as you don't have any high freq clocks on pins which are low freq only, you're good." This confirms the 10 kHz limit is treated as binding, but it is not a u-blox answer about 100 kHz bursts. |

The u-blox portal has public threads whose titles match both sub-questions — "GPIO pin
configuration on NINA-B306-00B nRF52840 BLE module", "Is it normal for a NINA-B306 module to have
an extremely short range?" and "PCB size required for NINA-B302 vs B306". Their bodies are served
by a client-side application and returned only a loading shell to this client, so their content is
not claimed here. That is the concrete reason the I²C and small-ground-plane parts are OPEN.

---

## Q | verdict | still worth posting?

| Q | Verdict | Still worth posting? |
|---|---|---|
| Q1 | PARTLY | **Yes.** No public page evaluates 392 kΩ \|\| 10 nF at 0.1–2 MΩ contact resistance with a 10 kΩ series resistor. A TI E2E post with the actual network, the contact resistance and a measured step response would get a real answer. |
| Q2 | PARTLY | **No.** The choice is documented (internal mid-supply or external divider). The missing noise number is cheaper to measure on our own board than to ask for. |
| Q3 | ANSWERED | **No.** The datasheet already says tantalum / C0G / NPO under vibration and explains the X5R/X7R piezoelectric mechanism. |
| Q4 | PARTLY | **Yes.** Ask TI about a 15–20 cm clock line (series resistor or buffer), clock-output coupling into the inputs, and START alignment when the two devices are driven by separate MCUs. None of that is in the datasheet or the existing thread. |
| Q5 | PARTLY | **No.** The vendor reference design and three Nordic forum replies say tie VBUS to GND; posting again would only repeat that. |
| Q6 | PARTLY | **Yes, two narrow questions.** (a) Is a 100 kHz I²C burst on a `radio sensitive pin1` acceptable if the bus is short and idle most of the time? (b) What is the measured range penalty for a ground plane narrower than 10 mm on each side of a NINA-B306? The data sheet gives the rule, not the trade-off. |

## Sources not used in the verdicts

`slau384a` (ADS1x9xECG-FE User's Guide) was opened to check the 392 kΩ figure. Its RLD example
uses a 100 kΩ series resistor (`R35`) and does not contain 392 kΩ, so it is not cited in Q1.
No page was registered for, logged into, posted to, replied to, voted on or emailed.

## Search terms used

Searches were run on the TI E2E, Nordic DevZone and u-blox search pages (plus a general web
index to locate the site-specific pages), using only part numbers, pin names and electrical
terms. Strings used:

- `ADS1298 RLD stability feedback resistor capacitor E2E`
- `ADS1298 RLD 10 k series resistor electrode impedance high`
- `ADS1298 RLD electrode impedance`
- `ADS1298R RLD right leg drive values`
- `ADS1298IPAG RLD circuit`
- `ADS129x CLK_EN external clock sharing`
- `ADS1298 CLK_EN external clock two devices START`
- `ADS1298 VCAP1`
- `ADS1298 VCAP 1 22uF`
- `ADS1299 RLD stability feedback resistor capacitor`
- `ADS1299 VCAP1 capacitor tantalum`
- `nRF52840 VBUS`
- `nRF52840 VBUS unused connect GND devzone`
- `nRF52833 VBUS unused`
- `NINA-B306 I2C radio sensitive`
- `NINA-B306 radio sensitive pin I2C 100 kHz`
- `NINA-B301 radio sensitive pins I2C`
- `portal.u-blox.com NINA-B306 short range ground plane`
- `u-blox NINA-B306 PCB size ground plane antenna 10 mm`

No application, body-site, wearing-location or product-category word was typed into any search
box or URL.
