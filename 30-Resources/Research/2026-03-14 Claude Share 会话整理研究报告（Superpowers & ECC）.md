---
title: Claude Share 会话整理研究报告（Superpowers & ECC）
date: 2026-03-14
tags: [openclaw, Research]
source: [https://claude.ai/share/2d5e0b71-f6c6-4da6-8349-e57bc3f12b36, https://claude.ai/share/d611484a-e291-4518-99e0-ad9a1b95053b]
---

# 研究报告：两段 Claude Share 会话全量 Q&A 整理（Superpowers / Everything Claude Code）

> 资料来源（原始会话）：
> - 会话1（Superpowers）：https://claude.ai/share/2d5e0b71-f6c6-4da6-8349-e57bc3f12b36
> - 会话2（Everything Claude Code, ECC）：https://claude.ai/share/d611484a-e291-4518-99e0-ad9a1b95053b
>
> 目标：不遗漏你提出的**所有问题**，也不遗漏回答中的**所有要点**；仅按主题与逻辑串联，并对个别衔接不顺的表述做轻微顺滑处理（不删要点）。

---

## 摘要（两段会话在讨论什么）

两段会话分别围绕两套 Claude Code 生态中的高星“方法论/配置体系”展开：

- **Superpowers（obra/superpowers）**：以 `SKILL.md` 为核心，把软件工程最佳实践固化为强制工作流（brainstorm → plan → subagent-driven-development → code review → TDD → finish），强调“纪律化执行、上下文隔离、多轮审查、TDD 强约束”，并通过 bootstrap hook 强行把“先查 skill”变成默认行为。
- **Everything Claude Code（ECC, everything-claude-code）**：更像一套“工程化配置与最佳实践样板库/Agent Harness 调优系统”。核心是用 `CLAUDE.md`、`.claude/rules/`、hooks、agents、skills 等分层管理长期协作；强调“文件化、系统化、自动化地固化协作方式”，并附带安全扫描与 token/上下文管理经验。

---

## 主题一：Superpowers 的整体结构与原理（会话1）

### Q1：帮我分析一下 SuperPower（Superpowers）这个 GitHub 上的 Skill 的整体结构、原理。

**A（全量要点整理）：**

1) **项目定位**
- Superpowers 是一套完整的软件开发工作流框架，构建在一组可组合的 Skills（技能）之上。
- 核心目标：把人类程序员的最佳实践编码成 Agent 可以自动读取与执行的结构化 Markdown 文档。

2) **核心原理：`SKILL.md` 机制**
- 每个 Skill 就是一个 Markdown 文件，包含：
  - 元数据（`name`、`description`、`when_to_use`、`version`、`languages`）
  - 操作指令（触发后必须遵循的步骤/原则）
- 示例：调试类技能 `skills/debugging/root-cause-tracing/SKILL.md` 会写清触发条件（如“Bug 出现在调用栈深处”）与核心原则（“追溯调用链到最初触发点，在源头修复”）。

3) **目录结构（仓库级）**
- `superpowers/`
  - `.claude-plugin/`：Claude Code 插件定义（插件入口）
  - `.codex/`：Codex 平台安装说明
  - `.opencode/`：OpenCode 平台安装说明
  - `agents/`：子 Agent 定义（subagent-driven-development 相关）
  - `commands/`：自定义命令
  - `docs/`：文档
  - `hooks/`：生命周期钩子（session-start-hook 等）
  - `lib/`：工具脚本（Skill 搜索等）
  - `skills/`：核心 Skill 库
  - `tests/`：Skill 的测试用例
- 社区可编辑的 Skills 在 `obra/superpowers-skills` 仓库，插件会自动克隆到 `~/.config/superpowers/skills/`。

4) **启动机制（Bootstrap / SessionStart Hook）**
- 会话开始注入类似：
  - `You have Superpowers. RIGHT NOW, go read: .../getting-started/SKILL.md`
- Bootstrap 传递三件事：
  1) 你拥有 Skills
  2) 通过脚本搜索、读取并按 Skill 指令执行
  3) 如果存在某 Skill 能做某件事，就必须使用

5) **内置开发工作流（按 Skill 串起来）**
- brainstorming（写代码前提问精化需求/探索方案/保存设计文档）
- using-git-worktrees（创建隔离工作区、初始化、跑测试基线）
- writing-plans（拆解 2–5 分钟细粒度任务，包含路径/代码结构/验证步骤）
- subagent-driven-development / executing-plans（逐任务分发给子 Agent 执行，并做两阶段 code review）
- test-driven-development（强制 RED-GREEN-REFACTOR：先测后写；先写实现则删掉重来）

6) **说服性设计（让 Agent 真正遵守 Skill）**
- 仅仅告诉 Agent “你有 skills”不够；需要在指令里嵌入说服技巧与压力场景测试。
- 压力测试例子：生产宕机每分钟损失 5000 美元，是立刻调试还是先花 2 分钟查技能？用这种场景不断强化“必须先查 skill”的要求。

7) **Skills 的自我进化**
- 其中一个技能是“如何创建 Skill”，使系统可扩展。
- 甚至提出“Skills 的 TDD”：把 TDD 用在 Skill 的创建与验证本身。

