# quarterOfYear

## 语法

`quarterOfYear(X)`

## 参数

**X** 可以是 DATE, MONTH, DATETIME, TIMESTAMP 或 NANOTIMESTAMP
类型的标量或向量。

## 详情

计算X在当年的第几个季度。返回的结果是整型。

## 例子

```
quarterOfYear(2012.07.02);
// output
3

quarterOfYear([2012.06.12T12:30:00,2012.10.28T12:35:00,2013.01.06T12:36:47,2013.04.06T08:02:14]);
// output
[2,4,1,2]
```

相关函数：[dayOfYear](../d/dayOfYear.md), [dayOfMonth](../d/dayOfMonth.md), [monthOfYear](../m/monthOfYear.md), [weekOfYear](../w/weekOfYear.md), [hourOfDay](../h/hourOfDay.md), [minuteOfHour](../m/minuteOfHour.md), [secondOfMinute](../s/secondOfMinute.md), [millisecond](../m/millisecond.md), [microsecond](../m/microsecond.md), [nanosecond](../n/nanosecond.md)

