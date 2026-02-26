# bondYield

## 语法

`bondYield(settlement, maturity, coupon, price, redemption, frequency,
[basis=1], [method='newton'], [maxIter])`

## 详情

通过债券净价（Clean Price）计算有价债券的收益率（Yield）。返回 DOUBLE 类型的标量或向量。注意：

* 如果结算日（settlement）距离到期日（maturity）不足一个票息期（coupon period），则收益率按以下方式计算：

![](../../tutorials/images/yield.png)

* 部分参数说明：
  + A：票息期开始日至结算日之间的天数（应计利息天数）。
  + DSR：从结算日期到赎回日期之间的天数。
  + E ：一个票息期内的天数。

* 如果在到期日之前有多个票息期，则通过牛顿法等优化算法迭代地调整收益率的值，使基于该收益率计算得到的债券净价接近用户输入的实际价格。本函数将收益率的初值设置为年息票利率（Annual
  Coupon Rate）。

## 参数

**settlement** DATE 类型标量或向量，表示有价证券的结算日，即购买日期。

**maturity** DATE 类型标量或向量，非负数，表示有价证券的到期日（有价证券有效期截止时的日期）。

**coupon** 数值型标量或向量，表示有价证券的年息票利率。

**price** 数值型标量或向量，表示有价证券净价（按面值为 ￥100 计算）。

**redemption** 数值型标量或向量，表示面值 ￥100 的有价证券的清偿价格。

**frequency** 整型或 DURATION 类型的标量或向量，表示年付息频率。可选值为：

* 1 / 1y：每年支付 1 次（按年支付）；
* 2 / 6M：每年支付 2 次（按半年期支付）；
* 4 / 3M：每年支付 4 次（按季支付）；
* 12 / 1M：每年支付 12 次（按月支付）。

**basis** 可选参数，整型或 STRING 类型的标量或向量，与 *settlement* 等长，表示要使用的日计数基准类型。默认值为 1。可选值为：

| Basis | 日计数基准 |
| --- | --- |
| 0 / "Thirty360US" | US (NASD) 30/360 |
| 1 / "ActualActual" (默认值) | 实际/实际 |
| 2 / "Actual360" | 实际/360 |
| 3 / "Actual365" | 实际/365 |
| 4 / "Thirty360EU" | 欧洲 30/360 |

**method**可选参数，字符串标量或向量，表示求解收益率所使用的优化算法，可选值为：

* “newton“：表示使用 Newton 算法，默认值。
* “brent“：表示使用 brent 算法。
* “nm“：表示使用 Nelder-Mead 单纯形算法。
* “bfgs“：表示使用 bfgs 算法。
* “lbfgs“ ：表示使用 lbfgs 算法。

**maxIter** 可选参数，整型标量或向量，表示求解收益率时优化算法的最大迭代次数。默认值为 100。

注意：如果输入参数中部分为标量，其余为向量时，则会将标量当作与向量长度相同，所有元素值等于该标量的向量。所有向量的长度必须一致。

## 例子

假设有一张净价为 95.04287 的债券，交易日期为 2008年2月15日，到期日期为 2016年11月15日，年息票利率为 5.75%，债券赎回价格为 100
元，每年付息 2 次（半年付息），以 US (NASD) 30/360 为日计数基准，分别使用 'newton', 'nm', 'brentq',
'bfgs','lbfgs'
优化算法计算其收益率。

```
settlement = 2008.02.15
maturity = 2016.11.15
coupon = 0.0575
price = 95.04287
redemption = 100
frequency = 2
basis = 0
method = ['newton', 'nm', 'brentq', 'bfgs','lbfgs']
bondYield(settlement, maturity, coupon, price, redemption, frequency, basis, method)
// Output:[0.065000006880755,0.064999847412109,0.065000006880759,0.064999999976412,0.065000004967984]
```

相关函数：[bondAccrInt](bondaccrint.md)、[bondConvexity](bondconvexity.md)、[bondDirtyPrice](bondDirtyPrice.md)、[bondDuration](bondDuration.md)、[bondCalculator](bondCalculator.md)

