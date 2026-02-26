# bondDirtyPrice

## 语法

`bondDirtyPrice(settlement, maturity, coupon, yield,
[frequency], [basis=1], [bondType=0])`

别名：fiDirtyPrice

## 详情

返回定期付息的面值 100 的有价证券的含息价格。

## 参数

* **settlement** DATE 类型标量或向量，表示有价证券的结算日，即购买日期。
* **maturity** DATE 类型标量或向量，与 *settlement*
  等长，表示有价证券的到期日（有价证券有效期截止时的日期）。
* **coupon** 数值型标量或向量，表示有价证券的年息票利率。
* **yield** 数值型标量或向量，表示有价证券的年收益率。
* **frequency** 整型或 DURATION 类型的标量或向量，表示年付息频率。当参数 *bondType*（详见后文介绍）指定为 1 或 2
  时无需指定此参数，*bondType* 为 0 或省略时则必须指定此参数。可选值为：
  + 1 / 1y：每年支付 1 次（按年支付）；
  + 2 / 6M：每年支付 2 次（按半年期支付）；
  + 4 / 3M：每年支付 4 次（按季支付）；
  + 12 / 1M：每年支付 12 次（按月支付）。

* **basis** 可选参数，整型或 STRING 类型的标量或向量，表示要使用的日计数基准类型。可选值为：

| Basis | 日计数基准 |
| --- | --- |
| 0 / "Thirty360US" | US (NASD) 30/360 |
| 1 / "ActualActual" (默认值) | 实际/实际 |
| 2 / "Actual360" | 实际/360 |
| 3 / "Actual365" | 实际/365 |
| 4 / "Thirty360EU" | 欧洲 30/360 |

* **bondType** 可选参数，整型或 STRING 类型的标量或向量，表示债券的类型。可选值为 0, 1, 2，默认值为 0 。
  + 0 / "FixedRate"：固息债券，定期（季度、半年或一年）按息票利率支付利息；
  + 1 / "Discount"：贴现债券，没有利息支付，以贴现方式发行的债券，期末FV=面值。
  + 2 / "ZeroCoupon"：零息债券，期末一次性支付利息和面值，期末FV=面值+利息；

注意：如果以上参数是向量，则长度必须一致。

## 例子

假设有一张债券，发行日期为 2023年1月1日，到期日期为 2030年12月31日，年息票利率为 5%，预期收益率为 6%，每年付息 2
次（半年付息），以实际/实际为日计数基准。

```
bondDirtyPrice(settlement=2023.01.01,maturity=2030.12.31,coupon=0.05,yield=0.06,frequency=2,basis=1)
```

返回：93.73475540066079

相关函数：[bondAccrInt](bondaccrint.md)、[bondConvexity](bondconvexity.md)、[bondCalculator](bondCalculator.md)、[bondDuration](bondDuration.md)、[bondYield](bondyield.md)

