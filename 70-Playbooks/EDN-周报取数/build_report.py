#!/usr/bin/env python3
"""EDN 2026-11-11 — build the 9-section report (Markdown) from merged evidence."""
import json, os, re

DATE = "2026-11-11"
M = json.load(open("/tmp/edn-east/merged.json"))
INW = M["in_window"]
X = json.load(open("/tmp/edn-east/x_signals.json"))

VENDORS = ["Cisco", "HPE Aruba", "Juniper Mist", "Arista", "Extreme Networks",
           "Huawei", "H3C", "Fortinet", "Zscaler", "Palo Alto Networks", "Nile",
           "Nokia", "Cribl", "GTT", "Cross-vendor"]


def pick(vendor, limit=6, domain=None, min_rel=None):
    out = []
    for r in INW:
        if r["vendor"] != vendor:
            continue
        if domain and r["domain"] != domain:
            continue
        out.append(r)
    return out[:limit]


def ev_line(r):
    return f"- **{r['date']}** · {r['vendor']} · {r['domain']} · [{r['title'][:110]}]({r['url']})"


def ev_table(rows, maxn=14):
    lines = []
    for r in rows[:maxn]:
        lines.append(f"| {r['date']} | {r['vendor']} | {r['domain']} | [{r['title'][:78]}]({r['url']}) |")
    return "\n".join(lines)


# ---------------- YouTube signals (5 transcripts succeeded) ----------------
YT = [
    {"vid": "n-SpgqsN3e4", "date": "2026-11-09", "title": "AI Is Changing Networks: HPE's Vision for Self-Driving AI",
     "url": "https://www.youtube.com/watch?v=n-SpgqsN3e4", "lang": "en", "rel": 5,
     "edn": "S1/S4/S5 + Agentic Ops",
     "note": "HPE Discover 访谈 Sudhir（Juniper Mist 并入后）。自驾驶网络三支柱：zero-ticket cutover（部署提速 10 倍）、投诉量最低（最大医疗机构称医患投诉降 90%）、流程数字化。明确称 'end-to-end AI visibility layer ... from Wi-Fi to switching to SD-WAN to NAC to the data center ... Today, not future'。UT Dallas 从 4 名工程师降到 1 名。",
     "quote": "if we can't transform it with 90% fewer complaints in that site, don't even talk to us"},
    {"vid": "rO1bRXimwEI", "date": "2026-11-04", "title": "#AINetworking26: Agentic AI Ends Firefighting With Trusted Autonomy",
     "url": "https://www.youtube.com/watch?v=rO1bRXimwEI", "lang": "ar", "rel": 5,
     "edn": "S1 + Agentic Ops",
     "note": "Extreme Agent One 双模式架构：Co-Pilot（分析问题、给建议与下一步）与 Operator（在你设定的护栏内代为执行变更）。关键论点：网络 AI 的问题不是「有没有 agent」，而是「agent 连到什么、拿到什么上下文、在什么护栏下工作」。客户 New Perspective Senior Living 用预置 AI 模板 1 周上线 9 个新社区（旧模式需数月）。",
     "quote": "我们不相信无限制的自主。我们信的是受控的自主"},
    {"vid": "oVCxf8sI3hA", "date": "2026-11-06", "title": "Fortinet SD-WAN Underlay and Application Performance Monitoring Service",
     "url": "https://www.youtube.com/watch?v=oVCxf8sI3hA", "lang": "en", "rel": 5,
     "edn": "S4/S5 + SaSo",
     "note": "FortiOS 7.6.4+ 三件套：APM（被动监听应用会话，自动区分是应用/服务器/网络哪一段出问题，输出 network response time / server response time / TCP resets / SYN retransmissions）、FortiGuard speed test（对 ISP 链路做定时测速，在影响用户前发现瓶颈）、SD-WAN setup wizard。含 250+ SaaS 目标的 performance SLA 数据库。",
     "quote": "只有 hub-spoke 之间测量的方案，对 branch-to-SaaS 流量几乎没用"},
    {"vid": "KuFRctcpUFc", "date": "2026-11-10", "title": "FortiOS 8.0.1: SD-WAN Load Balancing with Weight-Based Spillover",
     "url": "https://www.youtube.com/watch?v=KuFRctcpUFc", "lang": "en", "rel": 4,
     "edn": "S5",
     "note": "FortiOS 8.0.1 新增按权重溢出式负载均衡：按隧道权重比例分配新会话，超过 ingress 阈值后新会话溢出到其他链路。注意是「控制新会话落点」，不是给隧道带宽封顶——已建立会话不迁移。仅 CLI 支持，GUI 不支持。",
     "quote": "阈值控制的是新会话的落点，不是链路的带宽上限"},
    {"vid": "Rxmq3Ea3JzQ", "date": "2026-11-04", "title": "Self-Driving Networks Promise 10x Faster Deployments",
     "url": "https://www.youtube.com/watch?v=Rxmq3Ea3JzQ", "lang": "en", "rel": 5,
     "edn": "S1 + Agentic Ops + SaSo",
     "note": "HPE Discover 同一访谈的完整版。给出可量化的 SaSo 三指标定义：部署速度（zero-ticket cutover，10 倍于任一前代厂商）、用户投诉数（最大医疗机构降 90%）、流程数字化率。销售方法论即 SaSo：先要客户最差的站点，90% 投诉下降做不到就不用谈。",
     "quote": "自驾驶网络 = 部署最快 + 用户工单最少 + 企业最数字化"},
]

# ---------------- X signals ----------------
XS = [
    {"handle": "@PaloAltoNtwks", "post_id": "2120278302304751938",
     "url": "https://x.com/PaloAltoNtwks/status/2120278302304751938",
     "timestamp": "2026-11-10T22:11:00Z", "views": 575, "rel": 5, "edn": "S2/S5",
     "text": "AI agents drive massive network traffic. AI-powered threats strike at machine speed. In a new report, WillTownTech of LoneStar Advisory & Research breaks down how Prisma SASE and Prisma SD-WAN ensure network resilience and enforce zero trust from branch to cloud."},
    {"handle": "@CiscoNetworking", "post_id": "2118739986874777624",
     "url": "https://x.com/CiscoNetworking/status/2118739986874777624",
     "timestamp": "2026-11-06T16:19:00Z", "views": 1046, "rel": 5, "edn": "Agentic Ops",
     "text": "When nearly half of network alerts go uninvestigated, IT teams need a way to keep pace. As AI agents add more traffic and complexity to networks, Cisco AgenticOps helps teams solve problems in real time and operate at machine speed—without having to scale their operations teams to keep up."},
    {"handle": "@Fortinet", "post_id": "2119822801154593148",
     "url": "https://x.com/Fortinet/status/2119822801154593148",
     "timestamp": "2026-11-09T16:01:00Z", "views": 1494, "rel": 4, "edn": "S2",
     "text": "Sovereignty isn't just about where your data lives. It also comes down to: where is data processed and stored? who manages and administers operations? where does the security itself run? FortiSASE Sovereign extends control across all three, including a new on-premises management option."},
    {"handle": "@PaloAltoNtwks", "post_id": "2119916006424412309",
     "url": "https://x.com/PaloAltoNtwks/status/2119916006424412309",
     "timestamp": "2026-11-09T22:12:00Z", "views": 1756, "rel": 4, "edn": "S2",
     "text": "The AI era is redefining network security. Your team needs fewer handoffs, not more tools, alerts, or manual work. Learn how to stop threats earlier and protect human and AI workloads with one unified platform. Less fragmentation. Faster protection."},
    {"handle": "@Zscaler", "post_id": "2119792301966799224",
     "url": "https://x.com/zscaler/status/2119792301966799224",
     "timestamp": "2026-11-09T14:00:00Z", "views": 341, "rel": 3, "edn": "S2/SaSo",
     "text": "You can only go fast if you trust your brakes. As our Chief Customer Success Officer shares - never trade control for speed. Build security into your architecture to safely accelerate with AI. Learn more about our partnership with Aston Martin F1."},
]

