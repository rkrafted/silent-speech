Track 10-fasttrack-data. Two questions for a build that must work by 2026-12-31.
A) Buying used acquisition hardware NOW: used/refurbished OpenBCI Cyton (+Daisy), Ganglion, Cerelog, BioAmp, MindRove,
   TMSi, g.tec, Biosemi, Delsys, Bitalino, ADS1299 dev boards (ADS1299EEGFE-PDK) — where they are sold second-hand in the
   EU (eBay, Kleinanzeigen, Allegro, ss.lv, lab auctions), typical used prices, and which one is best for 8–16 ch sEMG at
   1 kHz with low latency. Note fakes/clones and what to check when buying used.
B) Synthetic and transferable data for silent-speech EMG: what is published on (1) EMG data augmentation (noise,
   channel dropout, time warping, electrode-shift simulation), (2) generating synthetic EMG from audio/text (audio-to-EMG,
   GAN/diffusion EMG synthesis), (3) using TTS audio instead of the user's own voiced audio as training targets,
   (4) LLM-generated prompt corpora for recording sessions and domain language models for rescoring,
   (5) cross-language: decoding Latvian or Russian silent speech when pretrained EMG data is English-only.
   Give numbers on how much each actually helps, and what cannot be replaced by synthetic data.
Output: research/10-fasttrack-data.md
