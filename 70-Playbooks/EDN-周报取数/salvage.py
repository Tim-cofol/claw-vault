#!/usr/bin/env python3
"""EDN 周报：从子 agent 的 raw Tavily JSON 中抢救证据条目。
子 agent 超时未落 evidence.json 时使用（2026-10-21 实测已验证该路径）。"""
import json, glob, os, sys, re
from datetime import datetime, timedelta

WINDOW_START = datetime(2026, 10, 21)
WINDOW_END = datetime(2026, 10, 28, 23, 59)

VENDOR_MAP = {
    'cisco': 'Cisco', 'aruba': 'HPE Aruba / Juniper', 'hpe': 'HPE Aruba / Juniper',
    'juniper': 'HPE Aruba / Juniper', 'mist': 'HPE Aruba / Juniper', 'silver peak': 'HPE Aruba / Juniper',
    'edgeconnect': 'HPE Aruba / Juniper', 'marvis': 'HPE Aruba / Juniper', 'arista': 'Arista',
    'extreme': 'Extreme Networks', 'nile': 'Nile',
    'fortinet': 'Fortinet', 'fortigate': 'Fortinet', 'fortisase': 'Fortinet',
    'zscaler': 'Zscaler', 'palo alto': 'Palo Alto Networks', 'panw': 'Palo Alto Networks',
    'cortex': 'Palo Alto Networks', 'prisma': 'Palo Alto Networks', 'unit 42': 'Palo Alto Networks',
    'huawei': 'Huawei', '华为': 'Huawei', 'h3c': 'H3C', '新华三': 'H3C',
    'nvidia': 'NVIDIA', 'broadcom': 'Broadcom', 'arista': 'Arista',
    'dell\'oro': "Dell'Oro Group", 'gartner': 'Gartner / 分析师', 'forrester': 'Forrester',
    'idc': 'IDC / 分析师', 'omdia': 'Omdia / 分析师',
}

DOMAIN_MAP = [
    (('agentic', 'aiops', 'aio-?ops', 'autonomous', 'self-driving', 'self driving'), 'Agentic Ops'),
    (('sase', 'sse', 'ztna', 'zero trust', 'zero-trust'), 'SASE-SSE / Zero Trust'),
    (('sd-wan', 'sdwan', 'branch', 'wan'), 'SD-WAN'),
    (('campus', 'wireless', 'wi-fi', 'wifi'), 'Campus Fabric / WLAN'),
    (('observab', 'telemetry', 'monitoring', 'telemetr'), '可观测性 / Telemetry'),
    (('naas', 'network as a service', 'managed service'), 'NaaS'),
    (('sonic', 'white box', 'white-box', 'ethernet', 'switching', 'ocp', 'silicon', 'asic'), 'Ethernet / Silicon / 白盒'),
    (('digital twin', '数字孪生'), 'Digital Twin'),
    (('dex', 'dem', 'digital experience'), 'DEX-DEM'),
    (('identity', 'nac', 'pam'), '身份-NAC'),
    (('orchestrat', 'automation', 'netops'), '策略编排'),
    (('ai security', 'ai agent', 'agentic ai', 'llm', 'genai'), 'Agentic AI'),
    (('market', 'forecast', 'outlook', 'spending', 'revenue'), '市场'),
]

BAD_URL = re.compile(r'facebook\.com|instagram\.com|linkedin\.com|reddit\.com|twitter\.com|x\.com/|'
                      r'youtube\.com|glassdoor|indeed\.com|jobleads|snagajob|monster|ziprecruiter|'
                      r'crunchbase|glassdoor|amazon\.com/shop|ebay|alibaba\.com/product|'
                      r'cnblogs|csdn\.net|jianshu\.com/zhuan|zhihu\.com/question', re.I)

def parse_date(s):
    if not s: return None
    s = s.strip()
    for fmt in ('%a, %d %b %Y', '%Y-%m-%d', '%b %d, %Y', '%Y/%m/%d', '%d %b %Y'):
        try: return datetime.strptime(s, fmt)
        except Exception: pass
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', s)
    if m:
        try: return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except Exception: pass
    return None

def classify(text):
    t = (text or '').lower()
    for v, k in VENDOR_MAP.items():
        if v in t: return k
    return None

def classify_domain(text):
    t = (text or '').lower()
    for pats, dom in DOMAIN_MAP:
        if any(re.search(p, t) for p in pats): return dom
    return '其他'

def norm_date(s):
    d = parse_date(s)
    if not d: return ''
    if WINDOW_START - timedelta(days=3) <= d <= WINDOW_END:
        return d.strftime('%Y-%m-%d')
    return ''

def main():
    out, seen = [], set()
    files = []
    for pat in sys.argv[1:] or ['/tmp/edn-west/*.json', '/tmp/edn-west/*/*.json',
                                '/tmp/edn-north/*.json', '/tmp/edn-north/*/*.json']:
        files.extend(glob.glob(pat))
    for p in files:
        try:
            d = json.load(open(p))
        except Exception:
            continue
        if not isinstance(d, dict): continue
        results = d.get('results')
        if not isinstance(results, list): continue
        for it in results:
            if not isinstance(it, dict): continue
            u = (it.get('url') or '').strip()
            title = (it.get('title') or '').strip()
            if not u or not title: continue
            if BAD_URL.search(u): continue
            body = (it.get('content') or it.get('raw_content') or '')[:600]
            blob = title + ' ' + body
            vendor = classify(blob)
            if not vendor: continue
            dt = norm_date(it.get('published_date') or '')
            key = u.split('?')[0]
            if key in seen: continue
            seen.add(key)
            out.append({
                'date': dt or '2026-10-21',
                'vendor': vendor,
                'domain': classify_domain(blob),
                'dimension': '市场',
                'source_type': 'media',
                'title': title[:180],
                'url': u,
                'summary': (body[:450] or title)[:450],
                'edn_link': 'S1',
                'recovered': True,
                'raw_file': os.path.basename(p),
            })
    print(f'RECOVERED {len(out)} from {len(files)} raw files', file=sys.stderr)
    json.dump(out, open('/tmp/edn-salvage/evidence.json', 'w'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    os.makedirs('/tmp/edn-salvage', exist_ok=True)
    main()
