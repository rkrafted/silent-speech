# ss-research-pubmed — jaw, chin, ear and neck sensor sites for silent speech

A PubMed literature sweep for a personal silent-speech wearable. It answers one question with
numbers: **which electrode sites decode silently articulated speech, which channel subsets were
actually tested, and which of those sites can be hidden** (under the jaw line, submental, behind
the ear, in the ear, or on the neck under a collar).

This is a research repository, not a program. There is nothing to compile or install.

## What is in here

| File | What it is |
|---|---|
| `research/jaw/pubmed-queries.md` | Every PubMed E-utilities query string with its hit count (31 queries). |
| `research/jaw/site-evidence.md` | The deliverable: study-by-study site/subset/accuracy tables, the ranked HIDDEN/VISIBLE site list, the mapping onto Gaddy's 8 sites, and the plain verdict + experiment. |
| `research/jaw/sources-pubmed.jsonl` | 50 opened sources, one JSON object per line (`pmid` on every line). |
| `scripts/pubmed_sweep.py` | Re-runs the search and rewrites the query log (Python standard library only). |
| `research/01-*.md ... 12-*.md` | The older research tracks this item builds on (04, 08 and 09 are the site/ear/e-tattoo ones). |

Every source line has the same schema as `ss-research-baltic`
(`kind, title, url, pmid, people, year, what_they_did, useful_for_us`) and was verified live.

## Install

Nothing to install. The verifier and the sweep script use only the Python 3 standard library.
Network access is needed to re-run the searches or re-verify the sources.
# Silent-speech wearable — research repository (Baltic item)

This repository collects the research behind a personal silent-speech wearable: a device that
recognises words a person articulates without sound, from face and neck biosignals (originally
modelled on MIT AlterEgo). It holds:

- `BRIEF.md` — the shared brief and rules for all research tracks.
- `CALL-PREP.md` — the prep sheet for calling Baltic labs about borrowing surface-EMG hardware.
- `research/01-*.md ... research/12-*.md` — twelve completed research tracks.
- `research/jaw/baltic.md` — the Baltic deep-dive deliverable (verdict, ranked group/device table,
  concrete asks, and the exact Pekša/Mamchur patent and paper record).
- `research/jaw/sources-baltic.jsonl` — one machine-readable line per source actually opened
  (40 entries: papers, the two Turiba patents, and lab/device pages).

## Install

Nothing to install: the research output is plain Markdown and JSON Lines, and the verifier uses the
Python 3 standard library. Network access is needed only to re-verify the sources.

## Run / verify

From the repository root:

```bash
# 1. the two deliverables exist and are non-empty
test -s research/jaw/site-evidence.md && test -s research/jaw/pubmed-queries.md

# 2. at least 25 sources carry a PubMed ID
test $(grep -c '"pmid"' research/jaw/sources-pubmed.jsonl) -ge 25

# 3. every source is live, real, and new relative to the older tracks
python3 ~/theprojects/orchestrator/bin/check_sources.py research/jaw/sources-pubmed.jsonl \
    --min 40 --min-new 25 --kinds paper --known research
```

Re-run the whole search (writes `.scratch/pubmed-sweep.json`, gitignored, and rewrites
`research/jaw/pubmed-queries.md`):

```bash
python3 scripts/pubmed_sweep.py
# 1. the Baltic report exists and names the Turiba patent application
test -s research/jaw/baltic.md && grep -q 'LVP2023000098' research/jaw/baltic.md

# 2. the required BCI paper (PMID 37447849) is in the source list
grep -q '37447849' research/jaw/sources-baltic.jsonl

# 3. every source is live and not already in the older tracks
python3 ~/theprojects/orchestrator/bin/check_sources.py research/jaw/sources-baltic.jsonl \
    --min 20 --min-new 15 --kinds paper,patent --known research
```

## Example output

```console
$ python3 ~/theprojects/orchestrator/bin/check_sources.py research/jaw/sources-pubmed.jsonl \
      --min 40 --min-new 25 --kinds paper --known research
50 sources: 50 verified, 0 could not be checked, 0 wrong or made up, 50 not already in our notes.
PASS
$ echo $?
0
```

```console
$ python3 scripts/pubmed_sweep.py
[1] silent speech EMG: 40 hits, 40 pulled
...
unique PMIDs: 776
wrote .scratch/pubmed-sweep.json (776 records) and research/jaw/pubmed-queries.md
```

## Key result in one paragraph

