# isNanInf

## 语法

`isNanInf(X, [includeNull=false])`

## 参数

**X** 是 DOUBLE 类型的标量/向量/矩阵。

**includeNull** 是一个布尔值。

## 详情

检测 *X* 中的每一个元素是否为 NaN 或 Inf。返回与 *X* 等长的布尔类型。若 *includeNull* 设为
true，NULL 值会被视为 Nan 或 Inf，默认为 false。

相关函数：[countNanInf](../c/countNanInf.md)

