---
title: Mega Scale Campus Mobility Powered by Arista VESPA（视频观点整理）
source: https://www.youtube.com/watch?v=FUriyTCSmUU
created: 2026-03-16
---

# Mega Scale Campus Mobility Powered by Arista VESPA（视频观点整理）

> 说明：以下内容根据视频字幕按原有逻辑做“整理成材料/笔记”的排版（加小标题、分段）。不做总结，不改变观点顺序。
> 输出默认中文；专业术语/更精确处保留英文（如 Layer 2、EVPN、VXLAN、ARP、MAC）。

## 开场与自我介绍
（music）

大家好，感谢参加。我是 Arista 的 Ken Duda。我很高兴和你聊聊我们在园区网络（campus networking）方面的一些进展。

## 为什么“超大园区网络”很难（挑战是什么）
你可能知道 Arista 在数据中心（data center）里以超大规模运行。你也许会想：园区相对数据中心的节点数量小很多，挑战是什么？

事实是，最大的园区其实是非常具有挑战性的运行环境，原因有好几个维度：
- 你要面对的客户端数量非常巨大
- 客户端类型多样
- 安全需求更高
- 以及 **Layer 2 的规模（Layer 2 scale）**

## 漫游与单一 IP 空间（Layer 2 scale 的根因）
因为如果你想要“移动性（mobility）”，如果你希望任何客户端在大型园区里去到任何位置，你需要考虑：**如何避免更换 IP 地址？**

因为当你更换 IP 地址时，客户端会丢掉它所有的连接。

一旦你意识到你需要在整个网络里使用一个单一的 IP 空间（single IP space），你可能会担心会遇到过去我们在规模上遇到过的同类问题——你可能还记得 1980 年代：broadcast storms、network loops、forwarding topology issues。

Layer 2 的规模是有挑战的，所以我非常兴奋想和你聊聊 Vespa。

## Vespa 是什么（定位与规模目标）
Vespa 是 Arista 针对**超大规模 Layer 2** 的答案。

到底能有多大规模？我们的客户用他们最大的园区来挑战我们：我们能做到什么？

我们认为 Vespa 能在一个 Layer 2 domain 里扩展到：
- 30,000 个 access points
- 超过 500,000 个 Wi‑Fi clients

并且这一切都在：
- 一个单一 IP space
- 一个 mobility roaming domain

## Vespa 的两个关键技术（高层概览）
我们是怎么做到的？我没有时间展开所有技术细节，但从高层看，Vespa 由两项技术组成：

- 用于 **EVPN** 的 **virtual ES（virtual Ethernet segments）**
- 以及用于减少 **MAC rewrites** 的 **proxy ARP**

## virtual ES / EVPN 的工作方式（按原逻辑整理）
virtual ES 的概念是：想象一个 routed core，通过 VXLAN tunnels 连接到非常大量的 access points。

我们把一组 tunnels 绑定成一个用于 EVPN 的 virtual Ethernet segment。

然后我们在这个 Ethernet segment 上做 MAC learning，并把这些信息分发出去：
- MAC addresses
- 以及 MAC to IP bindings

通过 EVPN。

## 消除 Layer 2 的“麻烦因素”（按原逻辑整理）
有了 Vespa，我们能够消除：
- 所有 ARPs
- 所有 broadcasts
- 所有 unknown DA flooding

以及所有这些过去导致 Layer 2 可扩展性问题的“麻烦因素”。

## proxy ARP + MAC rewrite（按原逻辑整理）
Vespa 还包含一个 proxy ARP 的 MAC rewrite 功能，用来扩展我们交换机里的 rewrite tables。

这些技术组合在一起，让我们实现了业内最大的 L2 scale。我们对能做到的事情感到非常兴奋。

## 统一 EOS（运维一致性）
而且这一切都基于我们已经在数据中心以超大规模部署过的、完全相同的操作系统。

这是一套 EOS——不仅仅是一个品牌，不仅仅是一棵 source tree，我指的是：
- 一个 build
- 一个 binary image

你可以把它部署在你整个基础设施上。

如果你一直在应对竞争对手那一堆“操作系统动物园（menagerie of operating systems）”，我希望你会对“只需要一套 OS”这件事感到如释重负：
- 只需要 qualify 一套
- 学习一套
- 部署一套

并获得：
- 运行的一致性（consistency of operation）
- 自动化的一致性（consistency of automation）

覆盖你整个基础设施。

## 结尾
我希望你和我一样，对把它部署到现代园区、把规模推到下一个层级的机会感到兴奋。

非常感谢。

（music）
