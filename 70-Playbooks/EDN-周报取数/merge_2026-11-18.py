#!/usr/bin/env python3
"""Merge all evidence sources into one canonical list for the EDN weekly report."""
import json, re, os, glob

WIN_LO, WIN_HI = "2026-11-11", "2026-11-18"
out = []

# 1. subagent A evidence (structured)
p = '/tmp/edn-west/evidence_west_a.json'
if os.path.exists(p):
    for r in json.load(open(p)):
        out.append({'date': r['date'], 'vendor': r['vendor'], 'domain': r['domain'],
                    'source_type': r['source_type'], 'title': r['title'], 'url': r['url'],
                    'summary': r['summary'], 'confidence': r['confidence'], 'origin': 'subagent_A'})

# 2. subagent B evidence (structured) if it landed
for p in glob.glob('/tmp/edn-north/evidence*.json'):
    try: rows = json.load(open(p))
    except Exception: continue
    if isinstance(rows, dict): rows = rows.get('evidence', [])
    for r in rows:
        if not isinstance(r, dict): continue
        out.append({'date': r.get('date'), 'vendor': r.get('vendor','Cross-vendor'),
                    'domain': r.get('domain',''), 'source_type': r.get('source_type',''),
                    'title': r.get('title',''), 'url': r.get('url',''), 'summary': r.get('summary',''),
                    'confidence': r.get('confidence','H2'), 'origin': 'subagent_B'})

# 3. mother-agent harvested primary rows
ev = json.load(open('/tmp/edn-evidence.json'))
PRIMARY = ['blogs.cisco.com','investor.cisco','cisco.com','hpe.com','arubanetworking','juniper.net',
 'arista.com','blogs.arista','extremenetworks','fortinet.com','docs.fortinet','community.fortinet',
 'community.hpe','zscaler.com','paloaltonetworks.com','unit42.paloaltonetworks','live.paloaltonetworks',
 'nilesecure','huawei.com','h3c.com','businesswire','prnewswire','siliconangle','networkworld','crn.com',
 'techaisle','voicendata','convergedigest','lightreading','servethehome','techtarget','fiercenetwork',
 'sdxcentral','infosecurity-magazine','securityweek','storagenewsletter','developingtelecoms',
 'itbusinessdigest','helpnetsecurity','quantumcomputingreport','wifinowglobal','cybersecurityasia',
 'thefastmode','qz.com','fortune.com','streetinsider','marketscreener','dataconsultant','itential.com',
 'delloro.com','nokia.com','kalkine.com','tomshardware','ip-insider','startup.ph','duo.com',
 'cxotoday','businessmirror','theglobeandmail','itwire','cybersecurityinstitute','lexology',
 'fool.com','gartner.com','nilesecure.com','nokia','ip-insider.de','tomshardware','mind.ad']
seen = set()
for o in ev['window']:
    u = o['url']
    if u in seen: continue
    if not any(k in u.lower() for k in PRIMARY): continue
    seen.add(u)
    out.append({'date': o['date'], 'vendor': ', '.join(o['vendors']) or 'Cross-vendor',
                'domain': ', '.join(o['domains']), 'source_type': '官方/媒体',
                'title': o['title'], 'url': u, 'summary': o['summary'][:400],
                'confidence': 'H1' if any(k in u.lower() for k in ['blogs.cisco','investor.cisco','cisco.com','hpe.com',
                    'arista.com','fortinet.com','zscaler.com','paloaltonetworks.com','unit42','nilesecure','huawei.com',
                    'h3c.com','businesswire','prnewswire','itential.com','tomshardware']) else 'H2',
                'origin': 'mother_pool'})