8) **设计思想总结（对话原文表格要点）**
- 知识载体：SKILL.md（结构化 Markdown，人类可读，Agent 可执行）
- 触发机制：Bootstrap Hook + 脚本搜索
- 合规保障：压力场景 + Cialdini 说服原则
- 工作流覆盖：brainstorm → plan → subagent → code review → TDD
- 可扩展：社区 PR；Agent 也可生成新 Skills
- 跨平台：支持 Claude Code、Cursor、Codex、OpenCode 等
- 本质：用“可检索的外部化长期记忆”弥补 LLM 无状态、无持久最佳实践的短板。

---

## 主题二：Subagent + Code Review + TDD 如何嵌入在一起（会话1）

### Q2：brainstorm → plan → subagent 实现 → code review → TDD 详细解释一下 subagent 的实现，以及 code review、TDD 这些机制如何嵌入在一起？它们如何传递需求、任务？

**A（全量要点整理）：**

1) **整体数据流（“接力棒”）**
- brainstorming：写入设计文档 `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`，并通过 `spec-document-reviewer` subagent 审核，最多循环 5 次直至通过。
- writing-plans：读取设计文档，写入计划文件 `docs/plans/YYYY-MM-DD-<feature-name>.md`。
  - 计划文件头部明确强制：`REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task`。
- subagent-driven-development：读取计划文件一次，解压所有任务 → 逐任务分发给 subagent。

2) **Subagent 的核心设计：上下文隔离 + 角色分工**
- 每个任务用一个全新的 Subagent，而不是同一上下文连续做。
- 工程动机：避免 TDD 的“上下文污染/作弊”——同一 Agent 同时知道测试与实现意图，会在测试阶段按实现思路设计，从而失真。

3) **角色分工（3 个 prompt 模板）**
- `implementer-prompt.md`：实现者（写代码/写测试/自我审查/提交/上报状态）
- `spec-reviewer-prompt.md`：规格审查者（对照任务要求核实“不多不少不偏”）
- `code-quality-reviewer-prompt.md`：代码质量审查者（规格通过后看架构/质量/测试覆盖）

4) **单任务控制流（状态机）**
- Controller（主 Agent）读取计划文件一次 → TodoWrite 记录任务。
- 分发 Implementer subagent：带该任务完整描述与必要上下文。
- Implementer 若需澄清：向 Controller 提问 → Controller 回答后重新派发。
- Implementer 完成后：提交代码，回报状态：`DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` / `NEEDS_CONTEXT`。
- 分发 Spec Reviewer：传入原始任务要求 + implementer 报告。
- Spec 通过后：分发 Code Quality Reviewer：通常传入 git SHA 范围 diff。
- 两审通过：TodoWrite 标记任务完成，进入下一个任务。
- 任一步失败：重新派 implementer 修复 → 再审，形成闭环。

5) **Spec Reviewer 的“极度怀疑主义”**
- 不能信 implementer 自述，必须亲读代码核实。
- 核查 3 类问题：
  - 漏实现（缺失需求）
  - 过度开发（多做未要求功能）
  - 理解偏差（做偏了）
- 用于对抗 LLM 常见问题：过度乐观/虚报完成。

6) **TDD 的嵌入方式：硬约束**
- TDD 在 implementer prompt 中强制执行 RED → GREEN → REFACTOR。
- TDD Skill 的状态机：
  - RED：写失败测试，并验证“失败原因正确”
  - GREEN：写最小实现直到全绿
  - REFACTOR：清理并保持全绿
- 红线：先写了实现再写测试 → 必须删除代码重来。
- Red Flags 表列出常见借口并统一否决：
  - “太简单不用测”
  - “手测过了”
  - “测试后写效果一样”
  - “这次情况不同”
  - … 结论都是删代码重来

7) **Implementer 的状态上报协议**
- `DONE`、`DONE_WITH_CONCERNS`、`BLOCKED`、`NEEDS_CONTEXT`。
- Controller 根据状态做不同处理：补上下文、拆分任务、提升模型、或升级给人类。

8) **整体设计思想总结（对话原文 5 点）**
- 文件接力棒：设计/计划文件存盘，通过文件系统传递信息
- 角色隔离：避免污染
- 双阶段审查：先规格合规再质量审查
- Reviewer 不信自述：必须读代码
- TDD 铁律：不给协商空间

---

### Q3：Subagent 是如何被调用和发起的？

**A（全量要点整理）：**

1) **底层原语：Task Tool（Claude Code 内置）**
- Subagent 只能通过 Task Tool 调用，不能通过 Bash/Shell 启动。

2) **调用格式示例（对话原文）**
```xml
<invoke name="Task">
  <parameter name="subagent_type">general-purpose</parameter>
  <parameter name="description">短描述（3-5词）</parameter>
  <parameter name="prompt">给 Subagent 的完整详细指令</parameter>
  <parameter name="run_in_background">true</parameter>
  <parameter name="model">haiku</parameter>
</invoke>
```

3) **Subagent 定义方式**
- 临时型（Ad-hoc Task）：用 prompt 模板（implementer/spec-reviewer/code-quality-reviewer）填充后直接发 Task。
- 持久化定义（File-based Agent）：`.claude/agents/` 下带 YAML frontmatter 的 Markdown 文件。
  - 可限制工具、指定模型、跨 session 使用、可 git 提交共享。

4) **上下文隔离如何实现**
- Subagent 上下文是全新的；父 Agent 传递信息的唯一通道是 Task 的 `prompt` 字符串。
- 父 Agent 只收到 subagent 最终消息；subagent 中间工具调用细节不回流。
- 因此 Controller 要“读取计划一次，提取任务文本”，把任务文本直接塞进 prompt，避免 subagent 看到整份计划产生跨任务污染。

