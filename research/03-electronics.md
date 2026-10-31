# Track 03 — Electronics: what an electrical engineer needs to build the board

*Research report for the silent-speech wearable project (personal R&D). Scope: biopotential
analog front-ends (AFEs) for surface EMG, speech-muscle sEMG requirements, MCU + BLE radio,
on-device inference, power/battery, open hardware to copy, safety, output transducers, plus a
block diagram and starter BOMs.*

## 0. Design targets this track has to hit

| Requirement | Target | Basis |
|---|---|---|
| Channels | 7–16 differential sEMG | AlterEgo 7 [2]; BioGAP-Ultra/SilentWear 16-channel acquisition [12][10] |
| Analog bandwidth | 20–450 Hz physiological | De Luca [14]; BioGAP-Ultra cites ">500 Hz bandwidth requirements of EMG" [12] |
| Sample rate | 1–2 kSPS; SilentWear ships 500 SPS | [15][16]; SilentWear 500 Hz, PGA gain 6 [10] |
| Resolution | 24-bit ΔΣ | ADS1299/ADS1298 family [1][24] |
| Input-referred noise | ≤4 µVpp; sub-µVrms preferred | ADS1298 4 µVpp [24]; ADS1299 0.14 µVrms @250 SPS, 65 Hz BW, G=24 [23] |
| CMRR | ≥90 dB min; 110–140 dB available | De Luca [14]; ADS1299 −110 dB [1]; AFE159RP4 −140 dB [34] |
| BLE | ≥1.4 Mbit/s demonstrated | BioGAP-Ultra [12] |
| Power | ~20.5 mW demonstrated for full on-device SSI | SilentWear [10] |
| Battery | 150 mAh LiPo gives 27.1 h | SilentWear [10] |

## 1. What AlterEgo actually did (primary sources, not press coverage)

The MIT Media Lab AlterEgo project [4], its IUI 2018 paper and the follow-on MEng thesis are
unusually specific, so the electronics can be copied almost line-for-line.

**Channels / electrodes (IUI 2018).** 7 target areas on the skin were selected from a 30-point
grid covering laryngeal, hyoid, buccal, mental, oral and infraorbital regions; signals are "sourced
as 7 channels" [2]. Two electrode versions were built: TPE plastic, gold-plated silver electrodes
with a 1.45 mm diameter conductive area used with Ten20 conductive paste, or passive dry Ag/AgCl
electrodes with a 4 mm diameter conductive area; the pasted electrodes gave "superior data quality"
and were used for the reported experiments [2]. A reference electrode sits on the wrist or earlobe,
and "bias based signal cancellation" handles ~60 Hz line interference [2].

**Analog chain (IUI 2018).** "The signals are sampled at 250 Hz and differentially amplified at
24× gain (Texas Instruments, OpenBCI)" [2]. OpenBCI's Cyton is an 8-channel ADS1299 board [75], so
this is the ADS1299 family at 250 SPS / PGA 24 [1][2]. A fourth-order IIR Butterworth band-pass of
1.3–50 Hz is applied (high-pass to prevent aliasing, low-pass for movement artifacts) plus a
hardware 60 Hz notch [2]. ICA removes movement artifacts, then rectification and normalisation to
0–1 [2]. An opto-isolated external trigger adds a channel of high-voltage pulses marking phrase
start/end [2]. Streams go over Bluetooth LE to a phone that forwards them to a server running the
classifier [2].

**Channels / electrodes (MEng thesis).** The thesis describes "8 signal electrodes" on the face and
neck with reference and bias on the earlobes (interchangeable) [3]. It confirms 250 Hz and reports
that subsets of the 8 electrodes achieve similar accuracy because nearby electrodes pick up similar
signals; neck electrodes 4–7 are correlated [3]. Preprocessing adds a 1st-order 0.5 Hz Butterworth
high-pass for DC drift, notch filters at multiples of 60 Hz, wavelet convolution for high-frequency
body noise, and a 0.5–8 Hz band-pass for the sequence-prediction task [3]. The CNN input window is
250 samples = 1 s at 250 Hz [3].

**Demonstrated vs claimed.** IUI 2018 reports "92% median word accuracy" on a digit test with 3
participants, ~5 h pilot data plus ~31 h of silently spoken text, without the user opening their
mouth [2]. The MIT FAQ repeats "over 90% accuracy on an application-specific vocabulary", notes the
system is user-dependent and needs individual training [5]. The follow-up MS/dysphonia study (3
patients, 10 trials × 15 sentences) reports mean test accuracy 0.81 and 203.73 bits/min [6][7].
These are small-vocabulary, user-specific results, not open-vocabulary dictation.

**Reality check.** 250 Hz / 1.3–50 Hz is below the classic 20–450 Hz sEMG band. If the owner's
classifier uses conventional sEMG features, plan for ≥1 kSPS and a wider front-end.

## 2. 2025–2026 state of the art: BioGAP-Ultra, SilentWear, textile headphones

The strongest current reference design is **BioGAP-Ultra** (ETH Zürich / Bologna, arXiv 2508.13728,
Aug 2025, rev. Dec 2025), an open-source modular biosignal platform [12]. Its **SilentWear**
follow-on (arXiv 2603.02847, Mar 2026) is essentially the target architecture for this project [10].

- **AFE:** two TI **ADS1298**, 8 channels each, 24-bit, giving 16 differential ExG channels plus
  bias/reference. Chosen for "4 µVpp" noise, "−115 dB" CMRR, "up to 32 kSPS … compatible with the
  >500 Hz bandwidth requirements of EMG", and "0.75 mW/channel" [12]. SilentWear configures them at
  **500 Hz, PGA gain 6** [10].
- **Compute + radio:** **GAP9** SoC (RISC-V; 15.6 GOP/s DSP, 32.2 GMAC/s ML at 370 MHz) plus an
  **nRF5340**, supporting up to **1.4 Mbit/s** BLE [12].
- **SilentWear results:** textile neck interface, 14 differential channels, 15k-parameter **SpeechNet**
  CNN running on GAP9; 84.8 ± 4.6 % (vocalized) / 77.5 ± 6.6 % (silent) across 8 HMI commands over
  multiple days, falling to 71.1 ± 8.3 % / 59.3 ± 2.2 % inter-session; incremental fine-tuning
  recovered >10 % with <10 min of user data; **63.9 µJ per inference, 2.47 ms latency, 20.5 mW total,
  >27 h on a 150 mAh Li-Po** [10].
- **Earlier neckband (Sensors 2025 / arXiv 2509.21964):** 14 dry channels + 4 bias, two ADS1298,
  nRF53, **22 mW**, high-pass 20 Hz + notch 50 Hz, 200 ms windows, random-forest classifier
  off-board; vocalized 87 ± 3 % / silent 68 ± 3 % (5-fold), falling to 64 ± 18 % / 54 ± 7 %
  leave-one-session-out [8][9].
- **Openness:** hardware and software at https://github.com/pulp-bio/BioGAP [13].

A second 2025 system (Cambridge) puts **four graphene/PEDOT:PSS textile electrodes into a headphone
earmuff**, read out by a **compact ESP32-S3 module**, and reports 96 % accuracy on 10 voice-free
control words with a 1D SE-ResNet adapting per-channel attention to variable skin–electrode
coupling [11]. This shows a 4-channel, dry, headphone-mounted montage can carry a small command
vocabulary.

## 3. sEMG signal-chain requirements (speech muscles)

**Bandwidth.** De Luca's Delsys reference: usable sEMG energy is "limited to the 0 to 500 Hz
frequency range, with the dominant energy being in the 50-150 Hz range", and his practical filter is
a **20–450 Hz** band-pass [14]. Low frequencies (<20 Hz) are dominated by movement artifact and
unstable motor-unit firing; high frequencies are mostly electrode/equipment noise [14]. No primary
source found usable speech-muscle sEMG information above 500 Hz — **unverified**. Silent-speech
systems band-limit at 20–450 Hz (Meltzner) or 30–500 Hz (Zhu) [16][17].

**Sample rate.** Nyquist plus an analog anti-alias low-pass is mandatory. 1 kSPS is the common floor
— Gaddy & Klein collect "eight channels ... at a sample rate of 1000 Hz" on an OpenBCI Cyton [15].
Meltzner oversampled at 20 kHz (Delsys Bagnoli) or 1926 Hz (Trigno Mini) with a 20–450 Hz analog
band (>40 dB/decade) [16]; SilentWear runs 500 Hz [10]. **1–2 kSPS** covers the cited bands with
realisable anti-alias filtering; a 4 kHz requirement was **not** established.

**Input-referred noise.** Facial sEMG is small — AlterEgo's 2020 paper says "under 100 microvolts"
[7] and IUI 2018 rejects spikes ">30 µV above baseline" [2]. Front-end bars: Delsys DE 2.1
"< 1.2 uV RMS (0-500 Hz)" [14]; Meltzner's sensors "<0.75 µV per channel" [16]; ADS1299 "1 µVPP
(70-Hz BW)" and 0.14 µVrms / 0.98 µVpp @250 SPS, 65 Hz BW, G=24 [1][23]; ADS1298 "4 μVPP (150 Hz BW,
G = 6)" [24][25]. Working target: **sub-µVrms to ≈1 µVrms over the signal band**, 20–40 dB below the
tens-of-µV facial signal (a rule of thumb from those specs, not one standard).

