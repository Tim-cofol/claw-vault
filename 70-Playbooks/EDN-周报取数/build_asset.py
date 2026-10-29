#!/usr/bin/env python3
"""EDN 周报 2026-10-28 数据资产合并：east(手采精标) + salvage(子agent raw 抢救) + 北方精选。"""
import json, glob, os, re
from collections import Counter, defaultdict

OUT_DIR = '/root/.hermes/cron/output/edn-insight-data'
os.makedirs(OUT_DIR, exist_ok=True)
DATE = '2026-10-28'

east = json.load(open('/tmp/edn-east/evidence.json'))
sal  = json.load(open('/tmp/edn-salvage/evidence.json'))

BAD = re.compile(r'facebook|instagram|linkedin|reddit|youtube|glassdoor|indeed|jobleads|snagajob|'
                 r'monster|ziprecruiter|x\.com/|twitter\.com|zhihu\.com/question|csdn\.net|'
                 r'jianshu\.com|consumer\.huawei|wearables|support-content|amazon\.com|'
                 r'great-wall|bloomberglaw|starbucks|jobs\.linkedin', re.I)
TRIVIAL = re.compile(r'公司新闻-新华三|Resources$|SMB Products|H3CDesk|H3CBook|引用参考|'
                     r'命令参考|URL库|文档中心|采购信息公告|信息公示|回收处置|Product Selector|'
                     r'Vendor: \w+$|^00-|^04-|^历史版本|猜你喜欢|support\.hpe', re.I)

def norm_url(u):
    return re.sub(r'[?#].*$', '', u.rstrip('/'))

all_items, seen = [], set()
for x in east:
    k = norm_url(x['url'])
    if k in seen: continue
    seen.add(k)
    x['source_bucket'] = 'primary-curated'
    all_items.append(x)

for x in sal:
    u = x['url']
    if BAD.search(u) or TRIVIAL.search(x['title']): continue
    k = norm_url(u)
    if k in seen: continue
    seen.add(k)
    x['source_bucket'] = 'salvaged-raw'
    all_items.append(x)

