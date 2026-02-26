# bondConvexity

## 语法

`bondConvexity(settlement, maturity, coupon, yield,
[frequency], [basis=1], [bondType=0])`

别名：fiConvexity

## 详情

返回定期付息的面值为 100 的有价证券的债券凸性。凸性指债券价格与利率间非线性关系的一种量度，表示为债券价格对利率的二阶导数。

返回值：DOUBLE 类型的标量或向量。

## 参数

* **settlement** 是 DATE 类型标量或向量，表示有价证券的结算日，即购买日期。
* **maturity** 是 DATE 类型标量或向量，与 *settlement*
  等长，表示有价证券的到期日（有价证券有效期截止时的日期）。
* **coupon** 是数值型标量或向量，表示有价证券的年息票利率。
* **yield** 是数值型标量或向量，表示有价证券的年收益率。
* **frequency** 是整型或 DURATION 类型的标量或向量，表示年付息频率。当参数 *bondType*（详见后文介绍）指定为 1 或 2
  时无需指定此参数，*bondType* 为 0 或省略时则必须指定此参数。可选值为：
  + 1 / 1y：每年支付 1 次（按年支付）；
  + 2 / 6M：每年支付 2 次（按半年期支付）；
  + 4 / 3M：每年支付 4 次（按季支付）；
  + 12 / 1M：每年支付 12 次（按月支付）。
* **basis** 为可选参数，是整型或 STRING 类型的标量或向量，表示要使用的日计数基准类型。可选值为：

| Basis | 日计数基准 |
| --- | --- |
| 0 / "Thirty360US" | US (NASD) 30/360 |
| 1 / "ActualActual" (默认值) | 实际/实际 |
| 2 / "Actual360" | 实际/360 |
| 3 / "Actual365" | 实际/365 |
| 4 / "Thirty360EU" | 欧洲 30/360 |

* **bondType** 可选参数，整型或 STRING 类型的标量或向量，表示债券的类型。可选值为 0, 1, 2，默认值为 0 。

* + 0 / "FixedRate"：固息债券，定期（季度、半年或一年）按息票利率支付利息；
  + 1 / "Discount"：贴现债券，没有利息支付，以贴现方式发行的债券，期末FV=面值。
  + 2 / "ZeroCoupon"：零息债券，期末一次性支付利息和面值，期末FV=面值+利息；

注意：如果以上参数是向量，则长度必须一致。

## 例子

现计算 2023 年 1 月 1 日购买，2030 年 12 月 31 日到期的债券的凸度。其年息票利率为 0.05，预计收益率为
0.06，付息频率为每年一次，日计数基准为实际/实际。

```
bondConvexity(settlement=2023.01.01, maturity=2030.12.31, coupon=0.05, yield=0.06, frequency=1, basis=1)
// output
50.78238914091385
```

相关函数：[bondAccrInt](bondaccrint.md)、[bondCalculator](bondCalculator.md)、[bondDirtyPrice](bondDirtyPrice.md)、[bondDuration](bondDuration.md)、[bondYield](bondyield.md)

