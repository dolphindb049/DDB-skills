# deleteChunkMetaOnMasterById

## 语法

`deleteChunkMetaOnMasterById(chunkPath, chunkId)`

## 参数

**chunkPath** 一个字符串，表示需要删除的 chunk 的路径。

**chunkId** 一个字符串，表示需要删除的 chunk 的 ID。

## 详情

根据 chunk 的路径和 ID，删除控制节点上该 chunk 的元数据。

该函数只能由 admin 在控制节点执行。

## 例子

```
deleteChunkMetaOnMasterById(chunkPath="/olap_value/8/40o", chunkId="11d45d2d-a995-7c97-c041-32362f3400d7")
```