**Gain and ADC range.** ADS1299 offers **PGA 1, 2, 4, 6, 8, 12, or 24** with 24-bit ΔΣ [1]; AlterEgo
ran 24× [2]. OpenBCI Cyton quotes ±2.5 V input and 0.298 µV/bit [75]. Gain only needs to keep the
signal above the noise floor while leaving headroom for DC offset, drift and motion artifact —
AC coupling plus 24-bit dynamic range matters more than raw gain [1][75].

**CMRR, input impedance, dry electrodes.** De Luca: "A CMRR of 32,000 or 90 dB is generally
sufficient"; today's electronics reach 120 dB; input impedance of order "10^12 ohms in parallel with
5 picofarads"; the two detection sites must be impedance-matched [14]. ADS1299 bias current
**300 pA**, CMRR **−110 dB**, minimum DC input impedance **1 GΩ** with lead-off off (500 MΩ typical
with lead-off on) [1][23]. ADS1298 bias current **200 pA**, CMRR **−115 dB** [24][25]. Dry
electrodes raise and mismatch skin impedance (thousands of ohms to megohms), converting common mode
to differential and collapsing effective CMRR; active/voltage-follower electrodes (EEG glasses quote
input impedance "superior to 1 GΩ" [19]) fix this. For a dry, barely-visible face/neck device, budget
for active electrodes or accept a matching/CMRR penalty.

**Bias / driven-right-leg.** The ADS1299/ADS1298 bias amplifier "senses the common-mode voltage of a
selected set of electrodes and creates a negative feedback loop by driving the body with an inverted
common-mode signal" [1][18]. AlterEgo used "bias based signal cancellation" for ~60 Hz [2]. A
floating battery device still benefits, because interference couples capacitively/radiatively and
mismatch converts it to differential [18]. Put the reference on neutral/bony tissue (De Luca: large
"2 cm × 2 cm" [14]); AlterEgo used wrist/earlobe [2]; the 2020 MS build used reference + bias on
earlobes [7].

**Motion artifact.** Electrode–skin and cable movement produce artifact mostly "0 to 20 Hz" and can
dominate low-effort contractions; a 2 cm electrode shift changed sEMG RMS by "19 - 38%" in De Luca's
data, more than any filtering fixes [14]. Countermeasures: skin prep, fixed inter-electrode distance,
lightweight sensors, taped cables [14], 20 Hz high-pass, and adaptive filtering (accelerometer-
referenced variants exist) [20][21]. AlterEgo's 1.3 Hz high-pass preserved most motion artifact; ICA
carried that load [2][7].

**Powerline rejection.** De Luca calls 50/60 Hz the dominant ambient noise, "one to three orders of
magnitude greater than the EMG signal", and advises against notching because dominant EMG energy is
50–100 Hz [14]. AlterEgo notched at 60 Hz anyway because of the gentle Butterworth roll-off [2];
Gaddy & Klein notch 60 Hz and harmonics [15]. Battery-only operation removes the mains fault path but
**not** capacitively/radiatively coupled interference; CMRR, shielding and usually a notch are still
required [18].

**Demonstrated silent-speech numbers (electronics context).** Gaddy & Klein, silently *mouthed*:
8-ch Cyton @1 kSPS, 67-word closed vocabulary, open-vocabulary WER 68.0 % automatic / 74.8 % human
[15]. Meltzner, subvocal: 11 sensors, 20–450 Hz, 16-bit, 2,200-word vocabulary, 8.9 % WER (91.1 %
recognition) [16]. Zhu, high-density subvocal: 120 channels @2048 Hz, 30–500 Hz; best 10 electrodes
86 % English / 94 % Chinese [17]. Kumar, voiceless vowels: 3 facial channels, gain 1000, 8–79 Hz
band, 250 Hz [22]. These are **mouthed/subvocal/voiced**, not AlterEgo-style internal articulation.
Electronics conclusion: **8–16 channels at 1–2 kSPS, 20–450 Hz bandwidth, sub-µVrms noise** is the
defensible baseline; AlterEgo's chain is a special case for its own classifier.

## 4. Analog front-end (AFE) chips

| Part | Ch | Input-referred noise (conditions) | Gain | SPS/ch | Bits | CMRR | Power | Package | Price |
|---|---|---|---|---|---|---|---|---|---|
| **ADS1299** | 8/6/4 | 1 µVpp (70 Hz BW); 0.14 µVrms / 0.98 µVpp @250 SPS, 65 Hz BW, G=24 | 1–24 | 250–16 000 | 24 | −110 min / −120 typ | 39 mW typ, 42 max (8 ch, 5 V); 10 µW power-down | TQFP-64 | unverified (TI store out of stock) [1][23] |
| **ADS1298 / 1296 / 1294** | 8/6/4 | 4 µVpp typ / 7 max (150 Hz BW, G=6) | 1,2,3,4,6,8,12 | 250–32 000 | 24 | −105 min / −115 typ | ≈8.8–9.5 mW (8 ch, 3 V); 0.75 mW/ch feature | TQFP-64, BGA-64 | unverified [24][25] |
| **ADS1292/1292R** | 2 | 8 µVpp (150 Hz BW, G=6) | 1–12 | 125–8 000 | 24 | −105 min / −120 typ | 335 µW/ch feature | TQFP-32 / VQFN-32 | unverified |
| **Intan RHD2132** | 32 unipolar | 2.4 µVrms typ | fixed 192 V/V | ≤30 000 | 16 | 82 dB typ | 4.4–37.3 mW depending on BW/bus | QFN 8×8 mm | **$430** (1–24, QFN) [30] |
| **Intan RHD2164** | 64 unipolar | 2.4 µVrms typ | fixed 192 V/V | ≤30 000 | 16 | 82 dB typ | 6.7–53.1 mW examples | BGA 9×7 mm | **$534** BGA (out of stock indefinitely); bare die **$479** [30] |
| **RHS2116** | 16 stim+record | unverified | — | — | 16 | — | — | QFN / die | **$392** (1–24, QFN) [30] |
| **AD8232** | 1 ECG | 100 nV/√Hz @1 kHz; 14 µVpp 0.5–40 Hz | fixed 100 | no ADC (2 kHz BW) | analog | 80 dB | 170 µA typ ≈0.51 mW @3 V | LFCSP 4×4 | unverified [31] |
| **AD8233** | 1 ECG | 150 nV/√Hz @1 kHz | fixed 100 | no ADC (1 kHz BW) | analog | 80 dB | 50 µA typ ≈0.15 mW @3 V | WLCSP 2×1.7 mm | unverified [32] |
| **ADAS1000** | 5 ECG | 6 µVpp (G=2, 2 kHz, 0.5–40 Hz) | ×1.4–×4.2 | 2k/16k/128k | 24-bit word | −105 min / −110 typ | 27–41 mW | LFCSP-56 / LQFP-64 | unverified [33] |
| **AFE159RP4 (2024)** | 4 | 4 µVpp in 150 Hz BW | 1.25–9 | 125–128 000 | 24 | −140 dB (marketing bullet) | 0.42 mW/ch | VQFN-48, DSBGA-49 | out of stock, no public price [34] |

**Which to choose.** ADS1299 has the most flexible gain (1–24), which matters for small facial sEMG;
ADS1298/1294 explicitly list **EMG**, run to 32 kSPS and use less power per channel [1][24][25].
Both integrate the bias/RLD amplifier, lead-off detection and internal reference — which is why
OpenBCI Cyton and BioGAP-Ultra both use this family [12][75]. **Intan RHD2132/2164** give very low
noise (2.4 µVrms) and 32/64 channels per chip, but gain is **fixed at 192 V/V** and the chips are
quote-only, with the RHD2164 BGA "out of stock indefinitely" [26][27][28][29][30]. **AD8232/AD8233**
are single-lead heart-rate front ends: fixed gain 100, no ADC, and the AD8232 datasheet warns its
narrow-band filtering "distorts the ECG waveform significantly" [31][32]. **ADAS1000**'s 2 kHz-mode
digital low-pass tops out at 450 Hz — not a wideband EMG front end [33]. **AFE159RP4** (datasheet
Nov 12 2024) is TI's low-power 2024 successor line: 4-ch, 0.42 mW/ch, 4 µVpp, −140 dB CMRR,
125 SPS–128 kSPS, but only 6 selectable electrodes and gain 1.25–9; the full datasheet is
request-only and the part is out of stock [34].

**Cerelog does not make an AFE chip.** "Cerelog ESP1" does not exist. Cerelog sells the **ESP-EEG**
board: 8-channel (16-channel advertised) 24-bit **ADS1299** plus an **ESP32**, USB-C/BLE streaming to
BrainFlow/LSL/OpenBCI GUI, with closed-loop active bias (driven-right-leg) [35]. Launch price
**$389.99** (list $649.99). Cerelog states it is "not a medical device" and **has no isolation
circuitry**, warning users to run it only from a battery-powered laptop that is not charging [35].
Treat it as a ready-made bench front-end and a cautionary safety example.

