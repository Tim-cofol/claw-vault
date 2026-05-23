# 个人知识管理与 Agent 记忆系统

## Purpose

维护 cofol1986 的长期知识库和 Agent shared memory substrate，让 Obsidian、Get笔记、Hermes memory、Hermes skills、日报和项目/领域记录形成清晰分工。

## Maintenance standard

- Obsidian Markdown 是主数据源。
- Git history 提供可审查的变更记录。
- Get笔记作为同步、阅读、移动端入口，不作为唯一 source of truth。
- Hermes memory 只保存长期稳定偏好和环境事实。
- Hermes skills 保存可复用流程，不保存一次性事实。
- PARA 概念用于区分 Projects、Areas、Resources、Archives。
- People / Decisions / Playbooks 作为 Agent 工作扩展层保留。

## Current health/status

- Vault 位于 `/root/obsidian-vault`。
- 已新增顶层 `AGENTS.md`。
- 已创建 `10-Projects/`、`50-People/`、`60-Decisions/`。
- 已开始引入 PARA 思路，并新增 `20-Areas/`。

## Active projects

- 待确认：是否创建 `10-Projects/将 Vault 改造成 Agent Shared Memory.md`。

## Related resources

- [[AGENTS]]
- [[70-Playbooks]]
- `obsidian-getnote-dualwrite` Hermes skill
- `vault-memory-routing` Hermes skill

## Recurring checks

- Inbox 是否需要清理。
- 哪些 Resources 应该关联到 Areas。
- 哪些持续工作流应升级为 Projects。
- 哪些 Playbooks 应提升为 Hermes skills。
- Get笔记同步是否成功、是否产生重复孤立笔记。

## Risks / watchpoints

- 把所有主题误建为项目，导致 Projects 污染。
- Obsidian 和 Get笔记内容版本不一致。
- Hermes memory 被短期任务状态污染。
- Playbooks 和 skills 分工不清。
