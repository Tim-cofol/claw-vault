# 拆解 Anthropic：最好的 AI 公司，可能也是一种组织发明

来源：海外独角兽  
原文：https://mp.weixin.qq.com/s/sA20Zc74FYWxKOu9Nu-T1Q  
主题：OpenAI 与 Anthropic 的战略、组织文化、创始人特质与产品路径比较

## 一句话结论

Anthropic 的崛起不只是模型能力或产品判断的胜利，更像是一种组织发明：它用更少的战略下注、更低的个人 ego、更强的使命共识和更高的信息透明度，在 AI 竞争中形成了与 OpenAI 完全不同的公司形态。

---

## 1. 核心判断

文章的核心观点是：

> 在 AI 时代，赢不一定靠更大的野心、更多的探索和更强的明星人才。  
> 有时候，赢来自相反的东西：更少的 bet、更低的 ego，以及一个天真的使命。

Anthropic 被作者视为一个值得研究的样本，因为它在资源不如 OpenAI 的情况下，靠战略聚焦、组织文化和执行一致性，在 coding 与 ToB 企业市场上形成了强势增长。

---

## 2. OpenAI vs Anthropic：核心差异

| 维度 | OpenAI | Anthropic |
|---|---|---|
| 创始人特点 | Sam Altman：创业者、投资人背景，野心强，擅长资源整合、说服和多线下注 | Dario Amodei：科学家背景，技术判断强，使命驱动，价值观清晰，较固执 |
| 组织方式 | 更 bottom-up，团队各自探索，创始人负责提供资源 | 模型方向 top-down，产品方向 bottom-up |
| 战略重心 | 业务线繁杂，多点开花，重研究突破与 ToC 产品 | All in coding + ToB enterprise，先做商业价值，再反哺研究 |
| 做事风格 | 明星文化强，依靠个人突破，结果驱动 | 战略聚焦，凝聚力强，更集体主义和使命驱动 |
| 招聘文化 | 文化被稀释，无专门文化面试，平均任期较短 | 极严 culture-fit，偏好 underdog，重使命、低 ego、复杂性处理能力 |
| 模型能力 | ML 能力仍然强，但数据 curation 相对粗 | Pre-train 和数据扎实，RL 相对偏弱 |
| 产品能力 | 重 0 到 1 创新，如 Sora、浏览器、Voice Mode，但产品线延续性弱 | PM 文化强，taste 统一，持续小步迭代，产品线稳定性高 |

---

## 3. Anthropic 为什么能选中 coding？

文章认为，Anthropic 选中 coding 是“一半远见，一半运气”。

### 3.1 Coding 是 AI 最重要的方向之一

原因有三点：

1. **Coding 是通往一切的道路**：数字世界的大部分任务都可以被代码表达。
2. **Coding 最适合模型学习**：结果可验证，反馈周期短，用户数据能更好地反哺模型训练。
3. **Coding 是 AGI 研发加速器**：更强的 coding model 可以加速 AI lab 自身研发，形成递归飞轮。

### 3.2 Anthropic 早期资源有限，被迫聚焦

Anthropic 早期融资不顺，不能像 OpenAI 一样多线扩张，所以必须找到一个能形成商业闭环的垂直方向。

它很早就意识到 coding 可能形成飞轮：

```text
更强 coding model
→ 客户真实工程环境使用
→ 获得高质量任务与反馈数据
→ 反哺模型训练
→ 更强 coding model
```

据文章称，Anthropic 内部早在 2021 年就有文件论证为什么应该 focus 在 coding 上。

### 3.3 ChatGPT 爆火后，Anthropic 被迫转向 ToB

ChatGPT 抢占 C 端入口后，Anthropic 转向 ToB 和企业场景。事后看，这个选择非常幸运，因为 coding 和 enterprise 正好成为它后来爆发的主战场。

---

## 4. Focus：Anthropic 的战略优势

文章反复强调，Anthropic 的关键战略能力是 focus。

### 4.1 OpenAI：多点开花

OpenAI 同时推进 math、science、coding、reasoning、多模态、Sora、浏览器、机器人、企业平台、智能硬件、芯片、数据中心等方向。据文章说，OpenAI 内部项目一度高达约 300 个。

### 4.2 Anthropic：少数关键下注

Anthropic 早期基本放弃多模态，不强调架构创新，也不追逐太多新范式，而是：

- 坚持语言模型 scaling
- 强化 pretraining 和数据
- 重点打穿 coding
- 面向 ToB 企业价值闭环

### 4.3 Focus 的两个组成

文章对 focus 的定义很重要：

1. **判断力**：知道什么最关键，并敢于牺牲其它一切。
2. **压强**：投入压倒性资源，把关键变量打穿。

