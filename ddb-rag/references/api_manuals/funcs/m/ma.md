# ma

## 语法

`ma(X, window, maType)`

TA-lib 系列函数其他通用参数说明和窗口计算规则请参考：[TA-lib 系列](../themes/TAlib.md)

## 参数

**maType** 计算平均线的方法。是一个0-8范围内的整数。各个整数分别表示：0= [sma](../s/sma.md) , 1= [ema](../e/ema.md) , 2= [wma](../w/wma.md) , 3=
[dema](../d/dema.md) , 4= [tema](../t/tema.md) , 5= [trima](../t/trima.md) , 6= [kama](../k/kama.md) , 7=(mama), 8= [t3](../t/t3.md) 。

## 详情

在给定长度（以元素个数衡量）的滑动窗口内，计算 *X* 的移动平均，计算公式由 *maType* 决定。