5) **关键 bug/洞察（对话原文）**
- SessionStart Hook 注入可能不会传给 subagent。
- 这会导致 subagent 跳过纪律（例如跳过 TDD）。
- 结论：subagent 行为完全取决于 prompt 字符串写了什么，所以必须把纪律/TDD/反理性化条款写进子代理模板。

6) **模型选择的“经济学”**
- 机械实现用便宜模型；集成类用标准；架构/Review 用最强。

---

## 主题三：Cialdini 说服原则在 Superpowers 中的应用（会话1）

### Q4：Cialdini 说服原则强化指令这个是指什么？

**A（全量要点整理）：**

1) **起点：作者发现 LLM 遵从也受语言框架影响**
- Jesse Vincent 原本相信 Cialdini 原则能作用于 LLM；后来得知 Dan Shapiro 与 Cialdini 联合论文验证。
- 目的不是“操纵”，而是让 Agent 更可靠、更有纪律。

2) **学术依据（对话原文引用）**
- 论文：Meincke, Shapiro, Duckworth, Mollick, Mollick & Cialdini（2025）
- 标题：Call Me A Jerk: Persuading AI to Comply with Objectionable Requests
- N=28,000；合规率 33% → 72%；p<.001。

3) **七条原则逐一对照（对话全量要点）**
- Authority 权威：命令式 + 明确后果
  - 好：`Write code before test? Delete it. Start over. No exceptions.`
  - 坏：`Consider writing tests first when feasible.`
- Commitment & Consistency 承诺一致性：强制公开声明“我在用某 Skill”
- Scarcity 稀缺性：用压力场景测试在紧迫下是否仍守纪律（宕机损失/赶饭点）
- Social Proof 社会证明：用“大家都这么做”的叙述强化规范
- Unity 统一/身份：共同体叙事（我们一起做工程）
- Liking 喜好：说明理由，让规则显得合理
- Reciprocity 互惠：先提供方法论与知识，增强遵循动机

4) **最核心：反理性化设计（对话原文强调）**
- 对抗 LLM 善于找借口：不仅说规则，还要明确禁止绕过方式。
- 示例：`Violating the letter of the rules is violating the spirit of the rules.`
- TDD Red Flags 表把借口列出来逐一反驳。

5) **本质洞察**
- LLM 并非纯理性执行机，受社会心理机制影响；应把 skill 写成能心理层面“锁死”行为的文档。

---

## 主题四：用 Superpowers 开发项目的端到端过程（会话1）

### Q5：利用 Superpower 进行项目开发的典型过程是怎么样的？你从需求的澄清开始。

**A（全量要点整理，按对话“CLI Todo 工具”示例）：**

0) **Session 启动（自动）**
- SessionStart Hook 注入：`RIGHT NOW, go read ... getting-started/SKILL.md`。
- Claude 建立“必须先查 Skills”的纪律。

1) **阶段一：需求澄清（brainstorming Skill）**
- 不会立刻写代码，会逐一提问（每次只问一个）：
  - 场景、优先级、存储、本地/同步、命令风格、提醒等
- 方案分段呈现（A 极简 vs B 功能全）并用 YAGNI 裁剪。
- 设计文档写入并提交：`docs/superpowers/specs/...-design.md`
- 派 spec-document-reviewer subagent 审核（最多 5 次循环）。
- 通过后请人类确认进入下一阶段。

2) **阶段二：工作区隔离（using-git-worktrees Skill）**
- 例：`git worktree add ...`，安装依赖，跑测试基线（全绿）。

3) **阶段三：编写实现计划（writing-plans Skill）**
- 拆成 2–5 分钟微任务（Task 1..6），每个任务含路径/验证。
- 计划文件头部强制：必须用 subagent-driven-development。
- 派 plan-document-reviewer 审核任务拆分。

4) **阶段四：subagent-driven-development 循环**
- Controller 读计划 → TodoWrite
- 对每个 Task：
  - implementer（TDD：RED/GREEN/REFACTOR）→ commit → DONE 状态上报
  - spec reviewer → code quality reviewer
  - 不通过则返工闭环

5) **阶段五：最终整体 Code Review（requesting-code-review Skill）**
- 汇总优点与问题（Important/Minor），Important 阻塞继续，修复后再审。

6) **阶段六：收尾（finishing-a-development-branch Skill）**
- 给选择：合并到 main / 创建 PR / 保留 / 丢弃。
- 示例：用 `gh pr create ...` 创建 PR。

7) **时间线总览与人类介入点**
- 介入点只有三处：
  1) 回答需求澄清问题
  2) 确认设计与计划
  3) 最终选择 merge/PR 等收尾方式

---

## 主题五：Git/GitHub 工作流（会话1）

### Q6：这个 PR 和 merge 有什么差别？

**A（全量要点整理）：**
- Merge：本地合并 feature → main 并 push；无审查/讨论/记录；适合个人/小改动/低风险。
- PR：在平台上创建审查窗口；展示 diff、评论、触发 CI、保留讨论历史、合并策略（squash/merge/rebase）。
- 在 Superpowers 语境：内部审查是“Agent 审查 Agent”；PR 提供人类最终把关入口，最终合并决定权应留给人类。

