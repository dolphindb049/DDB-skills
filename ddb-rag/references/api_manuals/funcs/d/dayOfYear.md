# dayOfYear

## 语法

`dayOfYear(X)`

## 参数

**X** 可以是 DATE, DATETIME, TIMESTAMP 或 NANOTIMESTAMP
类型的标量或向量。

## 详情

计算 *X* 是当年中的第几天。返回的结果是整型。

## 例子

```
dayOfYear(2011.01.01);
// output
1

dayOfYear([2011.12.31,2012.12.31]);
// output
[365,366]

dayOfYear([2012.06.12T12:30:00,2012.07.12T12:35:00]);
// output
[164,194]
```

相关函数：[dayOfMonth](dayOfMonth.md), [quarterOfYear](../q/quarterOfYear.md), [monthOfYear](../m/monthOfYear.md), [weekOfYear](../w/weekOfYear.md), [hourOfDay](../h/hourOfDay.md), [minuteOfHour](../m/minuteOfHour.md), [secondOfMinute](../s/secondOfMinute.md), [millisecond](../m/millisecond.md), [microsecond](../m/microsecond.md), [nanosecond](../n/nanosecond.md)