# 4. X signals (hand-curated, 5 max)
X = [
 {"handle":"@IntCyberDigest","post_id":"2122773264908931084",
  "url":"https://x.com/IntCyberDigest/status/2122773264908931084","timestamp":"2026-11-17T19:26:00Z",
  "text":"CODE BLUE 2026: 被入侵笔记本可通过复制会话、导出证书、伪造设备健康检查，在 Cisco / Palo Alto / Zscaler / Netskope 的 VPN 中取得受信任设备状态；TPM 只阻止密钥被复制，不阻止其被使用。GMO Flatt Security 181 天扫 19.2M 开源包，31840 个恶意包；LiteLLM（~1亿月下载）劫持源于 5 月泄漏且未吊销的 admin key。",
  "metrics":{"likes":None,"retweets":None,"replies":None,"views":12800},
  "relevance_score":5,"edn_link":"S3/S6/身份-NAC","source_type":"official-social"},
 {"handle":"@Fortinet","post_id":"2120969943059493175",
  "url":"https://x.com/Fortinet/status/2120969943059493175","timestamp":"2026-11-12T20:00:00Z",
  "text":"Digital sovereignty is moving from policy discussion to security architecture. Is your SASE strategy ready for that shift? 联合 TheFuturumGroup 发布数字主权白皮书，强调按司法辖区构建安全架构。",
  "metrics":{"likes":None,"retweets":None,"replies":None,"views":1347},
  "relevance_score":3,"edn_link":"S2/S5/新兴架构","source_type":"official-social"},
 {"handle":"@PaloAltoNtwks","post_id":"2120567480389349818",
  "url":"https://x.com/PaloAltoNtwks/status/2120567480389349818","timestamp":"2026-11-11T17:21:00Z",
  "text":"How did a single developer laptop lead to Binance's $6.3B heist? 攻击者未破解密码学，而是使用投毒依赖、凭据窃取与内部 AI 工具。集成防御在攻击链到达金库前阻断——指向 Palo Alto 官方安全运营博客。",
  "metrics":{"likes":None,"retweets":None,"replies":None,"views":1638},
  "relevance_score":4,"edn_link":"S2/S6/Agentic Ops","source_type":"official-social"},
 {"handle":"@helpnetsecurity","post_id":"2120894389455044862",
  "url":"https://x.com/helpnetsecurity/status/2120894389455044862","timestamp":"2026-11-12T15:00:00Z",
  "text":"Attackers breached 10 organizations with an open-source AI pentest framework — 引用 Palo Alto Networks，与 Unit 42 的 Cairn 报告相互印证。",
  "metrics":{"likes":None,"retweets":None,"replies":None,"views":473},
  "relevance_score":4,"edn_link":"S2/Agentic Ops","source_type":"official-social"},
 {"handle":"@Cisco","post_id":"2120992367398236245",
  "url":"https://x.com/Cisco/status/2120992367398236245","timestamp":"2026-11-12T21:29:00Z",
  "text":"Tune into our $CSCO Q1FY27 Earnings Call. Watch live here.（Q1FY27 营收 185 亿美元 +24%，FY27 AI 基础设施营收指引上调至 90 亿美元）",
  "metrics":{"likes":None,"retweets":None,"replies":None,"views":7423},
  "relevance_score":4,"edn_link":"S1/Agentic Ops","source_type":"official-social"},
]

