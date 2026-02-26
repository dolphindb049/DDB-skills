# dayOfMonth

## 语法

`dayOfMonth(X)`

## 参数

**X** 可以是 DATE, DATETIME, TIMESTAMP 或 NANOTIMESTAMP
类型的标量或向量。

## 详情

计算 *X* 在当月的第几天。

## 例子

```
dayOfMonth(2011.01.01);
// output
1

dayOfMonth([2012.06.12T12:30:00,2012.07.28T12:35:00]);
// output
[12,28]
```

相关函数：[dayOfYear](dayOfYear.md), [quarterOfYear](../q/quarterOfYear.md), [monthOfYear](../m/monthOfYear.md), [weekOfYear](../w/weekOfYear.md), [hourOfDay](../h/hourOfDay.md), [minuteOfHour](../m/minuteOfHour.md), [secondOfMinute](../s/secondOfMinute.md), [millisecond](../m/millisecond.md), [microsecond](../m/microsecond.md), [nanosecond](../n/nanosecond.md)

