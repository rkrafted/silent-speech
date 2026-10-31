# Track 10 — Fast-track data: buying used acquisition hardware now + synthetic/transferable EMG data

*Research report for the silent-speech wearable project (personal R&D). Part A: where to buy
used/refurbished biopotential acquisition hardware in the EU today, at what price, and which unit
fits 8–16 ch sEMG at ≥1 kHz with low latency. Part B: what is published on synthetic and
transferable data for silent-speech EMG — augmentation, generative EMG from audio/text, audio/TTS
as a substitute for the user's own voice, LLM-generated prompt corpora, and cross-language transfer
for Latvian/Russian.*

**Deadline framing.** The build must work by 2026-12-31. Hardware must be in hand within weeks, and
no part of the data pipeline can depend on something not already published with numbers. Every
figure below is quoted as the source gives it; claims that could not be checked to a primary source
are marked **unverified**.

---

## Part 0. Bottom line

1. **Stock OpenBCI cannot do 8–16 ch at ≥1 kHz.** The Cyton streams **250 SPS** over the dongle;
   Cyton+Daisy averages adjacent samples for ~**125 SPS** per channel. Higher rates needed the
   **WiFi Shield, which OpenBCI no longer sells** [4][5][7] — yet the 1 kHz reference dataset was
   recorded exactly that way, over WiFi [1].
2. **Used OpenBCI is priced close to new** ($1,800–$2,150 vs $2,499) [15][17][18][19]. The cheap
   path to 16 ch @ ≥1 kHz is the **PiEEG-16 ($390)** — SPI 250 SPS–16 kSPS, 24-bit, gain 1–24, MIT
   open source [32]; **Cerelog ESP-EEG ($389.99)** is the assembled EU-vendor option [33].
3. **Repositioning dominates real-world accuracy, not channel count.** SilentWear's 14-channel dry
   neckband scores **84.8 ± 4.6 %** (vocalized) / **77.5 ± 6.6 %** (silent) cross-validated, falling
   to **71.1 ± 8.3 % / 59.3 ± 2.2 %** across sessions; **<10 minutes** of new data recovers **>10 %**
   accuracy [2].
4. **LLM rescoring is the single biggest published lever.** MONA LISA cut silent-EMG WER from 28.8 %
   to **12.2 %** and vocal from 23.3 % to **3.7 %** [63]; HyPoradise cut ATIS from 8.3 % to **1.7 %**
   [99]. **No silent-speech EMG paper found uses an external LM to rescore decoder output.**
5. **Synthetic EMG from multi-speaker audio works for voiced EMG** (CoM2S: 54.21 % → **8.75 %** WER
   on multi-speaker Libri-EMG, **1:1** real:synthetic optimal) [65], **but nobody has trained a
   silent-speech decoder on audio-synthesised EMG**: audio→EMG tops out at **CCC 0.663** / envelope
   correlation **0.66** [68][69], and voiced→silent transfer fails at **88 %+ WER** [1]. TTS replaces
   the *audio target*, not the *EMG input* [66].
6. **Latvian/Russian speech data are adequate; cross-language silent-speech evidence is absent.**
   Latvian has **282.4 h** and a Whisper-large fine-tune at **3.2 % WER** (normalized CV19 test);
   Russian Common Voice v8.0 has **162.44 h / 1,970 speakers** [114][115]. No cross-language **sEMG**
   silent-speech study exists [123].

---

## Part A. Used acquisition hardware available in the EU now

### A.1 Requirements this hardware has to satisfy

The reference silent-speech dataset — Gaddy & Klein's Berkeley corpus — used an **OpenBCI Cyton,
8 channels at 1000 Hz**, gold-plated electrodes with Ten20 paste, a shared reference behind one ear
and the Cyton bias pin behind the other, transmitted to a computer over WiFi [1]. The 2025–2026
wearable state of the art moved to **14 fully-differential dry channels** in a textile neckband
[2][3].

| Requirement | Target | Basis |
|---|---|---|
| Channels | 8 minimum, 14–16 preferred | 8 ch in [1]; 14 ch in [2][3] |
| Sample rate | 1000 Hz achieved in the reference dataset | "Eight channels are collected at a sample rate of 1000 Hz" [1] |
| Latency | Single-digit ms demonstrated on-device | SilentWear: **2.47 ms**, **63.9 µJ** per inference; **20.5 mW** total, **>27 h** on battery [2] |
| Electrodes | gel (Ten20) for data quality; dry acceptable with per-session recalibration | [1]; [2] |

**8 channels is already enough to reproduce the reference dataset**; 16 is comfort margin. What
actually costs accuracy is re-donning the sensor (see B.6).

### A.2 OpenBCI Cyton / Daisy / Ganglion — the spec blocker

OpenBCI's ADS1299 front end is fed by an RFduino BLE radio and an FTDI serial link. The docs:
*"For the sample rate, we set the default rate to 250 Hz. Faster rates are supported by the ADS1299,
but the RFDuino wireless link and the serial limits might not be able to keep up with faster sample
rates"* [4]. The forum reproduces the SDK warning: *"IMPORTANT! The Cyton with USB Dongle cannot and
will not stream data over 250SPS. Plug in the WiFi Shield to get speeds over 250SPS streaming. You
may still write to an SD card though, the firmware will not send EEG data over the Bluetooth
radios"* [5]. The WiFi Shield was removed from the shop; higher-rate SD logging was a custom mod from
an older firmware generation that was "never integrated into the mainline firmware code" [5].

**Cyton + Daisy degrades further.** Both ADS1299s sample at 250 SPS, but packets alternate between
the chips and OpenBCI **averages the current and most recent channel values** before transmitting;
the first sample is invalid, and OpenBCI "highly recommends" SD-card logging of raw data for
16-channel work [4]. A separate thread reports the effective per-channel streaming rate falls to
**125 Hz** [7]. That rules out low-latency real-time decoding for Daisy over the dongle. At 250 SPS
Nyquist is 125 Hz, but the reference feature set splits each channel at **134 Hz** and computes
high-band power and zero-crossing-rate features on the upper band [1] — a 250 SPS stream cannot
represent that band.

Official Cyton hardware facts: ADS1299 AFE, PIC32MX250F128B MCU, RFduino BLE radio, LIS3DH
accelerometer, micro-SD slot, input range +2.5 to −2.5 V, **SNR 121 dB**, **0.298 µV/bit**, default
gain 24× giving **0.02235 µV/count**, gains 24/12/8/6/4/2/1× [6]. The Daisy is an ADS1299 daughter
card taking 8 → 16 channels, needs an external **2.048 MHz** clock from the Cyton, and the published
design contains a documented PCB error [6]. The dongle is an RFduino + FTDI FT231XQ-R — the simplest
authenticity check [6][25].

**Official new prices** (OpenBCI shop JSON, USD, records dated 2026-10-01; OpenBCI states roughly
**+25 % EU import tax**) [8]–[14]:

| Item | New price (USD) |
|---|---|
| Cyton 8-channel | $1,249.00 [8] |
| Cyton + Daisy 16-channel | $2,499.00 [9] |
| Daisy module upgrade | $1,249.00 [10] |
| Ganglion 4-channel | $624.99 [11] |
| Ganglion BLE dongle | $19.99 [12] |
| Galea headset | $42,980.00 [13] |
| Galea Neon eye-tracking add-on | $10,900.00 [14] |

**Observed second-hand asking prices.** No confirmed *sold* price was found — every figure is an ask,
so real transaction prices are probably lower [15]–[21]:

| Item | Ask | Where / when |
|---|---|---|
| Cyton 8-ch + dongle + 9 electrodes + battery holder + home-made headgear | **$800 + shipping** | Sweden, Jun 2026 [15] |
| 8-ch neurotechnologist bundle | **£1,100** | Newcastle UK, Aug 2025 [16] |
| Cyton + Daisy 16-ch + pre-wired EEG cap + case | **$1,800 OBO** ($900 offered for boards + dongle without cap) | San Diego, Apr 2026 [17] |
| 16-ch bundle | **$3,000 CAD (~$2,150)** | Canada, Sep 2026 [18] |
| Full Cyton + Daisy all-in-one R&D bundle | **$2,800 AUD** | Australia, Jul 2024 [19] |
| Ganglion, unused | ~**$400** each; 2 for $600, 3 for $800 | Apr 2023 [20] |
| "Cyton" knockoff | **$200 OBO** | AliExpress, Mar 2024 [21] |

**The Ganglion is not a workaround.** It is 4 channels sampled at **200 Hz**, with an **MCP3912**
front end and a **Simblee** BLE radio, and its micro-SD slot is explicitly **"Not supported"** [11][43].
Four channels at 200 Hz cannot carry speech-grade sEMG. The forum's own guidance is that 250 Hz is
adequate for on/off muscle detection but that EMG research "standard practices… require sampling
rates of a few kHz" [5]. Ganglion resolution is **0.1788 µV/bit**, and it draws **14 mA idle / 15 mA
streaming** [43].

**The clone warning is also a roadmap warning.** A maintainer's reply in the clone thread states the
Chinese boards fail because they "depend upon the WiFi Shield board. That board was removed from the
Shop pending re-engineering. **It never worked reliably with Cyton**" — the suspected cause being
Cyton firmware overdriving the ESP8266 and causing supply dips — and that the clone maker "just
added a capacitor and never even tested his system". The same post notes "A 'Cyton V2' is on the
todo list, which will include up to date wireless support, so no 'Shield' needed", but it is queued
behind the Galea project [21]. The WiFi Shield's Cyton documentation was moved to a deprecated
section in February 2025 [21]. **Do not plan around a Cyton V2 arriving before 2026-12-31.**

