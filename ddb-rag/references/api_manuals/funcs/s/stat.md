# stat

## 语法

`stat(X)`

## 参数

**X** 可以是向量或矩阵。

## 详情

返回一个字典，它包含了 *X* 的统计信息，有平均值、最大值、最小值、计数、中位数和标准差。

## 例子

```
x=5 7 4 3 2 1 7 8 9 NULL;

stat(x);
// output
Median->5
Avg->5.111111
Min->1
Stdev->2.803767
Count->9
Size->10
Name->x
Max->9

stats = stat(x);
stats[`Avg];
// output
5.111111
```

