# createNarrowReactiveStateEngine

## 语法

`createNarrowReactiveStateEngine(name, metrics, metricNames, dummyTable,
outputTable, keyColumn, [filter], [snapshotDir], [snapshotIntervalInMsgCount],
[keepOrder], [keyPurgeFilter], [keyPurgeFreqInSecond=0], [raftGroup],
[outputElapsedMicroseconds=false], [keyCapacity=1024], [parallelism=1],
[outputHandler=NULL], [msgAsTable=false])`

## 详情

创建生成窄表的响应式状态引擎。其计算规则和计算方式与 createReactiveStateEngine
一致，输出形式不同。createReactiveStateEngine 将每次计算的指标输出为一行的不同列，而该引擎则把通过 metricNames
指定指标的计算以窄表的形式输出，即计算结果输出到不同行的相同列。

## 参数

该引擎的的大部分参数和 createReactiveStateEngine 的参数相同，可以参考 createReactiveStateEngine
中的参数说明。这里仅对有区别的参数进行说明。

**metrics** 以元代码的格式表示计算指标，支持输入元组，表示需要输出到 outputTable 中的除 keyColumn
外的输入表中的列或计算指标。注意：这里不要求必须指定除 keyColumn 外的列，但必须指定计算指标，且计算指标必须与 *metricNames*
指定的名称一一对应。

**metricNames** 字符串标量或向量，表示输出到 *outputTable* 中的指标的名称。

**outputTable** 计算结果的输出表，可以是内存表或分布式表。使用
`createNarrowReactiveStateEngine`
函数之前，需要预先设立一个输出表，引擎会将计算结果注入该表。

输出表的各列的顺序如下：

(1) 分组列。根据 *keyColumn* 的设置，输出表的前几列必须和 *keyColumn* 设置的列及其顺序保持一致。

(2) 耗时列。指定 *outputElapsedMicroseconds* = true 时才有。此时需要增加一个 LONG 类型和一个 INT
类型的列，分别用于存储引擎内部每个 batch 的数据耗时（单位：微秒）和记录数。

(3) *metrics* 中指定的除 *metricNames* 指定的计算指标外的列。

(4) *metricNames* 列，仅1列。

(5) 计算结果列，仅1列。

注：

暂不支持指定以下三个参数：*snapshotDir*,*snapshotIntervalInMsgCount* 和
*raftGroup。*

**outputHandler** 一元函数。设置此参数时，引擎计算结束后，不再将计算结果写到输出表，而是会调用此函数处理计算结果。默认值为
NULL，表示仍将结果写到输出表。

**msgAsTable** 布尔标量，表示在设置了参数 outputHandler 时，将引擎的计算结果以表的结构调用函数。默认值为
false，此时将计算结果的每一列作为元素组成元组。

## 例子

下例通过 `createNarrowReactiveStateEngine`
计算累计成交量和移动平均最新价，并将计算结果输出到窄表中，即两个指标的结果输出到同一列。

```
dummy = streamTable(1:0, ["securityID1","securityID2","securityID3","createTime","updateTime","upToDatePrice","qty","value"], [STRING,STRING,STRING,TIMESTAMP,TIMESTAMP,DOUBLE,DOUBLE,INT])
outputTable = streamTable(1:0,["securityID1","securityID2","securityID3","createTime","updateTime","metricNames","factorValue"], [STRING,STRING,STRING, TIMESTAMP,TIMESTAMP,STRING,DOUBLE])
//这里定义计算指标，本例中定义了累计成交量和移动平均最新价两个指标。用户可根据实际需要修改指标。
factor = [<createTime>, <updateTime>,<cumsum(qty)>,<cumavg(upToDatePrice)>]
Narrowtest = createNarrowReactiveStateEngine(name="narrowtest1",metrics=factor,metricNames=["factor1","factor2"],dummyTable=dummy,outputTable=outputTable,keyColumn=["securityID1","securityID2","securityID3"])

num = 5
tmp = table(take("A" + lpad(string(1..4),4,"0"),num) as securityID1,take("CC.HH" + lpad(string(21..34),4,"0"),num) as securityID2,take("FFICE" + lpad(string(13..34),4,"0"),num) as securityID3, 2023.09.01 00:00:00+(1..num) as createTime, 2023.09.01 00:00:00+take(1..num, num).sort() as updateTime,take(rand(100.0,num) join take(int(),30),num) as upToDatePrice,take(take(100.0,num) join take(int(),30),num)+30 as qty,take(1..20 join take(int(),5),num) as value)
Narrowtest.append!(tmp)

select * from outputTable
```

| securityID1 | securityID2 | securityID3 | createTime | updateTime | metricNames | factorValue |
| --- | --- | --- | --- | --- | --- | --- |
| A0001 | CC.HH0021 | FFICE0013 | 2023.09.01T00:00:01.000 | 2023.09.01T00:00:01.000 | factor1 | 131 |
| A0001 | CC.HH0021 | FFICE0013 | 2023.09.01T00:00:01.000 | 2023.09.01T00:00:01.000 | factor2 | 101 |
| A0002 | CC.HH0022 | FFICE0014 | 2023.09.01T00:00:02000 | 2023.09.01T00:00:02.000 | factor1 | 132 |
| A0002 | CC.HH0022 | FFICE0014 | 2023.09.01T00:00:02.000 | 2023.09.01T00:00:02.000 | factor2 | 102 |
| A0003 | CC.HH0023 | FFICE0015 | 2023.09.01T00:00:03.000 | 2023.09.01T00:00:03.000 | factor1 | 133 |
| A0003 | CC.HH0023 | FFICE0015 | 2023.09.01T00:00:03.000 | 2023.09.01T00:00:03.000 | factor2 | 103 |
| A0004 | CC.HH0024 | FFICE0016 | 2023.09.01T00:00:04.000 | 2023.09.01T00:00:04.000 | factor1 | 134 |
| A0004 | CC.HH0024 | FFICE0016 | 2023.09.01T00:00:04.000 | 2023.09.01T00:00:04.000 | factor2 | 105 |
| A0001 | CC.HH0025 | FFICE0017 | 2023.09.01T00:00:05.000 | 2023.09.01T00:00:05.000 | factor1 | 135 |
| A0001 | CC.HH0025 | FFICE0017 | 2023.09.01T00:00:05.000 | 2023.09.01T00:00:05.000 | factor2 | 105 |

**相关信息**

* [addReactiveMetrics](../a/addreactivemetrics.html "addReactiveMetrics")
* [getReactiveMetrics](../g/getreactivemetrics.html "getReactiveMetrics")

