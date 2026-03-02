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