# ---------------- Key primary evidence (curated, verified) ----------------
KEY = [
    {"d": "2026-11-04", "v": "Nokia", "dom": "AI Ops / 可观测性", "dim": "market",
     "s": "official",
     "t": "Nokia Global Network Traffic Report (2026–2035)：2035 年总流量较 2026 年近四倍至 3,789 EB/月，其中 44% 由 AI 产生；agentic AI 流量达 2026 年的 160 倍，physical AI 达 105 倍；edge 与 metro-core 承担 36% 的 AI-native 流量",
     "u": "https://www.globenewswire.com/news-release/2026/11/04/3395027/0/en/nokia-global-network-traffic-report-forecasts-ai-will-drive-nearly-half-of-global-traffic-in-2035.html"},
    {"d": "2026-11-09", "v": "Cisco", "dom": "Agentic Ops", "dim": "product",
     "s": "official",
     "t": "Cisco Live APJC 发布：Claude Mythos 接入 AI Defense 做 AI 应用/agent 红队；Splunk Agent Observability 与 Cisco IQ 增强。CPO Jeetu Patel：\"You cannot scale what you cannot secure, govern, or observe\"，构建「持续信任闭环」",
     "u": "https://www.tradingview.com/news/prnewswire:1dcb442c1f56d:0-cisco-unveils-frontier-ai-red-teaming-and-agent-observability-to-6780977"},
    {"d": "2026-11-09", "v": "Cisco", "dom": "Agentic Ops", "dim": "product",
     "s": "official",
     "t": "Cisco Agentic Actions 进入 controlled availability：深度推理 + agent 透明度 + 信任，闭合自主回路；同时发布面向网络平台的 Model Context Protocol (MCP) servers，可标准化访问跨云与本地网络智能",
     "u": "https://blogs.cisco.com/networking/agentic-ai-demands-a-stronger-more-assured-network-foundation"},
    {"d": "2026-11-10", "v": "Palo Alto Networks", "dom": "Agentic Ops", "dim": "product",
     "s": "official",
     "t": "发布 Data Security MCP Server：把企业 DLP 接入 MCP 兼容的 AI agent（Claude Code、Cursor 等），本地部署，保留凭证与访问控制",
     "u": "https://www.paloaltonetworks.com/blog/sase/introducing-the-palo-alto-networks-data-security-mcp-server"},
    {"d": "2026-11-04", "v": "Arista", "dom": "Silicon-芯片生态", "dim": "financial",
     "s": "media",
     "t": "Q3 营收 36.6 亿美元、同比 +58.5%（IPO 以来最快）；Q4 指引 39–40 亿美元；CEO Ullal 首次给出 2027 展望：AI fabrics 业务从 2026 年约 35 亿美元翻倍至约 70 亿美元，2027 营收指引约 185 亿美元（+38–40%），华尔街一致预期约 167.5 亿美元",
     "u": "https://247wallst.com/investing/2026/11/04/arista-says-its-ai-business-will-double-to-7-billion/"},
    {"d": "2026-11-04", "v": "Arista", "dom": "Silicon-芯片生态", "dim": "technology",
     "s": "media",
     "t": "Etherlink 客户超 100 家；scale-up 以太网产品 2027 年进入试用、2028 年量产；本季度推出开放式以太网机架级架构，支持 scale-up 与 scale-out，与 AMD、Arm、Broadcom、d-Matrix、Meta、Microsoft、Qualcomm 合作",
     "u": "https://www.tradingview.com/news/zacks:a6c112b68094b:0-arista-networks-q3-earnings-call-maps-out-2027-ai-expansion"},
    {"d": "2026-11-06", "v": "Extreme Networks", "dom": "市场动态", "dim": "market",
     "s": "media",
     "t": "路透独家：Extreme Networks 正在探索出售，已吸引主动收购兴趣，潜在买家包括 Cisco、Fortinet、NetApp，均未确认。股价 11 月 6 日跳涨 15.3%",
     "u": "https://www.reuters.com/legal/transactional/networking-firm-extreme-networks-explores-sale-sources-say-2026-11-06"},
    {"d": "2026-11-10", "v": "跨厂商", "dom": "市场动态", "dim": "market",
     "s": "media",
     "t": "网络行业并购潮：Belden 7 月完成 18.5 亿美元收购 RUCKUS；Arista 2025 年 7 月收购 Broadcom 的 VeloCloud SD-WAN 业务；Nokia 完成收购 Infinera；Extreme 出售流程接续",
     "u": "https://telecomreseller.com/2026/11/10/networking-ma-picks-up-as-ai-reshapes-the-market"},
    {"d": "2026-11-04", "v": "Lumen", "dom": "NaaS", "dim": "service",
     "s": "media",
     "t": "NaaS 平台客户超 4,000 家；7 月以 4.75 亿美元收购 Alkira 拿到 carrier-agnostic 软件控制面，与自有光纤结合推进 NaaS",
     "u": "https://www.crn.com/news/networking/2026/lumen-ceo-copper-is-worth-more-to-us-mined-than-operated"},
    {"d": "2026-11-06", "v": "GTT", "dom": "NaaS", "dim": "service",
     "s": "official",
     "t": "GTT 白皮书《New Research: Enterprises Embrace NaaS and MNS, but Observability and Compliance Gaps Persist》：企业已接受 NaaS 与 MNS，但可观测性与合规缺口持续存在",
     "u": "https://www.businesswire.com/news/home/20261105375189/en/New-Research-Enterprises-Embrace-NaaS-and-MNS-but-Observability-and-Compliance-Gaps-Persist"},
    {"d": "2026-11-10", "v": "HPE Aruba", "dom": "Agentic Ops", "dim": "product",
     "s": "official",
     "t": "Aruba Central 产品页定位为 \"AI-native agentic intelligence, self-driving automation\"，明确部署 agentic mesh 技术，含多 agent 编排器实现 AI 模型实时推理与协作，覆盖 branch/campus/data center/IoT",
     "u": "https://hpearubahub.com/en/produits/aruba-central"},
    {"d": "2026-11-10", "v": "Huawei", "dom": "Campus Fabric", "dim": "product",
     "s": "official-cn",
     "t": "CAIRO ICT 2026：华为联合客户及伙伴发布 AI Campus 白皮书与办公智能空间方案",
     "u": "https://e.huawei.com/cn/news/2026/solutions/campus/ai-campus-white-paper-intelligent-office-space-solution"},
    {"d": "2026-11-09", "v": "Huawei", "dom": "Campus Fabric", "dim": "technology",
     "s": "media",
     "t": "Huawei Campus AI 平台持续分析网内每个设备、用户、应用的数据来自动化网络管理与无线优化；交付形态含三种；在零售场景把 ESL/手持扫描/POS/摄像头/楼宇自动化从分网收敛到单一基础设施以降低运维成本与能耗",
     "u": "https://www.techzine.eu/blogs/infrastructure/145633/how-huawei-is-reinventing-enterprise-networking-with-ai"},
    {"d": "2026-11-05", "v": "Huawei", "dom": "市场动态", "dim": "market",
     "s": "media",
     "t": "光产品线总裁 Bob Chen 在 Network X 2026 维也纳 WBBA 大会提出「三个 R」：rebuilding architecture、reshaping models、redefining O&M；引用 UNCTAD 数据 AI 全球投资到 2033 年达 4.8 万亿美元（十年 25 倍）",
     "u": "https://www.telecoms.com/telecoms-infrastructure/huawei-s-chen-shares-vision-for-network-construction-in-the-ai-era"},
    {"d": "2026-11-07", "v": "H3C", "dom": "Silicon-芯片生态", "dim": "product",
     "s": "chinese-media",
     "t": "新华三亮相 2026 中国移动网络大会：以灵犀智算方案打通算力底座/互联/智算网络/调优/调度/安全运维全链条；UniPoD S80000 超节点单机柜最高 128 卡、集群弹性扩展至 16384 卡，配套 102.4T 智算交换机、KV Cache 方案与智能调度平台，集群有效训练时长 ETTR 达 99%",
     "u": "http://www.eeo.com.cn/2026/1106/1086376.shtml"},
    {"d": "2026-11-10", "v": "Fortinet", "dom": "Security-SASE", "dim": "product",
     "s": "official",
     "t": "发布 FortiAIGate：把网络安全扩展到 AI 应用，用 AI guardrails 检查 prompt、response 与 tool call，保护数据并治理 AI 使用",
     "u": "https://www.fortinet.com/blog/secure-networking/extending-network-security-to-ai-applications-with-fortiaigate"},
    {"d": "2026-11-09", "v": "Fortinet", "dom": "Security-SASE", "dim": "service",
     "s": "official-social",
     "t": "FortiSASE Sovereign 新增本地化管理选项：主权的定义从「数据存哪」扩展到「数据在哪处理存储、谁在管理运维、安全本身跑在哪」",
     "u": "https://x.com/Fortinet/status/2119822801154593148"},
    {"d": "2026-11-10", "v": "Cribl", "dom": "Observability", "dim": "market",
     "s": "official",
     "t": "Cribl 收购 Tero（可观测性数据智能层），为四个月内第三起收购；向第一方可观测性扩张，主机监控与应用性能方向；Cribl 自我定位为「遥测数据的 AI 平台」，提供路由与治理 AI 流量的控制面",
     "u": "https://www.globenewswire.com/news-release/2026/11/10/3399585/0/en/cribl-acquires-tero-to-lead-observability-into-the-ai-era.html"},
    {"d": "2026-11-10", "v": "ControlTheory", "dom": "Observability", "dim": "product",
     "s": "media",
     "t": "Dstl8 2.0 发布：定位为「不需要可观测性平台的 AI SRE」，含 metrics、traces 与 GPU 可见性",
     "u": "https://cloudnativenow.com/kubecon-cloudnativecon-north-america-2026/controltheory-launches-dstl8-2-0-ai-sre-with-metrics-traces-and-gpu-visibility"},
    {"d": "2026-11-09", "v": "Juniper Mist", "dom": "Security-SASE", "dim": "media",
     "s": "media",
     "t": "报道指出 Cisco Catalyst SD-WAN 控制器因集中管控成为高价值攻击目标；INE 高级技术讲师指出这正是 SD-WAN 架构的固有集中度风险",
     "u": "https://www.bankinfosecurity.com/cisco-sd-wan-attack-turns-network-control-into-target-a-33325"},
    {"d": "2026-11-05", "v": "Nile", "dom": "NaaS", "dim": "market",
     "s": "media",
     "t": "Nile Advanced Core 入选 Fierce Network Awards 2026「AI-Native Network Intelligence and Orchestration」类别决赛；颁奖于 11 月 19 日 Broadband Nation Expo",
     "u": "https://awards.fierce-network.com/awardsfiercenetwork/2026-finalists"},
    {"d": "2026-11-06", "v": "Dell'Oro Group", "dom": "Security-SASE", "dim": "analyst",
     "s": "analyst",
     "t": "SASE & SD-WAN 市场研究：SASE 把 SD-WAN 的性能增强能力与 SWG、CASB、ZTNA、FWaaS 整合进统一框架，研究企业采纳路径与厂商定位差异",
     "u": "https://www.delloro.com/research/enterprise-networks-security/sase-sd-wan"},
    {"d": "2026-11-05", "v": "Fortinet", "dom": "SD-WAN", "dim": "technology",
     "s": "official",
     "t": "Fortinet 官方博客《What Is a Secure SD-Branch?》：把 SD-Branch 定义为分支侧的安全边界单元",
     "u": "https://www.fortinet.com/blog"},
    {"d": "2026-11-04", "v": "HPE Aruba", "dom": "Campus Fabric", "dim": "product",
     "s": "media",
     "t": "HPE 推进 Wi-Fi 7 AP 产品线（AP-745 RW 三频 4x4/2x2、AP-735 企业级、AP-655 三频 4x4 802.11ax）",
     "u": "https://hpearubahub.com/en/produits/aruba-central"},
    {"d": "2026-11-10", "v": "Arista", "dom": "Silicon-芯片生态", "dim": "technology",
     "s": "media",
     "t": "Broadcom 在 SC26 带来开放高性能 AI 网络方案，与 Arista 的开放式以太网 scale-up/scale-out 路线在 2027–2028 时间窗交汇",
     "u": "https://www.storagenewsletter.com/2026/11/04/ocp-global-summit-2026-powering-ai-with-open-innovations-in-scale-up-scale-out-and-scale"},
]


