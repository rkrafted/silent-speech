# What the OpenBCI forum knows that matters for the hidden jaw-EMG wearable

This is the forum sweep for the hidden jaw-integrated silent-speech prototype. It reads the 300
highest-scoring threads of the OpenBCI forum (kept by `scripts/forum_prefilter.py` into
`research/jaw/forum-selection.tsv`), extracts what each thread says with the runner's local 27B
model (`research/jaw/forum-extracts.jsonl`), spot-checks 30 of those extracts against the raw posts
(`research/jaw/forum-spotcheck.md`), and writes down only what changes the build or the recording
plan in `research/jaw/prototype-v1.md`.

Plain summary up front: the forum strongly validates the direction of v1. It says use an ADS1299
front end with dry-matched metal, run the bias loop exactly as the reference design does, do not
bother chasing wet-electrode impedance, keep the wireless link modest (250-500 Hz/channel is
enough), and prefer a BLE SoC over WiFi on the head. It also flags the PiEEG ground strategy, the
near-total absence of Cerelog data, and a handful of ESP32 streaming traps.

Every link below is `openbci.com/forum/...` and every linked thread is also a row in
`research/jaw/sources-forum.jsonl` (kind `web`).

---

## (a) The 18 things that change our build or our recording plan

### 1. Set the ADS1299 gain to x8 or x12 for dry electrodes, never leave the x24 default

The single most common self-inflicted failure in the whole kept set. A dry or active electrode has
a large offset; at the x24 EEG default the ADS1299 rails at +/-187,500 uV and the channel looks
dead or saturated. The thread's answer is to set x8, sometimes x12, before streaming, and to send
the gain command with Brainflow's `config_board()`:
<https://openbci.com/forum/index.php?p=/discussion/2869/thinkpulse-active-electrodes-q-a>.
This changes §2 (Stage 1) and §4.1 of `prototype-v1.md`: the PiEEG-16 bring-up script must set gain
before the first jaw channel is recorded.

### 2. Stop chasing low impedance on dry pads — 1-2 MOhm is fine for the ADS1299

Measured dry-electrode impedances in the thread run 100-200 kOhm, and 2.8-4.8 MOhm still does not
rail; the ADS1299 has a 1 GOhm input, so 1 MOhm is a <0.1% error and 2 MOhm is 0.2%. The GUI's
RAILED flag on a dry pad usually means contact or reference trouble, not "impedance too high":
<https://openbci.com/forum/index.php?p=/discussion/2476/impedances-less-with-pressure-what-is-normal-range-resolved>.
This removes an acceptance gate we did not need in §4 of `prototype-v1.md`.

### 3. An active electrode makes the ADS1299 impedance reading meaningless

A side-by-side active-vs-passive dry cap comparison shows the active buffer drops the lead-off
reading from ~40 kOhm to ~4 kOhm while the recorded SNR and 50 Hz noise are essentially unchanged:
<https://openbci.com/forum/index.php?p=/discussion/928/skin-impedance-measurement-of-active-vs-passive-electrodes>.
Judge the jaw-arm pads by recorded noise, not by the GUI impedance number.

### 4. Wire the BIAS loop exactly like the reference design, then test it

The forum repeats the same topology in several threads. One BIAS/body electrode for all
differential EMG channels, the EMG channels taken off the SRB2 and BIAS busses, and the
BIAS_DRV-to-BIAS_INV feedback bridge present on the board; without that bridge the bias loop
floats, CMRR drops and 50 Hz comes back:
<https://openbci.com/forum/index.php?p=/discussion/1166/why-we-need-reference-electrodes-in-bi-polar-configuration>,
<https://openbci.com/forum/index.php?p=/discussion/1651/myoware-and-emg-need-to-adjust-srb-bias>,
<https://openbci.com/forum/index.php?p=/discussion/2162/understanding-the-bias-pin-with-myoware-ecg>,
<https://openbci.com/forum/index.php?p=/discussion/3553/bias-feedback>,
<https://openbci.com/forum/index.php?p=/discussion/2917/bias-pinout>.
`prototype-v1.md` §4.1 already puts REF below the left ear and BIAS below the right; the forum says
also confirm the on-board bridge and keep one bias only.

### 5. Never use AGND as the EMG reference in a mixed montage

