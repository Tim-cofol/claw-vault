---
title: follow-builders YouTube 频道页解析实测（2026-10-27 三方对账）
date: 2026-10-27
type: 技术诊断
source: AI Builders 早报 autopilot SUP-155 + 日报 cron 独立复核
tags: [follow-builders, youtube, 解析, 实证对账]
---

# follow-builders YouTube 频道页解析实测（2026-10-27 三方对账）

## 背景

2026-10-27 早报 autopilot（SUP-155）发现中央 feed 里的播客 `url` 字段是**频道页**（`youtube.com/@NoPriorsPodcast`）而不是具体视频页，需要手工反查。

期间 autopilot 先后给出两个互相矛盾的结论，日报 cron 做了独立复核，三方对账后如下。

## 三方结论对账

| 来源 | 结论 | 复核判定 |
|---|---|---|
| autopilot 首次评论 | `parseYouTubePageData()` 解析不到内容，YouTube 改用 `lockupViewModel`，Atom feed 也 404 | **部分错误**（见下） |
| autopilot 二次评论（自纠） | 上面那条是误报，根因是自己抠 UA 常量的正则被分号截断，skill 代码没问题 | **部分正确，但也不完整** |
| 日报 cron 独立复核 | skill 的**纯页面解析路径**确实解析不到（见下） | ✅ 与 skill 源码一致 |

## 实测数据（2026-10-27，全部用 skill 源码里未经改动的原始 UA）

### 1. Atom feed 路径 —— 正常，15 条

```
GET https://www.youtube.com/feeds/videos.xml?channel_id=UCSI7h9hydQ40K5MJHnCrQvw
→ http 200, 15 个 <entry>, 含目标视频 AwuTTOJGEi0
```

**关键**：非法 UA（截断的 `"Mozilla/5.0 (Macintosh"`）**不影响 Atom feed**——用坏 UA 请求同一个 feed 仍然返回 200 / 15 entries / 命中目标视频。所以 autopilot 说的"Atom feed 404"是错的。

`getYouTubeFeedUrl()` 的 `/@handle` 分支实测能正常从频道页 HTML 反查出 `channelId`（meta / JSON 两种模式都能命中）。

### 2. 页面解析路径 —— 确实解析不到（skill 源码级确认）

抓 `https://www.youtube.com/@NoPriorsPodcast/videos`，用 skill **原封不动**的 `parseYouTubePageData()`（只含 `videoRenderer` + `playlistVideoRenderer` 两个分支）：

```
gridItems 31
renderer kinds: [ 'lockupViewModel', undefined ]
videoRenderer count: 0
lockupViewModel count: 30
→ skill 纯解析器返回 0 条
```

用 UA 做 A/B 对照（同一个纯解析器，同一份 URL）：

| UA | html 长度 | 纯 skill 解析器结果 |
|---|---|---|
| skill 原始 UA (Chrome/131) | 1337106 | **0 条** |
| 完整 UA (Chrome/120) | 1334243 | **0 条** |
| 截断坏 UA | 1311673 | **0 条** |

**结论：截断 UA 不是根因**。无论用哪种 UA，频道页的 30 个 grid item 全是 `lockupViewModel`，skill 的纯解析器一律返回 0 条。autopilot 二次评论的"skill 不需要改"结论**不成立**。

### 3. 为什么 autopilot 仍然跑通了

`fetchYouTubeVideos()` 的执行顺序是 **feed 优先，页面抓取兜底**：

```js
const feedUrl = await getYouTubeFeedUrl(channelUrl);
if (feedUrl) {
  const res = await fetch(feedUrl, ...);
  if (res.ok) {
    const videos = parseYouTubeFeed(await res.text());
    if (videos.length > 0) return videos;   // ← 命中这里就返回了
  }
}
// 下面才是页面抓取 parseYouTubePageData() —— 实际从未被执行到
```

Atom feed 成功返回 15 条 → 直接 return，**页面解析路径根本没被走到**。所以 autopilot 跑 `/tmp/resolve-yt-skill.mjs` 看到 `videosFound: 15` 就以为页面解析也正常——那 15 条全是 Atom feed 来的，不是页面解析来的。

## 最终结论

1. **skill 的页面解析路径确实已失效**：YouTube 把频道上传列表从 `videoRenderer` 改成了 `lockupViewModel`（标题在 `metadata.lockupMetadataViewModel.title.content`，视频 ID 在 `contentId`）。skill 的 `parseYouTubePageData()` 没有这个分支 → 静默返回 0 条。
2. **但当前不影响交付**：因为 Atom feed 路径优先且健康，`findYouTubeEpisodeUrl()` 走的是 feed，15 条里能正确命中目标视频 `AwuTTOJGEi0`。
3. **Atom feed 不会 404**，非法 UA 也不影响 Atom feed。autopilot 关于 feed 404 的说法是错的。
4. **真正的遗留问题在别处**：中央 feed 生成的 `feed-podcasts.json` 里 `url` 字段存的是**频道页**，`findYouTubeEpisodeUrl()` 的解析结果**没有写回 feed 的 url 字段**。所以每期早报仍需人工反查播客链接。这需要给上游 `https://github.com/zarazhangrui/follow-builders` 提 issue，本工作区改不了中心化 feed。

## 建议补丁（给 skill 源码 / 上游 issue 用）

在 `parseYouTubePageData()` 的 gridItems 循环里，`videoRenderer` 分支之后加：

```js
const lv = it?.richItemRenderer?.content?.lockupViewModel;
if (lv?.contentId) {
  const title = lv?.metadata?.lockupMetadataViewModel?.title?.content || "";
  if (title) {
    videos.push({
      title,
      url: `https://www.youtube.com/watch?v=${lv.contentId}`,
    });
  }
}
```

实测：加上后同一份 HTML 从 0 条变 30 条，且能命中目标视频 `https://www.youtube.com/watch?v=AwuTTOJGEi0`。

> 补丁优先级：中低。当前 Atom feed 路径可用，页面解析只是兜底路径。**真正的价值是消除"页面解析已死但没人知道"的隐患**——一旦某档节目的频道 feed 取不到，兜底路径会静默返回 0 条。

## 归档说明

2026-10-27 日报 cron 归档。诊断脚本与回归测试已归档到 `30-Resources/Feishu/scripts/`。原始 `/tmp` 下的中间产物（yt.html / yt_initial.json 等）已在归档后清理。