### A.3 ADS1299 dev boards — the cheapest route to 16 ch @ ≥1 kHz

The **ADS1299** itself easily exceeds the target: 8-channel (also 4-/6-ch), 24-bit,
simultaneous-sampling ΔΣ, **"Input-Referred Noise: 1 µVPP (70-Hz BW)"**, **"Data Rate: 250 SPS to
16 kSPS"**, **"CMRR: –110 dB"**, programmable gain 1/2/4/6/8/12/24, SPI, status ACTIVE [26]. The
bottleneck is never the silicon; it is the link and firmware.

The **TI ADS1299EEGFE-PDK** is the official demo kit and requires the **MMB0** modular EVM
motherboard for USB; its user guide lists "Real-time data processing" under **"Features Not
Supported in Current Version"** and requires **Windows XP SP2** ("Windows Vista and Windows 7 are
NOT supported") [28]. It is an evaluation tool, not a streaming front end. TI shows "Order now" but
no public price [27]; a distributor lists it ACTIVE at ₹32,073.44 (~US$385, FX unverified) [29].
Mouser, Digi-Key, Farnell, RS and Octopart bot-blocked this research, so EU stock and EUR price are
**unverified**.

**PiEEG-8 ($350) and PiEEG-16 ($390)** are Raspberry Pi ADS1299 shields advertising **"SPI 250 SPS to
16 kSPS", "24-bit resolution per channel"**, gain 1–24, **MIT open source**, sold via Elecrow [32].
PiEEG's own homepage says "up to 500 Hz", which conflicts with its hardware page — treat the exact
sustainable rate as **unverified** until measured [32]. **HackEEG** is the best *design*: "DMA
drivers can read and transfer eight channels of 24-bit resolution data at up to **16,000 samples per
second**… 32 channels can be read at **4,000 samples per second**", USB 2.0 HS, LSL, open schematics
— but every kit on its Crowd Supply page is "No longer available" [30]; Mouser EU lists Starcat
CS-HACKEEG-02 with price unverified [31].

### A.4 Cerelog, BioAmp, MindRove, BITalino

- **Cerelog ESP-EEG (Spain), $389.99** (list $649.99): **8 differential channels + 1 active bias**,
  ADS1299, **250 SPS default**, ESP32-WROOM-DA, USB-C plus WiFi/BT, **open-source firmware, software
  and schematic**, LSL and Brainflow compatible, 16-channel variant listed [33][34][35]. Closed-loop
  active bias is a genuine hum-rejection plus. It ships **non-isolated** and Cerelog warns it must
  run from a battery-powered laptop, never a mains-powered desktop [33]. Whether the open firmware
  exposes ≥1 kHz is **unverified**.
- **MindRove Armband 2 (Hungary), $799**: 8 EMG channels ("8 + 2" electrodes), **500 SPS**, 24-bit,
  **bandwidth 0–250 Hz**, WiFi, C++/C#/Python/MATLAB SDK and LSL [36]. The only turnkey EU wearable
  here, but **fails the ≥1 kHz requirement**.
- **BioAmp (Upside Down Labs)**: every product is **single-channel**. EXG Pill ("No. of channels:
  1", input impedance 10¹² Ω, ~$35/board) [37]; Muscle BioAmp Shield v0.3 ("No. of channels 1",
  fixed gain ×2420, band-pass **72–720 Hz**, Arduino UNO) [38]. Multichannel means N boards plus an
  external ADC. **Ceiling: 1 channel per board.**
- **BITalino (PLUX, Portugal)**: **"Sampling Frequency 1, 10, 100 or 1000 Hz"**, **"Resolution
  10-bit (A1–A4) + 6-bit (A5 & A6)"**, 4 analog ports [39]. Board $245 [40], muscleBIT (4× EMG)
  $445 [41]. **Ceiling: 4 channels at 1 kHz, 10-bit** — too few channels and coarse for sEMG.
- **ADS1298 vs ADS1299 for EMG**: ADS1298 is faster (250 SPS–32 kSPS) but noisier — **4 µVPP (150 Hz
  BW, G = 6)** vs **1 µVPP (70 Hz BW)** — so for surface sEMG the ADS1299 is the better front end,
  and its 16 kSPS ceiling already covers 8 ch at 1 kHz [26][42].

**Recommendation.** Buy **PiEEG-16 ($390) + Raspberry Pi 5** now as the stopgap [32]; **Cerelog
ESP-EEG ($389.99)** if an EU vendor and assembled board matter, budgeting a firmware task to raise
the 250 SPS default [33][34]. Use **HackEEG** as the custom-PCB reference [30]. For the final board:
two daisy-chained ADS1299 + STM32/ESP32 with USB-HS or BLE [26][30][32].

### A.5 Research-grade: TMSi, g.tec, Biosemi, Delsys

**Used research-grade EMG is possible but illiquid in the EU.** Across TMSi, g.tec, BioSemi and
Delsys, only **two live used asking prices** were found in the entire search: a **Noraxon Ultium at
€7,200** on Kleinanzeigen [60] and a **Noraxon TeleMyo DTS 7-K MR at 1,782 zł (~€415)** in a Polish
leasing sale [130]. eBay.de, LabX, Bimedis, EquipNet and DOTmed all returned **HTTP 403** to
automated fetching, so no verified used price exists for the four main vendors [136][137].

| System | Ch | Max rate | New price | Used seen | Licence/dongle risk |
|---|---|---|---|---|---|
| TMSi SAGA | 32/64/128 +4 bipolar | 4 kHz, 24-bit, DC–800 Hz | ~€10k+ (**unverified**) | none | SAGA app + open Python free; **Polybench needs activation** [44][45] |
| g.tec g.USBamp RESEARCH | 16 mono / 8 bipolar | 38.4 kHz, 24-bit | **€14,937.80** | none | g.HIsys is MATLAB/Simulink-bound [50][51][55] |
| g.tec g.HIamp | 16/32/80/144/256 | 38.4 kHz, 24-bit | **€16,192.75** (RESEARCH 16ch); **€19,959.50** (PRO 16ch) | none | as above [52][53] |
| BioSemi ActiveTwo | 32–256 +8 +sensors | 2048/4096/8192/16384 Hz, 24-bit | **€12,000.00** base; **€26,190.20** full set | 2016 forum offer, **no price** [139] | **Low**: ActiView **€2.00**, open BDF [56] |
| Delsys Trigno Avanti | up to 16 sensors | 2148 / 4370 sa/s | not published | none | **High**: base station required; dEMG licence expires after **120 days** [57][58] |
| Noraxon Ultium | up to 32 | 2,000 / 4,000 Hz, 24-bit | not published | **€7,200** (VB) [60] | myoRESEARCH transfer unverified [59] |
| PLUX biosignalsplux | 8 | up to 3,000 Hz/ch, 16-bit | **€3,950.00** | none | **Low**: GitHub APIs [131] |
| Shimmer3 EMG | 2 | not stated in spec sheet (**unverified**) | **€680** | none | unverified [132] |

Legacy TMSi models (Porti, Refa, Mobi, Mobita) all cap at **2048 Hz** and are **discontinued/EOL**
[46][47][48][49]. **g.Nautilus PRO is only 500 Hz** and is disqualified for this spec [54]; so is
**MbientLab MetaMotionR** (100 Hz stream) [141] and BITalino (1000 Hz / **10-bit**) [39].

**The cheapest branded research system observed is the €7,200 Noraxon Ultium** [60], and the
**€415 TeleMyo** is the only genuinely cheap research-grade find — but its channel count and rate are
unverified [130]. If new is acceptable, **PLUX biosignalsplux 8-ch at €3,950** (3 kHz, 16-bit, EU
vendor, GitHub APIs) is the sane research-grade alternative [131].

**Surplus and auction channels that actually carry EEG/EMG.** VEBEG's "Medizin- und Labortechnik"
category had **25 live lots** on 2026-10-01 but the contents were freezers, sterilizers and
anaesthesia monitors — **no EEG/EMG** — and it sells only to German invoice addresses [133].
Surplex listed **430 medical lots** but page 1 was ultrasound, endoscopy and patient monitors, again
**no EEG/EMG** [134]. Troostwijk previously ran a "Schwarzer EEG/PSG Equipment" auction, and that
URL now 404s — evidence that EEG/EMG does surface there occasionally [138]. **LabX has a dedicated
Neurology/EEG/EMG category** but its prices could not be fetched [136]. Consumer classifieds are a
trap: Kleinanzeigen "EMG" is dominated by guitar pickups and electric vehicles [140], Marktplaats by
guitars and Phoenix Contact relays [142], and 2dehands/willhaben returned **zero** "Delsys" hits
[143]. **Artinis runs a vendor trade-in programme**, which is a better lead than the classifieds
[135].

**Pitfalls before paying for any of these.**

1. **Licence/dongle transfer** — Polybench activation [45]; g.HIsys is MATLAB/Simulink-bound [55];
   Delsys dEMG expires after 120 days [58]. Get written confirmation; such licences are usually
   non-transferable.
2. **Missing base station/receiver** — Trigno needs its base station [57]; BioSemi needs the USB2.0
   receiver and fibre [56].
