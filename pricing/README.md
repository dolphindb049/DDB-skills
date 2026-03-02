# DolphinDB 债券定价技能包（专业版）

## 你会得到什么
- 一套可复用的债券定价流水线：标准接口映射 → 批量定价 → 风险指标 → 误差评估 → 可视化。
- 全流程不依赖共享内存表，结果持久化到 DFS：`dfs://bond_pricing_workflow_v2`。
- 支持与 `data_pricing` 联动，并支持外部市场价导入后正式对比。

## 脚本入口
- [scripts/00_cleanup_shared_objects.dos](scripts/00_cleanup_shared_objects.dos)
- [scripts/01_data_discovery.dos](scripts/01_data_discovery.dos)
- [scripts/02_prepare_output_schema.dos](scripts/02_prepare_output_schema.dos)
- [scripts/03_run_pricing_pipeline.dos](scripts/03_run_pricing_pipeline.dos)
- [scripts/04_asset_pricing_detail.dos](scripts/04_asset_pricing_detail.dos)
- [scripts/05_run_unified_pipeline.dos](scripts/05_run_unified_pipeline.dos)
- [scripts/06_compare_with_external_market.dos](scripts/06_compare_with_external_market.dos)

## 理论与数据源
- [reference/THEORY.md](reference/THEORY.md)
- [reference/DATA_SOURCES.md](reference/DATA_SOURCES.md)
- [reference/INTERFACE_CONTRACT.md](reference/INTERFACE_CONTRACT.md)
- [reference/ORCHESTRATION.md](reference/ORCHESTRATION.md)

## Python 可视化
- [python/visualize_pricing.py](python/visualize_pricing.py)
- [python/ingest_external_market_csv.py](python/ingest_external_market_csv.py)
- [python/requirements.txt](python/requirements.txt)

## 推荐执行顺序
1. 先看 [reference/ORCHESTRATION.md](reference/ORCHESTRATION.md) 选执行路径（instrument_db 或 data_pricing_raw）
2. 执行 [scripts/02_prepare_output_schema.dos](scripts/02_prepare_output_schema.dos)
3. 执行 [scripts/05_run_unified_pipeline.dos](scripts/05_run_unified_pipeline.dos)
4. 可选：导入外部市场价并执行 [scripts/06_compare_with_external_market.dos](scripts/06_compare_with_external_market.dos)
5. 执行 [python/visualize_pricing.py](python/visualize_pricing.py)

## 当前误差定义
- `priceDiff = modelPrice - marketProxyPrice`
- `diffBp = (modelPrice / marketProxyPrice - 1) * 10000`
- `modelVsIssue = modelPrice - issuePrice`

后续接入真实市场价后，可以把 `marketProxyPrice` 替换为 `marketPrice` 做正式模型评估。

## 职责边界
- `data_pricing`：抓取/入库/原始数据治理
- `pricing`：金融工程建模、定价、风险、误差与可视化
