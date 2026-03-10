# FICC Pricing 标准化 Pipeline

本目录实现了一个以 `.dos` 为主的标准化流水线，专门适配 `bondPricer` 官方入参要求：

- `instrument`（标准 Instrument 定义）
- `pricingDate`（估值日）
- `discountCurve` / `spreadCurve`（折现曲线 / 利差曲线）

## 流水线步骤

1. `scripts/01_pricing_data_readiness.dos`  
	检查资产与市场数据是否满足最低定价要求，输出缺失字段资产清单。

2. `scripts/02_curve_dependency_check.dos`  
	检查债券到曲线的映射依赖，拦截孤儿债券（缺曲线）。

3. `scripts/03_create_pricing_schema.dos`  
	创建标准输出表结构（已存在则 pass）。

4. `scripts/04_run_pricing_engine.dos`  
	批量执行核心定价引擎，调用 `bondPricer` 并回写结果。

5. `scripts/05_validate_pricing_results.dos`  
	估值结果核对与异常统计，输出验证报告。

## 一键执行

`scripts/00_run_pipeline.dos` 会顺序执行 1~5 步。

```dolphindb
pricingDate = 2026.03.04
outputDbPath = "dfs://ficc_pricing_pipeline"
outputTablePrefix = "pricing"
maxBondsPerProfile = 200
run(".github/skills/ficc_pricing/scripts/00_run_pipeline.dos")
```

## 默认输入源（两组）

- 组1：`dfs://instrument_std`.`Instrument` + `dfs://marketdata_std`.`MarketData`
- 组2：`dfs://ficc_api_pdf_2026`.`std_instrument_bond` + `dfs://ficc_api_pdf_2026`.`std_market_curve`

## 输出表（`outputDbPath`）

- `${outputTablePrefix}_price_result`
- `${outputTablePrefix}_risk_result`
- `${outputTablePrefix}_run_summary`
- `${outputTablePrefix}_validation_summary`
- `${outputTablePrefix}_failure_detail`（逐标的失败归因）

## 共享表报告

- `pricing_data_readiness_report`
- `pricing_data_readiness_missing_assets`
- `pricing_curve_dependency_report`
- `pricing_curve_orphan_bonds`
- `pricing_output_schema_report`
- `pricing_engine_run_report`
- `pricing_validation_report`

## Python 报告（可选）

执行 `scripts/generate_report.py` 可把共享表结果在终端打印成简报：

```bash
uv run .github/skills/ficc_pricing/scripts/generate_report.py --host 127.0.0.1 --port 7731 --pricing-date 2026.03.04
```
