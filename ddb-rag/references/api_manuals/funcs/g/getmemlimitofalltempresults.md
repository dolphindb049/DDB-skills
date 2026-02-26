# getMemLimitOfAllTempResults

## 语法

`getMemLimitOfAllTempResults()`

## 参数

无

## 详情

获取分布式查询操作（例如表连接、GROUP BY、CONTEXT BY、PIVOT BY）产生的临时表可以占用的内存上限。

## 例子

```
getMemLimitOfAllTempResults ()
// output: 3.0
```

相关函数：[setMemLimitOfAllTempResults](../s/setmemlimitofalltempresults.md)