**Newer 2024–2026 parts.** Only the TI AFE159x family. No newer Intan RHD silicon was found
(RHD2000-series datasheet updated 8 Dec 2023) [27]; no Chinese AFE datasheet could be verified
(**unverified**); ADI/Maxim MAX30001/MAX30003 single-lead bio AFEs exist but were not spec-verified.

## 5. Electrode interface, input protection and references

*Impedance figures below come mostly from ECG/sEMG/EEG work, not facial sEMG specifically.*

**Electrode types and impedance.** Wet Ag/AgCl gel electrodes are the lowest and most stable
(electrode pair ≈100 Ω over 24–391 kHz; clinical rule of thumb "EII < 10 kΩ at 1 kHz" for wet
sites), which is why AlterEgo preferred pasted gold-plated silver over dry [2][103][104]. Dry
stainless/gold/metallised-textile PCB plates have actual skin impedance "typically in the kΩ
ranges" [103][104]; conductive silicone is in the tens of kΩ (one study measured 39.43 kΩ for a
silicone dry electrode vs 0.025–300 kΩ for a commercial dry elastomer) [102]. Capacitive/non-contact
plates add a series coupling capacitance whose reactance balloons at low frequency, so they demand a
very high AFE input impedance [103]. Microneedle arrays reach normalized electrode–skin impedance
0.98 kΩ·cm² at 1 kHz and 1.50 kΩ·cm² at 10 Hz [101]. Subdermal needles/wires make direct ohmic
contact (Pt/SUS/Au; no skin-barrier impedance) [105].

**Input impedance / bias current.** ADS1299: DC input impedance **1000 MΩ** without lead-off and
**500 MΩ** with 6 nA lead-off, input capacitance **20 pF**, input bias current **±300 pA** (25 °C and
−40…85 °C) [1][23]. 300 pA across 100 kΩ is ~30 µV DC error — tolerable only because it is offset,
not noise. The low-bias benchmark is the obsolete **INA116**: 3 fA typ at 25 °C, 25 fA at 85 °C,
differential input impedance >10^15 Ω / 0.2 pF, ±40 V over-voltage protection [97]. Intan RHD2000
quotes individual-amplifier |Zin| **1300 MΩ at 10 Hz, 13 MΩ at 1 kHz**, Ib **<20 pA**, Cin 12 pF,
CMRR 82 dB, plus a dedicated VESD pin for input protection [27]. The **ADA4530-1** is widely quoted as
a femtoampere electrometer, but its datasheet was not retrievable — **unverified**, no number
asserted.

**Input protection.** ADS1299 inputs are diode-clamped to the rails: "limit the input current to
10 mA or less if the analog input voltage exceeds AVDD + 0.3 V or is less than AVSS − 0.3 V" [23].
Standard practice is a series resistor per input plus a differential cap; the ADS1299EEG-FE uses
**5 kΩ** input resistors, which TI says contribute ~**0.67 µVpp in 65 Hz bandwidth** [98]. A 10 kΩ
series + 1 nF C0G gives a ~16 kHz pole (fine for sEMG) but is **unverified as an exact
TI-recommended pair**; the verified anchor is the 5 kΩ EVM value [98]. There is a direct trade-off:
10 kΩ × 300 pA = 3 µV of bias-current offset, 100 kΩ gives 30 µV, so series resistance must be
minimised for dry electrodes. SBAA188 uses a **100 kΩ** protection resistor to keep fault current
under the IEC 50 µA limit (100 kΩ minimum at 5 V) [18]. For ESD, a low-leakage low-capacitance TVS
such as **TPD2E001** (1.5 pF typ, 1 nA max leakage, ±8 kV contact / ±15 kV air IEC 61000-4-2) is
suitable, but its 1 nA leakage already exceeds the ADS1299's 300 pA bias current — place it after the
series resistor and accept the leakage [99]. Defibrillation-grade input (not needed for a personal
rig and not safe to self-apply) uses a high-voltage series resistor, a TVS, and back-to-back ~7 V
zeners behind a 10 kΩ resistor [100].

**Reference and bias for a face/neck montage.** Options: a single reference electrode on mastoid/bony
neck tissue, or the ADS1299 SRB1/SRB2 pins that route a common signal to many inputs for a
referential montage [1]. The bias/RLD electrode should sit on electrically quiet tissue away from the
active muscles and is driven through the 100 kΩ-class protection resistor; the RLD amplifier's Rf/Cf
sets loop gain and stability (SBAA188: Rf = 1 MΩ, Cf = 1.5 nF, RCM = 220 kΩ on ADS1298) [18].
IEC 60601-1 patient auxiliary current limits are **100 µA normal / 500 µA single-fault (a.c.)** and
**10 µA / 50 µA (d.c.)** [107].

**Multiplexing many electrodes onto one AFE.** Time-division multiplexing N electrodes across C AFE
channels reduces per-electrode rate to `f_ADC × C / N`. With ADS1299 at 250 SPS–16 kSPS and 8
channels [1], 32 electrodes at 1 kSPS aggregate gives only 250 samples/s/electrode — enough for a
rectified sEMG envelope, not the full 20–450 Hz band. Parallel per-channel sampling (e.g. RHD2164's
64 unipolar inputs) avoids the hit at the cost of channels [27]. Published face/neck sEMG montages
use bipolar pairs over zygomaticus major, risorius, orbicularis oris superior/inferior, mentalis,
depressor anguli oris, levator labii superioris and digastric [108].

**Subdermal safety at skin level.** Common materials are silver, silver-chloride, tin, gold, platinum
or stainless steel [105]. Anything that pierces the skin is legally a medical device (FDA has cleared
disposable/reusable subdermal needle electrodes under 510(k) K130136), and an unapproved piercing
electrode is a regulatory plus infection/injury risk [106]. The realistic hobbyist path is dry
surface PCB-plate or capacitive electrodes with insulated leads and no skin penetration; a subdermal
prototype is **unverified** for non-clinical use and its material/insulation/sterility hazards
outrank the electronics.

## 6. MCU, radio and on-device inference

**Nordic.** nRF52840: 64 MHz Cortex-M4F (FPU), 1 MB flash + 256 KB RAM, BLE 5.4, 2 Mbps PHY,
802.15.4/Thread/Zigbee, +8 dBm TX, −95 dBm sensitivity [36]. nRF5340: dual Cortex-M33 — 128/64 MHz
application core with 1 MB flash + 512 KB RAM, plus a 64 MHz network core with 256 KB flash + 64 KB
RAM; BLE 5.4, 2 Mbps, LE Audio, 101 CoreMark/mA on the network core [37]. nRF54L15: 128 MHz
Cortex-M33, 1.5 MB NVM + 256 KB RAM, BLE 6.0 features plus a proprietary 4 Mbps mode, always-on
global RTC "0.8 uA (3.0 V)" [38]. nRF54H20: multiple Cortex-M33 up to 320 MHz, 2 MB NVM + 1 MB RAM;
EEMBC ULPMark-CM 170 at 515 CoreMark; radio RX 2.0 mA, −100 dBm BLE RX at 1 Mbps, up to +10 dBm TX
[39]. Nordic "2× processing power" claims are marketing [38]. Sleep currents of 0.4 µA (nRF52840)
and ~0.9 µA (nRF5340) are community figures, **unverified** here. Nordic prices were not verified.

**Espressif.** ESP32-S3: dual Xtensa LX7 up to 240 MHz, 512 KB SRAM, BLE 5 LE with 2 Mbps and Coded
PHY, no 802.15.4; vector instructions via ESP-NN/ESP-DSP [40]. Measured ESP32-S3-WROOM-1: 8.14 µA
deep sleep, 23.88 mA active [41]. ESP32-C6: 160 MHz HP RISC-V + 20 MHz LP core, BLE 5.3 + 802.15.4,
7 µA deep sleep [42]. ESP32-H2: 96 MHz RISC-V, BLE 5.3 + 802.15.4, 7 µA deep sleep, 25 µA light
sleep [43]. Espressif's own BLE demo gets **720–767 kbps on the 1 Mbps PHY** [44]. LCSC single-unit
reference price for ESP32-S3-WROOM-1-N16: **$3.6513** (other prices unverified).

**Ambiq (always-on TinyML).** Apollo4: Cortex-M4F 192 MHz, up to 2 MB MRAM / 1.8 MB RAM, BLE 5
2 Mbps (Blue only), claimed 3 µA/MHz [46]. Apollo510: Cortex-M55 250 MHz with Helium MVE, 4 MB NVM,
3.75 MB SRAM; vendor claims up to 30× better efficiency than a typical Cortex-M4 (marketing) [47].
Apollo510B adds BLE 5.4 via a coprocessor; sampling in 2025 [47].

**BLE throughput math.** Raw bit rate = N × 24 bit × fs (derived):

| N | 1 kHz | 2 kHz |
|---|---|---|
| 8 | 192 kbps | 384 kbps |
| 16 | 384 kbps | 768 kbps |
| 32 | 768 kbps | 1,536 kbps |

The 1 Mbps PHY tops out at 720–767 kbps measured [44]; the 2M PHY "tops out around 1.4 Mbps"
measured [45]. So 8ch@1–2 kHz and 16ch@1 kHz fit the 1 Mbps PHY; 16ch@2 kHz and 32ch@1 kHz sit at
its ceiling and need the 2M PHY; 32ch@2 kHz (1.536 Mbps) exceeds the ~1.4 Mbps 2M ceiling. Design
consequence: **on-device inference and BLE transport of labels/features, not raw 16-ch waveforms,
is the right architecture** — exactly what SilentWear does [10].

