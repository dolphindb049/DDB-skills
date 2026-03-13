# FICC 债券定价知识图谱（最小可运行版）

## 1. 你在做什么

这个 skill 的目标不是一次性堆很多功能，而是让用户能顺着下面这条链路理解并执行：

1. 原始债券信息 -> 标准化 `Instrument`
2. 原始收益率曲线 -> 标准化 `MarketData`
3. `Instrument` + `MarketData` -> `bondPricer`
4. `bondPricer` 结果 -> 与 `api_getCFETSValuation` 对比

其中最核心的 3 个对象是：

- `INSTRUMENT`
- `MKTDATA`
- `bondPricer`

官网文档入口：

- [bondPricer](https://docs.dolphindb.cn/zh/funcs/b/bondPricer.html)
- [parseInstrument](https://docs.dolphindb.cn/zh/funcs/p/parseInstrument.html)
- [parseMktData](https://docs.dolphindb.cn/zh/funcs/p/parseMktData.html)
- [extractInstrument](https://docs.dolphindb.cn/zh/funcs/e/extractInstrument.html)
- [extractMktData](https://docs.dolphindb.cn/zh/funcs/e/extractMktData.html)

## 2. 标准化建模在干什么

标准化建模的目标，是把来源各异的原始字段，统一成 DolphinDB 定价函数能识别的金融对象。

### 2.1 债券侧：统一成 `Instrument`

输入原始表通常是：
- `dfs://ficc_api_pdf_2026/api_getBond`

输出标准表是：
- `dfs://instrument_std/Instrument`

最核心的映射关系：

| 标准字段 | 金融含义 | 典型来源 | 用途 |
| --- | --- | --- | --- |
| `instrumentId` | 债券唯一标识 | `secID` | 对账、关联、结果落表 |
| `bondType` | 债券产品结构 | `couponTypeCD` | 决定是固定息、贴现债还是零息债 |
| `start` | 起息日 | `firstAccrDate` | 现金流起点 |
| `maturity` | 到期日 | `maturityDate` | 现金流终点 |
| `issuePrice` | 发行价 | 原始发行相关字段 | 贴现债定价需要 |
| `coupon` | 票息 | `coupon` | 息票计算 |
| `frequency` | 付息频率 | `cpnFreqCD` | 年付/半年付/季付/到期一次 |
| `dayCountConvention` | 日计数规则 | 当前脚本固定映射 | 利息和贴现计算 |
| `currency` | 币种 | `currencyCD` | 曲线匹配 |
| `subType` | 债券子类 | `typeName` | 曲线分类 |
| `creditRating` | 信用评级 | `typeName` 中括号评级 | 信用曲线匹配 |
| `discountCurve` | 显式贴现曲线名 | 映射生成 | 定价优先使用 |
| `issuer` | 发行人 | `issuer` | 描述性字段 |

### 2.2 曲线侧：统一成 `MarketData`

输入原始表通常是：
- `dfs://ficc_curve_raw_2026/curve_shch_yield_prepare`

输出标准表是：
- `dfs://marketdata_std/MarketData`

最核心的映射关系：

| 标准字段 | 金融含义 | 典型来源 | 用途 |
| --- | --- | --- | --- |
| `referenceDate` | 曲线参考日 | 原始曲线日期 | 定价日匹配 |
| `curveName` | 标准曲线名 | 原始 `curveName` + 规则映射 | 曲线命中 |
| `currency` | 币种 | 当前脚本固定 `CNY` | 曲线分类 |
| `curveType` | 曲线类型 | 固定 `IrYieldCurve` | `bondPricer` 要求 |
| `dayCountConvention` | 曲线日计数 | 映射生成 | 年化折算 |
| `compounding` | 复利方式 | 映射生成 | 曲线解释 |
| `frequency` | 计息频率 | 映射生成 | 曲线解释 |
| `interpMethod` | 插值方法 | 映射生成 | 节点间利率插值 |
| `extrapMethod` | 外推方法 | 映射生成 | 超出节点期限的处理 |
| `dates` | 曲线节点日期 | 原始节点聚合 | 曲线构造 |
| `values` | 曲线节点利率 | 原始节点聚合 | 曲线构造 |
| `data` | `MKTDATA` 对象 | `parseMktData(...)` | 直接给 `bondPricer` |

## 3. `bondPricer` 需要什么

根据官网文档，`bondPricer` 的输入最关键的是：

### 3.1 债券对象侧

债券必须先被解析为 `INSTRUMENT`。

对当前 skill 里的债券场景，最关键字段是：

- `productType = "Cash"`
- `assetType = "Bond"`
- `bondType`
- `instrumentId`
- `start`
- `maturity`
- `issuePrice` / `coupon`
- `frequency`
- `dayCountConvention`
- `currency`
- `discountCurve`
- `spreadCurve`（当前最小版未使用）
- `subType`
- `creditRating`

### 3.2 曲线对象侧

贴现曲线必须先被解析为 `MKTDATA`，且是 `IrYieldCurve`。

最关键字段是：

- `mktDataType = "Curve"`
- `curveType = "IrYieldCurve"`
- `referenceDate`
- `dayCountConvention`
- `compounding`
- `frequency`
- `interpMethod`
- `extrapMethod`
- `dates`
- `values`
- `curveName`
- `currency`

## 4. 当前最小定价 pipeline 在做什么

当前脚本是：
- [scripts/03_run_pricing_pipeline.dos](../scripts/03_run_pricing_pipeline.dos)

逻辑非常简单：

1. 从 `Instrument` 中取 `discountCurve / currency / subType / creditRating`
2. 生成候选曲线名
3. 依次在 `MarketData` 中查找候选曲线
4. 命中后调用 `bondPricer`
5. 保存 `npv / discountCurveDelta / discountCurveGamma / discountCurveKeyRateDuration`

## 5. 为什么很多债会回退到 `CNY_TREASURY_BOND`

这是当前“最小可运行版”的保守处理，不是最终业务最优规则。

原因通常是：

- `Instrument` 里没有明确 `discountCurve`
- `creditRating` 为空或不稳定
- `subType + rating` 无法稳定命中已存在的标准曲线名

这时脚本会按下面顺序回退：

1. 显式 `discountCurve`
2. `currency + "_" + subType + "_" + rating`
3. `currency + "_" + subType`（利率债）
4. `currency + "_TREASURY_BOND"`
5. `CNY_TREASURY_BOND`

所以大量命中 `CNY_TREASURY_BOND` 的根因，通常不在定价脚本本身，而在标准化阶段：

- `subType` 是否标准化得足够细
- `creditRating` 是否提取得足够准
- `discountCurve` 是否应该直接在标准化阶段生成

## 6. 当前最小校验在做什么

当前校验脚本是：
- [scripts/04_check_pricing_quality.dos](../scripts/04_check_pricing_quality.dos)

它只做一件事：

- 将 `pricing_price_result.npv` 与 `dfs://ficc_api_pdf_2026/api_getCFETSValuation` 中的估值字段对齐比较。

当前规则：

- 优先使用 `grossPx`
- 若无 `grossPx`，退回 `netPx`

这是一种“最小校验”，目的是先快速看模型结果和外部估值偏差，而不是做复杂质量报表。

## 7. 建议用户怎么理解和排查

建议按这个顺序看：

1. `Instrument` 是否字段齐全：`bondType/start/maturity/coupon/frequency/subType/rating`
2. `MarketData` 是否有对应标准 `curveName`
3. `03_run_pricing_pipeline.dos` 里最终命中的 `resolvedCurveName` 是什么
4. `pricing_price_result` 中 `errorMsg` 是否为空
5. `04_check_pricing_quality.dos` 中 `absDiff` 最大的是哪些债

这样可以把“数据标准化问题”和“定价函数问题”分开看。