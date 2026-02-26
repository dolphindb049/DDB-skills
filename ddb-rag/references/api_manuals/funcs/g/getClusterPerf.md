# getClusterPerf

## 语法

`getClusterPerf([includeMaster=false])`

## 参数

**includeMaster** 表示获取的节点信息中是否包含控制节点的信息。

## 详情

获取每个节点的多个配置和性能监控度量值。它只能在控制节点上执行。注意：代理节点的 connectionNum
是一个随机值，可以忽略。

返回一个表对象，包含以下几列：

* host：节点的主机名。
* port：节点的端口号。
* site：节点的局域网信息。
* mode：节点的类型。0 表示集群的数据节点，1 表示集群的代理节点，2 表示集群的控制节点，3 表示 single mode 的节点，4
  表示计算节点。
* state：节点是否存活。
* agentSite：当前节点的代理节点信息。
* maxConnections：最多可以从多少个外部 GUI ，API 或其它节点连接到本地节点。
* maxMemSize：当前节点的内存空间上限（单位：GB）。
* workerNum：常规作业的工作线程的数量。默认值是 CPU 的内核数。
* executorNum：本地执行线程的数量。默认值是 CPU 内核数减1。
* connectionNum：连接到本地节点的连接数。
* name：节点别名。
* memoryUsed：节点的内存占用量（单位：字节）。
* memoryAlloc：系统已分配给当前节点的内存（单位：字节）。
* cpuUsage：CPU 使用率。
* avgLoad：CPU 平均负载。
* medLast10QueryTime：前 10 个完成的查询执行所耗费时间的中间值（单位：纳秒）。注意：必须指定 perfMonitoring=1
  才会返回该字段。
* maxLast10QueryTime：前 10 个完成的查询执行所耗费时间的最大值（单位：纳秒）。注意：必须指定 perfMonitoring=1
  才会返回该字段。
* medLast100QueryTime：前 100 个完成的查询执行所耗费时间的中间值（单位：纳秒）。注意：必须指定 perfMonitoring=1
  才会返回该字段。
* maxLast100QueryTime：前100个完成的查询执行所耗费时间的最大值（单位：纳秒）。注意：必须指定 perfMonitoring=1
  才会返回该字段。
* maxRunningQueryTime：当前正在执行的查询的耗费时间的最大值（单位：纳秒）。
* runningJobs：正在执行中的 Job 个数。
* queuedJobs：队列中的 Job 个数。
* runningTasks：正在执行中的 Task 个数。
* queuedTasks：队列中的 Task 个数。
* jobLoad：作业负载。
* diskCapacity：磁盘容量（单位：字节）。
* diskFreeSpace：磁盘剩余空间（单位：字节）。
* diskFreeSpaceRatio：磁盘可用空间占比。
* diskWriteRate：磁盘写速率 （单位：字节/秒）。
* diskReadRate：磁盘读速率（单位：字节/秒）。
* lastMinuteWriteVolume：前一分钟写磁盘容量（单位：字节）。
* lastMinuteReadVolume：前一分钟读磁盘容量（单位：字节）。
* networkSendRate：网络发送速率（单位：字节/秒）。
* networkRecvRate：网络接收速率（单位：字节/秒）。
* lastMinuteNetworkSend：前一分钟网络发送字节数（单位：字节）。
* lastMinuteNetworkRecv：前一分钟网络接收字节数 （单位：字节）。
* publicName：若为控制节点，且配置了 publicName，则显示 publicName；否则显示控制节点所在服务器的
  网卡地址。若为数据节点或代理节点，则显示数据节点或代理节点所在服务器的网卡地址。
* lastMsgLatency：流数据订阅节点最后收到的消息的延时（单位：纳秒）。
* cumMsgLatency：流数据订阅节点所有已接收的消息的平均延时（单位：纳秒）。
* isLeader：是否是 raft 组的 leader，该字段仅在配置了控制节点高可用时才生效。请注意，若 raft 组存在宕机的节点，则该节点的
  isLeader 将返回空值。

## 例子

```
rpc(getControllerAlias(), getClusterPerf)
```