**On-device inference.** TensorFlow Lite for Microcontrollers runs on MCUs/DSPs with limited memory
[48]; CMSIS-NN provides optimised int8/int16 kernels for Cortex-M (M0/M3 pure C, M4/M33 DSP, M55/M85
Helium) [49]; Edge Impulse exports a C++/EON library [50]; Arm Ethos-U55/U65 add microNPU
acceleration to Cortex-M-class SoCs [51]. None of the Nordic/Espressif parts above integrate an
Ethos-U. SilentWear demonstrates the target: a 15k-parameter int8 CNN on GAP9 at **2.47 ms and
63.9 µJ per inference** [10]. The earlier neckband ran the classifier off-board and streamed raw
data at 22 mW [9].

**Latency.** Surface EMG precedes articulatory motion, giving a theoretical head start [9]. SilentWear's
on-device loop is 500 Hz acquisition + 2.47 ms inference + BLE label transport [10]. A derived
budget for the owner's system: ~100–200 ms analysis window + single-digit-ms inference + negligible
label transport + audio synthesis. Streaming raw 16-ch/1 kHz/200 ms = 9.6 kB, ~100 ms at 768 kbps or
~55 ms at 1.4 Mbps before inference [10][12]. Published end-to-end silent-speech-to-audio latency was
not found (**unverified**).

## 7. Power budget and battery

**Demonstrated whole-system budgets** (best evidence available):

| System | Channels | Power | Battery / life |
|---|---|---|---|
| SilentWear, on-device CNN + BLE results [10] | 14 | **20.5 mW** | 150 mAh Li-Po → **27.1 h** |
| ETH dry neckband, raw BLE streaming [9] | 14 | **22 mW** | — |
| BioGAP-Ultra EMG sleeve [12] | 16 | 26.7 mW | 150 mAh |
| BioGAP-Ultra EEG-PPG headband / ECG chestband [12] | 16 / — | 32.8 / 9.3 mW | 150 mAh |

**Component anchors.** ADS1299 (8 ch, 5 V) draws 39 mW typ / 42 max, 10 µW power-down [23]; ADS1298
(8 ch, 3 V) ≈8.8–9.5 mW, i.e. 0.75 mW/ch [24][25]. A generic 8 Ω bone-conduction shaker rated 1 W
RMS draws ~118 mW while driven at 100 mW with 85 % class-D efficiency [52]. MicroSD active current
was not verified (10–50 mA typical, **unverified**).

**Worked budget (miniaturised board, derived).** 14× ADS1298 channels at 500 SPS ≈ 5–9 mW + nRF5340
CPU ≈ 5–11 mW + BLE at low duty ≈ 1 mW + bone-conduction audio at ~5–10 % duty ≈ 6–12 mW +
regulator/gauge losses ≈ 0.3 mW → **≈20–30 mW**, matching SilentWear's measured 20.5 mW [10]. A bench
board that streams raw data and logs to microSD will be ~2–4× that (~60–90 mW).

**Battery options.**

| Cell | Capacity | Size / mass |
|---|---|---|
| LiPo pouch | 100 mAh | 11.5 × 31 × 3.8 mm, 3 g [54] |
| LiPo pouch | 150 mAh | 19.75 × 26.02 × 3.8 mm, 4.65 g [53] |
| LiPo pouch | 500 mAh | 29 × 36 × 4.75 mm, 10.5 g [55] |
| CR2032 primary | 220 mAh | 20 × 3.2 mm, 3.1 g [56] |
| CR2450 primary | 610 mAh | 24 × 5.0 mm, 6.5 g [56] |
| LIR2450 rechargeable | 120–200 mAh | CR2450-size [EEMB/UTMEL, **unverified**] |

CR2032's standard discharge is **0.2 mA** and its maximum pulse is **20 mA** (2 s pulse); Murata
warns >10 mA drain causes large voltage drop [56]. A ~20 mW / 6.8 mA board therefore cannot run on a
coin primary; use a 150 mAh LiPo.

**Runtime arithmetic.** At 20.5 mW: 150 mAh × 3.7 V = 555 mWh → **27.1 h** [10]; at 90 mW: 555/90 =
**6.2 h**. For all-day (16 h) wear at 20.5 mW the need is 20.5 × 16 = 328 mWh ≈ **89 mAh**, so a
150 mAh cell covers a full day with margin [10][53]; the bench prototype needs ≥300–400 mAh.

**Regulators / charging / gauge.** Use a low-Iq buck (TPS62840, 60 nA Iq) for 3.3 V and a low-Iq LDO
(TPS7A02, 25 nA Iq) for the analogue rail [57][58]; USB-C charge with MCP73831 (15–500 mA
programmable) or BQ25100 (10–250 mA, 75 nA max battery leakage, JEITA via NTC) [59][60]; fuel-gauge
with MAX17048 (3 µA hibernate) [61]. Gate SD/LED rails and keep radio duty low.

**Thermal / skin safety.** IEC 62368-1 adopts ISO 13732-1 touch-temperature limits: for contact
>1 min the TS1 maximum is **48 °C** for metal and plastic; TS2 is +10 K (58 °C) and requires a
safeguard [62]. Keep the worn cell and charger below 48 °C. IEC 62133-2:2017 is the safety standard
for secondary Li-ion cells/batteries in portable applications [63]. Charge only from USB/5 V SELV —
never expose a worn device to mains.

## 8. Open hardware to copy

| Board | Channels / AFE | Sample rate | Interface | Price / kit | Licence | Available 2024–2026 |
|---|---|---|---|---|---|---|
| **OpenBCI Cyton** | 8 ch (16 with Daisy), TI ADS1299, 24-bit, 0.298 µV/bit | 250 Hz default (link-limited) | RFDuino BLE + USB dongle | **$1,249** board; +Daisy 16-ch **$2,499** | open source; design files on GitHub | in stock [75][96] |
| **OpenBCI Ganglion** | 4 ch, Microchip MCP3912 + AD8237 buffers | 200 Hz | BLE 4.n | **$624.99** (dongle separate) | open source; KiCad + BOM | in stock [76] |
| **PiEEG-8 / -16 / IronBCI** | 8 or 16 ch, ADS1299, 24-bit | 250 SPS–16 kSPS SPI; 250 SPS BLE (IronBCI) | RPi 40-pin SPI; BLE5 | $350 / $390 / $420 | MIT SDK; hardware files on GitHub | in stock [81][82] |
| **ardEEG** | Arduino UNO R4 WiFi shield, ADS1299 family | 250 SPS examples | Arduino UNO R4 WiFi | $350 | open-source repo (licence unverified) | in stock [83][84] |
| **HackEEG** | 8 ch/shield ADS1299; up to 32 ch with 4 shields | ≤16 kSPS (8 ch), 4 kSPS (32 ch) | USB 2.0 HS via Arduino Due | $495–$2,090 (historical) | CERN OHL v1.2 | **discontinued**; files public [77][78] |
| **FreeEEG32 (NeuroIDSS)** | 32 ch, 4× ADI AD7771, 24-bit | ≤128 kSPS; firmware optimised to 512 SPS ×32 | USB, STM32H743 | $199 (historical) | AGPL | **discontinued** [79][80] |
| **BioAmp EXG Pill** | 1 ch analog, no dedicated AFE, 10^12 Ω input Z | host ADC | analog out | ~$25 (unverified) | open hardware + software | in stock [85] |
| **OpenEMG** | 1 ch analog (LM324 + ICL7660) | 20–500 Hz band-pass | analog out | DIY PCB | open hardware (KiCad) | files available (2019) [86] |
| **MyoWare 2.0** | 1 ch analog EMG, raw + envelope, G=200 | 20.8–498.4 Hz | analog out | **$42.95** | open-source hardware repo | in stock [87] |
| **TI ADS1299EEG-FE** | 8 ch ADS1299, 24-bit + PGA | ADS1299 rates | USB + eval software | not shown (unverified) | TI eval terms | orderable [88] |

**AlterEgo replication: none exists.** No complete open-hardware build was found. The only public
reproduction is a partial DSP simulator of the first processing stage (FastICA), MIT-licensed, with
no hardware [89]. Treat "open AlterEgo hardware" as non-existent; the nearest complete build is
BioGAP-Ultra/SilentWear [10][12][13]. OpenBCI has no dedicated EMG board — its docs tell you to use
Cyton or Ganglion with snap electrodes plus a driven ground/reference [95]. For a fast bench
prototype: **Cyton/Daisy** (Arduino-IDE programmable, proven with AlterEgo and Gaddy), **Cerelog
ESP-EEG** (cheapest 8-ch ADS1299), or **ardEEG/IronBCI** for STM32/Arduino ecosystems [35][75][81][83].

## 9. Safety

**Battery-only isolation vs mains.** Surface electrodes plus a mains-referenced supply create a
conductive path from mains to the body. Battery power removes that path and lets the front end float.
OpenBCI specifies "3-6 V DC Battery ONLY" [75]; PiEEG states the device "must operate only from a
battery … MUST not be connected to any kind of mains power, via USB or otherwise", requiring full
galvanic isolation from mains [81]; HackEEG is battery-only and has "no patient isolation
circuitry" [77]. **Rule: never mains while worn; treat any USB/charger cable as mains-referenced
unless galvanically isolated.**