The two best-evidenced hidden sites are the **submental / under-chin muscle complex** (mylohyoid,
anterior digastric, geniohyoid; Gaddy site 3, the channel whose removal hurts most) and the
**superior ventral neck over the larynx** (Gaddy site 4, under a collar). Behind-ear/mastoid is
the best concealed reference and host for a single non-EMG sensor (one magnetic skin behind the
ear decoded 87.3% of words), and the ear canal can detect jaw motion and speech intention but
in-ear EEG is far behind scalp for word decoding. The cheap channels to hide are the visible
cheeks and mid-jaw; the expensive loss is the front-of-chin channel (Gaddy site 2). Expect a
hidden-only closed-command set to cost roughly 3–6 WER points and an open-vocabulary set 8–15
points versus the full face montage; the paired 16-channel recording described in
`research/jaw/site-evidence.md` §5 measures it directly.
```
40 sources: 40 verified, 0 could not be checked, 0 wrong or made up, 40 not already in our notes.
PASS
```

`check_sources.py` resolves every PMID on PubMed, every patent number on Google Patents, checks each
URL answers with HTTP < 400, requires both free-text fields to be real sentences, and counts how many
sources are new relative to `research/*.md`.
# ss-research-patents — silent-speech patent and inventor sweep

A patent and literature sweep for a **hidden jaw wearable** that decodes silent speech:
CN, US, KR, JP, EP/DE/WO patents on silent / subvocal speech sensed at the face, jaw,
chin, submental, cheek, neck, throat, behind-ear and ear-canal sites, each traced to the
inventors' papers, code and datasets.

**What is in here**

| Path | What it is |
|---|---|
| `research/jaw/patents.md` | The analysis: top-10 ideas, design dead-ends, the full 35-patent table, family evolution, and the watch-out list (not legal advice). |
| `research/jaw/sources-patents.jsonl` | 52 live-checked sources: 35 patents, 13 papers, 3 code repos, 1 dataset. Same schema as `ss-research-baltic`. |
| `research/jaw/patent_candidates.txt` | The 61 candidate publication numbers from the search sweep. |
| `scripts/patent_search.py` | Google Patents keyword search (no key). |
| `scripts/fetch_patent.py` | Fetch a Google Patents page and extract metadata/claims/description. |
| `scripts/fetch_lens.py` | Fetch the same fields from Lens.org public JSON (fallback when Google throttles). |
| `scripts/patent_summarize.py` | Turn cached Lens records into the compact facts used in the table. |
| `scripts/build_sources.py` | Regenerate `sources-patents.jsonl`. |

`research/*.md` from earlier tracks in this series is the shared memory; this track adds
new facts only.

## Install

Python 3 standard library only — no packages, no venv.

```bash
cd ~/theprojects/queue/.worktrees/silent-speech/ss-research-patents
python3 --version        # 3.10+
```

## Run

Verify the sources (the project's own acceptance checks):

```bash
test -s research/jaw/patents.md
test $(grep -c '"kind": *"patent"' research/jaw/sources-patents.jsonl) -ge 25
test $(grep -ci 'CN[0-9]' research/jaw/sources-patents.jsonl) -ge 5
python3 ~/theprojects/orchestrator/bin/check_sources.py research/jaw/sources-patents.jsonl \
    --min 40 --min-new 30 --kinds paper,patent --known research
```

Rebuild the data files:

```bash
python3 scripts/fetch_lens.py US10621973B1 CN113288183B   # -> research/jaw/raw/ (gitignored)
python3 scripts/patent_summarize.py                       # facts for the table
python3 scripts/build_sources.py                          # -> sources-patents.jsonl
```

The `raw/` folder holds downloaded HTML/JSON and must stay out of git (it is in
`.gitignore`).

## Example output

```text
$ python3 scripts/build_sources.py
wrote 52 sources -> research/jaw/sources-patents.jsonl
Counter({'patent': 35, 'paper': 13, 'code': 3, 'dataset': 1})
too-short: []

$ python3 scripts/patent_summarize.py | head -6
===== US10621973B1 | ACTIVE | prio 2017-03-23 | 2020-04-14 | term 2038-07-06
T: Sub-vocal speech recognition apparatus and method
A: VOCASSO INC
I: MCVICKER RYAN; EIGENBRODE BRETT

$ python3 ~/theprojects/orchestrator/bin/check_sources.py research/jaw/sources-patents.jsonl \
    --min 40 --min-new 30 --kinds paper,patent --known research
52 sources: 50 verified, 2 could not be checked, 0 wrong or made up, 49 not already in our notes.
PASS
```

See `DONE.md` for the full acceptance run and `PROGRESS.md` for status and next steps.
# ss-jaw-design — hidden jaw-integrated silent-speech prototype v1

A **design document**, not software. It turns the repo's three research sweeps (Baltic groups and
patents, silent-speech patents, PubMed site evidence) into one buildable prototype plan for a
surface-EMG silent-speech wearable whose electrodes are hidden under the jaw line, behind the ear
and on the neck instead of on the face.

