# URL 抓取→Obsidian→PDF(含图)→Drive（wx2md + Supadata + gws）SOP

目标：给一个 URL，自动抓取正文（含图片）、写入 Obsidian 作为笔记，同时生成 **含图 PDF** 上传到 Google Drive，上传成功后本地 PDF 删除（仅作为过渡文件）。

## 路由策略（默认）

- **微信公众号（mp.weixin.qq.com）**：使用 `wx2md-worker` 拉取 Markdown（稳定、速度快）
- **海外/视频/社交（YouTube/TikTok/Instagram/X/Twitter）**：使用 **Supadata MCP** 的 `transcript`
- **其它网页**：使用 **Supadata MCP** 的 `scrape`（输出 Markdown）

> 备注：`x-reader` 本身也支持 WeChat/X/YouTube 等，但 WeChat 往往需要 Playwright 兜底，容易慢/超时；因此这里优先 wx2md-worker。

## 产物

- Obsidian 笔记：`10-Notes/WeChat/YYYY-MM-DD 标题.md`
  - 图片会下载到同名目录（相对引用），便于 PDF 内嵌
- PDF：上传到 Drive（成功后本地不保留）

## 依赖

- `gws` 已完成 OAuth：`gws auth login`
- `mcporter` 已配置 `supadata` MCP（`config/mcporter.json`）
- Workspace venv：`/root/.openclaw/workspace/.venv`
- 系统有 `google-chrome`（用于 headless 打印 PDF）

## 一键命令

```bash
cd /root/.openclaw/workspace
. .venv/bin/activate
python scripts/ingest_url.py "<URL>"
```

可选参数：
- `--drive-folder-id <FOLDER_ID>`：上传到指定 Drive 目录（或设置环境变量 `GWS_DRIVE_FOLDER_ID`）
- `--keep-pdf`：调试用，把 PDF 另存到笔记同名路径（默认不保留）

## 实现要点（脚本内部）

1) 抓取内容 → 统一产出 Markdown
2) 解析 Markdown 图片 `![](...)`：逐个下载到笔记同名目录，并改写为相对路径
3) Markdown → HTML（Python markdown 库）
4) `google-chrome --headless --print-to-pdf=... file://...` 生成 PDF（确保图片来自本地文件，因此可内嵌）
5) `gws drive files create --upload <pdf> --json '{"name":"...","mimeType":"application/pdf"}'` 上传
6) 把 Drive 链接回写到笔记末尾
7) `git add/commit/push` 同步 Obsidian vault

## 降级策略

- 图片下载失败：笔记保留原始图片 URL；PDF 仍可生成（可能缺图或加载远程图）
- Drive 上传失败：脚本会报错退出；可加 `--keep-pdf` 便于排查
