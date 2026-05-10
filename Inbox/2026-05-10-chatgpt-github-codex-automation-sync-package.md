---
source: chatgpt
project: my-claw
repo: Tim-cofol/claw-vault
status: inbox
trigger_coding: false
created_at: 2026-05-10T00:00:00+08:00
type: conversation_sync_package
topic: ChatGPT discussion to GitHub inbox automation and Codex workflow
risk_level: medium
recommended_next_step: triage_to_spec_and_tasks
---

# Conversation Sync Package: ChatGPT → GitHub → Codex 自动开发流水线

## 1. 背景

本轮讨论围绕一个核心想法展开：

> 把 ChatGPT 作为想法、沟通、需求澄清和方案推演入口；把 GitHub 仓库作为中转站、任务总线和工程状态机；再通过 Codex Cloud、本地 Codex CLI、IDE Extension 或其他本地编码工具完成自动开发、PR 生成、Review 与本地验证。

原始设想是：

```text
ChatGPT 讨论
  ↓
生成 Conversation Sync Package
  ↓
提交到 GitHub inbox/
  ↓
整理为 specs/ 或 tasks/
  ↓
标记 task: codex-ready
  ↓
Codex Cloud 执行
  ↓
生成 PR
  ↓
Codex review + 本地 IDE 验证
  ↓
merge
```

本同步包用于沉淀本轮讨论形成的方案，暂时仅进入 `Inbox/`，不直接触发编码。

---

## 2. 核心结论

### 2.1 方向正确，但不能把“聊天记录”直接变成“编码任务”

最重要的判断：

> GitHub 不应该是 ChatGPT 的聊天备份盘，而应该是 AI 开发系统的任务总线、决策账本和状态机。

真正要同步的不是原始聊天，而是经过整理的结构化产物：

- 背景
- 关键结论
- 决策
- 假设
- 开放问题
- 候选任务
- 不应执行内容
- 触发建议

因此，中间必须有一层 **Conversation Compiler / 对话编译器**。

---

### 2.2 自动化可以做，但要分层

自动化成熟度建议：

| 阶段 | 自动化内容 | 人工控制点 |
|---|---|---|
| 阶段 1 | ChatGPT 生成同步包，本地脚本提交到 GitHub Inbox | 人工触发同步 |
| 阶段 2 | GitHub Action 自动整理为 specs/tasks | 人工确认 task 是否 ready |
| 阶段 3 | 标记 `codex-ready` 后 Codex 自动开发 | 人工 Review PR |
| 阶段 4 | 低风险任务自动 Review / 自动修复 | 人工 merge |
| 阶段 5 | 极低风险任务条件自动 merge | 严格规则 + 可回滚 |

初期不建议自动 merge。

一句话：

> 自动化处理确定性流程，不要自动化处理意图判断。

---

## 3. 推荐架构

```text
ChatGPT
  ↓
Conversation Compiler
  ↓
GitHub Inbox
  ↓
Triage Workflow
  ↓
Specs / Tasks / Decisions
  ↓
Task State Machine
  ↓
Codex Cloud / Local Codex / IDE Agent
  ↓
Pull Request
  ↓
Codex Review + Local Verification
  ↓
Human Merge
```

角色分工：

| 组件 | 角色 |
|---|---|
| ChatGPT | 想法入口、需求澄清、产品讨论、方案推演 |
| Conversation Compiler | 把讨论编译成结构化同步包 |
| GitHub Inbox | 未处理输入区，只沉淀，不执行 |
| Specs | 产品需求、架构设计、流程设计 |
| Tasks | 可执行工程任务 |
| Decisions / ADR | 关键架构和流程决策 |
| Codex Cloud | 云端异步执行器 |
| Codex CLI | 本地/服务器脚本化执行器 |
| Codex IDE Extension | 本地深度开发和验证工具 |
| GitHub PR | 工程交付与 Review 载体 |

---

## 4. 仓库结构建议

建议在项目仓库中逐步形成如下结构：

