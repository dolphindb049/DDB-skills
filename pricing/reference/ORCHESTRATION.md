# Pricing Skill 编排说明（什么时候做什么）

## A. 只做模型通路验证（无外部市场价）
1. `scripts/02_prepare_output_schema.dos`
2. `scripts/05_run_unified_pipeline.dos` （`sourceMode=instrument_db`）
3. `python/visualize_pricing.py`

## B. 已有 data_pricing 原始表
1. 确保 `dfs://data_pricing_skill` 已存在并有：`raw_bond_info/raw_irs_curve`
2. `scripts/02_prepare_output_schema.dos`
3. `scripts/05_run_unified_pipeline.dos` （`sourceMode=data_pricing_raw`）
4. `python/visualize_pricing.py --db-path dfs://bond_pricing_workflow_v2`

## C. 接入真实市场价进行正式误差评估
1. 用 `python/ingest_external_market_csv.py` 导入 `pricing_market_external`
2. 执行 `scripts/06_compare_with_external_market.dos`
3. 执行 `python/visualize_pricing.py`（会额外输出 `error_vs_external_market.html`）

## D. 职责边界（你强调的重点）
- `data_pricing`：抓数/入湖/样本整理
- `pricing`：金融工程建模、定价、风险、误差与可视化

## E. 版本化建议
- 每次新数据源接入，仅增加一个 source adapter；
- 不改主流程输出表结构，保持可视化脚本长期稳定。
