---
Source: /tmp/edn-* (EDN 周报 cron 1d0cf41439ec，2026-10-28 那一轮的取数残件)
Archived: 2026-10-29 (Hermes 日报 cron，档 1 自动归档)
---

# EDN 周报取数脚本归档（2026-10-28 轮）

EDN 周报的两个采集子任务在 2026-10-28 那轮超时未落 `evidence.json`，母 agent 靠母目录里的
抢救脚本从 188 个 raw Tavily JSON 里回收了 373 条结构化条目。这些脚本当时只存在于 `/tmp`，
按 EDN skill 的收尾清单会被 `rm -f /tmp/edn-*/*.json` + `rm -rf` 一起清掉。

## 文件

| 文件 | 作用 |
|---|---|
| `salvage.py` | 从子 agent 的 raw Tavily JSON 中抢救证据条目（vendor/domain 归类、URL 去重、噪声过滤） |
| `build_asset.py` | 合并 east（手采精标）+ salvage（raw 抢救）+ 北方精选，输出最终数据资产 JSON |
| `batch.py` | 并发跑 `tvly search` 的批量子任务脚本（子任务取数用） |
| `dump.py` | 把单个 Tavily JSON 结果的 `raw_content` 抽成可读文本（带 marker 定位） |
| `EDN-周报-2026-10-28.md` | 当轮周报正文（HTML 格式，来自 `edn-insight-data/2026-10-28-report.md`） |

## 用法提示

- `salvage.py` 顶部有 `WINDOW_START` / `WINDOW_END` 两个硬编码时间窗，**换周必须改**。
- `build_asset.py` 顶部有 `DATE = '2026-10-28'`，同样需要改。
- `salvage.py` 的 `VENDOR_MAP` / `DOMAIN_MAP` 覆盖 11 家核心厂商 + 若干领域，换季新增厂商时补。
- 这些路径写在脚本里的 `/tmp/edn-east` / `/tmp/edn-salvage` 是**上一轮的目录名**，
  方向目录名会随子 agent 取数方向变化（见 EDN skill 收尾清单注释），复用时按实际目录调整。

## 关联

- Skill：`edn-weekly-cron-ops`（含 `tvly` 悬空符号链接修法、飞书替代投递路径、收尾清单）
- 本轮产物：`/root/.hermes/cron/output/edn-insight-data/2026-10-28.json`（390 条证据）
- 飞书投递：长住文档写入失败，替代路径新建文档 https://ruijie.feishu.cn/docx/M7pVdtNY8oMbq3x2zhxc6714n8g
