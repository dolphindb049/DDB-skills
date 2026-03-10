# 50_build_and_ingest_api_2026.py（主流程脚本）

## 作用

这是当前 skill 的主入口：

1. 先执行 `30_create_pricing_schema.dos` 建库建表；
2. 设置字段 comment，并维护表注释元数据；
3. 拉取目标年份行情与估值数据，构造到期债券池；
4. 批量拉取 6 类业务数据并入库；
5. 导出 CSV 与注释校验结果。

## 代码主结构

- `SCHEMA`：字段映射与写入对齐依据。
- `create_schema()`：读取并执行 `.dos` schema 脚本。
- `fetch_paginated()`：分页拉取与失败重试。
- `get_maturity_bond_universe()`：按到期年份筛选债券池。
- `append_table()`：按 schema 自动对齐字段并写入。
- `main()`：完整编排与导出。

## 可配置参数

- `TARGET_YEAR`：日频行情/估值抓取年份
- `MATURITY_YEAR`：到期债券筛选年份
- `MATURITY_YEARS`：到期债券筛选年份集合（逗号分隔，优先于 `MATURITY_YEAR`）
- `DDB_DB_PATH`：目标库路径
- `OUT_DIR`：导出目录

## 输出与验收

- 表行数：`table_counts.csv`
- 字段注释完整性：`comment_check.csv`（应全为 0）
- 表注释映射表：`api_table_comment_meta`
