# getStreamingLeader

## 语法

`getStreamingLeader(groupId)`

## 参数

**groupId** 是一个整数，表示流数据 Raft 组的 ID

## 详情

获取流数据 Raft 组中的 Leader。

## 例子

```
getStreamingLeader(11);
// output

DFS_NODE2
```

