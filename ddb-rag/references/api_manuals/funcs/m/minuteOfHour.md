# minuteOfHour

## 语法

`minuteOfHour(X)`

## 参数

**X** 可以是 TIME, MINUTE, SECOND, DATETIME, TIMESTAMP, NANOTIME 或
NANOTIMESTAMP 类型的标量或向量。

## 详情

返回 *X* 中的分钟数。

## 例子

```
minuteOfHour(12:32:00);
// output
32

minuteOfHour([2012.06.12T12:30:00,2012.10.28T12:35:00,2013.01.06T12:36:47,2013.04.06T08:02:14]);
// output
[30,35,36,2]
```

相关函数：[dayOfYear](../d/dayOfYear.md), [dayOfMonth](../d/dayOfMonth.md), [quarterOfYear](../q/quarterOfYear.md), [monthOfYear](monthOfYear.md), [weekOfYear](../w/weekOfYear.md), [hourOfDay](../h/hourOfDay.md), [secondOfMinute](../s/secondOfMinute.md), [millisecond](millisecond.md), [microsecond](microsecond.md), [nanosecond](../n/nanosecond.md)

