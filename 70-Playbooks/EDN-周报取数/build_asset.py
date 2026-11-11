#!/usr/bin/env python3
"""EDN 2026-11-11 — build the data asset JSON."""
import json, os
from datetime import datetime, timezone, timedelta

DATE = "2026-11-11"
SH = timezone(timedelta(hours=8))
M = json.load(open("/tmp/edn-east/merged.json"))
INW = M["in_window"]
X = json.load(open("/tmp/edn-east/x_signals.json"))

XS_FULL = [
    {"handle": "@PaloAltoNtwks", "post_id": "2120278302304751938",
     "url": "https://x.com/PaloAltoNtwks/status/2120278302304751938",
     "timestamp": "2026-11-10T22:11:00Z", "text": "AI agents drive massive network traffic. AI-powered threats strike at machine speed. In a new report, WillTownTech of LoneStar Advisory & Research breaks down how Prisma SASE and Prisma SD-WAN ensure network resilience and enforce zero trust from branch to cloud.",
     "metrics": {"views": 575, "likes": None, "retweets": None, "replies": None},
     "relevance_score": 5, "edn_link": "S2/S5", "source_type": "official-social"},
    {"handle": "@CiscoNetworking", "post_id": "2118739986874777624",
     "url": "https://x.com/CiscoNetworking/status/2118739986874777624",
     "timestamp": "2026-11-06T16:19:00Z", "text": "When nearly half of network alerts go uninvestigated, IT teams need a way to keep pace. As AI agents add more traffic and complexity to networks, Cisco AgenticOps helps teams solve problems in real time and operate at machine speed—without having to scale their operations teams to keep up.",
     "metrics": {"views": 1046, "likes": None, "retweets": None, "replies": None},
     "relevance_score": 5, "edn_link": "Agentic Ops", "source_type": "official-social"},
    {"handle": "@Fortinet", "post_id": "2119822801154593148",
     "url": "https://x.com/Fortinet/status/2119822801154593148",
     "timestamp": "2026-11-09T16:01:00Z", "text": "Sovereignty isn't just about where your data lives. It also comes down to: where is data processed and stored? who manages and administers operations? where does the security itself run? FortiSASE Sovereign extends control across all three, including a new on-premises management option.",
     "metrics": {"views": 1494, "likes": None, "retweets": None, "replies": None},
     "relevance_score": 4, "edn_link": "S2", "source_type": "official-social"},
    {"handle": "@PaloAltoNtwks", "post_id": "2119916006424412309",
     "url": "https://x.com/PaloAltoNtwks/status/2119916006424412309",
     "timestamp": "2026-11-09T22:12:00Z", "text": "The AI era is redefining network security. Your team needs fewer handoffs, not more tools, alerts, or manual work. Learn how to stop threats earlier and protect human and AI workloads with one unified platform. Less fragmentation. Faster protection.",
     "metrics": {"views": 1756, "likes": None, "retweets": None, "replies": None},
     "relevance_score": 4, "edn_link": "S2", "source_type": "official-social"},
    {"handle": "@Zscaler", "post_id": "2119792301966799224",
     "url": "https://x.com/zscaler/status/2119792301966799224",
     "timestamp": "2026-11-09T14:00:00Z", "text": "You can only go fast if you trust your brakes. As our Chief Customer Success Officer shares - never trade control for speed. Build security into your architecture to safely accelerate with AI. Learn more about our partnership with Aston Martin F1.",
     "metrics": {"views": 341, "likes": None, "retweets": None, "replies": None},
     "relevance_score": 3, "edn_link": "S2/SaSo", "source_type": "official-social"},
]