3. **Proprietary electrode cables** — BioSemi's 32-ch active set is **€1,600** and the 32-ch MK3
   cable **€1,280** [56]; Delsys silver contacts are delicate [57]; TMSi uses custom active-shielded
   cables [44].
4. **Rate/channel trade-off** — BioSemi reaches 8192 Hz only at ≤64+8 ch and 16384 Hz only at
   32+8 ch [56].
5. **Cross-border and EOL support** — VEBEG is domestic-only [133]; OpenBCI adds ~25 % EU import tax
   [8]; Porti/Mobi/Mobita/TeleMyo are EOL with uncertain repair paths [46][47][49][130].

**Verdict:** for a 2026-12-31 deadline, treat used research-grade gear as an opportunistic buy, not a
plan. Buy the **PiEEG-16** or **Cerelog ESP-EEG** now, and set an alert for BioSemi ActiveTwo and
PLUX listings so an EU lab liquidation can be picked up if one appears.

### A.6 Where the second-hand market actually is (EU)

The **OpenBCI forum "Opportunities"** category is the only channel where real EU stock was found: a
Sweden Cyton at $800 [15], a Newcastle 8-channel bundle at £1,100 [16], a Scotland Cyton advertised
on eBay [24], and a December 2025 Denmark lab sale whose price list is a JS-only Notion page with no
extractable prices [22][23]. Dutch, German, Italian and Latvian classifieds (Marktplaats,
Kleinanzeigen, Subito, ss.lv) returned **zero** OpenBCI hits. eBay.de/.co.uk/.com, Allegro,
Leboncoin, Ricardo, DOTmed and LabX blocked automated fetching, so live eBay prices are
**unverified** and worth ten minutes in a logged-in browser.

### A.7 Fakes, clones, and used-buying checklist

OpenBCI publishes full PCB design files (schematics, gerbers, BOMs), so clones are expected [25].
The known one is an **AliExpress "Cyton" at $200** that depends on the WiFi Shield/ESP8266 and that
its seller reportedly "never even tested" [21]. Any "new Cyton" far below $1,249 is suspect.

1. **Dongle present and correct.** Cyton: RFduino + FTDI FT231XQ-R [6]; Ganglion needs its own BLE
   dongle (BLED112) — without it the board is useless to a buyer.
2. **Check firmware and every channel.** Send `v` over serial; in the GUI, Radio Config
   STATUS/AUTOSCAN should report "System is Up". Dead-channel reports exist (**unverified**).
3. **Inspect header pins for dried Ten20/gel** contamination.
4. **Battery and polarity.** A reversed JST can destroy the board; confirm it holds charge.
5. **Daisy specifics.** Needs the 2.048 MHz clock from the Cyton; published design has documented
   rework [6]. Micro-SD logging works on Cyton, not Ganglion.
6. **Compare against the published gerbers** where a visual clone is suspected [25].

---

## Part B. Synthetic and transferable data for silent-speech EMG

### B.0 The reference numbers every technique has to beat

**Datasets.** EMG-UKA (Wand, Janke & Schultz) has audibly spoken, whispered and silently articulated
speech with synchronous acoustic reference: **63 sessions, 8 speakers, 7:32 hours**, with a
**1:52-hour** free trial subset [61]. Gaddy & Klein's single-speaker set is **nearly 20 hours**,
"nearly ten times larger than previous publicly available datasets" [62], captured at **8 channels /
1000 Hz** [1].

**The benchmark ladder on Gaddy & Klein's open-vocabulary silent EMG** (test set unless marked
val), from MONA LISA, which re-runs the line on the same split [63]:

| Model | Silent EMG WER | Vocal EMG WER |
|---|---|---|
| Gaddy 2022 (previous SOTA) | 28.8 % | 23.3 % |
| MONA (no LISA) | 22.2 % | 8.9 % |
| **MONA LISA** | **12.2 %** | **3.7 %** |
| Whisper v2, reference on clean audio | — | 2.3 % (Gaddy audio) |

The validation progression shows the levers: baseline **30.4 %** → +CTC on Gaddy audio **27.6 %** →
+LibriSpeech audio-only data **25.5 %** → +cross-contrastive alignment **23.3 %** → crossCon + DTW
**20.6 %** → LLM rescoring of a 10-model ensemble **13.1 %** → fine-tuned LLM **7.3 %** [63]. The
paper treats **15 % WER** as the SSI viability threshold [63]. Three conclusions drive everything
below: **audio-only data from a different corpus measurably helps**, **LLM rescoring is the biggest
lever**, and **the silent/vocalized gap stays large** (12.2 % vs 3.7 %). AlterEgo reports "**92 %
median word accuracy**" on a small closed task — not comparable to the WER table [64]. The same
Berkeley authors' follow-up model improved voicing further and is the direct predecessor MONA LISA
measures against [129].

### B.1 EMG data augmentation — numbers

The only systematic sEMG augmentation benchmark located is **Tsinganos 2020**, on Ninapro-DB1
(27 subjects, 53 gestures, 10 ch) and putEMG (44 subjects, 8 gestures, 24 ch): **magnitude warping
and wavelet decomposition give "up to 16 %" accuracy increase and "+1 %" on the state-of-the-art
CNN**; **additive Gaussian noise "performed the worst"**; earlier electrode-displacement and
muscle-fatigue simulation "**failed to improve the classification accuracy**" [83]. Per-method
percentages beyond those quotes are **unverified** (full-text tables were blocked).

**Channel masking is the best-verified modern augmentation.** SplashNet, on emg2qwerty (108 users,
32 ch, character decoding), masks ~55 % of input features in most mini-batches (vs ~6 % for baseline
SpecAugment): zero-shot CER **51.78 % → 42.62 %**, and with rolling normalization **51.78 % →
36.42 %** (−15.36 points) [85][84]. Plain SpecAugment on emg2qwerty gives "modest but consistent
improvements" [84]; in ASR it moved LibriSpeech test-other from 7.5 % to 6.8 % (no LM) / 5.8 %
(shallow fusion) [86]. Caveat: aggressive masking **without** normalization was *worse than
baseline* in the fine-tuned setting — augmentation can trade zero-shot robustness against per-user
accuracy [85].

**Electrode shift is expensive and only partly fixable.**

| Setting | Result | Source |
|---|---|---|
| 1 cm shift, 10 gestures | average accuracy drops **~25 %**; adding shifted data reduces the drop | Hargrove 2006, cited in [88] |
| 10 mm shift, transient HD-sEMG, >60 gestures | decoder drops to **"as low as 20 %"**; deep augmentation + 3D CNN recovers to **84.6 %** | [89] |
| CapgMyo 128 ch, 8 gestures, 18 subj, intra-session | central 8-ch: **91.7 %**; shifted subsets: **66.7 %** (−25 %) | [88] |
| Training on all valid subsets (proximal–distal, up to 2.4/3.2 cm) | **87.9 %** across subsets, **90.1 %** back on central | [88] |
| Channel-subset augmentation, inter-session | **42.1 %** vs **35.5 %** central-subset (+6.9), vs **25.0 %** all-128-ch (+20.7) | [88] |

Limits in [88]: only proximal–distal shifts helped; **circumferential (clockwise/anticlockwise)
shifts "typically result in larger performance drops" but training on them "did not contribute to
generalization."** Increasing interelectrode distance 2 → 4 cm and using longitudinal+perpendicular
configurations improves shift robustness (p < 0.01, p < 0.05) [90].

**Transfer learning and self-supervision.** Côté-Allard 2019 (pre-train on 19 subjects, Myo armband)
reaches **98.31 %** for 7 gestures / 17 participants and **68.98 %** for 18 gestures / 10
participants (NinaPro DB5); the abstract gives no no-transfer baseline [92]. **FS-HGR** with 5-way
5-shot meta-learning on NinaPro DB2 (40 subjects, 49 gestures) reaches **85.94 %** on new
repetitions, **81.29 %** on new subjects, **73.36 %** on new gestures [93]. **MAST** masked-autoencoder
pretraining at 50 % mask gives **+4 %** (CapgMyo DB-a) and **+6 %** (DB-b); the full framework
reaches **97.3 %** / **56.2 %**, and adding just **10 % of session-2 data** lifts DB-b from 56.2 % to
**78.2 %** [87]. On emg2qwerty, a generic model gets **51.78 %** CER, random-init personalization
**9.55 %**, fine-tuning the generic model **6.95 %** (best user **3.16 %**) [84]. **Du 2017** raises
inter-session recognition from **58.9 %** to **75.4 %** for 27 gestures by estimating electrode shift
with a GMM plus a little calibration data [91]. **CPEP** aligns EMG with pose and claims "up to
**21 %**" in-distribution and "**72 %**" unseen improvements over emg2pose — an abstract-level claim
whose tables could not be read [94].

**Critical caveat: no source quantified "augmentation = +N sessions."** The closest is Kanoga 2021,
where time-domain mixup augmenting source subjects up to 10× "improved the performance of
TL-combined classifiers" on an 8-class, 25-subject set (no delta given) [96]. And offline gains may
not survive real time: a TCN trained with augmentation gave only a small offline improvement and
accuracy *decreased* in real-time evaluation [97, as reported]. No rigorous sEMG SMOTE/cutmix/
DC-offset/baseline-wander accuracy delta was found.