### Q7：把一个完整的 GitHub 项目开发流程和命令给我解释一下（创建/checkout/特性开发/提交 PR 或直接 merge）。

**A（全量要点整理，含命令）：**

- 情景一：新项目
  - `mkdir && git init` → 写 README → `git add . && git commit` → `gh repo create --push` 或手动 `remote add` + `push -u`。
- 情景二：已有项目 checkout
  - `git clone` → `git status/log/branch -a`。
- 特性开发循环
  - `git checkout main && git pull origin main`
  - `git checkout -b feature/...`（或 `git switch -c`）
  - 开发→`git add`→`git commit`（Conventional Commits 格式）
  - `git push -u origin feature/...`
- 路径 A：PR
  - `gh pr create`（title/body/base）
  - review 反馈继续 commit+push，PR 自动更新
  - 合并：`gh pr merge --squash/--merge/--rebase`
- 路径 B：直接 merge
  - `git checkout main && git pull`
  - `git merge feature/...` → 解决冲突→commit
  - `git push origin main`
  - 删除分支：`git branch -d` + `git push origin --delete`
- 常用救命命令：restore/stash/amend/log/checkout - 等。

### Q8：`git checkout -b feature/add-priority` 如果原来没有这个分支，也是用这个命令创建新分支吗？

**A（全量要点整理）：**
- 是，`-b` = create and checkout。
- 等价：`git branch ...` + `git checkout ...`。
- 新 Git：`git switch -c ...`。
- 若分支已存在，`-b` 会报错，应直接 checkout/switch。

### Q9：这里使用 gh，这个和 git 不是同一套命令体系，它们俩是怎么衔接的？

**A（全量要点整理）：**
- Git：本地版本控制；gh：GitHub 平台功能（PR/Issue/Actions/Release…）CLI。
- 衔接点：远程仓库 URL（`.git/config` 的 remote origin url）。
- 代码 push 到 GitHub 后，gh 才能通过 API 操作对应 repo。
- 职责边界表：git 管分支/提交/推送；gh 管 PR/Issue/CI 等平台能力。
- gh 不是必须：也可浏览器网页操作。

### Q10：介绍一下查看 CI 状态、创建 Issue。

**A（全量要点整理）：**
- Issue：任务/问题追踪（bug/需求/技术债），生命周期 open→讨论→认领→修复→关联 PR→合并后关闭。
  - gh：`gh issue create/list/view/close`；PR 描述写 `Closes #42` 自动关闭。
- CI：每次 push/PR 自动跑检查（测试/lint/build/扫描等）。GitHub Actions 通过 `.github/workflows/*.yml`。
  - gh：`gh run list/view/watch`。
- 健康团队流程示例：Issue → 分支 → 开发 push 触发 CI → PR（Closes #42）→ merge → issue auto close。

### Q11：介绍 GitHub Actions 针对 CI 的常见用法和配置。

**A（全量要点整理）：**
- 基本结构：workflow（yml）→ job（VM）→ step（命令/Action）。
- 触发：push/pull_request/workflow_dispatch/schedule。
- Node 示例：matrix 多版本、setup-node cache、npm ci、lint/typecheck/test/build。
- Python 示例：setup-python cache、ruff/mypy/pytest、覆盖率上传。
- 多 job 依赖：`needs`。
- 缓存：setup-node cache 或 actions/cache + hashFiles。
- Secrets：GitHub Secrets 注入 env，日志会遮蔽。
- 分支保护：Require status checks、Require PR review、Block force pushes。
- 常用 actions：checkout/setup-node/setup-python/cache/upload-artifact、codecov、docker build/push、AWS/GCP 部署等。
- 调试：`gh run view --log`、rerun。

### Q12：lint 是什么？

**A（全量要点整理）：**
- 静态代码分析（不运行代码），发现风格问题、潜在 bug、危险写法。
- 与测试互补：lint 管“写法/规范”，测试管“逻辑/功能”。
- 常见工具：ESLint、Ruff/Flake8/Pylint、Clippy、golangci-lint、Stylelint。
- 放进 CI 作为强制门槛。

---

## 主题六：ECC（Everything Claude Code）——主体结构、机制与项目视角（会话2）

> 从本主题开始，问题来自会话2（ECC）。

### Q1：请你帮忙查找一下编程 Hackathon 的他们提出的 Claude Code 库是什么？

**A（全量要点整理）：**
- 主要库：`everything-claude-code`
  - GitHub：affaan-m/everything-claude-code
- 背景：Anthropic x Forum Ventures Hackathon 获奖（价值 $15,000 API credits）；8 小时内用 Claude Code 构建 zenith.chat；该套配置打磨了约 10 个月；在 X 上短期高曝光。
- 核心功能：不仅是配置文件，而是一套系统：skills、instincts、内存优化、持续学习、安全扫描、研究优先开发；包含生产就绪的 agents/hooks/commands/rules/MCP 配置；适配 Claude Code、Codex、Cowork 等。
- 内置安全扫描 AgentShield：`ecc-agentshield`（1282 测试、98% 覆盖、102 条静态规则），可扫描 CLAUDE.md、settings.json、MCP、hooks 等，涵盖机密检测、权限审计、hook 注入分析、MCP 风险分析。
- 也提到 Anthropic 官方 Claude Code 一周年 Hackathon（500 名、$500 credits/人、大奖 $100,000 credits 等背景信息）。

