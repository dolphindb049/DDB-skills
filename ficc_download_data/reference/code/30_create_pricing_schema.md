# 30_create_pricing_schema.dos

## 作用

主流程 schema 脚本，负责一次性创建以下对象：

- 6 张 API 业务表（`api_getBond*` / `api_getCFETSValuation` / `api_getMktIBBondd`）
- `api_table_comment_meta`（表注释元数据）

## 关键点

- `dbPath = "__DB_PATH__"` 使用占位符，由主脚本替换为 `DDB_DB_PATH`。
- 默认是重跑模式：先 `dropDatabase` 再 `database(...)`。
- 字段注释和表注释都在 `.dos` 内定义。

## 调用关系

不需要手动执行。`50_build_and_ingest_api_2026.py` 会自动读取并执行它。