**Best-evidence recipe for one user:** (1) channel-subset/electrode-rotation augmentation
(+6.9 % inter-session, +20.7 % vs all-channel) [88][84]; (2) aggressive channel + spectrogram
masking (51.78 → 36.42 % CER) [85]; (3) magnitude warping + wavelet decomposition (up to +16 %)
[83]; (4) time-domain mixup when source data are small [96]; (5) self-supervised pretraining plus
<10 min real calibration [87][2].

### B.2 Synthetic EMG generation from audio/text

**Audio→EMG is real but low-fidelity, and nobody has closed the loop into a decoder.**
**Botelho et al. 2020** convert speech MFCCs to five EMG time-domain features, then reconstruct
6-channel EMG from EMG-UKA: CCC **0.663** from ground-truth features, falling to **0.54** (speaker 2)
and **0.63** (speaker 8) single-session from audio-predicted features and **0.46** in the
multi-speaker setting; high-frequency ZCR is essentially unpredictable (**CCC 0.182**) [68].
**STE-GAN** (Scheck & Schultz 2023) generates EMG end-to-end from voice-conversion content units:
envelope correlation **0.66**, framewise phoneme accuracy **82.65 %**, resynthesis WER **10.29 %**
same-speaker and **12.28 %** on 200 unseen LibriTTS utterances from 39 speakers (MFCC conditioning
collapses, WER up to 100 %) [69]. Crucially, **STE-GAN's own introduction frames training an
EMG-to-speech model on synthetic EMG as future work** — no paper found reports training a real
decoder on audio-derived synthetic EMG [69]. For scale, the inverse task is older: Toth et al.
voice-converted 5-channel face EMG to speech in 2009 with MCD **6.37** and **19.2 %** ASR WER on 12
test sentences [70].

**Generative sEMG helps closed-set gestures only.** GAN augmentation is small: EBGAN **+1–5 points**
[79], 1DDCGAN **+1.21–5 points** [80]. Diffusion is stronger: **DiffSpkSync** on HD-sEMG (8×8)
reports Hyser session-1 real-only **90.21 %** → mixed **92.52 %**, with **generated-only** training
still reaching **79.37 %** (Hyser) and **88.63–91.44 %** (XDHDEMG) on real test data [73].
**SeqEMG-GAN** (conditioned on hand joint angles) reaches synthetic-only **55.71 %** vs real-only
**57.77 %** and real+synthetic **60.53 %** (+2.76 points) [71]. **EMGFlow**, the first flow-matching
sEMG generator, reaches ~**84–97 %** of the real baseline train-on-synthetic/test-on-real, and on
DB7 augmentation gives **78.26 %** vs TSTR **68.91 %** [72]. **PatchEMG** introduced few-shot
diffusion augmentation for sEMG [82].

**Voiced EMG-to-speech synthesis, however, really does work with synthetic supervision.** **CoM2S**
generates time-aligned EMG from multi-speaker speech with a **GAN conditioned on HuBERT soft speech
units** plus session embeddings, filters by phoneme confidence, then self-trains [65]: a **<0.5**
threshold kept only **~0.5 h** of a **~5.4 h** synthetic pool yet scored **29.36 % WER** on raw test
data versus **42.75 %** and **48.87 %** for weaker/unfiltered data — quality beat quantity. The
optimal threshold yielded **8.3 h across 1,532 speakers**; **1:1 real:synthetic was best**; scaling
gave **3.2 h → 23.85 %**, **6.4 h → 21.88 %**, **16 h → 18.03 %**; train-from-scratch reached
**21.87 %** on the real single-speaker test set (SOTA 23.30 %) and **8.75 %** on multi-speaker
Libri-EMG versus **54.21 %** real-only [65].

**Biophysical simulators do not close the gap.** **MyoGen** is a current NEURON-based neuromuscular
simulator generating surface EMG from motor-unit recruitment and fibre geometry, but has no face or
laryngeal muscle model or speech task found [78]. OpenSim/CEINMS are mature for limbs and solve the
*inverse* (EMG → activation); no published OpenSim/CEINMS pipeline outputs 8–16-channel facial/neck
speech sEMG [78]. Face biomechanics exists — Pitermann & Bailly recover **7 independent lower-face
muscle groups** from OPTOTRAK motion [77] — but outputs activation, not measured surface EMG.
Budget months, not days, for this route.

### B.3 Audio and TTS as training supervision

The foundational result is Gaddy & Klein's **audio target transfer**: silent EMG has no aligned
audio, so they align silent→vocalized EMG with **DTW refined by CCA and predicted audio**, then use
the vocalized audio features as targets [1]. Silent-EMG WER: closed vocabulary human **88.8 %
(direct transfer) → 64.6 % (drop throat electrode) → 3.6 % (full method)**; open vocabulary
**95.1 % → 74.8 %** human and **88.0 % → 68.0 %** automatic. Ablations: without CCA 69.8 %, without
audio alignment 76.5 % [1].

MONA generalises this into **contrastive cross-modal alignment**, which is what lets **LibriSpeech
audio-only data improve silent EMG recognition** — 27.6 % → 25.5 % validation WER, then crossCon to
23.3 % [63]. **Mohapatra et al. (ACL 2025)** map EMG into an **LLM's input space** and learn from
**unvoiced EMG alone**, reaching "an average word error rate (WER) of **0.49** on a
closed-vocabulary unvoiced EMG-to-text task", improving over specialized models by **nearly 20 %**
with only **six minutes** of data [67]. The absolute 49 % WER is poor, but the direction — LLM priors
compensating for near-zero data — is the fast-track regime.

**TTS targets match real targets for the decoder — but only the audio target.** **DiffMV-ETS**
(Interspeech 2025) reports TTS-target CER **45.8** vs same-speaker **46.0** and auxiliary-speaker
**51.7**, i.e. intelligibility and naturalness are retained with synthetic speech [66]. But it still
uses **~10 h of that one user's own silent EMG** [66]. **TTS replaces the audio target, not the EMG
input.** Relatedly, **emg2speech** shows self-supervised speech features linearly predict EMG power
at **r = 0.85**, and its orofacial gesture space clusters at **70.6 %** (power) / **73.7 %** (full
covariance) versus 10 % chance across 12 participants and 13 movements [95].

### B.4 LLM-generated prompt corpora and language-model rescoring

**Prompt corpora: coverage selection beats LLM generation.** TIMIT is phonetically and dialectally
balanced by design (**630 speakers, eight major American-English dialects**) [107]; the Harvard/IEEE
sentences are **720 phonetically balanced read sentences** [108]; greedy text selection for
read-speech corpora was formalised in 1997 [105], and auto-encoder embeddings plus clustering were
used for audiobook script design [106]. **Cowerage** showed coverage-based subset selection beating
random/pruning by **up to 17 % relative WER** on TIMIT, LibriSpeech and LJSpeech with wav2vec 2.0 and
HuBERT [97]. LLM-generated text helps mainly by training an **external LM**: Scottish Gaelic
in-domain generation cut WER **24.48 %** in an unseen broadcast domain [103]; Arabic-English
code-switched generation cut WER **5.5 % relative** [104]. No published method selects a user's
*prompt* sentences by personal LM perplexity — **absent**.

**Rescoring: large, replicated gains.**

| Method | Task | Baseline WER | Rescored WER | Source |
|---|---|---|---|---|
| 4-gram LM, N-best rerank | WSJ / ATIS | 11.87 / 8.82 | 11.21 / 8.57 | [98] |
| InstructGPT + task-activating prompt | WSJ / ATIS | 9.97 / 7.15 | 8.72 / 6.39 | [98] |
| HyPoradise H2T T5 fine-tune | ATIS | 8.3 | **1.7** | [99] |
| HyPoradise LLaMA-13B LoRA | WSJ | 4.5 | **3.8** | [99] |
| N-best T5, constrained decoding | LibriSpeech clean/other | 2.88 / 7.06 | 2.53 / 6.27 | [100] |
| BERT/LoRB rescoring | LibriSpeech (Whisper-tiny first pass) | 6.17 / 13.81 | 4.37 / 10.80 | [101] |
| Gazetteer/prompt personalisation | voice-assistant entities | — | >10 % WERR | [102] |
| LISA (10-model ensemble + LLM) | Gaddy silent EMG, open vocab | 20.6 (val) | **13.1** (val) | [63] |
| LISA, fine-tuned LLM | Gaddy silent EMG, open vocab | 20.6 (val) | **7.3** (val) | [63] |

The negative result matters: in the HyPoradise setup a **frozen 1.5B GPT-2 was catastrophic**
(WSJ 11.87 → **29.56**), OpenLLaMA-13B was worse than baseline and BLOOM-176B roughly neutral; only
*prompted* or *fine-tuned* LLMs beat the baseline [98]. A plain 4-gram LM buys only ~0.5–0.7
absolute [98]. **No EMG silent-speech paper found uses an external LM to rescore decoder output** —
Gaddy & Klein used DeepSpeech to transcribe *generated audio* as an evaluation tool [1][99].
Vocabulary size dominates the decoder: **67-word closed → 3.6 % WER**, **9,828-word open → 68.0 %**
[1]; Meltzner et al. report **10.3 % average WER on a 2,500-word vocabulary** with 8 sensors [128],
and a second Meltzner study reports **8.9 % WER on 1,200+ subvocal phrases** with a 2,200-word
vocabulary and 19 subjects [76].
A 2026 ceiling statement: Myovox reaches 18.53 % WER on emg2speech with a Conformer + QLoRA-tuned 7B
reranker, but shows the reranker is **exhausted** because acoustic phone error (~20.9 %) is the
binding constraint and the **9.30 % N-best oracle is unreachable** — better language models cannot
manufacture articulatory information the EMG does not carry [81].

