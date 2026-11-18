#!/usr/bin/env python3
"""Harvest Tavily raw pool -> windowed evidence.
Multi-format date parsing (RFC-2822 + ISO). Never use d[:10].
published_date=None items are counted separately and KEPT (page date may exist).
"""
import json, glob, os, sys, re
from datetime import datetime, date, timedelta
from email.utils import parsedate_to_datetime

WIN_LO = os.environ.get("EDN_WIN_LO", "2026-11-11")
WIN_HI = os.environ.get("EDN_WIN_HI", "2026-11-18")

def pdate(s):
    if not s: return None
    s = str(s).strip()
    for f in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%a, %d %b %Y %H:%M:%S %Z",
              "%a, %d %b %Y", "%a, %d %b %Y %H:%M:%S", "%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(s, f).strftime("%Y-%m-%d")
        except Exception:
            pass
    try:
        return parsedate_to_datetime(s).strftime("%Y-%m-%d")
    except Exception:
        pass
    m = re.search(r"(\d{4}-\d{2}-\d{2})", s)
    if m: return m.group(1)
    m = re.search(r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+2026", s)
    if m:
        try: return datetime.strptime(m.group(0).replace(".", ""), "%B %d, %Y").strftime("%Y-%m-%d")
        except Exception: return None
    return None

def in_window(d):
    if not d: return False
    return WIN_LO <= d <= WIN_HI

def load(dirs):
    items = []
    seen = set()
    for d in dirs:
        for f in sorted(glob.glob(os.path.join(d, "*.json")) + glob.glob(os.path.join(d, "raw", "*.json"))):
            try:
                data = json.load(open(f))
            except Exception:
                continue
            res = data.get("results") if isinstance(data, dict) else None
            if not res: continue
            for r in res:
                u = r.get("url") or ""
                if not u or u in seen: continue
                c = (r.get("content") or "").strip()
                if len(c) < 120: continue
                seen.add(u)
                d_ = pdate(r.get("published_date"))
                items.append({
                    "date": d_, "in_window": in_window(d_),
                    "url": u, "title": (r.get("title") or "").strip(),
                    "content": c, "score": r.get("score"),
                    "published_raw": r.get("published_date"),
                    "src_file": os.path.basename(f),
                })
    return items

if __name__ == "__main__":
    dirs = sys.argv[1:] or ["/tmp/edn-west/raw", "/tmp/edn-north/raw"]
    items = load(dirs)
    win = [i for i in items if i["in_window"]]
    none_dated = [i for i in items if i["date"] is None]
    out = os.environ.get("EDN_RAW_OUT", "/tmp/edn-harvest.json")
    json.dump({"all": items, "window": win, "none_dated": none_dated},
              open(out, "w"), ensure_ascii=False, indent=1)
    print(f"total kept (content>=120): {len(items)}")
    print(f"in window {WIN_LO}..{WIN_HI}: {len(win)}")
    print(f"published_date=None: {len(none_dated)}")
    print("WROTE", out)
    # quick signal peek
    seen_host = {}
    for i in win:
        h = re.sub(r"^https?://([^/]+).*", r"\1", i["url"])
        seen_host[h] = seen_host.get(h, 0) + 1
    for h, c in sorted(seen_host.items(), key=lambda kv: -kv[1])[:18]:
        print(f"   {c:>3}  {h}")
