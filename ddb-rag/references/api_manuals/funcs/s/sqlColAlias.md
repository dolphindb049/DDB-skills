# sqlColAlias

## 语法

`sqlColAlias(colDefs, [colNames])`

## 参数

**colDefs** 是给定的元代码；

**colNames** 是表示别名的字符串。

## 详情

使用元代码和可选择的别名来定义一个列。它通常用于计算列。

## 例子

```
sqlColAlias(<x>, `y);
// output
< x as y >

sqlColAlias(<avg(PRC)>, `avgPRC);
// output
< avg(PRC) as avgPRC >

sqlColAlias(<avg(PRC)>);
// output
< avg(PRC) as avg_PRC >
```

