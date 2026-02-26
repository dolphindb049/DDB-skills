# getStreamingStat

## 语法

`getStreamingStat()`

## 参数

无

## 详情

监控流计算的状态。返回的结果是一个字典，包含以下表：

* 表 pubConns
  监控本地发布节点和它的所有订阅节点之间的连接状态。每一行表示一个订阅节点。它包含以下列：

  | 列名 | 含义 |
  | --- | --- |
  | client | 订阅节点的 IP 地址和端口号 |
  | queueDepthLimit | 发布节点上的消息队列深度的上限 |
  | queueDepth | 发布节点上的当前消息队列深度 |
  | tables | 发布节点上所有的共享流数据表 |
* 表 subConns 监控本地订阅节点和发布节点之间的连接状态。每一行表示一个发布节点。它包含以下列：

  | 列名 | 含义 |
  | --- | --- |
  | publisher | 发布节点的别名 |
  | cumMsgCount | 已经接收到的消息数量 |
  | cumMsgLatency | 所有已接收的消息的平均延迟 |
  | LastMsgLatency | 最后接收到的消息的延迟 |
  | lastUpdate | 最后接收到消息的时间 |

* 表 pubTables 监控流数据表状态。每一行表示一个流数据表的信息。它包含以下列：

  | 列名 | 含义 |
  | --- | --- |
  | tableName | 发布的流数据表名 |
  | subscriber | 订阅端的 ip 和端口信息 |
  | msgOffset | 已经发布的最后一条数据在总数据中的偏移量 |
  | actions | 订阅任务的名称 |

  上表中的延迟表示从消息到达发布节点的消息队列开始，到消息到达订阅节点的消息队列所耗费的时间。
* 表 persistWorkers 监控负责持久化流数据表的工作线程的状态。它包含以下列：

  | 列名 | 含义 |
  | --- | --- |
  | workerId | 线程 ID |
  | queueDepthLimit | 持久化的消息队列深度的上限 |
  | queueDepth | 持久化的当前消息队列深度 |
  | tables | 已经持久化的流数据表 |
* 表 subWorkers 监控订阅节点的工作线程的状态。工作线程状态信息会按照 topic
  来展示。它包含以下列：

  | 列名 | 含义 |
  | --- | --- |
  | workerId | 线程 ID。若此列为空，代表该订阅尚未收到数据。 |
  | topics | 订阅主题 |
  | type | 当前订阅节点的订阅方式：UDP 组播订阅（udp）或 TCP 订阅（tcp） |
  | queueDepthLimit | 订阅节点上的消息队列深度的上限 |
  | queueDepth | 订阅节点上的当前消息队列深度 |
  | processedMsgCount | 已经处理的消息数 |
  | lastMsgId | 最后一条消息的 ID |
  | failedMsgCount | 处理失败的消息数 |
  | lastFailedMsgId | 最后一条错误消息的 ID |
  | lastFailedTimestamp | 最后一条错误消息发生的时间 |
  | lastErrMsg | 最后一条错误消息的信息 |
  | msgAsTable | 布尔值，表示订阅的数据是否为表。true 表示订阅的数据为表；false 表示订阅的数据是由列组成的元组。 |
  | batchSize | handler 批量处理的消息数 |
  | throttle | 数值类型，单位为毫秒。表示继上次 handler 处理消息之后，若 batchSize 条件一直未达到，多久后再次处理消息 |
  | hash | 非负整数，指定某个订阅线程处理进来的消息 |
  | filter | 流数据表指定的过滤列 |
  | persistOffset | 布尔值，表示是否持久化保存最新一条已经处理的订阅数据的偏移量 |
  | timeTrigger | 布尔值，若为 true，表示即使没有新的消息进入，handler 也会在 throttle 参数所设定的时间间隔被触发 |
  | handlerNeedMsgId | 布尔值，默认值为 false。若为 true，handler 必须支持两个参数：msgBody，msgId |
  | raftGroup | 高可用下 Raft 组的 ID |
* 表 udpPubTables 用于监控流数据表进行 UDP 组播发布的状态。它包含以下列：

  | 列名 | 含义 |
  | --- | --- |
  | tableName | 发布的流数据表名 |
  | channel | 发布的 UDP 组播地址 |
  | msgOffset | 已经发布的最后一条数据在总数据中的偏移量 |
  | actions | 订阅该发布表的所有订阅任务名称 |
  | subNum | 订阅该发布表的所有订阅数量 |

## 例子

```
getStreamingStat().pubConns;
getStreamingStat().subConns;
getStreamingStat().pubTables;
getStreamingStat().persistWorkers;
getStreamingStat().subWorkers;
getStreamingStat().udpPubTables
```

