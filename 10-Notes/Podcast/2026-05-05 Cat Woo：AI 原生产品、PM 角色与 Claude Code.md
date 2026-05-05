# Cat Woo：AI 原生产品、PM 角色与 Claude Code

来源：https://youtu.be/PplmzlgE0kg?si=drrWpQNI2cQ3wm0-
类型：YouTube / Podcast 笔记
日期：2026-05-05
人物：Cat Woo（Anthropic，Claude Code / Co-work 产品负责人）、Lenny

---

## 一句话总结

Cat Woo 认为，AI 原生产品时代的核心变化不是“PM 消失”，而是**代码变便宜后，判断该写什么、如何最快验证、如何让团队围绕正确目标高速 shipping，变得更值钱**。PM、工程师、设计师的边界正在融合，但产品品味、第一性原理、评估能力、低 ego 的跨职能执行力会更重要。

---

## 核心观点

### 1. AI 时代 PM 的工作重心正在变化

过去软件开发节奏较慢，PM 可以围绕 6–12 个月路线图做规划，重点是跨团队对齐、长期依赖协调、减少昂贵代码浪费。

现在模型能力和工程效率提升很快，Anthropic 内部很多产品功能的周期已经从：

- 6 个月
- 1 个月
- 1 周
- 有时甚至 1 天

因此 PM 的关键任务变成：

- 明确目标用户是谁
- 明确要解决的具体问题
- 明确哪些任务必须 out-of-the-box 成功
- 降低从想法到上线的摩擦
- 建立可以每周甚至每天发布的机制
- 帮团队快速拿到真实用户反馈

她强调，AI 原生产品里的好 PM 要能回答：

> 如何把一个想法最快放到用户手里？

---

### 2. 产品品味比“写代码能力”更稀缺

Cat Woo 反复强调 product taste：

> As code becomes much cheaper to write, the thing that becomes more valuable is deciding what to write.

当代码生成成本下降后，真正稀缺的是：

- 判断哪些需求值得做
- 判断 UX 应该如何设计
- 判断用户真正想完成的任务是什么
- 从海量反馈里识别高价值方向
- 知道当前模型能力的边界，设计能最大化模型能力的产品路径

工程背景仍然有价值，因为它帮助 PM 判断实现难度和优先级：

- 容易做的，不必长时间争论，直接试
- 难做的，需要更谨慎地判断投入产出

但她也提醒，这些技能价值会随着模型能力每几个月变化而变化，不能静态判断。

---

### 3. “正确程度的 AGI pilled”很难

她提出一个很重要的判断：

构建“超级 AGI 已经存在时的产品”很容易，因为那时可能只需要一个文本框，模型足够聪明，能自己加工具、自己问澄清问题、自己完成任务。

难的是：

> 面对当前这个还不完美的模型，如何设计产品来最大化它的能力？

这包括：

- 引导用户走 golden path
- 利用模型强项
- 补齐模型弱点
- 用产品设计降低失败概率
- 把模型不稳定处转化为可控流程

这类判断要求 PM 深度使用模型，而不是停留在概念层面。

---

### 4. PRD 没有消失，但变轻了

Anthropic 的做法不是完全取消 PRD，而是分情况使用。

他们更依赖：

- 每周 metrics readout
- 团队原则文档
- 明确的核心用户和业务目标
- 团队成员能独立做决策的上下文

但对于特别模糊、涉及复杂基础设施、周期较长的项目，仍然会写一页式 PRD，说明：

- 目标是什么
- Delightful use case 是什么
- 当前 failure mode 是什么
- 要修掉哪些核心问题

结论：

> PRD 从“重型规划文档”变成“必要时澄清目标和失败模式的轻量工具”。

---

### 5. 高速 shipping 依靠的是流程极简和预览机制

Claude Code 团队会把很多功能以 research preview 方式发布，明确告诉用户：

- 这是早期想法
- 可能会变
- 可能不会长期支持
- 目标是收集反馈

这样可以降低发布承诺，让团队更敢于把东西放出去。

同时他们建立了低摩擦发布流程：

- 工程师 dogfood 后认为功能 ready
- 发到 evergreen launch room
- docs、PMM、DevRel 快速接上
- 第二天即可完成文档、公告、发布材料

PM 在这里的价值不是审批，而是建立这种机制。

---

### 6. Claude Code / Desktop / Mobile / Co-work 的定位

Cat Woo 对 Anthropic 产品矩阵的划分：

#### Claude Code CLI

适合：

- 一次性 coding task
- 需要最新能力
- 同时跑少量 coding agent
- 专业开发者使用

CLI 是功能最先落地的产品面，也是最强大的入口。

#### Claude Code Desktop

适合：