YT_FULL = [
    {"video_id": "n-SpgqsN3e4", "url": "https://www.youtube.com/watch?v=n-SpgqsN3e4",
     "title": "AI Is Changing Networks: HPE's Vision for Self-Driving AI", "date": "2026-11-09",
     "channel": "Converge Digest / HPE Discover", "lang": "en", "relevance_score": 5,
     "edn_link": "S1/S4/S5 + Agentic Ops", "source_type": "official-video",
     "key_points": ["zero-ticket cutover：部署速度 10 倍于任一前代厂商",
                    "最大医疗机构：医患投诉下降 90%",
                    "端到端 AI 可见性层：Wi-Fi → 交换 → SD-WAN → NAC → 数据中心，Today not future",
                    "UT Dallas：4 名工程师 → 1 名"],
     "quote": "if we can't transform it with 90% fewer complaints in that site, don't even talk to us"},
    {"video_id": "rO1bRXimwEI", "url": "https://www.youtube.com/watch?v=rO1bRXimwEI",
     "title": "#AINetworking26: Agentic AI Ends Firefighting With Trusted Autonomy",
     "date": "2026-11-04", "channel": "AINetworking26", "lang": "ar", "relevance_score": 5,
     "edn_link": "S1 + Agentic Ops", "source_type": "official-video",
     "key_points": ["Extreme Agent One 双模式：Co-Pilot（分析/建议/下一步）与 Operator（护栏内代执行）",
                    "Extreme Platform One 汇聚全网遥测：设备、用户、应用、基础设施",
                    "客户 New Perspective Senior Living：预置 AI 模板 1 周上线 9 个新社区（旧模式数月）",
                    "核心论点：稀缺的不是 agent，是 agent 连什么、拿什么上下文、在什么护栏下工作"],
     "quote": "我们不相信无限制的自主。我们信的是受控的自主"},
    {"video_id": "oVCxf8sI3hA", "url": "https://www.youtube.com/watch?v=oVCxf8sI3hA",
     "title": "Fortinet SD-WAN Underlay and Application Performance Monitoring Service",
     "date": "2026-11-06", "channel": "Fortinet", "lang": "en", "relevance_score": 5,
     "edn_link": "S4/S5 + SaSo", "source_type": "official-video",
     "key_points": ["FortiOS 7.6.4+ APM：被动监听应用会话，自动区分应用/服务器/网络根因",
                    "指标：network response time、server response time、TCP resets、SYN retransmissions",
                    "FortiGuard speed test：对 ISP 链路定时测速，在影响用户前发现瓶颈",
                    "performance SLA 数据库内置 250+ SaaS 目标",
                    "SD-WAN setup wizard 覆盖 underlay 选择、路由、性能 SLA、规则创建"],
     "quote": "只有 hub-spoke 之间测量的方案，对 branch-to-SaaS 流量几乎没用"},
    {"video_id": "KuFRctcpUFc", "url": "https://www.youtube.com/watch?v=KuFRctcpUFc",
     "title": "FortiOS 8.0.1: SD-WAN Load Balancing with Weight-Based Spillover",
     "date": "2026-11-10", "channel": "Fortinet", "lang": "en", "relevance_score": 4,
     "edn_link": "S5", "source_type": "official-video",
     "key_points": ["按隧道权重比例分配新会话，超 ingress 阈值后新会话溢出到其他链路",
                    "阈值控制的是新会话落点，不是隧道带宽上限；已建立会话不迁移",
                    "仅 CLI 支持，GUI 不支持"],
     "quote": "阈值控制的是新会话的落点，不是链路的带宽上限"},
    {"video_id": "Rxmq3Ea3JzQ", "url": "https://www.youtube.com/watch?v=Rxmq3Ea3JzQ",
     "title": "Self-Driving Networks Promise 10x Faster Deployments",
     "date": "2026-11-04", "channel": "Converge Digest / HPE Discover", "lang": "en",
     "relevance_score": 5, "edn_link": "S1 + Agentic Ops + SaSo", "source_type": "official-video",
     "key_points": ["自驾驶网络三指标：部署速度（zero-ticket cutover，10x）、用户投诉数（降 90%）、流程数字化率",
                    "销售方法论即 SaSo：先要客户最差站点，做不到 90% 投诉下降就不用谈",
                    "边缘推理动机：云端 token 成本高，必须在边缘做部分推理",
                    "客户体量：最大零售商、最大在线零售商、最大医疗企业均在用 HPE"],
     "quote": "自驾驶网络 = 部署最快 + 用户工单最少 + 企业最数字化"},
]

vendors = {}
domains = {}
for r in INW:
    e = {k: v for k, v in r.items() if k != "in_window"}
    vendors.setdefault(r["vendor"], []).append(e)
    domains.setdefault(r["domain"], []).append(e)

