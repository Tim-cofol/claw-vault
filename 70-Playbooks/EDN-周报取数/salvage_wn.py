#!/usr/bin/env python3
"""EDN 2026-11-11 — salvage subagent raw Tavily JSON (west/north) into evidence."""
import json, glob, os, re, sys
from datetime import datetime, date
from email.utils import parsedate_to_datetime

WINDOW_START = date(2026, 11, 4)
WINDOW_END = date(2026, 11, 11)

VENDOR_MAP = [
    ("arubanetworks", "HPE Aruba"), ("hpe.com", "HPE Aruba"), ("aruba", "HPE Aruba"),
    ("juniper", "Juniper Mist"), ("mist", "Juniper Mist"),
    ("arista", "Arista"), ("cisco", "Cisco"),
    ("extremenetworks", "Extreme Networks"), ("extreme networks", "Extreme Networks"),
    ("huawei", "Huawei"), ("新华三", "H3C"), ("h3c", "H3C"),
    ("fortinet", "Fortinet"), ("zscaler", "Zscaler"),
    ("paloaltonetworks", "Palo Alto Networks"), ("nilesecure", "Nile"),
    ("broadcom", "Cross-vendor"), ("ethernet alliance", "Cross-vendor"),
]
DOMAIN_MAP = [
    ("sd-wan", "SD-WAN"), ("sdwan", "SD-WAN"), ("branch", "SD-WAN"),
    ("campus", "Campus Fabric"), ("fabric", "Campus Fabric"), ("wireless", "Campus Fabric"),
    ("wi-fi 7", "Campus Fabric"), ("802.11be", "Campus Fabric"),
    ("agentic", "Agentic Ops"), ("aiops", "AI Ops"), ("autonomous", "Agentic Ops"),
    ("observability", "Observability"), ("telemetry", "Telemetry-Data Platform"),
    ("white box", "White-box"), ("whitebox", "White-box"), ("silicon", "Silicon-芯片生态"),
    ("broadcom", "Silicon-芯片生态"), ("tomahawk", "Silicon-芯片生态"),
    ("ethernet", "Ethernet-交换标准"), ("ieee 802", "Ethernet-交换标准"),
    ("naas", "NaaS"), ("as a service", "NaaS"), ("subscription", "NaaS"),
    ("dex", "DEX-DEM"), ("device experience", "DEX-DEM"),
    ("digital twin", "Digital Twin"),
    ("zero trust", "Zero Trust-SASE"), ("sase", "Security-SASE"), ("sse", "Zero Trust-SASE"),
    ("security", "Security-SASE"), ("nac", "身份-NAC"), ("identity", "身份-NAC"),
    ("policy", "策略编排"),
]


def pdate(s):
    if not s:
        return None
    s = str(s).strip()
    for f in ("%Y-%m-%d", "%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y", "%d %b %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(s.split("+")[0].strip() if f == "%Y-%m-%d" else s, f).date()
        except Exception:
            pass
    try:
        return parsedate_to_datetime(s).date()
    except Exception:
        pass
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except Exception:
            return None
    return None


def classify(url, title, content):
    blob = (url + " " + title + " " + (content or "")).lower()
    vendor = "Cross-vendor"
    for dom, v in VENDOR_MAP:
        if dom in url.lower():
            vendor = v
            break
    if vendor == "Cross-vendor":
        for key, v in VENDOR_MAP:
            if key in blob:
                vendor = v
                break
    domain = "Cross-vendor"
    for key, d in DOMAIN_MAP:
        if key in blob:
            domain = d
            break
    return vendor, domain


def load_dir(d, tag):
    rows, seen, stats = [], set(), {"files": 0, "total": 0, "in_window": 0, "null_date": 0}
    for fp in sorted(glob.glob(os.path.join(d, "raw", "*.json"))):
        if fp.endswith(".err"):
            continue
        stats["files"] += 1
        try:
            data = json.load(open(fp))
        except Exception:
            continue
        res = data.get("results") if isinstance(data, dict) else data
        if not isinstance(res, list):
            continue
        for r in res:
            if not isinstance(r, dict):
                continue
            stats["total"] += 1
            url = (r.get("url") or "").strip()
            title = (r.get("title") or "").strip()
            content = (r.get("content") or "").strip()
            if not url or not title:
                continue
            if len(content) < 120:
                continue
            key = url.split("?")[0].rstrip("/")
            if key in seen:
                continue
            seen.add(key)
            d0 = pdate(r.get("published_date"))
            inw = bool(d0 and WINDOW_START <= d0 <= WINDOW_END)
            if d0 is None:
                stats["null_date"] += 1
            elif inw:
                stats["in_window"] += 1
            vendor, domain = classify(url, title, content)
            rows.append({
                "vendor": vendor, "date": d0.isoformat() if d0 else None,
                "in_window": inw, "title": title, "domain": domain,
                "dimension": "product", "source_type": "media",
                "url": url, "snippet": content[:700],
                "relevance": 3, "confidence": "H2" if inw else "H3",
                "origin": tag,
            })
    return rows, stats


all_rows = []
for d, tag in (("/tmp/edn-west", "A_west"), ("/tmp/edn-north", "B_north")):
    r, s = load_dir(d, tag)
    all_rows += r
    print(tag, json.dumps(s, ensure_ascii=False), "rows", len(r))

json.dump(all_rows, open("/tmp/edn-east/evidence_west_north.json", "w"),
          ensure_ascii=False, indent=1)
from collections import Counter
print("vendors:", Counter(r["vendor"] for r in all_rows).most_common())
print("in_window total:", sum(1 for r in all_rows if r["in_window"]))