# 5. YouTube signals (10 max, transcript excerpts recovered from Tavily content field)
YT = [
 {"vid":"7w0YFpz1GYA","url":"https://www.youtube.com/watch?v=7w0YFpz1GYA","channel":"HPE","date":"2026-11-11",
  "title":"Reimagining SONiC to Power AI at Scale","views":240,"likes":2,"lang":"en",
  "relevance_score":5,"edn_link":"S1/Silicon-芯片生态",
  "excerpt":"SONiC adoption is accelerating in AI infrastructure... Network congestion silently kills GPU utilization. Poor observability leaves teams flying blind. And human error, responsible for over half of all outages, keeps your best engineers stuck firefighting instead of building. ... Scale out on key QFX switches based on Broadcom Tomahawk and Trident ASIC. And scale across on PTX routers for DCI.",
  "source_type":"official-video"},
 {"vid":"cJ5xTUWLCoE","url":"https://www.youtube.com/watch?v=cJ5xTUWLCoE","channel":"Vamaze Tech","date":"2026-11-17",
  "title":"Cisco Live 2026 Melbourne: Every AI Networking Announcement Explained","views":None,"likes":None,"lang":"en",
  "relevance_score":4,"edn_link":"S1/Agentic Ops",
  "excerpt":"Cisco's keynote at Cisco Live in Melbourne titled Lead in the Agentic era landed on November 10th local time... Cisco now pitches one stack silicon 1 chips and optics at the bottom, Nexus and 8,000 systems above the secure AI factory with Nvidia on top of that... Cisco also announced new MCP servers for its networking platforms, giving AI agents standardized access to network intelligence across cloud and on-prem.",
  "source_type":"media-video"},
 {"vid":"9JuTe8NNSds","url":"https://www.youtube.com/watch?v=9JuTe8NNSds","channel":"TelecomTV","date":"2026-11-13",
  "title":"Swisscom on its approach to network autonomy","views":18,"likes":0,"lang":"en",
  "relevance_score":4,"edn_link":"Agentic Ops",
  "excerpt":"At the Ericsson OSS/BSS Summit 2026 Mark Düsener, CTIO, Swisscom discusses building true agentic autonomous network loops while mastering decoupled architectures and cognitive autonomy.",
  "source_type":"media-video"},
 {"vid":"5PkBYAy9MhI","url":"https://www.youtube.com/watch?v=5PkBYAy9MhI","channel":"TelecomTV","date":"2026-11-11",
  "title":"From rApps to autonomous networks – making open ecosystems work","views":525,"likes":None,"lang":"en",
  "relevance_score":4,"edn_link":"Agentic Ops/新兴架构",
  "excerpt":"Featuring: Gustavo Hylander, EIAP Ecosystem Strategic Product Manager, Ericsson; Marcin Hoffmann, Technical Solutions Manager, Rimedo Labs; Nathan Romero, Technical Lead, Future Connections; Pierre Ouellette, Strategic Product Manager, Ericsson; Ramesh Sriraman, Chief Architect, HCL.",
  "source_type":"media-video"},
 {"vid":"0dK__zQmEhc","url":"https://www.youtube.com/watch?v=0dK__zQmEhc","channel":"Acclivity Labs","date":"2026-11-11",
  "title":"Acclivity Labs Juniper: Your Junos network, explained in plain English","views":1,"likes":0,"lang":"en",
  "relevance_score":3,"edn_link":"S1",
  "excerpt":"Welcome to Juniper, the AI agent built specifically for Juno's OS environments. Whether you are troubleshooting a firewall policy, auditing configs before a compliance review, or planning a fabric change, Juniper gives you precise deployment ready answers without digging through vendor documentation.",
  "source_type":"third-party-video"},
 {"vid":"L5JOBu22jgw","url":"https://www.youtube.com/watch?v=L5JOBu22jgw","channel":"NetPilot","date":"2026-11-17",
  "title":"I Tested an EVPN VXLAN Fabric Design Before Building It (Arista, Nokia, Cisco)","views":None,"likes":None,"lang":"en",
  "relevance_score":3,"edn_link":"S1",
  "excerpt":"You can test an EVPN VXLAN fabric design on real routers before you build it. AI builds it on real Arista, Nokia and Cisco, checks every claim on each device's CLI, and takes a spine down to prove it. In minutes. And this run found something. With one spine down, the hosts lost traffic for eight and a half seconds.",
  "source_type":"third-party-video"},
 {"vid":"RSbXFoUDr98","url":"https://www.youtube.com/watch?v=RSbXFoUDr98","channel":"NetPilot","date":"2026-11-12",
  "title":"ChatGPT Can Now Build Real Network Labs: Cisco, Arista, Junos","views":8,"likes":2,"lang":"en",
  "relevance_score":3,"edn_link":"S1/Agentic Ops",
  "excerpt":"ChatGPT can now build real network labs. Describe any network you want, in plain words. It designs the topology, writes the config for every vendor, checks it on the real device CLI, and hands you a running lab.",
  "source_type":"third-party-video"},
 {"vid":"z3BrGKZ6OAg","url":"https://www.youtube.com/watch?v=z3BrGKZ6OAg","channel":"TelecomReviewTV","date":"2026-11-12",
  "title":"From Digital Transformation to AI: Fortinet Explains Why Security Must Scale","views":21,"likes":None,"lang":"en",
  "relevance_score":4,"edn_link":"S2/Agentic Ops",
  "excerpt":"During the 20th Telecom Review Leaders' Summit, Ahmad Issa, Regional Sales Director, Middle East, Fortinet, explored the company's evolving approach to cybersecurity as organizations move beyond individual solutions toward integrated, scalable platform... Um no [...]",
  "source_type":"media-video"},
 {"vid":"SX5bmi-k0qE","url":"https://www.youtube.com/watch?v=SX5bmi-k0qE","channel":"Palo Alto Networks","date":"2026-11-17",
  "title":"What Is Agentic Endpoint Security? How AI Agents Bypass EDR","views":None,"likes":None,"lang":"en",
  "relevance_score":4,"edn_link":"S6/S2",
  "excerpt":"And that's why Palo Alto Networks integrated Cortex AES into Cortex XDR and Prisma AIRS to allow organizations to embrace the next generation of AI tools today with absolute confidence and zero compromise.",
  "source_type":"official-video"},
 {"vid":"r_01Cyqmq30","url":"https://www.youtube.com/watch?v=r_01Cyqmq30","channel":"Huawei Network","date":"2026-11-17",
  "title":"Authoritative Insights! Huawei has been named a Leader in the 2026 Forrester Wave™","views":None,"likes":None,"lang":"en",
  "relevance_score":4,"edn_link":"S1/Agentic Ops",
  "excerpt":"Join Muhammad Badar Farooq, CTO of Data Center Network for Huawei Middle East and Central Asia Regions, as we explore the newly upgraded Stellar AI Fabric 2.0 solution.",
  "source_type":"official-video"},
]

# dedupe evidence by url
final = []
seen2 = set()
for e in out:
    if not e['url']: continue
    if e['url'] in seen2: continue
    seen2.add(e['url'])
    final.append(e)

json.dump({'evidence': final, 'x_signals': X, 'youtube_signals': YT},
          open('/tmp/edn-final.json','w'), ensure_ascii=False, indent=1)

win = [e for e in final if e['date'] and WIN_LO <= e['date'] <= WIN_HI]
vc = {}
for e in win:
    for v in e['vendor'].split(', '): vc[v] = vc.get(v,0)+1
cc = {}
for e in win: cc[e['confidence']] = cc.get(e['confidence'],0)+1
print('total evidence:', len(final), '| windowed:', len(win), '| no-date:', len(final)-len(win))
print('vendor coverage:', dict(sorted(vc.items(), key=lambda kv:-kv[1])))
print('confidence:', cc)
print('x_signals:', len(X), '| youtube:', len(YT))
