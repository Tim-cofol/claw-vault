---
type: image
source: 飞书会话 20260609_103145_a05fe05b
created: 2026-06-09
archived: 2026-06-11
tags: [Cisco, AI-Security, NHI, Hermes]
---

# 思科 AI 安全 + 身份图谱架构图（v3）

这张图源自 2026-06-09 飞书会话"AI 安全生态图"——你给的手稿被重读成思科产品视角下的 AI 安全 + 身份图谱叙事。

## 核心结构

- **左输入侧**：Armorblox（邮件/NHI 行为信号）
- **核心层**：Splunk SIEM + SOAR
- **右上 Security for AI**：Robust Intelligence（模型/应用 AI 防护）+ AI Defense（应用层防护）
- **右中 Identity 栈**：Oort / Duo / ISE / Astrix
- **底部**：身份图谱 + 知识图谱

## 与 v1 / v2 的差异

- **v1（已废弃）**：通用 "Security Platform + Identity" 模板，被你当场否决。
- **v2**：套用思科叙事版，主结构定稿；右上仍保留 "Fail-safe / Resilience" 横切标签。
- **v3**：按你的最终确认，**去掉 Fail-safe 标注**，Security for AI 只保留 Robust Intelligence + AI Defense + Galileo 三个并列产品。

## 归档说明

原文件 `/tmp/cisco_nhi_v3.png` 在 /tmp 停留超 48 小时未归档，今日按 cron skill 默认动作（第 3 天升级为 `档 1`）直接落 Vault，不再等用户拍板。

## 相关

- 关联笔记：[[2026-04-15 思科零信任方案用户需求层级]]
- 上游会话：飞书 20260609_103145_a05fe05b（71 条消息）
- v1 错误版：/tmp/ai_security_infographic.png（保留作教训对照）
- v2 中间版：/tmp/cisco_ai_security_v2.png