- 前端开发
- 需要实时预览 UI
- 不喜欢终端的用户
- 统一查看 CLI、Desktop、Web、Mobile 会话

Desktop 更像控制面板 + 图形化入口。

#### Claude Code Web / Mobile

适合：

- 外出时启动任务
- 不想一直开着电脑
- 在路上/散步/移动场景里派发任务

解决的是“不能带着 laptop 到处跑”的问题。

#### Co-work

适合非代码输出：

- 清空 Slack / Gmail
- 做 slide deck
- 写 feature goal 文档
- 写 launch plan
- 汇总会议材料
- 生成客户会议 brief

她的划分很清楚：

> 输出是代码，用 Claude Code；输出不是代码，用 Co-work。

---

### 7. Co-work 的价值来自连接上下文

Cat Woo 说，如果要用好 Co-work，第一步是连接工作上下文：

- Slack
- Google Calendar
- Gmail
- Google Drive
- 团队 source of truth
- 设计模板 / Figma / deck template

她举了一个例子：

她要为 Code with Claude conference 做一份关于 Claude Code 从 assistant 到 agent 演进的 deck。她把 PMM 的建议、已有草稿、参考 deck、希望讲述的 narrative 给 Co-work。Co-work 会：

- 查 Twitter 上发布过什么
- 查 evergreen launch room
- 查 Claude Code announce channel
- 找内部成功案例和 demo
- 综合成 20 页 deck
- 使用 Anthropic 的设计系统做出接近正式设计稿的版本

她仍然需要决策最终 narrative，但大量信息搜集、结构化和视觉初稿被自动化。

这说明 PM 的角色不是消失，而是从“亲手拼材料”变成：

- 设定叙事方向
- 选择哪些内容进入最终版本
- 判断质量
- 给反馈迭代

---

### 8. 人类仍然重要的地方

Cat Woo 认为，在当前阶段，人类仍然提供模型缺失的 common sense 和组织判断。

产品发布有上千个细节，包括：

- 谁是 stakeholder
- 各方偏好是什么
- 用什么渠道沟通
- 哪些小风险会变成大问题
- 哪些事可以晚点做
- 哪些事必须今天解决

模型会越来越强，但目前在人际、组织、常识、优先级判断上还有明显差距。

她总结的人类价值包括：

- 选方向
- 判断市场
- 决定优先级
- 判断产品是否足够好
- 处理复杂 stakeholder
- 在混乱中保持冷静

---

### 9. AI 原生团队需要能承受混乱的人

Anthropic 团队节奏很快，经常出现 P0、P00、P000 的突发问题。Cat Woo 说，团队里的人需要：

- lean into chaos
- 面对挑战保持乐观
- 睡好觉，第二天做更好决策
- brutal prioritize
- 接受有些东西不够完美
- 快速发布、快速修正

她提到，过去上线一个有 bug 的功能会让她睡不着，现在只要不阻塞核心 use case，就可以接受，因为团队会很快收到反馈并修掉。

---

### 10. 角色边界正在融合

PM、工程师、设计师的边界越来越模糊：

- PM 会写代码
- 工程师会做产品决策
- 设计师会 PM，也会落前端代码
- 工程师可以从 Twitter 用户反馈一路做到周末发版

Claude Code 团队倾向于招聘有强产品品味的工程师，以减少协调开销。

她认为：

> product taste 可以来自任何背景，但它是最重要的能力。

---

### 11. 高速迭代的代价：产品一致性下降

过去代码昂贵，产品套件会被仔细规划：

- 每个 use case 一个产品
- 各产品边界清晰
- 用户路径明确

现在为了快速试验，Anthropic 有时会发布功能重叠的产品或形态，让真实用户反馈决定哪种更好。

代价是：

- 新用户不知道完成某件事的最佳路径
- 用户感觉自己必须每天看 Twitter 才不落后
- 产品教育压力变大
- 产品一致性会下降

`/powerup` 这类内置 onboarding，就是为了解决“功能太多，用户不知道哪些最重要”的问题。

---

### 12. 模型变强后，产品 harness 会被吃掉

她提到一个例子：Claude Code 早期需要显式 todo list，因为模型会做大型重构时改了 5 个 call site 就停下。todo list 帮它记住所有待办。

后来模型变强后，很多 prompt intervention 不再必要。每次新模型发布，团队都会重新读系统提示词，判断哪些提醒可以删除。

原则是：

> 新模型会让一些产品辅助机制变得多余，但也会解锁以前不可靠的新功能。

例如 code review 产品，早期模型不够可靠，直到后来的模型让团队觉得它可以在 merge 前抓住大部分 bug，才真正可用。

---

### 13. 未来 Claude Code / Co-work 的方向：从单任务到多 agent 管理

Anthropic 的视角是 building blocks：

