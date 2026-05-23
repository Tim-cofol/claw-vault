# Hermes Agent 基础设施

## Purpose

维护 cofol1986 的 Hermes Agent 运行基础设施，让 Hermes 作为稳定的消息入口、任务调度器、工具执行器和多 Agent 协作控制面运行。

## Maintenance standard

- VPS gateway 稳定运行，作为唯一主要消息入口。
- 多平台连接状态清晰，避免重复 gateway 抢 token 或重复回复。
- Profile、toolsets、MCP、cron、gateway 配置可解释、可恢复。
- 重型开发/执行任务优先下放到 devbox 或 worker，不让 2C2G VPS 承担过重负载。
- 关键操作有可复用 playbook 或 skill。

## Current health/status

- VPS 是主 Hermes gateway。
- devbox 已被定位为重型执行机，不常驻 gateway。
- 已有 `/root/.hermes/scripts/devbox-hermes` 用于从 VPS 远程调用 devbox Hermes。

## Active projects

- 待确认：Hermes 多主机执行架构是否进入 `30-Projects/`。

## Related resources

- [[20-Playbooks]]
- Hermes runtime / gateway / profile / devbox 相关会话记录可通过 `session_search` 检索。

## Recurring checks

- gateway 是否只有一个主入口在跑。
- Discord / Slack / Feishu / Weixin / Yuanbao 连接是否健康。
- VPS 内存、swap、cron、日志是否异常。
- devbox 是否仍能通过 SSH 和 `devbox-hermes` 调用。

## Risks / watchpoints

- 多 gateway 同时运行导致平台 token 冲突或重复回复。
- VPS 2C2G 内存不足，不适合多个常驻 profile gateway。
- MCP/toolset 过重导致普通聊天延迟上升。
