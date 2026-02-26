# getRaftElectionTick

## 语法

`getRaftElectionTick(groupId)`

## 参数

**groupId** 是一个正整数，表示 raft 组的 ID，目前只能是1，表示控制节点组成的 raft 组 ID。

## 详情

获取 group ID 对应的 raft 组当前有效的 election tick，即通过 `setRaftElectionTick`
设置的 *tickCount* 或配置项 *raftElectionTick* 的设置值。

相关函数： [setRaftElectionTick](../s/setRaftElectionTick.md), [getControllerElectionTick](getControllerElectionTick.md)

