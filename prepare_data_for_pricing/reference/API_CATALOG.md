# 通联 API 目录与实测说明（prepare_data_for_pricing）

> 数据来源：`scripts/10_probe_uqer_api.py` 实测输出 `reference/sample_data/api_probe_summary.json`（日期默认 `2026-01-05`）。

## 1) 债券与估值主链路（本 skill 核心）

| API | Endpoint | 最小参数 | 主要用途 | 实测状态 |
|---|---|---|---|---|
| getBond | `/api/bond/getBond.json` | `ticker` | 获取债券静态信息（起息/到期/票息/频率/类型） | OK |
| getCFETSValuation | `/api/bond/getCFETSValuation.json` | `ticker, beginDate, endDate` | 获取净价/全价/YTM，用作模型对照 | OK |
| getBondCmIrsCurve | `/api/bond/getBondCmIrsCurve.json` | `beginDate,endDate,curveCD,curveTypeCD,priceTypeCD` | 获取IRS期限点（如6M/1Y/2Y）并构建贴现曲线 | OK |

### 字段要点

- `getBond` 关键字段：
  - `secID, ticker, exchangeCD`
  - `couponTypeCD, cpnFreqCD, coupon`
  - `firstAccrDate, maturityDate`
  - `typeName`
- `getCFETSValuation` 关键字段：
  - `tradeDate, netPx, grossPx, ytm`
  - `modifiedDuration, convexity`
- `getBondCmIrsCurve` 关键字段：
  - `tradeDate, curveName, maturity, yield`

## 2) 曲线反推案例辅助链路

| API | Endpoint | 最小参数 | 主要用途 | 实测状态 |
|---|---|---|---|---|
| getMktIBBondd | `/api/market/getMktIBBondd.json` | `beginDate,endDate,pagenum,pagesize` | 取银行间债券行情，生成候选ticker池 | OK |
| getBondType | `/api/bond/getBondType.json` | `ticker` | 辅助理解`typeID/typeName` | OK |
| getBondTicker | `/api/bond/getBondTicker.json` | `pagenum,pagesize` | secID/ticker映射检索 | OK |

## 3) 期货与CTD（已探测，非本次定价主流程）

| API | Endpoint | 最小参数 | 主要用途 | 实测状态 |
|---|---|---|---|---|
| getFutu | `/api/future/getFutu.json` | `pagenum,pagesize` | 合约静态信息 | OK |
| getFutuCtd | `/api/future/getFutuCtd.json` | `tradeDate` | 最便宜可交割券（CTD） | OK |
| getMktFutd | `/api/market/getMktFutd.json` | `beginDate,endDate,pagenum,pagesize` | 期货日行情 | OK |

## 4) 现金流 API 备注

| API | Endpoint | 说明 |
|---|---|---|
| getBondCfNew | `/api/bond/getBondCfNew.json` | 对单日参数常见 `No Data Returned`，建议用更宽日期窗口（如`beginDate=20250101,endDate=20270101`） |

## 5) 参数建议

- 统一日期参数格式：`YYYYMMDD`。
- `getBondCmIrsCurve` 常用：`curveCD=01, curveTypeCD=2, priceTypeCD=2`。
- `ticker` 建议传不带市场后缀（如 `240025`），由返回中的 `secID` 决定市场对象。

## 6) 本 skill 中 API 到表映射

- `getBond` -> `raw_bond_info`
- `getCFETSValuation` -> `raw_cfets_valuation`
- `getBondCmIrsCurve` -> `raw_irs_curve`
- `getMktIBBondd` -> `raw_ib_bond_market`
- （筛选生成） -> `case2_bond_basket`
