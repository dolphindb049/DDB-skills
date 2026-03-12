---
name: confluence-cloud-editor
description: 使用 Confluence Cloud REST API 进行页面读取、子页面树遍历与小范围编辑验证。适用于需要在 Atlassian Confluence 私有空间里做认证测试、页面抓取、版本递增更新、追加测试标记文本等自动化操作的场景。
---

# Confluence Cloud Editor

用于在本机通过 Confluence Cloud API（`/wiki/rest/api`）执行：
- 认证连通性检查
- 单页读取（含 body.storage 与 version）
- 子页面树遍历
- 页面批量导出为 Markdown（Confluence storage HTML -> GFM）
- 从 Markdown 一键发布到 Confluence（自动超链接、本地图片附件上传并嵌入）
- 对页面做最小可验证编辑（append note）
- 添加页面评论（page comment）
- 添加划词文内评论（inline comment）
- 评论查询与回滚删除

## 准备配置

### 新服务器环境准备（推荐）

建议 Python 相关统一用 `uv` 管理，避免在新机器上因解释器/依赖差异导致卡点。

1. 安装基础命令行依赖
- `curl`（脚本当前通过 `curl` 发 REST 请求）
- `pandoc`（仅 `export-pages-md` 命令需要）

2. 安装 `uv` 并创建虚拟环境
```bash
uv venv .venv
```

3. 激活环境
```bash
# PowerShell
.venv\Scripts\Activate.ps1
```

4. 安装 Python 依赖（如需）
```bash
uv pip install requests
```

注：当前 `confluence_api.py` 主要使用标准库 + `curl`，通常不需要额外 Python 包；如果后续扩展脚本再按需增加。

5. Windows 推荐设置 UTF-8（避免 GBK 解码问题）
```powershell
$env:PYTHONUTF8='1'
```

1. 复制模板并填入凭据：
```bash
cp .github/skills/confluence-cloud-editor/.env.example .github/skills/confluence-cloud-editor/.env
```

2. 编辑 `.env`：
- `CONFLUENCE_BASE_URL`：例如 `https://dolphindb1.atlassian.net/wiki`
- `CONFLUENCE_EMAIL`：Atlassian 登录邮箱
- `CONFLUENCE_API_TOKEN`：Atlassian API Token

## 命令速查

在仓库根目录运行：

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py auth-test
```

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py get-page --page-id 2257649834
```

从 Markdown 创建新页面（推荐用于产品单页发布）：

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py publish-md-page \
  --md-file .github/skills/confluence-cloud-editor/产品单页-Shark异构平台-草稿.md \
  --title "【Shark】产品单页" \
  --space-key mfYhIEPn2ojV \
  --parent-id 2534670386
```

从 Markdown 更新已有页面（保留原页面 ID）：

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py publish-md-page \
  --md-file .github/skills/confluence-cloud-editor/产品单页-Shark异构平台-草稿.md \
  --page-id 2547974305
```

发布前预览（不写入 Confluence）：

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py publish-md-page \
  --md-file .github/skills/confluence-cloud-editor/产品单页-Shark异构平台-草稿.md \
  --page-id 2547974305 \
  --dry-run
```

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py list-children --page-id 2257649834 --recursive
```

导出根页下“前 4 个子页面”为 md（不包含根页）：

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py export-pages-md \
  --page-id 2257649834 \
  --out-dir projects/swordfish \
  --max-pages 4
```

按标题前缀筛选后再导出（例如“下面四章”）：

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py export-pages-md \
  --page-id 2257649834 \
  --out-dir projects/swordfish \
  --title-prefix "大纲-第" \
  --max-pages 4
```

先 dry-run 查看将导出的页面清单：

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py export-pages-md \
  --page-id 2257649834 \
  --out-dir projects/swordfish \
  --title-prefix "大纲-第" \
  --max-pages 4 \
  --dry-run
```

对页面追加一行测试标记（自动读取版本并 `+1`）：

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py append-note \
  --page-id 2257649834 \
  --note "[Codex smoke edit]"
```

对根页面及所有子页面追加同一条测试标记（先建议 dry-run）：

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py append-note-tree \
  --page-id 2257649834 \
  --note "[Codex tree smoke edit]" \
  --dry-run
```

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py append-note-tree \
  --page-id 2257649834 \
  --note "[Codex tree smoke edit]"
```

对指定页面添加评论（先 dry-run）：

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py add-comment \
  --page-id 2257649834 \
  --text "[Codex comment smoke test]" \
  --dry-run
```

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py add-comment \
  --page-id 2257649834 \
  --text "[Codex comment smoke test]"
```

对根页面及所有子页面批量添加评论：

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py add-comment-tree \
  --page-id 2257649834 \
  --text "[Codex tree comment smoke test]" \
  --dry-run