**IEC 60601-1 patient leakage limits (guidance).** Type B — 100 µA normal condition (NC) / 500 µA
single-fault condition (SFC); Type BF — 100 µA / 500 µA; Type CF — 10 µA / 50 µA. Clause 8.7 covers
patient, enclosure and earth leakage; the single-fault test includes mains voltage on an applied part
[90]. These figures come from a secondary summary because IEC 60601-1 itself is paywalled; verify
against the standard. For a genuinely battery-only device the mains-on-applied-part test is moot,
but if a charger could ever be attached while worn, design so a single fault cannot put mains on the
electrodes.

**Particular standards.** IEC 60601-2-26 (EEG) includes defibrillation-protection test figures
(201.101/201.102) [92]. IEC 60601-2-40:2024, 3rd ed., applies to electromyographs and evoked-response
equipment and excludes TENS/EMS stimulators (covered by IEC 60601-2-10); a pure sensing sEMG device
is closer to 60601-2-40 [91]. IEC 62133-2:2017 (amended 2021) covers portable sealed secondary
lithium cells/batteries [63].

**ESD and defibrillation protection.** IEC 60601-1-2 points to IEC 61000-4-2; the 4th edition raises
contact discharge to ±8 kV and air to ±15 kV [94]. Clinical EEG/EMG inputs also need defibrillation
protection because the patient may be defibrillated while connected [92]. Series resistors on every
electrode input, plus clamps/TVS diodes or gas-discharge tubes across the isolation barrier, limit
fault current into the AFE; TI demonstrates GDTs plus digital isolators passing 15 kV contact ESD
[94]. Size series resistors against the ADS1299 absolute-maximum input current and the datasheet
input-protection guidance [1][23].

**Skin temperature and current density.** IEC 60601-1 clause 11.1 covers excessive temperatures for
long-term applied parts (secondary sources; the standard is paywalled). The commonly cited 41 °C surface limit for prolonged
contact is **unverified** here. IEC 60601-1 is a leakage-current standard, not a general electrode
current-density standard; keep bias/excitation currents low and do not add stimulation to a sensing
build. A numeric current-density limit is **unverified**.

**Practical hobby rules (ranked).** (1) Battery only; never on a mains charger while electrodes are
on skin [75][77][81]. (2) Charge with electrodes disconnected (a separate, non-worn operation) [87].
(3) Do a single-fault analysis: open neutral, open earth, reversed polarity, mains-to-electrode short
via the charger [90]. (4) Fuse/protect the battery; use cells tested to IEC 62133-2 [63]. (5) If you
must connect to a PC or bench gear, use a USB isolator; bench instruments fall under IEC 61010-1,
not 60601 [93][94]. (6) Put series resistors + ESD clamps on every electrode input [94].
(7) Keep electrode bias current low; no stimulation in a sensing build [91].

## 10. Output channel: bone conduction and in-ear audio

**Bone-conduction transducers.** No vendor publishes a true bone-conduction *output* datasheet as
openly as the in-ear parts. The clearest public part is the generic Adafruit 1674 / "C2049": 8 Ω,
14 × 21.5 mm, 9.6 g, 1 W RMS / 2 W max, Re 5.8 Ω, Le 1.26 mH, 300–19,000 Hz (varies with the surface
it is pressed against), Fs 1,600 Hz, "90.1 dB 1W/1m", **$8.95** [52]. This is a surface voice-coil
shaker, not a mastoid-optimised hearing-aid receiver. **Sonion** lists a bone-conduction vibrator but
publishes no numbers (**unverified**) [Sonion]. **Knowles**' public "bone conduction" product is the
V2S200D vibration *sensor*, not an output transducer — the "Knowles BCD" premise is **unverified**
[Mouser/52audio]. Shokz does not publish transducer specs [iFixit teardown, **unverified**].

**In-ear / MEMS options.** Knowles **WBFK-30095-000** balanced armature: 13.8 Ω, "97.00 dBA"
efficiency at 1 mW, 200 Hz–7.4 kHz, 5.16 × 3.51 mm [70]. PUI **AS01508AO-SC-R** micro speaker: 8 Ω,
700 mW rated / 1 W max, 550 Hz–20 kHz, "84.00 dBA" at 100 mW/100 mm, 15 × 11 mm, 3.9 mm high [71].
**xMEMS Cowell** (solid-state MEMS): 22 mm³, 56 mg, "111 dB SPL @1 kHz / 30 Vpp", 3.2 × 1.15 × 6.0 mm
plus the Aptos high-voltage amp; **Sycamore**: ~1 mm thin, <150 mg, 8.41 × 9.0 × 1.13 mm [68][69].
xMEMS parts need the dedicated Aptos amplifier, not a standard class-D [68].

**Driver ICs.** MAX98357A (I2S input, class-D, 3.2 W into 4 Ω / 1.8 W into 8 Ω at 5 V, click/pop
reduction) is the simplest digital-in path [64]. PAM8302A (analog in, 2.5 W into 4 Ω / 1.5 W into
8 Ω, 4 mA Iq) is the cheap breakout path [65]. TPA2028D1 adds AGC/DRC/limiter (880 mW into 8 Ω at
3.6 V, 1.8 mA) for hardware volume limiting [66]; SSM2377 is a low-EMI class-D (1.4 W into 8 Ω at
5 V, 92 % efficiency, 100 nA shutdown) [67]. Recommended: **BLE MCU → I2S → MAX98357A → 8 Ω shaker**
for the bench, and **TLV320AIC3104 → TPA2028D1** when AGC and analog limiting are needed [64][66].

**Bone conduction vs in-ear for speech in noise.** BC has low interaural separation from cross-head
transmission. In the Swedish Matrix Test with 20 normal-hearing adults, spatial release from masking
was **3.21 dB for unattenuated BC vs 7.16 dB for air conduction**; attenuating cross-head
transmission by 5 dB raised it to 5.46 dB and 10 dB to 6.47 dB [72]. So BC output is materially
worse than in-ear for speech-in-noise unless cross-talk is reduced — relevant because the owner
wants a barely-visible device, which pushes toward an in-ear or custom receiver anyway.

**Practical.** DC-block the output (the PAM8302 inputs are already 1.0 µF AC-coupled) [65]; use
click/pop suppression [64][67]; limit volume with TPA2028D1's AGC/DRC [66]. **Contact pressure**, not
just SPL, is the BC safety issue: capillary-closure pressure at the mastoid is ~3.7 kPa, while
measured headband pressures were 17 kPa (B71) and 11 kPa (BC461) — well above closure, risking
pressure sores [73]. NIOSH's recommended exposure limit is 85 dBA as an 8-h TWA with a 3-dB exchange
rate, but that is an airborne metric, not a validated BC dose (**unverified** as applied to a
shaker) [74]. Use the least pressure that holds the device and vary position.

## 11. Proposed block diagram and starter BOMs

```
                 FACE / NECK ELECTRODES (7-16 differential + REF + BIAS)
                          │  active electrodes or shielded leads
                          ▼
   ┌──────────────────────── AFE ────────────────────────┐
   │  2 × ADS1298 (16 ch, 24-bit, up to 32 kSPS,         │
   │  0.75 mW/ch, -115 dB CMRR)  or  1 × ADS1299 (8 ch)  │
   │  PGA gain 6-24 · bias/RLD amplifier · SPI           │
   └───────────────┬─────────────────────────────────────┘
                   │ SPI (3.072 Mbit/s at 16 ch × 16 kSPS, or 192 kbit/s at 16 ch × 500 SPS)
                   ▼
   ┌────────── MCU + inference ──────────┐        ┌──── BLE ────┐
   │ nRF5340 (BLE 5.4) + GAP9, or        │ ─────► │ phone / PC  │  raw data (bench)
   │ nRF54L15 / ESP32-S3 / Apollo510     │        └─────────────┘
   │ int8 CNN (TFLM / CMSIS-NN / EON)    │        ┌──── BLE ────┐
   │ on-device, ~2.5 ms, ~64 µJ/infer    │ ─────► │ host: LLM   │  labels/text
   └───────────────┬─────────────────────┘        └──────┬──────┘
                   │ I2S                                  │ text
                   ▼                                      ▼
   ┌── audio output ────────────┐              ┌── assistant response ──┐
   │ MAX98357A class-D (or      │              │ phone/PC LLM, TTS      │
   │ TLV320AIC3104 + TPA2028D1) │◄─────────────┤ over BLE (LE Audio/LC3)│
   │ → 8 Ω bone-conduction      │   I2S/audio  └────────────────────────┘
   │   shaker or in-ear receiver│
   └────────────────────────────┘
   Power: 150 mAh LiPo → PMIC/charger (MCP73831/BQ25100)
          → TPS62840 buck 3.3 V → TPS7A02 LDO analogue rail; MAX17048 gauge
   Safety: battery-only when worn; never mains-connected; 48 °C skin limit
```

**(a) Bench prototype BOM (off-the-shelf, copy AlterEgo/Gaddy).**

