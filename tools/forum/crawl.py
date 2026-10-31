"""Polite OpenBCI forum crawler (runs inside a throwaway podman container).

Reads the public Vanilla forum pages: every discussion title, then the full text of threads whose
title matches silent-speech/EMG/hardware terms or that sit in the hardware-type categories.
Stores post TEXT only (no usernames, no profiles). robots.txt allows /forum (only /archive is
disallowed). 1 request per 1.5 s. Resumable.
Output: /out/discussions.jsonl (all titles), /out/threads.jsonl (selected threads, posts as text).
"""
import html, json, re, sys, time, urllib.error, urllib.request
from html.parser import HTMLParser

ROOT = "https://openbci.com/forum/index.php?p="
UA = {"User-Agent": "Mozilla/5.0 research-crawler (polite, 1 req/1.5s)"}
DELAY = 1.5
KEEP = re.compile(r"(emg|electromyo|silent|subvocal|speech|jaw|chin|face|facial|mouth|tongue|throat|"
                  r"neck|\bear\b|ears|ceegrid|behind|ads1?29|ads131|pieeg|cerelog|clone|diy|pcb|schematic|"
                  r"bias|srb|reference|noise|artifact|artefact|electrode|dry|gel|impedance|sample.?rate|"
                  r"sampling|hz\b|bluetooth|\bble\b|wifi|latency|esp32|nrf|battery|wearable|glasses|"
                  r"headphone|myoware|muscle|daisy|sync|lsl|marker)", re.I)
CATS = ["electrodes", "build-it-yourself", "hardware", "research", "headware", "other-platforms"]
last = [0.0]

def get(path):
    wait = DELAY - (time.time() - last[0])
    if wait > 0:
        time.sleep(wait)
    for attempt in range(4):
        last[0] = time.time()
        try:
            req = urllib.request.Request(ROOT + path, headers=UA)
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return ""
            time.sleep(15 * (attempt + 1))
        except Exception:
            time.sleep(10 * (attempt + 1))
    return ""

LINK = re.compile(r'href="https://openbci\.com/forum/index\.php\?p=/discussion/(\d+)/([^"/#]+)"[^>]*>(.*?)</a>', re.S)

def list_pages(prefix):
    found, page = {}, 1
    while True:
        h = get(f"{prefix}/p{page}" if page > 1 else prefix)
        new = 0
        for did, slug, label in LINK.findall(h):
            title = html.unescape(re.sub(r"<[^>]+>", "", label)).strip()
            if did not in found and title:
                found[did] = {"id": int(did), "slug": slug, "title": title}
                new += 1
        print(f"{prefix} p{page}: +{new}", flush=True)
        if new == 0:
            return found
        page += 1

class Msg(HTMLParser):
    """Collect the text of every <div class="Message userContent"> (nested divs tracked)."""
    def __init__(self):
        super().__init__(); self.posts, self.depth, self.buf = [], 0, []
    def handle_starttag(self, tag, attrs):
        if tag == "div":
            cls = dict(attrs).get("class") or ""
            if self.depth:
                self.depth += 1
            elif "Message" in cls and "userContent" in cls:
                self.depth, self.buf = 1, []
        if self.depth and tag in ("br", "p", "li"):
            self.buf.append("\n")
    def handle_endtag(self, tag):
        if tag == "div" and self.depth:
            self.depth -= 1
            if self.depth == 0:
                self.posts.append(re.sub(r"[ \t]+", " ", "".join(self.buf)).strip()[:5000])
    def handle_data(self, data):
        if self.depth:
            self.buf.append(data)

def thread(did, slug):
    posts, page = [], 1
    while page <= 30:
        h = get(f"/discussion/{did}/{slug}/p{page}" if page > 1 else f"/discussion/{did}/{slug}")
        m = Msg(); m.feed(h)
        fresh = [p for p in m.posts if p not in posts]
        if not fresh:
            break
        posts += fresh
        if f"/discussion/{did}/{slug}/p{page + 1}" not in h:
            break
        page += 1
    return posts

def main():
    out = "/out"
    alld = list_pages("/discussions")
    cat_ids = set()
    for c in CATS:
        cat_ids |= set(list_pages(f"/categories/{c}"))
    with open(f"{out}/discussions.jsonl", "w") as f:
        for d in alld.values():
            f.write(json.dumps(d) + "\n")
    sel = [d for k, d in alld.items() if KEEP.search(d["title"] + " " + d["slug"]) or k in cat_ids]
    print(f"selected {len(sel)} of {len(alld)} discussions", flush=True)
    if not alld:
        sys.exit(2)
    done = set()
    try:
        done = {json.loads(l)["id"] for l in open(f"{out}/threads.jsonl")}
    except FileNotFoundError:
        pass
    with open(f"{out}/threads.jsonl", "a") as f:
        for i, d in enumerate(sel, 1):
            if d["id"] in done:
                continue
            d["url"] = f"https://openbci.com/forum/index.php?p=/discussion/{d['id']}/{d['slug']}"
            d["posts"] = thread(d["id"], d["slug"])
            f.write(json.dumps(d) + "\n"); f.flush()
            if i % 25 == 0:
                print(f"threads {i}/{len(sel)}", flush=True)
    print("done", flush=True)

main()
