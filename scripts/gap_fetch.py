#!/usr/bin/env python3
"""Polite Google Patents fetcher for the gaps sweep (search + full record).

Caches raw JSON/HTML under research/jaw/raw/ (gitignored). Retries on 429/503
with exponential backoff so a burst throttle does not lose the run.

usage:
  python3 scripts/gap_fetch.py search 'q=CPC%3D%3DG10L15%2F24&after=priority:20190101'
  python3 scripts/gap_fetch.py fetch US10878818B2 EP3688897A1
"""
from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "research" / "jaw" / "raw"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) research/1.0"}


def get(url: str, tries: int = 5) -> str:
    """curl, not urllib: Google answers urllib's TLS/HTTP1.1 fingerprint with 503."""
    import subprocess

    last = ""
    for i in range(tries):
        p = subprocess.run(
            ["curl", "-sS", "-L", "--max-time", "40", "-A", UA["User-Agent"],
             "-H", "Accept: text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
             "-H", "Accept-Language: en-US,en;q=0.9", "-w", "\n__HTTP__%{http_code}", url],
            capture_output=True, text=True)
        body = p.stdout
        code = body.rsplit("__HTTP__", 1)[-1].strip() if "__HTTP__" in body else "0"
        body = body.rsplit("\n__HTTP__", 1)[0]
        if code == "200" and "Sorry..." not in body[:600]:
            return body
        last = f"HTTP {code}"
        time.sleep(6 + 8 * i)
    raise RuntimeError(last)


def strip_tags(s: str) -> str:
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def meta(b: str, name: str) -> str:
    m = re.search(rf'<meta name="{re.escape(name)}" content="([^"]*)"', b)
    return html.unescape(m.group(1)).strip() if m else ""


def item(b: str, prop: str) -> str:
    m = re.search(rf'itemprop="{re.escape(prop)}"[^>]*>(.*?)</', b, re.S)
    return strip_tags(m.group(1)) if m else ""


def items_all(b: str, prop: str) -> list[str]:
    return [strip_tags(x) for x in re.findall(rf'itemprop="{re.escape(prop)}"[^>]*>(.*?)</', b, re.S)]


def section(b: str, prop: str) -> str:
    m = re.search(rf'<section[^>]*itemprop="{re.escape(prop)}"[^>]*>(.*?)</section>', b, re.S)
    return strip_tags(m.group(1)) if m else ""


def extract(no: str, b: str) -> dict:
    prio = re.search(r'itemprop="priorityDate"[^>]*datetime="([^"]*)"', b)
    filed = re.search(r'itemprop="filingDate"[^>]*datetime="([^"]*)"', b)
    pubd = re.search(r'itemprop="publicationDate"[^>]*datetime="([^"]*)"', b)
    exp = re.search(r'itemprop="expiration"[^>]*datetime="([^"]*)"', b)
    i = b.find("Also Published As")
    also = strip_tags(b[i:i + 4000]) if i > 0 else ""
    also = also.replace("Also Published As", "").replace("Similar Documents", "|SIM|").split("|SIM|")[0]
    j = b.find("Current Assignee")
    ca = strip_tags(b[j:j + 700]) if j > 0 else ""
    return {
        "no": no, "title": meta(b, "DC.title") or item(b, "title"),
        "abstract": meta(b, "description"),
        "assignee": item(b, "assigneeOriginal") or item(b, "assigneeCurrent"),
        "current_assignee": ca,
        "inventors": items_all(b, "inventor"),
        "priority": prio.group(1) if prio else "",
        "filed": filed.group(1) if filed else "",
        "publication": pubd.group(1) if pubd else "",
        "status": item(b, "status"), "expiration": exp.group(1) if exp else "",
        "also_published": re.sub(r"\s+", " ", also)[:800],
        "claims": section(b, "claims")[:9000],
        "description": section(b, "description")[:60000],
        "url": f"https://patents.google.com/patent/{no}/en",
    }


def cmd_search(spec: str) -> int:
    out = RAW / "search"
    out.mkdir(parents=True, exist_ok=True)
    key = re.sub(r"[^A-Za-z0-9]+", "_", spec)[:120]
    cache = out / f"{key}.json"
    if cache.exists() and cache.stat().st_size > 100:
        d = json.loads(cache.read_text())
        print(f"cached {cache.name}")
    else:
        url = "https://patents.google.com/xhr/query?url=" + spec
        d = json.loads(get(url))
        cache.write_text(json.dumps(d), encoding="utf-8")
        time.sleep(4)
    rs = [r["patent"] for c in (d.get("results", {}) or {}).get("cluster", []) or []
          for r in c.get("result", []) or []]
    print(f"### {urllib.parse.unquote(spec)} total={d.get('results',{}).get('total_num_results')} shown={len(rs)}")
    for p in rs:
        print(f"  {str(p.get('publication_number')):16} {str(p.get('priority_date')):10} "
              f"{(p.get('assignee') or '?')[:30]:30} {(p.get('title') or '')[:78]}")
    return 0


def cmd_fetch(nos: list[str]) -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    for no in nos:
        out = RAW / f"{no}.json"
        if out.exists() and out.stat().st_size > 500:
            print(f"cached {no}")
            continue
        try:
            b = get(f"https://patents.google.com/patent/{no}/en")
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {no}: {e}")
            continue
        (RAW / f"{no}.html").write_text(b, encoding="utf-8")
        d = extract(no, b)
        out.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        print(f"ok {no} status={d['status']!r} prio={d['priority']} claims={len(d['claims'])} "
              f"inv={len(d['inventors'])} assignee={d['assignee'][:30]!r} {d['title'][:50]}")
        time.sleep(3)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "search":
        sys.exit(cmd_search(sys.argv[2]))
    sys.exit(cmd_fetch(sys.argv[2:]))
