# AI 原生公司到 Harness Engineering：对 Hermes 与 OpenClaw 的启发

## 来源

本笔记整理自 2026-05-23 对三条 YouTube 视频的内容汇总与延伸判断。

### 引用链接

1. 第一条：AI 原生公司组织形态  
   https://youtu.be/t-G67yKAHBQ?si=RdbVI8LtKGMnKOxo
2. 第二条：AI 作为 Company OS / Closed-loop Company  
   https://youtu.be/EN7frwQIbKc?si=vSTRPdgv1jA-ZArr
3. 第三条：OpenAI Ryan Laapo - Harness Engineering  
   https://youtu.be/am_oeAoUhew?si=d0Il5peTMxe8IX0m

---

## 核心结论

这三条视频不是三组孤立观点，而是一条完整链条：

```text
AI-native company
→ closed-loop company OS
→ harness engineering
```

换句话说：

- 公司层面：公司不再是罗马军团式层级组织，而是一组 recursive self-improving AI loops。
- 流程层面：公司必须 queryable、legible、closed-loop，所有关键过程都能被 AI 读取、反馈和改进。
- 工程层面：代码库、文档、CI、review、lint、tests、skills 都要被设计成 agent harness，让 agents 能稳定执行完整工程任务。

对 Hermes / OpenClaw 来说，最重要的启发是：

> Hermes 的价值不只是回答问题，而是构建一个持续积累上下文、修正错误、自动执行、自动复盘、自动改进的个人/组织操作系统。  
> OpenClaw 的价值不只是多 Agent 跑任务，而是把需求、规格、测试、review、质量门和知识沉淀组成可重复的 agent software factory。

---

## 和前两条视频的关系

第三条 Harness Engineering 和前两条 YC / AI-native company 视频是同一思想在不同层面的展开。

### 第一条：公司形态

第一条强调宏观组织哲学：

- 传统公司像罗马军团，依赖层级、汇报链和中层管理。
- AI 原生公司应该是一组自我改进循环。
- 公司最重要的资产是可被 AI 理解的领域知识。
- 软件可以临时生成，数据、经验、业务语境和 skills 才是长期资产。
- 人类从信息管道变成现实接口、方向判断者和最终责任人。

这一条回答的是：

> AI 时代的公司应该长什么样？

### 第二条：创业公司运营

第二条更像创始人落地手册：

- AI 不是 productivity tool，而是 company OS。
- 公司要从 open loop 变成 closed loop。
- 所有关键行为都要留下 artifact，让公司对 AI queryable / legible。
- 工程管理、sprint planning、客服、销售、招聘、运营都应该被智能层持续分析和反馈。
- 未来组织角色变成 IC / builder / operator、DRI、AI founder。
- 优化目标从 headcount maxing 转向 token maxing 和 agent throughput。

这一条回答的是：

> 创业公司现在应该怎样把 AI 放进公司运行系统里？

### 第三条：工程实现

第三条 Harness Engineering 把前两条落到软件工程现场：

- 代码不再是稀缺资源，implementation is no longer the scarce resource。
- 真正稀缺的是 human time、human/model attention、model context window。
- 工程师的新职责是设计规格、约束、反馈机制和执行环境。
- repo 结构、AGENTS.md、skills、lint、tests、CI、review agents、PR 流程、错误信息都要成为 agent harness。
- 每周 Garbage Collection Day 用来消灭反复出现的失败类别，把 review 负担转成文档、skill、lint、test、CI 或 reviewer agent。

这一条回答的是：

> 如何让 agent 真正稳定地写代码、跑测试、review、修 bug、交付软件？

### 三者的统一表达

```text
公司层面：AI-native company
流程层面：closed-loop company OS
工程层面：harness engineering
```

三者共同指向一个判断：

> 未来的核心竞争力不是“用了多少 AI 工具”，而是能否把业务、流程、工程和组织设计成可被 AI 持续学习、执行、验证、改进的闭环系统。

---

## 对 Hermes / OpenClaw 的直接启发

### 1. Hermes 要从聊天助手升级为个人 / 组织操作系统

Hermes 不应该只追求“回答得好”。更重要的是形成操作循环：

```text
输入线索
→ 收集上下文
→ 执行任务
→ 生成 artifact
→ 验证结果
→ 记录状态
→ 沉淀 skill / memory / playbook
→ 下次表现更好
```

对应到 Hermes 当前系统：

- Discord / Feishu / Weixin / Yuanbao 是 sensor layer。
- Obsidian / Get笔记 / session DB / memory / skills 是 shared memory。
- terminal / file / web / browser / MCP / cron 是 tool layer。
- 测试、review、git diff、用户确认、cron 报告是 quality gate。
- Garbage Collection Day、日报、skill patch 是 learning mechanism。

需要继续加强的是最后两层：质量门和学习机制。

### 2. OpenClaw 应该按 agent software factory 设计

OpenClaw 做项目执行时，不应该直接让多 Agent 并行写代码。那只会并行制造 slop。

更好的顺序是：

