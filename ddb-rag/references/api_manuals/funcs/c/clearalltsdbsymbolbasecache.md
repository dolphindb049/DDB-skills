# clearAllTSDBSymbolBaseCache

## 语法

`clearAllTSDBSymbolBaseCache()`

## 参数

无

## 详情

清除缓存中所有未被使用的 symbolBase。其中，未被使用的 symbolBase 是指其对应分区的数据不在 Cache
Engine 中，也不在执行的任何事务中。

## 例子

```
clearAllTSDBSymbolBaseCache();
```

