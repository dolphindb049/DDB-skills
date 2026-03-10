```skill
---
name: ficc_curve_fitting_import
description: 将上清所曲线原始 CSV 全量导入 DolphinDB（含字段注释与表注释），并输出可复核验收结果。
license: MIT
metadata:
  author: ddb-user
  version: "1.0.0"
---

## 目标

本 Skill 只做“原始曲线数据入库”，不做拟合：

- 建立曲线原始库（默认 `dfs://ficc_curve_raw_2026`）；
- 将 `curve/*.csv` 全量导入 `curve_shch_yield_raw`；
- 维护字段注释与表注释元数据；
- 导出行数与注释完整性检查结果。

## 路由提示（给 Agent）

- 优先使用本 Skill 的关键词：曲线原始入库、CSV 导入、上清所曲线、字段注释、表注释。
- 出现以下词时应转到标准化 Skill：`parseMktData`、对象表 `MarketData`、字段映射、质检。

## 默认调度路径

1. 建库建表：`scripts/30_create_curve_raw_schema.dos`
2. 主流程执行：`scripts/50_build_and_ingest_curve_raw_2026.py`

## AI 使用指南（默认执行顺序）

1. 设置 DDB 连接参数与可选路径参数（见下文环境变量）。
2. 执行：`python .github/skills/ficc_curve_fitting_import/scripts/50_build_and_ingest_curve_raw_2026.py`
3. 脚本自动完成：建库 -> 全量导入 -> 文件清单写入 -> 验收导出。
4. 读取 `OUT_DIR` 下 `table_counts.csv` 与 `comment_check.csv` 做验收。

## 环境变量

- `DDB_HOST` / `DDB_PORT` / `DDB_USER` / `DDB_PASSWORD`
- `DDB_DB_PATH`（默认 `dfs://ficc_curve_raw_2026`）
- `CURVE_DIR`（默认 `.github/skills/ficc_curve_fitting_import/curve`）
- `CSV_ENCODING`（默认 `gb18030`）
- `OUT_DIR`（默认 `/hdd/hdd9/jrzhang/data/ficc_curve_raw_2026`）

## 输出产物

- 原始表：`curve_shch_yield_raw`
- 文件清单表：`curve_file_manifest`
- 表注释元数据：`curve_table_comment_meta`
- 导出文件：`table_counts.csv`、`comment_check.csv`

## 验收标准

- `curve_shch_yield_raw` 有数据；
- `curve_file_manifest` 与导入文件数一致；
- `comment_check.csv` 的 `missingColComments` 全为 0。

```