1. 人类或 Hermes 先写 PRD / spec。
2. 定义 acceptance criteria。
3. 补 test harness / eval / QA checklist。
4. 拆成 Kanban cards。
5. implementation agent 执行。
6. reviewer agents 按 persona 做 review。
7. verification agent 跑测试和验收。
8. 失败原因回流到 skill、lint、test、文档。

这就是 OpenClaw 版的 software factory：

```text
Spec + Tests + Docs + Guardrails + Review Personas
→ Agents compile implementation
→ CI / QA / Review gates accept or reject
→ Failure categories become better harness
```

### 3. Skill 不应该越多越散，而要少数高杠杆、持续维护

Ryan 的经验偏向 5-10 个核心高杠杆 skills，而不是几千个碎片 skill。

对 Hermes 来说，这意味着：

- skill 数量不是 KPI。
- 高频工作流要沉淀成强 skill。
- skill 必须持续维护，过期 skill 比没有 skill 更危险。
- 工具细节应该隐藏在 skill 后面，用户不需要记底层命令。
- 每次用户纠正、工具失败、流程中断，都应该判断是否 patch skill。

适合成为核心 skill 的方向：

- Obsidian + Get笔记双写。
- Hermes runtime / gateway / profile 运维。
- 多主机 Hermes 协作。
- Kanban 工程执行。
- PRD / Plan / Tests / Review 工作流。
- 周复盘 / Garbage Collection Day。

### 4. 错误信息要写给 agent 看

未来的 lint、CI、脚本报错不应该只说“失败”。它们应该告诉 agent：

- 错在哪里。
- 为什么错。
- 正确模式是什么。
- 应该用哪个命令修复或验证。
- 常见误区是什么。

例如不要只输出：

```text
sync failed
```

而应该输出：

```text
Get笔记同步失败：缺少 path→note_id 映射。不要创建重复 note。请先读取 /root/.openclaw/workspace/config/getnote_sync_map.json；若不存在，使用 OpenAPI fallback 并在回执中标记幂等风险。
```

这类错误信息本身就是 prompt injection 到工程系统里，是 agent harness 的一部分。

### 5. 用户纠正必须进入 harness 改进

如果用户反复纠正 Hermes：

- 没有保存笔记。
- 没有同步 Get笔记。
- 没有跑测试。
- 没有继续做完。
- 只说“我可以做”，但没有实际执行。
- Feishu / Discord topic 行为混淆。
- 任务没有沉淀成 skill 或 memory。

这些不应该只留在聊天上下文里。应该被转化为：

- memory：稳定偏好和长期事实。
- skill patch：可复用流程。
- SOUL / AGENTS.md 规则：全局执行纪律。
- checker：任务结束前的验证清单。
- cron / Garbage Collection Day：周期性复盘。

也就是说，用户纠正不是一次性反馈，而是系统训练数据。

### 6. Hermes Garbage Collection Day 是关键闭环

Garbage Collection Day 不只是“周报”。它应该是 Hermes harness self-improvement loop。

每周检查：

- 用户纠正了什么？
- 哪些任务失败或半途停了？
- 哪些工具调用失败？
- 哪些同步脚本、cron、MCP、profile 出问题？
- 哪些 skill 过期、缺步骤或互相冲突？
- 哪些重复劳动应该封装成工具或 skill？
- 哪些 memory 已经陈旧、过满或不该长期保存？
- 哪些项目/Area 状态没有更新？

每周产出：

- skill patch。
- 新 playbook。
- 新 checker。
- memory cleanup 建议。
- cron / gateway / devbox / tool health report。
- 下周最高杠杆改进清单。

这正好对应 Ryan 团队的每周五工程垃圾回收，只是 Hermes 版本安排在每周六上午 9 点。

### 7. PRD / Plan / Tests 比代码更重要

如果 OpenClaw 要承担大的开发任务，最稀缺的不是写代码，而是：

- 需求规格是否清楚。
- 完成标准是否可验证。
- 测试是否能给 agent 反馈。
- review persona 是否明确。
- QA checklist 是否覆盖关键风险。
- 失败时是否能自动定位原因。

因此新项目不应该直接开工编码。更合理的项目启动包是：

```text
PRD
Architecture
Implementation Plan
Acceptance Criteria
Test Plan
Review Personas
Rollback / Risk Plan
Kanban Card Breakdown
```

这也符合当前偏好：新项目先项目启动包 / PRD / 架构 / Plan，不直接编码。

### 8. Reviewer agents 要 persona 化，并只抓 P2 以上问题

OpenClaw / Hermes 的 review 不应该只有一个笼统的“代码审查”。应该拆成 persona：

- 架构 reviewer：边界、模块、抽象、可演进性。
- 安全 reviewer：权限、鉴权、注入、敏感信息、外部副作用。
- Reliability reviewer：重试、超时、幂等、错误恢复、日志。
- 产品 reviewer：是否满足用户真实目标。
- 测试 reviewer：关键路径、回归风险、可重复验证。
- 文档 / 知识库 reviewer：是否沉淀到 Obsidian、skill、memory。
- 用户偏好 reviewer：是否违反 cofol1986 的长期偏好。

