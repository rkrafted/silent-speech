#!/usr/bin/env python3
"""Fetch a Lens.org patent record (public page) as JSON and extract what we need.

Lens serves the front-page model as embedded JSON in the public HTML page, so no
account or API key is involved. Works for US/EP/CN/JP/KR grants and for documents
addressed by Lens ID (WO and US pre-grant publications included).

usage:
  python3 scripts/lens_fetch.py US12482449B2 EP3688897A1 045-073-728-605-863
Writes full JSON to research/jaw/raw/lens/<file>.json and appends a compact
record to research/jaw/raw/lens/_compact.jsonl.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "research" / "jaw" / "raw" / "lens"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"


def norm_id(s: str) -> str:
    if re.fullmatch(r"[0-9]{3}-[0-9]{3}-[0-9]{3}-[0-9]{3}-[0-9]{3}", s):
        return s
    m = re.fullmatch(r"([A-Z]{2})[ _]?([0-9]+)[ _]?([A-Z][0-9]?)", s.strip().upper())
    if not m:
        raise SystemExit(f"cannot parse id {s!r}")
    return f"{m.group(1)}_{m.group(2)}_{m.group(3)}"


def get(url: str, tries: int = 3) -> str:
    last = ""
    for i in range(tries):
        p = subprocess.run(["curl", "-sS", "-L", "--max-time", "45", "-A", UA,
                            "-w", "\n__HTTP__%{http_code}", url], capture_output=True, text=True)
        body, _, code = p.stdout.rpartition("__HTTP__")
        if code.strip() == "200":
            return body.rstrip("\n")
        last = f"HTTP {code.strip()}"
        time.sleep(5 + 5 * i)
    raise RuntimeError(last)


def txt(node) -> str:
    if not node:
        return ""
    if isinstance(node, str):
        return node
    if isinstance(node, dict):
        for v in node.values():
            return txt(v)
    if isinstance(node, list):
        return " ".join(txt(x) for x in node)
    return str(node)


def extract(pid: str, d: dict) -> dict:
    vm = d["frontPageModel"]["patentViewModel"]
    doc = vm["document"]
    claims = []
    for c in (d.get("frontPageModel", {}).get("claims", {}) or {}).get("claims", []) or []:
        body = " ".join(c.get("lines") or [])
        body = re.sub(r"<[^>]+>", " ", body)
        body = re.sub(r"&[a-z]+;", " ", body)
        claims.append({"number": c.get("number"), "text": re.sub(r"\s+", " ", body).strip()})
    fam = []
    for m in (doc.get("family", {}) or {}).get("extended", {}).get("member", []) or []:
        di = m.get("document_id", {})
        fam.append({"jurisdiction": di.get("jurisdiction"), "doc_number": di.get("doc_number"),
                    "kind": di.get("kind"), "date": di.get("date"), "lens_id": m.get("lens_id")})
    cpcs = []
    cc = doc.get("class_cpc") or {}

    def add_cpc(v):
        if isinstance(v, str):
            cpcs.append(v)
        elif isinstance(v, dict):
            s = v.get("symbol") or v.get("value")
            if isinstance(s, str):
                cpcs.append(s)
        elif isinstance(v, list):
            for x in v:
                add_cpc(x)

    if isinstance(cc, dict):
        for k in ("first_symbol", "inv_symbol", "later_symbol", "add_symbol"):
            add_cpc(cc.get(k))
    else:
        add_cpc(cc)
    return {
        "lens_id": pid,
        "no": doc.get("doc_key", ""),
        "jurisdiction": doc.get("jurisdiction"),
        "kind": doc.get("kind"),
        "title": txt(doc.get("title")),
        "applicants": [a.get("name") for a in doc.get("applicant", []) or []],
        "owners": [a.get("name") for a in doc.get("owner", []) or []],
        "inventors": [a.get("name") for a in doc.get("inventor", []) or []],
        "priority": doc.get("earliest_priority_claim_date"),
        "published": doc.get("date_published"),
        "legal_status": doc.get("legal_status", {}),
        "cpc": sorted({c for c in cpcs if c}),
        "family": fam,
        "claims": claims,
        "url": f"https://www.lens.org/lens/patent/{pid}",
    }


def main(argv: list[str]) -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    comp = RAW / "_compact.jsonl"
    for raw_id in argv:
        pid = norm_id(raw_id)
        out = RAW / f"{pid}.json"
        if out.exists() and out.stat().st_size > 2000:
            d = json.loads(out.read_text())
            print(f"cached {pid}")
        else:
            try:
                body = get(f"https://www.lens.org/lens/patent/{pid}")
                d = json.loads(body)
            except Exception as e:  # noqa: BLE001
                print(f"FAIL {pid}: {e}")
                continue
            out.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            time.sleep(2)
        r = extract(pid, d)
        with comp.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        ls = r["legal_status"]
        print(f"ok {pid} {r['no']} status={ls.get('patent_status')} "
              f"prio={r['priority']} exp={ls.get('anticipated_term_date')} "
              f"claims={len(r['claims'])} fam={len(r['family'])} "
              f"{r['title'][:55]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