## What it is

- `research/jaw/prototype-v1.md` — the deliverable. Three concealed form factors (behind-ear pod +
  jaw-line arm; headphone/earbud + submental strip; collar/neckband), a bill of materials with real
  part numbers and EU sources cheapest-first, what others tried and dropped, a borrowed-EMG week
  plan with a 16-channel electrode map that records Gaddy's 8 sites and the hidden candidates at
  the same time, and a week-by-week route to a first wearable by 2026-12-31.
- `CALL-PREP.md` — the call sheet for the labs, now with an appended **Electrode plan** section
  that points at `prototype-v1.md` §4.

Every accuracy claim is tagged with a source id: `[pubmed-<PMID>]` and `[baltic-<PMID|row>]` index
the JSONL source lists, `[patents-<number>]` indexes the patent list, and `[research/NN §x]`
points into the repo's earlier track notes.

## Install

Nothing to install. It is Markdown. There is no code, no dependency, no network call.

## Verify

Run from the repo root; both commands must exit 0:

```console
$ test -s research/jaw/prototype-v1.md && grep -qi 'electrode plan' CALL-PREP.md; echo $?
0
$ test $(grep -cE '\[(baltic|patents|pubmed)-?[0-9]+\]|sources-(baltic|patents|pubmed)' research/jaw/prototype-v1.md) -ge 15; echo $?
0
```

Example output (real, 2026-10-06):

```console
$ grep -cE '\[(baltic|patents|pubmed)-?[0-9]+\]|sources-(baltic|patents|pubmed)' research/jaw/prototype-v1.md
39
$ wc -l research/jaw/prototype-v1.md CALL-PREP.md
  393 research/jaw/prototype-v1.md
  161 CALL-PREP.md
```

## Where the inputs live

`research/jaw/baltic.md`, `research/jaw/patents.md`, `research/jaw/site-evidence.md` and the three
`sources-*.jsonl` lists come from the sibling research items in this repo series. This item adds
only `prototype-v1.md`, the `CALL-PREP.md` section, and the progress/readme/done notes.

## Not legal advice

The patent summaries in `prototype-v1.md` §3 are design observations, not freedom-to-operate
opinions. Read the cited claims with a patent attorney before filing or selling.

## OpenBCI forum sweep (`ss-openbci-forum`) — done

What it is: the OpenBCI community forum mined for what it knows about the parts and problems in our
hidden-jaw EMG wearable — ADS1299 boards and clones, bias/SRB/reference wiring, mains hum, dry vs
gel electrodes, ear/cEEGrid, sample rate and wireless throughput, LSL sync, battery and wearability.
The input is a local dump of 1330 threads (post text only, gitignored). The forum is not fetched
again.

**What exists now** (all committed):

| Path | What it is |
|---|---|
| `scripts/forum_prefilter.py` | Stdlib keyword scorer: keeps at most 300 threads, writes the selection and the prompts. |
| `scripts/test_forum_prefilter.py` | Three offline assert checks (redaction, rare-part ranking, selection cap). |
| `research/jaw/forum-selection.tsv` | 300 kept threads + header: `rank, id, score, title, url` (210 rare-part pins, cutoff 36.5). |
| `local_batch/forum.yaml`, `local_batch/forum-prompts.jsonl` | The runner's local-batch request and the 300 prompts (usernames/e-mails redacted). |
| `research/jaw/forum-extracts.jsonl` | 300 extracts, runner-written by the local 27B (`qwen3.8-27b-uncensored`); never edited in-session. |
| `research/jaw/forum-spotcheck.md` | 30 extracts checked against the raw posts (28 right, 2 partial, 0 wrong). |
| `research/jaw/openbci-forum.md` | The deliverable: 18 build/recording changes, part problems and fixes, EMG/face/jaw reports, what to avoid — 46 thread links. |
| `research/jaw/sources-forum.jsonl` | 46 threads, one JSON object per line, `kind: "web"`, each HTTP-checked live. |

Install: nothing. Python 3 standard library only. Network is needed only to re-verify the final
thread URLs.

Run the pre-filter (input path is the gitignored main-checkout dump):

