#!/usr/bin/env python3
"""Fetch a Google Patents page and extract the fields the patent table needs.

Caches raw HTML + extracted JSON under research/jaw/raw/ (gitignored: downloaded
data must not be committed).

usage: python3 scripts/fetch_patent.py US10621973B1 CN113288183B ...
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
        time.sleep(2 + 2 * i)
    raise RuntimeError(last)


def strip_tags(s: str) -> str:
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def meta(b: str, name: str) -> str:
    m = re.search(rf'<meta name="{re.escape(name)}" content="([^"]*)"', b)
    return html.unescape(m.group(1)).strip() if m else ""


def item(b: str, prop: str, what: str = "inner") -> str:
    m = re.search(rf'itemprop="{re.escape(prop)}"[^>]*>(.*?)</', b, re.S)
    if not m:
        return ""
    return strip_tags(m.group(1)) if what == "inner" else html.unescape(m.group(1)).strip()


def items_all(b: str, prop: str) -> list[str]:
    return [strip_tags(x) for x in re.findall(rf'itemprop="{re.escape(prop)}"[^>]*>(.*?)</', b, re.S)]


def section(b: str, prop: str) -> str:
    m = re.search(rf'<section[^>]*itemprop="{re.escape(prop)}"[^>]*>(.*?)</section>', b, re.S)
    return strip_tags(m.group(1)) if m else ""


def extract(no: str, b: str) -> dict:
    title = meta(b, "DC.title") or item(b, "title")
    abstract = meta(b, "description")
    desc = section(b, "description")
    if not desc:
        m = re.search(r'itemprop="description"[^>]*>(.*?)</section>', b, re.S)
        desc = strip_tags(m.group(1)) if m else ""
    claims = section(b, "claims")
    prio = re.search(r'itemprop="priorityDate"[^>]*datetime="([^"]*)"', b)
    filed = re.search(r'itemprop="filingDate"[^>]*datetime="([^"]*)"', b)
    pubd = re.search(r'itemprop="publicationDate"[^>]*datetime="([^"]*)"', b)
    status = item(b, "status")
    exp = re.search(r'itemprop="expiration"[^>]*datetime="([^"]*)"', b)
    # family / also-published
    fam = []
    for m in re.finditer(r'itemprop="knownRelated"[^>]*>(.*?)</', b, re.S):
        fam.append(strip_tags(m.group(1)))
    m = re.search(r'Also published as(.*?)(?:<h2|</dl>)', b, re.S)
    also = strip_tags(m.group(1)) if m else ""
    m = re.search(r'worldwide applications(.*?)(?:</table>|</section>)', b, re.S)
    worldwide = strip_tags(m.group(1)) if m else ""
    m = re.search(r'itemprop="events"(.*?)</table>', b, re.S)
    events = strip_tags(m.group(1)) if m else ""
    return {
        "no": no, "title": title, "abstract": abstract,
        "assignee": item(b, "assigneeOriginal") or item(b, "assigneeCurrent"),
        "inventors": items_all(b, "inventor"),
        "priority": prio.group(1) if prio else "",
        "filed": filed.group(1) if filed else "",
        "publication": pubd.group(1) if pubd else "",
        "status": status, "expiration": exp.group(1) if exp else "",
        "also_published": also[:1200], "worldwide": worldwide[:1500],
        "claims": claims[:8000], "description": desc[:60000],
        "url": f"https://patents.google.com/patent/{no}/en",
    }


def main(argv: list[str]) -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    failed = 0
    for no in argv:
        out = RAW / f"{no}.json"
        if out.exists() and out.stat().st_size > 500:
            print(f"cached {no}")
            continue
        try:
            b = get(f"https://patents.google.com/patent/{no}/en")
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {no}: {e}")
            failed += 1
            continue
        (RAW / f"{no}.html").write_text(b, encoding="utf-8")
        d = extract(no, b)
        out.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        print(f"ok {no} status={d['status']!r} prio={d['priority']} "
              f"claims={len(d['claims'])} inv={len(d['inventors'])} {d['title'][:60]}")
        time.sleep(1.5)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
