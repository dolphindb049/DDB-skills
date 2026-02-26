# StreamGraph::haSource

## 语法

`StreamGraph::haSource(name, capacity:size, colNames, colTypes, raftGroup,
cacheLimit, [retentionMinutes=1440])`

## 详情

创建一个高可用流数据表。参考 [haStreamTable](../h/haStreamTable.md)。

**返回值**：一个 DStream 对象。

## 参数

**name** 表示持久化共享流表的名称。字符串标量，可以传入完整的流表全限定名（如
trading.orca\_graph.trades）；也可以仅提供流表名（如 trades），系统会根据当前的 catalog 设置自动补全为对应的全限定名。

**capacity** 是正整数，表示建表时系统为该表分配的内存（以记录数为单位）。当记录数超过
*capacity* 时，系统首先会分配 *capacity*
1.2~2倍的新的内存空间，然后复制数据到新的内存空间，最后释放原来的内存。对于规模较大的表，此类操作的内存占用会很高。因此，建议建表时预先分配一个合理的
*capacity*。

**size** 是整数，表示该表新建时的行数。若 *size* =0，创建一个空表。 若
*size*>0，则建立一个只包含 size 条记录的表，记录初始值如下：

* BOOL 类型默认值为 false；
* 数值类型、时间类型、IPADDR、COMPLEX、POINT 的默认值为 0；
* Literal, INT128 类型的默认值为 NULL。

注： 如果
*colTypes* 指定为数组向量， *size* 必须为0。

**colNames** 是一个向量，表示列名。

**colTypes**
是一个向量，表示每列的数据类型，支持数组向量类型和元组（ANY）类型。可使用表示数据类型的系统保留字或相应的字符串。

**raftGroup** 是一个大于1的整数，表示 Raft 组的 ID。

**cacheLimit** 是一个整数，表示高可用流数据表在内存中最多保留多少行。如果 *cacheLimit*
是小于100,000的正整数，它会被自动调整为100,000。

**retentionMinutes** 可选参数，是一个整数，表示保留大小超过 1GB 的 log
文件的时间（从文件的最后修改时间开始计算），单位是分钟。默认值是1440，即一天。

## 例子

```
if (!existsCatalog("orca")) {
	createCatalog("orca")
}
go
use catalog orca

g = createStreamGraph("indicators")
g.haSource("ha_table", 1:0, `time`symbol`price`volume, [DATETIME,SYMBOL,DOUBLE,LONG], 3, 50000)
```