```console
$ python3 scripts/forum_prefilter.py --input ~/theprojects/queue/silent-speech/data/raw/openbci-forum/threads.jsonl
threads: 1330  kept: 300  cutoff: 36.5  max: 293.5  rare kept: 210
redacted 918 e-mail/@handle strings from the kept post text
wrote research/jaw/forum-selection.tsv (300 rows) and local_batch/forum-prompts.jsonl (2374 KiB)
$ python3 scripts/test_forum_prefilter.py
ok: 3 checks passed
```

Acceptance checks, with their real output:

```console
$ test -s research/jaw/openbci-forum.md && test $(grep -c 'openbci.com/forum' research/jaw/openbci-forum.md) -ge 15; echo $?
0
$ grep -c 'openbci.com/forum' research/jaw/openbci-forum.md
62
$ test $(grep -c . research/jaw/forum-spotcheck.md) -ge 20; echo $?
0
$ python3 ~/theprojects/orchestrator/bin/check_sources.py research/jaw/sources-forum.jsonl --min 15 --kinds web
46 sources: 46 verified, 0 could not be checked, 0 wrong or made up, 46 not already in our notes.
PASS
```

Redaction: quoted usernames (`@handle`), e-mail addresses and home-directory paths are replaced in
the prompt text before it is committed, so no username or personal detail from a post enters the
repo. The raw forum dump itself is not committed.

---

# ss-grants-eu — public LV + EU funding for the silent-speech wearable

A research deliverable, not a program: `research/jaw/grants-eu.md` lists the public grants and
funds a Latvia-based solo builder can realistically win for the hidden-jaw sEMG wearable in
2026–2027, split into **case A** (a private individual, no company) and **case B** (a newly founded
Latvian SIA). It gives a top-5 order with the exact next step and the deadline quoted from the
official page, a full table per case, and what must be ready (one-pager, budget, pitch, 3-minute
video, company) versus which funds need a working MVP.

Sources: `research/jaw/sources-grants-eu.jsonl` — 25 official pages, one JSON object per line,
`kind: "web"`, each HTTP-checked live. Nothing to install; the verifier is the orchestrator's
`check_sources.py` plus network access.

```console
$ test -s research/jaw/grants-eu.md && grep -qi 'deadline' research/jaw/grants-eu.md; echo $?
0
$ python3 ~/theprojects/orchestrator/bin/check_sources.py research/jaw/sources-grants-eu.jsonl --min 12 --kinds web
25 sources: 25 verified, 0 could not be checked, 0 wrong or made up, 25 not already in our notes.
PASS
```

Rules followed: research only from official public pages; no application, registration or e-mail;
no personal data (all `people` lists are empty).

---

# ss-pod-datasheets — vendor PDFs for the pod v1 schematic review

Fetch-only item: the official datasheets for the pod v1 BOM, downloaded so a reviewer can read the
primary sources. Everything lives in **`hw/pod/ref/ds/`**: 13 PDFs plus **`INDEX.md`**, which
lists one line per file — filename, source URL, size, and for LCSC
parts the LCSC number, the stock count and the unit price seen on 2026-10-07. The PDFs and
`INDEX.md` are **committed** (public vendor documents; the repo already tracks 211 reference PDFs):
the runner re-runs the `done_when` check in the main checkout after merging the item branch, and a
gitignored `ds/` never got there. Only `.gitignore` needed a one-line un-ignore
(`hw/pod/ref/*` + `!hw/pod/ref/ds/`). `INDEX.md` also
resolves the open questions a reviewer would otherwise have to chase:

- the BOM's **LP5907 (C80670) is out of stock**; the MSKSEMI drop-in (C20538881) is in stock, and
  `INDEX.md` lists four other same-pinout SOT-23-5 3.3 V low-noise LDOs with stock and datasheets;
- the JST SH connector (C160402) is JLCPCB extended and stocked, plus the cable-side housing name
  (SHR-02V-S-B) and crimp terminals;
- the **KT-0603R polarity/pad drawing** is on page 2 of its datasheet;
- the current u-blox NINA-B3 System Integration Manual is **UBX-17056748 R15** (UBX-17005730 is
  gone);
- **`C55173001` is a 6-pin 2.50 mm-pitch single-row pogo**, not the "2x6 1.27 mm" the brief said —
  flagged for the layout review;
- no separate ADS1298ECG-FE schematic PDF exists; it is inside SBAU171D, kept at
  `hw/pod/ref/ti_ads1298ecgfe_ug.pdf`.

Nothing to install and nothing to run offline. The `INDEX.md` is generated from live pages, so the
stock/price columns need a re-check before ordering.