---

### Q2：请详细解释 ECC 的主体结构和关键机制；站在我开发项目的视角，它如何获取需求？需求改变如何管理？如何迭代？

**A（全量要点整理）：**

1) **整体架构：四层堆栈**
- Memory（CLAUDE.md / Memory）：“Claude 知道什么”
- Skills：“Claude 能做什么”（可复用工作流，概率性触发）
- Hooks：“Claude 必须做什么”（自动化触发器，确定性执行；exit code 2 可阻止操作）
- Agents：“谁来做”（专属子代理，并行/隔离上下文）
- 原则：CLAUDE.md 与 Hooks 更确定性；Skills/Agents 更概率性。

2) **文件结构示例**
- 项目根：`CLAUDE.md`
- `.claude/`：settings.json、rules/、skills/、agents/、.mcp.json

3) **记忆层级与技巧**
- 三级：项目级 CLAUDE.md（团队共享）→ 用户级 `~/.claude/CLAUDE.md`（个人偏好，不入库）→ Auto Memory（自动积累）。
- 经验阈值：200 行以内规则执行率高（对话里给了 200 行以内 92%，400 行以上 71% 的经验数据）。
- 命令式写法：把“项目用 TS”改成“所有新文件用 TS strict”。
- Auto Memory vs PreCompact：Auto Memory 是长期积累知识；PreCompact 是压缩前的状态快照，两者互补。

4) **需求如何流入（启动加载顺序）**
- 全局 `~/.claude/CLAUDE.md` → 项目 CLAUDE.md → `.claude/rules/`（按路径）→ Auto Memory → 当前指令。

5) **需求变更管理（分层处理）**
- 架构级变更（技术栈/API 设计）：更新 CLAUDE.md
- 规范级变更（代码风格/测试策略）：更新 `.claude/rules/`
- 流程级变更（部署/CI）：更新 Skill
- 强制约束（安全/格式硬门控）：更新 Hooks
- 警告：不要把频繁变化的执行计划写进 CLAUDE.md（避免“化石”）；计划用 issue tracker/commands/skills。

6) **迭代开发节奏（Hackathon 团队节奏）**
- 探索阶段：并行 2–3 个探索代理
- 澄清阶段：问边界/集成/性能，等待确认
- 架构选项：2–3 种
- 实现→审查→总结：需你批准计划后才编码
- 并行策略：按模块/文件夹分工避免冲突。

---

## 主题七：语音输入法项目落地蓝图（会话2）

### Q3：比如我想实现语音输入法，用 ECC 来做，具体实现过程怎么样？管理机制如何配合？

**A（全量要点整理，包含两次平台分歧的回答）：**

#### 3.1 iOS 键盘扩展方案（你明确回复：iOS 系统级输入法，从零开始，云端 API，语音转文字 + AI 优化 + MCP 对话）
- 架构模块：Keyboard Extension（录音→Whisper→AI 优化→MCP 对话 UI）+ 主 App（设置/授权）+ App Group 共享。
- CLAUDE.md 建议内容：targets、App Group、Swift/iOS 版本、内存上限、Open Access、权限、Keychain、外部 API、目录结构、构建/测试命令、并发约束。
- rules 示例：api-rules、keyboard-extension-rules。
- skills 示例：whisper-integration、ai-polish、mcp-connector。
- hooks 示例：修改键盘扩展代码时检查内存；PreCompact 保存进度快照。
- sprint：先最小闭环→接 Whisper→AI 优化→MCP。
- iOS 键盘扩展陷阱：录音/网络权限/生命周期/后台 kill/主线程 UI 等（对话给了 5 条陷阱清单）。

#### 3.2 Windows/Linux 桌面方案（你后续又出现“平台是 Windows/Linux 桌面”的分支）
- 核心挑战：全局热键 hook 与系统级文字注入。
- 推荐技术栈：Python 3.11+，pynput 热键，sounddevice 录音，aiohttp 异步 API，keyring 存 key，托盘 pystray，文字注入 Windows SendInput，Linux xdotool/ydotool，MCP WebSocket，PyInstaller 打包。
- CLAUDE.md 示例：core/api/ui/config/tests 目录，关键约束（超时、keyring、临时音频删除、平台分支等）。
- rules 示例：api-rules、platform-rules、ui-rules。
- skills 示例：recording-pipeline、text-injection、ai-polish-pipeline、mcp-chat。
- hooks 示例：检查 imports/硬编码 key；PreCompact 保存进度。
- 从零启动：Day 1 先做热键+录音原型（只打印“录音结束”），然后 Day2 接 Whisper，Day3 文字注入，Day4-5 AI 优化+托盘，Day6-7 MCP。

---

## 主题八：新增模块/目录时，CLAUDE.md / rules / skills 维护会不会爆炸？（会话2）

### Q4：新增目录/模块是不是 CLAUDE.md 也要跟着改？自动化吗？Skill 更新会不会遗漏？

**A（全量要点整理）：**

1) **直接回答：不是完全自动**
- 新需求→Claude 实现代码 ✅
- 目录/文件创建 ✅
- CLAUDE.md 自动更新 ❌
- Skill 自动更新 ❌
- Rules 自动更新 ❌

2) **解法一（推荐）：CLAUDE.md 写“自维护元规则”**
- 当新增目录/模块，完成实现后主动更新 CLAUDE.md 的“目录结构”章节，不需要询问。

