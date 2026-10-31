#!/usr/bin/env python3
"""PubMed sweep for silent-speech electrode sites (stdlib only).

Runs a fixed list of MeSH + free-text queries through NCBI E-utilities, records the
hit count for every query string, and dumps the candidate records (id, title,
journal, year, authors) to a JSON file for manual curation.

Usage:
    python3 scripts/pubmed_sweep.py --out /tmp/pubmed-sweep.json \
        [--queries research/jaw/pubmed-queries.md]

The query log is what gets committed; the candidate JSON stays a working file.
"""
from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) research-sweep/1.0"}

# (topic, PubMed query). Topics map to the item brief: silent-speech EMG, subvocal,
# electrode/channel selection & ablation, per-muscle sites, jaw kinematics, ear
# region, dry/textile/skin-like electrodes, concealment/acceptability.
QUERIES: list[tuple[str, str]] = [
    ("silent speech EMG", 'silent speech[tiab] AND (EMG[tiab] OR electromyograph*[tiab])'),
    ("subvocal", '(subvocal*[tiab] OR sub-vocal*[tiab]) AND (EMG[tiab] OR electromyograph*[tiab] OR silent speech[tiab])'),
    ("silent speech channels", 'silent speech[tiab] AND (electrode*[tiab] OR channel*[tiab])'),
    ("EMG speech channel selection", '(surface EMG[tiab] OR sEMG[tiab]) AND speech[tiab] AND ("channel selection"[tiab] OR "electrode selection"[tiab] OR "channel reduction"[tiab] OR ablation[tiab])'),
    ("EMG electrode site selection", '(electrode selection[tiab] OR electrode placement[tiab] OR optimal electrode*[tiab]) AND (EMG[tiab] OR electromyograph*[tiab]) AND speech[tiab]'),
    ("masseter EMG speech", 'masseter[tiab] AND (EMG[tiab] OR electromyograph*[tiab]) AND (speech[tiab] OR articulation[tiab] OR speech recognition[tiab])'),
    ("digastric EMG speech", 'digastric[tiab] AND (EMG[tiab] OR electromyograph*[tiab]) AND (speech[tiab] OR articulation[tiab] OR swallowing[tiab])'),
    ("mylohyoid EMG", 'mylohyoid[tiab] AND (EMG[tiab] OR electromyograph*[tiab])'),
    ("submental EMG speech", 'submental[tiab] AND (EMG[tiab] OR electromyograph*[tiab]) AND (speech[tiab] OR articulation[tiab])'),
    ("platysma EMG", 'platysma[tiab] AND (EMG[tiab] OR electromyograph*[tiab])'),
    ("buccinator EMG", 'buccinator[tiab] AND (EMG[tiab] OR electromyograph*[tiab])'),
    ("facial EMG articulation", 'facial EMG[tiab] AND (speech[tiab] OR articulation[tiab] OR word[tiab])'),
    ("speech surface EMG recognition", '"speech recognition"[tiab] AND ("surface electromyography"[tiab] OR "surface EMG"[tiab] OR sEMG[tiab])'),
    ("EMG speech MeSH", '("Electromyography"[MeSH] AND "Speech"[MeSH])'),
    ("voiceless speech EMG", '(voiceless[tiab] OR mouthed[tiab] OR "silent articulation"[tiab]) AND (EMG[tiab] OR electromyograph*[tiab])'),
    ("jaw kinematics speech", '(jaw[tiab] OR mandib*[tiab]) AND (kinematic*[tiab] OR IMU[tiab] OR acceleromet*[tiab] OR magnet*[tiab]) AND (speech[tiab] OR articulation[tiab])'),
    ("articulography speech decoding", '(articulograph*[tiab] OR EMA[tiab]) AND (speech[tiab] OR silent[tiab]) AND (decoding[tiab] OR recognition[tiab] OR classification[tiab])'),
    ("in-ear EMG", '(in-ear[tiab] OR ear canal[tiab] OR ear-canal[tiab] OR intra-aural[tiab]) AND (EMG[tiab] OR electromyograph*[tiab] OR biopotential*[tiab] OR electrode*[tiab])'),
    ("behind-the-ear electrodes", '(behind-the-ear[tiab] OR behind the ear[tiab] OR retroauricular[tiab] OR mastoid[tiab]) AND (EMG[tiab] OR electrode*[tiab] OR EEG[tiab])'),
    ("ear-EEG speech", '(ear-EEG[tiab] OR ear EEG[tiab] OR in-ear EEG[tiab] OR cEEGrid[tiab]) AND (speech[tiab] OR attention[tiab] OR silent[tiab])'),
    ("dry facial electrodes", '(dry electrode*[tiab] OR dry-contact[tiab]) AND (face[tiab] OR facial[tiab] OR neck[tiab]) AND (EMG[tiab] OR electromyograph*[tiab] OR biopotential*[tiab])'),
    ("textile EMG electrodes", '(textile electrode*[tiab] OR fabric electrode*[tiab] OR conductive textile*[tiab]) AND (EMG[tiab] OR electromyograph*[tiab])'),
    ("tattoo electrodes", '(tattoo[tiab] OR epidermal electrode*[tiab] OR on-skin electrode*[tiab] OR skin-like[tiab]) AND (EMG[tiab] OR electromyograph*[tiab] OR biopotential*[tiab] OR sensor*[tiab])'),
    ("wearable facial acceptability", '(wearable*[tiab] OR wearable device*[tiab]) AND (acceptab*[tiab] OR conceal*[tiab] OR "social acceptability"[tiab] OR stigma[tiab]) AND (face[tiab] OR facial[tiab] OR neck[tiab])'),
    ("silent speech interface", '"silent speech interface"[tiab] OR "silent speech interfaces"[tiab]'),
    ("neck EMG speech", '(neck[tiab] OR laryngeal[tiab] OR paralaryngeal[tiab] OR sternohyoid[tiab] OR genioglossus[tiab]) AND (EMG[tiab] OR electromyograph*[tiab]) AND (speech[tiab] OR word*[tiab] OR recognition[tiab])'),
    ("subvocal recognition", '(subvocal[tiab] OR sub-vocal[tiab]) AND (recognition[tiab] OR decoding[tiab] OR classification[tiab])'),
    ("earable speech", '(earable*[tiab] OR ear-worn[tiab] OR hearable*[tiab] OR earbud*[tiab]) AND (speech[tiab] OR EMG[tiab] OR sensing[tiab])'),
    ("neckband EMG", '(neckband[tiab] OR neck-band[tiab] OR collar[tiab]) AND (EMG[tiab] OR speech[tiab] OR sensor*[tiab])'),
    ("single-channel speech EMG", '(single channel[tiab] OR single-channel[tiab] OR "one channel"[tiab]) AND (EMG[tiab] OR electromyograph*[tiab]) AND (speech[tiab] OR word*[tiab])'),
    ("EMG electrode array face neck", '(electrode array[tiab] OR multichannel[tiab] OR multi-channel[tiab]) AND (facial[tiab] OR face[tiab] OR neck[tiab]) AND (EMG[tiab] OR electromyograph*[tiab])'),
]


