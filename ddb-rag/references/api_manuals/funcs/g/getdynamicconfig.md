# getDynamicConfig

## 语法

`getDynamicConfig()`

## 参数

无

## 详情

返回一个向量，包含所有可以通过 `setDynamicConfig` 在线修改的配置项名。

## 例子

```
getDynamicConfig();
// output: ["TSDBVectorIndexCacheSize","TSDBCacheEngineSize","dfsChunkNodeHeartBeatTimeout","reservedMemSize","recoveryWorkers","OLAPCacheEngineSize","memLimitOfTempResult","maxMemSize","memLimitOfAllTempResults","maxPartitionNumPerQuery","memLimitOfTaskGroupResult","memLimitOfQueryResult","maxConnections","maxBlockSizeForReservedMemory","TSDBBlockCacheSize","logLevel","enableNullSafeJoin","enableMultiThreadMerge"]
```

**相关信息**

* [setDynamicConfig](../s/setdynamicconfig.html "setDynamicConfig")

