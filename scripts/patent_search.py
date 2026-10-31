#!/usr/bin/env python3
"""Google Patents search helper for the silent-speech patent sweep.

No API key. Uses the public xhr/query endpoint that patents.google.com itself
calls. Prints one candidate per line; nothing is stored.

usage: python3 scripts/patent_search.py "query one" "query two" ...
"""
from __future__ import annotations

import json
import sys
import time
import urllib.parse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) research/1.0"}


def query(q: str, num: int = 25, page: int = 0) -> dict:
    inner = urllib.parse.urlencode({"q": q, "num": num, "page": page})
    url = "https://patents.google.com/xhr/query?url=" + urllib.parse.quote(inner, safe="")
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.loads(r.read().decode())


def rows(d: dict) -> list[dict]:
    out = []
    for c in (d.get("results", {}) or {}).get("cluster", []) or []:
        for r in c.get("result", []) or []:
            p = r.get("patent", {})
            out.append({
                "no": p.get("publication_number"),
                "title": (p.get("title") or "").strip(),
                "assignee": p.get("assignee"),
                "prio": p.get("priority_date"),
                "pub": p.get("publication_date"),
            })
    return out


def main(argv: list[str]) -> int:
    seen: dict[str, dict] = {}
    for q in argv:
        try:
            rs = rows(query(q))
        except Exception as e:  # noqa: BLE001 - best effort research tool
            print(f"ERR {q}: {e}")
            continue
        print(f"### {q}: {len(rs)}")
        for r in rs:
            if r["no"] in seen:
                continue
            seen[r["no"]] = r
            print(f"  {str(r['no']):18} {str(r['prio']):10} "
                  f"{(r['assignee'] or '?')[:30]:30} {r['title'][:74]}")
        time.sleep(1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