```console
$ test -s hw/pod/ref/ds/INDEX.md && test $(ls hw/pod/ref/ds/*.pdf | wc -l) -ge 8; echo $?
0
$ ls hw/pod/ref/ds/*.pdf | wc -l
13
$ git check-ignore -q hw/pod/ref/ds/ti_lp5907.pdf; echo "ignored rc=$?"
ignored rc=1
```

---

# ss-crowdfunding — how first hardware products did on crowdfunding and pre-orders

Research only, from public pages. **`research/jaw/crowdfunding.md`** answers what a first-time
hardware startup actually gets from Kickstarter, Indiegogo, Crowd Supply and direct pre-orders:
a 22-case table (money/speed and shipping/outcome), the platform rules and fees that matter, the
published evidence on how late hardware ships, and the patterns behind the campaigns that shipped
on time. It covers Pebble, Oculus, OpenBCI, Emotiv Insight, CST-01, Bragi Dash, Kreyos, Skully,
Muse, Mudra Band, Rabbit r1, Humane AI Pin, Brilliant Labs (Monocle/Frame/Halo), Even Realities
(G1/G2), Friend, Omi, Limitless and Neurosity Crown. Every number is tagged **(quoted)** or
**(est)**.

**`research/jaw/sources-crowdfunding.jsonl`** holds the 74 pages actually opened, one JSON object
per line (`kind, title, url, people, year, what_they_did, useful_for_us`). Kickstarter and
Indiegogo block this machine, so their campaign pages were read through the public `r.jina.ai`
reader (URL kept in each line) or via Kicktraq totals; the rest are official help/guide pages,
company pages, news and peer-reviewed papers.

Nothing to install: the deliverable is Markdown plus JSON Lines, and the only script is the
standard-library source checker.

```console
$ test -s research/jaw/crowdfunding.md && grep -qi 'kickstarter' research/jaw/crowdfunding.md && grep -qi 'crowd supply' research/jaw/crowdfunding.md; echo $?
0
$ python3 ~/theprojects/orchestrator/bin/check_sources.py research/jaw/sources-crowdfunding.jsonl --min 20 --kinds web
74 sources: 73 verified, 1 could not be checked, 0 wrong or made up, 74 not already in our notes.
PASS
```

---

# ss-nda-research — one-way NDA for a hardware design review

Research only, from official or primary public pages. **`research/jaw/nda-research.md`** answers
what a one-way NDA for a hardware design review must contain to hold up in Latvia and with overseas
freelancers: the Latvian Trade Secret Protection Law definition, "appropriate and reasonable steps",
remedies and the 3-year limitation period; the Civil Law līgumsods (Article 1716 fixed vs increasing
penalties, the 10 % cap, Article 1724.1 reduction); whether English-only is valid under the State
Language Law; cession of the NDA claims to a later SIA; Rome I and Brussels I bis; the LTRK and RICAC
arbitration model clauses and small-claim fees; the New York Convention (172 parties, US/UK/India/
Pakistan/Philippines/Ukraine); US liquidated damages vs penalties and enforcement of a foreign
arbitration clause against a US freelancer; EPC Article 54 and EPO case law on disclosure under a
confidentiality agreement; eIDAS and the Latvian Electronic Documents Law on simple vs qualified
e-signatures; Upwork and Fiverr confidentiality, IP and off-platform rules; and the clauses that
hurt the discloser (chiefly the residuals clause). It is **not legal advice** and says where a
lawyer is needed. Note: EUR-Lex, the live Upwork/Fiverr legal pages and `rsst.lv` block this
machine, so those texts are quoted from `legislation.gov.uk` and Internet Archive snapshots of the
official URLs — each source line records the exact URL used.

**`research/jaw/sources-nda.jsonl`** holds the 59 pages actually opened, one JSON object per line
(`kind, title, url, people, year, what_they_did, useful_for_us`).

Nothing to install: the deliverable is Markdown plus JSON Lines, and the only script is the
standard-library source checker.

```console
$ test -s research/jaw/nda-research.md && grep -qi 'līgumsod\|ligumsod' research/jaw/nda-research.md && grep -qi 'Rome I' research/jaw/nda-research.md && grep -qi 'New York Convention' research/jaw/nda-research.md; echo $?
0
$ python3 ~/theprojects/orchestrator/bin/check_sources.py research/jaw/sources-nda.jsonl --min 10 --kinds web
59 sources: 59 verified, 0 could not be checked, 0 wrong or made up, 59 not already in our notes.
PASS
```
