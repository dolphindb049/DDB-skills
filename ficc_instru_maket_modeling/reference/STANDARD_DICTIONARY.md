# 债券 Instrument / MarketData 标准字典（parse 口径）

本字典仅覆盖债券标准化所需字段，字段约束以 DolphinDB 官方函数文档为准：

- `parseInstrument`：债券类型 `FixedRateBond` / `DiscountBond` / `ZeroCouponBond`
- `parseMktData`：`IrYieldCurve`

---

## 1. 标准资产表：std_instrument_bond（对应 parseInstrument）

### 1.1 必填字段（债券）

| 字段名 | 类型 | 是否必填 | 含义 | 典型源字段 |
|---|---|---|---|---|
| productType | STRING | 是 | 产品类型，固定 `Cash` | 常量 |
| assetType | STRING | 是 | 资产类型，固定 `Bond` | 常量 |
| bondType | STRING | 是 | 债券类型：`FixedRateBond`/`DiscountBond`/`ZeroCouponBond` | couponTypeCD 映射 |
| instrumentId | STRING | 否（建议填） | 债券唯一标识 | secID |
| start | DATE | 是 | 起息日 | firstAccrDate |
| maturity | DATE | 是 | 到期日 | maturityDate |
| dayCountConvention | STRING | 是 | 日期计数惯例，如 `ActualActualISDA` | 常量/映射 |

### 1.2 条件必填字段

| 字段名 | 类型 | 条件 | 含义 | 典型源字段 |
|---|---|---|---|---|
| coupon | DOUBLE | FixedRateBond / ZeroCouponBond 必填 | 票面利率（小数） | coupon / 100 |
| frequency | STRING | FixedRateBond 必填 | 付息频率，如 `Annual`/`Semiannual` | cpnFreqCD 映射 |
| issuePrice | DOUBLE | DiscountBond 必填 | 发行价 | 常量 100 或源字段 |

### 1.3 常用可选字段

| 字段名 | 类型 | 含义 | 典型源字段 |
|---|---|---|---|
| currency | STRING | 货币，默认 `CNY` | currencyCD |
| nominal | DOUBLE | 名义本金，默认 100 | par |
| calendar | STRING | 交易日历 | 常量 `CFET` |
| subType | STRING | 债券子类型（国债/政策行债等） | typeName 映射 |
| issuer | STRING | 发行人 | issuer |
| discountCurve | STRING | 定价贴现曲线名 | 规则生成 |
| spreadCurve | STRING | 定价利差曲线名 | 规则生成 |
| creditRating | STRING | 信用评级 | 源评级字段（如有） |

---

## 2. 标准市场曲线表：std_market_curve（对应 parseMktData.IrYieldCurve）

### 2.1 必填字段

| 字段名 | 类型 | 是否必填 | 含义 | 典型来源 |
|---|---|---|---|---|
| mktDataType | STRING | 是 | 固定 `Curve` | 常量 |
| curveType | STRING | 是 | 固定 `IrYieldCurve` | 常量 |
| referenceDate | DATE | 是 | 参考日 | tradeDate |
| dayCountConvention | STRING | 是 | 曲线计息天数规则 | 常量/映射 |
| compounding | STRING | 是 | 复利规则，如 `Continuous` | 常量 |
| frequency | STRING 或 INT | 是 | 计息频率，如 `Annual` | 常量/映射 |
| interpMethod | STRING | 是 | 插值方法，如 `Linear` | 常量 |
| extrapMethod | STRING | 是 | 外推方法，如 `Flat` | 常量 |
| dates | DATE[]（落库为 STRING） | 是 | 节点日期向量 | maturityDate 聚合 |
| values | DOUBLE[]（落库为 STRING） | 是 | 节点值向量（小数） | YTM/closeYield 聚合后 /100 |
| currency | STRING | 是 | 货币，如 `CNY` | 常量/映射 |

### 2.2 可选字段

| 字段名 | 类型 | 含义 | 典型来源 |
|---|---|---|---|
| curveName | STRING | 曲线名称 | 规则生成，如 `CNY_TREASURY_BOND_YTM` |
| settlement | DATE | 结算日 | referenceDate + 2 |
| curveModel | STRING | 曲线模型（Bootstrap/NS/NSS） | 常量或策略 |
| curveParams | DICT/ANY（落库为 STRING） | 曲线参数（NS/NSS） | 模型参数 |

---

## 3. 本技能采用的源表

- `api_getBond`：债券静态字段（secID、起息到期、票息、类型、发行人）
- `api_getMktIBBondd`：日行情收益率（tradeDate、YTM/closeYield）
- `curve_shch_yield_raw`：上清所曲线原始节点（curveName/curveType/referenceDate/tenorLabel/yieldPct）

> 说明：
>
> - API 曲线通道：`dates` 使用债券到期日，`values` 使用收益率转小数；按 `referenceDate + curveName` 聚合为向量。
> - curve_raw 曲线通道：`dates` 使用 `referenceDate + tenor` 推导节点日，`values` 使用 `yieldPct/100`；按 `referenceDate + curveName + curveType` 聚合为向量。