**One-user recipe:** ~2–5k prompt sentences by greedy coverage selection over your own texts, topped
up with an LLM for rare phonemes/words [97][103]; start with a closed 20–100-word command set
[1][128]; produce an N-best list (beam 10–60) and rescore with a small fine-tuned BERT/T5 or
LoRA-adapted LLM [99][100][101]; add a personal gazetteer [102]. Expect **10–40 % relative** WER
reduction when correct words are in the N-best — and measure the **oracle N-best WER first**, because
it bounds everything.

### B.5 Cross-language: Latvian / Russian silent speech from English-only pretraining

**The gap:** essentially all silent-speech EMG work is English and single-speaker, and no
cross-language **sEMG** silent-speech transfer study was found. The nearest evidence is
articulatory: Mandarin sEMG-to-voice with **6 speakers and 5.79 h of silent data** and pretrained
Mandarin MFA toneme supervision reached **6.41 % average CER** by human evaluation [121]; a combined
EEG+EMG decoder reached **95.3 %** word classification on healthy participants and **54.5 %** on a
speech-impaired patient versus **70.1 % / 13.2 %** single-subject, with "gains in cross-language
calibration performance" but no per-language WER [122]; ultrasound tongue imaging adapted
English→Cantonese gave up to **4.75 % / 2.59 % absolute** WER/CER reductions with MLAN domain
adaptation [123]; and Azerbaijani L1/L2 English showed lower CNN MSE on L1 while mel-cepstral
distortion did not reflect it — evidence of **vocoder language bias** [124]. Adversarial
cross-subject work on **100 closed Chinese sentences** reaches **89.46 %** accuracy on 40 unseen
subjects, but that is closed-set classification, not text [75].

**Phoneme inventories bridge languages only partially.** AlloVera maps **218 allophones to 148
phoneme symbols across 14 languages, including Russian (45 phonemes / 62 phones)** but **not
Latvian**; shared-phoneme models performed far worse (average PER **73.8 %** vs private
**25.6 %**), while the allophone model (Allosaurus) reached **25.0 %** full and **41.8 %** at 10k
utterances; Russian PER was **26.3 %** full [116]. Latvian would need a hand-built IPA mapping — not
published.

**Data and models are adequate.** XLS-R pretrained on **436k hours across 128 languages**, including
**Latvian 13,126 h** and **Russian 166 h** (the Russian figure looks anomalous and is reported as
given) [117]; MMS covers **1,406 languages** with ASR for 1,107 and 44.7k hours of MMS-lab data
[118]; VoxLingua107 has **6,628 h / 107 languages**, with Latvian **42 h** and Russian **73 h**
[119]. FLEURS provides roughly **12 h per language across 102 languages**, with multilingual corpus
quality issues documented [125]. Common Voice Russian v8.0: **162.44 h, 111,904 utterances, 1,970 speakers** (216 F / 653 M /
1,101 unknown) [115]. Latvian Common Voice 19.0's VW train split is **212.6 h**; adding **69.8 h** of
LATE-Media gives **282.4 h**, on which a Whisper-large-v3 fine-tune scores **WER 4.8 / CER 1.6
formatted** and **3.2 / 1.0 normalized** on the CV19 test set (LATE-Media: 19.2 / 7.6 and 12.8 /
5.3) [114]. BalsuTalka grew the Latvian corpus more than tenfold in under a year [120].

**Per-user adaptation is cheap.** On three low-resource African languages, DoRA PEFT matched full
fine-tuning at **22.0 % vs 22.1 %** macro-average WER while updating **4M instead of 240M
parameters** [126]. Rescoring LMs exist for both languages: **LV-BERT** (BERT-base, 32k vocab, ~500M
tokens, Apache-2.0) [109]; Latvian encoder benchmarking [110]; **mGPT 1.3B covering 61 languages
including both Latvian and Russian** (Apache-2.0) [111]; a family of **13 Russian Transformer LMs**
[112]. **Vikhr is retracted — do not use its numbers** [113]. LLM rescoring for English ASR gives
**5–25 % relative** WER improvement [127].

**Verdict:** English-only EMG pretraining plus Latvian/Russian adaptation is realistic as an
**articulatory → shared-IPA phoneme → text** pipeline, not direct acoustic transfer. Missing: a
cross-language sEMG experiment, a Latvian phone inventory, per-user silent-EMG calibration, and
LV/RU rescoring numbers. Budget those as your own experiments.

### B.6 What synthetic data cannot replace

1. **The user's own silent EMG.** No published system trains a silent-speech decoder on EMG
   synthesised from audio or text [68][69]. Audio→EMG tops out at **CCC 0.66 / envelope correlation
   0.66** and does not capture subject- and electrode-specific fine structure [68][69].
   Voiced→silent model transfer fails at **88 %+ WER** [1].
2. **Cross-subject generalisation.** Le et al. (27 subjects, ~21 min each, 50-sentence closed
   corpus): **21.7 % CER / 31.9 % WER with target calibration**, **49.3 % CER with none**, and
   **78.6 % CER / 99.9 % WER when the five evaluation sentences are excluded from all sEMG training
   data** — the closed-corpus headline is largely sentence identification, not decoding [74]. The
   demonstrated minimum is small: **~3 minutes** of target-subject silent EMG reached **20.5 % CER**
   versus 21.7 % for the full ~13-min pool [74].
3. **Electrode repositioning.** SilentWear loses ~15–25 accuracy points between sessions
   (77.5 → 59.3 % silent) [2]; Meier et al. lose ~14 points (68 ± 3 % → 54 ± 7 %) [3]. Only real
   per-session data fixes it, though **<10 minutes** recovers >10 % [2].
4. **Your montage.** CoM2S notes that open EMG corpora use 40, 8 and 6 electrodes and are "not
   compatible with one another" [65]; synthetic generators are conditioned on a specific
   configuration and session embedding.
5. **Rare personal vocabulary.** 67 words → 3.6 %, 9,828 words → 68.0 % WER [1]. Rescoring helps
   most when the right token is already in the N-best [98][99]; names and domain terms still need a
   gazetteer [102] or real examples.
6. **Honest labels for silent speech.** Silent EMG has no audible ground truth; alignment quality
   (DTW/CCA) is a ceiling on everything downstream [1].

---

---

## Sources

[1] D. Gaddy, D. Klein, "Digital Voicing of Silent Speech," EMNLP 2020 — https://ar5iv.labs.arxiv.org/html/2010.02960 (2020)

[2] G. Spacone, S. Frey, G. Pollo, A. Burrello, D. Jahier Pagliari, V. Kartsch, A. Cossettini, L. Benini, "SilentWear: an Ultra-Low Power Wearable System for EMG-based Silent Speech Recognition," arXiv:2603.02847 — https://arxiv.org/abs/2603.02847 (2026)

[3] F. Meier, G. Spacone, S. Frey, L. Benini, A. Cossettini, "A Parallel Ultra-Low Power Silent Speech Interface based on a Wearable, Fully-dry EMG Neckband," arXiv:2509.21964 — https://arxiv.org/abs/2509.21964 (2025)

[4] OpenBCI Documentation, "Cyton Data Format" — https://docs.openbci.com/Cyton/CytonDataFormat/ (last updated 2025-07-16)

[5] OpenBCI Forum, "Sampling rate modification on Cyton board" (discussion 3615) — https://openbci.com/forum/index.php?p=/discussion/3615/sampling-rate-modification-on-cyton-board (2023)

[6] OpenBCI Documentation, "Cyton Specs" — https://docs.openbci.com/Cyton/CytonSpecs/ (last updated 2026-06-12)

[7] OpenBCI Forum, "Options for Cyton/Daisy Sampling Rate" (discussion 3304) — https://openbci.com/forum/index.php?p=/discussion/3304/options-for-cyton-daisy-sampling-rate (2022)

[8] OpenBCI Shop, "Cyton Biosensing Board (8-channels)" — https://shop.openbci.com/products/cyton-biosensing-board-8-channel.json (price data 2026-10-01)

[9] OpenBCI Shop, "Cyton + Daisy Biosensing Boards (16-Channels)" — https://shop.openbci.com/products/cyton-daisy-biosensing-boards-16-channel.json (price data 2026-10-01)

[10] OpenBCI Shop, "Daisy Module (Upgrade Kit)" — https://shop.openbci.com/products/daisy-module.json (price data 2026-10-01)

[11] OpenBCI Shop, "Ganglion Board (4-channels)" — https://shop.openbci.com/products/ganglion-board.json (price data 2026-10-01)

[12] OpenBCI Shop, "Ganglion Dongle (Mac, Windows & Linux)" — https://shop.openbci.com/products/ganglion-dongle.json (price data 2026-10-01)

[13] OpenBCI Shop, "Galea" — https://shop.openbci.com/products/galea.json (price data 2026-10-01)

[14] OpenBCI Shop, "Galea Neon Eye Tracking Add-On" — https://shop.openbci.com/products/galea-beta-standalone-eye-tracking-add-on.json (price data 2026-10-01)

