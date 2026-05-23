# 2026-03-05 飞书 OAuth user_access_token 配通复盘

## 背景
之前创建飞书日程用 tenant_access_token（应用身份），组织者是机器人。目标：获取 user_access_token 以用户身份调飞书 API。

## 踩坑 & 解决

### 坑1：授权链接格式 → 20043 openid有误
- ❌ `accounts.feishu.cn` + `app_id` → 报 20043
- ❌ `accounts.feishu.cn` + `client_id` + `response_type=code` → 仍报 20043
- ✅ **旧版端点** `open.feishu.cn/open-apis/authen/v1/authorize` + `app_id`，不需要 scope/response_type
- **教训**：飞书新版 OIDC（accounts.feishu.cn）和旧版授权是两套，自建应用走旧版更稳

### 坑2：回调服务不可达 → 502
- 回调服务端口被占 / 绑了 127.0.0.1 / 腾讯云安全组未放行
- ✅ **最终方案**：redirect_uri 设为 `http://127.0.0.1/callback`，不需要真的可达。授权后从浏览器地址栏复制 code 即可

### 坑3：回调脚本端口冲突
- 18800 被 Chrome 占了，改 18801 后安全组仍未放行
- 教训：不依赖回调服务是最简方案

## 最终成功流程

1. 飞书后台安全设置添加重定向 URL：`http://127.0.0.1/callback`
2. 权限管理开启日历等所需权限
3. 访问授权链接（旧版端点 + app_id）
4. 登录授权后从地址栏复制 code
5. `python3 scripts/feishu_oauth_token.py exchange --code '<code>' --redirect-uri 'http://127.0.0.1/callback'`
6. Token 保存到 `config/feishu_oauth.json`

## Token 维护
- user_access_token 有效期 2h，refresh_token 30天
- Cron 每 1.5h 自动刷新
- 如果 refresh_token 过期，需用户重新走授权流程

## 验证结果
- 用户身份创建日程成功，组织者显示"张起强"
- scope 覆盖：日历/文档/云盘/表格/多维表格/知识库/邮箱/消息/搜索

## 关键文件
- `config/feishu_oauth.json` — token 存储
- `scripts/feishu_oauth_token.py` — OAuth 工具 CLI
- `scripts/feishu_oauth_refresh.sh` — 刷新快捷脚本
