"""Rank fetched repos for the silent-speech pod with a local 9B (Ollama). Quotes are checked in code:
a repo whose quote is not in its README is marked unverified and capped at relevance 1."""
import json, re, sys, concurrent.futures as cf, urllib.request
from pathlib import Path

RAW = Path("research/jaw/raw/repos")
MODEL = "hf.co/empero-ai/Qwen3.8-9B-Distill-GGUF:Q4_K_M"
CONTEXT = """Our project: a hidden jaw-worn silent-speech wearable (AlterEgo-style). Pod = ADS1298 (8-ch biopotential ADC,
SPI) + u-blox NINA-B306 (nRF52840) BLE to a phone, 16 MB QSPI flash, LiPo. Firmware streams 8-ch sEMG at 250-1000 SPS.
Phone app decodes silent words/phonemes with ML trained on the user's own EMG. Useful repos: ADS129x drivers/emulators/
firmware (esp. nRF52/Zephyr), BLE biosignal streaming, EMG/sEMG speech or silent-speech decoding code, datasets, models,
open biopotential hardware (KiCad), signal processing for EMG. Not useful: unrelated EEG games, generic ML tutorials."""
PROMPT = """{ctx}

Repo: {name}  (stars {stars}, last push {pushed}, license {lic}, lang {lang})
Description: {desc}
README (truncated):
<<<
{readme}
>>>

Answer JSON only: {{"relevance": 0-3 (3 = directly reusable in our pod/firmware/decoder, 2 = useful reference,
1 = loosely related, 0 = not related), "category": one of ["ads129x-driver","firmware-ble","emg-speech-decoding",
"dataset","hardware","signal-processing","eeg-tooling","other"], "use_for": "one sentence: what we would take from it",
"quote": "an exact short phrase (5-15 words) copied from the README that proves the category"}}"""

def norm(s): return re.sub(r"\s+", " ", (s or "").lower()).strip()

def ask(r):
    f = RAW / "readme" / (r["full_name"].replace("/", "__") + ".md")
    readme = f.read_text(errors="ignore") if f.exists() else ""
    p = PROMPT.format(ctx=CONTEXT, name=r["full_name"], stars=r.get("stargazers_count"), pushed=(r.get("pushed_at") or "")[:10],
                      lic=r.get("license"), lang=r.get("language"), desc=r.get("description") or "", readme=readme[:6000])
    body = json.dumps({"model": MODEL, "prompt": p, "stream": False, "format": "json",
                       "options": {"temperature": 0.1, "num_ctx": 8192}}).encode()
    req = urllib.request.Request("http://127.0.0.1:11434/api/generate", body, {"Content-Type": "application/json"})
    try:
        out = json.loads(json.loads(urllib.request.urlopen(req, timeout=600).read())["response"])
    except Exception as e:
        return {**r, "relevance": 0, "category": "error", "use_for": repr(e)[:120], "quote": "", "verified": False}
    q = norm(out.get("quote"))
    ok = bool(q) and len(q) >= 12 and q in norm(readme + " " + (r.get("description") or ""))
    rel = int(out.get("relevance") or 0) if str(out.get("relevance", "0")).isdigit() else 0
    return {**r, "relevance": rel if ok else min(rel, 1), "model_relevance": rel, "category": out.get("category"),
            "use_for": out.get("use_for"), "quote": out.get("quote"), "verified": ok, "model": MODEL}

repos = list(json.load(open(RAW / "repos.json")).values())
repos = [r for r in repos if r.get("full_name") and not r.get("archived")]
res = []
with cf.ThreadPoolExecutor(3) as ex:
    for i, x in enumerate(ex.map(ask, repos)):
        res.append(x)
        if i % 20 == 0: print(f"{i}/{len(repos)}", flush=True)
with open(RAW / "ranked.jsonl", "w") as f:
    for x in res: f.write(json.dumps(x) + "\n")

res.sort(key=lambda x: (-x["relevance"], -(x.get("stargazers_count") or 0)))
lines = ["# GitHub repo scan for the silent-speech pod", "",
         f"Fetched by tools/reposcan/fetch.py (podman), ranked by {MODEL} via tools/reposcan/rank.py.",
         "Relevance 0-3 by the local model; quotes checked in code (unverified -> capped at 1).", "",
         "| rel | repo | stars | pushed | license | category | use for |", "|---|---|---|---|---|---|---|"]
for x in res:
    if x["relevance"] < 2: continue
    lines.append(f"| {x['relevance']} | [{x['full_name']}]({x.get('html_url')}) | {x.get('stargazers_count')} | "
                 f"{(x.get('pushed_at') or '')[:10]} | {x.get('license')} | {x.get('category')} | "
                 f"{(x.get('use_for') or '').replace('|', '/')} |")
Path("research/jaw/repos-scan.md").write_text("\n".join(lines) + "\n")
print("ranked", len(res), "kept", sum(1 for x in res if x["relevance"] >= 2))
