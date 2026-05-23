# X-Read 微信文章导入 Google Docs（gws）SOP

目标：给一个微信公众号文章 URL，自动获取 X-Read/Markdown 清洗版内容，创建 Google Doc 写入正文，并返回文档链接。

## 输入
- WeChat 文章 URL（形如 `https://mp.weixin.qq.com/s/<SLUG>`）

## 依赖
- 已完成 `gws auth login`，本机可直接调用 `gws`（或通过 SSH -L 端口转发完成 OAuth）
- Markdown 获取：使用 `wx2md-worker`（示例公共前缀：`https://mp.084817.xyz/s/<SLUG>`；生产建议自部署）

## 流程

### 1) 取文章 slug
从 URL 中提取 `<SLUG>`：
- `https://mp.weixin.qq.com/s/B5hK8BywPla6LG3hVxHGqA` → slug = `B5hK8BywPla6LG3hVxHGqA`

### 2) 拉取 Markdown
```bash
SLUG=B5hK8BywPla6LG3hVxHGqA
MD_URL="https://mp.084817.xyz/s/${SLUG}"
curl -fsSL "$MD_URL" -o /tmp/xread_${SLUG}.md
```

### 3) Markdown → 纯文本（用于写入 Docs）
说明：Google Docs API 的 `insertText` 是纯文本写入；这里做最小清洗：
- 去 frontmatter
- 去图片 `![](...)`
- 标题 `#` 变成普通行

### 4) 创建 Google Doc
```bash
gws docs documents create --json '{"title":"X-Read 导入：<文章标题>"}'
```
拿到 `documentId`。

### 5) 批量写入正文（batchUpdate / insertText）
把文本按 ~9000 字符分块，生成：
```json
{"requests":[{"insertText":{"location":{"index":1},"text":"..."}}]}
```
然后调用：
```bash
gws docs documents batchUpdate \
  --params '{"documentId":"<DOC_ID>"}' \
  --json "$(cat /tmp/docs_batch_update.json)"
```

### 6) 返回文档链接
```text
https://docs.google.com/document/d/<DOC_ID>/edit
```

## 注意事项
- 内容很长时必须分块；否则可能触发 API 限制/请求体过大。
- 公共 wx2md 前缀可能不稳定/限流，建议自部署 worker。

## 含图版（内嵌图片）

使用 Docs API `insertInlineImage`，直接用图片 URL 作为 `uri` 插入（前提：图片 URL 能被 Google 服务器访问到）。

- 解析 Markdown：把 `![](<url>)` 识别为图片 token
- 写入顺序：`insertText`（文本）→ `insertInlineImage`（图片）→ `insertText("\n")`
- 建议给一个固定 `objectSize`（例如宽 450pt，高 300pt）；后续可按需要调
- **降级策略**：若图片插入失败（403/防盗链/超时），改为在正文里插入图片 URL（可点击）