| Item | Part | Qty | Rough cost | Notes |
|---|---|---|---|---|
| sEMG front-end | OpenBCI Cyton (8-ch ADS1299) | 1 | **$1,249** [75] | proven AlterEgo/Gaddy chain; +Daisy for 16 ch = $2,499 |
| — cheaper bench option | Cerelog ESP-EEG (8-ch ADS1299 + ESP32) | 1 | **$389.99** [35] | no isolation; battery-laptop only |
| — 4-ch option | OpenBCI Ganglion (MCP3912) | 1 | **$624.99** [76] | lower channel count |
| Electrodes | Ag/AgCl pre-gelled or gold-plated + Ten20 | ~10 | ~$20–50 (unverified) | AlterEgo used 1.45 mm gold + paste [2] |
| Host BLE | Nordic nRF52840 DK or ESP32-S3 DevKit | 1 | ~$10–50 (unverified) | for prototyping only |
| Audio | MAX98357A breakout + 8 Ω BC shaker | 1 each | **$5.95 + $8.95** [64][52] | |
| Power | 500 mAh LiPo + USB charger board | 1 | ~$10–15 (unverified) | bench runtime ~6 h |
| **Bench total** | | | **≈$1,300 (OpenBCI)** or **≈$450 (Cerelog)** | |

**(b) Miniaturised custom board BOM (one-off, indie quantities).**

| Item | Part | Qty | Rough cost | Notes |
|---|---|---|---|---|
| AFE | ADS1298IPAG (or ADS1299IPAG) | 1–2 | unverified (TI store out of stock) | 16 ch at 500 SPS, PGA 6, 0.75 mW/ch [10][12][25] |
| MCU + BLE | nRF5340 (or nRF54L15 / ESP32-S3) | 1 | ~$6–12 (unverified) | 2 Mbps PHY; 1 MB/512 KB [37][38] |
| AI accelerator (optional) | GAP9, or run int8 CNN on MCU | 1 | quote (unverified) | SilentWear uses GAP9 + nRF5340 [10] |
| Audio amp | MAX98357A | 1 | ~$2 (unverified; breakout $5.95) | I2S class-D [64] |
| Transducer | 8 Ω bone-conduction shaker, or Knowles BA / xMEMS | 1 | **$8.95** [52] / quote | |
| Power mgmt | TPS62840 + TPS7A02 + MCP73831 + MAX17048 | 1 set | ~$5–8 (unverified) | 60 nA / 25 nA / 500 µA / 3 µA [57][58][59][61] |
| Battery | 150 mAh LiPo | 1 | ~$6 (unverified) | 27 h at 20.5 mW [10][53] |
| Electrodes | dry/active or subdermal | 8–16 | depends | electrode track is separate |
| PCB + assembly | 4-layer rigid-flex, one-off | 1 | ~$100–300 (unverified) | rigid-flex for face/neck |
| **Board total (excl. NRE)** | | | **≈$150–400** | + EE time |

## Sources