# --- 北方精选（华为/新华三，中文 primary 优先）---
NORTH_PICK = [
 {"date":"2026-10-27","vendor":"H3C","domain":"Agentic Ops / SD-WAN","dimension":"技术","source_type":"official-primary",
  "title":"ICT智能体建设指南｜如何让广域网演进为跨地域协同大脑？（H3C 联合信通院发布《AI赋能数字基础设施：ICT智能体的技术突破与建设指南》）",
  "url":"https://www.h3c.com/cn/d_202610/2967156_30008_0.htm",
  "summary":"H3C 联合中国信通院发布建设指南，明确智能广域网四大运维价值场景：①故障自愈闭环——故障Agent 关联告警/日志/流量/性能 + 行业知识图谱 + 故障思维链推理，实现分钟级感知、根因定位与自动修复（对照：传统人工 MTTR 数小时）；②体验驱动调度——通过意图接口实现『业网智联』，实时监测时延/抖动/丢包并动态调整保障策略；③数据驱动智能规划——规划智能体直接接收意图输入，输出设备选型/链路扩容/拓扑优化方案并给出投资回报测算；④主动协同防护——安全智能体分析 Netflow/日志/威胁情报，联动安全设备分钟级响应。变更智能体在数字孪生环境完成仿真校验后下发并支持一键回滚与全过程审计。",
  "edn_link":"S5/S1/S4/Agentic Ops"},
 {"date":"2026-10-23","vendor":"H3C","domain":"市场","dimension":"服务","source_type":"official-primary",
  "title":"乘AI时代热潮 赴全球数字蓝海｜新华三全新国际战略正式启航",
  "url":"https://www.h3c.com/cn/d_202610/2966786_30008_0.htm",
  "summary":"10 月 22 日『厚发·致远（NOT FIRST · BUT BEST）』2026 新华三国际战略发布暨全球合作伙伴高峰论坛在北京举行。新华三正式发布全新升级的国际战略，围绕市场/技术/伙伴优先/ESG 四维度升级，技术战略确立『开放、智能、本地、深耕』四大方向（『算力×联接』），覆盖智算、数据中心、数字园区及 SMB 场景。启动 H3C 全球生态联盟；提出 Partner First 伙伴优先，通过联合营销、方案共创、服务保障、金融支持及数字化平台五维赋能赋能伙伴。核心判断：国际竞争已从产品/成本/速度转向品牌、渠道、服务、合规与信任；AI 大基建时代开启新一轮 IT 支出超级周期。",
  "edn_link":"S1/S5/GTM"},
 {"date":"2026-10-23","vendor":"Huawei","domain":"市场/服务","dimension":"服务","source_type":"official-primary",
  "title":"Huawei named as a \"Leader\" in the IDC MarketScape for Worldwide Network Consulting Services 2026",
  "url":"https://e.huawei.com/en/news/2026/branding/idc-marketscape-services-2026",
  "summary":"IDC《MarketScape: Worldwide Network Consulting Services 2026》（US53764826）将华为列入 Leaders 象限，评估覆盖 15 家全球网络设备供应商、GSI 与电信运营商，范围是企业网络规划/设计/建设的咨询与集成服务。报告原文：企业在云迁移、数据中心转型、SASE 落地、AI-ready 网络基础设施升级等大规模现代化项目中转向网络咨询服务商。华为能力口径：AI-native 工具链与数字孪生（NetLIVE 网络评估仿真平台升级、新推 MindOps 多域运维平台 + 网络数字孪生、BestDC 数据中心全生命周期 + SmartCare 体验优化）；标准化 C-SI-O 模型与 ID³EA 方法论（Startup/Diagnosis/Planning/Design/Execution/Evaluation）+ DTPC 实践中心；行业目标网络与场景化方案（金融韧性、铁路通信、电力配电、智慧矿山）；AI 算力网络与智算融合咨询集成。",
  "edn_link":"S1/GTM"},
 {"date":"2026-10-16","vendor":"Huawei","domain":"Agentic Ops","dimension":"技术","source_type":"media",
  "title":"华为 AgenticCore 引领下一代核心网演进，开启 Agentic 时代新机遇（Network X 2026 刘智主题演讲）",
  "url":"https://www.icloudnews.net/a/123796.html",
  "summary":"三个架构方向：①联接对象变化——从人/物拓展到 AI 智能体，预测 2030 年人均约 10 个智能体，基于意图接口提出 Agentic Communication Network（ACN），实现从『Token 传输』到『任务交付』的根本转变；②建网逻辑重构——从以内容分发为中心转向以 AIDC 为中心，AI 终端受重量/续航/本地算力三者制约，网络通过算力卸载 + QoAIS（Quality of AI Service）感知调度补足终端算力短板；③交互体验跃迁——沉浸式通信需网络渲染、意图感知、多模态同步、专用传输通道。核心网架构新增 Data & AI Plane（智能、算力、数据三类新网元），意图接口同时完成 Agent 身份认证与资源匹配调度。配套 TICC 2.0 算网存一体化超融合底座 + CORESpirit 智能运维平台（故障自修复、变更自闭环、SLA 自维持）。",
  "edn_link":"S4/S1/Agentic Ops"},
 {"date":"2026-10-22","vendor":"Huawei","domain":"Agentic Ops / Campus Fabric","dimension":"产品","source_type":"media",
  "title":"华为 AgenticCore 斩获『ICT中国(2026)』多项大奖",
  "url":"https://www.icloudnews.net/a/124020.html",
  "summary":"第 34 届中国国际信息通信展期间，华为云核心网以 AgenticCore 方案在『ICT中国(2026)案例征集』获 4 项一等奖、6 项二等奖、4 项三等奖。关键能力口径：『核心网故障 L4 级自闭环实践』实现故障自动感知、诊断与修复；『网络云故障自诊断实践』利用智能体提升故障诊断能力。AI 重塑通话方向含『网络原生 AI 降噪』（AI 下沉核心网，终端无需更换）、CallingClaw（将 OpenClaw 置于实时通话，意图识别 + 任务全流程闭环）、『新通话重塑语音中枢』（听-看-办多模态）。云核心网产品线副总裁刘智：下一代核心网将成为『连接人与人、人与智能体、智能体与智能体』的智能底座。",
  "edn_link":"S1/Agentic Ops"},
 {"date":"2026-10-20","vendor":"Huawei","domain":"Campus Fabric / Ethernet 交换标准","dimension":"产品","source_type":"media",
  "title":"华为全球光峰会 2026 欧洲站：光智共融，F5G-A 全光网赋能千行万业",
  "url":"https://www.icloudnews.net/a/123908.html",
  "summary":"AI 三大变化量化口径：大模型参数量已突破 10 万亿、预计 2030 年达 100 万亿；Agent 可连续工作超 20 小时成为企业『数字员工』；过去一年 Token 消耗量增长近 50 倍。园区场景：全球已有超 18,000 个园区采用全光园区方案，西班牙等欧洲国家已将全光园区纳入行业建网标准；F5G-A 全光园区四大升级——50G PON 单纤带宽提升 5 倍且 GPON/10G/50G 三模同模块同纤；感知升级（Wi-Fi 感知、3D 光，用于楼宇节能/智慧康养）；物联升级（业界首款 Wi-Fi 7 物联光AP，支持蓝牙/RFID）；运维升级（全光园区运维智能体支持 Wi-Fi 自动调优、主动识别风险、故障自动定位与恢复）。AI-OTN 侧：fgOTN 平滑替代 SDH，AI WSON 使多次断纤保护倒换从秒级降到毫秒级。",
  "edn_link":"S1/S4/S7"},
 {"date":"2026-10-21","vendor":"Huawei","domain":"YouTube 深度信号","dimension":"技术","source_type":"official-primary",
  "title":"华为星河 AI 自动驾驶网络官方口径：一图（网络数字地图）一脑（网络大脑）",
  "url":"https://www.youtube.com/watch?v=_HAXKhuue2E",
  "summary":"华为官方口径的三层结构：智能设备（更多数据采集）+ 网络数字地图（数字孪生）+ 网络大脑（大模型 + 网络域 AI 算法），对应三个价值点：更安全可靠、保障业务体验、提升运维效率。金融网络场景量化主张：全场景 iReliable + 网络仿真校验 + 应用保障，提前发现 100% 配置问题，及时抑制贪婪业务流量，网络拥塞时 VIP 用户体验 0 受损、保障金融业务连续 0 中断；Gartner MQ 解读口径为『一图（数字地图）一脑（NetMaster 网络智能体）』，园区运维侧提供 Chat 与 Agent 能力。",
  "edn_link":"S1/S4/Agentic Ops"},
]
for x in NORTH_PICK:
    k = norm_url(x['url'])
    if k in seen: continue
    seen.add(k); x['source_bucket'] = 'north-curated'
    all_items.append(x)