3) **解法二：Hook 自动同步结构**
- PostToolUse 触发脚本扫描目录树并更新 CLAUDE.md 目录章节；一次性成本，让 Claude 写脚本。

4) **解法三：Skill 从实践中提炼，不需要预先写好**
- 第一次做某事：直接对话实现
- 第二次重复：总结成 Skill
- Skill 是终点，不是起点

5) **解法四：用 PROJECT_LOG/CHANGELOG 替代频繁改 CLAUDE.md**
- CLAUDE.md 保持稳定，只引用日志。

6) **真实维护成本的诚实结论**
- 约束变化需更新 rules
- Claude 自动更新内容仍需 review
- Skill 需要调整时要编辑 SKILL.md
- 但成本远小于每次新会话重新解释背景。

---

## 主题九：ECC 的实际项目最佳实践（会话2）

### Q5：找一下实际项目使用过程中的最佳实践有哪些？要举例说明。

**A（全量要点整理：九条实践 + 语音输入法例子）：**

1) `/init` 自动生成 CLAUDE.md 初稿，再精炼
2) Plan Mode（Shift+Tab 两次）：先规划再动手；暴露风险点（例：Linux pynput 权限）
3) 用“参照物提示”替代空泛需求：参照已有模块风格
4) `.claudeignore` 降噪：排除 venv、构建产物、临时音频等（例：排除 `*.wav` 防止吃上下文）
5) 任务粒度极其精确：防“蝴蝶效应”（给出危险写法 vs 安全写法表）
6) 两次纠错就 `/clear`：上下文污染时重开更优（给了 Wayland 例子）
7) Subagent 做隔离扫描/调研：主会话保持干净，节省 token
8) 每次有效改动后立刻 commit：建立回滚安全网（给了 commit 示例）
9) “访谈模式”处理模糊需求：先问清楚→写 spec→新会话实现（给了 MCP 访谈例子）

核心一句话：控制 Claude 看到的信息质量，而不是控制 Claude 本身。

---

## 主题十：你要求“把我提的问题全部列一下”（会话2）

### Q6：你把我提的问题全部列一下。不要有遗漏。

**A（对话原文列出的 6 个问题）：**
1) 查 Hackathon 的 Claude Code 库是什么？
2) 解释主体结构与关键机制；从项目视角：需求获取/变更管理/迭代
3) 语音输入法用这个项目做，具体实现与机制配合
4) 新增目录/模块与 CLAUDE.md/Skill 更新是否自动、是否容易遗漏
5) 实际项目最佳实践（举例）
6) 把问题全部列一下（本题）

---

## 主题十一：你要求“整理截止到现在所有问题及结论/解法要点”（会话2）

### Q7：请整理截止到现在我提到的所有问题以及对应的结论和解法要点（每题列关键 2–3 个解法或优选解法）。

**A（对话原文的 Q1–Q6 汇总要点）：**
- Q1：ECC 是 Hackathon 获奖库；内置 agentshield 等
- Q2：四层堆栈；需求加载顺序；变更分层（CLAUDE.md/rules/skills/hooks）
- Q3：语音输入法技术栈/CLAUDE.md 内容/核心 skills/迭代节奏
- Q4：不完全自动；推荐元规则自维护；PROJECT_LOG；Skill 从实践提炼
- Q5：九条实践，关键 3 条（Plan Mode、两次纠错就 clear、任务粒度精确）
- Q6：共 6 个问题
- 跨问题主线：把“如何与 Claude 协作”系统化、文件化、自动化。

---

## 主题十二：ECC vs Superpowers 对比与市场定位（会话2）

### Q8：把 ECC 和 Superpowers 针对我实现语音输入法进行对比，并查市场定位差异。

**A（全量要点整理）：**

1) 市场定位一句话
- Superpowers = 给 Claude 装上高级工程师工作方法论（纪律、TDD、强制）
- ECC = 给 AI 开发环境做全面性能调优（配置系统、Token 优化、跨工具）

2) 核心机制对比表（对话原文要点）
- skill 触发：ECC 概率性；Superpowers 强制
- TDD：ECC 无强制；Superpowers 强制（先写实现则删掉重来）
- 规划：ECC Plan Mode + 记忆；Superpowers 固定 7 阶段
- 记忆：ECC CLAUDE.md + Auto Memory；Superpowers 设计/计划文档落盘（不强调自动记忆）
- 安全：ECC 有 agentshield；Superpowers 无
- Token：ECC 设计；Superpowers 轻量
- 安装：ECC 模板仓库；Superpowers 插件市场安装

3) 语音输入法场景对比
- Whisper 接入：Superpowers 流程重但质量高；ECC 灵活但依赖规则质量
- Wayland bug：Superpowers systematic-debugging 强；ECC 依赖 platform-rules
- 新增 MCP：Superpowers 强制澄清；ECC 需要访谈/规则固化

4) 综合建议：两者配合
- Superpowers：需求澄清、TDD、系统调试、分支/PR
- ECC：跨平台规则持久化、API 约束、.claudeignore/token、agentshield

---

## 主题十三：社区组合使用（Superpowers + Context7 + feature-dev …）如何配合（会话2）

### Q9：社区组合使用 Superpowers + Context7 + feature-dev … 怎么配合？请详细展开。

**A（全量要点整理）：**