```text
claw-vault/
  Inbox/
    2026-05-10-chatgpt-github-codex-automation-sync-package.md

  Specs/
    my-claw-automation-architecture.md
    chatgpt-to-github-sync-design.md

  Tasks/
    TASK-0001-build-sync-script.md
    TASK-0002-build-github-action-triage.md
    TASK-0003-build-codex-ready-trigger.md

  Decisions/
    ADR-0001-use-github-as-agent-bus.md
    ADR-0002-default-trigger-coding-false.md

  Prompts/
    triage-inbox.md
    generate-task.md
    implement-task.md
    review-pr.md

  .github/
    workflows/
      triage-inbox.yml
      generate-tasks.yml
      run-codex-task.yml
      codex-review.yml

  AGENTS.md
```

大小写可以按仓库现有风格调整。当前请求明确指定 `Inbox`，因此本同步包写入 `Inbox/`。

---

## 5. 关键安全原则

### 5.1 默认不触发编码

所有同步包默认必须带：

```yaml
status: inbox
trigger_coding: false
```

只有明确转换为 task，并且被标记为：

```yaml
status: codex-ready
trigger_coding: true
```

才允许进入 Codex 编码流程。

---

### 5.2 GitHub 是状态机，不是垃圾桶

禁止做法：

```text
每次聊天全文 → GitHub → 自动触发开发
```

推荐做法：

```text
重要讨论 → 结构化同步包 → Inbox
Inbox 经整理 → Specs / Tasks
Task 经确认 → codex-ready
Codex 执行 → PR
人类验证 → Merge
```

---

### 5.3 权限最小化

如果后续做 ChatGPT Action / MCP / 后端服务，建议：

- ChatGPT 不直接保存 GitHub PAT
- GitHub Token 只放在后端环境变量
- Token 只授予目标仓库 contents write 权限
- 后端只允许写 `Inbox/`
- 默认不允许修改源码目录
- 默认不允许修改 `.github/workflows/`
- 默认不允许自动 merge

后端应硬编码路径限制：

```python
if not path.startswith("Inbox/"):
    raise HTTPException(400, "Only Inbox/ writes are allowed")
```

---

## 6. “提交到 GitHub Inbox” 的三种实现方式

### 6.1 方案 A：本地脚本提交

适合 MVP，最快落地。

流程：

```text
ChatGPT 输出同步包
  ↓
复制到 sync.md
  ↓
运行 sync_inbox.py
  ↓
写入 Inbox/*.md
  ↓
git add / commit / push
  ↓
GitHub Action 触发
```

优点：简单、稳定、可控。  
缺点：需要手动复制或一键脚本。

---

### 6.2 方案 B：ChatGPT Action → 后端 → GitHub API

适合在 ChatGPT 内一句话同步。

流程：

```text
ChatGPT
  ↓
Custom GPT Action: sync_to_github_inbox()
  ↓
VPS / Cloudflare Worker / FastAPI 服务
  ↓
GitHub REST API
  ↓
Inbox/*.md
```

推荐接口：

```http
POST /sync/chatgpt/inbox
```

请求体：

```json
{
  "project": "my-claw",
  "title": "chatgpt-github-codex-automation",
  "summary_package": "# Conversation Sync Package...",
  "target_repo": "claw-vault"
}
```

后端负责：

- 文件命名
- 加 frontmatter
- 限制只能写 Inbox
- 调 GitHub API
- 返回 commit 信息

---

### 6.3 方案 C：MCP / ChatGPT App 工具化

适合长期产品化。

工具可设计为：

```text
push_to_github_inbox
list_recent_sync_packages
create_task_from_inbox
mark_task_codex_ready
get_task_status
```

推荐先不要直接使用完整 GitHub MCP 暴露所有仓库写能力，而是封装一个窄工具：

- 只允许写 Inbox
- 只允许生成 Tasks
- 只允许修改任务状态
- 不允许改 src
- 不允许直接 merge

---

## 7. GitHub Action 自动化建议

### 7.1 Inbox 入库后自动整理

触发：

```yaml
on:
  push:
    paths:
      - "Inbox/**"
```

动作：

```text
读取新增 Inbox 文件
  ↓
判断类型：idea / decision / spec / task candidate
  ↓
生成整理 PR
  ↓
把内容拆分到 Specs / Tasks / Decisions
```

初期可以只做“打开整理 PR”，不要直接写主分支。

---

### 7.2 Task 被确认后触发 Codex

Task 文件建议格式：