```

添加“划中一段话”的文内评论（API 自动计算 `textSelectionMatchCount`）：

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py add-inline-comment \
  --page-id 2257649834 \
  --selection "Swordfish" \
  --text "[Codex inline comment smoke test]" \
  --match-index 0 \
  --dry-run
```

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py add-inline-comment \
  --page-id 2257649834 \
  --selection "Swordfish" \
  --text "[Codex inline comment smoke test]" \
  --match-index 0
```

列出评论（可用关键字过滤）：

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py list-comments \
  --page-id 2257649834 \
  --contains "Codex"
```

回滚删除指定评论：

```bash
python3 .github/skills/confluence-cloud-editor/scripts/confluence_api.py delete-comment \
  --comment-id 2539978863
```

## 已完成的实测摘要（2026-03-05）

- 认证：可用（API token 有效）
- 页面读取：`2257649834` 可读取
- 子页面递归：共识别 5 个子页面
- 批量最小编辑：根页 + 5 子页均成功追加测试标记
- 评论写入：已成功在 `2257649834` 创建 1 条测试评论
- 文内评论：已成功通过 `POST /api/v2/inline-comments` 创建并验证
- 评论回滚：测试评论已成功删除

## 在线技能复用建议

- OpenAI curated skills 里目前没有专门的 Confluence skill（已检查列表）。
- 该场景建议直接复用本技能脚本；若后续发现第三方稳定仓库，可用 `skill-installer` 按 GitHub 路径安装并并行保留本技能。

## 安全约束

- 不把 token 写入命令行参数，统一从 `.env` 读取。
- 更新页面前总是先拉取当前 `version.number`，写回时自动加 1，避免版本冲突。
- 导出 md 属于只读操作，不会修改 Confluence 页面内容。
- 建议先在测试页面运行 `append-note`，确认权限与审计流程后再批量操作。
- 建议评论测试使用明确标记文本（例如日期），便于后续检索和清理。
- 文内评论要求 `--selection` 与页面正文完全匹配；同一文本出现多次时用 `--match-index` 指定目标位置。

## 常见卡点与排障（2026-03-10 增补）

1. 网页抓取已登录但仍跳 Atlassian 登录页
- 现象: `fetch_webpage` 返回登录跳转，无法拿到正文。
- 原因: 该工具不共享浏览器登录态 cookie。
- 建议: 直接使用本技能脚本走 REST API（`auth-test`、`get-page`、`list-children`、`search`）。

2. Windows 下 `get-page` 报 GBK/UnicodeDecodeError
- 现象: `subprocess.run(..., text=True)` 读取 `curl` 输出时出现 `gbk` 解码报错。
- 临时解法: 命令前设置 UTF-8 模式。
```powershell
$env:PYTHONUTF8='1'; python .github/skills/confluence-cloud-editor/scripts/confluence_api.py get-page --page-id <id>
```
- 建议: 后续可将脚本中的 `subprocess.run` 增加 `encoding='utf-8', errors='replace'`。

3. `export-pages-md` 失败，提示找不到 `pandoc`
- 现象: `FileNotFoundError: [WinError 2]`。
- 原因: 本机未安装 `pandoc`。
- 快速检查:
```bash
pandoc --version
```
- 方案 A: 安装 `pandoc` 后继续使用 `export-pages-md`。
- 方案 B: 用 REST API 拉 `body.storage`，用轻量 HTML->Markdown 转换先产出草稿。

5. Confluence 中 URL 没有自动变成可点击链接
- 现象: 页面上显示纯文本 URL，点击无效。
- 方案: 使用 `publish-md-page` 命令发布 Markdown。该命令会把 `https://...` 和 `[text](url)` 统一转换为 `<a href>`。

6. 页面图片不显示（本地 Markdown 图片路径）
- 现象: `![...](image.png)` 在 Confluence 中不渲染。
- 方案: 使用 `publish-md-page`。该命令会自动上传本地图片为页面附件，并转为 Confluence 图片宏。
- 说明: 若页面中已存在同名附件，命令会自动跳过该附件上传（`reason=duplicate_filename`），不会中断发布流程。

4. 外部 docs 站点抓取失败（握手被重置）
- 现象: 访问 `docs.dolphindb.cn` 出现 `WinError 10054`。
- 方案: 优先使用仓库内镜像文档（如 `rag/DocForRag/documentation/...`）作为官方口径替代来源。

## Confluence 检索建议

1. 模板页+子页结构化获取（用于产品单页）
- 先 `get-page --page-id <模板页ID>` 获取模板。
- 再 `list-children --page-id <模板页ID>` 获取同类单页样式样本。

2. 用 CQL 做跨空间搜索（用于补证据）
- 示例: `type=page AND title ~ "Shark" order by lastmodified desc`
- 示例: `type=page AND text ~ "GPLearn" order by lastmodified desc`
- 示例: `space="mfYhIEPn2ojV" AND type=page AND text ~ "@gpu"`

3. 写入前建议
- 先本地生成 `md` 草稿并给业务方审阅。
- 审阅通过后再新建 Confluence 子页面，避免反复改线上版本号。
