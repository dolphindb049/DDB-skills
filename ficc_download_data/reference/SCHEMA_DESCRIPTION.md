# Schema 说明（当前版本）

本 Skill 当前只保留一套 schema 方案。

## 主流程

- 调度入口：`scripts/50_build_and_ingest_api_2026.py`
- schema 文件：`scripts/30_create_pricing_schema.dos`
- 默认库：`dfs://ficc_api_pdf_2026`

## 表集合

- `api_getBond`
- `api_getBondCfNew`
- `api_getBondTicker`
- `api_getBondType`
- `api_getCFETSValuation`
- `api_getMktIBBondd`
- `api_table_comment_meta`

## 定义来源

- 字段与注释权威来源：`reference/API/*.pdf`
- 实际建表定义：`scripts/30_create_pricing_schema.dos`
- 入库字段对齐：`scripts/50_build_and_ingest_api_2026.py` 的 `SCHEMA`