# AGENTS.md

This vault is cofol1986's long-term working memory. It is not a raw chat archive.

## Source of truth

- Obsidian Markdown files are the primary source of truth.
- Git history is the audit trail for changes to memory and notes.
- Get笔记 is a synced reading, capture, and mobile-access layer, not the canonical source.
- Hermes memory stores only stable user/environment preferences and long-lived facts.
- Hermes skills store reusable procedures and workflows.

## PARA + Agent Memory model

Use PARA as the primary organization principle, extended with People, Decisions, and Playbooks for agent work.

### Projects

Projects are short- or medium-term efforts with a clear outcome and finish line.

A note belongs in `30-Projects/` only when it has most of these:

- a clear desired result;
- a finish condition or success criteria;
- repeated follow-up actions;
- dependencies, risks, or open loops;
- implementation, operational, or collaboration state that changes over time.

Do not turn every topic, article, or conversation into a project. When something looks project-like but the boundary is unclear, remind the user and ask whether to create a project note.

### Areas

Areas are long-term responsibilities with standards to maintain. They do not have a natural finish line.

Use `35-Areas/` for ongoing responsibility domains such as:

- Hermes Agent 基础设施;
- 个人知识管理与 Agent 记忆系统;
- AI 编程与 Agent 工作流;
- 信息摄取与研究;
- 服务器与自动化运维.

Areas should track health, standards, active projects, related resources, and recurring checks.

### Resources

Resources are durable reference materials that are useful but do not require immediate action. In this vault, `10-Notes/`, `10-Knowledge/`, and topic subfolders usually act as Resources.

Examples:

- article notes;
- research summaries;
- podcast transcripts;
- external links and source material;
- methods or concepts not yet tied to an active project.

### Archives

Archives are completed, paused, stale, or no-longer-active materials. This vault does not yet have a dedicated archive folder; when archiving becomes necessary, prefer `40-Archives/` or an `Archive/` subfolder inside the relevant section.

### Agent extensions

- `40-People/`: people, preferences, responsibilities, communication context, and collaboration notes.
- `50-Decisions/`: cross-project decisions and decision records when they are not owned by a single project note.
- `20-Playbooks/`: reusable operational playbooks, SOPs, retrospectives, and workflow patterns. High-frequency playbooks should be promoted into Hermes skills.

## Directory roles

- `00-Inbox/`: temporary or unsorted captures. Use when no better location is clear.
- `00-Inbox/TODO.md`: temporary TODOs, reminders, open loops, unfinished items, and topics to discuss later. If an item gains a clear outcome, state, and repeated follow-up actions, ask whether to promote it to `30-Projects/`. If it is a recurring responsibility, link it to `35-Areas/`.
- `10-Notes/`: durable knowledge notes, article notes, research summaries, meeting notes, and external content整理。
- `10-Knowledge/`: durable knowledge/reference material when the content is closer to a standing resource than a dated note.
- `10-Notes/Daily/Hermes/`: Hermes-generated daily reports.
- `20-Playbooks/`: reusable operational playbooks, SOPs, retrospectives, and workflow patterns.
- `30-Projects/`: active project state, decisions, open loops, risks, and plans.
- `35-Areas/`: long-term responsibility areas and their health/standards.
- `40-People/`: people, preferences, responsibilities, communication context, and collaboration notes.
- `50-Decisions/`: cross-project decisions and decision records when they are not owned by a single project note.
- `90-Index/`: indexes and navigation notes.
- `99-AI-Logs/`: AI-generated logs only when they have audit value. Avoid dumping raw logs here by default.

## Write policy

Prefer updating an existing note over creating a duplicate.

Create a new note only when:

- the topic is genuinely new;
- no existing note can own the information;
- the content is durable enough to matter later.

Append to an existing note when:

- the user adds a thought about an existing article;
- a project receives a status update;
- an area health/status note changes;
- a decision changes;
- an open loop is closed;
- new information is a continuation of an existing workstream.

## Memory policy

Record only information that is likely to remain useful after one week.

Do not record:

- temporary task progress;
- one-off execution logs;
- stale PR/issue/commit identifiers;
- unverified claims;
- generic summaries without action value;
- raw tool output unless it is necessary evidence.

## Area notes

Each area note should include:

- Purpose
- Maintenance standard
- Current health/status
- Active projects
- Related resources
- Recurring checks
- Risks / watchpoints

## Project notes

A project note is for an ongoing workstream, not every topic. Before creating one, check whether the user considers it a project unless the user explicitly requested project creation.

Each active project note should include:

- Area
- Goal
- Finish condition / success criteria
- Current status
- Key decisions
- Open loops
- Risks
- Next actions
- Related notes

## Article and external-content notes

Article notes should include:

- Source
- Author / publisher
- Core thesis
- Key ideas
- Useful quotes or evidence
- Implications for cofol1986's workflows
- Follow-up actions, if any

When the user asks for “整理成笔记”, include a section for:

- `对我的系统/工作的启发`
- `可落地动作`
- `应更新的规则或 skill`
- `暂不采用的部分`

## Get笔记 sync

When the user asks to save notes:

1. Write or update the Obsidian Markdown file.
2. Commit and push the vault.
3. Sync to Get笔记 MyClaw unless the user explicitly says not to.
4. Report both Obsidian path and Get笔记 note_id.

For follow-up thoughts on an existing note, prefer creating a child note in Get笔记 using `parent_id` rather than creating an unrelated duplicate.

## Agent operating boundaries

- Ask before publishing, posting, purchasing, deleting, or making irreversible external changes.
- For local Markdown organization and reversible file changes inside this vault, act directly when the user's intent is clear.
- If a workflow is repeated or non-trivial, update or create a Hermes skill rather than burying the procedure in a note.
