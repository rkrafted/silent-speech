Track 05-ml-pipeline. Software that turns the signals into words for one user.
- Open datasets: Gaddy silent speech EMG (~20 h), EMG-UKA, AlterEgo data (any public?), Meta's
  emg2qwerty / emg2pose, Chinese sEMG silent-speech corpora 2023–2026.
- Open code: dgaddy/silent_speech, tbenst (MONA LISA) repo, any 2024–2026 repos; licenses.
- Model approaches and results: classification (closed vocab, AlterEgo-style), sequence-to-sequence /
  CTC for open vocabulary, transferring audio targets from voiced to silent speech, LLM rescoring /
  "LLM-assisted" decoding, self-supervised pretraining on EMG, cross-session adaptation.
- How much per-user data is needed for (a) 20–100 command words, (b) open-vocabulary dictation, with
  numbers from papers. Recording protocol (voiced + silent parallel data, prompts, sessions).
- Real-time constraints: latency, phone vs on-device vs PC GPU (owner has an RTX 3090).
- Evaluation: WER/CER, session-to-session drift.
Finish with a staged training plan (commands -> phrases -> open vocab) and expected accuracy at each stage,
citing the evidence.
Output: research/05-ml-pipeline.md