[15] OpenBCI Forum, "For Sale: Cyton 8 channel with dongle and a some beginner accessories" (discussion 4138) — https://openbci.com/forum/index.php?p=/discussion/4138/for-sale-cyton-8-channel-with-dongle-and-a-some-beginner-accessories (2026)

[16] OpenBCI Forum, "Selling neurotechnologist bundle (England, can ship abroad)" (discussion 4046) — https://openbci.com/forum/index.php?p=/discussion/4046/selling-neurotechnologist-bundle-england-can-ship-abroad (2025)

[17] OpenBCI Forum, "[SALE] Complete 16-Channel Cyton + Daisy EEG Cap Bundle - San Diego / Ship - $1,800" (discussion 4117) — https://openbci.com/forum/index.php?p=/discussion/4117/sale-complete-16-channel-cyton-daisy-eeg-cap-bundle-san-diego-ship-1-800 (2026)

[18] OpenBCI Forum, "3D-Print-it-Yourself 16-channel Neurotechnologist Bundle FOR SALE" (discussion 4170) — https://openbci.com/forum/index.php?p=/discussion/4170/3d-print-it-yourself-16-channel-neurotechnologist-bundle-for-sale (2026)

[19] NeuroBB, "Selling 2nd hand but barely used All-in-One Biosensing R&D Bundle from OpenBCI" — https://neurobb.com/t/selling-2nd-hand-but-barely-used-all-in-one-biosensing-r-d-bundle-from-openbci/2200 (2024)

[20] OpenBCI Forum, "unused / new Ganglion EEG units for sale, with case, batteries and touchproof electrode adapters" (discussion 3588) — https://openbci.com/forum/index.php?p=/discussion/3588/unused-new-ganglion-eeg-units-for-sale-with-case-batteries-and-touchproof-electrode-adapters (2023)

[21] OpenBCI Forum, "AliExpress Cyton Knockoff for sale $200 OBO" (discussion 3815) — https://openbci.com/forum/index.php?p=/discussion/3815/aliexpress-cyton-knockoff-for-sale-200-obo (2024)

[22] OpenBCI Forum, "Selling used OpenBCI headsets" (discussion 4081) — https://openbci.com/forum/index.php?p=/discussion/4081/selling-used-openbci-headsets (2025)

[23] Affecture (Notion), "Equipment for Sale" — https://affecture.notion.site/Equipment-for-Sale-1ac80ca1a5178095b52fd072b626b4b4 (2025; JS-only page, no prices extractable)

[24] OpenBCI Forum, "Selling a used OpenBCI Cyton Board + Electrodes" (discussion 4093) — https://openbci.com/forum/index.php?p=/discussion/4093/selling-a-used-openbci-cyton-board-electrodes (2026)

[25] OpenBCI, "V3 Hardware Design Files" — https://github.com/OpenBCI/V3_Hardware_Design_Files (accessed 2026)

[26] Texas Instruments, "ADS1299 Low-Noise, 8-Channel, 24-Bit ADC for Biopotential Measurements" — https://www.ti.com/product/ADS1299 (datasheet Rev. C, 2017)

[27] Texas Instruments, "ADS1299EEGFE-PDK Evaluation board" — https://www.ti.com/tool/ADS1299EEGFE-PDK (2024)

[28] Texas Instruments, "ADS1299EEG-FE EEG Front-End Performance Demonstration Kit (Rev. B), SLAU443B" — https://www.ti.com/lit/pdf/SLAU443 (2016)

[29] LionCircuits, "ADS1299EEGFE-PDK" — https://www.lioncircuits.com/parts/ADS1299EEGFE-PDK (2026)

[30] Crowd Supply, "HackEEG" — https://www.crowdsupply.com/starcat/hackeeg (2020)

[31] Mouser EU, "Starcat CS-HACKEEG-02" — https://eu.mouser.com/ProductDetail/Starcat/CS-HACKEEG-02 (2026; listing only)

[32] PiEEG, "Products / Hardware" — https://www.pieeg.com/hardware (2026)

[33] Cerelog ESP-EEG, README — https://raw.githubusercontent.com/Cerelog-ESP-EEG/ESP-EEG/main/README.md (2026)

[34] Cerelog, "ESP-EEG for Researchers" — https://www.cerelog.com/eeg_researchers.html (2026)

[35] Cerelog — https://www.cerelog.com/ (2026)

[36] MindRove, "Armband 2 – Wearable EMG Sensor with 8 Channels" — https://mindrove.com/product/emg-armband-2/ (2026)

[37] Crowd Supply, "BioAmp EXG Pill" — https://www.crowdsupply.com/upside-down-labs/bioamp-exg-pill (2022)

[38] Upside Down Labs, "Muscle BioAmp Shield" — https://docs.upsidedownlabs.tech/hardware/bioamp/muscle-bioamp-shield/ (2026)

[39] PLUX, "BITalino (r)evolution User Manual v1.0" — https://support.pluxbiosignals.com/wp-content/uploads/2021/11/bitalino-revolution-user-manual.pdf (2020)

[40] PLUX, "BITalino Board" — https://www.pluxbiosignals.com/products/bitalino-board (2026)

[41] PLUX, "muscleBIT (BT)" — https://www.pluxbiosignals.com/products/musclebit (2026)

[42] Texas Instruments, "ADS1298 8-Channel 24-bit ADC With Integrated ECG Front End" — https://www.ti.com/product/ADS1298 (datasheet Rev. K, 2015)

[43] OpenBCI Documentation, "Ganglion Specs" — https://docs.openbci.com/Ganglion/GanglionSpecs/ (last updated 2025-07-15)

[44] TMSi (Artinis), "SAGA" — https://www.tmsi.artinis.com/saga (2026)

[45] TMSi Knowledge Base, "How can I activate my Polybench License?" — https://knowledge.tmsi.com/how-can-i-activate-my-polybench-license (n.d.)

[46] TMSi, "Mobi" (archived) — https://web.archive.org/web/2019id_/https://www.tmsi.com/products/mobi/ (2019)

[47] TMSi, "Porti" (archived) — https://web.archive.org/web/2020/https://www.tmsi.com/products/porti/ (2020)

[48] TMSi, "Refa" (archived) — https://web.archive.org/web/2020/https://www.tmsi.com/products/refa/ (2020)

[49] TMSi, "Mobita" (archived) — https://web.archive.org/web/2019id_/https://www.tmsi.com/products/mobita/ (2019)

[50] g.tec, "g.USBamp RESEARCH" — https://www.gtec.at/product/gusbamp-research-16-channel-biosignal-amplifier/ (2026)

[51] g.tec, "g.USBamp product configurator" — https://www.gtec.at/product-configurator/g-usbamp/ (2026)

[52] g.tec, "g.HIamp" — https://www.gtec.at/product/g-hiamp/ (2026)

[53] g.tec, "g.HIamp product configurator" — https://www.gtec.at/product-configurator/g-hiamp/ (2026)

[54] g.tec, "g.Nautilus PRO Flexible" — https://www.gtec.at/product/g-nautilus-pro/ (2026)

[55] g.tec, "g.HIsys Professional" — https://www.gtec.at/product/ghisys-biosignal-acquisition-analysis/ (2026)

[56] BioSemi, "Price List 2024" — https://biosemi.com/download/BioSemi%20Pricelist%202024.pdf (2024)

[57] Delsys, "Trigno Avanti Spring Contact Adapter User's Guide (MAN-042-1-2)" — https://delsys.com/downloads/USERSGUIDE/MAN-042-1-2%20Trigno%20Avanti%20Spring%20Contact%20Adapter.pdf (2023)

[58] Delsys, "dEMG Acquisition User's Guide (MAN-011-1-9)" — http://data.delsys.com/DelsysServicePortal/dEMG%20Files/dEMG%20Acquisition%20(MAN-011-1-9).pdf (n.d.)

[59] Noraxon, "Ultium EMG" — https://www.noraxon.com/our-products/ultium-emg/ (2026)

[60] Kleinanzeigen, "Noraxon Ultium EMG — Physiotherapie, Analyse" (€7,200 asking) — https://www.kleinanzeigen.de/s-anzeige/noraxon-ultium-emg-physiotherapie-analayse/3350414398-230-17916 (2026)

[61] M. Wand, M. Janke, T. Schultz, "The EMG-UKA Corpus for Electromyographic Speech Processing," Interspeech 2014 — https://www.isca-archive.org/interspeech_2014/wand14b_interspeech.html (2014)

[62] D. Gaddy, "Voicing Silent Speech," UC Berkeley Technical Report UCB/EECS-2022-68 — https://www2.eecs.berkeley.edu/Pubs/TechRpts/2022/EECS-2022-68.html (2022)

[63] T. Benster, G. Wilson, R. Elisha, F. R. Willett, S. Druckmann, "A Cross-Modal Approach to Silent Speech with LLM-Enhanced Recognition" (MONA LISA) — https://ar5iv.labs.arxiv.org/html/2403.05583 (2024)

[64] A. Kapur, S. Kapur, P. Maes, "AlterEgo: A Personalized Wearable Silent Speech Interface," IUI 2018 — https://www.media.mit.edu/publications/alterego-IUI/ (2018)

[65] X. Chen, X. Gao, M. Quoy, A. Pitti, N. F. Chen, "Confidence-Based Self-Training for EMG-to-Speech: Leveraging Synthetic EMG for Robust Modeling" (CoM2S), arXiv:2506.11862 — https://arxiv.org/html/2506.11862v2 (2026)

