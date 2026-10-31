Track 12-fast-personalization. The owner wants to spend ~1 day recording and get the most understanding possible,
"like QLoRA": a big pretrained model + a small personal adapter + a recording script designed for maximum gain per
minute. Research with numbers:
- Pretrain-then-adapt for EMG: per-session/per-user adapters, LoRA/adapter layers, fine-tuning only the input layer
  (electrode-position mapping), session embeddings; results from Gaddy, emg2qwerty personalization, SplashNet,
  multi-subject pretraining (e.g. "3 min calibration"), Meta Nature 2025 personalization, BCI daily recalibration.
  How many minutes of a NEW user's data are needed to reach X% WER/CER when starting from a pretrained model?
- Which English phoneme distinctions silent EMG can and cannot see (voicing p/b t/d k/g, nasals m/b, vowels,
  tongue-back consonants) — articulatory phonetics + EMG confusion matrices from papers. What that implies for
  vocabulary design and language-model help.
- Recording-script design for maximum information per minute: phonetically balanced / diphone-covering prompt sets
  (TIMIT, Harvard sentences, CMU ARCTIC, Rainbow Passage), minimal pairs, how Gaddy chose prompts; active learning
  (record what the model confuses most); optimal session length before fatigue; voiced + silent parallel protocol.
- Can a HUMAN-written list of pronunciation rules/differences help directly (e.g. as phoneme-confusion priors in the
  decoder or LM), versus only by shaping the recording script? Be honest.
- QLoRA's real role here: EMG models are small (tens of M params) so quantization is irrelevant to them; where QLoRA
  DOES fit is fine-tuning a local LLM rescorer/corrector on the owner's domain text on an RTX 3090 — evidence.
Finish with a concrete 1-day (≈6 h, with breaks) recording plan and the adaptation recipe, with expected accuracy.
Output: research/12-fast-personalization.md
