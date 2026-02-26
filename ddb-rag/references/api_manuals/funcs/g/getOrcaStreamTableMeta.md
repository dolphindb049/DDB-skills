# getOrcaStreamTableMeta

## 语法

`getOrcaStreamTableMeta([name])`

## 参数

**name** 可选参数，表示持久化共享流表的名称。字符串标量，可以传入完整的流表全限定名（如
trading.orca\_graph.trades）；也可以仅提供流表名（如 trades），系统会根据当前的 catalog 设置自动补全为对应的全限定名

## 详情

返回 Orca 中指定流表的元信息。如果未指定 *name*，则返回 Orca 中所有流表的元信息。

返回结果为一个表，包含以下字段：

* id：流表 id
* fqn：该流表的全限定名
* site：流表所在节点的名称。
* graphRefs：引用此流表的所有流图的 id 列表
* raftGroupId：高可用流表所属的 raft 组 id，非高可用流表返回 0

## 例子

```
getOrcaStreamTableMeta("trade1") // name 是流表名称
getOrcaStreamTableMeta("catalog1.orca_table.trade1") // name 是全限定名
```

