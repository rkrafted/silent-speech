#!/usr/bin/env python3
"""Fetch structured patent data from Lens.org public pages (no key, no account).

Fallback / cross-check for Google Patents. Google throttles hard, Lens serves the
whole page as JSON.

usage: python3 scripts/fetch_lens.py US10621973B1 CN113288183B ...
"""
from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) research/1.0"}
RAW = Path(__file__).resolve().parent.parent / "research" / "jaw" / "raw"


def lens_id(no: str) -> str:
    m = re.match(r"^([A-Z]{2})(\d+)([A-Z]\d?)$", no.upper())
    if not m:
        raise ValueError(f"cannot parse publication number {no!r}")
    cc, num, kind = m.groups()
    return f"{cc}_{num}_{kind}"


def get(url: str, tries: int = 3) -> str:
    last = ""
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
        except Exception as e:  # noqa: BLE001
            last = repr(e)
        time.sleep(3 + 3 * i)
    raise RuntimeError(last)


def clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def en_text(d: dict | None) -> str:
    """Lens keys title/abstract/claim by language; prefer English, else any."""
    if not isinstance(d, dict):
        return ""
    for lang in ("en", "de", "fr", "zh", "ja", "ko"):
        v = d.get(lang)
        if isinstance(v, list) and v:
            return clean(v[0].get("text", ""))
    for v in d.values():                      # any language at all
        if isinstance(v, list) and v and isinstance(v[0], dict):
            return clean(v[0].get("text", ""))
    return ""


def family_members(fam: dict) -> list[str]:
    out = []
    for key in ("simple", "extended"):
        for m in (fam.get(key) or {}).get("member", []) or []:
            did = m.get("document_id", {})
            out.append(f"{did.get('jurisdiction','')}{did.get('doc_number','')}{did.get('kind','')}")
    return out


def extract(no: str, d: dict) -> dict:
    fpm = d["frontPageModel"]
    doc = fpm["patentViewModel"]["document"]
    claims_obj = doc.get("claim") or fpm.get("claims") or {}
    lines: list[str] = []
    for c in (fpm.get("claims") or {}).get("claims", []) or []:
        lines.extend(c.get("lines", []))
    claim_text = en_text(claims_obj) or clean(" ".join(lines))
    ls = doc.get("legal_status") or {}
    return {
        "no": no, "lens_id": lens_id(no),
        "title": en_text(doc.get("title")),
        "abstract": en_text(doc.get("abstract")),
        "claims": claim_text[:20000],
        "description": en_text(doc.get("description"))[:60000],
        "applicants": [a.get("name") for a in doc.get("applicant", []) or []],
        "inventors": [a.get("name") for a in doc.get("inventor", []) or []],
        "priority": doc.get("earliest_priority_claim_date", ""),
        "filed": (doc.get("application_reference") or {}).get("date", ""),
        "published": doc.get("date_published", ""),
        "grant_date": ls.get("grant_date", ""),
        "status": ls.get("patent_status", ""),
        "term": ls.get("anticipated_term_date", ""),
        "cpc": [c.get("symbol") for c in doc.get("class_cpc", []) or []][:8],
        "family": sorted(set(family_members(doc.get("family") or {}))),
        "url": f"https://www.lens.org/lens/patent/{lens_id(no)}",
    }


def main(argv: list[str]) -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    for no in argv:
        out = RAW / f"lens_{no}.json"
        if out.exists() and out.stat().st_size > 500:
            print(f"cached {no}")
            continue
        lid = lens_id(no)
        try:
            b = get(f"https://www.lens.org/lens/patent/{lid}")
            d = json.loads(b)
            rec = extract(no, d)
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {no} ({lid}): {e}")
            time.sleep(1.0)
            continue
        out.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
        print(f"ok {no} status={rec['status']!r} prio={rec['priority']} "
              f"claims={len(rec['claims'])} inv={rec['inventors'][:2]} {rec['title'][:55]}")
        time.sleep(1.2)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