A combined EEG/EMG/EOG recording picked up heavy 50 Hz on the EMG channel because AGND was the
reference; removing that lead, using BIAS instead and switching the channel off SRB/Bias fixed it:
<https://openbci.com/forum/index.php?p=/discussion/2687/eeg-cap-kit-noise-issue-eeg-emg-eog-agnd-resolved>.
For the borrowed-EMG week this is a one-line fix with a large effect.

### 6. A custom ADS1299 board must not tie unused inputs to AVDD

With SRB2 on, every unused IN*P pin is bussed to AVDD, so tying unused inputs to the analog supply
pulls the whole front end to the rail — this is the exact bug in one DIY Cyton:
<https://openbci.com/forum/index.php?p=/discussion/2251/diy-cyton-board-ads1299-clamping-signal>.
Add it to the §5 PCB design review checklist.

### 7. Match the electrode metals — mixed metals create galvanic offset and noise

Two threads trace unstable low-frequency noise to mixing gold ear clips with silver-chloride dry
electrodes, and to stainless steel as an electrode metal. The fix is one metal family for signal,
reference and bias, plus a 0.5 Hz high-pass for the DC offset that remains:
<https://openbci.com/forum/index.php?p=/discussion/2648/noise-in-signal-from-my-diy-ads1299-board-not-cyton>,
<https://openbci.com/forum/index.php?p=/discussion/3594/very-strong-noise-in-the-delta-waves-range>,
<https://openbci.com/forum/index.php?p=/discussion/1720/very-high-dc-offset-maxes-out-adc>.
This is a BOM rule for the jaw-arm pads and the behind-ear reference.

### 8. 250 Hz is enough for the silent-speech envelope; 1 kHz is only for waveform shape

The forum is consistent: 250 Hz preserves the EMG amplitude envelope (about 20% of the energy above
250 Hz is lost, which does not matter for an envelope/decoder), while exact waveform work wants
800 Hz-1 kHz. Facial motor units rarely exceed 100 Hz, so a 10-125 Hz band is the practical
face-EMG band:
<https://openbci.com/forum/index.php?p=/discussion/1532/required-sampling-rate-for-emg>,
<https://openbci.com/forum/index.php?p=/discussion/1494/sample-rate-of-1khz-for-emg-cursor-control-how>.
This lowers the throughput requirement in `prototype-v1.md` §2 and §4: our BLE pod does not need
16 channels at 1 kHz to carry a silent-speech signal.

### 9. The ADS1299 needs no external analog anti-aliasing filter

The data rate sets the sinc-filter bandwidth, and the front-end RC (about 72 kHz) is only EMI
protection; at 1 kHz every frequency above 500 Hz is already removed:
<https://openbci.com/forum/index.php?p=/discussion/1753/anti-aliasing-filters-for-emg-application>.
Drop the analog anti-alias stage from the §2 Stage-2 front-end plan.

### 10. There is no hardware 50/60 Hz notch — plan a software notch and matched impedances

The GUI 50/60 Hz switch is a computer-side notch; the hardware relies on ADS1299 CMRR and the BIAS
drive, and tolerates 50-150 mVpp of interference before saturating:
<https://openbci.com/forum/index.php?p=/discussion/136/50hz-power-filter-rather-than-60hz-power-filter>.
For our 50 Hz region: software notch/bandpass, matched impedances, and a working bias loop — not a
hardware filter.

### 11. Ground, reference and signal must not be shorted or crowded

"Do not short ground and reference"; keep the active signal pads away from ground and reference;
the reference can sit on the midline and the bias ground radiates the counter-mains signal more
evenly from the midline:
<https://openbci.com/forum/index.php?p=/discussion/3788/how-far-apart-do-ground-ref-and-signal-electrodes-have-to-be>.
This constrains the tiny geometry of the Option-A jaw arm, where the pads are close together.

### 12. Expect Cyton-class timing drift; use LSL/Brainflow and calibrate timestamps

The Cyton hardware is stable at 250/125 Hz but has no crystal (measured ~250.3 Hz), and the erratic
111-399 Hz readings come from the OS and serial buffering. LSL or a Brainflow TCP stream is more
stable than OSC/GUI, and marker timing drifted 200-300 ms over 10 minutes:
<https://openbci.com/forum/index.php?p=/discussion/2329/how-steady-is-cytons-sampling-rate-resolved>.
Our own pod has a real crystal, but the borrowed-rig analysis in §4 still needs a timestamp
calibration step and should not trust GUI-displayed rates.

### 13. Put an acoustic sync track on a low-gain, attenuated channel