很多公司以为自己专注，但其实只是“少做了一点事”。真正的 focus 是知道哪些东西必须放弃，并承受放弃带来的代价。

---

## 5. 创始人性格如何塑造战略路径

### 5.1 Sam Altman：多线下注型 founder

文章对 Sam 的描述是：野心极强、YC / 投资人背景、熟悉多点播种和并行下注、擅长资源整合、偏好 0 到 1 的 fancy idea。

这塑造了 OpenAI 的风格：

```text
多项目并行
→ 大量探索
→ 强 0 到 1 创新
→ 但产品连续性与运营打磨不足
```

### 5.2 Dario Amodei：技术判断 + 使命驱动

Dario 的特点是：科学家背景、GPT-3 核心 research lead、scaling laws 信徒、技术判断更强、不容易被市场共识影响、价值观明确甚至固执。

这塑造了 Anthropic 的风格：

```text
少数坚定判断
→ 高度聚焦
→ 技术路线有定力
→ 组织文化围绕 mission 构建
```

---

## 6. Anthropic 的文化为什么重要？

文章认为，Anthropic 最大的 secret sauce 可能不是战略，而是文化。

### 6.1 Mission-oriented：强使命驱动

Anthropic 的使命是：

> 确保世界能够安全地度过 transformative AI 的转变。

这不是口号，而是组织决策的真实约束。文章提到：员工普遍把 safety 视为加入公司的核心原因；早期员工甚至认为，如果 Anthropic 实现了使命但公司失败了，也可以接受；公司在治理结构、安全研究、可解释性研究、订单取舍上都体现了使命优先。

这使 Anthropic 更像一个“教派型组织”：不是松散的雇佣关系，而是一群人围绕同一个终极目标形成强绑定。

### 6.2 High trust, low ego：高信任、低 ego

frontier AI lab 很容易长出明星文化和山头主义，因为顶尖 researcher 天然追求个人突破和独立路线。但 Anthropic 的特殊之处在于：内部政治少、山头感弱、愿意为他人做嫁衣、高级人才愿意做脏活细活、不过度强调 title 和个人英雄主义。

这点在 coding 和 agentic AI 上尤其关键，因为这些方向的真正壁垒不只是算法突破，而是大量系统工程、数据清洗、任务轨迹、环境搭建、evaluation 和 verification。

> OpenAI 更擅长让天才做突破。  
> Anthropic 更擅长让聪明人踏实做脏活。

### 6.3 人文底色：bookish misfits

Anthropic 的员工气质被描述为书卷气、nerd、理想主义、科幻感、有历史责任感和人文关怀。Claude 模型命名也体现了这种气质：Haiku、Sonnet、Opus。

这和 OpenAI 的 GPT-4 / 4o / o1、Google 的 Gemini Ultra / Pro / Flash 很不一样。文章认为，这种文化审美不是装饰，而是公司使命感的一部分。

---

## 7. Anthropic 如何制度化文化？

文章认为，Anthropic 的文化不是自然形成的，而是被非常刻意地设计和维护。

### 7.1 极严招聘文化

Anthropic 招聘重视：

1. 是否真的认同 safety mission
2. 是否 nice、低 ego、能承认错误
3. 是否能处理复杂性和 second-order effects
4. 是否有 direct evidence of ability，而不是只有名校、大厂、头衔
5. 是否愿意为了 mission 接受个人利益的不确定性

它有专门的 culture interview，一小时问 15-20 个 scenario questions。

一个典型问题是：

> 如果 Anthropic 因为无法保证安全，最终决定不发布模型，你愿意接受自己的股票归零吗？

Anthropic 的招聘逻辑不是“尽可能多招最强的人”，而是“尽可能早筛掉不适合的人”。

### 7.2 Context sharing：极高信息透明度

Dario 会高频进行全员沟通：两周一次 Dario Vision Quest，分享公司方向、产品策略、行业变化，现场回答问题，并在 Slack channel 里写自己的思考、担忧和判断。

员工也有 notebook channel，像内部个人 Twitter feed：记录自己在想什么、项目进展、公开讨论观点，也允许挑战领导层判断。

这种透明度让员工理解决策逻辑，从而做出一致的分布式决策。

### 7.3 七位创始人同股同权

Anthropic 有 7 位创始人，Dario 坚持同股同权。文章认为它本质上是一种文化机制：公司不是围绕某个 founder，而是围绕 mission；七个 founder 是七个文化复制节点，能在不同业务线上扩散同一套价值观。

### 7.4 One team：避免山头

Anthropic 强调 one team，弱化身份边界：高管以下统一叫 MTS，member of technical staff；弱化 researcher / engineer / product 的等级差异；鼓励每个人承担一部分 founder 视角。

