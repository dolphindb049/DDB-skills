# DStream::parallelize

## 语法

`DStream::parallelize(columnName, count)`

## 参数

**columnName** 字符串，指定分区列。

**count** 整数，指定并行度。

## 详情

基于指定分区列对流数据进行哈希分区，生成多个并行的 DStream 处理分支。

注意：`DStream::parallelize` 和 `DStream::sync`
接口必须同时调用。

## 例子

基于 symbol 列拆分 4 个分区，分别执行计算任务：

```
use catalog test

g = createStreamGraph("graph")
g.source("trade", 1024:0, `symbol`datetime`price`volume, [SYMBOL, TIMESTAMP,DOUBLE, INT])
  .parallelize("symbol", 4)
  .timeSeriesEngine(60*1000, 60*1000, <[first(price),max(price),min(price),last(price),sum(volume)]>, "datetime", false, "symbol")
  .reactiveStateEngine(<[datetime, first_price, max_price, min_price, last_price, sum_volume, mmax(max_price, 5), mavg(sum_volume, 5)]>, `symbol)
  .sync()
  .sink("output")
g.submit()
```

