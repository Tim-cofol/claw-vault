#!/usr/bin/env python3
"""Build the EDN evidence table from the harvested raw pool.
Filters out noise (jobs, stock chatter, social media, knowledge cards, PDF datasheets
that are product spec sheets with no strategic signal) and emits a clean evidence list.
"""
import json, re, os, sys

d = json.load(open('/tmp/edn-harvest.json'))
allitems = d['all']

NOISE_HOST = ['linkedin.com/jobs','remoteok.com','jobtoday','glassdoor','indeed.com','monster.com',
              'ziprecruiter','facebook.com','instagram.com','twitter.com','x.com','tiktok.com',
              'tavily.com/knowledge','moomoo','stockanalysis.com','tradingview.com','investing.com/equities',
              'youtube.com','reddit.com','amazon.com','ebay','alibaba','olx','upwork','builtin.com',
              'fiverr','freelancer','coursera','udemy','medium.com','wordpress','weebly','scribd',
              'pdfcoffee','slideshare','quizlet','coursehero','indeed','payscale','glassdoor',
              'jobgether','euremotejobs','builtin','startup.jobs','greenhouse.io','lever.co','ashbyhq',
              'icouldbenanything','seekingalpha','fintel','benzinga','marketbeat','simplywall.st',
              'tickeron','tipranks','stocktitan','wallstreetzen','macrotrends','stocktwits','investors.com',
              'hellenicshippingnews','lightreading.com/ai-machine-learning','thefastmode','vantage',
              'conference-series','speakerhub','allconferencealert','conferenceindex','ieeexplore',
              'worldconferencecalendar','researchgate','academia.edu','semanticscholar','arxiv',
              'noaa','weather','nasa','spacex','wikiwand','wikipedia','imdb','spotify','netflix',
              'ebay','walmart','target','costco','ikea','bestbuy','homedepot','lowes','wayfair']
NOISE_TITLE = [
    r'stock analysis', r'exam prep', r'practice questions', r'how to install', r'webinar: bringing ai',
    r'ai and games conference', r'high school', r'internship', r'income trades', r'job',
    r'vacancy', r'career', r'salary', r'interview questions', r'what is a ', r'\bfree download\b',
    r'coupon', r'discount', r'black friday', r'\bdeals\b', r'watch online', r'full movie', r'episode',
    r'lyrics', r'recipe', r'newsletter', r'webinar replay', r'podcast episode',
    r'\bdonate\b', r'merch', r'shop ', r'order status', r'return policy', r'used car', r'house for sale',
    r'apartment', r'\bhoroscope\b', r'\brecipe\b', r'\bmom\b', r'\bfitness\b', r'\bdating\b',
]
BAD_HOST_PART = ['/jobs/', '/careers/', '/salary', '/pinterest', '/quora.com', '/quizz', '/exam',
                 '/practice', '/questions', '/certification', '/training/course']

def noisy(it):
    u = it['url'].lower()
    t = (it['title'] or '').lower()
    for h in NOISE_HOST:
        if h in u: return True
    for b in BAD_HOST_PART:
        if b in u: return True
    for pat in NOISE_TITLE:
        if re.search(pat, t): return True
    if u.endswith('.pdf') and 'whitepaper' not in t and 'datasheet' not in t: return True
    return False

VENDOR_PATTERNS = {
 'Cisco': [r'cisco'],
 'HPE Aruba': [r'hpe', r'aruba', r'mist', r'juniper'],
 'Juniper Mist': [r'juniper', r'\bmist\b', r'marvis'],
 'Arista': [r'arista', r'etherlink'],
 'Extreme Networks': [r'extreme networks'],
 'Fortinet': [r'fortinet', r'fortigate', r'fortios', r'forti'],
 'Huawei': [r'huawei', r'华为'],
 'H3C': [r'h3c', r'新华三'],
 'Zscaler': [r'zscaler'],
 'Palo Alto Networks': [r'palo alto', r'panw', r'paloaltonetworks', r'unit 42', r'cortex'],
 'Nile': [r'nilesecure', r'\bnile\b'],
 'Arista/Comtel': [r'cornelis'],
 'Cribl': [r'cribl'],
 'Nokia': [r'nokia'],
 'Cross-vendor': [r'dell[\'’]?o', r'gartner', r'forrester', r'idc\b', r'omdia', r'light reading',
                  r'converge digest', r'securityweek', r'infosecurity', r'google threat', r'gtig'],
}

