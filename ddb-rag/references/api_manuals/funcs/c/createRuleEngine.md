# createRuleEngine

## 语法

`createRuleEngine(name, ruleSets, dummyTable, outputColumns, outputTable,
[policy], [ruleSetColumn], [callback])`

## 详情

创建一个规则引擎，支持设置一个包含多个规则的规则集。数据流入引擎时，会根据某一列的值，决定使用规则集中的哪一条规则对此数据进行检测。引擎的规则可以动态增加、删除、修改。例如可以按照维度设置不同的检测规则，实现风控规则的配置。

与异常检测引擎（createAnomalyDetectionEngine）相比：

* 规则引擎是无状态引擎；异常检测引擎是有状态的。
* 规则引擎可以对不同数据，采用不同的检查规则；异常检测引擎会对所有数据以相同的规则进行检测。
* 规则引擎可以动态调整检测规则，包括增加、删除和修改；异常检测引擎创建后无法修改。
* 规则引擎支持设置回调函数，用户可根据检测结果进行相应处理；异常检测引擎不支持设置回调函数。

## 参数

**name** 是一个字符串，表示引擎名。

**ruleSets** 是一个字典，表示规则集。字典的 key 是 STRING 或 INT 类型，value
是一个包含元代码的元组。如果 key 为NULL，表示此条为默认规则。一个规则集必须包含默认规则。

**dummyTable** 一个表对象，和订阅的流数据表的 schema 一致，可以含有数据，亦可为空表。

**outputColumns** 一个 STRING 类型向量，表示输入表中需要保留到输出表的列。

**outputTable** 是一个表对象，表示输出表，可以是内存表或者分布式表。其结构为 ***outputColumns***
指示的列，以及一列规则检查的结果列。当参数 **policy** 设置为 "shortcut" 时，最后一列的数据类型为 INT；否则，数据类型为 BOOL
类型。

**policy** 是一个字符串标量，表示规则检查策略。可取以下值：

* "shortcut" 是默认值，代表短路逻辑。当检查到任一规则不符合（该规则的计算结果为 false）时，返回对应的 index ，index 从
  0 开始；否则返回 NULL。
* "all" 检查全部规则，返回一个 BOOL 类型的数组向量，其元素的布尔值是按照规则集 key 对应的规则执行的结果。

**ruleSetColumn** 是一个 STRING
类型标量，为输入表的某一列名，如果没有定义或者输入数据中的该列数据没有命中任何一个规则集，则使用默认规则。

**callback**
是一个函数，其参数为一个表，是引擎输出的一行。若设置此参数，引擎每处理一行，在将引擎处理结果输出到输出表的同时，会将该结果作为入参调用此函数。此参数未设置时，仅将引擎处理结果输出到输出表。

## 例子

首先

```
// 设置规则集
x = [1, 2, NULL]
y = [ [ < value > 1 > ], [ < price < 2 >, < price > 6 > ], [ < value*price > 10 > ] ]
ruleSets = dict(x, y)

// 创建分布式表，用于回调函数写入数据
db = database("dfs://temp", VALUE, 1..3)
t1 = table(1:0, `sym`value`price, [INT,DOUBLE,DOUBLE])
pt = db.createPartitionedTable(t1,`pt,`sym)

// 创建回调函数，根据检测结果，将数据写入分布式表
def writeBack(result){
    if(result.rule[0]==false){
        temp = select sym,value,price from result
        loadTable("dfs://temp",`pt).append!(temp)
    }
}

// 创建规则引擎
names = `sym`value`price`quantity
types = [INT, DOUBLE, DOUBLE, DOUBLE]
dummy = table(1:0, names, types)
outputNames = `sym`value`price`rule
outputTypes = [INT, DOUBLE, DOUBLE, BOOL[]]
outputTable = table(10:0, outputNames, outputTypes)
test = createRuleEngine(name="ruleEngineTest", ruleSets=ruleSets, dummyTable=dummy, outputColumns=["sym","value","price"], outputTable=outputTable, policy="all", ruleSetColumn="sym", callback=writeBack)

// 分别插入两条 sym=1 的数据，此时会根据规则集 ruleSets 中 key=1 对应的规则，即 value >1 来检测这两条数据
test.append!(table(1 as sym, 0 as value, 2 as price, 3 as quantity))
test.append!(table(1 as sym, 2 as value, 2 as price, 3 as quantity))

// 分别插入三条 sym=2 的数据，此时会根据规则集 ruleSets 中 key=2 对应的规则，即 price < 2 和 price > 6 来检测这三条数据
test.append!(table(2 as sym, 2 as value, 0 as price, 3 as quantity))
test.append!(table(2 as sym, 2 as value, 4 as price, 3 as quantity))
test.append!(table(2 as sym, 2 as value, 8 as price, 3 as quantity))

// 插入两条 sym=3 的数据，由于规则集 ruleSets 只设置了键值为 1 和 2 的规则，此时会根据规则集中 key=NULL 对应的规则，即 value*price > 10 来检测这两条数据
test.append!(table(3 as sym, 2 as value, 3 as price, 3 as quantity))
test.append!(table(3 as sym, 2 as value, 6 as price, 3 as quantity))

```

此时的输出表 outputTable 内容如下

| sym | value | price | rule |
| --- | --- | --- | --- |
| 1 | 0 | 2 | [false] |
| 1 | 2 | 2 | [true] |
| 2 | 2 | 0 | [true,false] |
| 2 | 2 | 4 | [false,false] |
| 2 | 2 | 8 | [false,true] |
| 3 | 2 | 3 | [false] |
| 3 | 2 | 6 | [true] |

此时，由回调函数向分布式表 dfs://temp/pt
中写入的数据可通过以下语句查看

```
select * from loadTable("dfs://temp","pt")
```

| sym | value | price |
| --- | --- | --- |
| 1 | 0 | 2 |
| 2 | 2 | 4 |
| 2 | 2 | 8 |
| 3 | 2 | 3 |

**相关信息**

* [updateRule](../u/updateRule.html "updateRule")
* [deleteRule](../d/deleteRule.html "deleteRule")
* [getRules](../g/getrules.html "getRules")