If a silent-speech recording needs an audio marker, feed the line/mic signal through a voltage
divider to <200 uV, set the channel gain to 1x, take it off bias/SRB2, and keep the cable away from
the EMG leads:
<https://openbci.com/forum/index.php?p=/discussion/1512/recording-microphone-audio-signals-on-openbci-for-use-as-a-trigger-channel>.
Alternatively, the Cyton cannot generate a deterministic TTL output at all, so any stimulator
trigger has to be generated by a separate microcontroller and captured on the aux channels:
<https://openbci.com/forum/index.php?p=/discussion/4130/ttl-trigger-output-synchronization-for-external-electrical-stimulator>.

### 14. For 16 channels at 1 kHz the stock OpenBCI radio is the bottleneck

16 channels at 1 kHz needs roughly 400 kb/s; the RFduino BLE link is capped low, and the thread's
routes are SPI WiFi, BT 2.x modules or isolated USB serial:
<https://openbci.com/forum/index.php?p=/discussion/712/prospects-for-higher-sample-rates>. The
16-channel Daisy path defaults to 125 Hz for the same reason:
<https://openbci.com/forum/index.php?p=/discussion/614/change-sampling-rate-frequency>. This is the
quantitative reason `prototype-v1.md` §2 rules out a Cyton purchase.

### 15. On the head, use BLE (nRF52840/nRF5340), not ESP32 WiFi

A DIY ADS1299 headset thread spells it out: ESP32 WiFi draws 150-200 mA at 20 dBm and adds EMI;
nRF52840 BLE draws 5-10 mA at +4 dBm, with 7.5 ms connection intervals and packet
retransmission, and the DK firmware ports straight to a Raytac MDBT50Q module:
<https://openbci.com/forum/index.php?p=/discussion/4125/diy-eeg-headset-does-my-ads1299-based-architecture-make-sense>.
This is independent confirmation of the nRF5340 choice in the v1 pod.

### 16. The cheap ESP32+ADS1299 streaming route has a real software trap

A custom ESP32 board speaks the Cyton WiFi protocol to OpenBCI GUI 4.1.2 but cannot start streaming
on GUI 5.0.4+ (`BOARD_WRITE_ERROR`), and the GUI reads its bias/SRB register bits back wrongly; no
fix was posted:
<https://openbci.com/forum/index.php?p=/discussion/3552/once-cannot-start-the-system-session-but-twice>.
If the bench recorder uses that route, pin the software version and verify the register readback
before recording anything.

### 17. The cEEGrid really does see jaw and peri-auricular muscle activity

The cEEGrid author confirms it works for jaw clenching, peri-auricular EMG and trigeminal/jaw
reflexes with feature engineering plus simple ML, at 1-60 Hz with Cyton+Daisy (125 Hz) or 1-125 Hz
with Cyton only (250 Hz):
<https://openbci.com/forum/index.php?p=/discussion/4131/using-ceegrid-for-trigeminal-jaw-reflex-electrophysiology>.
This supports the Option-A behind-ear pod as an ear-worn jaw sensor, not only an EEG sensor.

### 18. With cEEGrid + Daisy, the SRB2 Y-split is what keeps all 16 channels alive

Two threads report half the channels or all channels dying/jumping; the fix in both is the REF
electrode split to the SRB2 pin on both boards and a solid reference contact:
<https://openbci.com/forum/index.php?p=/discussion/3887/openbci-ceegrids-cythondaisy-board-gui>,
<https://openbci.com/forum/index.php?p=/discussion/4091/ceegrid-missing-second-half-of-channels-9-16>.
If the borrowed week or the hidden-set test uses the OpenBCI cEEGrid, check this first.

---

## (b) The parts we plan to buy: known problems and their fixes

### PiEEG-16