1. 单个任务成功
2. 多个任务同时成功
3. 未来 50 个、100 个 Claude 同时运行
4. 远程运行，而不是全在本地机器
5. 人类只关注需要介入的任务
6. agent 自己验证工作是否完成
7. 当用户给出反馈后，系统能在未来任务中记住并避免重复错误

核心问题会变成：

- 如何管理大量远程 agent？
- 如何知道哪个任务需要人看？
- 如何快速验证 agent 是否真的完成？
- 如何让反馈进入自我改进循环？

---

### 14. 对普通知识工作者的建议：从重复工作开始自动化

Cat Woo 的建议很实用：

> Anytime you realize that you're doing some manual task multiple times, think about how you can use AI tools to automate that for you.

步骤是：

1. 找到自己反复做、但不喜欢做的工作
2. 用 Claude Code / Co-work / 其他 AI 工具自动化
3. 不要停在 90–95% 可用
4. 花时间把它调到接近 100% 可靠
5. 把省下来的时间投入创造性工作和更高价值项目

她特别强调：

> 如果一个自动化不能 100% 工作，它还不是真正的自动化。

最后 5–10% 很花时间，但真正的杠杆在这里。

---

### 15. 不要沉迷配置，简单 setup 往往更好

她也提醒另一种极端：有些人会花太多时间配置技能、MCP、workflow、个性化工具，但反而不去完成原本要做的产品和任务。

观点：

- hackability 很重要
- 自定义工具很有价值
- 但过度配置会偏离核心目标
- 简单 setup 通常更有效

这对 AI 工具重度用户很有警示意义。

---

## 对 PM / 产品团队的启发

### PM 不会消失，但评价标准会变

未来更重要的不是：

- 会不会写漂亮 PRD
- 会不会做季度 roadmap
- 会不会开很多对齐会

而是：

- 有没有产品品味
- 能不能定义一个月后的产品形态
- 能不能理解当前模型能力边界
- 能不能把 idea 快速送到用户手里
- 能不能设计 eval / feedback loop
- 能不能跨职能推动 shipping
- 能不能在混乱中保持低 ego 和高 agency

### AI 产品的核心是“贴着模型能力边界做设计”

不要只想象 AGI 终局，也不要按传统 SaaS 思路照搬。更重要的是判断：

- 当前模型哪里强？
- 当前模型哪里弱？
- 用户怎么提示它会成功率最高？
- 产品能在哪些地方补齐模型短板？
- 下一代模型出来后，哪些 crutch 可以删掉？

### 团队机制比单个模型能力更重要

Anthropic 的 shipping 速度不完全来自最强模型，也来自：

- 低流程
- research preview
- 明确目标
- 高授权
- 快速 docs / PMM / DevRel 联动
- 团队成员默认可以“just do things”

---

## 可执行清单

### 给 PM

- 每周亲自高强度使用最新模型和工具
- 建立 5 个你信任的高质量模型反馈用户
- 为关键能力写 5–10 个高质量 eval
- 把 PRD 压缩成目标、用例、失败模式、验收标准
- 推动团队建立低摩擦发布流程
- 学会判断模型能力变化对产品设计的影响

### 给工程师

- 培养产品品味，不只是实现需求
- 直接从用户反馈出发做小实验
- 用 AI 自动化重复开发、测试、发布工作
- 做完后验证，不要只信 agent 的完成声明
- 学会给 agent 明确 spec 和反馈

### 给知识工作者

- 找一个每周重复出现的烦人任务
- 用 AI 做第一个自动化版本
- 记录每次失败原因
- 把规则、偏好、边界逐步写进 workflow
- 直到接近 100% 可依赖，再推广到其他任务

---

## 值得摘录的句子

> As code becomes much cheaper to write, the thing that becomes more valuable is deciding what to write.

> The hard thing is figuring out for the current model, how do you elicit the maximum capability?

> Just do things.

> If an automation doesn't work 100% of the time, it's not really an automation.

> The simple setups actually work better.

---

## 我的理解

这期访谈最有价值的地方，是把“AI 让 PM 失业吗”这个问题转换成了另一个更准确的问题：

> 当代码和产出变便宜后，什么判断会变贵？

答案是：方向、品味、边界判断、组织协调、验证闭环。

AI 原生产品的 PM 不是写更多文档的人，而是能在模型能力快速变化中，持续回答三个问题的人：

1. 现在的模型真正能稳定做什么？
2. 用户应该被引导到哪条路径上才能成功？
3. 团队如何用最短路径把假设放到真实世界验证？

这也是对所有 AI 工具使用者的提醒：不要只追逐 setup、prompt 和 MCP，而要把 AI 真正接入每天的高频任务，并把自动化从“看起来能跑”打磨到“可靠到可以放心交给它”。