1) 为什么组合（各自盲区）
- Superpowers：纪律强但可能 API 过时
- Context7：文档最新但不强制 TDD/规划
- ECC：规则持久但缺实时文档与强制流程

2) Context7 的职责
- 解决“API 幻觉/过时 API”问题：通过 MCP 工具 `resolve-library-id`、`query-docs` 拉取版本特定文档。
- 不需要特殊口令，技能自动识别何时需要文档并检索。

3) feature-dev 的职责
- 需求模糊时并行探索 2–3 个方案（探索→澄清→选型→实现/审查/总结）。
- 与 Superpowers 区别：feature-dev 更像规划协调器，不强制 TDD。

4) Sequential Thinking MCP
- 强制走系统性推理链，适用于复杂跨平台问题；最好与 Context7 搭配。

5) 推荐组合工作流（对话原文流程）
- feature-dev 并行探索方案
- Superpowers brainstorming 追问并固化设计
- Context7 在实现前拉最新版文档
- Superpowers TDD 强制
- ECC rules 提供平台/API 细则
- Superpowers systematic-debugging 解决 bug
- commit-commands 生成规范 commit message

6) “少即是多”
- 插件过多会吃掉上下文；建议按需启用。
- 社区“甜蜜点”：4 插件 + 2 MCP（Language Server + Superpowers + commit-commands + pr-review-toolkit；Context7 + Sequential Thinking）。

---

## 主题十四：ECC 的“跨平台规则持久化”是什么意思（会话2）

### Q10：ECC 的跨平台规则持久化具体是指什么？

**A（全量要点整理）：**
- 把 Windows/Linux 平台差异（SendInput/xdotool/ydotool、自启、平台判断等）写入 `.claude/rules/platform-rules.md`。
- 没有规则：每次新会话都可能写错（需要你重复纠正）。
- 有规则：每次会话自动加载，长期不忘。
- “跨平台”只是规则内容主题；同理可持久化 API 规则、测试规则等。

---

## 主题十五：你问“rules 是否需要手动调用 ECC / 只用 rules 会不会流程不完整”（会话2）

### Q11：我用 Superpowers 开发时，rules 要手动调用 ECC 吗？只调用 rules 会不会流程不完整？

**A（全量要点整理）：**
- 关键纠偏：ECC 不是需要调用的工具。
- `.claude/rules/` 不是 ECC 独有，是 Claude Code 原生能力，会按目录自动加载。
- 会话加载顺序（对话原文）：全局 CLAUDE.md → 项目 CLAUDE.md → rules → Auto Memory → 插件注入（Superpowers/Context7）→ 当前指令。
- 规则与 Superpowers 的关系：rules 是背景约束；Superpowers 是流程纪律；Context7 是实时文档；三者天然同时工作。
- 可能瑕疵：rules 与 Superpowers 流程冲突时需在 CLAUDE.md 声明优先级（例如“Superpowers 工作流 > rules 细则；rules 只补充细节”）。

### Q12：我需要从头做 ECC 流程吗？还是只需要定义 rules 阶段？

**A（全量要点整理）：**
- ECC 没有可运行的“流程”；它是参考模板仓库。
- 实操：在 Superpowers brainstorming 确认约束后，让 Claude 把约束写成对应 rules 文件；30 秒完成，不打断后续 TDD/review。
- 什么时候创建规则文件：
  - brainstorming 确认技术约束
  - 同一问题被纠正两次
  - 新模块有特殊要求

---

## 主题十六：Superpowers（插件）与 Skill 的区别；ECC 又是什么（会话2）

### Q13：Superpowers 是插件，那插件与 Skill 的关系区别是什么？

**A（全量要点整理）：**
- Skill = 一个 `SKILL.md`（纯文本指令）
- Plugin = 把多个 Skill 打包 + 安装/分发（manifest），可一键安装
- 你自己写的 Skill（`.claude/skills/`）项目专属；Plugin 是通用打包发布。
- Superpowers 提供通用工程方法论；你项目技能提供语音输入法专属工作流。

### Q14：那 ECC 呢？

**A（全量要点整理）：**
- ECC 既不是 plugin 也不是 skill；是最佳实践样板集合/参考模板仓库。
- 用途：不知道某类文件怎么写时，去翻它的示例“抄结构与写法”。

---

## 主题十七：你要求“用 ECC 从 Day1 开始详细描述开发语音输入功能过程”（会话2）

### Q15：假设我要开发前面说的语音输入功能，那么用 ECC 开发的具体过程，请详细描述。

**A（全量要点整理，按对话 Day1→Day7）：**

1) Day1 上午：初始化项目结构 + 配置体系
- 建项目骨架：创建 `.claude/rules`、`.claude/skills`、`.claude/agents`、`.claude/hooks`；代码目录 core/api/ui/config/tests。
- 运行 `/init` 自动生成 CLAUDE.md 初稿，再补充项目专属约束（技术栈、异步、keyring、超时、临时音频删除、平台分支、自维护规则、命令）。

2) Day1：按需创建 rules 文件（先两个最核心）
- `api-rules.md`：aiohttp、超时、keyring、Whisper 分片/错误分类、Claude AI 优化策略。
- `platform-rules.md`：Windows/Linux 差异（SendInput/xdotool/ydotool、Wayland 检测、自启等）。

3) Day1 下午：第一个功能（录音热键）
- 先要计划，不写代码；确认后实现 hotkey/recorder/main 组装。
- 跑通后立刻 commit。

