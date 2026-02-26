# getTSDBCacheEngineSize

## 语法

`getTSDBCacheEngineSize()`

## 参数

无

## 详情

返回一个 LONG 类型数据，表示 TSDB 引擎 Cache Engine 允许使用的内存上限（单位为字节）。

**首发版本**：2.00.4

## 例子

```
setTSDBCacheEngineSize(0.5)
getTSDBCacheEngineSize()
// output
536870912
```

相关函数： [setTSDBCacheEngineSize](../s/setTSDBCacheEngineSize.md)

