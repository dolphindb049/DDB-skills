# getControllerElectionTick

## 语法

`getControllerElectionTick()`

## 参数

无

## 详情

获取控制节点组成的 raft 组的 election tick，即通过 `setRaftElectionTick` 设置的
*tickCount* 或配置项 *raftElectionTick* 的设置值。

相关函数： [setRaftElectionTick](../s/setRaftElectionTick.md), [getRaftElectionTick](getRaftElectionTick.md)

