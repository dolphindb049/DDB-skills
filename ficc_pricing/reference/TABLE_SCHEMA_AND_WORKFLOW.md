<<<<<<< HEAD
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
=======
# 表结构与定价流程详情

本文档用于详细说明 `02_prepare_output_schema.dos` 和 `05_run_unified_pipeline.dos` 所管理或产出的表结构，以及 `05_run_unified_pipeline.dos` 内部涉及的核心函数及其参数说明。

## 输出库表与结构 (Pricing Output Schema)

这些表结构建立在对基础数据（见 prepare 技能的数据库）的整合上。

### 1. 资产描述表 (pricing_instrument_desc)
整合了基础信息以便单独查询或在定价前展示资产的静态属性。
**包含字段**: `instrumentId`, `bondType`, `issueDate`, `maturityDate`, `couponRate` 等。

### 2. 定价所用市场数据关键点 (pricing_curve_points)
定价折现前对关键点的收集。
**包含字段**: `curveDate`, `discountYield`, `spreadYield`, `pricingDate`。

### 3. 定价结果表 (pricing_result) & 风险明细表 (pricing_risk)
包含所有债券的最终定价计算结果或各因子的分析风险值（PV, Duration, Convexity 等）。
**包含字段**: `instrumentId`, `pricingDate`, `cleanPrice`, `dirtyPrice`, `accruedInterest`, `pv01`, `duration`, `convexity`。

## 统一流水线函数的调用 (05_run_unified_pipeline.dos 内部)

### 核心计算函数说明

在 `05_run_unified_pipeline.dos` 脚本中，主要的逻辑调用包括对 `ficc_price_asset` 的使用，这是整个计算流水线的入口点之一：

#### 函数: `ficc_price_asset(instrumentData, marketData, pricingDate, ...) `
- **用途**: 计算指定的单资产在某个特定时间的价格和相关风险指标。
- **输入参数**:
    - `instrumentData`: 资产本身的属性集合（记录）。
    - `marketData`: 折算到当期的市场相关指标（基准利率曲线、利差等）。
    - `pricingDate`: 需要进行定价的计算日。
- **输出**: 返回一个包含了计算出来的净价、全价和相关的几个核心风险指标的信息块。
- **使用示例**:
  如果需要单独评估某个资产或修改计算模型，你可以复制并调整这个函数的输入，或者查看内部的具体数学公式和实现。

> **说明**: 这些函数封装在相关的 `.dos` 库或模块中，你可以在遇到定价异常情况时深入该函数的实现。
>>>>>>> 9d5b720b37ab39d8527dcefd33710ba118119305
