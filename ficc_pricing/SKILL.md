<<<<<<< HEAD
---
name: ficc_pricing
description: FICC 债券定价技能：按 01/02/03/04 四步完成标准源选择、结果建表、批量定价、CFETS 估值校验。
license: MIT
metadata:
  author: ddb-user
  version: "3.0.0"
  dependencies: [".github/skills/execute-dlang", ".github/skills/ficc_instru_maket_modeling"]
---

## 目标

本技能当前只保留 4 个顺序执行步骤：

1. 选择标准化的 `Instrument` / `MarketData` 输入源。
2. 创建单一结果表 `pricing_price_result`。
3. 逐债匹配标准曲线并调用 `bondPricer`。
4. 用 `dfs://ficc_api_pdf_2026/api_getCFETSValuation` 对结果做最小校验。

官网入口：
- `bondPricer`：https://docs.dolphindb.cn/zh/funcs/b/bondPricer.html
- `parseInstrument`：https://docs.dolphindb.cn/zh/funcs/p/parseInstrument.html
- `parseMktData`：https://docs.dolphindb.cn/zh/funcs/p/parseMktData.html
- `extractInstrument`：https://docs.dolphindb.cn/zh/funcs/e/extractInstrument.html
- `extractMktData`：https://docs.dolphindb.cn/zh/funcs/e/extractMktData.html

推荐先读：
- [README.md](README.md)
- [reference/PRICING_KNOWLEDGE_MAP.md](reference/PRICING_KNOWLEDGE_MAP.md)

## 执行脚本

- `scripts/01_select_standard_sources.dos`
- `scripts/02_create_result_schema.dos`
- `scripts/03_run_pricing_pipeline.dos`
- `scripts/04_check_pricing_quality.dos`

## 默认参数

- `pricingDate = 2026.03.04`
- `outputDbPath = "dfs://ficc_pricing_pipeline"`
- `outputTablePrefix = "pricing"`
- `maxBondsToPrice = 500`

## 当前结果库

- `dfs://ficc_pricing_pipeline`
  - `pricing_price_result`

## 使用方式

按步骤手动执行：

```dolphindb
pricingDate = 2026.03.04
run(".github/skills/ficc_pricing/scripts/01_select_standard_sources.dos")
run(".github/skills/ficc_pricing/scripts/02_create_result_schema.dos")
run(".github/skills/ficc_pricing/scripts/03_run_pricing_pipeline.dos")
run(".github/skills/ficc_pricing/scripts/04_check_pricing_quality.dos")
```

## 使用示例

```dolphindb
pricingDate = 2026.03.04
outputDbPath = "dfs://ficc_pricing_pipeline"
outputTablePrefix = "pricing"
maxBondsToPrice = 500
run(".github/skills/ficc_pricing/scripts/00_run_pipeline.dos")
```
=======
```skill
---
name: ficc_pricing
description: 基于 DolphinDB bondPricer 的标准化 5 步定价流水线。支持两组输入源自动探测、曲线依赖拦截、批量定价、共享表报告与落库 schema。
license: MIT
metadata:
  author: ddb-user
  version: "2.0.0"
  tags: ["dolphindb", "ficc", "bondPricer", "pipeline"]
  dependencies: [".github/skills/execute-dlang"]
---

# FICC Pricing Pipeline Skill

本技能严格按 `bondPricer(instrument, pricingDate, discountCurve, [spreadCurve], [setting])` 设计，拆成可参数化 5 步流水线。

## 支持的数据源组

1. 标准组：
   - `dfs://instrument_std`.`Instrument`
   - `dfs://marketdata_std`.`MarketData`
2. 建模组：
   - `dfs://ficc_api_pdf_2026`.`std_instrument_bond`
   - `dfs://ficc_api_pdf_2026`.`std_market_curve`

## 脚本清单（按执行顺序）

- `scripts/01_pricing_data_readiness.dos`
- `scripts/02_curve_dependency_check.dos`
- `scripts/03_create_pricing_schema.dos`
- `scripts/04_run_pricing_engine.dos`
- `scripts/05_validate_pricing_results.dos`
- 一键入口：`scripts/00_run_pipeline.dos`
- 核心模块：`scripts/pricing_engine_module.dos`
- 报告脚本：`scripts/generate_report.py`

## 参数（所有步骤可注入）

- `pricingDate`：估值日，默认 `2026.03.04`
- `outputDbPath`：结果库，默认 `dfs://ficc_pricing_pipeline`
- `outputTablePrefix`：结果表前缀，默认 `pricing`
- `maxBondsPerProfile`：每组最大定价资产数，默认 `200`
- `isStreaming`：是否流模式（当前实现按批处理执行），默认 `false`
- `toleranceBp`：验证阈值（bp），默认 `0.05`

## 共享表输出

- `pricing_data_readiness_report`
- `pricing_data_readiness_missing_assets`
- `pricing_curve_dependency_report`
- `pricing_curve_orphan_bonds`
- `pricing_output_schema_report`
- `pricing_engine_run_report`
- `pricing_validation_report`

## 持久化失败明细

- `${outputTablePrefix}_failure_detail`：逐标的失败归因（stage/reason/detail）。

## 使用方式（推荐）

在 DolphinDB 会话中设置参数后执行：

```dolphindb
pricingDate = 2026.03.04
outputDbPath = "dfs://ficc_pricing_pipeline"
outputTablePrefix = "pricing"
maxBondsPerProfile = 200
run(".github/skills/ficc_pricing/scripts/00_run_pipeline.dos")
```

## 说明

- 对于曲线缺失或曲线类型不满足 `IrYieldCurve` 的资产，流程会标记为 `Unpriced(Fail)` 并在共享表中给出原因。
- 核心循环与 `bondPricer` 调用封装在 `pricing_engine_module.dos`，Agent 仅需传参并调用步骤脚本。
```
>>>>>>> 9d5b720b37ab39d8527dcefd33710ba118119305
