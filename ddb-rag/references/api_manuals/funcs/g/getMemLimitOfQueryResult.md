# getMemLimitOfQueryResult

## 语法

`getMemLimitOfQueryResult()`

## 参数

无

## 详情

获取单次查询结果占用的内存上限（单位为字节），返回一个 DOUBLE 类型数据。

## 例子

```
setMemLimitOfQueryResult(0.2)
getMemLimitOfQueryResult() / 1024 / 1024 / 1024
// output
0.2
```

相关函数：[setMemLimitOfQueryResult](../s/setMemLimitOfQueryResult.md)

