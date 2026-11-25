#!/usr/bin/env python3
"""EDN 2026-11-25 rescue report — built from the landed data asset.

The EDN cron crashed (provider timeout) after writing the data asset but
before writing the report. This mirrors the 2026-11-18 rescue path: read the
asset, emit a factual coverage summary. NOT an agent-written analysis.
"""
import json

DATE = "2026-11-25"
ASSET = f"/root/.hermes/cron/output/edn-insight-data/{DATE}.json"
OUT = "/root/.hermes/state/edn_rescue_2026-11-25.md"

d = json.load(open(ASSET))
lines = []
A = lines.append

A(f"# EDN 市场洞察周报 · {DATE}（抢救版）")
A("")
A(f"**状态**：EDN cron 本轮取数成功、数据资产已落盘，但**综合分析阶段崩溃**（provider timeout 234s，3 次重试全耗尽）。")
A("**以下为日报 cron 从数据资产机械生成的覆盖摘要（非 agent 分析正文）**。")
A(f"**数据资产**：`{ASSET}`（{d['sources_total']} 条证据 / {len(d['vendors'])} 个厂商标签 / {len(d['domains'])} 个领域）")
A(f"**置信度分布**：{d['confidence_breakdown']}")
A(f"**窗口**：{d.get('week')}")
A("")

A("## 厂商覆盖")
A("")
vendors = sorted(d["vendors"].items(), key=lambda kv: -len(kv[1].get("hits", [])))
for name, blob in vendors:
    A(f"- {name}: {len(blob.get('hits', []))} 条")
A("")

A("## 领域覆盖")
A("")
for name, blob in sorted(d["domains"].items(), key=lambda kv: -len(kv[1].get("hits", []))):
    A(f"- {name}: {len(blob.get('hits', []))} 条")
A("")

A("## 窗口内高价值条目（按厂商取样，每家 2 条）")
A("")
for name, blob in vendors:
    hits = blob.get("hits", [])
    if not hits:
        continue
    A(f"### {name}")
    for h in hits[:2]:
        A(f"- [{h.get('date')}] {(h.get('title') or '').strip()[:150]}")
        A(f"  {h.get('url')}")
    A("")

A("## X 高价值信号")
A("")
for s in (d.get("x_signals") or []):
    A(f"- [{s.get('timestamp')}] @{s.get('handle')}: {(s.get('text') or '')[:300]}")
    A(f"  {s.get('url')}")
A("")

A("## YouTube 高价值视频")
A("")
for s in (d.get("youtube_signals") or []):
    A(f"- [{s.get('date')}] {s.get('channel')} — {s.get('title')}")
    A(f"  {s.get('url')}")
A("")

A("## 采集统计")
A("")
for k, v in (d.get("capture_stats") or {}).items():
    A(f"- {k}: {v}")
A("")

A("## 待补")
A("")
A("- 完整 9 节分析正文（执行结论 / 领域演化 / 跨厂商模式 / EDN 启示 / 推荐行动）未生成")
A("- 飞书长住文档未追加（bot 身份无该文档权限，API 3380004 + cron 崩溃）")
A("- 原文缺失 EDN 策略启示段落，需下轮重跑或人工补写")
A("")

open(OUT, "w").write("\n".join(lines))
print("WROTE", OUT, len("\n".join(lines)), "chars")
print("vendors:", len(vendors), "domains:", len(d["domains"]),
      "x:", len(d.get("x_signals") or []), "yt:", len(d.get("youtube_signals") or []))
