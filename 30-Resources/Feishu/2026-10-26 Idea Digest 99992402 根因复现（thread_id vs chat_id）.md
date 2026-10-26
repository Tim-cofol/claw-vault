# Idea Digest 99992402 根因复现：thread_id vs chat_id

**日期**：2026-10-26
**关联 issue**：SUP-153（已闭环）/ SUP-154（待拍板修法）
**关联 cron**：`2e8ecd9b7cb2` — Hermes Idea Recall Weekly Digest

## 问题

Idea Recall Weekly Digest 的 cron `last_status='ok'`，但 `last_delivery_error` 连续 **11 周**非空：

```
live adapter send failed: [99992402] field validation failed;
delivery error: Feishu send failed: [99992402] field validation failed
```

前 10 周日报只记成"原因不明"，今天首次定位到根因。

## 根因

cron job 的 `origin.thread_id = omt_195b15107a561c82` 被 FeishuAdapter 当成消息接收方传给
`im.v1.message.create`，而 `receive_id_type='thread_id'` **不是该 API 支持的取值**。

live-adapter 与 standalone fallback 两条路径传的是同一个 `thread_id`，所以**两条腿一起失败**，
最终表现为 `last_status='ok'` + `last_delivery_error` 非空这种假绿。

**对照组吻合**：日报 job 的 `origin.platform` 是 discord → `thread_id=None` → 一直正常；
EDN job 的 `thread_id` 也是 None → 没踩坑。**只有这个 job 同时是 feishu origin + 带 thread_id。**

## 复现

脚本：[`scripts/2026-10-26 idea-digest thread_id 投递复现探针.py`](scripts/2026-10-26%20idea-digest%20thread_id%20投递复现探针.py)

它镜像 `FeishuAdapter._send_raw_message()` 的行为，对同一个 chat 发两次探针：

| `im.v1.message.create` 调用 | 结果 |
|---|---|
| `receive_id_type='thread_id'`, `receive_id=omt_195b15107a561c82` | 失败 `99992402 field validation failed` |
| `receive_id_type='chat_id'`, `receive_id=oc_d5de...92b` | 成功 `code=0` |

## 两个待拍板修法

- **(A) 纯配置零代码**：`deliver` 改成 `feishu:oc_d5de551525d3a4ae9e1a52815bb9a92b`，
  解析出 `thread_id=None`，走已验证成功的 chat_id 路径。
  注意：只改 `deliver=feishu` 无效——`origin.platform` 也是 feishu，resolver 会优先复用
  origin 的 thread_id。必须显式写 `feishu:<chat_id>` 或清空 `origin.thread_id`。
  代价：digest 从 thread 落到 Home DM 主会话（用户可见的路由选择）。
  改 `jobs.json` 须走备份 → Python 改写 → 二次校验，不能用 sed。
- **(B) 治本**：修 `FeishuAdapter._send_raw_message` 的 `metadata['thread_id']` 分支，
  改走 `message.reply` + `reply_in_thread`，用 thread 根消息 id（`om_`）而不是把 `omt_` 当 receive_id。
  一次性修掉所有飞书 cron 的 thread 投递，但属于 Hermes core 改动，需要配测试和 review。

## 本轮的处置

本轮已用 `lark-cli im +messages-send --as bot` 直投绕过 gateway live-adapter 成功送达
（`om_x100b62de30d76508b4b740ec00424ba`，09:07，post，921 字符，回读核验正文完整落地），
证据留在 SUP-153 comment。**未擅自改配置**——它会改变消息落点，属于用户可见的路由选择。

## 对我的系统/工作的启发

- cron 的 `last_status` 只反映"agent 进程跑完没有"，**不反映"消息送出去了没有"**。
  任何投递型 cron 的健康判定必须读 `last_delivery_error`。
- 「配置 vs 代码」互相打架时，先读 `jobs.json` 的非 prompt 字段（origin / deliver），
  不要一直在 cron 输出日志里找——日志里看到的是症状，不是原因。
