# createPricingEngine

## 语法

`createPricingEngine(name, dummyTable, timeColumn, typeColumn, securityType,
method, outputTable, [securityReference], [keyColumn],
[extraMetrics])`

## 详情

本函数用于计算估值定价。

该引擎既可调用 DolphinDB
诸多用于估值定价的函数，也支持传入自定义函数或表达式。适用于多种业务场景、交易品种、数据频率的现代金融工具，进而帮助用户准确判断市场动态、优化投资决策、并有效管理市场风险。

## 参数

**name** 字符串标量，表示引擎的名称。该参数是引擎在一个数据节点上的唯一标识，可包含字母，数字和下划线，但必须以字母开头。

**dummyTable** 表，用于指定输入数据的表结构。

**timeColumn** 字符串向量，用于指定输入表中的时间列。

**typeColumn** 字符串向量，用于指定表中的债券列。根据债券列，引擎调用 *method*
中相应的方法。

**securityType** 整型向量，用于指定需要定价的债券类型。

**method** 元代码元组，用于指定债券定价算法和参数。注意：

* *method* 指定的方法和 *securityType* 指定的债券列一一对应。
* 可以传入内置函数、自定义函数或表达式。
* 算法中的参数可以是输入表中的列或者是参数 *securityReference* 中的列或者常量，优先查找参数
  *dummyTable* 中的列；如果有重名，可以用列引用的方式，如
  `dummyTable.X`。
* 对于 [vanillaOption](../v/vanillaoption.md) 的 kwargs,
  支持以下几种写法：
  + 单独指定kwargs

    ```
    kwargs = dict(STRING, ANY)
    kwargs['theta'] = <theta>
    kwargs['kappa'] = <kappa>
    kwargs['rho'] = <rho>
    kwargs['sigma'] = <sigma>
    method=[<vanillaOption(settlement, maturity, valDay, spot, strike, riskFree, dividend, volatility, isCall, style, basis, calendar,"heston",kwargs)>]
    ```
  + 直接在method中构造kwargs

    ```
    method=[<vanillaOption(settlement, maturity, valDay, spot, strike, riskFree, dividend, volatility, isCall, style, basis, calendar,"heston",dict(`theta`kappa`rho`sigma, [theta, kappa, rho, sigma]))>]
    ```

**outputTable** 计算结果的输出表。遵循如下列顺序：

1. 时间列，与参数 *timeColumn* 保持一致。
2. 债券类型，与参数 *typeColumn* 保持一致。
3. 合约代码列，与参数 *keyColumn* 保持一致。
4. 定价结果，DOUBLE 型数组向量，输出值的数量与参数 *methodList* 中指定算法的数量保持一致。
5. 额外指定输出的算子，与 *extraMetrics* 保持一致。

**securityReference**
可选参数，内存表，用于指定每个合约基础信息。注意：不同品种的合约基础信息略有不同，如有需要请先整合到一张表里再输入；若没有信息则为空值。如下为表说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| type | INT | 整型标量或向量，表示标的类型 |
| assetType | INT | 资产类型 |
| symbol | SYMBOL | 合约名 |
| maturity | DOUBLE | 到期日 |
| coupon | DOUBLE | 票面利率 |
| frequency | INT | 付息频率 |
| underlying | SYMBOL | 表示标的利率，可选值为：”FR007”, “Shibor3M“，“FDR001”，“FDR007”，“ShiborO/N”，“LPR1Y”，“LPR5Y” |
| startDate | DATE | 第一次利率互换的日期 |
| endDate | DATE | 最后一次利率互换的日期。注意：须晚于 *startDay。* |
| fixRate | DOUBLE | 百分数值，表示利率互换中固定利率支付方所支付的利率，在整个利率互换期间该利率不变 |
| interval | INT | 利率互换的间隔时间 |
| basis | INT | 表示要使用的日计数基准类型 |
| Price | DOUBLE | 标的资产的当前价格。 |
| strike | DOUBLE | 标的资产的行权价格 |
| dividendYield | DOUBLE | 表示分红利率 |

**keyColumn** 可选参数，字符串标量或元组（长度为2），用于指定 *dummyTable* 和
*securityReference*  中的合约代码列。注意：需要同时指定或同时不指定参数 *sucurityReference* 和
*keyColumn*。

**extraMetrics**
可选参数，元代码元组，用于指定除定价结果外需要额外输出的信息。该参数可以传入输入列中的部分列、*securityReference*
中的部分列等。注意：不可包含常量。

## 例子

首先指定参数，创建一个估值定价引擎。

```
//指定传入表结构、合约基础信息、输出表结构
dummyTable = table(1:0, `tradeTime`Symbol`realTimeX`predictY`price,[TIMESTAMP,SYMBOL, DOUBLE, DOUBLE, DOUBLE])
securityReference= table(take(0 1 2, 100) as type, take(1 2 3 4, 100) as assetType,"s"+string(1..100) as symbol, 2025.07.25+1..100 as maturity, rand(10.0, 100) as coupon, rand(10,100) as frequency,take([1],100) as basis )
outputTable = table(1:0, `tradeTime`type`symbol`result`factor1`factor2,[TIMESTAMP, INT, SYMBOL, DOUBLE, DOUBLE, DOUBLE])

//指定需要定价的债券类型、有价证券的购买日期、证券票面值、债券定价算法和参数
typeList=[0,1,2]
date=2024.07.25
par=100
methodList=[<bondDirtyPrice(date, maturity, coupon, predictY, frequency,basis)>,
             <bondAccrInt(date, maturity, coupon, frequency,par,basis)>,
             <bondDuration(date, maturity, coupon, predictY, frequency, basis)>]

//基于上述参数创建估值定价引擎
createPricingEngine(name="engine1", dummyTable=dummyTable, timeColumn=`tradeTime, typeColumn=`type, securityType=typeList, method=methodList, outputTable=outputTable, securityReference=securityReference, keyColumn=`Symbol, extraMetrics=[<price * predictY>, <coupon+price>])
```

成功创建引擎后，传入符合期望格式的数据并使用 `getStreamEngine`
函数调用引擎句柄，从而计算估值定价。

```
data = table(take(now(), 100)as tradeTime,"s"+string(1..100) as symbol, rand(10.0, 100) as realTimeX,  rand(10.0, 100) as predictY, rand(10.0, 100) as price)
getStreamEngine(`engine1).append!(data)
```

**相关函数**

* [bondDirtyPrice](../b/bondDirtyPrice.md)
* [bondAccrInt](../b/bondaccrint.md)
* [bondDuration](../b/bondDuration.md)
* [bondConvexity](../b/bondconvexity.md)
* [bondYield](../b/bondyield.md)
* [irs](../i/irs.md)