The forum has almost nothing on it. The prefilter pinned every thread that mentions PiEEG; three are
kept, but only two say anything about the board: the question "will OpenBCI headband cables fit a
third-party PiEEG IronBCI board?" is answered yes, because they are plain 0.1" (2.54 mm) female
headers
(<https://openbci.com/forum/index.php?p=/discussion/4124/eeg-headband-kit-compatibility-with-third-party-boards>),
and the one substantive thread warns that the current PiEEG board may not follow TI star-ground and
multi-plane practice and recommends tying the Pi digital ground to the client as a noise
workaround, and to run it battery-powered
(<https://openbci.com/forum/index.php?p=/discussion/3900/in-search-of-old-hardware-schematic-for-the-ads1299-breakout-board>).
**Fix / action:** treat the PiEEG-16 as a bench recorder with a measurable noise floor, not a
finished wearable front end. Before the recording week, capture a 5-minute shorted-input noise
record with (i) the Pi grounded as shipped, (ii) the Pi on a battery, and (iii) the Pi digital
ground tied to the client as the vendor suggests; pick the quietest. The header answer means we can
reuse OpenBCI-style electrode cables with the PiEEG, which removes an adapter from the BOM.

### Cerelog ESP-EEG

The entire 300-thread kept set contains exactly one Cerelog mention, inside a pipeline thread's
"next priorities" list — a Cerelog 16-channel v2 board and "Cerelog and OpenBci EMG" — with no
price, noise figure, wiring or pinout at all:
<https://openbci.com/forum/index.php?p=/discussion/4153/open-source-praycg-pipeline-openbci-lsl-media-protocol-timing-qc-and-exploratory-eeg-autonomic>.
**Fix / action:** the forum cannot de-risk this buy. Get the noise floor and input-referred noise
from the vendor datasheet and confirm the ESP32 board's dropout/throughput before treating the
Cerelog as the EU alternative in `prototype-v1.md` §2. It is not on the list of things the
community has tested.

### ADS1299 modules (PiEEG, Cerelog, custom board)

The forum is a good bug list for the silicon itself:

- **Gain railing at x24 with dry electrodes** — set x8/x12:
  <https://openbci.com/forum/index.php?p=/discussion/2869/thinkpulse-active-electrodes-q-a>.
- **Unused inputs tied to AVDD** pull the whole front end to the rail when SRB2 is on:
  <https://openbci.com/forum/index.php?p=/discussion/2251/diy-cyton-board-ads1299-clamping-signal>.
- **Bias loop must have BIAS_DRV joined to BIAS_INV**; without it the driven reference floats and
  50 Hz returns:
  <https://openbci.com/forum/index.php?p=/discussion/2917/bias-pinout>,
  <https://openbci.com/forum/index.php?p=/discussion/3553/bias-feedback>.
- **A mistuned or floating bias network oscillates** when dry contact is intermittent
  (impedance-dependent low-frequency instability):
  <https://openbci.com/forum/index.php?p=/discussion/3953/low-frequency-noise-instability-when-bias-amp-is-used-on-custom-cyton-based-board>.
- **VREF must be 0.5 V** between VREFP and VREFN, and the reference/bias wiring has to match the
  firmware's SRB1/SRB2 configuration, or the input is dominated by common-mode junk:
  <https://openbci.com/forum/index.php?p=/discussion/1171/ads1299-common-mode-interference-problem>.
- **Mixed metals and steel** are the dominant DC-offset/1-f noise source:
  <https://openbci.com/forum/index.php?p=/discussion/3594/very-strong-noise-in-the-delta-waves-range>.

**Fix:** copy the Cyton bias/RC values, keep AVDD away from unused inputs, verify BIAS_DRV-BIAS_INV
continuity and VREF=0.5 V at bring-up, and make `prototype-v1.md` §5 week-8's design review check
exactly these five items.

### ESP32 streaming (the OpenBCI WiFi shield and DIY ESP32+ADS1299 boards)

- The WiFi shield caps at about 1 kHz in practice and needs its own 4xAA pack to keep the radio
  current off the amplifier supply:
  <https://openbci.com/forum/index.php?p=/discussion/2997/how-do-we-change-the-sampling-frequency-of-the-wifi-board>.
- The RFduino BLE link on the Cyton is the throughput ceiling in the first place
  (<https://openbci.com/forum/index.php?p=/discussion/1105/how-to-practically-increase-sample-rate>).
- A custom ESP32+ADS1299 board that implements the Cyton WiFi protocol fails on GUI 5.0.4+ with
  `BOARD_WRITE_ERROR` and misreports CHnSET bits; serial boards read the settings correctly while
  WiFi ones do not
  (<https://openbci.com/forum/index.php?p=/discussion/3552/once-cannot-start-the-system-session-but-twice>).
- Keeping the radio on the same board as the ADS1299 is itself a noise source; the same board and
  layout problems show up as extra delta-band noise when switching from Bluetooth to WiFi
  (<https://openbci.com/forum/index.php?p=/discussion/3594/very-strong-noise-in-the-delta-waves-range>).

**Fix:** for the wearable, use the nRF5340 BLE path (20 dBm WiFi is the wrong radio on the head);
for the bench, run the ESP32/WiFi radio on a separate battery and verify protocol compatibility
against the exact GUI/driver version before a session.

---

## (c) EMG, face and jaw reports

The forum's EMG-on-the-face material is thin but on-point, and it repeatedly says what this project
already assumes.

- **Face EMG is the right modality for speech, not EEG.** In a thread asking for real-time speech
  from an EEG headset, the moderator answers that EEG resolution is too low for detailed speech and
  that EMG around the mouth and jaw is the better route:
  <https://openbci.com/forum/index.php?p=/discussion/4063/real-time-speech-recognition>. The same
  answer recurs for a "verbal mind reading" request, which is pointed at subvocalization/facial EMG
  instead:
  <https://openbci.com/forum/index.php?p=/discussion/3920/verbal-mind-reading-using-openbci-tech>.
- **Subvocalization on the face rails easily.** A user recording subvocalization with paste and
  gold cups rails the Cyton; the fix is a lower scale/gain for EMG, the reference placed near the
  muscle, and trying several ground/reference positions:
  <https://openbci.com/forum/index.php?p=/discussion/2401/subvocalization-pins-settings>. This is the
  first thing to get right in the borrowed-EMG week.
- **Throat/under-chin sEMG electrodes.** Foam pre-gelled Ag/AgCl button electrodes with snap
  connectors are recommended for sEMG over gold cups, and the thread's use case (throat EMG for
  subvocalization) is ours:
  <https://openbci.com/forum/index.php?p=/discussion/2226/using-the-ganglion-board-to-read-emg-detecting-subvocalizations-for-biofeedback-to-train-suppression>.
- **Snap electrodes are the comfortable face option**, and Cyton+Daisy samples all 16 channels at
  exactly the same instant:
  <https://openbci.com/forum/index.php?p=/discussion/1290/newbie-question-openbci-for-surface-emg-eeg-of-cranial-nerves>.
  That simultaneous sampling is what makes the paired subset scoring in `prototype-v1.md` §4.3
  valid.
- **250 Hz facial EMG with a 10-125 Hz band is a working interface**, not a compromise:
  <https://openbci.com/forum/index.php?p=/discussion/1494/sample-rate-of-1khz-for-emg-cursor-control-how>.
- **Electrode repeatability across sessions is the first gate.** A current builder's
  leakage-controlled baselines on public imagined/silent-speech data show sEMG voiced-to-silent
  transfer above null while EEG spoken-to-imagined does not, that same-trial splits fake a transfer
  effect (8.7%, p=0.0002) that temporal-block splits remove (6.4%, chance), and that electrode
  repeatability must be measured before any decoding claim:
  <https://openbci.com/forum/index.php?p=/discussion/4158/leakage-controlled-baselines-on-3-public-imagined-silent-speech-datasets-before-building-a-16-ch-rig>.
  Add the temporal-block split as a hard rule to the §4.3 analysis and the day-2 re-donning
  session.
- **Dry face pads need a lower-impedance front end than a Ganglion.** A Ganglion (AD8237) shows
  large mains-driven step artifacts near AC equipment where an ADS1299 Cyton does not, because of
  the 1 GOhm ADS1299 input:
  <https://openbci.com/forum/index.php?p=/discussion/2743/sensitivity-to-background-noise-problem-ganglion-vs-cython>.
  This is why the prototype picks ADS1299-class silicon for the dry jaw arm.
- **Dry electrode tips wear out and then throw intermittent 50 Hz bursts.** One user's FRI comb tips
  had worn through their AgCl coating; the advice is to inspect or replace the tips, and to rule out
  the WiFi shield, before blaming the recording setup:
  <https://openbci.com/forum/index.php?p=/discussion/1505/help-with-50-hz-noise-bursts>.
- **MyoWare naming lies about "reference".** MyoWare uses [mid, end, reference] while OpenBCI uses
  [electrode, reference, ground], so a MyoWare "reference" is not a body ground:
  <https://openbci.com/forum/index.php?p=/discussion/3425/why-is-there-no-ground-electrode-on-myoware>.
- **MyoWare pre-processing is unnecessary on an ADS1299.** For raw multi-muscle EMG the advice is
  Cyton, not MyoWare, because the ADS1299 already streams raw EMG:
  <https://openbci.com/forum/index.php?p=/discussion/1907/myoware-measuring-muscle-fatigue-asking-for-hardware-advice>.

---

## (d) What to avoid

1. **Steel, and mixed metals, on the skin.** Stainless steel is the primary noise source in one
   build; gold+AgCl mixtures cause galvanic offset:
   <https://openbci.com/forum/index.php?p=/discussion/3594/very-strong-noise-in-the-delta-waves-range>,
   <https://openbci.com/forum/index.php?p=/discussion/2648/noise-in-signal-from-my-diy-ads1299-board-not-cyton>.
2. **AGND as the EMG reference** in any montage that also has EEG:
   <https://openbci.com/forum/index.php?p=/discussion/2687/eeg-cap-kit-noise-issue-eeg-emg-eog-agnd-resolved>.
3. **Leaving the ADS1299 at the x24 EEG gain** with dry pads:
   <https://openbci.com/forum/index.php?p=/discussion/2869/thinkpulse-active-electrodes-q-a>.
4. **Tying unused ADS1299 inputs to AVDD** while SRB2 is on:
   <https://openbci.com/forum/index.php?p=/discussion/2251/diy-cyton-board-ads1299-clamping-signal>.
5. **ESP32 WiFi on the head** (EMI + 150-200 mA) and **the DIY ESP32+ADS1299 Cyton-protocol route**
   on current GUI versions:
   <https://openbci.com/forum/index.php?p=/discussion/4125/diy-eeg-headset-does-my-ads1299-based-architecture-make-sense>,
   <https://openbci.com/forum/index.php?p=/discussion/3552/once-cannot-start-the-system-session-but-twice>.
6. **Trusting the Cerelog hype without a datasheet or bench noise floor.** One mention, zero data:
   <https://openbci.com/forum/index.php?p=/discussion/4153/open-source-praycg-pipeline-openbci-lsl-media-protocol-timing-qc-and-exploratory-eeg-autonomic>.
7. **Expecting medical certification to be the blocker.** The boards are not medical devices, the
   battery design is the shock protection, and the Cyton-vs-g.tec comparison paper is the published
   precedent for IRB:
   <https://openbci.com/forum/index.php?p=/discussion/2704/do-openbci-products-have-international-approval>.
8. **Skipping the cEEGrid Y-split** and blaming the electrodes when half the channels die:
   <https://openbci.com/forum/index.php?p=/discussion/3887/openbci-ceegrids-cythondaisy-board-gui>.

---

## What this changes in `prototype-v1.md`

| prototype-v1 § | Change forced by the forum |
|---|---|
| §2 Stage 1 (PiEEG-16) | Add a shorted-input noise-floor test and the PiEEG ground-tie experiment before the PiEEG is trusted; OpenBCI-style 0.1" cables fit it. |
| §2 Stage 1 (Cerelog) | Mark the Cerelog as "not community-tested"; require vendor input-referred-noise and dropout figures. |
| §2 Stage 2 (front end) | Drop the external analog anti-alias stage; add the five ADS1299 bring-up checks (gain x8/x12, no AVDD on unused inputs, BIAS_DRV-BIAS_INV, VREF 0.5 V, star ground). |
| §2 Stage 2 (radio) | Keep nRF5340 BLE; the forum's power/EMI numbers (5-10 mA BLE vs 150-200 mA WiFi) confirm it. |
| §4.1 (electrode map) | One BIAS only; EMG channels off SRB2/BIAS; REF/BIAS not crowded against the signal pads; matched metals. |
| §4.2 / §4.3 | Calibrate timestamps, use LSL/Brainflow, and add a temporal-block split to the analysis; add an electrode-repeatability check on day 2. |
| §4.4 (decision rule) | Unchanged, but the analysis now has to pass the temporal-block split before the WER gap is believed. |

## Provenance and how to re-run

- Input: `data/raw/openbci-forum/threads.jsonl`, 1330 threads (gitignored; lives in the main
  checkout). This session did not fetch the forum again.
- Selection: `python3 scripts/forum_prefilter.py` writes `research/jaw/forum-selection.tsv`
  (300 kept threads, score and rare-part pins) and `local_batch/forum-prompts.jsonl`.
- Extraction: `local_batch/forum.yaml` — the runner's own local batch served
  `research/jaw/forum-extracts.jsonl` (300 lines, `qwen3.8-27b-uncensored`, `format: json`). That
  file is runner-written and was not edited.
- Spot-check: `research/jaw/forum-spotcheck.md`, 30 extracts checked against the raw posts.
- Sources: `research/jaw/sources-forum.jsonl`, 37 threads, all HTTP-checked live by
  `~/theprojects/orchestrator/bin/check_sources.py ... --kinds web`.