def get(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def esearch(term: str, retmax: int = 40) -> tuple[int, list[str]]:
    q = urllib.parse.urlencode({"db": "pubmed", "term": term, "retmode": "json", "retmax": str(retmax)})
    d = json.loads(get(f"{BASE}/esearch.fcgi?{q}"))
    res = d["esearchresult"]
    return int(res.get("count", 0)), list(res.get("idlist", []))


def esummary(ids: list[str]) -> dict:
    out: dict = {}
    for i in range(0, len(ids), 100):
        chunk = ids[i : i + 100]
        q = urllib.parse.urlencode({"db": "pubmed", "id": ",".join(chunk), "retmode": "json"})
        d = json.loads(get(f"{BASE}/esummary.fcgi?{q}"))
        out.update(d.get("result", {}))
        time.sleep(0.4)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=".scratch/pubmed-sweep.json")
    ap.add_argument("--queries", default="research/jaw/pubmed-queries.md")
    a = ap.parse_args()

    log_lines = [
        "# PubMed query log — jaw / ear / neck electrode sites for silent speech",
        "",
        "Every query string run through NCBI E-utilities `esearch` (db=pubmed), with the hit count",
        "returned on the day of the sweep. `retmax` was capped at 40 per query for the candidate pull.",
        "",
        "| # | Topic | Query string | Hits |",
        "|---|---|---|---|",
    ]
    all_ids: list[str] = []
    per_query: dict[str, list[str]] = {}
    for i, (topic, term) in enumerate(QUERIES, 1):
        try:
            count, ids = esearch(term)
        except Exception as e:  # keep going; log the failure
            print(f"[{i}] {topic}: ERROR {type(e).__name__}: {e}")
            log_lines.append(f"| {i} | {topic} | `{term}` | error |")
            continue
        per_query[topic] = ids
        all_ids.extend(ids)
        print(f"[{i}] {topic}: {count} hits, {len(ids)} pulled")
        log_lines.append(f"| {i} | {topic} | `{term}` | {count} |")
        time.sleep(0.4)

    uniq = list(dict.fromkeys(all_ids))
    print(f"unique PMIDs: {len(uniq)}")
    summ = esummary(uniq)
    records = []
    for pmid in uniq:
        r = summ.get(pmid, {})
        if not isinstance(r, dict) or "error" in r:
            continue
        auth = [x.get("name", "") for x in r.get("authors", [])][:12]
        records.append(
            {
                "pmid": pmid,
                "title": r.get("title", "").rstrip("."),
                "journal": r.get("source", ""),
                "year": (r.get("pubdate", "") or "")[:4],
                "authors": auth,
                "pubtype": r.get("pubtype", []),
            }
        )
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps({"queries": per_query, "records": records}, indent=1))
    Path(a.queries).write_text("\n".join(log_lines) + "\n")
    print(f"wrote {a.out} ({len(records)} records) and {a.queries}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
