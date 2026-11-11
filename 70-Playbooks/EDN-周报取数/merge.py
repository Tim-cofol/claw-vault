#!/usr/bin/env python3
"""EDN 2026-11-11 — merge all lanes, build final data asset."""
import json, glob, os, re, hashlib
from datetime import datetime, date, timezone, timedelta
from email.utils import parsedate_to_datetime

SH = timezone(timedelta(hours=8))
W0, W1 = date(2026, 11, 4), date(2026, 11, 11)
DATE = "2026-11-11"

VMAP = [
    ("arubanetworks", "HPE Aruba"), ("hpe.com", "HPE Aruba"), ("aruba", "HPE Aruba"),
    ("juniper", "Juniper Mist"), ("mist ai", "Juniper Mist"),
    ("arista", "Arista"), ("cisco", "Cisco"),
    ("extremenetworks", "Extreme Networks"), ("extreme networks", "Extreme Networks"),
    ("huawei", "Huawei"), ("新华三", "H3C"), ("h3c", "H3C"),
    ("fortinet", "Fortinet"), ("zscaler", "Zscaler"),
    ("paloaltonetworks", "Palo Alto Networks"), ("nilesecure", "Nile"),
    ("nokia", "Nokia"), ("gtt.net", "GTT"), ("cribl", "Cribl"),
    ("broadcom", "Cross-vendor"), ("nvidia", "Cross-vendor"),
]
DMAP = [
    ("sd-wan", "SD-WAN"), ("sdwan", "SD-WAN"), ("branch", "SD-WAN"), ("sase", "Security-SASE"),
    ("zero trust", "Zero Trust-SASE"), ("sse", "Zero Trust-SASE"), ("fortigate", "Security-SASE"),
    ("fortiaigate", "Security-SASE"), ("security", "Security-SASE"), ("firewall", "Security-SASE"),
    ("campus", "Campus Fabric"), ("fabric", "Campus Fabric"), ("wireless", "Campus Fabric"),
    ("wi-fi 7", "Campus Fabric"), ("802.11be", "Campus Fabric"), ("access point", "Campus Fabric"),
    ("agentic", "Agentic Ops"), ("aiops", "AI Ops"), ("autonomous", "Agentic Ops"),
    ("self-driving", "Agentic Ops"), ("mcp", "Agentic Ops"),
    ("observability", "Observability"), ("telemetry", "Telemetry-Data Platform"),
    ("white box", "White-box"), ("whitebox", "White-box"), ("silicon", "Silicon-芯片生态"),
    ("broadcom", "Silicon-芯片生态"), ("tomahawk", "Silicon-芯片生态"), ("etherlink", "Silicon-芯片生态"),
    ("ethernet", "Ethernet-交换标准"), ("ieee 802", "Ethernet-交换标准"),
    ("naas", "NaaS"), ("as a service", "NaaS"), ("subscription", "NaaS"), ("managed network", "NaaS"),
    ("dex", "DEX-DEM"), ("device experience", "DEX-DEM"),
    ("digital twin", "Digital Twin"), ("nac", "身份-NAC"), ("identity", "身份-NAC"),
    ("policy", "策略编排"), ("orchestrat", "策略编排"),
]
STOP = {"cross-vendor": True}


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
    for dom, v in VMAP:
        if dom in url.lower():
            vendor = v
            break
    if vendor == "Cross-vendor":
        for key, v in VMAP:
            if key in blob:
                vendor = v
                break
    domain = "Cross-vendor"
    for key, d in DMAP:
        if key in blob:
            domain = d
            break
    return vendor, domain


NOISE = ["nile.com.ae", "nilecom.ae", "blue nile", "nile river", "juniper hotels",
         "walnutca.gov", "jobgether", "indeed.com", "ourcryptotalk", "jobspresso",
         "nvidia.com/newsroom", "bambulab", "h3c 3d", "h3c is", "nile advanced core",
         "lakewood", "nile systems"]


def load_lane(dirs):
    rows, seen = [], set()
    for d in dirs:
        for fp in sorted(glob.glob(os.path.join(d, "raw", "*.json"))):
            if fp.endswith(".err"):
                continue
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
                url = (r.get("url") or "").strip()
                title = (r.get("title") or "").strip()
                content = (r.get("content") or "").strip()
                if not url or not title or len(content) < 120:
                    continue
                low = url.lower()
                if any(n in low for n in NOISE):
                    continue
                key = url.split("?")[0].rstrip("/")
                if key in seen:
                    continue
                seen.add(key)
                d0 = pdate(r.get("published_date"))
                inw = bool(d0 and W0 <= d0 <= W1)
                vendor, domain = classify(url, title, content)
                rows.append({
                    "vendor": vendor, "date": d0.isoformat() if d0 else None,
                    "in_window": inw, "title": title, "domain": domain,
                    "dimension": "product", "source_type": "media",
                    "url": url, "snippet": content[:700],
                    "relevance": 3, "confidence": "H2" if inw else "H3",
                })
    return rows


rows = load_lane(["/tmp/edn-east", "/tmp/edn-west", "/tmp/edn-north"])
inw = [r for r in rows if r["in_window"]]
outw = [r for r in rows if not r["in_window"]]
print("merged rows:", len(rows), "| in_window:", len(inw), "| out:", len(outw))

vendors = {}
for r in inw:
    vendors.setdefault(r["vendor"], []).append(r)
domains = {}
for r in inw:
    domains.setdefault(r["domain"], []).append(r)

print("vendors:", {k: len(v) for k, v in sorted(vendors.items(), key=lambda x: -len(x[1]))})
print("domains:", {k: len(v) for k, v in sorted(domains.items(), key=lambda x: -len(x[1]))})
json.dump({"in_window": inw, "out_window": outw}, open("/tmp/edn-east/merged.json", "w"),
          ensure_ascii=False, indent=1)
