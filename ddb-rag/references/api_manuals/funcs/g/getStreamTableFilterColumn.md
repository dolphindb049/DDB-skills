# getStreamTableFilterColumn

## 语法

`getStreamTableFilterColumn(streamTable)`

## 参数

**streamTable** 是流数据表。

## 详情

返回由函数 [setStreamTableFilterColumn](../s/setStreamTableFilterColumn.md) 指定的流数据表中过滤列的名称。

## 例子

```
share streamTable(10000:0,`time`symbol`price, [TIMESTAMP,SYMBOL,INT]) as trades
setStreamTableFilterColumn(trades, `symbol)
trades_1=table(10000:0,`time`symbol`price, [TIMESTAMP,SYMBOL,INT])
filter=symbol(`IBM`GOOG)
subscribeTable(tableName=`trades, actionName=`trades_1, handler=append!{trades_1}, msgAsTable=true, filter=filter);

n=100
time=take(2018.01.01T09:30:00.000,n)
symbol=take((`IBM`GOOG`AAPL`C`BABA),n)
price=1..n

t=table(time,symbol,price)
trades.append!(t)

// 获取流数据表trades由setStreamTableFilterColumn函数指定的过滤列名
getStreamTableFilterColumn(trades) ;
// output
symbol
```