[66] K. Scheck, T. Dombeck, Z. Ren, P. Wu, M. Wand, T. Schultz, "DiffMV-ETS: Diffusion-based Multi-Voice Electromyography-to-Speech Conversion using Speaker-Independent Speech Training Targets," Interspeech 2025 — https://www.isca-archive.org/interspeech_2025/scheck25_interspeech.html (2025)

[67] P. Mohapatra, A. Pandey, X. Zhang, Q. Zhu, "Can LLMs Understand Unvoiced Speech? Exploring EMG-to-Text Conversion with LLMs," ACL 2025, arXiv:2506.00304 — https://arxiv.org/abs/2506.00304 (2025)

[68] Botelho et al., "Toward Silent Paralinguistics: Speech-to-EMG — Retrieving Articulatory Muscle Activity from Speech," Interspeech 2020 — https://www.isca-archive.org/interspeech_2020/botelho20_interspeech.html (2020)

[69] K. Scheck, M. Wand, T. Schultz, "STE-GAN: Speech-to-Electromyography Signal Conversion using Generative Adversarial Networks," Interspeech 2023 — https://www.isca-archive.org/interspeech_2023/scheck23_interspeech.html (2023)

[70] Toth et al., "Synthesizing speech from electromyography using voice transformation techniques," Interspeech 2009 — https://www.isca-archive.org/interspeech_2009/toth09_interspeech.html (2009)

[71] Wang et al., "New Synthetic Goldmine: Hand Joint Angle-Driven EMG Data Generation" (SeqEMG-GAN), arXiv:2509.23359 — https://arxiv.org/abs/2509.23359 (2025/AAAI 2026)

[72] Jiang et al., "EMGFlow: Robust and Efficient Surface Electromyography Synthesis via Flow Matching," arXiv:2604.13685 — https://arxiv.org/abs/2604.13685 (2026)

[73] Su et al., "DiffSpkSync: A Muscle Synergy-Guided Spiking Diffusion Model for EMG Signal Generation" — https://eprints.whiterose.ac.uk/id/eprint/240724/ (2026)

[74] Le et al., "Multi-Subject Pretraining Enables Short-Calibration Personalization for Closed-Corpus Surface EMG Speech Decoding," arXiv:2609.21288 — https://arxiv.org/abs/2609.21288 (2026)

[75] Cui et al., "A simplified adversarial architecture for cross-subject silent speech recognition using electromyography" — https://doi.org/10.1088/1741-2552/ad7321 (2024)

[76] Meltzner et al., "Development of sEMG sensors and algorithms for silent speech recognition" — https://pubmed.ncbi.nlm.nih.gov/29855428/ (2018)

[77] Pitermann, Bailly, "A face-to-muscle inversion of a biomechanical face model," Eurospeech 2001 — https://www.isca-archive.org/eurospeech_2001/pitermann01_eurospeech.html (2001)

[78] NsquaredLab, "MyoGen: Unified Biophysical Modeling of Human Neuromotor Activity and Resulting Signals" — https://nsquaredlab.github.io/MyoGen/ (2026)

[79] Zhang, Ma, "Research on sEMG Feature Generation and Classification Performance Based on EBGAN" — https://doi.org/10.3390/electronics12041040 (2023)

[80] Gouda et al., "Synthesis of sEMG Signals for Hand Gestures Using a 1DDCGAN" — https://doi.org/10.3390/bioengineering10121353 (2023)

[81] Myovox: Reading Speech from the Muscles of the Face, arXiv:2609.17548 — https://arxiv.org/abs/2609.17548 (2026, preprint)

[82] PatchEMG: Few-Shot EMG Signal Generation With Diffusion Models — https://ieeexplore.ieee.org/abstract/document/10648713 (2024)

[83] A. Tsinganos et al., "Data Augmentation of Surface Electromyography for Hand Gesture Recognition" — https://pmc.ncbi.nlm.nih.gov/articles/PMC7506981/ (2020)

[84] emg2qwerty: A Large Dataset with Baselines for Touch Typing using Surface Electromyography, arXiv:2410.20081 — https://arxiv.org/abs/2410.20081 (2024)

[85] SplashNet: Split-and-Share Encoders for Accurate and Efficient Typing with Surface Electromyography, arXiv:2506.12356 — https://arxiv.org/abs/2506.12356 (2025)

[86] SpecAugment: A Simple Data Augmentation Method for Automatic Speech Recognition, arXiv:1904.08779 — https://arxiv.org/abs/1904.08779 (2019)

[87] MAST: Masked Autoencoder with Swin Transformer Network for Mitigating Electrode Shift in HD-EMG-based Gesture Recognition, arXiv:2410.17261 — https://arxiv.org/abs/2410.17261 (2024)

[88] Pereira et al., "Tackling Electrode Shift in Gesture Recognition with HD-EMG Electrode Subsets," arXiv:2401.02773 — https://arxiv.org/abs/2401.02773 (2024)

[89] Sun et al., "Deep Augmentation for Electrode Shift Compensation in Transient High-density sEMG" — https://www.biorxiv.org/content/10.1101/2022.02.25.481922v2 (2022)

[90] Young et al., "Improving Myoelectric Pattern Recognition Robustness to Electrode Shift by Changing Interelectrode Distance and Electrode Configuration" — https://pmc.ncbi.nlm.nih.gov/articles/PMC4234037/ (2012)

[91] Du et al., "Surface EMG-Based Inter-Session Gesture Recognition Enhanced by Deep Domain Adaptation" — https://pmc.ncbi.nlm.nih.gov/articles/PMC5375744/ (2017)

[92] Côté-Allard et al., "Deep Learning for Electromyographic Hand Gesture Signal Classification Using Transfer Learning" — https://pubmed.ncbi.nlm.nih.gov/30714928/ (2019)

[93] FS-HGR: Few-shot Learning for Hand Gesture Recognition via ElectroMyography, arXiv:2011.06104 — https://arxiv.org/abs/2011.06104 (2021)

[94] CPEP: Contrastive Pose-EMG Pre-training Enhances Gesture Generalization on EMG Signals, arXiv:2509.04699 — https://arxiv.org/abs/2509.04699 (2025)

[95] emg2speech: Synthesizing speech from electromyography using self-supervised speech models, arXiv:2510.23969 — https://arxiv.org/abs/2510.23969 (2025)

[96] Kanoga et al., "Time-domain Mixup Source Data Augmentation of sEMGs for Motion Recognition" — https://pubmed.ncbi.nlm.nih.gov/34891233/ (2021)

[97] Azeemi, Qazi, Raza, "Representative Subset Selection for Efficient Fine-Tuning in Self-Supervised Speech Recognition" (Cowerage), arXiv:2203.09829 — https://arxiv.org/abs/2203.09829 (2022)

[98] C.-H. H. Yang et al., "Generative Speech Recognition Error Correction with Large Language Models and Task-Activating Prompting," ASRU, arXiv:2309.15649 — https://arxiv.org/abs/2309.15649 (2023)

[99] C. Chen et al., "HyPoradise: An Open Baseline for Generative Speech Recognition with Large Language Models," NeurIPS 2023, arXiv:2309.15701 — https://arxiv.org/abs/2309.15701 (2023)

[100] R. Ma et al., "N-best T5: Robust ASR Error Correction using Multiple Input Hypotheses and Constrained Decoding Space," arXiv:2303.00456 — https://arxiv.org/abs/2303.00456 (2023)

[101] Y. Yu et al., "Low-rank Adaptation of Large Language Model Rescoring for Parameter-Efficient Speech Recognition" (LoRB), arXiv:2309.15223 — https://arxiv.org/abs/2309.15223 (2023)

[102] T. Kolehmainen et al., "Personalization for BERT-based Discriminative Speech Recognition Rescoring," arXiv:2307.06832 — https://arxiv.org/abs/2307.06832 (2023)

[103] C. Lamb et al., "Text-only Domain Adaptation for Low-Resource ASR Using Large Language Models" — https://aclanthology.org/2026.llms4ssh-1.10/ (2026)

[104] A. Alharbi et al., "Leveraging LLM for Augmenting Textual Data in Code-Switching ASR: Arabic as an Example" — https://www.isca-archive.org/syndata4genai_2024/alharbi24_syndata4genai.html (2024)

[105] J. van Santen, A. Buchsbaum, "Methods for optimal text selection," Eurospeech 1997 — https://www.isca-archive.org/eurospeech_1997/santen97b_eurospeech.html (1997)

[106] T. Shamsi et al., "Corpus Design Using Convolutional Auto-Encoder Embeddings for Audio-Book Synthesis," Interspeech 2019 — https://www.isca-archive.org/interspeech_2019/shamsi19_interspeech.html (2019)

[107] TIMIT Acoustic-Phonetic Continuous Speech Corpus (LDC93S1) — https://catalog.ldc.upenn.edu/LDC93S1 (1993)

[108] Harvard Sentences, IEEE Recommended Practice for Speech Quality Measurements — https://www.cs.columbia.edu/~hgs/audio/harvard.html (1969)

[109] AiLab-IMCS-UL, "lvbert" model card — https://huggingface.co/AiLab-IMCS-UL/lvbert (2020)

[110] A. Znotins, "Pretraining and Benchmarking Modern Encoders for Latvian," arXiv:2603.15005 — https://arxiv.org/abs/2603.15005 (2026)