| host | port | site | mode | state | agentSite | maxConnections | maxMemSize | workerNum | executorNum | connectionNum | name | memoryUsed | memoryAlloc | cpuUsage | avgLoad | medLast10QueryTime | maxLast10QueryTime | medLast100QueryTime | maxLast100QueryTime | maxRunningQueryTime | runningJobs | queuedJobs | runningTasks | queuedTasks | jobLoad | diskCapacity | diskFreeSpace | diskFreeSpaceRatio | diskWriteRate | diskReadRate | lastMinuteWriteVolume | lastMinuteReadVolume | networkSendRate | networkRecvRate | lastMinuteNetworkSend | lastMinuteNetworkRecv | publicName | lastMsgLatency | cumMsgLatency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 192.168.1.48 | 8,894 | 192.168.1.48:8894:datanode3 | 0 | 1 | 192.168.1.48:8891:agent1 | 192 | 16 | 16 | 15 | 4 | datanode3 | 9,073,704 | 12,648,448 | 1.0309 | 0.0103 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1,000,068,870,144 | 941,631,864,832 | 0.9416 | 0 | 0 | 1,058 0 | 0 | 0 | 0 | 0 | 0 | 127.0.0.1 | 0 | 0 |
| 192.168.1.48 | 8,895 | 192.168.1.48:8895:datanode4 | 0 | 1 | 192.168.1.48:8891:agent1 | 192 | 16 | 16 | 15 | 4 | datanode4 | 8,862,912 | 9,502,720 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1,000,068,870,144 | 941,631,864,832 | 0.9416 | 0 | 0 | 1,058 0 | 0 | 0 | 0 | 0 | 0 | 127.0.0.1 | 0 | 0 |
| 192.168.1.48 | 8,891 | 192.168.1.48:8891:agent1 | 1 | 1 | 192.168.1.48:8891:agent1 | 32 | 12 | 4 | 15 | 0 | agent1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | 0 | 0 |
| 192.168.1.48 | 8,892 | 192.168.1.48:8892:datanode1 | 0 | 1 | 192.168.1.48:8891:agent1 | 192 | 16 | 16 | 15 | 4 | datanode1 | 8,976,200 | 10,551,296 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1,000,068,870,144 | 941,631,864,832 | 0.9416 | 0 | 0 | 1,058 0 | 0 | 0 | 0 | 0 | 0 | 127.0.0.1 | 0 | 0 |
| 192.168.1.48 | 8,893 | 192.168.1.48:8893:datanode2 | 0 | 1 | 192.168.1.48:8891:agent1 | 192 | 16 | 16 | 15 | 5 | datanode2 | 9,290,232 | 11,599,872 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1,000,068,870,144 | 941,631,864,832 | 0.9416 | 0 | 0 | 1,058 0 | 0 | 0 | 0 | 0 | 0 | 127.0.0.1 | 0 | 0 |

```
rpc(getControllerAlias(), getClusterPerf).keys()
// output
["host","port","site","mode","state","agentSite","maxConnections","maxMemSize","workerNum","executorNum","connectionNum","name","memoryUsed","memoryAlloc","cpuUsage","avgLoad","medLast10QueryTime","maxLast10QueryTime","medLast100QueryTime","maxLast100QueryTime","maxRunningQueryTime","runningJobs","queuedJobs","runningTasks","queuedTasks","jobLoad","diskCapacity","diskFreeSpace","diskFreeSpaceRatio","diskWriteRate","diskReadRate","lastMinuteWriteVolume","lastMinuteReadVolume","networkSendRate","networkRecvRate","lastMinuteNetworkSend","lastMinuteNetworkRecv","publicName","lastMsgLatency","cumMsgLatency"]
```

集群高可用环境下执行：

```
rpc(getControllerAlias(), getClusterPerf,true)
```

