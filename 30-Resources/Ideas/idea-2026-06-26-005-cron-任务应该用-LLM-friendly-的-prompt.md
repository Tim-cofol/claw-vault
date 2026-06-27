---
id: idea-2026-06-26-005
created: 2026-06-26
status: raw
tags: [cron, hermes, ops]
importance: 3
last_surfaced:
surface_count: 0
---

# cron 任务应该用 LLM-friendly 的 prompt

写 cron prompt 时不要假设上下文已知,要把触发条件、读取路径、输出格式、失败处理全部写全。每个 cron 任务应该自带一个测试用的 sample input。
