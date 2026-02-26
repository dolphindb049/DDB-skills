# isMonthStart

## 语法

`isMonthStart(X)`

## 参数

**X** 可以是 DATE, DATEHOUR, DATETIME, TIMESTAMP 或 NANOTIMESTAMP
类型的标量或向量。

## 详情

判断 *X* 是否为月初第一天。

## 例子

```
isMonthStart(2012.05.01);
// output
true

isMonthStart([2012.05.01,2012.05.02]);
// output
[true,false]
```

相关函数：[isMonthEnd](isMonthEnd.md)

