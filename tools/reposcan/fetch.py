"""Stdlib only. Runs in a podman container (mount token at /run/token, out at /out) or directly in a sandboxed
session with REPOSCAN_TOKEN_FILE / REPOSCAN_OUT set.
GitHub search -> repo metadata + README text, saved under /out. Token read from /run/token, never printed."""
import json, os, time, urllib.request, urllib.parse, sys

TOKEN_FILE = os.environ.get("REPOSCAN_TOKEN_FILE", "/run/token")
TOKEN = open(TOKEN_FILE).read().strip() if os.path.exists(TOKEN_FILE) else ""
OUT = os.environ.get("REPOSCAN_OUT", "/out")
SINCE = "2024-06-01"
QUERIES = [
    "ads1298", "ads1299", "ads129x", "ads1299 nrf52", "ads1298 nrf52840", "ads1299 zephyr", "ads1299 esp32",
    "openbci cyton firmware", "ads1299 ble", "emg ble nrf52", "sEMG wearable firmware",
    "silent speech", "silent speech interface", "subvocal", "subvocalization", "alterego",
    "emg speech recognition", "emg speech", "semg speech", "facial emg", "emg phoneme",
    "voiceless speech", "digital voicing emg", "emg2qwerty", "electromyography speech decoding",
    "emg to text", "brainflow", "emg transformer", "emg gesture nrf52840", "eeg nrf52840",
    "ads129x emulator", "biopotential pcb kicad", "eeg headphones", "ear eeg", "cEEGrid",
    "emg dataset speech", "mouthing words emg", "lip reading emg",
    "holter ecg ads1298", "open source ecg kicad", "wearable ecg nrf52",
]
EXTRA = ["mateusglucas/ads129x-emulator", "RobertCsordas/MobilECG-II", "shriram-m/12-lead-holter-ecg"]

def get(url, accept="application/vnd.github+json"):
    h = {"Accept": accept, "User-Agent": "silent-speech-reposcan", "X-GitHub-Api-Version": "2022-11-28"}
    if TOKEN:
        h["Authorization"] = "Bearer " + TOKEN
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                time.sleep(30); continue
            if e.code == 404:
                return None
            raise
    return None

repos = {}
for q in QUERIES:
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode(
        {"q": f"{q} pushed:>={SINCE}", "sort": "stars", "order": "desc", "per_page": 25})
    data = json.loads(get(url) or b"{}")
    for it in data.get("items", []):
        r = repos.setdefault(it["full_name"], {"queries": []})
        r["queries"].append(q)
        r.update({k: it.get(k) for k in ("full_name", "html_url", "description", "stargazers_count", "forks_count",
                                         "language", "pushed_at", "created_at", "archived", "topics")})
        r["license"] = (it.get("license") or {}).get("spdx_id")
    print(f"{q!r}: {len(data.get('items', []))}", flush=True)
    time.sleep(2.5 if TOKEN else 6.5)   # search API: 30/min with a token, 10/min without

for full in EXTRA:
    it = json.loads(get(f"https://api.github.com/repos/{full}") or b"{}")
    if it:
        r = repos.setdefault(full, {"queries": ["user-supplied"]})
        r.update({k: it.get(k) for k in ("full_name", "html_url", "description", "stargazers_count", "forks_count",
                                         "language", "pushed_at", "created_at", "archived", "topics")})
        r["license"] = (it.get("license") or {}).get("spdx_id")

json.dump(repos, open(f"{OUT}/repos.json", "w"), indent=1)   # saved before READMEs: a stop later loses nothing
print("repos:", len(repos), "token used:", bool(TOKEN), flush=True)

# READMEs from raw.githubusercontent.com: not counted against the API rate limit; resumable (skips files on disk)
import concurrent.futures as cf
os.makedirs(f"{OUT}/readme", exist_ok=True)
NAMES = ("README.md", "readme.md", "Readme.md", "README.rst", "README.markdown", "README.txt", "README")

def readme(full):
    dst = f"{OUT}/readme/{full.replace('/', '__')}.md"
    if os.path.exists(dst):
        return full, os.path.getsize(dst)
    for n in NAMES:
        try:
            req = urllib.request.Request(f"https://raw.githubusercontent.com/{full}/HEAD/{n}",
                                         headers={"User-Agent": "silent-speech-reposcan"})
            with urllib.request.urlopen(req, timeout=20) as r:
                body = r.read(60000)
            open(dst, "wb").write(body)
            return full, len(body)
        except Exception:
            continue
    return full, 0

with cf.ThreadPoolExecutor(8) as ex:
    for i, (full, n) in enumerate(ex.map(readme, sorted(repos))):
        repos[full]["readme_chars"] = n
        if i % 50 == 0:
            print(f"readme {i}/{len(repos)}", flush=True)
json.dump(repos, open(f"{OUT}/repos.json", "w"), indent=1)
print("done:", len(repos), "repos,", sum(1 for r in repos.values() if r.get("readme_chars")), "with README")