| host | port | site | mode | state | agentSite | maxConnections | maxMemSize | workerNum | executorNum | connectionNum | name | memoryUsed | memoryAlloc | cpuUsage | avgLoad | medLast10QueryTime | maxLast10QueryTime | medLast100QueryTime | maxLast100QueryTime | maxRunningQueryTime | runningJobs | queuedJobs | runningTasks | queuedTasks | jobLoad | diskCapacity | diskFreeSpace | diskFreeSpaceRatio | diskWriteRate | diskReadRate | lastMinuteWriteVolume | lastMinuteReadVolume | networkSendRate | networkRecvRate | lastMinuteNetworkSend | lastMinuteNetworkRecv | publicName | lastMsgLatency | cumMsgLatency | isLeader |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 192.168.100.10 | 17,000 | 192.168.100.10:17000:master3 | 2 | 1 |  | 512 | 16 | 64 | 3 | 1 | master3 | 23,449,272 | 24,133,632 | 0.7788 | 0.0037 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4,658 | 2,736 | 102,468 | 59,193 | 78,351 | 8,012,182 | 2,378,846 | 192.198.1.10;172.17.0.1;10.244.5.0;10.244.5.1 | 0 | 0 | false |
| 192.168.100.11 | 17,000 | 192.168.100.11:17000:master2 | 2 | 1 |  | 512 | 16 | 64 | 3 | 2 | master2 | 23,527,872 | 24,133,632 | 11.5625 | 0.3219 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4,670 | 2,785 | 116,733 | 62,402 | 56,160 | 1,366,293 | 1,398,238 | 192.198.1.11;172.17.0.1;10.244.4.0;10.244.4.1 | 0 | 0 | false |
| 192.168.100.12 | 17,000 | 192.168.100.12:17000:master1 | 2 | 1 |  | 512 | 16 | 64 | 3 | 20 | master1 | 25,002,792 | 46,538,752 | 14.0406 | 0.1136 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4,671 | 13,546,528 | 19,964,606 | 53,206 | 56,891 | 22,543,771 | 8,226,278 | 192.198.1.12;172.17.0.1;10.244.3.0;10.244.3.1 | 0 | 0 | true |
| 192.168.100.12 | 17,102 | 192.168.100.12:17102:server19-datanode1 | 0 | 1 | 192.168.100.12:17101:server19-agent1 | 254 | 120 | 5 | 31 | 1 | server19-datanode1 | 23,118,960 | 24,133,632 | 13.928 | 0.1136 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 17,790,585,659,392 | 16,826,060,464,128 | 0.9458 | 0 | 4,687 | 1,289 | 23,477 | 44,197 | 55,104 | 352,258 | 6,163,159 | 192.198.1.12;172.17.0.1;10.244.3.0;10.244.3.1 | 0 | 0 |  |
| 192.168.100.11 | 17,102 | 192.168.100.11:17102:server18-datanode1 | 0 | 1 | 192.168.100.11:17101:server18-agent1 | 254 | 120 | 5 | 31 | 1 | server18-datanode1 | 23,111,912 | 24,133,632 | 14.1066 | 0.3219 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 17,790,585,659,392 | 16,714,392,956,928 | 0.9395 | 0 | 4,698 | 1,989 | 23,530 | 40,896 | 50,706 | 243,008 | 250,727 | 192.198.1.11;172.17.0.1;10.244.4.0;10.244.4.1 | 0 | 0 |  |
| 192.168.100.11 | 17,101 | 192.168.100.11:17101:server18-agent1 | 1 | 1 | 192.168.100.11:17101:server18-agent1 | 304 | 4 | 4 | 63 | 0 | server18-agent1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 192.198.1.11;172.17.0.1;10.244.4.0;10.244.4.1 | 0 | 0 |  |
| 192.168.100.10 | 17,102 | 192.168.100.10:17102:server17-datanode1 | 0 | 1 | 192.168.100.10:17101:server17-agent1 | 254 | 120 | 5 | 31 | 1 | server17-datanode1 | 40,872,496 | 52,445,184 | 0.7788 | 0.0037 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 53,783,736,754,176 | 50,336,934,432,768 | 0.9359 | 0 | 4,699 | 13,900,218 | 18,835 | 118,935 | 109,862 | 6,170,512 | 408,018 | 192.198.1.10;172.17.0.1;10.244.5.0;10.244.5.1 | 0 | 0 |  |
| 192.168.100.12 | 17,101 | 192.168.100.12:17101:server19-agent1 | 1 | 1 | 192.168.100.12:17101:server19-agent1 | 304 | 4 | 4 | 63 | 0 | server19-agent1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 192.198.1.12;172.17.0.1;10.244.3.0;10.244.3.1 | 0 | 0 |  |
| 192.168.100.10 | 17,101 | 192.168.100.10:17101:server17-agent1 | 1 | 1 | 192.168.100.10:17101:server17-agent1 | 304 | 4 | 4 | 63 | 0 | server17-agent1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 192.198.1.10;172.17.0.1;10.244.5.0;10.244.5.1 | 0 | 0 |  |

