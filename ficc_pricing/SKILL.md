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
