import json, subprocess, sys, re
from concurrent.futures import ThreadPoolExecutor

def run(args):
    p = subprocess.run(args, capture_output=True, text=True, timeout=180)
    return p.stdout, p.stderr

def search(q, fname, extra=None):
    cmd = ["tvly", "search", q, "--time-range", "week", "--topic", "news",
           "--max-results", "10", "--json"]
    if extra: cmd += extra
    out, err = run(cmd)
    try:
        d = json.loads(out)
    except Exception:
        print("FAIL", q, err[:200]); return
    json.dump(d, open(fname, "w"), ensure_ascii=False)
    print("==", q)
    for r in d.get("results", []):
        print("  ", r.get("published_date"), "|", r["title"][:75], "|", r["url"])

def extract(url, fname):
    out, err = run(["tvly", "extract", url, "--json"])
    try:
        d = json.loads(out)
    except Exception:
        print("FAILX", url, err[:200]); return
    json.dump(d, open(fname, "w"), ensure_ascii=False)
    for r in d.get("results", []):
        t = r.get("raw_content", "") or ""
        m = re.search(r'\n# ([^\n]+)\n\n【发布时间：([^\]]+)\】\n\n(.{0,1600})', t, re.S)
        print("=====", url)
        if m:
            print("T:", m.group(1), "|", m.group(2))
            print(m.group(3)[:1500].replace("\n", " "))
        else:
            print("NOMATCH len=", len(t), t[:300].replace("\n", " "))

if __name__ == "__main__":
    mode = sys.argv[1]
    jobs = json.load(open(sys.argv[2]))
    fn = search if mode == "s" else extract
    with ThreadPoolExecutor(max_workers=5) as ex:
        list(ex.map(lambda j: fn(j[0], j[1]), jobs))
