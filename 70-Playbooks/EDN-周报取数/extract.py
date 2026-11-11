#!/usr/bin/env python3
"""EDN 2026-11-11 — 从 raw Tavily JSON 抽取窗口内证据（子任务 C：安全厂商 + 跨厂商领域）"""
import json, glob, os, re, sys
from datetime import datetime, date
from email.utils import parsedate_to_datetime

WINDOW_START = date(2026, 11, 4)
WINDOW_END = date(2026, 11, 11)
RAW = "/tmp/edn-east/raw"

VENDOR_MAP = [
    ("nilesecure.com", "Nile"), ("nile.co", "Nile"),
    ("fortinet.com", "Fortinet"), ("fortinet.net", "Fortinet"),
    ("zscaler.com", "Zscaler"),
    ("paloaltonetworks.com", "Palo Alto Networks"), ("pan.dev", "Palo Alto Networks"),
    ("extremenetworks.com", "Extreme Networks"),
]
DOMAIN_MAP = [
    ("fortinet", "Security-SASE"), ("zscaler", "Zero Trust-SASE"), ("palo alto", "Security-SASE"),
    ("sase", "Security-SASE"), ("zero trust", "Zero Trust-SASE"), ("sse", "Zero Trust-SASE"),
    ("sd-wan", "SD-WAN"), ("sdwan", "SD-WAN"), ("branch", "SD-WAN"),
    ("campus", "Campus Fabric"), ("fabric", "Campus Fabric"), ("wireless", "Campus Fabric"),
    ("agentic", "Agentic Ops"), ("aiops", "AI Ops"), ("a.i. ops", "AI Ops"),
    ("autonomous", "Agentic Ops"),
    ("observability", "Observability"), ("telemetry", "Telemetry-Data Platform"),
    ("white box", "White-box"), ("whitebox", "White-box"), ("silicon", "Silicon-芯片生态"),
    ("broadcom", "Silicon-芯片生态"), ("tomahawk", "Silicon-芯片生态"),
    ("ethernet", "Ethernet-交换标准"), ("ieee 802", "Ethernet-交换标准"),
    ("naas", "NaaS"), ("as a service", "NaaS"), ("subscription", "NaaS"),
    ("dex", "DEX-DEM"), ("device experience", "DEX-DEM"),
    ("digital twin", "Digital Twin"),
    ("nile", "NaaS"), ("cloud networking", "NaaS"),
    ("network security", "Security-SASE"),
]


def pdate(s):
    if not s:
        return None
    s = str(s).strip()
    for f in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%a, %d %b %Y %H:%M:%S %Z",
              "%a, %d %b %Y", "%Y/%m/%d", "%d %b %Y", "%b %d, %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(s.split("T")[0].split("+")[0].strip()
                                     if f in ("%Y-%m-%d", "%Y/%m/%d") else s, f).date()
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
            if key.split(".")[0] in blob:
                vendor = v
                break
    domain = "Cross-vendor"
    for key, d in DOMAIN_MAP:
        if key in blob:
            domain = d
            break
    return vendor, domain


rows, seen, stats = [], set(), {"files": 0, "total": 0, "in_window": 0, "null_date": 0, "short": 0, "dup": 0}
for fp in sorted(glob.glob(os.path.join(RAW, "*.json"))):
    if fp.endswith(".err"):
        continue
    stats["files"] += 1
    try:
        data = json.load(open(fp))
    except Exception:
        continue
    for r in data.get("results", []):
        stats["total"] += 1
        url = r.get("url") or ""
        title = (r.get("title") or "").strip()
        content = (r.get("content") or "").strip()
        if not url or not title:
            continue
        if len(content) < 120:
            stats["short"] += 1
            continue
        key = url.split("?")[0].rstrip("/")
        if key in seen:
            stats["dup"] += 1
            continue
        seen.add(key)
        d = pdate(r.get("published_date"))
        if d is None:
            stats["null_date"] += 1
            in_win = False
        else:
            in_win = WINDOW_START <= d <= WINDOW_END
            if in_win:
                stats["in_window"] += 1
        vendor, domain = classify(url, title, content)
        rows.append({
            "vendor": vendor, "date": d.isoformat() if d else None,
            "in_window": in_win, "title": title, "domain": domain,
            "dimension": "product", "source_type": "media",
            "url": url, "snippet": content[:600],
            "relevance": 3, "confidence": "H2" if in_win else "H3",
        })

json.dump(rows, open("/tmp/edn-east/evidence_raw.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(stats, ensure_ascii=False))
print("rows:", len(rows))
from collections import Counter
print("vendors:", Counter(r["vendor"] for r in rows).most_common())
print("domains:", Counter(r["domain"] for r in rows).most_common())