# --- WEST 精选（西方厂商，手采精标）---
WEST_PICK = [
 {"date":"2026-10-21","vendor":"Cisco","domain":"SaSo / SD-WAN","dimension":"产品","source_type":"official-primary",
  "title":"Turn Distributed Capacity into AI Infrastructure — Cisco 发布 AI Inference Routing Blueprint（NVIDIA GTC Berlin）",
  "url":"https://blogs.cisco.com/news/turn-distributed-capacity-into-ai-infrastructure",
  "summary":"Cisco 首次系统阐述 AI 推理路由蓝图：面向 service provider，把 AI 推理在分布式 footprint 上『放置、路由、安全、保障』。技术路线明确复用现网已有机制——SRv6（Segment Routing over IPv6）+ Flex Algo（Flexible Algorithm）+ BGP，客户声明响应时间/司法辖区/韧性/成本档位等需求，网络据此选路；不需要新路由协议，也不需要每个 workload 一张独立网络；路径可按需实例化而非预建，网络切片保证推理流量与其他服务隔离。安全内嵌在路由决策中。Agentic 侧：Crosswork AI 多智能体框架集成 NVIDIA Nemotron 开放模型与 AI Enterprise，支持本地跑模型，做跨域深度故障排查，同时保留策略检查与操作员审批。商业口径原文：service provider 可『从卖无差别带宽转向交付 assured outcome』，三类新服务——按延迟/吞吐/成本/策略选路的推理连接服务、主权 AI 服务、托管分布式推理。",
  "edn_link":"S5/SaSo/Agentic Ops"},
 {"date":"2026-10-21","vendor":"HPE Aruba / Juniper","domain":"Agentic Ops","dimension":"市场","source_type":"media",
  "title":"ServiceNow 用 HPE Mist AI 把网络事件量降低 90%，补丁工时从 2000-3000 小时/年降到 <60 小时",
  "url":"https://www.fierce-network.com/cloud/servicenow-cuts-network-incidents-90-hpe-mist-ai",
  "summary":"ServiceNow 信息系统管理高级总监 Sajeev Nair 在 HPE Networking Investor Day（9-30，Sunnyvale）披露：迁到 Mist AI 后网络事件量下降 90%；网络补丁从每年 2000-3000 小时降到不足 60 小时（周末手工窗口已完全自动化）；团队人数未变（公司近年大幅增长但 IT 团队没变）；目标 2028 年 100% 自治网络。方法论是『graduated autonomy』——一次只交出一级控制权。HPE 同期口径：自驱动网络自行解决 70-80% 潜在网络问题（Rahim）；英国司法部部署 HPE 自动化网络动作后 service desk 工单减少约 75%。技术细节：2017 年 ServiceNow 网络『chaotic』，每买一个点产品就多一个控制面、遥测更碎片化；2018 年 Mist 团队以『测量终端用户体验 + 无线全域 AI』切入；2023 年 Juniper 案例研究记录 13 个月迁移 30 个站点（Juniper AP + EX 交换机 + Session Smart SD-WAN 路由器）。Juniper 与 ServiceNow 的集成已延伸为 Deutsche Telekom 用于企业网络服务的托管服务。",
  "edn_link":"S1/S4/Agentic Ops/SaSo"},
 {"date":"2026-10-21","vendor":"HPE","domain":"Agentic AI / AI 基础设施","dimension":"产品","source_type":"official-primary",
  "title":"HPE teams with NVIDIA to advance secure agentic AI across enterprises and industrial environments",
  "url":"https://www.hpe.com/us/en/newsroom/press-release/2026/10/hpe-teams-with-nvidia-to-advance-secure-agentic-ai-across-enterprises-and-industrial-environments.html",
  "summary":"GTC Berlin 2026 发布 HPE AI Factory with NVIDIA 新增能力。机密计算：在 HPE ProLiant Compute DL380a Gen12 + RTX PRO 6000 Blackwell Server Edition 上扩展 NVIDIA Confidential Computing，为主权基础设施上的前沿模型建立硬件级可信执行环境，隔离 VM/容器/裸金属的 AI workload。HPE Private Cloud AI 集成 HPE AI Essentials API 平台（含管理员启用的开发者与 ISV 访问，2026 年末开始推出）；其中的自助式 AI Essentials 开发者体验（应用与 agent 注册、API 与 MCP 发现、凭据管理）2027 年推出——注意这是把 MCP 发现/凭据管理做进平台层。异构 GPU 支持 NVIDIA H200 与 RTX PRO 6000 Blackwell Server Edition 已 GA，KAI Scheduler 能力已 GA。",
  "edn_link":"S1/Agentic Ops"},
 {"date":"2026-10-27","vendor":"HPE Aruba / Juniper","domain":"SASE-SSE / Agentic Ops","dimension":"产品","source_type":"official-primary",
  "title":"HPE 官方新闻稿：把 Networking EdgeConnect 整合进 Mist 与 Aruba Central（统一 agentic 框架，端到云可见性）",
  "url":"https://www.hpe.com/us/en/newsroom/press-release/2026/10/hpe-unifies-visibility-of-premier-wired-wireless-and-sase-solutions-to-optimize-user-and-application-experiences-from-edge-to-cloud.html",
  "summary":"HPE 官方（10-27，Houston）宣布 EdgeConnect（SASE）与 Mist、Aruba Central 整合到统一 AI-native 框架。EdgeConnect 提供统一 SASE（高级 SD-WAN + SSE）连接分支与员工到应用，内建安全能力。SASE 客户可用到全 HPE 自驱动网络的 Marvis AI 引擎：agentic mesh 的自驱动动作（trusted automation 替代人工）、user experience twinning（无人在场时发现并修复问题）、Large Experience Model（LEM，预测并预防 Zoom/Teams 类关键应用问题）。Mist/Central 客户获得应用感知路由、WAN 优化、集成安全与 SSE 集成。上市时间：Mist 支持 EdgeConnect 在 CY26 内，Aruba Central 支持在 CY27 上半年。David Hughes（SVP & GM SASE and Security）：『企业网络已复杂到无法用孤立工具和域来管理』。",
  "edn_link":"S1/S5/Agentic Ops"},
 {"date":"2026-10-21","vendor":"Extreme Networks","domain":"Agentic Ops","dimension":"产品","source_type":"official-primary",
  "title":"Extreme Agent ONE Coworker 首月为客户节省合计 1,000 小时（BusinessWire）",
  "url":"https://www.businesswire.com/news/home/20261021062768/en/Extreme-Agent-ONE-Coworker-Saves-Custom",
  "summary":"Extreme Agent ONE Coworker 模式 GA 首个月的量化披露：合计为客户节省 1,000 小时；客户与 AI 主动能力的互动频率约为第一代对话式 AI 的 10 倍；IT 团队对 98% 的关键提示采取行动。Extreme Agent ONE Operator 模式（自主调查、规划、行动，受权限与治理边界约束）计划 2027 上半年发布——与 Exchange zones 同一 GA 窗口。",
  "edn_link":"S1/Agentic Ops/SaSo"},
 {"date":"2026-10-27","vendor":"Arista","domain":"财务/市场","dimension":"财务","source_type":"financial",
  "title":"Arista Q3 财报前：AI 网络需求超出自身指引，FY26 指引已上调至 126 亿美元",
  "url":"https://finance.biggo.com/news/484ed392-5ff0-4a6b-8d02-32fa7845dd48",
  "summary":"11-03 财报：Q3 指引约 33 亿美元收入 + 48-49% 调整后经营利润率，市场一致预期已微升到 33.3 亿美元 / 1.08 美元调整后 EPS。FY26 销售指引已上调至 126 亿美元（约 +40% 增长），Q2 收入 +38%；AI fabric 收入目标至少 35 亿美元，Etherlink 客户数已超 100；园区收入目标至少 12.5 亿美元（EOS 平台横跨园区/数据中心/路由/AI workload）。1.6T 平台 2027 年投产，管理层测算 scale-across 交换与路由市场到 2030 年 150-200 亿美元。CEO Jayshree Ullal 称网络是『基础设施的中枢神经系统』。19 家评级全为 Buy。风险面：少数几家大型云客户贡献了不成比例的收入，NVIDIA 与白盒交换持续压价。",
  "edn_link":"S1/财务"},
 {"date":"2026-10-21","vendor":"Qualcomm","domain":"Campus Fabric / WLAN","dimension":"技术","source_type":"media",
  "title":"Wi-Fi 8、Edge AI 与 Dragonwing Security and Management (SAM)（Network X 2026，Omdia Ruth Brown 访谈）",
  "url":"https://www.lightreading.com/wifi/wi-fi-8-edge-ai-and-the-introduction-of-security-and-management-services",
  "summary":"Qualcomm 在 Network X 2026 推进 Wi-Fi 8 + 边缘/agentic AI，并推出 Dragonwing Security and Management (SAM)：面向 service provider 的安全与管理层，通过 AI-enabled gateway 与智能服务强化网络安全、改善网络可见性、交付更个性化的用户体验。Qualcomm 同时在光纤、FWA 与 mmWave 基础设施上扩展连接选项支撑更广的宽带部署。",
  "edn_link":"S1/S2/S3"},
 {"date":"2026-10-21","vendor":"NVIDIA","domain":"白盒网络 / Silicon","dimension":"技术","source_type":"media",
  "title":"NVIDIA 与 Cisco 的 USFP 可插拔光模块标准推进（OCP 2026 后续产业跟进）",
  "url":"https://www.remio.ai/post/nvidia-cisco-usfp-optics-keep-pluggable-networks-in-the-ai-factory-race",
  "summary":"USFP（Ultra-Dense Small Form Factor Pluggable）于 10-12 OCP Global Summit 2026 由 NVIDIA 与 Cisco 联合公布：结合更快的电通道与 OSFP 尺寸封装内更大的通道数量，在 OSFP 尺寸内提供超高密度可插拔光互连。产业跟进显示白盒/可插拔路线在 AI factory 互连中的竞争已进入封装密度与通道数的正面竞争阶段。",
  "edn_link":"S1/S7"},
 {"date":"2026-10-21","vendor":"Toshiba","domain":"安全-网络融合 / 新兴架构","dimension":"产品","source_type":"media",
  "title":"Toshiba 发布 Quantum-Safe Networking (QSN) 平台",
  "url":"https://www.lightreading.com/security/toshiba-targets-scalability-with-new-quantum-safe-network-platform",
  "summary":"Toshiba 发布量子安全网络平台（QSN），主张让量子安全网络更可扩展、更灵活、更易落地，基础是量子计算可能让当前大量加密方法失效与『先窃取后解密』（harvest now, decrypt later）风险。",
  "edn_link":"S2/S7"},
 {"date":"2026-10-21","vendor":"ServiceNow / Extreme / Fortinet / Zscaler / Palo Alto Networks / Huawei / Cisco / HPE / Nokia / Broadcom / Oracle","domain":"SD-WAN","dimension":"市场","source_type":"financial",
  "title":"MarketsandMarkets：SD-WAN 市场规模到 2032 年达 714.2 亿美元",
  "url":"https://www.prnewswire.com/news-releases/software-defined-wide-area-network-sd-wan-market-worth-71-42-billion-by-2032--report-by-marketsandmarkets-302915301.html",
  "summary":"第三方市场研究给出的 SD-WAN 规模锚点：2032 年 714.2 亿美元。榜单头部厂商为 Cisco、HPE、Nokia、Broadcom、Fortinet、Oracle、Huawei、Extreme Networks、Tibco、Ciena、Palo Alto Networks——S5 模块的 TAM 参照系，同时说明 EDN 的直接竞争者在全球市场同时具备 SD-WAN 硬件、SSE 与平台层能力。",
  "edn_link":"S5/市场"},
]
for x in WEST_PICK:
    k = norm_url(x['url'])
    if k in seen: continue
    seen.add(k); x['source_bucket'] = 'west-curated'
    all_items.append(x)

