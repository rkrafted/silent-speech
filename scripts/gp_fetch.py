#!/usr/bin/env python3
"""Read public Google Patents pages by publication number into compact JSON.

usage: python3 scripts/gp_fetch.py US20230088533A1 [more numbers ...]

Writes research/jaw/raw/google/<number>.json (gitignored) with the title, assignee,
inventors, priority/filing/publication dates, legal status, CPC codes and the text of
claim 1. Only publication numbers are sent to the host: no query, no description of our
device. Parsing is regex over the served HTML because the page carries schema.org
microdata; no extra packages.
"""
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "research" / "jaw" / "raw" / "google"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124 Safari/537.36")
URL = "https://patents.google.com/patent/{no}/en"


def fetch(no: str) -> str:
    r = subprocess.run(
        ["curl", "-sS", "-L", "-m", "60", "-A", UA, URL.format(no=no)],
        capture_output=True, text=True,
    )
    if r.returncode != 0 or not r.stdout:
        raise RuntimeError(f"{no}: curl failed ({r.returncode}) {r.stderr[:200]}")
    return r.stdout


def first(pat: str, text: str) -> str:
    m = re.search(pat, text, re.S)
    return html.unescape(m.group(1)).strip() if m else ""


def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def claim1(page: str) -> str:
    """First claim, for both the US (CLM-00001) and WO (num="1", <li>) markup."""
    m = re.search(r'<div id="CLM-00001"[^>]*>(.*?)(?=<div id="CLM-00002"|</div>\s*</div>\s*</div>)', page, re.S)
    if not m:
        m = re.search(r'<li class="claim">\s*<div num="1" class="claim">(.*?)</li>', page, re.S)
    return strip_tags(m.group(1)) if m else ""


def parse(no: str, page: str) -> dict:
    contributors = re.findall(r'<meta name="DC.contributor" content="([^"]*)" scheme="([^"]*)"', page)
    people = {scheme: [] for _, scheme in contributors}
    for name, scheme in contributors:
        people.setdefault(scheme, []).append(html.unescape(name).strip())
    cpc = []
    for code, desc, is_cpc in re.findall(
            r'<li itemprop="classifications"[^>]*>.*?<span itemprop="Code">(.*?)</span>.*?'
            r'<span itemprop="Description">(.*?)</span>.*?'
            r'<meta itemprop="IsCPC" content="(true|false)">', page, re.S):
        if is_cpc == "true":
            cpc.append({"code": html.unescape(code).strip(), "desc": html.unescape(desc).strip()})
    return {
        "no": no,
        "title": first(r'<meta name="DC.title" content="([^"]*)"', page),
        "url": URL.format(no=no),
        "assignees": people.get("assignee", []),
        "inventors": people.get("inventor", []),
        "priority": first(r'itemprop="priorityDate" datetime="([^"]*)"', page),
        "filed": first(r'itemprop="filingDate" datetime="([^"]*)"', page),
        "published": first(r'itemprop="publicationDate" datetime="([^"]*)"', page),
        "status": first(r'itemprop="status">([^<]*)<', page),
        "cpc": cpc,
        "claim1": claim1(page),
    }


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    OUT.mkdir(parents=True, exist_ok=True)
    for no in argv:
        no = no.strip().upper()
        try:
            rec = parse(no, fetch(no))
        except Exception as exc:
            print(f"{no}: ERROR {exc}", file=sys.stderr)
            continue
        (OUT / f"{no}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{no} | {rec['status']} | prio {rec['priority']} | {rec['assignees']} | {rec['title'][:70]}")
        print(f"   claim1: {rec['claim1'][:240]}")
        time.sleep(2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
