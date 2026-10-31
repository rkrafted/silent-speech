#!/usr/bin/env python3
"""Keyword-score the OpenBCI forum dump and queue the local-model extraction.

Reads data/raw/openbci-forum/threads.jsonl ({"id","slug","title","url","posts"}).
Scores title + post text against the topics that matter for the hidden-jaw EMG
wearable, keeps at most the top N threads, and writes:

  research/jaw/forum-selection.tsv   rank, id, score, title, url for the kept threads
  local_batch/forum-prompts.jsonl    one {"id","prompt"} per kept thread

The prompts are the input to local_batch/forum.yaml, which the runner serves to
the local 27B after the session (research/jaw/forum-extracts.jsonl). Stdlib only.

Selection rule: every thread that mentions a rare, directly on-topic part
(PiEEG, Cerelog, HackEEG, cEEGrid, MyoWare, ADS1299, silent/subvocal speech) is
kept first; the remaining slots go to the highest keyword scores, so a long
generic EEG thread cannot crowd out a short one naming our exact hardware.

Redaction: post text can quote usernames (@handle), e-mail addresses and home
directories. All three are replaced before the prompt is written, so no personal
data or absolute /home path enters the repo.

usage: python3 scripts/forum_prefilter.py [--input PATH] [--top 300] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
from pathlib import Path

DEFAULT_INPUT = "data/raw/openbci-forum/threads.jsonl"
SELECTION = "research/jaw/forum-selection.tsv"
PROMPTS = "local_batch/forum-prompts.jsonl"

# A hit in a group scores w * (1 + min(hits,4)/4): presence matters more than a
# keyword repeated in a long thread, so a rare part name lifts a short thread.
GROUPS: dict[str, tuple[float, list[str]]] = {
    "silent_speech": (20, [
        r"\bsilent speech\b", r"\bsubvocal\w*", r"\bsub-vocal\w*", r"\binner speech\b",
        r"\bimagined speech\b", r"\bsilent\b",
    ]),
    "ads1299_parts": (18, [
        r"\bads1299\b", r"\bads1298\b", r"\bads129\w*", r"\bads131\w*", r"\bpieeg\b",
        r"\bcerelog\b", r"\bhackeeg\b",
    ]),
    "emg": (14, [
        r"\bemg\b", r"\belectromyograph\w*", r"\bsemg\b", r"\bsurface emg\b",
        r"\bmuscle\b", r"\bmasseter\b", r"\bdigastric\b", r"\bmylohyoid\b",
        r"\bmentalis\b", r"\bplatysma\b", r"\bbuccinator\b",
    ]),
    "face_jaw_neck": (14, [
        r"\bjaw\b", r"\bchin\b", r"\bsubmental\b", r"\bmandib\w*", r"\bcheek\b",
        r"\bfacial\b", r"\bface\b", r"\bthroat\b", r"\blaryn\w*", r"\btongue\b",
        r"\blips?\b", r"\bmouth\b",
    ]),
    "ear_ceegrid": (12, [
        r"\bceegrid\b", r"\bear-?eeg\b", r"\bin-?ear\b", r"\bearbud\w*",
        r"\bearphone\w*", r"\bheadphone\w*", r"\bmastoid\b", r"\bretroauricular\b",
        r"\bhearable\b", r"\bmyoware\b", r"\bear\b",
    ]),
    "openbci_boards": (8, [
        r"\bcyton\b", r"\bdaisy\b", r"\bganglion\b", r"\bopenbci\b", r"\bultracortex\b",
    ]),
    "mcu_wireless": (8, [
        r"\besp32\b", r"\bnrf52\w*\b", r"\bbluetooth\b", r"\bble\b", r"\bwifi\b",
        r"\bxbee\b", r"\bwixel\b", r"\brfduino\b", r"\barduino\b", r"\braspberry pi\b",
        r"\brpi\b", r"\bthroughput\b", r"\bbandwidth\b",
    ]),
    "bias_srb_reference": (9, [
        r"\bsrb2?\b", r"\bsrb\b", r"\bbias\b", r"\breference\b", r"\bdrl\b",
        r"\bcommon mode\b", r"\bcmrr\b",
    ]),
    "noise_mains": (8, [
        r"\bnoise\b", r"\bmains\b", r"\bhum\b", r"\b50 ?hz\b", r"\b60 ?hz\b",
        r"\bnotch\b", r"\bfilter\w*\b", r"\bartifact\w*\b", r"\binterference\b",
        r"\bemf\b", r"\bshield\w*\b", r"\bground loop\b",
    ]),
    "electrodes": (7, [
        r"\bdry\b", r"\bgel\b", r"\bag/agcl\b", r"\bgold\b", r"\bten20\b",
        r"\bconductive paste\b", r"\belectrode\w*", r"\bimpedance\b", r"\bskin prep\b",
        r"\be-tattoo\b", r"\btextile\b",
    ]),
    "sample_wireless_rate": (8, [
        r"\bsample rate\b", r"\bsampling rate\b", r"\bsps\b", r"\bksps\b", r"\bhz\b",
        r"\b125 ?hz\b", r"\b250 ?hz\b", r"\b1 ?khz\b", r"\b16 ?ksps\b",
        r"\bdownsampl\w*", r"\bdata rate\b", r"\blatency\b", r"\bdropout\b",
        r"\bpacket loss\b", r"\bmissing packet\w*",
    ]),
    "sync_markers": (6, [
        r"\blsl\b", r"\blab streaming\w*", r"\bmarker\w*", r"\bsync\w*",
        r"\btimestamp\w*", r"\btrigger\w*", r"\bevent\b", r"\baudio\b", r"\bstream\w*",
    ]),
    "battery_safety": (5, [
        r"\bbatter\w*", r"\blithium\b", r"\blipo\b", r"\bsafety\b", r"\bisolation\w*",
        r"\bmedical\b", r"\biec\b", r"\b60601\b", r"\bcharging\b",
    ]),
    "wearable_glasses": (5, [
        r"\bwearable\w*", r"\bglasses\b", r"\bheadset\b", r"\bheadband\b",
        r"\bhelmet\b", r"\bneckband\b", r"\bconceal\w*", r"\bdiscreet\b",
    ]),
}
COMP = {g: [re.compile(p, re.I) for p in pats] for g, (_, pats) in GROUPS.items()}

# Kept unconditionally (within --top): the exact parts and the exact application.
RARE = [re.compile(p, re.I) for p in [
    r"\bsubvocal\w*", r"\bsub-vocal\w*", r"\bsilent speech\b", r"\binner speech\b",
    r"\bimagined speech\b", r"\bsilent\b", r"\bpieeg\b", r"\bcerelog\b",
    r"\bhackeeg\b", r"\bceegrid\b", r"\bmyoware\b", r"\bmasseter\b",
    r"\bdigastric\b", r"\bmylohyoid\b", r"\bsubmental\b", r"\bads1299\b",
    r"\bads1298\b", r"\bads131\w*",
]]

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
HANDLE_RE = re.compile(r"@[A-Za-z0-9_]+(?:[.-][A-Za-z0-9_]+)*")
PATH_RE = re.compile(r"(?:/(?:home|Users)/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)")
BODY_CHARS = 16000          # ~4-5k tokens, fits num_ctx 8192 with the answer
MAX_POSTS = 40

INSTRUCTIONS = """You are reading one thread from the OpenBCI community forum. Extract only what helps build a hidden jaw/face surface-EMG silent-speech wearable: ADS1299-class front end, dry electrodes, ESP32/nRF BLE streaming, mains-noise and bias/reference problems, sample rate, LSL sync, battery and wearability. Ignore pure-EEG, sales and social content.

