# clearDSCacheNow

## 语法

`clearDSCacheNow(ds)`

## 参数

**ds** 是数据源或数据源列表。

## 详情

函数 `clearDSCacheNow` 立即清除数据源和缓存。

## 例子

```
PTNDB_DIR = "/home/db_testing"
dbName = database(PTNDB_DIR + "/NYSETAQByName")
Trades = dbName.loadTable(`Trades)

ds=sqlDS(<select Time,Exchange,Symbol,Trade_Volume as Vol, Trade_Price as Price from Trades>)
ds.cacheDSNow()        // cache the data immediately
ds.clearDSCacheNow()  // clear the cache immediately
```

