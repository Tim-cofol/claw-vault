# 2026-11-22 Latent Space｜Linear COO Cristina Cordova 谈 GTM 做到 $100M ARR（逐字稿）

- 来源：Latent Space 播客（YouTube）
- 页面：https://www.youtube.com/watch?v=x0VSm6IjcDQ
- 标题：Scaling Linear's GTM to $100M ARR — Cristina Cordova, COO
- 嘉宾：Cristina Cordova（Linear COO）
- 发布：2026-11-19（UTC）
- 产出时间：2026-11-22 08:00（早报 autopilot 当日跑通时落地）
- 归档时间：2026-11-22（日报 cron 档 1 自动归档，生成物改名为 `/tmp/digest_raw.json`）
- 体量：约 93,500 字符完整逐字稿

---

## 这期在讲什么

Linear COO 讲三件事：

1. **"issue tracking 已死"不是产品宣言，是业务事实**——Linear 自己的博客把这句话推成行业口号，COO 在播客里承认它是客户反馈驱动的：客户不再问「你们是什么」，而是问「issue tracking 都死了，我买的是什么」。
2. **Agent 已经在真实业务里承担创建工作量**——Linear 上超过 50% 的 issue 由 agent 创建；MCP 使用曲线与 App 使用曲线同时上升。
3. **AI 预算泡沫的判断**——现在客户在试、签一年合同甚至做 pilot，不会签三年。

另有一条数据点：Linear 三年半没有因为客服体验收到过一次升级投诉。

## 对我的系统/工作的启发

- **"超过 50% 的 issue 由 agent 创建"这条可以直接搬到 Hermes 的工作流判断上**：agent 承担的是"创建"，人负责"判断和收尾"。Hermes 现在的日报流程正是这个形状——采集、建档、git push、同步都可自动，但"这件事该不该闭环"始终留给人拍板。这个分工不需要每次重新论证，写成默认假设即可。
- **"三年半零升级投诉"是一条比 ARR 更硬的护城河指标**。映射回 Hermes：真正难被替代的不是"跑得快"，是"出问题时的兜底路径"。日报 cron 连续多天在同一位置失守（用户授权缺失、状态库膨胀），说明兜底路径本身要定期演练。
- **对 AI 预算泡沫的判断（只签一年，不签三年）适用于供应商/工具选型**：任何需要承诺三年以上的依赖，都要按"一年一议"来设计退出路径。

## 可落地动作

- 原始逐字稿已存同目录 `podcast-transcript.txt`，供检索与引用。
- 早报中本期三条观点已在 2026-11-22 日报正文记录，此处保留长文本版本。
- 归档时发现：早报 autopilot 当日产物文件名已从 `/tmp/fb-digest.json` 换成 `/tmp/digest_raw.json`，扫描器的永久排除清单尚未覆盖新名——已在日报中记录并作为待修项。

## 应更新的规则或 skill

- 无（本次只是归档，未产生新流程规则）。

## 暂不采用的部分

- 播客中关于 Linear 具体定价、组织扩张节奏的细节暂不进入决策层，仅作背景。

---

原始文件：`podcast-transcript.txt`（93,524 字节）
