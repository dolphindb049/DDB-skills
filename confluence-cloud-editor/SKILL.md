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
- 对页面做最小可验证编辑（append note）
- 添加页面评论（page comment）
- 添加划词文内评论（inline comment）
- 评论查询与回滚删除

## 准备配置

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
