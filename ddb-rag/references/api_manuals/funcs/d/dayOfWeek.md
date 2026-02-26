# dayOfWeek

## 语法

`dayOfWeek(X)`

## 参数

**X** 可以是 DATE, DATETIME, DATEHOUR, TIMESTAMP 或 NANOTIMESTAMP
类型的标量或向量。

## 详情

计算 *X*
是一个星期中的第几天。返回的结果是0到6之间的整数，0表示星期一，1表示星期二，...，6表示星期日。

## 例子

```
dayOfWeek(2012.12.05);
// output
2

dayOfWeek 2013.05.23T12:00:00;
// output
3

dayOfWeek(2014.01.11T23:04:28.113);
// output
5

dayOfWeek(2012.12.05 2012.12.06 2013.01.05);
// output
[2,3,4]
```