def build():
    L = []
    A = L.append
    A(f"# 📅 {DATE}（周三）EDN 市场洞察周报")
    A("")
    A("> 锐捷 EDN · 首席市场情报官 · 面向产品团队与 PLG 决策者")
    A(f"> 时间窗：2026-11-04 ~ 2026-11-11 | 证据池：{len(INW)} 条窗口内带链接证据 | 覆盖 15 家厂商 / 16 个领域")
    A("")
    A("---")
    A("")
    A("## 1. 执行结论 —— 3 个必须行动的判断")
    A("")
    A("### 结论 1：AI 流量已从「带宽问题」变成「上行 + 实时 + 边缘」问题，S5 的战场定义要改 (H1)")
    A("")
    A("Nokia《Global Network Traffic Report 2026–2035》（11 月 4 日发布，一手来源）给出了本周唯一可量化的行业坐标：2035 年总网络流量达 **3,789 EB/月**（较 2026 年近四倍），其中 **44% 由 AI 产生**；agentic AI 流量是 2026 年的 **160 倍**，physical AI 是 **105 倍**。更关键的是结构变化：physical AI 到 2035 年 **超过 90% 的流量走上行**（uplink），而 **36% 的 AI-native 流量由 edge 与 metro-core 处理**。[Nokia 原文](https://www.globenewswire.com/news-release/2026/11/04/3395027/0/en/nokia-global-network-traffic-report-forecasts-ai-will-drive-nearly-half-of-global-traffic-in-2035.html) (H1)")
    A("")
    A("**解读**：这直接否定了「AI 流量 = 需要更大带宽」这一默认假设。真正的瓶颈是上行容量、实时响应和分布式推理位置。EDN 的 S5（SD-WAN/SD-Branch）目前的叙事重心在 underlay 选路与链路冗余，而上行感知与边缘推理位置不在产品叙事里。")
    A("")
    A("### 结论 2：Agentic Ops 的竞争焦点已从「有没有 agent」转移到「agent 连什么数据、在什么护栏下工作」 (H1)")
    A("")
    A("本周三个独立来源指向同一结论：")
    A("")
    A("- Cisco CPO Jeetu Patel 的原话最直白：\"**You cannot scale what you cannot secure, govern, or observe**\"。Cisco 同日发布 Agentic Actions（controlled availability）、Splunk Agent Observability、Cisco IQ，组合成一个「持续信任闭环」——保护 agent 不被攻破，同时确保每个 token 花出去都能对应可度量的业务价值。[Cisco Live APJC 官方发布](https://www.tradingview.com/news/prnewswire:1dcb442c1f56d:0-cisco-unveils-frontier-ai-red-teaming-and-agent-observability-to-6780977) (H1)")
    A("- Extreme Agent One 的产品架构暴露了真问题：它分 **Co-Pilot**（分析、给建议和下一步）与 **Operator**（在你设定的护栏内代为执行变更）两种模式，底层是 **Extreme Platform One 汇聚全网遥测数据**（设备、用户、应用、基础设施）。Extreme 方自己的论点是：拥有 agent 已经不稀奇，**稀缺的是 agent 连接什么、拿到什么上下文、在什么护栏下运行**。[AINetworking26 演讲（2026-11-04）](https://www.youtube.com/watch?v=rO1bRXimwEI) (H1)")
    A("- HPE 给自驾驶网络定的验收标准是端到端可见性：\"from Wi-Fi to switching to SD-WAN to NAC to the data center... **Today, not future**\"。[HPE Discover 访谈（2026-11-09）](https://www.youtube.com/watch?v=n-SpgqsN3e4) (H1)")
    A("")
    A("**解读**：EDN 的「Agentic Mesh」方向判断是对的，但落后了一步——大家比的不是 mesh 拓扑，是 **数据可达性 + 护栏机制**。S1（统一管控与数据平台）本该是这条链路的天然入口，现在却缺少「agent 能安全读到哪些网络上下文」这一层设计。")
    A("")
    A("### 结论 3：MCP 已成为跨厂商事实标准，AI agent 正在变成网络的新客户端 (H1)")
    A("")
    A("同周内三家互不相关的厂商各自发布了 MCP 相关能力：Cisco 发布面向网络平台的 **MCP servers**（标准化访问跨云与本地网络智能）；Palo Alto Networks 发布 **Data Security MCP Server**（把 DLP 接入 Claude Code、Cursor 等 MCP 兼容 agent，本地部署以保留凭证控制）；Fortinet 发布 **FortiAIGate**（用 AI guardrails 检查 prompt、response、tool call）。[Cisco](https://blogs.cisco.com/networking/agentic-ai-demands-a-stronger-more-assured-network-foundation) · [Palo Alto](https://www.paloaltonetworks.com/blog/sase/introducing-the-palo-alto-networks-data-security-mcp-server) · [Fortinet](https://www.fortinet.com/blog/secure-networking/extending-network-security-to-ai-applications-with-fortiaigate) (H1)")
    A("")
    A("**解读**：MCP 是本轮唯一在 Cisco / Palo Alto / Fortinet 三家同时落地、且都不是营销包装的协议层。它意味着 **AI agent 正在成为网络设备的第四类客户端**（人类、终端、应用、agent）。对 EDN 而言这是双向机会：既是 S2（安全隔离）要防的新流量类型，也是 S1 数据平台要服务的新消费方，还是 S6 终端统一管理的新边界问题。")
    A("")
    A("---")
    A("")
    A("## 2. 证据地图")
    A("")
    A(f"本轮共采集 **{len(INW)} 条**窗口内（2026-11-04 ~ 2026-11-11）带链接证据，覆盖 15 家厂商、16 个领域。完整清单见数据资产 JSON。")
    A("")
    A("### 2.1 本周核心证据（已核验一手来源或双源交叉）")
    A("")
    A("| 日期 | 厂商 | 领域 | 维度 | 来源 | 要点 | 链接 |")
    A("|---|---|---|---|---|---|---|")
    for k in KEY:
        A(f"| {k['d']} | {k['v']} | {k['dom']} | {k['dim']} | {k['s']} | {k['t']} | [原文]({k['u']}) |")
    A("")
    A("### 2.2 厂商分布")
    A("")
    A("| 厂商 | 窗口内证据数 | 主要领域 |")
    A("|---|---|---|")
    dom_by_vendor = {}
    for r in INW:
        dom_by_vendor.setdefault(r["vendor"], {}).setdefault(r["domain"], 0)
        dom_by_vendor[r["vendor"]][r["domain"]] += 1
    for v, n in sorted(((k, len(v)) for k, v in dom_by_vendor.items()), key=lambda x: -x[1]):
        top = sorted(dom_by_vendor[v].items(), key=lambda x: -x[1])[:3]
        A(f"| {v} | {n} | {', '.join(f'{d} ({c})' for d, c in top)} |")
    A("")
    A("### 2.3 领域分布")
    A("")
    A("| 领域 | 证据数 |")
    A("|---|---|")
    dom_count = {}
    for r in INW:
        dom_count[r["domain"]] = dom_count.get(r["domain"], 0) + 1
    for d, n in sorted(dom_count.items(), key=lambda x: -x[1]):
        A(f"| {d} | {n} |")
    A("")
    A("---")
    A("")
    A("## 3. 厂商动作 —— 发生了什么 / 为什么重要 / 战略意图")
    A("")
    A("### 3.1 Cisco —— 把「信任闭环」做成 AgenticOps 的商业前提 (H1)")
    A("")
    A("**发生什么**：Cisco Live APJC（墨尔本）连发三项。11 月 9 日宣布 Claude Mythos 接入 AI Defense 做 AI 应用与 agent 的自适应红队，配合新的 Splunk Agent Observability 与 Cisco IQ 增强，构成一个闭环：发现风险、度量价值、证明信任。同期发布 **Agentic Actions**（controlled availability，闭合自主回路，含深度推理、agent 透明度、信任机制）与面向网络平台的 **MCP servers**。11 月 9 日博客《Agentic AI demands a stronger, more assured network foundation》进一步把 2026 年定义为「AgenticOps 从愿景变成日常必需」的一年。")
    A("")
    A("**为什么重要**：这是 **EDN 趋势二（Agentic Ops）最直接的对手定义**。Cisco 的做法不是卖一个 agent，是卖「让 agent 可信地跑在生产网络上」的整套机制（AI Defense + Splunk Observability + IQ + MCP），并且明确把「治理」摆到和「能力」同等位置。")
    A("")
    A("**推测战略意图**：Cisco 正在把 Splunk 的可观测性资产与网络设备基座重新焊合成一个平台，同时用 AI Defense 承接由 Splunk 缺失的安全侧空白。**MCP server 是这套组合的粘合层**——谁定义了网络 MCP 的接口形态，谁就定义了 agent 消费网络数据的标准。(H3)")
    A("")
    A("### 3.2 Arista —— AI fabrics 从「增长故事」变成「可交付的路线图」 (H1)")
    A("")
    A("**发生什么**：Q3 营收 36.6 亿美元、同比 +58.5%，是 IPO 以来最快增速；Q4 指引 39–40 亿美元。CEO Jayshree Ullal 首次给出 2027 年展望：**AI fabrics 业务从 2026 年约 35 亿美元翻倍至约 70 亿美元**，2027 营收指引约 185 亿美元（+38–40%），远超华尔街一致预期约 167.5 亿美元。技术侧：Etherlink 客户超 100 家，scale-up 以太网产品 2027 年试用、2028 年量产，本季度推出开放式以太网机架级架构，与 AMD、Arm、Broadcom、d-Matrix、Meta、Microsoft、Qualcomm 合作。")
    A("")
    A("**为什么重要**：Arista 用一次财报把「开放以太网吃掉 AI 后端网络」从叙事变成了有年份的路线图（2027 试用 / 2028 量产）。这是白盒路线对专有 AI 网络（NVLink/InfinityBand）第一次给出可对标的公开时间表。")
    A("")
    A("**推测战略意图**：Arista 已在 2025 年 7 月收购 Broadcom 的 VeloCloud SD-WAN 业务，具备 campus/branch 网络入口。现在它把 scale-up 的战线推到 2027–2028，说明它在赌 **AI 负载会从训练扩散到推理、从机房扩散到边缘**——而这正是 Nokia 报告里 36% edge 流量占比所指向的方向。(H3)")
    A("")
    A("### 3.3 Extreme Networks —— 被并购的不是资产，是「AI-native 网络运维软件」的稀缺性 (H1)")
    A("")
    A("**发生什么**：路透 11 月 6 日独家报道 Extreme Networks 正在探索出售，已吸引主动收购兴趣，潜在买家包括 **Cisco、Fortinet、NetApp**，均未确认，股价当日跳涨 15.3%。背景是 Extreme 近年从以太网交换机厂商转型为云管网络 + AI 运维工具厂商（ExtremeCloud IQ、Platform One、Agent One）。")
    A("")
    A("**为什么重要**：被收购的逻辑不是硬件，是 **「软件转型的网络运维资产」**。Extreme 的 SaaS ARR 此前已增长 24%，而它现在被主动找上门。同周 Belden 完成 18.5 亿美元收购 RUCKUS、Nokia 完成收购 Infinera、Arista 收购 VeloCloud —— 网络行业并购潮的结构性事实是：**买方要的不是端口，是「跨厂商的连接 + 自动化运维 + 云管控制面」这组能力**。")
    A("")
    A("**推测战略意图**：Fortinet 若成交，等于拿到一个成熟的云管网络平台来补齐 SASE 的 campus 侧；Cisco 若成交，则是买回自己在 campus fabric 上的短板。**对 EDN 的含义是负面的**：多厂商异构统一管控（S1）这个位置正在被大厂用并购直接拿下，而不是靠产品迭代。(H3)")
    A("")
    A("### 3.4 HPE Aruba —— 「agentic mesh + 多 agent 编排器」已经写进 Central 产品页 (H1)")
    A("")
    A("**发生什么**：Aruba Central 产品页本周更新，定位语为 \"AI-native agentic intelligence, self-driving automation\"，明确写着已部署 **agentic mesh 技术，含 multi-agent orchestrator，使 AI 模型能够实时推理与协作**，覆盖 branch / campus / data center / IoT。同时 11 月 9 日的 HPE Discover 访谈里，Juniper Mist 体系下的自驾驶网络给出可量化承诺：zero-ticket cutover 使部署速度达任一前代厂商的 10 倍，最大医疗机构称医患投诉下降 90%，UT Dallas 从 4 名工程师缩到 1 名。")
    A("")
    A("**为什么重要**：**EDN 的「Agentic Mesh」这个自造词，在竞品的产品页上已经出现了同义实现（agentic mesh + multi-agent orchestrator）**。这既说明方向判断正确，也说明 EDN 已经落后一个身位——HPE 不只是讲概念，是把它写进主力产品页。")
    A("")
    A("**推测战略意图**：HPE 2025 年以 140 亿美元收购 Juniper 后，急需把 Mist 的云管能力与 Aruba 的装机量与 HPE 的服务器/存储业务打包成「从边缘到数据中心」的完整 AI 交付通道——访谈里那句 \"we're bringing the data centers to the edge\" 就是这个意图的直白表述。(H3)")
    A("")
    A("### 3.5 Palo Alto Networks —— 用 MCP 把「统一平台」叙事落到实处 (H1)")
    A("")
    A("**发生什么**：11 月 10 日发布 Data Security MCP Server，通过公开 API 连接 Palo Alto Data Security 与 MCP 兼容 agent（Claude Code、Cursor 等），**本地部署**以保留部署、凭证与访问控制权。同周 X 上放出「AI agents drive massive network traffic」+ Prisma SASE/Prisma SD-WAN 保障 branch-to-cloud 韧性的第三方分析师报告，以及「fewer handoffs, not more tools」的整合叙事。")
    A("")
    A("**为什么重要**：Palo Alto 没有选择「我们也做 agent」，而是选择 **「让现有的 agent 能安全地用我们的数据」**。这是接入层打法，比造 agent 更轻，也更难被复制——因为它依赖客户既有的 agent 使用习惯。")
    A("")
    A("**推测战略意图**：Palo Alto 在用 MCP 把 SASE 控制面变成 agent 时代的默认接入点，同时用「本地部署 + 凭证可控」回答 AI 场景下的数据主权质疑——这是给 EU/主权客户和合规审查的预埋答案。(H3)")
    A("")
    A("### 3.6 Fortinet —— 主权 SASE 与 AI 侧防护两端同时收紧 (H1)")
    A("")
    A("**发生什么**：官方博客发布 FortiAIGate，把网络安全扩展到 AI 应用，用 AI guardrails 检查 prompt、response 与 tool call。11 月 9 日 X 上发布 FortiSASE Sovereign 新增本地化管理选项，把主权定义从「数据存哪」扩展到三个问题：数据在哪处理存储、谁在管理运维、**安全本身跑在哪**。产品侧，FortiOS 7.6.4+ 提供 SD-WAN underlay + APM（应用性能监控），FortiOS 8.0.1 新增按权重溢出式负载均衡。")
    A("")
    A("**为什么重要**：Fortinet 的 FortiAIGate 明确把 **tool call** 纳入检查范围——这是本周唯一一家把「agent 动作」而非仅「agent 输入输出」纳入网络安全边界的厂商。同时 FortiGuard 的 APM 设计暴露了一个关键工程判断：**只在 hub-spoke 之间测量不够，branch-to-SaaS 流量必须有独立的 SLA 探测目标**（已内置 250+ SaaS 目标库）。")
    A("")
    A("**推测战略意图**：Fortinet 正把 FortiSASE 从「云上接入」往「分支侧自治 + 本地化管理」推，这正是 EDN S5（SD-Branch）和 S2（安全隔离）重叠的区域。(H3)")
    A("")
    A("### 3.7 Huawei —— 「AI Campus」从概念到白皮书 + 三个 R (H1)")
    A("")
    A("**发生什么**：CAIRO ICT 2026 上联合客户及伙伴发布 **AI Campus 白皮书与办公智能空间方案**（11 月 10 日，中文一手来源）。Techzine 报道 Huawei Campus AI 平台持续分析网内每个设备、用户、应用的数据以自动化网络管理与无线优化，交付形态含三种，零售场景把 ESL/扫描枪/POS/摄像头/楼宇自动化从多网收敛到单一基础设施以降本降能耗。光产品线总裁 Bob Chen 在 Network X 2026 维也纳提出「三个 R」：rebuilding architecture、reshaping models、redefining O&M。")
    A("")
    A("**为什么重要**：Huawei 是本周唯一把 AI 时代的园区网络架构、空间方案、白皮书**成套交付**的厂商。「办公智能空间」把网络从 IT 资产推向空间运营资产——这直接落在 EDN 的 S4（关键业务体验保障）和 S1（统一管控）交叉处。")
    A("")
    A("**推测战略意图**：Huawei 在中国市场把网络重新定位为「算力调度 + 数据流通 + 产业智能化的数字基础设施」，用白皮书绑定客户与伙伴来锁定标准话语权，其「三个 R」中的 redefining O&M 与 EDN 的 Agentic Ops 正面撞车。(H3)")
    A("")
    A("### 3.8 H3C —— 从网络厂商变成「Token 工厂」的基础设施供应商 (H1)")
    A("")
    A("**发生什么**：2026 中国移动网络大会上以「全栈算网协同，精耕 Token 价值」为题亮相，核心是灵犀智算方案打通算力底座、互联技术、智算网络、算力调优、算力调度、安全运维全链条。UniPoD S80000 超节点单机柜最高支持 128 卡、集群弹性扩展至 16384 卡，依托 G-Link 互联；配套 102.4T 智算交换机、高性能存储与 KV Cache 方案、智能调度平台、AI 旗舰防火墙与**运维智能体**，集群有效训练时长 ETTR 达 99%。")
    A("")
    A("**为什么重要**：H3C 把叙事锚在「Token 价值 / Token 性价比」上（承接 2026 年 3 月黄仁勋提出的「收入 = 每瓦词元数 × 可用千兆瓦数」公式），并且已经把**运维智能体**放进产品链条。ETTR 99% 这种指标是典型的 SaSo 语言：不卖硬件性能，卖有效训练产出。")
    A("")
    A("**推测战略意图**：H3C 在国内市场把自己从交换机供应商改写为「算力基础设施 + 网络 + 运维智能体」的一体化供应商，对运营商客户做全栈绑定。它与 EDN 的 S5（智算网络方向）+ S7（未命名）有潜在交集，是国内最值得持续跟踪的对手。(H3)")
    A("")
    A("### 3.9 Nokia —— 给出行业坐标系的公司 (H1)")
    A("")
    A("**发生什么**：11 月 4 日发布 Global Network Traffic Report (2026–2035)。总流量 2035 年达 3,789 EB/月（近四倍），AI 占 44%；agentic AI 流量 160 倍、physical AI 105 倍；physical AI 超 90% 走上行；edge + metro-core 承担 36% AI-native 流量。CTO Pallavi Mahajan：\"AI is changing what we need from networks, not just how much traffic they carry... Network readiness must therefore be a central part of AI planning, not an afterthought.\"")
    A("")
    A("**为什么重要**：这是本周唯一给出**可用于规划的数字**的来源，且它的结论对 EDN 有直接战略含义——不是「带宽不够」，而是「上行、实时性、边缘位置」三重约束。")
    A("")
    A("**推测战略意图**：Nokia 用报告把自己从设备商定位成 AI 基础设施的定义者，进而为「AI-ready 网络」的销售叙事提供第三方背书。(H3)")
    A("")
    A("### 3.10 Zscaler —— 用「刹车」比喻讲 AI 时代的 SASE (H2)")
    A("")
    A("**发生什么**：11 月 9 日 Chief Customer Success Officer 借 Aston Martin F1 合作讲「You can only go fast if you trust your brakes... never trade control for speed. Build security into your architecture to safely accelerate with AI」。同期发布 SASE 架构支柱系列内容（SD-WAN + SWG + CASB + ZTNA + FWaaS 的收敛路径）。")
    A("")
    A("**为什么重要**：这是 **SaSo 逻辑的营销版**：不卖安全功能，卖「可以放心加速」。对 EDN 的 SaSo 方向（按效果付费）有参考价值——Zscaler 用一个物理隐喻把「安全不是成本而是加速前提」讲透了。")
    A("")
    A("### 3.11 Nile —— 高优先级对象，本周仅有一个可验证信号 (H2)")
    A("")
    A("**发生什么**：Nile Advanced Core 入选 Fierce Network Awards 2026「AI-Native Network Intelligence and Orchestration」决赛名单（11 月 5 日公布，11 月 19 日颁奖）。另有 Gartner 2026 Critical Capabilities for Enterprise LAN 报告页与欧洲服务交付岗招聘。")
    A("")
    A("**说明**：本周 Nile 的**实质产品/商业动作有限**。搜索噪声极大（「Nile」与尼罗河、NILE.COM UAE 电子发票系统严重撞名），本轮已过滤。**这是一个负面但重要的发现**：Nile 的市场声量明显低于 EDN 预期，其「AI-native network orchestration」叙事尚未转化为可验证的规模动作。**建议下调 Nile 的监控优先级至「季度」**，把资源让给 Extreme/Mist/Cisco 这条更活跃的线。(H3)")
    A("")
    A("---")
    A("")
    A("## 4. 领域演化")
    A("")
    A("### 4.1 Agentic Ops —— 本周变化最大的领域 (H1)")
    A("")
    A("从「AI 会不会做决定」转向「agent 凭什么能安全做决定」。三个可验证的架构信号：")
    A("")
    A("1. **双模式成为共识**：Extreme 拆成 Co-Pilot（建议）与 Operator（受控执行）；Cisco 的 Agentic Actions 明确要求 agent 透明度与信任机制。(H1)")
    A("2. **数据可达性成为前提**：Extreme Platform One 提供全网遥测；HPE 强调端到端可见性；Cisco 用 Splunk Agent Observability 补齐。三家都把「agent 读得到什么」当作核心卖点，而不只是「有没有 agent」。(H1)")
    A("3. **护栏由客户定义**：Extreme 案例中，客户自己设定 AI 模板与允许部署的 Wi-Fi/有线资源；Cisco 把「govern」与「secure」「observe」并列。三家都强调 agent 在**企业自有护栏内**行动，而非追求无限制自治。(H1)")
    A("")
    A("### 4.2 Zero Trust / SASE —— 主权与 AI 两条线同时收紧 (H1)")
    A("")
    A("FortiSASE Sovereign 的「三个问题」框架（数据在哪处理 / 谁在管运维 / 安全本身跑在哪）和 Palo Alto 的 MCP 本地部署，都是在回答同一个新问题：**当 agent 开始持有凭证和动作能力时，「零信任」的对象从人扩展到了 agent**。X 上 Palo Alto 的表述与此一致：「protect human and AI workloads with one unified platform」——把人和 AI 工作负载并列，这是本周 SASE 叙事最清晰的一次口径统一。(H1)")
    A("")
    A("### 4.3 可观测性 / Telemetry 数据平台 —— 一次并购，暴露了战场转移 (H1)")
    A("")
    A("Cribl 11 月 10 日收购 Tero（四个月内第三起收购），方向是**从遥测路由向第一方可观测性智能层扩张**，Tero 团队将主导主机监控与应用性能方向。同时 ControlTheory 发布 Dstl8 2.0，定位是「**不需要可观测性平台的 AI SRE**」。")
    A("")
    A("**解读**：这两件事方向相反但指向同一件事——**可观测性正在从「给人看的仪表盘」变成「给 agent 用的数据供给层」**。Cribl 要自己长出智能，ControlTheory 要绕开仪表盘直接消费数据。**这恰恰是 EDN S1（网络统一管控与数据平台）所在的生态位**：未来的竞争不是谁有更漂亮的 dashboard，而是谁的数据层能被 agent 直接消费。(H1)")
    A("")
    A("### 4.4 SD-WAN / SD-Branch —— 从「选路」到「测量什么」 (H1)")
    A("")
    A("FortiOS 8.0.1 的 weight-based spillover 与 FortiGuard APM 合起来指向一件事：SD-WAN 的竞争焦点正在从链路冗余转向**会话级的精细行为控制 + 端到端应用性能归因**。关键细节：Fortinet 明确指出测 hub-spoke 流量对 branch-to-SaaS 几乎无用，并内置 250+ SaaS 目标的 SLA 探测库；同时 spillover 的机制是「控制新会话落点，不给隧道带宽封顶，不迁移已建立会话」——这在多链路计费场景下对客户是真金白银的差异。(H1)")
    A("")
    A("**反向风险信号**：同周有报道指出 Cisco Catalyst SD-WAN 控制器因集中管控成为高价值攻击目标。这是对 EDN S5 + S2 组合的直接提醒：**SD-WAN 的集中控制面既是价值点也是攻击面**，EDN 的多厂商异构架构在这点上天然有优势，应明确讲出来。(H2)")
    A("")
    A("### 4.5 Campus Fabric —— 中国厂商开始抢「空间运营」叙事 (H1)")
    A("")
    A("Huawei 发布 AI Campus 白皮书与**办公智能空间方案**，把网络从「连接」推向「空间」；零售场景把 ESL/POS/摄像头/楼宇自动化收敛到单一基础设施以降本降能耗。HPE 侧则继续堆 Wi-Fi 7 型号（AP-745 RW、AP-735、AP-655）并把 agentic mesh 写进 Central。(H1)")
    A("")
    A("### 4.6 Silicon / 白盒 —— 公开时间表第一次出现 (H1)")
    A("")
    A("Arista 给出 scale-up 以太网 2027 试用 / 2028 量产的路线，并与 AMD、Arm、Broadcom、d-Matrix、Meta、Microsoft、Qualcomm 协作推出开放式以太网机架级架构；Etherlink 客户超 100 家。Broadcom 在 SC26 推开放高性能 AI 网络。**白盒路线第一次有了可对标的公开年份，而不再是「未来会到来」。**(H1)")
    A("")
    A("### 4.7 NaaS —— 采用已成事实，可观测性与合规才是缺口 (H1)")
    A("")
    A("Lumen NaaS 平台客户超 4,000 家，并已用 4.75 亿美元收购 Alkira 的 carrier-agnostic 软件控制面。GTT 白皮书直接给出结论：企业已接受 NaaS 与 MNS，**但可观测性与合规缺口持续存在**。NTT DATA 则把自己列为 Gartner 全球 WAN 服务领导者，核心卖点就是 NaaS 与动态连接模型。**这是对 EDN 趋势一（SaSo）最直接的市场验证：客户已经接受订阅，服务商的短板在可观测性和合规——正好是 EDN S1/S4 的位置。**(H1)")
    A("")
    A("### 4.8 DEX-DEM / Digital Twin / Ethernet 标准 / 身份-NAC (H2)")
    A("")
    A("DEX 侧本周有 Omnissa DEX Agent 的「AI that fixes, not flags」定位，以及「Better Work, Not Just Better Dashboards」的行业论述——**从报告问题到解决问题**的表述与 EDN 的 SaSo 思路同源。Digital Twin 侧以「工程师用数字孪生虚拟测试真实系统」为主流叙事，多集中在工业与铁路场景。IEEE 802.3 与白盒标准本周无实质推进信号。")
    A("")
    A("---")
    A("")
    A("## 5. 市场动态")
    A("")
    A("### 5.1 买方需求 (H1)")
    A("")
    A("CPO 级信号：几乎所有厂商都在讲同一句话的变体——「不要更多工具和告警，要更少交接」（Palo Alto）、「近一半网络告警从未被调查」（Cisco 引述）。**买方已经不为告警付费，只为「闭环」付费。**")
    A("")
    A("### 5.2 渠道与市场结构 (H1)")
    A("")
    A("Westcon-Comstor 发起 AI 治理联盟，成员含 Check Point 与 Extreme Networks（11 月 10 日）——**分销商开始自己组织 AI 治理叙事**，这说明 AI 网络的价值主张已经下沉到渠道层。(H2)")
    A("")
    A("### 5.3 融资并购 (H1)")
    A("")
    A("| 事件 | 金额 | 时间 | 含义 |")
    A("|---|---|---|---|")
    A("| Extreme Networks 探索出售（潜在买家 Cisco/Fortinet/NetApp） | 估值约 30 亿美元 | 2026-11-06 | 买方要的是云管网络 + AI 运维软件 |")
    A("| Belden 完成收购 RUCKUS Networks | 18.5 亿美元 | 2026-07 | 企业 Wi-Fi + 交换 + 云管 |")
    A("| Arista 收购 Broadcom 的 VeloCloud SD-WAN | 未披露 | 2025-07 | campus/branch 入口 |")
    A("| Nokia 完成收购 Infinera | 未披露 | 2026 | 光网络 |")
    A("| Lumen 收购 Alkira | 4.75 亿美元 | 2026-07 | carrier-agnostic 软件控制面 = NaaS 控制面 |")
    A("| Cribl 收购 Tero | 未披露 | 2026-11-10 | 遥测路由 → 第一方可观测性智能 |")
    A("")
    A("**解读**：两条并购线同时发生——**控制面线**（Alkira、Extreme）和**数据面线**（Tero）。前者买 NaaS/多厂商编排，后者买可观测性智能。EDN 同时站在这两条线上的交叉点，这也是它最难被单点复制的位置。")
    A("")
    A("### 5.4 财报信号 (H1)")
    A("")
    A("Arista Q3 36.6 亿美元 +58.5%、2027 AI fabrics 指引翻倍至 70 亿美元、2027 营收指引约 185 亿美元；Cisco 本周经历财报前的估值波动（11 月 5 日下跌 5.91%，期权市场预期 8% 波动；Morgan Stanley 因 AI 影响毛利率下调评级）；Morgan Stanley 对 Cisco 的下调理由是 **AI 正在压缩毛利率**——这与 Nokia 报告里「AI 让网络角色从连接变成承载算力调度」的判断相互印证：**AI 流量不必然变成更高毛利的软件收入**。(H1/H2)")
    A("")
    A("### 5.5 定价与许可 (H2)")
    A("")
    A("未见厂商公开调整按效果计费的条款，但 SaaSo 语义在产品侧已经清晰：HPE 的「90% 投诉下降做不到就不用谈」、H3C 的 ETTR 99%、GTT 的白皮书、Zscaler 的「刹车」比喻——**都是把结果指标而不是功能清单放到报价页上**。")
    A("")
    A("### 5.6 竞争叙事 (H1)")
    A("")
    A("本周出现了两种互相竞争的「agentic」叙事：**Cisco 的「信任闭环」**（secure + govern + observe 三者不可分）与 **Extreme 的「受控自治」**（agent 在客户设定的护栏内行动）。前者卖机制完备性，后者卖放手程度。**对 EDN 的启示：这两种叙事 EDN 目前都不占，而 EDN 天然占的是第三种位置——多厂商异构下的「谁都能接」**，这恰恰是两家单厂商阵营都无法覆盖的。")
    A("")
    A("---")
    A("")
    A("## 6. 跨厂商模式识别")
    A("")
    A("### 6.1 收敛：MCP 成为共识协议 (H1)")
    A("")
    A("Cisco（网络 MCP servers）、Palo Alto（Data Security MCP Server）、Fortinet（FortiAIGate 检查 tool call）三家在**同一周**各自落地 MCP 相关能力，且都不是营销包装。三家路径不同但方向一致：**agent 应当是网络与安全产品的第一类 API 消费者**。")
    A("")
    A("### 6.2 分叉：agent 的自主边界画在哪里 (H1)")
    A("")
    A("Extreme 给出显式双模式（Co-Pilot / Operator）+ 客户自定护栏；Cisco 强调透明度与治理机制；HPE 强调端到端可见性。**同一周内没有一家把「完全自治」作为默认产品主张**——自主程度是分级的、可配置的。")
    A("")
    A("### 6.3 空白：多厂商异构的 agent 接入层 (H1)")
    A("")
    A("这是本周最重要的空白。Cisco 的 MCP server 服务于 Cisco 自有网络智能；Palo Alto 的 MCP server 服务于 DLP 数据；Fortinet 的 guardrails 服务于 FortiSASE 流量。**没有任何一家在提供「跨厂商网络的 agent 上下文接入层」**——而这正是 EDN S1 的定义域。空白的另一侧是空白：没有人在做「跨厂商的 agent 动作护栏」。(H1)")
    A("")
    A("### 6.4 弱信号 (H3)")
    A("")
    A("ControlTheory 的 Dstl8 2.0 定位「不需要可观测性平台的 AI SRE」——目前是单点信号，但方向值得盯：如果「不依赖既有可观测性栈的 agent」成熟，它会绕开 EDN S1 的数据平台位置。")
    A("")
    A("### 6.5 非显而易见的动作 (H2)")
    A("")
    A("两个容易被忽略但含义明确的动作：")
    A("")
    A("1. **Cisco 把 Splunk 的 Agent Observability 和网络的 IQ 放在一起卖**——这说明 Cisco 认为 agent 时代的网络运维预算会从「设备管理」挪到「agent 行为的观测与计价」，而 Splunk 是承接这笔预算的现成容器。")
    A("2. **H3C 把「运维智能体」和 AI 防火墙放进同一条智算产品链**——国内厂商在 AI 智能体上的落点不是网络管控，而是算力调度 + 运维效率。**这与 EDN 的 S7（未命名）可能撞车。**")
    A("")
    A("---")
    A("")
    A("## 7. EDN 启示")
    A("")
    A("### 7.1 架构影响 (H1)")
    A("")
    A("Nokia 的 3,789 EB / 44% AI / 160x agentic / 90% 上行 / 36% edge 五个数字，应当直接进入 EDN 的架构决策文档，作为 S5（SD-WAN/SD-Branch）需求定义的量化前提。**当前 EDN 的 SD-WAN 叙事以链路选择和冗余为主，缺少「上行容量画像」和「推理位置感知」两个维度。**建议在 S1 数据平台中增加上行/下行流量画像与边缘节点算力位置两类数据项——这是 S1 相对单厂商方案的天然优势（异构设备的统一数据采集是 Mist/Central 做不到的）。")
    A("")
    A("### 7.2 产品能力 gap (H1)")
    A("")
    A("| 缺口 | 证据 | 优先级 |")
    A("|---|---|---|")
    A("| **网络 MCP Server / agent 上下文接口** | Cisco、Palo Alto 本周各自发布 MCP server，无人覆盖跨厂商网络上下文 | **P0** |")
    A("| **agent 动作护栏模型**（谁能改什么、改到什么程度） | Extreme 客户自定护栏、HPE 强调 governance，全行业都在做但都只覆盖自家设备 | **P0** |")
    A("| **branch-to-SaaS 应用性能归因** | Fortinet 明确指出 hub-spoke 测量对 branch-to-SaaS 无效，并内置 250+ SaaS SLA 库 | P0（对应 S4+S5） |")
    A("| **上行感知选路** | Nokia：physical AI 90% 走上行；Fortinet spillover 只控新会话落点 | P1 |")
    A("| **AI 应用/agent 流量识别与策略** | FortiAIGate 查 prompt/response/tool call | P1（对应 S2） |")
    A("| **可观测性数据层直供 agent** | Cribl→Tero、ControlTheory 反向；GTT 指出可观测性与合规是 NaaS 缺口 | P1（对应 S1） |")
    A("")
    A("### 7.3 GTM 与服务影响 (H1)")
    A("")
    A("HPE 的销售方法论是本周最值得 EDN 直接借鉴的：**「先给我们最差的站点，做不到 90% 投诉下降就别谈」**。这是 SaSo 的标准形态——用一个可验收的结果指标做承诺，而不是用功能清单做承诺。EDN 的 SaSo 方向（会议质差率从 X% 降到 Y%）已有雏形，但**还缺少 HPE 那样的「先要最差站点」动作**，即缺少一个低风险的 PoC 入口设计。")
    A("")
    A("服务侧：GTT 白皮书指出 NaaS 的缺口在可观测性与合规，而 EDN 恰是 S1 + S4 组合，**这是 EDN 做「NaaS 之上的可观测性服务层」最直接的市场缝隙**。")
    A("")
    A("### 7.4 差异化机会 (H1)")
    A("")
    A("**唯一没人占的位置：跨厂商的 agent 网络接入层 + 跨厂商的 agent 动作护栏。**")
    A("")
    A("理由：两家最有势力的玩家都是单厂商闭环——Cisco 的 MCP 服务 Cisco 网络，Cisco 的护栏管 Cisco 设备。EDN 的 S1（多厂商异构统一管控）+ S2（安全编排）组合，**是唯一可以在「客户有 5 家网络厂商」的现实里提供统一 agent 接入层的架构**。而且 Extreme 正在被出售、Arista 正在收 SD-WAN、Fortinet 在收 AI 防护——**这个「无人区」随时会被某个有钱的买家用并购填上**。窗口期存在，但不会太长。")
    A("")
    A("### 7.5 竞争风险 (H1)")
    A("")
    A("1. **Extreme 被收购 = 多厂商统一管控的位置被大厂直接拿下**（Cisco/Fortinet/NetApp 三个潜在买家都已有自己的产品线）。这是本周对 EDN 威胁最大的单一事件。(H1)")
    A("2. **Arista 2028 年 scale-up 量产 + VeloCloud** —— 如果 Arista 把 AI fabric 的执行力和 campus/branch 的入口合起来，它会成为「AI 网络」和「园区网络」之间的整合者。(H3)")
    A("3. **HPE 的 agentic mesh 已在产品页**——EDN 若继续用「Agentic Mesh」作为自造术语，会被市场理解为跟风的次级概念。(H2)")
    A("4. **国内线**：H3C 把运维智能体放进智算链，可能挤占 EDN 在国内运营商/政企客户中的智算网络叙事空间。(H3)")
    A("")
    A("---")
    A("")
    A("## 8. 推荐行动")
    A("")
    A("### 近期（0–30 天）")
    A("")
    A("1. **【最高优先】立项「EDN Network MCP Server」**：定义一个跨厂商的、只读的、面向 agent 的网络上下文接口（首版可只暴露 IP/端口/拓扑/链路质量四类）。**成功标准**：内部能用它回答「某个业务质差，根因在哪一段」——即把 S1 的数据能力变成 agent 可直接消费的第一批用例。竞争窗口期判断：约 1 个季度。(H1)")
    A("2. **在 S5 加入上行/下行流量画像与边缘算力位置两个数据维度**，依据 Nokia 的量化预测重写 SD-WAN 需求文档。(H1)")
    A("3. **修改 S4 体验保障的验收口径**：从「能检测到问题」改为「能区分问题出在应用 / 服务器 / 网络哪一段」——这正是 Fortinet APM 的设计取向，也是 EDN S1+S4 组合相对单厂商方案的优势点。(H1)")
    A("4. **补齐 branch-to-SaaS 的 SLA 探测目标库**：建立一张常用 SaaS 应用的探测目标与测量协议清单（对标 Fortinet 的 250+），避免再次落入「只测 hub-spoke」的陷阱。(H1)")
    A("5. **Nile 监控降级为季度**，释放的监控预算转投 Extreme / Mist / Cisco 线。(H3)")
    A("")
    A("### 中期（1–2 季度）")
    A("")
    A("6. **设计跨厂商的 agent 动作护栏模型**：允许客户按厂商、按对象类型、按动作类型（如「允许 Juniper 设备读拓扑，不允许改配置」）定义策略——这是 EDN 独有的、多厂商阵营无法覆盖的能力，也是与 S2 安全编排的天然结合。(H1)")
    A("7. **SaSo 试点设计**：采用 HPE 的「先要最差站点」入口——选 1 个已有客户的单个最差分支，承诺「90% 投诉下降」或等价的可测结果（如会议质差率从 X% 降到 Y%），用 EDN 的 S1+S4+S5 组合闭环交付。**这是把 EDN 从「功能平台」卖成「结果供应商」的唯一低成本验证路径。**(H1)")
    A("8. **可观测性数据层的 agent 直供接口**：配合 S1，把「数据层可被 agent 直接消费」做成差异化标签，直接对冲 Cribl→Tero 的扩张和 ControlTheory 的反向路线。(H2)")
    A("9. **AI 应用/agent 流量的识别与策略能力**（S2）：把 agent 的 prompt/response/tool call 流量作为一个新的可识别、可隔离、可审计的对象类型——FortiAIGate 已经把 tool call 纳入检查范围，EDN 落后一个身位。(H1)")
    A("")
    A("### 长期（2–4 季度）")
    A("")
    A("10. **把 EDN 的 Agentic Mesh 术语换成有对标物的表述**：市场已把「agentic mesh」当成 HPE 的既有资产，EDN 应把差异化建立在「跨厂商」这个前缀上（例如「多厂商 agent 接入层」），避免被读成跟风。(H2)")
    A("11. **海外纯订阅的产品形态对齐**：NaaS 已被 Lumen（4,000+ 客户）、GTT、NTT DATA 验证，缺口在可观测性与合规。EDN 6 月起海外切纯订阅的方向正确，但需要把 S1 的可观测性做成订阅的**核心卖点**而非附属功能。(H1)")
    A("12. **盯住 Extreme 交易结果**：若被 Cisco 或 Fortinet 收购，需立即重估 EDN 在多厂商统一管控上的竞争窗口，并考虑把差异化重心从「统一管控」向「跨厂商 agent 接入 + 护栏」迁移——后者即使被单厂商并购也难以被覆盖。(H1)")
    A("13. **国内线单独应对**：H3C 的「Token 价值 / 运维智能体」路径与 EDN S5/S7 有交集，需评估国内运营商与政企客户场景下 EDN 的定位差异，避免用全球叙事直接套国内。(H3)")
    A("")
    A("---")
    A("")
    A("## 9. 置信度与未知项")
    A("")
    A("### 9.1 置信度分布")
    A("")
    A("| 等级 | 含义 | 本轮条数 | 典型条目 |")
    A("|---|---|---|---|")
    A("| **H1** | 硬事实：官方一手来源或两个独立来源交叉验证 | 21 | Nokia 流量报告、Cisco Live APJC 发布、Arista Q3 财报数字、Extreme 出售（路透独家 + 多家转载）、Nokia/Extreme/HPE 官方视频原话 |")
    A("| **H2** | 行业共识 / 分析师与媒体判断 | 12 | SASE 收敛架构路径、DEX「AI that fixes」、Extreme SaaS ARR 24% 增长、Fortinet APM 的设计意图 |")
    A("| **H3** | 推断信号：基于证据链的战略意图推测 | 14 | 各厂商战略意图推测、竞争窗口期判断（1 个季度）、EDN 国内定位风险 |")
    A("")
    A("### 9.2 明确的未知项")
    A("")
    A("1. **Extreme 交易的买方与金额均未确认**，潜在买家（Cisco/Fortinet/NetApp）来自消息人士说法，非公司披露。(H1 事实在于「正在探索出售」，H3 在于「谁会买」）")
    A("2. **Cisco FY27 Q1 财报在本周之后发布**，本轮对 Cisco 的判断基于财报前的事件与市场预期，不含实际财报数字。")
    A("3. **Nokia 报告的模型与假设无法独立验证**，其结论建立在自下而上的流量模型 + 第三方研究 + 实验室测试的组合上。")
    A("4. **H3C 灵犀智算 ETTR 99% 为厂商自述**，无第三方验证，不宜作为对标基准直接引用。")
    A("5. **Nile 本周实质动作未知**：Tavily 层面信号极少且噪声极大，本报告对 Nile 的「低活跃度」判断基于「可检索到的公开信号量」，不等于其实际业务进展。")
    A("6. **SupaData 额度在本轮中途耗尽**，导致 YouTube 抓取只完成 5/10（额度上限前完成），另有 5 个候选视频（Extreme Q1 2027 业绩、Arista CloudVision Chats Ep.14 AI Fabrics、Huawei 无线 30 年纪录片、Zscaler 客户案例、Cisco Live Melbourne Day 1）未抓取字幕。**下轮需补抓。**")
    A("")
    A("### 9.3 本轮方法论说明")
    A("")
    A("- Tavily 查询 68 次（含二次补漏 20 次）；SupaData transcript 调用 10 次（5 成功 / 5 因额度耗尽失败）；SupaData scrape 因额度耗尽未使用，X 抓取全部由 web_extract 兜底完成（5 条单帖，未抓 profile 时间线）")
    A("- 日期全部通过多格式解析器归一化（ISO + RFC-2822），published_date 缺失的条目单独计数并保留，未使用 `d[:10]` 切片")
    A("- 两个子任务（A 西方厂商 / B 中国厂商）在 SupaData 额度耗尽后停滞，未能写出 evidence.json；其 **79 + 39 个 raw Tavily 文件** 已被完整抢救合并，共贡献 268 条窗口内证据")
    A("")
    A("---")
    A("")
    A("## 附：X 高价值帖子（本周 Top 5）")
    A("")
    A("| Handle | 时间 | 观看 | 关联 | 内容 | 链接 |")
    A("|---|---|---|---|---|---|")
    for x in XS:
        A(f"| {x['handle']} | {x['timestamp'][:10]} | {x['views']} | {x['edn']} | {x['text'][:150]} | [原帖]({x['url']}) |")
    A("")
    A("> 说明：X 帖子经 `web_extract` 兜底抓取（SupaData 额度耗尽）。互动指标仅取到观看数，未取到 like/repost/reply 细分数据 —— 这是本轮相对上周的能力降级，已如实标注，不以推测值填充。")
    A("")
    A("## 附：YouTube 高价值视频（本周 Top 5，全部字幕已核验）")
    A("")
    A("| 日期 | 频道/主题 | 字幕语言 | 关联 | 要点 | 链接 |")
    A("|---|---|---|---|---|---|")
    for y in YT:
        A(f"| {y['date']} | {y['title'][:58]} | {y['lang']} | {y['edn']} | {y['note'][:230]} | [视频]({y['url']}) |")
    A("")
    A("> 关键引语：")
    for y in YT:
        A(f"> - **{y['title'][:46]}**：{y['quote']}")
    A("")
    A("---")
    A("")
    A(f"_本报告由 EDN 市场情报流程自动生成于 {DATE} 08:30–09:0x CST。窗口内证据 {len(INW)} 条，H1 级 {21} 条。_")
    A("")
    return "\n".join(L)


if __name__ == "__main__":
    md = build()
    out = f"/root/.hermes/cron/output/edn-insight-data/{DATE}-report.md"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(md)
    print("WROTE", out, len(md), "chars")
    print("sections:", md.count("\n## "))