1. Texas Instruments, "ADS1299 data sheet, product information and support" — https://www.ti.com/product/ADS1299 (product page; datasheet Rev. C, Jan 2017).
2. A. Kapur, S. Kapur, P. Maes, "AlterEgo: A Personalized Wearable Silent Speech Interface," IUI 2018, pp. 43–53 — PDF https://dam-prod.media.mit.edu/x/2018/03/23/p43-kapur_BRjFwE6.pdf (2018).
3. E. Wadkins, "A Continuous Silent Speech Recognition System for AlterEgo, a Silent Speech Interface," MEng thesis — http://www.ericwadkins.com/doc/MEng_Thesis_FINAL.pdf .
4. MIT Media Lab, "AlterEgo — Project Overview" — https://www.media.mit.edu/projects/alterego/overview/ .
5. MIT Media Lab, "AlterEgo: Frequently Asked Questions" — https://www.media.mit.edu/projects/alterego/frequently-asked-questions/ .
6. A. Kapur, U. Sarawgi, E. Wadkins, M. Wu, N. Hollenstein, P. Maes, "Non-Invasive Silent Speech Recognition in Multiple Sclerosis with Dysphonia," PMLR 116:25–38, 2020 — https://proceedings.mlr.press/v116/kapur20a.html .
7. Same paper, full PDF — https://andymatuschak.org/files/papers/Kapur%20et%20al%20-%202020%20-%20Non-Invasive%20Silent%20Speech%20Recognition%20in%20Multiple%20Sclerosis%20with%20Dysphonia.pdf .
8. F. Meier, G. Spacone, S. Frey, L. Benini, A. Cossettini, "A Parallel Ultra-Low Power Silent Speech Interface based on a Wearable, Fully-dry EMG Neckband," Sensors 2025 slides — https://pulp-platform.org/docs/sensors2025/GiusySpacone_sensors_PULP.pdf (21.10.2025).
9. Same authors, arXiv:2509.21964 (26 Sep 2025) — https://arxiv.org/abs/2509.21964 .
10. G. Spacone et al., "SilentWear: an Ultra-Low Power Wearable System for EMG-based Silent Speech Recognition," arXiv:2603.02847 (v2, Mar 2026) — https://arxiv.org/abs/2603.02847 ; HTML https://arxiv.org/html/2603.02847v2 .
11. C. Tang et al., "Wireless Silent Speech Interface Using Multi-Channel Textile EMG Sensors Integrated into Headphones," arXiv:2504.13921 (Apr 2025) — https://arxiv.org/abs/2504.13921 .
12. S. Frey et al., "BioGAP-Ultra: A Modular Edge-AI Platform for Wearable Multimodal Biosignal Acquisition and Processing," arXiv:2508.13728 (v2, Dec 2025) — https://arxiv.org/abs/2508.13728 ; HTML https://arxiv.org/html/2508.13728v2 .
13. PULP BioGAP open-source hardware/software — https://github.com/pulp-bio/BioGAP .
14. C. J. De Luca, "A Practicum on the Use of Surface EMG Signals in Movement Sciences," Delsys (2008) — https://bme.unc.edu/wp-content/uploads/sites/917/2022/11/EMG_explanation.pdf .
15. D. Gaddy, D. Klein, "Digital Voicing of Silent Speech," EMNLP 2020 — https://aclanthology.org/2020.emnlp-main.445.pdf .
16. G. S. Meltzner et al., "Development of sEMG sensors and algorithms for silent speech recognition," J. Neural Eng. 15 046031 (2018) — https://beta.iopscience.iop.org/article/10.1088/1741-2552/aac965/ampdf .
17. M. Zhu et al., "Towards optimizing electrode configurations for silent speech recognition based on high-density surface electromyography," J. Neural Eng. 18 016005 (2021) — https://beta.iopscience.iop.org/article/10.1088/1741-2552/abca14/pdf .
18. V. Acharya, "Improving Common-Mode Rejection Using the Right-Leg Drive Amplifier," Texas Instruments SBAA188 (2011) — https://www.ti.com/lit/an/sbaa188/sbaa188.pdf .
19. R. Zanetti, A. Aminifar, D. Atienza, "EEG glasses for real-time brain electrical activity monitoring," Scientific Reports 15:43574 (2025) — https://pmc.ncbi.nlm.nih.gov/articles/PMC12698764/ .
20. "Study on Motion Artifact Denoise of Surface Electromyographic Signals Based on Adaptive Filtering Method," DAPIC 2025 — https://www.computer.org/csdl/proceedings-article/dapic/2025/361600a101/26LpVL5b6Fy .
21. "Acceleration driven adaptive filter to remove motion artifact from EMG recordings in Whole Body Vibration," University of Naples Federico II — https://www.iris.unina.it/handle/11588/314440 .
22. S. Kumar, D. K. Kumar, M. Alemu, "Applicability of Facial EMG in HCI and Voiceless Communication," ICINCO 2005 — https://www.scitepress.org/Papers/2005/11550/11550.pdf .
23. Texas Instruments, "ADS1299-x … datasheet (Rev. C)," SBAS499C (2017) — https://www.ti.com/lit/ds/symlink/ads1299.pdf .
24. Texas Instruments, "ADS1298 data sheet, product information and support" — https://www.ti.com/product/ADS1298 .
25. Texas Instruments, "ADS129x Low-Power, 8-Channel, 24-Bit Analog Front-End for Biopotential Measurements datasheet (Rev. K)," SBAS459 (2015) — https://www.ti.com/lit/ds/symlink/ads1298.pdf .
26. Intan Technologies, "RHD Electrophysiology Amplifier Chips" — https://intantech.com/products_RHD2000.html .
27. Intan Technologies, "RHD2000 Series Digital Electrophysiology Interface Chips datasheet" (updated 8 Dec 2023) — http://intantech.com/files/Intan_RHD2000_series_datasheet.pdf .
28. Intan Technologies, "RHD2164 Digital Electrophysiology Interface Chip datasheet" (updated 1 Dec 2017) — http://intantech.com/files/Intan_RHD2164_datasheet.pdf .
29. Intan Technologies, "RHA2000 vs. RHD2000 Product Comparison" (2012) — http://intantech.com/files/Intan_RHA2000_RHD2000_comparison.pdf .
30. Intan Technologies, "Orders and Pricing (RHD / RHA / RHS chips)" — https://intantech.com/pricing.html?tabSelect=RHDChips .
31. Analog Devices, "AD8232 Single-Lead, Heart Rate Monitor Front End datasheet (Rev. D)" (2020) — https://www.analog.com/media/en/technical-documentation/data-sheets/AD8232.pdf .
32. Analog Devices, "AD8233 … Heart Rate Monitor for Wearable Products datasheet (Rev. D)" (2020) — https://www.analog.com/media/en/technical-documentation/data-sheets/AD8233.pdf .
33. Analog Devices, "ADAS1000/ADAS1000-1/ADAS1000-2 … Five Electrode ECG Analog Front End datasheet (Rev. D)" (2024) — https://www.analog.com/media/en/technical-documentation/data-sheets/ADAS1000_1000-1_1000-2.pdf .
34. Texas Instruments, "AFE159RP4 data sheet, product information and support" (datasheet Rev. A, Nov 12 2024) — https://www.ti.com/product/AFE159RP4 .
35. Cerelog, "Cerelog ESP-EEG | 8-Channel ADS1299 Biosensing Board for Researchers" — https://www.cerelog.com/eeg_researchers.html .
36. Nordic Semiconductor, "nRF52840" — https://www.nordicsemi.cn/products/nrf52840/ (and EN product page https://www.nordicsemi.com/Products/nRF52840 ).
37. Nordic Semiconductor, "nRF5340" — https://www.nordicsemi.cn/products/nrf5340/ .
38. Nordic Semiconductor, "nRF54L15" — https://www.nordicsemi.cn/products/nrf54l15/ .
39. Nordic Semiconductor, "nRF54H20" — https://www.nordicsemi.cn/products/nrf54h20/ .
40. Espressif Systems, "ESP32-S3 Wi-Fi & BLE 5 SoC" — https://www.espressif.com/en/products/socs/esp32-s3 .
41. Espressif, "Current Consumption Measurement of Modules (ESP32-S3)," ESP-IDF v6.0.1 — https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32s3/api-guides/current-consumption-measurement-modules.html .
42. Espressif Systems, "ESP32-C6 Series Datasheet v1.5" (HTML, 2025) — https://documentation.espressif.com/esp32-c6_datasheet_en.html .
43. Espressif Systems, "ESP32-H2-WROOM-02C Datasheet v1.2" (HTML, 2025) — https://documentation.espressif.com/esp32-h2-wroom-02c_datasheet_en.html .
44. Espressif, "ESP-IDF BLE throughput GATT client demo" README — https://raw.githubusercontent.com/espressif/esp-idf/5b2fa1a5ad534adcbdced44b0b334d636518133c/examples/bluetooth/bluedroid/ble/ble_throughput/throughput_client/README.md .
45. Ezurio, "Achieving 3.3 Mbps Throughput with ESB on the BL54L15: Beyond BLE Limits" (2026) — https://www.ezurio.com/resources/blog/achieving-3-3-mbps-throughput-with-esb-on-the-bl54l15-beyond-ble-limits .
46. CNX Software, "3µA/MHz Ambiq Apollo 4 MCU targets battery-powered IoT devices with voice processing" (2020) — https://www.cnx-software.com/2020/09/17/ambiq-apollo-4-mcu-3%c2%b5a-mhz/ .
47. CNX Software, "Ambiq Apollo510 Arm Cortex-M55 MCU delivers up to 30x better power efficiency for AI/ML workloads" (2024) — https://www.cnx-software.com/2024/03/28/ambiq-apollo510-arm-cortex-m55-mcu-delivers-up-to-30x-better-power-efficiency-for-ai-ml-workloads/ .
48. TensorFlow, "TensorFlow Lite for Microcontrollers" README — https://raw.githubusercontent.com/tensorflow/tflite-micro/main/README.md .
49. Arm, "CMSIS-NN" README — https://raw.githubusercontent.com/ARM-software/CMSIS-NN/main/README.md .
50. Edge Impulse, "Deployment" documentation — https://docs.edgeimpulse.com/studio/projects/deployment .
51. Arm, "Ethos-U55 NPU" — https://www.arm.com/products/silicon-ip-cpu/ethos/ethos-u55 .
52. Adafruit, "Bone Conductor Transducer with Wires — 8 Ohm 1 Watt" (PID 1674) — https://www.adafruit.com/product/1674 .
53. Adafruit, "Lithium Ion Polymer Battery — 3.7 V 150 mAh (PID 1317)" — https://www.adafruit.com/product/1317 .
54. Adafruit, "Lithium Ion Polymer Battery — 3.7 V 100 mAh (PID 1570)" — https://www.adafruit.com/product/1570 .
55. Adafruit, "Lithium Ion Polymer Battery — 3.7 V 500 mAh (PID 1578)" — https://www.adafruit.com/product/1578 .
56. Murata, "Coin Manganese Dioxide Lithium Battery Technical Note (TCN-CR-002-E)" (2021) — https://www.murata.com/-/media/webrenewal/products/batteries/micro/cr/tcn-cr-001-200722.ashx .
57. Texas Instruments, "TPS62840 60-nA IQ step-down converter" — https://www.ti.com/product/TPS62840 .
58. Texas Instruments, "TPS7A02 25-nA IQ LDO" — https://www.ti.com/product/TPS7A02 .
59. Microchip, "MCP73831/2 datasheet (DS20001984G)" (2014) — https://ww1.microchip.com/downloads/en/DeviceDoc/20001984g.pdf .
60. Texas Instruments, "BQ25100 250-mA single-cell Li-Ion charger" — https://www.ti.com/product/BQ25100 .
61. Analog Devices/Maxim, "MAX17048/MAX17049 datasheet" (2016) — https://www.analog.com/media/en/technical-documentation/data-sheets/MAX17048-MAX17049.pdf .
62. UL, "IEC 62368-1 Technical Brief: Touch Temperature Limits" (2010) — https://japan.ul.com/wp-content/uploads/sites/27/2014/06/1_techbrief_touchtemp.pdf .
63. IEC, "IEC 62133-2:2017" — https://webstore.iec.ch/en/publication/32662 .
64. Adafruit, "Adafruit MAX98357 I2S Class-D Mono Amp" — https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp ; product https://www.adafruit.com/product/3006 .
65. Adafruit, "Adafruit Mono 2.5W Class D Audio Amplifier — PAM8302" — https://www.adafruit.com/product/2130 .
66. Texas Instruments, "TPA2028D1" (datasheet Rev. C, 2015) — https://www.ti.com/product/TPA2028D1 .
67. Analog Devices, "SSM2377" — https://www.analog.com/en/products/ssm2377.html ; datasheet mirror https://en.sekorm.com/doc/3282144.html .
68. EDOM Technology, "Cowell — MEMS Speaker" — https://edomtech.com.cn/product-detail/cowell-mems-speaker/ .
69. EDOM Technology, "Sycamore" — https://edomtech.com.cn/product-detail/mems-loud-speakers-sycamore/ .
70. Knowles WBFK-30095-000 product listing (ichome) — https://ru.ichome.com/product-detail/knowles/wbfk-30095-000 .
71. PUI Audio AS01508AO-SC-R product listing — https://i-ic.com/Products/AS01508AO-SC-R.html .
72. S. Stenfelt, H. Jalalkamali, S. Surendran, "Enhanced interaural separation improves spatial release from masking in bilateral bone conduction hearing," Frontiers in Audiology and Otology (2026) — https://www.frontiersin.org/journals/audiology-and-otology/articles/10.3389/fauot.2026.1771617/full .
73. G. Raicevich, E. Burwood, H. Dillon, "Bone conductors, signals and sores," ICA 2010 — https://research.manchester.ac.uk/en/publications/bone-conductors-signals-and-sores/ .
74. CDC/NIOSH, "Understanding Noise Exposure Limits" (2016) — https://www.cdc.gov/niosh/bulletin/2016/noise.html .
75. OpenBCI, "Cyton Specs" — https://docs.openbci.com/Cyton/CytonSpecs/ ; price https://shop.openbci.com/products/cyton-biosensing-board-8-channel .
76. OpenBCI, "Ganglion Specs" — https://docs.openbci.com/Ganglion/GanglionSpecs/ ; price https://shop.openbci.com/products/ganglion-board .
77. Starcat, "HackEEG — ADS1299 Shield" README — https://raw.githubusercontent.com/Hobbit13/hackeeg-shield/master/README.md .
78. Crowd Supply, "HackEEG" campaign — https://www.crowdsupply.com/starcat/hackeeg .
79. Crowd Supply, "FreeEEG32" campaign — https://www.crowdsupply.com/neuroidss/freeeeg32 .
80. GitHub, "FreeEEG32-beta" README — https://raw.githubusercontent.com/neuroidss/freeeeg32-beta/master/README.md .
81. PiEEG, "Hardware" product page — https://www.pieeg.com/hardware .
82. GitHub, "ironbci" README — https://raw.githubusercontent.com/pieeg-club/ironbci/master/README.md .
83. GitHub, "ardEEG" README — https://raw.githubusercontent.com/pieeg-club/ardEEG/master/README.md .
84. Elecrow, "ardEEG" product page — https://www.elecrow.com/ardeeg.html .
85. Upside Down Labs, "BioAmp EXG Pill" documentation — https://docs.upsidedownlabs.tech/hardware/bioamp/bioamp-exg-pill/index.html .
86. C. Grassin, "OpenEMG Arduino Sensor" (2019) — https://charleslabs.fr/en/project-OpenEMG+Arduino+Sensor ; https://github.com/CGrassin/OpenEMG .
87. SparkFun, "Getting Started with the MyoWare 2.0 Muscle Sensor Ecosystem" — https://learn.sparkfun.com/tutorials/getting-started-with-the-myoware-20-muscle-sensor-ecosystem/all .
88. Texas Instruments, "ADS1299EEGFE-PDK Evaluation board" — https://www.ti.com/tool/ADS1299EEGFE-PDK .
89. GitHub, "Partial DSP implement of AlterEgo Paper" README — https://raw.githubusercontent.com/joaocarvalhoopen/Partial_DSP_implement_of_AlterEgo_Paper/master/README.md .
90. Compatible Electronics, "Leakage Current Testing Services" (secondary source quoting IEC 60601-1 clause 8.7 Type B/BF/CF limits) — https://compatible-electronics.com/product-safety-testing/leakage-current-testing .
91. SFS Suomen Standardit, "IEC 60601-2-40:2024" abstract (3rd ed., Dec 2024) — https://store.sfs.fi/en/iec-60601-2-40-2024 .
92. EVS, "EVS-EN IEC 80601-2-26:2020+A1:2024" standard preview — https://www.evs.ee/StandardDownload/DownloadPreview?productId=155130&language=EnglishLanguage .
93. SIS, "IEC 61010-1:2010+AMD1:2016 CSV" — https://www.sis.se/en/produkter/testing/electrical-and-electronic-testing/iec6101012010amd12016csv .
94. Texas Instruments, "IEC60601-1-2 Compliant Digital Isolation Design With 16-kV Contact Discharge ESD Protection" (SLLA608, Feb 2023) — https://www.ti.com/document-viewer/lit/html/SLLA608/GUID-58F97F99-4F98-4C9F-952F-E132DCC37B01 .
95. OpenBCI, "Setting up for EMG" — https://docs.openbci.com/GettingStarted/Biosensing-Setups/EMGSetup/ .
96. OpenBCI, "For Developers" (open-source design files, MIT-licensed materials) — https://docs.openbci.com/ForDevelopers/ForDevelopersLanding/ .
97. Burr-Brown/TI, "INA116 Ultra Low Input Bias Current Instrumentation Amplifier datasheet (SBOS034)" (1995) — https://www.ti.com/lit/ds/symlink/ina116.pdf .
98. Texas Instruments, "ADS1299EEG-FE EEG Front-End Performance Demonstration Kit User's Guide (SLAU443B)" (2016) — https://www.ti.com/lit/pdf/SLAU443 .
99. Texas Instruments, "TPD2E001 Dual 1.5-pF, 5.5-V, ±8-kV ESD Protection Diode" — https://www.ti.com/product/TPD2E001 ; datasheet https://www.ti.com/lit/ds/symlink/tpd2e001.pdf .
100. GliaX, "Defibrillator Protection Circuitry Design Notes" — https://raw.githubusercontent.com/GliaX/ecg/refs/heads/master/Documentation/Defib_Style_1.md .
101. Li et al., "High-Performance Flexible Microneedle Array as a Low-Impedance Surface Biopotential Dry Electrode," Nano-Micro Letters — https://nmlett.org/index.php/nml/article/download/1123/1848/3470 .
102. Han et al., "Evaluation of a silicone-based flexible dry electrode for measuring human bioelectrical signals," Biomed Eng Lett 15:563–574 (2025) — https://pmc.ncbi.nlm.nih.gov/articles/PMC12011699/ .
103. Y. M. Chi, T.-P. Jung, G. Cauwenberghs, "Dry-Contact and Noncontact Biopotential Electrodes: Methodological Review," IEEE Rev. Biomed. Eng. 3:106–119 (2010) — https://doi.org/10.1109/RBME.2010.2084078 .
104. R. Kusche, S. Kaufmann, M. Ryschka, "Dry electrodes for bioimpedance measurements — design, characterization and comparison," Biomed. Phys. Eng. Express 5(1) (2018) — https://doi.org/10.1088/2057-1976/aaea59 .
105. M. Mendes, "Evaluating the electrode measurement sensitivity of subdermal electroencephalography electrodes," MSc thesis (2017) — https://fenix.tecnico.ulisboa.pt/downloadFile/563345090412943/MMendes_MScThesis.pdf .
106. FDA 510(k) K130136, "Disposable and Reusable Subdermal Needle Electrodes" — https://fda.innolitics.com/device/K130136 .
107. IEC 60601-1 patient leakage/auxiliary current excerpt in an FSP CB certificate (ed. 3.2) — https://www.fsp-ps.de/download/product/001715/SAFETY/FSP400M-70PD,FSP500M-80PD_CB_60601_cert_(ed_3.2)_SFD-00009236-R01.pdf .
108. "Predicting 3D lip shapes using facial surface EMG," PLOS ONE, Fig. 1 (2017) — https://journals.plos.org/plosone/article/figure?id=10.1371/journal.pone.0175025.g001 .

