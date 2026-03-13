# ficc_pricing

这是一个按步骤执行的最小 FICC 债券定价 skill。

## 你会做什么

1. 从标准化建模结果中选定：
  - `dfs://instrument_std/Instrument`
  - `dfs://marketdata_std/MarketData`
2. 在 `dfs://ficc_pricing_pipeline` 中只建立一个结果表：
  - `pricing_price_result`
3. 逐只债券：
  - 从 `Instrument` 里读取标准字段
  - 从 `MarketData` 里匹配标准曲线
  - 调 `bondPricer`
4. 用 `dfs://ficc_api_pdf_2026/api_getCFETSValuation` 做最小外部校验。

## 手动执行顺序

```dolphindb
pricingDate = 2026.03.04
run(".github/skills/ficc_pricing/scripts/01_select_standard_sources.dos")
run(".github/skills/ficc_pricing/scripts/02_create_result_schema.dos")
run(".github/skills/ficc_pricing/scripts/03_run_pricing_pipeline.dos")
run(".github/skills/ficc_pricing/scripts/04_check_pricing_quality.dos")
```

## 官网文档入口

- [bondPricer](https://docs.dolphindb.cn/zh/funcs/b/bondPricer.html)
- [parseInstrument](https://docs.dolphindb.cn/zh/funcs/p/parseInstrument.html)
- [parseMktData](https://docs.dolphindb.cn/zh/funcs/p/parseMktData.html)
- [extractInstrument](https://docs.dolphindb.cn/zh/funcs/e/extractInstrument.html)
- [extractMktData](https://docs.dolphindb.cn/zh/funcs/e/extractMktData.html)

## 推荐阅读

- [reference/PRICING_KNOWLEDGE_MAP.md](reference/PRICING_KNOWLEDGE_MAP.md)
- [reference/INTERFACE_CONTRACT.md](reference/INTERFACE_CONTRACT.md)
