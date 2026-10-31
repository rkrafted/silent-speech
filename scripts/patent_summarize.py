#!/usr/bin/env python3
"""Turn the cached Lens JSON into a compact per-patent summary for the table.

Prints sensor-site keyword hits, electrode mentions and family members so the
facts in research/jaw/patents.md can be written without re-reading raw pages.

usage: python3 scripts/patent_summarize.py [--md]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "research" / "jaw" / "raw"

SITES = [
    "chin", "submental", "submandibular", "submaxillary", "jaw", "masseter",
    "temporalis", "temple", "cheek", "buccal", "zygomatic", "oral", "lip",
    "infraorbital", "mental", "neck", "throat", "larynx", "hyoid", "carotid",
    "ear", "earbud", "ear-canal", "ear canal", "behind the ear", "behind-ear",
    "mastoid", "forehead", "face", "facial", "tragus", "concha", "nose",
    "under-chin", "under the chin", "sublingual", "tongue", "palate",
    # CJK site / signal words
    "\u4e0b\u988c", "\u4e0b\u5df4", "\u9888", "\u9762", "\u8138", "\u988a",
    "\u8033", "\u820c", "\u5507", "\u56bc\u808c", "\u9854", "\u9831",
    "\u808c\u7535", "\u7535\u6781", "\u65e0\u58f0", "\u7f04\u9ed8",
    "\u9854", "\u9996", "\u8033", "\u820c", "\u5507", "\u7b4b\u96fb", "\u96fb\u6975",
    "\ud130", "\ubaa9", "\ubcfc", "\uadc0", "\ud600", "\uc785\uc220", "\uadfc\uc804\ub3c4", "\uc804\uadf9",
]


def hits(text: str, words: list[str]) -> list[str]:
    t = (text or "").lower()
    out = []
    for w in words:
        if w in t:
            out.append(w)
    return out


def electrode_count(text: str) -> str:
    t = (text or "").lower()
    pat = re.findall(r"(\d{1,3})\s*(?:dry\s+|bipolar\s+|surface\s+|disposable\s+)?electrodes?", t)
    return ",".join(sorted(set(pat), key=lambda x: -int(x))[:6]) if pat else ""


def main(argv: list[str]) -> int:
    files = sorted(RAW.glob("lens_*.json"))
    for f in files:
        d = json.loads(f.read_text())
        body = " ".join([d.get("claims", ""), d.get("abstract", ""), d.get("title", "")])
        print(f"===== {d['no']} | {d['status']} | prio {d['priority']} | {d.get('grant_date','')} | term {d.get('term','')}")
        print(f"T: {d['title'][:140]}")
        print(f"A: {'; '.join(d.get('applicants') or [])[:120]}")
        print(f"I: {'; '.join(d.get('inventors') or [])[:160]}")
        print(f"CPC: {','.join(d.get('cpc') or [])[:120]}")
        print(f"FAM({len(d.get('family') or [])}): {','.join((d.get('family') or [])[:14])}")
        print(f"SITES: {','.join(hits(body, SITES))}")
        print(f"ELEC: {electrode_count(body)}")
        ab = (d.get("abstract") or "").strip()
        if ab:
            print(f"ABS: {ab[:420]}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