4) Day2：第一个 Skill 自然浮现
- 接 Whisper 时发现步骤可复用 → 提炼 `whisper-integration` skill（含触发条件/步骤/测试要求）。

5) Day2 下午：Hooks（对话后又纠偏为：规范检查更适合 rules）
- 初始做法：PostToolUse 写脚本检查 requests 与硬编码 key；settings.json 配 hook。
- 纠偏结论：规范检查更适合写入 rules（声明式更易维护）；hook 留给真正需要程序执行的事（如 PreCompact 保存进度快照、SessionEnd 追加日志）。

6) Day3–7：中期迭代节奏（固定循环）
- 每次：读 CLAUDE.md + 对应 rules（自动）→ 计划→实现→hook（若有）→测试→必要时提炼 skill / 更新规则→commit。
- Day3：AI 优化层（读 api-rules 知道超时/跳过规则）
- Day4：文字注入（读 platform-rules 知道分平台实现）
- Day5：托盘 UI（新模块出现，依赖自维护元规则更新 CLAUDE.md 目录结构）
- Day6–7：MCP（先访谈+写 spec，再 clear 开新会话实现）。

7) 目录体系最终样貌（对话原文示例）
- `.claude/settings.json`
- `.claude/rules/`：api/platform/mcp...
- `.claude/skills/`：whisper-integration/text-injection/ai-polish...
- `.claude/hooks/`：check_code.py/save_progress.py（其中 save_progress 是否需要取决于是否会遇到 compact）

8) 与单纯用 Superpowers 的区别
- Superpowers：保证流程纪律
- ECC rules：保证第 30 天开新会话仍遵守平台/API 约束；新模块目录可通过元规则自动同步；必要时 hook 做真正“程序型”保障。

---

## 主题十八：你对“把检查放在 Hook 还是 rules”提出质疑（会话2）

### Q16：第五步是不是直接写入 rules 更合适？PostToolUse 会不会后面要持续改，越来越复杂？

**A（全量要点整理）：**
- 结论：你的判断对。
- PostToolUse Hook 是“程序化检查逻辑”，新增规则要改脚本；维护成本会上升。
- rules 是“声明性自然语言规范”，新增规则只需加一行文字。
- 修正做法：把代码规范检查写进 rules（如 api-rules）；Hook 用于 rules 做不到的“必须程序执行”的事（PreCompact/SessionEnd 等）。

### Q17：save_progress.py 是做什么的？前面推导过程没有。

**A（全量要点整理）：**
- 你观察正确：它在第五步被“顺带引入”，理由不够自然。
- 作用：应对 Claude Code Compact（压缩）导致细节丢失；在压缩前保存工作状态快照（正在做什么、已完成接口、未解决 bug、下一步计划），压缩后读文件恢复状态。
- 是否需要：不一定；如果你的节奏是“小功能跑通就 commit，然后 /clear 开新会话”，就不太需要；只有长会话连续做复杂模块才值得配置。

---

## 附录A：按时间顺序的“问题→回答”索引（快速定位）

### 会话1（Superpowers）按顺序问题列表
1) 分析 Superpowers 结构与原理
2) subagent、code review、TDD 的嵌入与任务传递
3) subagent 如何被调用与发起
4) Cialdini 说服原则强化指令是什么
5) 用 Superpowers 开发项目的典型过程（从需求澄清开始）
6) PR vs merge
7) 完整 GitHub 项目开发流程（创建/checkout/特性开发/PR/merge）
8) checkout -b 是否创建新分支
9) gh 与 git 如何衔接
10) CI 状态与 Issue
11) GitHub Actions CI 配置
12) lint 是什么

### 会话2（ECC）按顺序问题列表
1) Hackathon 提到的 Claude Code 库是什么
2) 主体结构与机制；需求获取；变更管理；迭代
3) 语音输入法如何做（iOS→后续又给 Windows/Linux 方案）
4) 新增模块/目录与 CLAUDE.md / rules / skills 维护是否自动、是否会遗漏
5) 实际项目最佳实践（举例）
6) 列出我提的问题（不遗漏）
7) 汇总截止到现在所有问题与结论/解法
8) ECC vs Superpowers 对比与市场定位
9) 组合使用 Superpowers + Context7 + feature-dev 的协作方式
10) ECC 的跨平台规则持久化是什么意思
11) rules 是否需要手动调用 ECC、只用 rules 会不会流程不完整
12) 是否要从头做 ECC 流程/还是只定义 rules 阶段
13) 插件 vs skill 的区别
14) ECC 是什么
15) 用 ECC 从 Day1 开始开发语音输入功能的详细过程
16) 检查项放 rules vs PostToolUse Hook 的取舍
17) save_progress.py 的用途与是否必要

---

## 结语

两段会话共同给出了一条“高可靠 AI 工程协作”的主线：
- 用 **Superpowers** 把工程纪律（澄清/计划/隔离/TDD/审查/收尾）变成强制流程，降低“直接开写”带来的返工与质量风险。
- 用 **ECC 的文件体系（CLAUDE.md + rules + skills + hooks + agents）** 把项目知识与约束沉淀为长期资产，避免“会话结束即失忆”。
- 用 **Context7** 解决实时文档与 API 过时问题；用 **feature-dev/Sequential Thinking** 在需求模糊或复杂问题时做并行探索/慢思考。
