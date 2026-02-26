# DStream::haSink

## 语法

`DStream::haSink(name, raftGroup, cacheLimit,
[retentionMinutes=1440])`

## 参数

**name** 字符串，指定目标表名。

**raftGroup** 是一个大于1的整数，表示 Raft 组的 ID。

**cacheLimit** 是一个整数，表示高可用流数据表在内存中最多保留多少行。如果 *cacheLimit*
是小于100,000的正整数，它会被自动调整为100,000。

**retentionMinutes** 可选参数，是一个整数，表示保留大小超过 1GB 的 log
文件的时间（从文件的最后修改时间开始计算），单位是分钟。默认值是1440，即一天。

## 详情

将流数据输出到高可用流数据表。

有关最新高可用流数据表的更多信息，请参阅 [haStreamTable](../h/haStreamTable.md)
手册。

**返回值**：DStream 对象。

