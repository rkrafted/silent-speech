# PubMed query log — jaw / ear / neck electrode sites for silent speech

Every query string run through NCBI E-utilities `esearch` (db=pubmed), with the hit count
returned on the day of the sweep. `retmax` was capped at 40 per query for the candidate pull.

| # | Topic | Query string | Hits |
|---|---|---|---|
| 1 | silent speech EMG | `silent speech[tiab] AND (EMG[tiab] OR electromyograph*[tiab])` | 40 |
| 2 | subvocal | `(subvocal*[tiab] OR sub-vocal*[tiab]) AND (EMG[tiab] OR electromyograph*[tiab] OR silent speech[tiab])` | 23 |
| 3 | silent speech channels | `silent speech[tiab] AND (electrode*[tiab] OR channel*[tiab])` | 31 |
| 4 | EMG speech channel selection | `(surface EMG[tiab] OR sEMG[tiab]) AND speech[tiab] AND ("channel selection"[tiab] OR "electrode selection"[tiab] OR "channel reduction"[tiab] OR ablation[tiab])` | 1 |
| 5 | EMG electrode site selection | `(electrode selection[tiab] OR electrode placement[tiab] OR optimal electrode*[tiab]) AND (EMG[tiab] OR electromyograph*[tiab]) AND speech[tiab]` | 4 |
| 6 | masseter EMG speech | `masseter[tiab] AND (EMG[tiab] OR electromyograph*[tiab]) AND (speech[tiab] OR articulation[tiab] OR speech recognition[tiab])` | 51 |
| 7 | digastric EMG speech | `digastric[tiab] AND (EMG[tiab] OR electromyograph*[tiab]) AND (speech[tiab] OR articulation[tiab] OR swallowing[tiab])` | 81 |
| 8 | mylohyoid EMG | `mylohyoid[tiab] AND (EMG[tiab] OR electromyograph*[tiab])` | 80 |
| 9 | submental EMG speech | `submental[tiab] AND (EMG[tiab] OR electromyograph*[tiab]) AND (speech[tiab] OR articulation[tiab])` | 14 |
| 10 | platysma EMG | `platysma[tiab] AND (EMG[tiab] OR electromyograph*[tiab])` | 34 |
| 11 | buccinator EMG | `buccinator[tiab] AND (EMG[tiab] OR electromyograph*[tiab])` | 52 |
| 12 | facial EMG articulation | `facial EMG[tiab] AND (speech[tiab] OR articulation[tiab] OR word[tiab])` | 6 |
| 13 | speech surface EMG recognition | `"speech recognition"[tiab] AND ("surface electromyography"[tiab] OR "surface EMG"[tiab] OR sEMG[tiab])` | 21 |
| 14 | EMG speech MeSH | `("Electromyography"[MeSH] AND "Speech"[MeSH])` | 539 |
| 15 | voiceless speech EMG | `(voiceless[tiab] OR mouthed[tiab] OR "silent articulation"[tiab]) AND (EMG[tiab] OR electromyograph*[tiab])` | 17 |
| 16 | jaw kinematics speech | `(jaw[tiab] OR mandib*[tiab]) AND (kinematic*[tiab] OR IMU[tiab] OR acceleromet*[tiab] OR magnet*[tiab]) AND (speech[tiab] OR articulation[tiab])` | 250 |
| 17 | articulography speech decoding | `(articulograph*[tiab] OR EMA[tiab]) AND (speech[tiab] OR silent[tiab]) AND (decoding[tiab] OR recognition[tiab] OR classification[tiab])` | 29 |
| 18 | in-ear EMG | `(in-ear[tiab] OR ear canal[tiab] OR ear-canal[tiab] OR intra-aural[tiab]) AND (EMG[tiab] OR electromyograph*[tiab] OR biopotential*[tiab] OR electrode*[tiab])` | 246 |
| 19 | behind-the-ear electrodes | `(behind-the-ear[tiab] OR behind the ear[tiab] OR retroauricular[tiab] OR mastoid[tiab]) AND (EMG[tiab] OR electrode*[tiab] OR EEG[tiab])` | 604 |
| 20 | ear-EEG speech | `(ear-EEG[tiab] OR ear EEG[tiab] OR in-ear EEG[tiab] OR cEEGrid[tiab]) AND (speech[tiab] OR attention[tiab] OR silent[tiab])` | 36 |
| 21 | dry facial electrodes | `(dry electrode*[tiab] OR dry-contact[tiab]) AND (face[tiab] OR facial[tiab] OR neck[tiab]) AND (EMG[tiab] OR electromyograph*[tiab] OR biopotential*[tiab])` | 10 |
| 22 | textile EMG electrodes | `(textile electrode*[tiab] OR fabric electrode*[tiab] OR conductive textile*[tiab]) AND (EMG[tiab] OR electromyograph*[tiab])` | 49 |
| 23 | tattoo electrodes | `(tattoo[tiab] OR epidermal electrode*[tiab] OR on-skin electrode*[tiab] OR skin-like[tiab]) AND (EMG[tiab] OR electromyograph*[tiab] OR biopotential*[tiab] OR sensor*[tiab])` | 410 |
| 24 | wearable facial acceptability | `(wearable*[tiab] OR wearable device*[tiab]) AND (acceptab*[tiab] OR conceal*[tiab] OR "social acceptability"[tiab] OR stigma[tiab]) AND (face[tiab] OR facial[tiab] OR neck[tiab])` | 80 |
| 25 | silent speech interface | `"silent speech interface"[tiab] OR "silent speech interfaces"[tiab]` | 30 |
| 26 | neck EMG speech | `(neck[tiab] OR laryngeal[tiab] OR paralaryngeal[tiab] OR sternohyoid[tiab] OR genioglossus[tiab]) AND (EMG[tiab] OR electromyograph*[tiab]) AND (speech[tiab] OR word*[tiab] OR recognition[tiab])` | 331 |
| 27 | subvocal recognition | `(subvocal[tiab] OR sub-vocal[tiab]) AND (recognition[tiab] OR decoding[tiab] OR classification[tiab])` | 23 |
| 28 | earable speech | `(earable*[tiab] OR ear-worn[tiab] OR hearable*[tiab] OR earbud*[tiab]) AND (speech[tiab] OR EMG[tiab] OR sensing[tiab])` | 63 |
| 29 | neckband EMG | `(neckband[tiab] OR neck-band[tiab] OR collar[tiab]) AND (EMG[tiab] OR speech[tiab] OR sensor*[tiab])` | 387 |
| 30 | single-channel speech EMG | `(single channel[tiab] OR single-channel[tiab] OR "one channel"[tiab]) AND (EMG[tiab] OR electromyograph*[tiab]) AND (speech[tiab] OR word*[tiab])` | 3 |
| 31 | EMG electrode array face neck | `(electrode array[tiab] OR multichannel[tiab] OR multi-channel[tiab]) AND (facial[tiab] OR face[tiab] OR neck[tiab]) AND (EMG[tiab] OR electromyograph*[tiab])` | 58 |
