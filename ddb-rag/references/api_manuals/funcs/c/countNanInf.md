# countNanInf

## 语法

`countNanInf(X, [includeNull=false])`

## 参数

**X** 是 DOUBLE 类型 的标量/向量/矩阵。

**includeNull** 是一个布尔值。

## 详情

聚合函数，用于统计 *X* 中 NaN 或 Inf 值的数量。若 *includeNull* 设为 true，NULL 值也会被统计，默认为
false。

相关函数：[isNanInf](../i/isNanInf.md)

