# TABLE_SCHEMA_AND_WORKFLOW

## 1. 输入来源

- 上游债券源：`dfs://ficc_api_pdf_2026 / api_getBond`
- 上游曲线源：`dfs://ficc_curve_raw_2026 / curve_shch_yield_prepare`
- 外部估值源：`dfs://ficc_api_pdf_2026 / api_getCFETSValuation`

## 2. 标准化中间表

- `dfs://instrument_std / Instrument`
- `dfs://marketdata_std / MarketData`

这两个表分别承接：

- 债券标准化结果
- 曲线标准化结果

并且已经包含可直接给定价函数使用的对象字段：

- `Instrument.instrument`
- `MarketData.data`

## 3. 定价输出表

当前只保留一个输出表：

- 库：`dfs://ficc_pricing_pipeline`
- 表：`pricing_price_result`

### 3.1 pricing_price_result 字段

| 字段 | 含义 |
| --- | --- |
| `pricingDate` | 定价日期 |
| `instrumentId` | 债券唯一标识 |
| `bondType` | 债券产品类型 |
| `currency` | 币种 |
| `subType` | 标准化债券子类 |
| `creditRating` | 标准化信用评级 |
| `discountCurveInput` | Instrument 中原始/映射得到的贴现曲线名 |
| `resolvedCurveName` | 实际命中的标准曲线名 |
| `triedCurveNames` | 尝试过的候选曲线名 |
| `curveRefDate` | 实际使用曲线日期 |
| `status` | `Priced` 或 `Unpriced(Fail)` |
| `errorMsg` | 失败原因 |
| `npv` | `bondPricer` 返回净现值 |
| `discountCurveDelta` | 贴现曲线 Delta |
| `discountCurveGamma` | 贴现曲线 Gamma |
| `discountCurveKeyRateDuration` | 关键利率久期向量（字符串化） |
| `runTime` | 写入时间 |

## 4. 执行工作流

### Step 1
- [../scripts/01_select_standard_sources.dos](../scripts/01_select_standard_sources.dos)
- 确认 `Instrument` / `MarketData` 的实际来源与表名。

### Step 2
- [../scripts/02_create_result_schema.dos](../scripts/02_create_result_schema.dos)
- 清理遗留旧表，只创建 `pricing_price_result`。

### Step 3
- [../scripts/03_run_pricing_pipeline.dos](../scripts/03_run_pricing_pipeline.dos)
- 读取标准 `Instrument` 与 `MarketData`
- 生成候选曲线名
- 命中曲线后调用 `bondPricer`
- 将结果写入 `pricing_price_result`

### Step 4
- [../scripts/04_check_pricing_quality.dos](../scripts/04_check_pricing_quality.dos)
- 读取 `pricing_price_result`
- 读取 `api_getCFETSValuation`
- 以 `instrumentId` 对齐
- 比较 `npv` 与外部估值（优先 `grossPx`，其次 `netPx`）
