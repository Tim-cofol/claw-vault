# AGENTS.md

This vault is cofol1986's long-term working memory. It is not a raw chat archive.

## Source of truth

- Obsidian Markdown files are the primary source of truth.
- Git history is the audit trail for changes to memory and notes.
- Get笔记 is a synced reading, capture, and mobile-access layer, not the canonical source.
- Hermes memory stores only stable user/environment preferences and long-lived facts.
- Hermes skills store reusable procedures and workflows.

## Directory roles

- `00-Inbox/`: temporary or unsorted captures. Use when no better location is clear.
- `10-Notes/`: durable knowledge notes, article notes, research summaries, meeting notes, and external content整理。
- `10-Notes/Daily/Hermes/`: Hermes-generated daily reports.
- `20-Playbooks/`: reusable operational playbooks, SOPs, retrospectives, and workflow patterns.
- `30-Projects/`: active or recurring project state, decisions, open loops, risks, and plans. Do not create project notes casually; use only when a workstream has ongoing ownership, repeated actions, or a meaningful outcome.
- `40-People/`: people, preferences, responsibilities, communication context, and collaboration notes.
- `50-Decisions/`: cross-project decisions and decision records when they are not owned by a single project note.

## Write policy

Prefer updating an existing note over creating a duplicate.

Create a new note only when:

- the topic is genuinely new;
- no existing note can own the information;
- the content is durable enough to matter later.

Append to an existing note when:

- the user adds a thought about an existing article;
- a project receives a status update;
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

## Project notes

A project note is for an ongoing workstream, not every topic. Before creating one, check whether the user considers it a project.

A good project candidate usually has at least two of these:

- repeated follow-up actions;
- a clear desired outcome;
- multiple related notes or sessions;
- dependencies or open loops;
- implementation, operational, or collaboration state that changes over time.

Each active project note should include:

- Goal
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