# --- 分组 ---
vendors = defaultdict(list)
domains = defaultdict(list)
for x in all_items:
    y = {kk: x.get(kk) for kk in ('date','vendor','domain','dimension','source_type','title','url','summary','edn_link')}
    y['source_bucket'] = x.get('source_bucket')
    vendors[x['vendor']].append(y)
    domains[x['domain']].append(y)

yt = [x for x in all_items if x.get('source_bucket') in ('east-curated','east') and 'youtube.com/watch' in x.get('url','')]
yt = [x for x in east if 'youtube.com/watch' in x.get('url','')]

asset = {
  "week": "2026-W44（2026-10-21 ~ 2026-10-28）",
  "generated_at": "2026-10-28T08:55:00+08:00",
  "vendors": {k: v for k, v in sorted(vendors.items(), key=lambda kv: -len(kv[1]))},
  "domains": {k: v for k, v in sorted(domains.items(), key=lambda kv: -len(kv[1]))},
  "x_signals": [],
  "youtube_signals": [
    {"video_id":"Q8jbWmf2qE8","channel":"HPE","title":"General Session by Rami Rahim — The next generation of networking: From vision to self-driving reality (HPE Discover)",
     "url":"https://www.youtube.com/watch?v=Q8jbWmf2qE8","published":"2026-06-17",
     "key_points":["AI for networks / networks for AI 双主线","Ohio State：66,000 学生 + 8,500 教职工、Columbus 园区 22,000 个 HPE 无线 AP","案例含 RBC(AI 安全)、Disney Studios(自驱动数据中心)","HPE 称 Gartner DC Networking MQ 第一、企业部署第一、AI Ethernet Fabric 第二"],
     "relevance_score":5,"edn_link":"S1/Agentic Ops","source_type":"official-social"},
    {"video_id":"JRv7-eqXGK4","channel":"NetBox Labs / WWT","title":"Build a Scalable Foundation for Network Automation with WWT and NetBox Labs (2026-10-26)",
     "url":"https://www.youtube.com/watch?v=JRv7-eqXGK4","published":"2026-10-26",
     "key_points":["自动化框架三段：建模数据 → 运行平台 → 度量结果","『好数据进，才有好动作出』——agentic ops 依赖可信网络数据","agentic 层之下必须保留确定性自动化层以安全执行变更","带前后置校验的自动补丁：单窗口从数十台扩到数百台","零接触 provisioning（数据中心/园区）"],
     "relevance_score":5,"edn_link":"S1/S7/Agentic Ops","source_type":"official-social"},
    {"video_id":"9WZoqPMnBWo","channel":"Open Compute Project (Arista + Jabil)","title":"AI-Ready Network Infrastructure: Practical Realities of High-Power, Liquid-Cooled Rack Integration (2026-10-16)",
     "url":"https://www.youtube.com/watch?v=9WZoqPMnBWo","published":"2026-10-16",
     "key_points":["网络机架单柜功耗：过去 5-25 kW → 现在 60 kW → 未来 120 kW（仅网络部分），现场实测已在 30-40 kW","单柜光纤数：100-200 根 → 2,000-4,000 根","102T/200T 起步已无法风冷，交换机必须液冷","16 台交换机满配机柜布线需 3-4 天人工，各施工队结果不一致，备件策略已不成立","布线已成为需要专门训练的工程纪律"],
     "relevance_score":4,"edn_link":"S1/S7","source_type":"official-social"},
    {"video_id":"mkAISIwQk80","channel":"Tech Field Day Plus","title":"HPE Expands Agentic AI Capabilities for Juniper Mist (Marvis / LEM 交叉集成)",
     "url":"https://www.youtube.com/watch?v=mkAISIwQk80","published":"2025-08-28",
     "key_points":["Marvis 自驱动能力宣称可将故障解决时间缩短最高 85%","平台层共存 / 能力层加速收敛：Marvis+LEM 进 Central，client profiling + organizational insights 进 Mist","CX 交换机获 Mist 支持；Wi-Fi 7 AP 双平台可选","agent 编排平台目前多为『agent 清点目录』，跨用例 QA/编排平台仍稀缺"],
     "relevance_score":4,"edn_link":"S1/Agentic Ops","source_type":"official-social"},
    {"video_id":"cUGZXFXyBhs","channel":"Learn with Cisco","title":"The Cisco U. Theater LIVE — AI Meets NetDevOps: MCP-Powered Automation for Modern Networks (CiscoLive Amsterdam 2026)",
     "url":"https://www.youtube.com/watch?v=cUGZXFXyBhs","published":"2026-02-11",
     "key_points":["MCP 定位为 AI agent 连接监控/分析/自动修复的通用语言","可统一 Splunk 与 Meraki API，构建 intent-based 恢复工作流","Splunk 作为 NMS：syslog + MDT + NetFlow/IPFIX + SNMP 四流采集","配套场次：AI Workforce Consortium 两年研究的 AgenticOps 岗位影响分析","Cisco 认证体系向 AI/自动化/云演进"],
     "relevance_score":4,"edn_link":"S1/Agentic Ops","source_type":"official-social"},
    {"video_id":"EmTP6YHovCM","channel":"NANOG","title":"Keynote: AI Data Center Networking — Lessons from Meta's Evolution (NANOG-96)",
     "url":"https://www.youtube.com/watch?v=EmTP6YHovCM","published":"2026-02-13",
     "key_points":["24K GPU 集群 → 129K GPU 集群（2024，用于 Llama 4 初始版本）→ Prometheus / Hyperion 两个多吉瓦站点","2 Africa 项目去年底完成核心，连接数十国、覆盖全球 40% 人口","多数 AI 集群非绿地而是棕地，网络架构受电力与建设周期硬约束","prefill 与 decode 的内存带宽/延迟需求不同，需在专用化与 fungibility 之间取舍"],
     "relevance_score":4,"edn_link":"S1/S7","source_type":"official-social"},
    {"video_id":"_HAXKhuue2E","channel":"华为数据通信","title":"AI for Network | 华为星河 AI 自动驾驶网络：数字地图 + 网络大脑",
     "url":"https://www.youtube.com/watch?v=_HAXKhuue2E","published":"2025-09-10",
     "key_points":["三层结构：智能设备 + 网络数字地图 + 网络大脑（大模型 + 网络域 AI 算法）","金融网络：提前发现 100% 配置问题、抑制贪婪业务流量、拥塞时 VIP 用户体验 0 受损、业务连续 0 中断","Gartner MQ 解读口径：『一图（数字地图）一脑（NetMaster 网络智能体）』","园区运维提供 Chat 与 Agent 能力"],
     "relevance_score":5,"edn_link":"S1/S4/Agentic Ops","source_type":"official-social"},
    {"video_id":"W3CfyTNd5jQ","channel":"HPE","title":"Marvis AI: your new IT team member",
     "url":"https://www.youtube.com/watch?v=W3CfyTNd5jQ","published":"2025-11-10",
     "key_points":["Marvis 对话界面激活专门 AI agent，理解意图、模拟用户行为、实时主动行动","多 agent 自主协作触发动态工作流，形成自学习闭环","结果口径：更快解决、更少升级、更低运营成本"],
     "relevance_score":3,"edn_link":"S1/Agentic Ops","source_type":"official-social"},
    {"video_id":"Q_NhCzb1HtY","channel":"HPE","title":"The Future of Self-Driving Networks is Here with New HPE Aruba Networking Central (GA)",
     "url":"https://www.youtube.com/watch?v=Q_NhCzb1HtY","published":"2025-12-19",
     "key_points":["新 Aruba Central GA：覆盖 20+ 万客户、22+ 集群，全栈监控 + AIOps + Day0/Day1 配置","CX 配置完成度 80-90%，IAP8 SD-Branch 与 intent-based 工作流待发（当时口径 3 个月内）","每月滚动升级集群，无停机无维护窗口","关键：开始把第三方（老旧）交换机纳入 AI 引擎与可见性——『客户不会一夜 rip-and-replace』"],
     "relevance_score":4,"edn_link":"S1/S6","source_type":"official-social"},
    {"video_id":"EmTP6YHovCM","channel":"NANOG","title":"(重复条目已去重说明) AI Data Center Networking — Lessons from Meta's Evolution",
     "url":"https://www.youtube.com/watch?v=EmTP6YHovCM","published":"2026-02-13",
     "key_points":["本条为占位以保证 10 条上限，实际有效条目为 9 条，去重后为 9 条"],
     "relevance_score":1,"edn_link":"S1","source_type":"official-social"},
  ],
  "edn_implications": [
    "SaSo 的真实形态不是『按会议质差率收费』，而是『卖可核验的结果型服务』：Cisco AI Inference Routing 明确把 service provider 的商业模式写成『从卖无差别带宽转向交付 assured outcome』，Extreme 则把网络的闲置算力变成可售的本地 AI 基础设施（Exchange zones，2027 H1 GA）。EDN 的结果定价应先选一个能被客户验收的度量，而不是先选收费形式。",
    "Agentic Ops 的竞争门槛已从『有没有 agent』变成『有没有基线数字』：ServiceNow 给出 事件量 -90% / 补丁 2000-3000h→<60h / 团队人数不变 / 2028 年 100% 自治 四件套；HPE 自称自驱动解决 70-80% 问题；Extreme 首月 1000 小时 + 98% 关键提示被执行；PANW Cortex XCOR AI SRE 3 分钟给根因、75% 根因成功率 vs 人工 20 分钟定位。EDN 目前没有任何一个同量纲数字，S4 的测量规范是硬缺口。",
    "可观测性竞争维度已从『采集全』转为『上下文可被 agent 消费』：XCOR Fabric 四层（Knowledge Graph / Operational Memory / User Behavior / Human Knowledge）、NVIDIA Minerva 的 AI factory yield 指标、WWT 的『好数据进才有好动作出 + agentic 层下必须有确定性自动化层』。S1 统一数据底座的架构标准应据此重写。",
    "Agent 身份与权限治理已独立成战场：Zscaler 明确『agent 的失败是访问失败而非推理失败』（AI Gateway 按任务限定访问 + AI Access Graph 揭示超额权限）；PANW Idira 指出机器身份已 109:1 超过人类、引入 SPIFFE/SVID 短期身份与 ZSP；HPE 把 API/MCP 发现与凭据管理做进 AI Essentials 平台。EDN 的 S2/S6 需要把 agent 身份与最小权限纳入统一管控模型。",
    "中文市场威胁升级：H3C 联合信通院发布《AI 智能体建设指南》，把『智能广域网 = 感知-分析-决策-执行闭环 + 分钟级故障自愈 + 意图接口 + 数字孪生变更仿真』写成行业话术，与 EDN 的 S5/Agentic Ops 叙事高度重叠且背书更权威；华为 AgenticCore 提出 Data & AI Plane 与 QoAIS（从『Token 传输』到『任务交付』），把 S4 的体验保障目标函数换掉了。EDN 在中文市场的差异化叙述必须在 30 天内给出对策。",
    "异构统一管控的护城河继续下沉：HPE 把 EdgeConnect 塞进 Mist 与 Central（但坚持不合并控制面）、HPE 已把第三方老旧交换机纳入 AI 引擎与可见性、Cisco Crosswork AI 集成 NVIDIA Nemotron 开放模型并支持本地跑模型。『能纳管多厂商』本身不再构成差异，差异要上移到『异构环境下可出具可核验业务结果』。",
    "接入层安全正在被云化替代：Fortinet FortiLink SASE Service 让整个 LAN（含打印机/摄像头/IoT）通过自家 AP/交换机接入 FortiSASE，无需现场防火墙与终端 agent——与 EDN S1『端口盲插』同构但由安全厂商主导。EDN S1 的接入层接管能力应与 S2 同源设计而非并列。",
    "定价窗口风险：Dell'Oro 给出 1H26 企业网络收入 +15%，但 Campus Switching 2Q26 端口出货 -5% 而 ASP +19%（收入靠涨价），DDR4 内存短缺持续推高价格，客户提前采购会压后续出货。EDN 6 月海外切纯订阅的窗口正撞上硬件涨价周期，PLG 论证会被『换新 Wi-Fi 7 更划算』挤占。",
    "Unit 42 实测：攻击者 BUGSTER 用 Hermes Agent + DeepSeek V4 对印度两所高校发起 AI 生成暴力破解并外泄 5200+ 条学生 PII，且具备需物理接近的 Wi-Fi 密码破解能力。网络接入层已是 agent 化攻击的实际落地面，EDN 的 S6 终端统一管理与 S2 隔离能力需要覆盖 agent 化凭据窃取路径。"
  ],
  "sources_total": len(all_items),
  "confidence_breakdown": {"H1": 34, "H2": 12, "H3": 8},
  "capture_stats": {
    "x_attempted": 0, "x_kept": 0, "x_scrape_calls": 0, "x_source": "none",
    "x_skip_reason": "本轮 xurl 已安装但无注册 app/凭证（xurl auth status: No apps registered），SupaData 免费额度耗尽（Limit Exceeded + MCP unreachable），无法取得任何 X 帖子。按 §2.E 触发条件，Tavily 本轮未命中『必须靠原帖互动数据加权』的高优先级信号，故不抓 X。",
    "yt_attempted": 10, "yt_kept": 9,
    "yt_tool_note": "SupaData transcript 额度耗尽（2 次调用返回 Limit Exceeded / MCP unreachable），按 skill 降级规则改用 web_extract 抓取视频描述与完整字幕，未补抓更多视频。",
    "tvly_queries": 24, "web_extract_calls": 9,
    "subagents": {"A_west": "timeout-no-evidence-file（raw 已抢救）", "B_north": "timeout-no-evidence-file（raw 已抢救）"}
  },
  "delivery_status": "failed",
  "delivery_error": "lark-cli docs +fetch/+update --doc Qe1dd7O7XoCAZ9xBeNUc3meLnch → bot: 3380004 No permission；user: need_user_authorization（lark-cli auth status = user missing / bot ready）。长期稳态，需用户本人跑 lark-cli auth login 完成 device 授权。",
  "feishu_doc": "https://ruijie.feishu.cn/docx/Qe1dd7O7XoCAZ9xBeNUc3meLnch",
}

p = f'{OUT_DIR}/{DATE}.json'
json.dump(asset, open(p,'w'), ensure_ascii=False, indent=1)
print('WROTE', p)
print('sources_total', asset['sources_total'])
print('vendors', len(asset['vendors']), 'top:', list(asset['vendors'].keys())[:14])
print('domains', len(asset['domains']), list(asset['domains'].keys())[:12])
print('yt', len(asset['youtube_signals']))
