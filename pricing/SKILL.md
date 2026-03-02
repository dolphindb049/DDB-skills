---
name: pricing
description: 债券定价与风险分析技能。聚焦金融工程建模、定价、风险与误差评估，可与 data_pricing 联动。
license: MIT
metadata:
  author: ddb-user
  version: "1.2.0"
  tags: ["bond", "pricing", "risk", "dolphindb", "visualization", "reusable"]
---

# 债券定价技能（Pricing Workflow）

本技能遵循 execute-dlang 的执行方式，强调可复用接口：
- 数据抓取和入湖由 data_pricing 负责
- 本技能只做标准化映射、定价、风险、误差评估、可视化

默认输出库：dfs://bond_pricing_workflow_v2。

## 目录结构

```text
pricing/
├── SKILL.md
├── README.md
├── scripts/
│   ├── 00_cleanup_shared_objects.dos
│   ├── 01_data_discovery.dos
│   ├── 02_prepare_output_schema.dos
│   ├── 03_run_pricing_pipeline.dos
│   ├── 04_asset_pricing_detail.dos
│   ├── 05_run_unified_pipeline.dos
│   └── 06_compare_with_external_market.dos
├── reference/
│   ├── THEORY.md
│   ├── DATA_SOURCES.md
│   ├── INTERFACE_CONTRACT.md
│   └── ORCHESTRATION.md
└── python/
    ├── requirements.txt
    ├── visualize_pricing.py
    └── ingest_external_market_csv.py
```

## 统一入口

- 使用 scripts/05_run_unified_pipeline.dos
- 通过 sourceMode 切换输入源：
  - instrument_db
  - data_pricing_raw

## 快速执行

```bash
python3 ./skills/execute-dlang/scripts/ddb_runner/execute.py ./skills/pricing/scripts/02_prepare_output_schema.dos --host 192.168.100.43 --port 8671 --user admin --password 123456
python3 ./skills/execute-dlang/scripts/ddb_runner/execute.py ./skills/pricing/scripts/05_run_unified_pipeline.dos --host 192.168.100.43 --port 8671 --user admin --password 123456
python3 ./skills/execute-dlang/scripts/ddb_runner/execute.py ./skills/pricing/scripts/04_asset_pricing_detail.dos --host 192.168.100.43 --port 8671 --user admin --password 123456
```

## 外部市场价接入

```bash
python3 ./skills/pricing/python/ingest_external_market_csv.py --csv /path/to/market_price.csv --host 192.168.100.43 --port 8671 --user admin --password 123456
python3 ./skills/execute-dlang/scripts/ddb_runner/execute.py ./skills/pricing/scripts/06_compare_with_external_market.dos --host 192.168.100.43 --port 8671 --user admin --password 123456
```

## 可视化

```bash
pip install -r ./skills/pricing/python/requirements.txt
python3 ./skills/pricing/python/visualize_pricing.py --host 192.168.100.43 --port 8671 --user admin --password 123456 --db-path dfs://bond_pricing_workflow_v2 --pricing-date 2025-08-18 --instrument-id 109400.XSHE
```
