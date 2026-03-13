<<<<<<< HEAD
# Pricing Skill 接口契约

## 1) Instrument 输入接口

本 skill 直接消费标准化建模后的：
- `dfs://instrument_std/Instrument`

当前债券定价主流程最关心的字段：
- `instrumentId`：债券唯一标识
- `bondType`：`FixedRateBond` / `ZeroCouponBond` / `DiscountBond`
- `start`：起息日
- `maturity`：到期日
- `issuePrice`：发行价
- `coupon`：票息，按小数存储，例如 3% -> `0.03`
- `calendar`：交易日历，当前默认 `CFET`
- `frequency`：付息频率，例如 `Annual` / `Semiannual` / `Quarterly` / `Once`
- `dayCountConvention`：计息日规则
- `currency`：币种，当前主要为 `CNY`
- `subType`：债券子类型，例如 `TREASURY_BOND` / `MTN` / `NCD`
- `creditRating`：评级，例如 `AAA` / `AA+`
- `discountCurve`：若已知，则直接指定对应标准曲线名
- `issuer`：发行人
- `instrument`：最终 `parseInstrument(...)` 生成的 `INSTRUMENT` 对象

官网对应：
- [parseInstrument](https://docs.dolphindb.cn/zh/funcs/p/parseInstrument.html)
- [extractInstrument](https://docs.dolphindb.cn/zh/funcs/e/extractInstrument.html)

## 2) MarketData 输入接口

本 skill 直接消费标准化建模后的：
- `dfs://marketdata_std/MarketData`

当前债券定价主流程最关心的字段：
- `referenceDate`
- `curveName`
- `currency`
- `curveType`，固定为 `IrYieldCurve`
- `dayCountConvention`
- `compounding`
- `frequency`
- `interpMethod`
- `extrapMethod`
- `dates`
- `values`
- `data`：最终 `parseMktData(...)` 生成的 `MKTDATA` 对象

官网对应：
- [parseMktData](https://docs.dolphindb.cn/zh/funcs/p/parseMktData.html)
- [extractMktData](https://docs.dolphindb.cn/zh/funcs/e/extractMktData.html)

## 3) 定价接口

当前定价统一调用：
- [bondPricer](https://docs.dolphindb.cn/zh/funcs/b/bondPricer.html)

当前脚本使用的 `setting` 键：
- `calcDiscountCurveDelta`
- `calcDiscountCurveGamma`
- `calcDiscountCurveKeyRateDuration`
- `discountCurveShift`
- `discountCurveKeyTerms`
- `discountCurveKeyShifts`

## 4) 输出接口

默认只保留一个结果表：
- 库：`dfs://ficc_pricing_pipeline`
- 表：`pricing_price_result`

核心输出字段：
- `instrumentId`
- `resolvedCurveName`
- `triedCurveNames`
- `status`
- `errorMsg`
- `npv`
- `discountCurveDelta`
- `discountCurveGamma`
- `discountCurveKeyRateDuration`

## 5) 校验接口

外部校验表：
- `dfs://ficc_api_pdf_2026/api_getCFETSValuation`

当前最小校验逻辑：
- 以 `instrumentId` 对齐
- 模型结果使用 `npv`
- CFETS 侧优先使用 `grossPx`，若缺失再回退 `netPx`
=======
# Pricing Skill 接口契约（可复用核心）

## 1) 输入接口（标准化债券描述）
统一中间结构（脚本内部表 `bondDesc`）：
- `instrumentId` STRING
- `issuer` STRING
- `bondType` STRING (`FixedRateBond`/`ZeroCouponBond`)
- `start` DATE
- `maturity` DATE
- `issuePrice` DOUBLE
- `coupon` DOUBLE (小数，如 0.03)
- `frequency` STRING (`Annual/Semiannual/Quarterly/Once`)
- `dayCountConvention` STRING
- `subType` STRING

任何上游数据源只要能映射到上述结构，即可进入统一定价流程。

## 2) 曲线接口
统一曲线字典字段：
- `mktDataType="Curve"`
- `curveType="IrYieldCurve"`
- `referenceDate` DATE
- `currency` STRING
- `curveName` STRING
- `dayCountConvention` STRING
- `compounding` STRING
- `interpMethod` STRING
- `extrapMethod` STRING
- `frequency` STRING
- `dates` DATE VECTOR
- `values` DOUBLE VECTOR

## 3) 输出接口（DFS 持久化）
默认库：`dfs://bond_pricing_workflow_v2`
- `pricing_instrument_desc`
- `pricing_curve_points`
- `pricing_result`
- `pricing_risk`
- `pricing_market_external`
- `pricing_compare_external`

## 4) 可视化接口
`python/visualize_pricing.py` 支持参数：
- `--db-path`
- `--result-table`
- `--curve-table`
- `--risk-table`
- `--compare-table`
- `--pricing-date`
- `--instrument-id`

## 5) 适配建议
- 数据导入 skill（例如 data_pricing）只负责把原始字段准备好。
- pricing skill 只负责：标准化映射 -> 定价 -> 风险 -> 误差评估 -> 可视化。
- 若有新源，仅新增“映射函数”而不改核心定价流程。
>>>>>>> 9d5b720b37ab39d8527dcefd33710ba118119305