这和 OpenAI 的 researcher-driven 文化形成对比。文章认为，OpenAI 内部存在更明显的鄙视链：

```text
Researcher > Research Engineer > Software Engineer
```

这会导致产品与研究之间咬合不够紧密。

---

## 8. Anthropic 文化的两个来源

### 8.1 业务性质决定文化

文章提出一个重要组织判断：

> 组织文化不是价值观装饰，而是员工行为模式是否能帮助公司成功。

对 Anthropic 来说，coding 和 agentic AI 的竞争本质要求：细致的数据工程、长期系统打磨、高质量 eval、强协作、愿意做脏活、不追逐个人高光。

所以 low ego、high trust、mission-driven 的文化，正好匹配它的业务要求。

### 8.2 创始团队对百度和 OpenAI 旧经历的反作用

Dario 曾经历过百度 AI 团队和 OpenAI 内部的政治斗争。文章认为 Anthropic 的文化，很大程度上是这些经历的反向塑造：

| 过去经历 | Anthropic 的反向设计 |
|---|---|
| 见过控制权和资源争斗 | 强调 low ego |
| 见过明星 researcher 山头 | 弱化 title 和个人英雄主义 |
| 见过价值观冲突 | 强化 mission 和文化筛选 |
| 见过高层信任破裂 | 强调透明、真诚、context sharing |
| 见过组织内耗 | 强调 one team |

所以 Anthropic 不是偶然变成这样，而是在主动避免重演 Dario 曾经厌恶的组织模式。

---

## 9. 为什么这不等于 OpenAI 会输？

文章没有简单得出“Anthropic 一定优于 OpenAI”的结论。它也指出 OpenAI 仍有强优势：

1. **Coding 已经是明牌，OpenAI 可能追上来**：市场上已经出现开发者从 Claude Code 向 Codex 迁移的趋势。
2. **算力可能成为新胜负手**：OpenAI 锁定的算力资源远超 Anthropic。
3. **OpenAI 的开放探索文化仍有巨大价值**：它更激进、更敢押注新范式，下一次范式跃迁可能重新翻盘。

所以更准确的判断不是“Anthropic 模式必胜”，而是：

> Anthropic 证明了在 AI 时代，另一种完全不同于 OpenAI 的组织路径也可以成立。

---

## 10. 对创业和组织建设的启发

### 10.1 战略不是选择什么，而是放弃什么

真正的战略核心是“略”：

```text
知道什么最重要
→ 敢于砍掉其它诱惑
→ 把资源压到关键变量上
→ 用压强打穿
```

### 10.2 公司文化必须服务业务本质

不同业务需要不同文化：

- 短周期创新业务：鼓励试错、速度、敢为人先
- 高可靠工程业务：强调纪律、流程、长期打磨
- AI agent / coding 业务：需要聪明人愿意做脏活、细活、协作活

文化不是口号，而是业务成功所需的行为模式。

### 10.3 低 ego 是 AI 组织的重要能力

AI 早期靠范式突破，但进入 agentic / coding / enterprise 后，越来越需要数据质量、工程细节、eval 系统、用户反馈闭环和长期产品迭代。这些都不适合纯个人英雄主义。

### 10.4 Mission 可以成为组织护城河

如果 mission 真实存在，它能带来：更强招聘筛选、更低人才流失、更强组织凝聚、更高协作效率、更少内部政治。

但前提是 mission 必须真实约束决策，而不是墙上的标语。

---

## 11. 最值得摘录的金句

> Focus 的重要性被低估了。

> 战略的核心不是想清楚你要选择什么，而是想清楚你要放弃什么。

> Focus 本质上包括两个层面：判断力和压强。前者是认知问题，后者是意志问题。

> 在 AI 时代，赢不一定靠更大的野心、更多的探索和更强的人才。有时候，赢也可以来自相反的东西：更少的 bet，更低的 ego，以及一个天真的使命。

> 或许下一代伟大的 AI 公司，首先就是一种新的组织发明。

---

## 12. 我的判断

这篇文章最有价值的部分，不是“Anthropic 比 OpenAI 好”这个结论，而是它把 AI 公司竞争从模型参数、benchmark、产品功能，拉回到了一个更底层的问题：

> 什么样的组织，最适合持续推进 AGI / agentic AI 这种高复杂度、高不确定性、高协作密度的任务？

Anthropic 的样本说明，AI 竞争后半场可能不只是模型竞争，而是组织系统竞争：

```text
战略聚焦
+ 数据工程
+ 产品反馈闭环
+ 文化一致性
+ 人才留存
+ 低 ego 协作
= AI lab 的长期复利
```

这对任何想做 AI 产品、AI agent、AI infra 或 AI-native 公司的团队都很有参考价值。