DOMAIN_PATTERNS = {
 'Agentic Ops': [r'agentic', r'ai ops', r'aiops', r'slingshot', r'self-driving', r'self driving',
                 r'autonomous (network|operation|ops)', r'agent one', r'mcp\b', r'marvis'],
 'Zero Trust-SASE': [r'sase', r'sse\b', r'zero trust', r'pra\b', r'fortisase', r'zscaler'],
 'Observability': [r'observab', r'telemetry', r'thousandeyes', r'cribl', r'cisco iq', r'splunk'],
 'SD-WAN': [r'sd-wan', r'sdwan', r'branches?', r'wan\b', r'sd-branch', r'sd branch'],
 'Campus Fabric': [r'campus', r'cnaas', r'lan-as-a-utility', r'wifi', r'wi-fi', r'wireless'],
 'NaaS': [r'naas', r'network as a service', r'lan-as-a-utility'],
 'DEX-DEM': [r'\bdex\b', r'digital experience management', r'\bdem\b', r'experience management'],
 'Security-Network': [r'security framework', r'sase', r'zero trust', r'secure ai', r'ai defense',
                       r'firewall', r'\bpqc\b', r'post-quantum', r'pass-the-device'],
 'Digital Twin': [r'digital twin'],
 'Strategy编排': [r'policy', r'orchestrat', r'playbook', r'security service chain', r'service chain'],
 'Telemetry-Data Platform': [r'telemetry', r'data fabric', r'data platform', r'context memory'],
 'Silicon-芯片生态': [r'silicon one', r'tomahawk', r'trident', r'5nm', r'asic', r'optical', r'800g',
                     r'1\.6t', r'scale-up', r'scale across', r'scale-out'],
 'Ethernet-交换标准': [r'ethernet', r'roce', r'ultra ethernet', r'ieee', r'802\.', r'switch'],
 '身份-NAC': [r'\bnac\b', r'\bidentity', r'zero trust access', r'device trust', r'certificate'],
 '新兴架构': [r'multicloud', r'agentic mesh', r'mesh', r'sovereign', r'digital sovereignty'],
 'AI 安全对抗': [r'cairn', r'artex', r'pentagi', r'offensive framework', r'vulnerability discovery',
                 r'ai pentest', r'fully autonomous attack'],
}

def classify(it):
    blob = (it['title'] or '') + ' ' + (it['content'] or '')[:1500] + ' ' + it['url']
    vendors = [v for v, pats in VENDOR_PATTERNS.items()
               if any(re.search(p, blob, re.I) for p in pats)]
    domains = [dm for dm, pats in DOMAIN_PATTERNS.items()
               if any(re.search(p, blob, re.I) for p in pats)]
    return vendors, domains

out = []
for it in allitems:
    if noisy(it): continue
    if it['date'] is None and len(it['content']) < 400: continue
    v, dm = classify(it)
    if not v and not dm: continue
    # extract a compact summary from content
    c = re.sub(r'\s+', ' ', it['content']).strip()
    out.append({
        'date': it['date'],
        'title': (it['title'] or '')[:200],
        'url': it['url'],
        'vendors': v, 'domains': dm,
        'summary': c[:420],
        'src': it['src_file'],
    })

# windowed subset = the core evidence
win = [o for o in out if o['date'] and '2026-11-11' <= o['date'] <= '2026-11-18']
# none-dated but substantive: keep separately (needs page-date confirmation)
nodate = [o for o in out if not o['date']]
json.dump({'window': win, 'nodate': nodate, 'all': out},
          open('/tmp/edn-evidence.json', 'w'), ensure_ascii=False, indent=1)
print('window evidence:', len(win))
print('no-date substantive:', len(nodate))
vs = {}
for o in win:
    for v in o['vendors']: vs[v] = vs.get(v, 0) + 1
print('vendor coverage (window):', dict(sorted(vs.items(), key=lambda kv: -kv[1])))
ds = {}
for o in win:
    for dm in o['domains']: ds[dm] = ds.get(dm, 0) + 1
print('domain coverage (window):', dict(sorted(ds.items(), key=lambda kv: -kv[1])))
