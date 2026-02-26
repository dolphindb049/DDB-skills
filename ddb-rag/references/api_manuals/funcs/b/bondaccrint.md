# bondAccrInt

## 语法

`bondAccrInt(settlement, maturity, coupon, frequency, [par=100],
[basis=1])`

别名：`fiAccrInt`

## 详情

返回有价证券的应付利息（Accrued Interest），是一个 DOUBLE 类型的标量或向量。应付利息是自上次票息支付（last coupon
payment）到交易日（settlement）所赚取的利息。

另外，应付利息（Accrued Interest）常用来计算除息价格（Clean Price）。相关计算公式为：*除息价格（Clean Price） =
含息价格（Dirty Price）- 应付利息（Accrued Interest）*。

## 参数

* **settlement** DATE 类型标量或向量，表示有价证券的结算日，即购买日期。
* **maturity** DATE 类型标量或向量，表示有价证券的到期日（有价证券有效期截止时的日期）。
* **coupon** 数值型标量或向量，表示有价证券的年息票利率。
* **frequency** 整型或 DURATION 类型的标量或向量，表示年付息频率。可选值为：
  + 1 / 1y：每年支付 1 次（按年支付）；
  + 2 / 6M：每年支付 2 次（按半年期支付）；
  + 4 / 3M：每年支付 4 次（按季支付）；
  + 12 / 1M：每年支付 12 次（按月支付）。
* **par** 可选参数，数值型标量或向量，表示证券的票面值，默认值为 100。
* **basis** 可选参数，整型或 STRING 类型的标量或向量，表示要使用的日计数基准类型，默认值为 1。可选值为：

  | Basis | 日计数基准 |
  | --- | --- |
  | 0 / "Thirty360US" | US (NASD) 30/360 |
  | 1 / "ActualActual" (默认值) | 实际/实际 |
  | 2 / "Actual360" | 实际/360 |
  | 3 / "Actual365" | 实际/365 |
  | 4 / "Thirty360EU" | 欧洲 30/360 |

## 例子

假设有一张面值为 1000 的债券，购买日期为 2024 年 1 月 1 日，到期日期为 2030 年 12 月 31 日，年息票利率为 10%，每年付息 2
次（半年付息），以 US (NASD) 30/360 为日计数基准。

```
bondAccrInt(settlement=2024.01.01, maturity=2030.12.31, coupon=0.1, frequency=2, par=1000, basis=0)
//output:0.277778
```

相关函数：[bondDirtyPrice](bondDirtyPrice.md)、[bondConvexity](bondconvexity.md)、[bondCalculator](bondCalculator.md)、[bondDuration](bondDuration.md)、[bondYield](bondyield.md)