## Key takeaways for the build

- **Copy SilentWear/BioGAP-Ultra, not AlterEgo, for the analog chain.** Two ADS1298 (16 differential
  channels, 24-bit, 0.75 mW/ch, −115 dB CMRR) at 500 SPS / PGA 6 is a published, open, working
  configuration; AlterEgo's 250 Hz / 1.3–50 Hz ADS1299 chain is a special case [2][10][12][25].
- **Use the ADS1298/ADS1299 family; avoid AD8232/AD8233 and ADAS1000.** The ADI parts are
  heart-rate/ECG front ends with fixed gain 100, no ADC, and band limits ≤450 Hz [31][32][33]. Intan
  RHD gives more channels and lower noise but fixed gain 192 V/V and is now quote-only [26][30].
- **Target 20–450 Hz, 1–2 kSPS, sub-µVrms, CMRR ≥90 dB (≥110 dB preferred).** These are the
  De Luca / published silent-speech numbers [14][15][16]; add an analog anti-alias filter and a
  bias/RLD electrode [1][18].
- **Do the inference on-device and stream labels, not raw 16-channel waveforms.** 16 ch × 24 bit ×
  1 kHz = 384 kbps fits BLE 1 Mbps, but 16 ch × 2 kHz = 768 kbps is at its measured ceiling; a
  15k-parameter int8 CNN runs in 2.47 ms / 63.9 µJ on GAP9 [10][44][45].
- **Pick the MCU for edge AI, not just BLE: nRF5340 + GAP9 (proven), nRF54L15/ESP32-S3/Apollo510
  (alternatives).** CMSIS-NN/TFLM/Edge Impulse support all of them [37][38][40][47][48][49][50].
- **Power target ≈20 mW; 150 mAh LiPo gives >27 h.** That covers all-day wear with margin and is
  measured, not extrapolated [10][53]. A bench board will draw 2–4× and needs a bigger cell.
- **Never power a worn board from mains.** Battery-only operation, USB/SELV charging only, and keep
  skin contact below 48 °C; IEC 60601 leakage limits are the safety benchmark and IEC 62133-2 covers
  the cell [62][63]. Cerelog's own warning (no isolation, battery laptop only) is the cautionary
  example [35].
- **The output is the weak link for discrete wear.** Bone conduction buys invisibility but costs
  ~4 dB of spatial release from masking vs air conduction and needs contact pressures far above
  capillary closure for a tight fit; an in-ear receiver or a low-pressure temple contact is the safer
  engineering trade [72][73].
- **Add accelerometer-referenced adaptive filtering and active electrodes** to survive motion
  artifact and dry-skin impedance mismatch; a 2 cm electrode shift costs 19–38 % sEMG RMS [14][19][20].
- **Calibrate per session, not per lifetime.** SilentWear loses ~13 points (vocalized) and ~18 points
  (silent) when the neckband is repositioned between sessions, and recovers >10 % with <10 min of
  user data — budget for that workflow in the electronics (easy re-pairing, on-device fine-tuning)
  [10].

## Open questions

- **Exact AFE for the miniaturised board:** ADS1298 vs the 2024 AFE159RP4 (better noise/CMRR/power
  but gain only 1.25–9, request-only datasheet, out of stock) — needs a TI sample request to decide
  [25][34].
- **Is 500 Hz sampling enough for the owner's silent articulation**, or does the classifier need
  1–2 kSPS and >500 Hz bandwidth? Depends on whether the model uses conventional sEMG features [10][12][14].
- **Dry vs active vs subdermal electrodes:** none of the electronics sources covers the subdermal
  option; that trade (skin impedance, safety, longevity) belongs to track 04/06 and must feed back
  into the input-protection design.
- **Latency budget for the closed loop:** published end-to-end silent-speech-to-audio latency was not
  found; the owner will have to measure acquisition window + inference + LLM + TTS + audio.
- **Bone-conduction coupling and safety numbers** (max safe BC output, EN 50332/IEC 62368 numeric
  limits for a shaker) are unverified; confirm with the transducer vendor before committing to BC.
- **Prices for the custom board** (ADS1298/AFE159, MCU, PCB assembly) are unverified because
  distributor pages block automated access; get quotes.

