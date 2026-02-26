# nanosecond

## 语法

`nanosecond(X)`

## 参数

**X** 可以是 TIME, TIMESTAMP, NANOTIME 或 NANOTIMESTAMP
类型的标量或向量。

## 详情

返回 *X* 中的纳秒数。

## 例子

```
nanosecond(13:30:10.008);
// output
8000000

nanosecond([2012.12.03 01:22:01.999999999, 2012.12.03 01:25:08.000000234]);
// output
[999999999,234]
```

相关函数：[dayOfYear](../d/dayOfYear.md), [dayOfMonth](../d/dayOfMonth.md), [quarterOfYear](../q/quarterOfYear.md), [monthOfYear](../m/monthOfYear.md), [weekOfYear](../w/weekOfYear.md), [hourOfDay](../h/hourOfDay.md), [minuteOfHour](../m/minuteOfHour.md), [secondOfMinute](../s/secondOfMinute.md), [millisecond](../m/millisecond.md), [microsecond](../m/microsecond.md)

