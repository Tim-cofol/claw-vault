---
title: Boris Cherny：Claude Code 与工程未来
date: 2026-06-07
source: https://www.youtube.com/watch?v=RkQQ7WEor7w&t=1s
publisher: WorkOS / Acquired Unplugged
author_or_speaker: Boris Cherny
tags:
  - AI编程
  - ClaudeCode
  - Agent工作流
  - 组织设计
  - Hermes
---

# Boris Cherny：Claude Code 与工程未来

> 来源：[Boris Cherny: Claude Code & the Future of Engineering | Acquired Unplugged presented by WorkOS](https://www.youtube.com/watch?v=RkQQ7WEor7w&t=1s)

## 核心 thesis

Claude Code 的意义不只是「AI 帮工程师写代码」，而是把工程工作的抽象层从手写代码推进到：设计任务、设计反馈循环、组织多个 Agent 并验证结果。随模型能力提升，工程、产品、设计、数据分析等角色边界会被压缩到更通用的 `builder` 角色里。

## 背景：Claude Code 怎么来的

Claude Code 起源于 Anthropic 内部 late 2024 的 Labs/prototyping 团队。这个团队的目标是探索「下一个大产品」，同时反过来推动模型能力改进。

当时 Anthropic 有一种明显的 `product overhang`：模型已经能做很多事，但还没有足够好的产品把能力释放出来。编码是一个很自然的切入点：

- 代码有大量训练数据；
- 结果相对可验证：能否编译、能否测试、能否运行；
- 商业价值强；
- 工具使用、computer use、真实世界交互都可以在 coding 场景中被观察；
- 对 Anthropic 来说，coding 也是研究 AI safety 的「野外实验场」。

早期 Claude Code 并不好用，只能写 Boris 大约 10–20% 的代码。后来的跃迁主要来自两部分：

1. 底层模型持续变强，例如 Sonnet 4、Opus 4、Opus 4.5；
2. 产品 harness 和使用形态持续改进，包括 CLI、desktop、mobile、Slack、GitHub、plan mode 等。

Boris 的判断很直接：从「能写多少代码」这个指标看，最大的 step change 来自模型能力，而不是外围产品小功能。

## Anthropic 内部怎么用 Claude Code

Anthropic 内部几乎所有人每天都在用 Claude Code，包括模型研究员和产品团队。它既是产品，也是模型改进的反馈环。

几个关键变化：

- 新员工 ramp-up 从过去几周缩短到大约两天；
- 新人不再大量问同事「数据库怎么查」，而是打开 Claude Code，让它在代码库里找 skill、查库、跑分析；
- 每位工程师的代码产出显著上升。访谈中提到以前公开过约 3x，但这个数字已经过时；
- 团队规模扩大后，传统组织中常见的生产力下降被部分抵消，因为 AI 降低了 onboarding 和协作摩擦。

这里的关键不是「每个人更快打字」，而是组织里的信息寻路、上下文读取、局部自动化都被 Claude Code 接管了一部分。

## 「写代码」的定义正在变化

Boris 用自己的工作流描述了抽象层变化：

1. 以前是在 IDE 里写代码，搭配 autocomplete；
2. 后来不用 IDE，主要通过 Claude Code 写代码；
3. 再后来同时运行 5–10 个 Claude Code 实例；
4. 现在进入下一层：不是自己 prompt Claude，而是写循环，让 Claude 自己 prompt Claude、自己决定下一步。

这句话是整期最重要的判断之一：

> 我的工作是写 loops。

这意味着未来工程师的高价值工作可能从「直接实现」迁移到：

- 设计任务循环；
- 设计验证机制；
- 设计 Agent 之间的分工与通信；
- 设计失败恢复与 stop-loss；
- 判断什么时候应该继续自动跑，什么时候应该人工介入。

## Claude Co-work：从工程师工具到大众工具

Claude Code 起初是 CLI，因为最早的强需求来自工程师。但 Anthropic 后来发现，非工程师也愿意为了 Claude Code 学终端、装 Node、配置 API key。

例子：Anthropic 的数据科学家为了用 Claude Code 做数据分析，主动学会打开终端、安装工具、配置 API key。很快，多个数据科学家同时开多个 Claude Code 窗口做分析。

Claude Co-work 的定位是：

> 把 Claude Code 的能力给不想打开终端的人用。

他们试过 Slack bot、web app 等形态，但效果不好：

- Slack bot 很难做出好体验；
- 浏览器里缺少对本地文件和工具的访问；
- 拖文件进浏览器这种小摩擦足以破坏体验。

最后桌面形态更合理，因为它能接触本地文件系统和用户日常工具。

## 组织设计：从专职角色到 builder/generalist

访谈里对组织设计的判断很激进。

传统产品开发流程是：

```text
用户研究 → 设计 → PM scope → 工程实现
```

但 Claude Code 团队内部已经不是这样了。每个工程师都在：

- 做 scope；
- 每天和用户交流；
- 做设计；
- 拉数据、分析数据；
- 建 dashboard；
- 写代码并交付产品。

Boris 认为工程、PM、设计、用户研究、数据分析等角色边界会逐渐融化，形成更通用的 `builder` 角色。这个角色不一定是传统工程师，但必须能用 AI 把想法变成可运行、可验证的东西。

这也是为什么 Anthropic 使用 `member of technical staff` 这类弱化职能和等级感的 title。Boris 认为显性的 senior/principal title 会让人因为资历而不敢质疑坏主意。弱化 title 是一种文化 forcing function：让观点本身而不是头衔获得权重。

## 给公司和创始人的建议

Boris 给出的组织建议很明确：

1. 给每个人尽可能多的 token；
2. 让大家实验；
3. 项目刻意少配人；
4. 通过资源不足迫使团队自动化。

例如，一个项目传统上觉得需要 4 个工程师，可以先只放 2 个工程师，再给足 token，让他们用 AI 和自动化补齐能力。

这背后的逻辑是：

- 人少会迫使团队自动化；
- 自动化后的流程下次更便宜；
- token 成本可能提高前期投入，但降低长期重复劳动；
- 小团队 + 高 token 预算可能比大团队 + 低自动化更有复利。

可以理解为：把一部分人力预算转移到 token 和自动化系统上，用前期系统化投入换取后续边际成本下降。

## 关于 taste：人类品味也不是绝对壁垒

Boris 对「品味」的态度比较反直觉。他说自己以前有强烈代码风格偏好，比如喜欢函数式，不喜欢 class。但当模型开始大量写 class，而且业务结果更快更好、代码也不差时，他开始怀疑这类偏好只是个人执念。

他进一步认为，现在大家说「产品品味是 alpha」，但这也可能只是暂时的。因为他已经有大量 Claude 实例在看 Twitter、GitHub issue、Slack 反馈，并提出下一步应该做什么。现在可能只有 20% 点子好，但随着模型进步，几个月后多数点子可能都会变好。

他的最终判断是：最后人类要教模型的可能不是技能，而是 values。像教孩子做个好人一样，教模型成为一个好模型。

## 对我的系统/工作的启发

### 1. Hermes 不应该只做响应式助手

如果只等用户提问再执行，Hermes 会停留在「更快的打字员/搜索员」层级。更高价值的形态应该是：

- 主动发现任务；
- 拆成 Agent 可执行单元；
- 自动跑验证循环；
- 汇总失败和下一步；
- 只在关键风险或授权边界处打断用户。

这和 Hermes 当前的多主机、多 Agent、Kanban 方向一致。

### 2. 重点不是 prompt，而是 loop

单次 prompt 优化的收益会被模型升级稀释。更值得沉淀的是：

- 任务分解规则；
- 验证规则；
- stop-loss 规则；
- 子 Agent 分工；
- 证据收集格式；
- 失败重试与升级路径。

换句话说，要把「怎么工作」写成可执行循环，而不是把希望寄托在一次提示词里。

### 3. 小团队 + 多 Agent 应成为默认假设

对新项目，不应默认「多招人/多开人工协作」。更合理的默认实验是：

- 小范围定义目标；
- 给足 Agent/token；
- 让 Agent 做调研、实现、测试、review；
- 用真实验证结果决定是否扩大投入。

### 4. 角色边界会继续弱化

未来有价值的不是「我是 PM/工程/设计/数据分析」，而是能否完成完整闭环：

```text
发现问题 → 定义目标 → 设计方案 → 构建 → 验证 → 迭代 → 沉淀成系统
```

这也意味着个人知识库、技能库、项目笔记不应该只记录结论，还要记录可复用的工作流和判断标准。

## 可落地动作

1. **把重要工作流从聊天迁移到 skill / playbook**  
   只记录总结不够，应该把可复用步骤变成 Hermes skill 或 Obsidian playbook。

2. **新项目优先设计 Agent loop**  
   不先问「要写什么代码」，而先问：这个项目的目标、反馈信号、验证方式、失败条件分别是什么？哪些部分可以交给子 Agent 独立循环？

3. **对每个持续工作流建立 stop-loss**  
   Agent 很容易无限细化任务。需要提前定义：跑到什么信号就停止、升级、询问用户或放弃。

4. **把 taste 外显化**  
   如果某个判断依赖「品味」，要尽量转成 examples、checklist、反例和验收标准，而不是只写「要有品味」。

5. **定期审视哪些人工角色边界可以被合并**  
   对项目流程做复盘：哪些 PM/设计/工程/数据分析交接，其实可以由一个 builder + 多 Agent 完成？

## 应更新的规则或 skill

本次笔记本身暂不直接更新 Hermes skill。原因：这期内容是方向性启发，不是已经在本地验证过的稳定操作流程。

但它提示后续可以补强两个方向：

- `subagent-driven-development`：增加「loop-first」设计原则，即先定义反馈循环和 stop-loss，再分配子 Agent；
- `kanban-orchestrator`：强化「少人多 Agent」和「验证优先」的任务分解策略。

等这些做法在实际项目中跑通一次后，再沉淀进 skill 更稳。

## 暂不采用的部分

1. **不盲目接受「少人多 token」作为所有项目默认策略**  
   这个策略适合软件、研究、数据、内容等可快速验证的任务；但对强依赖人际协作、线下执行、法律/财务责任的任务，仍需要明确责任人和人工审核。

2. **不把 title 弱化等同于组织无层级**  
   弱化 title 可以降低权威偏见，但实际组织仍需要明确决策权、责任边界和升级路径。

3. **不把「模型会拥有产品品味」当作已经发生的事实**  
   当前更可靠的做法还是让模型提出候选，人类用明确标准筛选，并把筛选标准逐步外显。

## 一句话结论

Claude Code 的真正冲击不是让工程师少写几行代码，而是把软件开发推进到「人设计目标和循环，Agent 执行、验证、反馈」的新抽象层；组织上则会奖励能跨工程、产品、设计、数据完成闭环的 generalist/builder。