但 reviewer agents 不能变成完美主义噪音源。原则是：

> 只抓 P2 以上会阻塞交付、导致风险或明显返工的问题。细枝末节不要打断主流程。

### 9. “需要用户提醒继续”应视为系统 bug

Ryan 的观点是：

> Every time I have to type continue to the agent is a failure of the harness.

对 Hermes 来说，这条非常关键。

如果工具可用、权限足够、风险可逆，Hermes 不应该停在：

- “我可以继续。”
- “如果你愿意，我可以……”
- “下一步建议……”
- “我会稍后处理。”

而应该直接继续执行、验证、回执。

真正需要停下来问用户的情况只有：

- 发布 / 发消息 / 购买 / 删除 / 不可逆操作。
- 需求存在会改变执行路径的关键歧义。
- 权限、凭证、目标环境缺失且无法自行获取。
- 高风险决策需要人类拍板。

这条已经写入 Hermes 执行纪律，但需要通过 Garbage Collection Day 和任务结束 checklist 持续检查。

### 10. 代码、内部工具和 dashboard 可以临时化，知识和上下文要长期化

三条视频都反复强调：软件越来越像 build artifact，知识、数据、流程、约束才是源代码。

对 Hermes / OpenClaw 的含义是：

- 临时 dashboard / HTML artifact / 小脚本可以快速生成和丢弃。
- 但领域知识、用户偏好、项目状态、失败原因、skill、test、decision log 必须长期保存。
- Obsidian 是 source of truth，Get笔记是同步/移动访问层，session DB 是可追溯记录，memory 只存稳定偏好。

这和当前 Vault 的 AGENTS.md 方向一致。

---

## 可落地动作

### 已落地

- Hermes Garbage Collection Day 已安排为每周六上午 09:00。
- `35-Areas/Hermes Agent 基础设施.md` 已记录该 recurring check。

### 建议下一步自动推进

1. **建立 Garbage Collection Day Playbook / Skill**  
   把每周复盘固定成可执行清单：系统健康、失败任务、用户纠正、skill patch、memory cleanup、项目状态、下周动作。

2. **为 OpenClaw 项目执行建立启动包模板**  
   包含 PRD、架构、验收标准、测试计划、review persona、Kanban 拆解。

3. **恢复或重建 Obsidian → Get笔记同步脚本**  
   当前 fallback 缺少幂等映射，日报/周报这类 recurring note 容易重复创建。

4. **设计 Hermes 任务完成 checklist**  
   检查是否已执行、验证、保存、同步、回执、沉淀 skill/memory，避免“建议但没做”。

5. **建立 reviewer persona 文档**  
   先从架构、安全、可靠性、测试、知识库五类开始，不要一开始做太多。

---

## 应更新的规则或 skill

### 应新增或加强

- `garbage-collection-day` skill：每周系统复盘与 harness 改进。
- `openclaw-project-startup-pack` skill：新项目启动包与验收设计。
- `agent-review-personas` skill：多 persona review 标准。
- `hermes-task-completion-checklist` skill：任务结束前验证与沉淀。

### 应纳入现有规则

- 用户纠正默认进入 harness 改进判断。
- 工具错误信息要写成 agent 可执行修复提示。
- 长任务结束必须确认是否有 skill / memory / Obsidian 更新价值。
- 重复失败不能只在日报里抱怨，要变成修复项。

---

## 暂不采用的部分

### 1. 不盲目追求大量 skill

Ryan 提到 5-10 个高杠杆 skills 的思路更适合当前 Hermes。不要为了“看起来系统化”创建大量低质量小 skill。

### 2. 不让 agent 自动作出高风险外部操作

自动化可以研究、起草、检查、生成、复盘，但仍不应擅自：

- 发布内容。
- 发消息给外部人。
- 合并 PR。
- 购买。
- 删除数据。
- 改不可逆配置。

### 3. 不把多 Agent 并行当成默认答案

多 Agent 只有在 spec、测试、review 和质量门足够明确时才有价值。否则只是更快地产生不一致的结果。

### 4. 不把代码完全视为无价值

“代码是 disposable build artifact”适用于趋势判断，但当前项目仍需要可读、可维护、可审查的代码。约束、测试、文档是源，代码仍是交付物和运行实体。

---

## 我的判断

这三条视频对 Hermes / OpenClaw 的最大价值，是把“AI 工具使用”提升到“系统设计”层面。

真正应该建设的不是更多 prompt，而是：

```text
Memory
+ Tools
+ Skills
+ Tests
+ Review Personas
+ Cron / Monitor
+ Garbage Collection
+ Human Approval Boundaries
= Self-improving Agent Operating System
```

Hermes 当前已经有很多基础件：多平台入口、工具调用、skills、memory、Obsidian/Get笔记、cron、devbox、Kanban 倾向。下一阶段最该补的不是再接一个工具，而是让失败、纠正、重复劳动和项目结果持续回流为 harness 改进。

一句话：

> Hermes / OpenClaw 的方向不应该是“更聪明的聊天机器人”，而应该是“能把每次工作都转化为下一次更强执行力的闭环系统”。