Return ONLY a JSON object with exactly these keys:
{"id": <thread id as a number>, "relevant": 0, "topic": "", "problem": "", "fix_or_answer": "", "numbers": "", "parts": "", "applies_to_us": ""}

Rules:
- relevant: 3 = directly useful (EMG on face/jaw/neck, silent speech, ADS1299 board, bias/SRB/reference wiring, mains hum, dry vs gel, ear/cEEGrid, sample rate or wireless throughput, LSL sync, battery/safety, wearable); 2 = partly useful (EEG or general biosignal hardware that transfers); 1 = background only; 0 = not useful.
- topic: the thread subject, <= 12 words.
- problem: the concrete problem or question, <= 60 words; "" if none.
- fix_or_answer: the concrete answer or fix, <= 80 words; "" if none.
- numbers: every concrete number useful to us with what it measures (sample rate/Hz, noise in uV or uVrms, impedance in kOhm, battery hours or mAh, latency ms, price with currency, channel count, electrode size). "" if none.
- parts: exact boards, parts or software named (e.g. ADS1299, Cyton, PiEEG, ESP32, LSL). "" if none.
- applies_to_us: one sentence on what we should change, buy, avoid or test because of this thread; "" if nothing.

JSON only. No markdown, no commentary."""


def score(title: str, posts: list[str]) -> float:
    body = title + " \n " + " ".join(posts)
    low_title = title.lower()
    total = 0.0
    groups_hit = 0
    for group, (weight, _) in GROUPS.items():
        n = sum(len(rx.findall(body)) for rx in COMP[group])
        if n:
            groups_hit += 1
            total += weight * (1 + min(n, 4) / 4)
        title_hits = sum(1 for rx in COMP[group] if rx.search(low_title))
        total += weight * 0.5 * min(title_hits, 2)
    return total + 2.0 * groups_hit


def is_rare(text: str) -> bool:
    return any(rx.search(text) for rx in RARE)


def clean(text: str) -> str:
    """Collapse whitespace and drop usernames, e-mails and home-dir paths from quoted post text."""
    text = EMAIL_RE.sub("[email]", text)
    text = PATH_RE.sub("[path]", text)
    text = HANDLE_RE.sub("@user", text)
    return re.sub(r"[ \t]+", " ", text).replace("\t", " ").strip()


def build_prompt(tid: int, title: str, posts: list[str]) -> str:
    body = "\n\n---\n\n".join(clean(p) for p in posts[:MAX_POSTS] if p.strip())
    if len(body) > BODY_CHARS:
        body = body[:BODY_CHARS] + "\n\n[...thread truncated...]"
    if not body:
        body = "(no post text captured)"
    return (f"{INSTRUCTIONS}\n\nThread id: {tid}\nTitle: {clean(title)}\n\nPosts:\n{body}\n\n"
            "Remember: JSON only, keys id, relevant, topic, problem, fix_or_answer, "
            "numbers, parts, applies_to_us.")


def tsv_cell(text: str) -> str:
    return re.sub(r"[\t\r\n]+", " ", text).strip()


def select(threads: list[dict], top: int) -> list[tuple[float, dict]]:
    scored = [(score(t["title"], t.get("posts") or []), t) for t in threads]
    scored.sort(key=lambda x: (-x[0], x[1]["id"]))
    rare = [row for row in scored if is_rare(row[1]["title"] + " " + " ".join(row[1].get("posts") or []))]
    kept = rare[:top]
    if len(kept) < top:
        chosen = {row[1]["id"] for row in kept}
        kept += [row for row in scored if row[1]["id"] not in chosen][: top - len(kept)]
    kept.sort(key=lambda x: (-x[0], x[1]["id"]))
    return kept[:top]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=DEFAULT_INPUT)
    ap.add_argument("--top", type=int, default=300)
    ap.add_argument("--selection", default=SELECTION)
    ap.add_argument("--prompts", default=PROMPTS)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    threads = [json.loads(line) for line in Path(args.input).read_text(encoding="utf-8").splitlines() if line.strip()]
    kept = select(threads, args.top)

    sel_lines = ["rank\tid\tscore\ttitle\turl"]
    prompt_lines = []
    redactions = 0
    for rank, (s, t) in enumerate(kept, 1):
        sel_lines.append(
            f"{rank}\t{t['id']}\t{s:.1f}\t{tsv_cell(t['title'])}\t{tsv_cell(t.get('url', ''))}"
        )
        raw = " ".join(t.get("posts") or [])
        redactions += (len(EMAIL_RE.findall(raw)) + len(HANDLE_RE.findall(raw))
                       + len(PATH_RE.findall(raw)))
        prompt_lines.append(json.dumps(
            {"id": t["id"], "prompt": build_prompt(t["id"], t["title"], t.get("posts") or [])},
            ensure_ascii=False,
        ))

    scores = [s for s, _ in kept]
    print(f"threads: {len(threads)}  kept: {len(kept)}  cutoff: {scores[-1]:.1f}  "
          f"max: {scores[0]:.1f}  rare kept: {sum(1 for _, t in kept if is_rare(t['title'] + ' ' + ' '.join(t.get('posts') or [])))}")
    print(f"redacted {redactions} e-mail/@handle strings from the kept post text")

    if args.dry_run:
        print("dry run: nothing written")
        return 0
    out_sel, out_prompts = Path(args.selection), Path(args.prompts)
    out_sel.parent.mkdir(parents=True, exist_ok=True)
    out_prompts.parent.mkdir(parents=True, exist_ok=True)
    out_sel.write_text("\n".join(sel_lines) + "\n", encoding="utf-8")
    out_prompts.write_text("\n".join(prompt_lines) + "\n", encoding="utf-8")
    print(f"wrote {out_sel} ({len(kept)} rows) and {out_prompts} "
          f"({out_prompts.stat().st_size / 1024:.0f} KiB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
