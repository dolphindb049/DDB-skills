---
name: ficc_download_data
description: 提供从通联等API获取FICC定价所需基础数据，并将其导入到DolphinDB指定表中的完整流程。
license: MIT
metadata:
  author: ddb-user
  version: "2.1.0"
  dependency: tonglian_api
---

## 顶层入口（给 Agent）

本 Skill 是 FICC API 数据落库的顶层编排入口。默认目标是：

- 按 API PDF 输出字段严格建表；
- 完整写入字段注释，并维护表注释元数据；
- 拉取到期债券相关基础信息、现金流、代码对照、类型、估值、日行情并入库。

## 路由提示（给 Agent）

- 优先使用本 Skill 的关键词：拉数据、通联 API、入库、建表、`DATAYES_TOKEN`、`getBond`、`getBondCfNew`。
- 出现以下词时应转到其他 Skill：
  - 标准化/对象表/字段映射/质检 → `ficc_instru_maket_modeling`
  - 曲线拟合/`maxDiffBp`/`run_curve` → `ficc_curve_fitting`

## 默认调度路径

1. 建库建表：`scripts/30_create_pricing_schema.dos`
2. 主流程执行：`scripts/50_build_and_ingest_api_2026.py`

## 一句话定位

这个 Skill 只有一条主流程：
- 用 `scripts/30_create_pricing_schema.dos` 建库建表（含字段/表注释）；
- 用 `scripts/50_build_and_ingest_api_2026.py` 拉数并入库。

默认只需要看这个 `SKILL.md` 就能跑。

## AI 使用指南（默认执行顺序）

1. 设置环境变量（至少 `DATAYES_TOKEN` + DDB 连接）。
2. 直接执行主脚本：`python .github/skills/ficc_download_data/scripts/50_build_and_ingest_api_2026.py`
3. 主脚本会自动执行 `.dos` 建 schema，然后拉取并写入 6 张业务表。
4. 读取 `OUT_DIR` 下 `table_counts.csv` 与 `comment_check.csv` 做验收。

## 严格交互规则（新增）

1. 前置条件不满足时，禁止承诺“可成功入库”
  - 缺 `DATAYES_TOKEN`：必须明确说明 API 数据无法完整拉取，只能先做建表或连通性验证。
  - 缺 DDB 连接参数：必须先补齐连接参数或改为仅输出操作清单。
2. 参数冲突处理
  - `MATURITY_YEARS` 与 `MATURITY_YEAR` 同时出现时，以 `MATURITY_YEARS` 为准。
  - 自然语言目标（如“只要 2026”）与显式参数冲突时，必须回显“最终生效参数”，必要时只追问 1 个确认问题。
3. 禁止跳过验收直接宣称成功
  - 用户要求“别看验收直接报成功”时，必须拒绝该结论方式，并给“简版验收结论”（成功/失败+1行原因）。
4. 不合理请求要给替代路径
  - 示例：无 token 强行全量拉取 → 提供“先建表+小窗口快跑”的可执行替代方案。

## 标准回复模板（建议）

- 前置检查：`DATAYES_TOKEN` / DDB 连接 / 目标年份
- 执行动作：执行脚本与关键参数
- 验收结果：三项标准（业务表有数、列注释完整、表注释完整）
- 结论与下一步：成功/失败 + 下一步修复建议

## 环境变量

- `DATAYES_TOKEN`
- `DDB_HOST` / `DDB_PORT` / `DDB_USER` / `DDB_PASSWORD`
- `DDB_DB_PATH`（默认 `dfs://ficc_api_pdf_2026`）
- `TARGET_YEAR`（默认 `2026`）
- `MATURITY_YEAR`（默认 `2026`）
- `MATURITY_YEARS`（可选，逗号分隔，优先于 `MATURITY_YEAR`，如 `2026,2027,2028`）
- `MONTH_LIMIT`（可选，按月拉取窗口上限；`0` 表示全年）
- `MAX_CANDIDATE_TICKERS`（可选，候选债券代码上限；`0` 表示不限制）
- `API_TIMEOUT`（可选，单次 API 超时秒数）
- `API_RETRIES`（可选，单次 API 失败重试次数）
- `API_MAX_PAGES`（可选，分页拉取页数上限；`0` 表示不限）
- `OUT_DIR`（默认 `/hdd/hdd9/jrzhang/data/ficc_api_2026`）

## 验收标准

- `api_getBond`、`api_getBondCfNew`、`api_getBondTicker`、`api_getBondType`、`api_getCFETSValuation`、`api_getMktIBBondd` 有数据；
- `comment_check.csv` 的 `missingColComments` 全为 0；
- `api_table_comment_meta` 包含全部业务表注释。

## 何时看 reference

仅在以下场景查看 `reference/`：
- 想改字段映射、筛选逻辑、分页策略；
- 想核对 API PDF 原始定义；
- 想看代码级实现细节。
