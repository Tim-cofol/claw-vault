# AGENTS.md

## Purpose

This vault is cofol1986's long-term working memory. It is not a raw chat archive.

Use this file as the operating guide for agents working inside the vault: classify notes correctly, avoid duplicates, preserve source-of-truth boundaries, and keep durable memory useful.

## Source of truth

- Obsidian Markdown files are the primary source of truth.
- Git history is the audit trail for changes to memory and notes.
- Get笔记 is a synced reading, capture, and mobile-access layer, not the canonical source.
- Hermes memory stores only stable user/environment preferences and long-lived facts.
- Hermes skills store reusable procedures and workflows.

## PARA routing

Use PARA as the default routing model, extended with People, Decisions, and Playbooks for agent work.

- `10-Projects/`: finite work with a clear goal, finish condition, open loops, dependencies, risks, or changing state.
- `20-Areas/`: ongoing responsibilities with standards to maintain and no natural finish line.
- `30-Resources/`: durable references, articles, research, transcripts, external links, methods, and concepts.
- `40-Archives/`: completed, paused, stale, or no-longer-active material.

Do not turn every topic, article, or conversation into a project. If something looks project-like but the boundary is unclear, ask whether to create a project note.

## Directory roles

- `00-Inbox/`: unsorted captures and temporary material.
- `00-Inbox/TODO.md`: temporary TODOs, reminders, open loops, and topics to revisit.
- `10-Projects/`: active project state, decisions, risks, plans, and next actions.
- `20-Areas/`: long-term responsibility areas and their health/standards.
- `30-Resources/`: durable knowledge, article notes, research summaries, meeting notes, and external content整理。
- `30-Resources/Knowledge/`: durable knowledge/reference material when it is closer to standing resource than dated note.
- `30-Resources/Daily/Hermes/`: Hermes-generated daily reports.
- `40-Archives/`: inactive, completed, stale, or paused material.
- `50-People/`: people, preferences, responsibilities, and collaboration context.
- `60-Decisions/`: cross-project decisions and decision records not owned by a single project note.
- `70-Playbooks/`: reusable SOPs, retrospectives, templates, and workflow patterns. High-frequency playbooks should become Hermes skills.
- `90-Index/`: indexes and navigation notes.
- `99-AI-Logs/`: AI-generated logs only when they have audit value. Avoid dumping raw logs here by default.

## Write policy

Prefer updating an existing note over creating a duplicate.

Create a new note only when the topic is genuinely new, no existing note can own it, and the content is durable enough to matter later.

Append to an existing note when new information continues an existing article, project, area, decision, open loop, or workstream.

For local Markdown organization and reversible file changes inside this vault, act directly when the user's intent is clear.

## Memory policy

Record only information likely to remain useful after one week.

Do not record temporary task progress, one-off logs, stale PR/issue/commit IDs, unverified claims, generic summaries without action value, or raw tool output unless it is necessary evidence.

Obsidian Markdown is for durable notes. Hermes memory is for compact stable facts. Hermes skills are for reusable procedures.

## Note structures

Keep note structures practical, not ceremonial.

Area notes should usually cover purpose, maintenance standard, current health/status, active projects, related resources, recurring checks, and risks/watchpoints.

Project notes should usually cover area, goal, finish condition, current status, key decisions, open loops, risks, next actions, and related notes.

Article and external-content notes should usually cover source, author/publisher, core thesis, key ideas, useful evidence, implications for cofol1986's workflows, and follow-up actions if any.

When the user asks for “整理成笔记”, include:

- `对我的系统/工作的启发`
- `可落地动作`
- `应更新的规则或 skill`
- `暂不采用的部分`

Move detailed templates, SOPs, and repeated workflows to `70-Playbooks/` or Hermes skills instead of expanding this file.

## Get笔记 sync

When the user asks to save notes:

1. Write or update the Obsidian Markdown file.
2. Commit and push the vault.
3. Sync to Get笔记 MyClaw unless explicitly told not to.
4. Report both Obsidian path and Get笔记 note_id.

For follow-up thoughts on an existing note, prefer creating a Get笔记 child note with `parent_id` rather than creating an unrelated duplicate.

## Agent operating boundaries

Ask before publishing, posting, purchasing, deleting, or making irreversible external changes.

For local Markdown organization and reversible file changes inside this vault, act directly when intent is clear.

If a workflow is repeated or non-trivial, update or create a Hermes skill rather than burying the procedure in a note.
