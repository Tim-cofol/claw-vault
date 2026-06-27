# Ideas — 第二大脑的想法库

> 这不是收件箱,不是项目笔记,不是参考资料库。这是 **跨越单个会话的、原子化的、半结构化的个人想法**。
>
> 由 Hermes 通过 FTS5 在相关任务里自动召回,而不是靠你手动翻找。

## 这是什么 / 不是什么

| 它是 ✅ | 它不是 ❌ |
|---|---|
| 一条原子化的想法(1-3 句话核心) | 长文 / 文章笔记(放 `30-Resources/Knowledge/`) |
| 跨项目、跨会话长期保留 | 临时待办(放 `00-Inbox/TODO.md`) |
| 重要度 1-5,可分 `raw/developed/parked/archived` | 当前活跃项目的状态(放 `10-Projects/<name>/`) |
| 可被 Hermes 在上下文相关时召回 | 一定要立刻用到的参考资料(放 `30-Resources/` 主题子目录) |

## 文件命名

`idea-YYYY-MM-DD-NNN.md` —— 当天递增编号。

## Frontmatter 约定

```yaml
---
id: idea-2026-06-26-001
created: 2026-06-26
status: raw | developed | parked | archived
tags: [agent-memory, recall, pkm]
importance: 1-5            # 1 = 随手记,5 = 人生方向级
last_surfaced: 2026-06-26  # 由 recall 脚本自动更新,不用手填
surface_count: 0           # 由 recall 脚本自动更新
---

# 短原子化标题

想法本身,1-3 句话。

## Why it matters
…

## Possible uses
…

## Links
- [[related note]]
```

## 怎么用

### 快速添加

在和 Hermes 对话时直接说"我有个想法"、"记一下"、"以后想用 ……",Hermes 会:

1. 问 1-2 个澄清问题(tags? importance?)
2. 在这个文件夹创建文件
3. 重建 SQLite 索引
4. 告诉你路径 + 第一行预览

### CLI 手动添加

```bash
~/.hermes/scripts/idea_capture.py \
  --title "把每周复盘改成 voice note" \
  --body "开车时复盘比打字效率高 3 倍,先用 Otter.ai 转写再让 Hermes 整理" \
  --tags workflow,voice \
  --importance 4
```

### 查询召回

```bash
# 单次查询(给 Hermes 看的格式)
~/.hermes/scripts/idea_recall.py "Hermes 召回 想法"

# JSON 输出(给程序用)
~/.hermes/scripts/idea_recall.py --json "memory"

# 高重要度召回
~/.hermes/scripts/idea_recall.py --importance-min 4 "agent workflow"
```

### 重建索引

```bash
~/.hermes/scripts/idea_index.py           # 全量重建
~/.hermes/scripts/idea_index.py --incremental   # 增量(只处理 mtime 变化的文件)
```

## 维护

- **每月一次**:翻一遍 `status: raw` 的想法 → 决定 promote 到 `developed`、park、还是 archive
- **`importance` 调整**:被反复召回且真的有用 → +1;被召回但用不上 → 降级或 archive
- **别忘了 Get笔记同步**:这个文件夹也会走 `obsidian-getnote-dualwrite` skill,移动端可读

## 相关基础设施

- 索引: `~/.hermes/idea-recall/ideas.sqlite` (FTS5)
- Skill: `~/.hermes/skills/productivity/idea-recall/`
- Cron: 每周一 9am 推送未唤醒的高重要度想法