[111] O. Shliazhko et al., "mGPT: Few-Shot Learners Go Multilingual" — https://huggingface.co/ai-forever/mGPT (2022)

[112] "A Family of Pretrained Transformer Language Models for Russian," LREC-COLING 2024 — https://aclanthology.org/2024.lrec-main.45/ (2024)

[113] A. Nikolich et al., "Vikhr: Bilingual Open-Source Instruction-Following LLM for Russian" [RETRACTED] — https://aclanthology.org/2024.mrl-1.15/ (2024)

[114] AiLab-IMCS-UL, "whisper-large-v3-lv-late-cv19" model card — https://huggingface.co/AiLab-IMCS-UL/whisper-large-v3-lv-late-cv19 (2025)

[115] Montreal Forced Aligner, "Common Voice Russian v8.0" corpus README — https://raw.githubusercontent.com/MontrealCorpusTools/mfa-models/refs/heads/main/corpus/russian/common_voice_russian/8.0/README.md (2023)

[116] M. Mortensen et al., "AlloVera: A Multilingual Allophone Database," arXiv:2004.08031 — https://ar5iv.labs.arxiv.org/html/2004.08031 (2020)

[117] A. Babu et al., "XLS-R: Self-supervised Cross-lingual Speech Representation Learning at Scale," arXiv:2111.09296 — https://ar5iv.labs.arxiv.org/html/2111.09296 (2022)

[118] V. Pratap et al., "Scaling Speech Technology to 1,000+ Languages" (MMS), arXiv:2305.13516 — https://ar5iv.labs.arxiv.org/html/2305.13516 (2023)

[119] J. Valk, T. Alumäe, "VoxLingua107: a Dataset for Spoken Language Recognition," arXiv:2011.12998 — https://ar5iv.labs.arxiv.org/html/2011.12998 (2021)

[120] R. Dargis et al., "BalsuTalka.lv — Boosting the Common Voice Corpus for Low-Resource Languages," LREC-COLING 2024 — https://aclanthology.org/2024.lrec-main.187/ (2024)

[121] "Sequence-to-Sequence Voice Reconstruction for Silent Speech in a Tonal Language," arXiv:2108.00190 — https://ar5iv.labs.arxiv.org/html/2108.00190 (2021)

[122] K. Inoue et al., "A Silent Speech Decoding System from EEG and EMG with Heterogeneous Electrode Configurations," Interspeech 2025 — https://www.isca-archive.org/interspeech_2025/inoue25b_interspeech.html (2025)

[123] "Exploiting Cross-Domain and Cross-Lingual Ultrasound Tongue Imaging Features," arXiv:2206.07327 — https://ar5iv.labs.arxiv.org/html/2206.07327 (2022)

[124] S. Ibrahimov et al., "Exploring Language Dependency in Ultrasound-to-Speech Synthesis," SSW 2025 — https://www.isca-archive.org/ssw_2025/ibrahimov25_ssw.html (2025)

[125] "Data Quality Issues in Multilingual Speech Datasets," arXiv:2506.17525 — https://arxiv.org/html/2506.17525v2 (2025)

[126] "Full Fine-Tuning vs PEFT for Low-Resource African ASR," AfricaNLP 2026 — https://aclanthology.org/2026.africanlp-main.19/ (2026)

[127] "ProGRes: Prompted Generative Rescoring on ASR n-Best," arXiv:2409.00217 — https://arxiv.org/abs/2409.00217 (2024)

[128] G. S. Meltzner et al., "Silent Speech Recognition as an Alternative Communication Device for Persons with Laryngectomy," IEEE/ACM TASLP — https://doi.org/10.1109/TASLP.2017.2740000 (2017)

[129] D. Gaddy, D. Klein, "An Improved Model for Voicing Silent Speech," ACL 2021 — https://aclanthology.org/2021.acl-short.23/ (2021)

[130] Sprzedajemy.pl, "Urządzenie Medyczne TELEMYO DTS 7-K MR" (1,782 zł asking) — https://sprzedajemy.pl/urzadzenie-medyczne-telemyo-dts-7-k-mr-magnice-4-4a1708-nr72786138 (n.d.)

[131] PLUX Biosignals, "8-Channel biosignalsplux Kit" (€3,950.00) — https://www.pluxbiosignals.com/products/8-channel-biosignals-kit (2026)

[132] Shimmer Sensing, "Shimmer3 EMG Unit" (€680) — https://shimmersensing.com/product/shimmer3-emg-unit/ (2026)

[133] VEBEG, "Medizin- und Labortechnik" — https://www.vebeg.de/de/verkauf/suchen.htm?DO_SUCHE=1&SUCH_MATGRUPPE=1210 (2026)

[134] Surplex, "Medizinische Ausrüstung" — https://www.surplex.com/c/medizinisch/medizinische-ausrustung/fe4e0c20-9ea9-4852-ab50-84536a251b42 (2026)

[135] Artinis, "Trade-in program" — https://www.artinis.com/trade-in (2026)

[136] LabX, "Neurology / EEG / EMG" category — https://www.labx.com/categories-a/neurology-eeg-emg (2026; fetch blocked)

[137] eBay.de, "Delsys Trigno" search (HTTP 403 to automated fetch) — https://www.ebay.de/sch/i.html?_nkw=delsys+trigno (2026)

[138] Troostwijk Auctions, "Schwarzer EEG/PSG Equipment" (now 404) — https://www.troostwijkauctions.com/en/l/schwarzer-eeg-psg-equipment-A1-26482-195 (n.d.)

[139] BioSemi Forum, "Used BioSemi system for sale" (no price given) — http://www.biosemi.nl/forum/viewtopic.php?p=2916 (2016)

[140] Kleinanzeigen, search "EMG" — https://www.kleinanzeigen.de/s-suchanfrage.html?keywords=EMG (2026)

[141] MbientLab, "MetaMotionR" (100 Hz stream) — https://mbientlab.com/store/metamotionr/ (2026)

[142] Marktplaats, search "EMG" — https://www.marktplaats.nl/q/emg/ (2026)

[143] 2dehands.be search "delsys" and willhaben search "Delsys" (0 hits) — https://www.2dehands.be/q/delsys/ and https://www.willhaben.at/iad/kaufen-und-verkaufen/marktplatz?keyword=delsys (2026)

---

## Key takeaways for the build

1. **Do not buy a stock OpenBCI Cyton + Daisy for 8–16 ch @ 1 kHz.** It is 250 SPS (8 ch) or an
   averaged ~125 SPS/channel (16 ch); 1 kHz needed the discontinued WiFi Shield [4][5][7].
2. **Used OpenBCI is priced close to new** ($1,800–$2,150 vs $2,499) [15][17][18][19]. Buy
   **PiEEG-16 ($390)** as the stopgap and **Cerelog ESP-EEG ($389.99)** if you want an EU vendor
   [32][33]; copy **HackEEG** for the custom board [30].
3. **Buy electrodes and Ten20 paste first** — the reference dataset used gold electrodes plus paste,
   and dry electrodes cost inter-session accuracy [1][2].
4. **Treat <10 min per-session recalibration as a fixed product requirement** — it recovers >10 %
   accuracy after repositioning [2].
5. **Augment with channel-subset/electrode rotation and aggressive channel masking**, not with
   additive Gaussian noise or electrode-shift/fatigue simulation, which failed [88][85][83].
6. **Synthetic multi-speaker EMG is real for voiced EMG** (54.21 % → 8.75 % WER; 1:1 mix best)
   [65], but **do not plan to skip your own silent recordings** — no synthetic route replaces them
   [68][69][74].
7. **Use audio-only data (LibriSpeech) via cross-modal alignment** — it measurably improves silent
   EMG decoding (30.4 → 25.5 % validation WER) [63].
8. **Rescoring is the highest-return software work.** MONA LISA: 20.6 → 13.1 → 7.3 % validation WER;
   HyPoradise: ATIS 8.3 → 1.7 [63][99]. Measure the N-best oracle before promising anything [81].
9. **Start with a closed 20–100-word command vocabulary** — the only regime with wearable-grade
   numbers; open-vocabulary EMG sits near 68 % WER [1][2][128].
10. **For Latvian/Russian, plan articulatory → shared IPA → text**, with ~10 h of per-user
    adaptation and mGPT/LV-BERT rescoring [116][114][111][126]. The cross-language sEMG experiment is
    yours to run — nothing is published.

## Open questions

1. Which research-grade system (TMSi/g.tec/Biosemi/Delsys) can an individual realistically buy used
   in the EU, at what price, and without a licence/dongle trap? Only two live used asks were found
   at all, so this needs a human broker conversation.
2. Does DiffMV-ETS's TTS-target parity hold for *silent* EMG and for languages other than English?
   [66]
3. Can a multi-speaker synthetic EMG generator be conditioned on **your** 8/16-channel montage
   without real paired data from it? [65]
4. Does cross-modal alignment still help when the pretrained audio corpus is **Latvian/Russian**
   rather than English? Unpublished.
5. What is the oracle N-best WER for your own silent-EMG decoder? It bounds every rescoring gain
   [81].
6. What is PiEEG-16's *measured* sustainable sample rate — its own pages say both 500 Hz and
   16 kSPS [32]?
7. Are there live eBay/Allegro/Ricardo OpenBCI or research-grade listings, and what do they actually
   sell for? Only asks were verifiable [15]–[21].