```yaml
---
id: TASK-0001
project: my-claw
status: codex-ready
trigger_coding: true
max_change_lines: 200
requires_tests: true
risk: low
---
```

触发条件：

```text
status == codex-ready
trigger_coding == true
risk != high
```

---

### 7.3 PR 自动 Review

PR 创建后可自动触发 Codex Review，也可以通过评论触发：

```text
@codex review
```

如果 Review 发现问题，再通过：

```text
@codex fix the P1 issue
```

让 Codex 继续修复。

---

## 8. 最小 MVP 任务拆解

### TASK-0001：建立目录结构

目标：

```text
Inbox/
Specs/
Tasks/
Decisions/
Prompts/
.github/workflows/
AGENTS.md
```

验收标准：

- 目录存在
- `AGENTS.md` 存在
- Inbox 文件不会自动触发编码

---

### TASK-0002：实现本地同步脚本

目标：

实现 `scripts/sync_inbox.py`，把本地 markdown 文件提交到 `Inbox/`。

验收标准：

- 自动生成文件名
- 自动添加 frontmatter
- 默认 `trigger_coding: false`
- 自动 git add / commit / push

---

### TASK-0003：实现 Inbox triage workflow

目标：

新增 `.github/workflows/triage-inbox.yml`。

验收标准：

- 当 `Inbox/**` 有新文件时触发
- 能列出新增文件
- 暂不直接调用 Codex
- 暂不直接修改源码

---

### TASK-0004：设计 Task frontmatter 标准

目标：

定义统一任务文件规范。

建议字段：

```yaml
id: TASK-0001
project: my-claw
source_inbox: Inbox/xxx.md
status: draft | ready | codex-ready | in-progress | pr-opened | done
trigger_coding: false
risk: low | medium | high
max_change_lines: 200
requires_tests: true
owner: human | codex | local-agent
```

---

### TASK-0005：接入 Codex 执行流程

目标：

当 task 被标记为 `codex-ready` 后，触发 Codex Cloud 或 Codex GitHub Action。

验收标准：

- Codex 只读取明确 task
- Codex 创建分支
- Codex 生成 PR
- 不自动 merge

---

## 9. 不应立即执行的内容

以下动作暂不建议自动化：

- 每个 ChatGPT 会话全文自动同步
- Inbox 文件一入库就触发编码
- 高风险任务自动执行
- 自动修改认证、权限、密钥、部署脚本
- 自动 merge
- 让 ChatGPT 直接拥有完整 GitHub 写权限
- 让 Codex 在 Full Access 下长期无人值守

---

## 10. 决策记录候选

### ADR-0001：使用 GitHub 作为 Agent Bus

决策：

> 使用 GitHub 作为 ChatGPT、Codex Cloud、本地 Agent、PR Review 之间的中转站和状态机。

理由：

- GitHub 原生支持 issue、PR、branch、commit、Actions
- 适合审计和回滚
- 适合把 AI 输出转化为工程资产
- 适合云端和本地工具协同

---

### ADR-0002：所有同步包默认不触发编码

决策：

> 所有从 ChatGPT 同步进入 Inbox 的内容，默认 `trigger_coding: false`。

理由：

- 防止误触发
- 防止探索性讨论被当作需求
- 防止 Codex 被噪声牵引
- 保留人类对意图确认的控制权

---

### ADR-0003：Codex 只消费明确 Task，不消费原始 Chat

决策：

> Codex 不直接消费原始聊天或 Inbox 内容，只消费经过整理和确认的 Task。

理由：

- 降低误解概率
- 便于验收
- 便于控制变更范围
- 便于测试和 Review

---

## 11. 下一步建议

推荐后续按这个顺序推进：

1. 人工 review 本同步包
2. 从本同步包生成 `Specs/chatgpt-github-codex-automation-architecture.md`
3. 生成 `Decisions/ADR-0001-use-github-as-agent-bus.md`
4. 生成 `Tasks/TASK-0001-build-sync-script.md`
5. 实现本地脚本版同步闭环
6. 再实现 GitHub Action 自动整理
7. 最后接入 Codex Cloud 自动执行

---

## 12. 当前同步包状态

```yaml
status: inbox
trigger_coding: false
recommended_action: human_review_then_triage
```

本文件只用于沉淀方案，不应直接触发编码。