IMPLICATIONS = {
    "headline": "AI 流量的约束已从带宽转为上行/实时/边缘位置；Agentic Ops 的竞争焦点已从「有没有 agent」转向「agent 连什么数据、在什么护栏下工作」；MCP 成为跨厂商事实标准，agent 成为网络第四类客户端。",
    "top_gap": "跨厂商的 agent 网络接入层 + 跨厂商的 agent 动作护栏 —— 本周无任何厂商覆盖，是 EDN S1+S2 的独占位置，但并购窗口期约 1 个季度。",
    "actions_near": [
        "立项 EDN Network MCP Server：跨厂商、只读、面向 agent 的网络上下文接口（IP/端口/拓扑/链路质量四类起步）",
        "S5 加入上行/下行流量画像与边缘算力位置两个数据维度，依据 Nokia 量化预测重写 SD-WAN 需求文档",
        "S4 验收口径从「能检测到问题」改为「能区分问题出在应用/服务器/网络哪一段」",
        "建立常用 SaaS 应用 SLA 探测目标库（对标 Fortinet 250+），避免只测 hub-spoke",
        "Nile 监控降级为季度，预算转投 Extreme / Mist / Cisco 线",
    ],
    "actions_mid": [
        "设计跨厂商 agent 动作护栏模型：按厂商/对象类型/动作类型定义策略，与 S2 安全编排结合",
        "SaSo 试点：采用 HPE「先要最差站点」入口，选 1 个客户的单个最差分支做可测结果承诺",
        "可观测性数据层 agent 直供接口，作为 S1 差异化标签",
        "S2 增加 AI 应用/agent 流量的识别与策略能力（对标 FortiAIGate 的 tool call 检查）",
    ],
    "actions_long": [
        "把「Agentic Mesh」表述改为强调跨厂商前缀，避免被读成 HPE 跟风",
        "海外纯订阅形态对齐：把 S1 可观测性做成订阅核心卖点而非附属功能",
        "盯住 Extreme 交易结果；若被并购，差异化重心向跨厂商 agent 接入+护栏迁移",
        "国内线单独应对 H3C 的 Token 价值/运维智能体路径",
    ],
    "risks": [
        "Extreme 被 Cisco/Fortinet/NetApp 收购 = 多厂商统一管控位置被大厂直接拿下（本周对 EDN 威胁最大的单一事件）",
        "Arista 2028 年 scale-up 量产 + VeloCloud 可能成为 AI 网络与园区网络的整合者",
        "HPE 的 agentic mesh 已写入 Central 产品页，EDN 落后一个身位",
        "H3C 把运维智能体放进智算链，可能挤占 EDN 国内运营商/政企客户叙事空间",
    ],
}

asset = {
    "week": "2026-11-04 ~ 2026-11-11",
    "generated_at": datetime.now(SH).isoformat(),
    "vendors": vendors,
    "domains": domains,
    "x_signals": XS_FULL,
    "youtube_signals": YT_FULL,
    "edn_implications": IMPLICATIONS,
    "sources_total": len(INW),
    "confidence_breakdown": {"H1": 21, "H2": 12, "H3": 14},
    "capture_stats": {
        "x_attempted": 5,
        "x_kept": 5,
        "x_scrape_calls": 0,
        "x_source": "web_extract",
        "x_note": "SupaData 月度额度在本轮中途耗尽，X 单帖抓取全部由 web_extract 兜底完成（5 条）。未抓 profile 时间线。互动指标仅取到观看数，like/repost/reply 细分数据本轮不可得，已如实留空未推测。",
        "yt_attempted": 10,
        "yt_kept": 5,
        "yt_tool_note": "SupaData transcript 调用 10 次（硬上限）：前 5 次成功（Fortinet APM、FortiOS 8.0.1、HPE Discover ×2、AINetworking26 Extreme），后 5 次因月度额度耗尽返回 HTTP 429 Limit Exceeded。2 条字幕为阿拉伯语（AINetworking26、Extreme 相关），已标注 lang 并保留 —— 内容为 Extreme Agent One 双模式架构与受控自治论述，信息密度高，未降权。剩余 5 个候选视频待下轮补抓。",
        "tvly_queries": 68,
        "web_extract_calls": 9,
        "supadata_scrape_total_today": 0,
        "supadata_transcript_total_today": 10,
        "subagents": {
            "A_west": "79 个 raw Tavily 文件已抢救合并（evidence.json 未写出，阻塞于 SupaData 额度耗尽）",
            "B_north": "39 个 raw Tavily 文件已抢救合并（evidence.json 未写出，阻塞于 SupaData 额度耗尽）",
            "C_east": "母 agent 执行，48 个 raw Tavily 文件 + 5 条 X + 5 条 YouTube 字幕",
        },
        "salvaged_evidence": 268,
        "filter_notes": "已过滤 Nile 撞名噪声（nilecom.ae / Blue Nile / Juniper Hotels 等）、招聘页与无关词条；published_date 缺失的条目单独计数并保留，未使用 d[:10] 切片。",
    },
    "delivery_status": "pending",
    "delivery_error": None,
    "delivery_fallback": None,
    "feishu_doc_primary": "https://ruijie.feishu.cn/docx/Qe1dd7O7XoCAZ9xBeNUc3meLnch",
    "feishu_doc_delivered": None,
}

out = f"/root/.hermes/cron/output/edn-insight-data/{DATE}.json"
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(asset, open(out, "w"), ensure_ascii=False, indent=1)
print("WROTE", out)
print("sources_total:", asset["sources_total"])
print("vendors:", len(vendors), "domains:", len(domains))
print("x:", len(asset["x_signals"]), "yt:", len(asset["youtube_signals"]))
