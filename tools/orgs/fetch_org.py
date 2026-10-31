"""Stdlib only. Searches for an ORGANISATION by generic queries (never anything about our product), then reads
the about / team / partners pages of the top hits. Saves org.json under OUT for a reader to summarise.
    ORG_OUT=research/jaw/raw/vc python3 tools/orgs/fetch_org.py tools/orgs/venture-catalysts.json
The JSON file: {"queries": [[query, region], ...], "max_hosts": 25}. People: only what the org pages and press
publish about professional roles; social networks are skipped."""
import html, json, os, re, sys, time, urllib.parse, urllib.request

CFG = json.load(open(sys.argv[1]))
OUT = os.environ.get("ORG_OUT", "research/jaw/raw/org")
os.makedirs(OUT, exist_ok=True)
UA = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
SKIP = ("duckduckgo.", "facebook.", "linkedin.", "youtube.", "wikipedia.", "twitter.", "x.com", "instagram.",
        "tiktok.", "reddit.")
PATHS = ["", "/about", "/about-us", "/team", "/our-team", "/people", "/partners", "/mentors", "/investors",
         "/en/about", "/en/team", "/en/partners", "/par-mums", "/komanda", "/partneri", "/lv/komanda"]


def get(url, n=500000):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en,lv;q=0.8"})
        with urllib.request.urlopen(req, timeout=12) as r:
            return r.status, r.read(n).decode("utf-8", "replace"), r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, "", url
    except Exception as e:  # network errors are recorded, not fatal
        return 0, repr(e)[:200], url


def text(h):
    h = re.sub(r"(?is)<(script|style|noscript|svg).*?</\1>", " ", h)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[^>]+>", " ", h))).strip()


out, hosts = {"search": {}, "sites": {}}, {}
for q, region in CFG["queries"]:
    st, b, _ = get("https://html.duckduckgo.com/html/?" + urllib.parse.urlencode({"q": q, "kl": region}))
    links = []
    for m in re.finditer(r'class="result__a" href="([^"]+)"[^>]*>(.*?)</a>', b, re.S):
        href = html.unescape(m.group(1))
        if "uddg=" in href:
            href = urllib.parse.unquote(urllib.parse.parse_qs(urllib.parse.urlparse(href).query)["uddg"][0])
        links.append({"url": href, "title": text(m.group(2))})
    snippets = [text(s) for s in re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', b, re.S)]
    for l, s in zip(links, snippets + [""] * len(links)):
        l["snippet"] = s
    out["search"][q] = {"status": st, "results": links[:10]}
    print("q", repr(q), st, len(links), flush=True)
    for l in links[:5]:
        p = urllib.parse.urlparse(l["url"])
        if p.scheme.startswith("http") and not any(s in p.netloc for s in SKIP):
            hosts.setdefault(p.netloc, {"from_query": q, "first_url": l["url"], "title": l["title"]})
    time.sleep(4)

for host, meta in list(hosts.items())[:CFG.get("max_hosts", 25)]:
    site, seen = dict(meta, pages={}), set()
    for path in PATHS:
        u = meta["first_url"] if path == "" else f"https://{host}{path}"
        st, b, final = get(u)
        if st == 0:  # dead or very slow host: stop trying its other paths
            break
        if st == 200 and b and final not in seen:
            seen.add(final)
            site["pages"][final] = text(b)[:12000]
        time.sleep(1)
    out["sites"][host] = site
    print("site", host, len(site["pages"]), flush=True)
    json.dump(out, open(f"{OUT}/org.json", "w"), indent=1, ensure_ascii=False)  # partial results survive a timeout

json.dump(out, open(f"{OUT}/org.json", "w"), indent=1, ensure_ascii=False)
print("done: queries", len(out["search"]), "sites", len(out["sites"]), flush=True)
