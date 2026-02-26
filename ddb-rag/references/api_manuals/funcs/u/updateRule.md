# updateRule

## 语法

`updateRule(engineName, key, rules)`

## 详情

如果此规则引擎中存在指定的规则 *key*，则修改其 value 为输入参数 *rules*。

如果此规则引擎中不存在这个规则 *key*，则向其增加此规则 *key* 及其 *rules*。

如果执行成功，返回 true，否则返回false。

## 参数

**engineName** 是一个字符串，表示引擎名。

**key** 是 STRING 或 INT 类型的标量，表示要更新的规则对应的 key 。

**rules** 是一个元代码元组，表示要更新的规则对应的 value。

## 例子

```
// 设置规则集，并创建规则引擎
x = [1, 2, NULL]
y = [ [ < value>1 > ], [ < price<2 >, < price>6 > ], [ < value*price>10 > ] ]
ruleSets = dict(x, y)
names = `sym`value`price`quantity
types = [INT, DOUBLE, DOUBLE, DOUBLE]
dummy = table(10:0, names, types)
outputNames = `sym`value`price`rule
outputTypes = [INT, DOUBLE, DOUBLE, BOOL[]]
outputTable = table(10:0, outputNames, outputTypes)
test = createRuleEngine(name="ruleEngineTest", ruleSets=ruleSets, dummyTable=dummy, outputColumns=["sym","value","price"], outputTable=outputTable, policy="all", ruleSetColumn="sym")

// 修改规则前
test.append!(table(1 as sym, 0 as value, 2 as price, 3 as quantity))
test.append!(table(3 as sym, 6 as value, 1 as price, 3 as quantity))

// 将 sym=1 对应的规则修改为 value >=0
updateRule("ruleEngineTest", 1, [ <value >= 0>])
test.append!(table(1 as sym, 0 as value, 2 as price, 3 as quantity))

// 增加 sym=3 对应的规则为 value > 5
updateRule("ruleEngineTest",3,[<value>5>])
test.append!(table(3 as sym, 6 as value, 1 as price, 3 as quantity))

```

此时的输出表 outputTable 内容如下

表 1. outputTable

| sym | value | price | rule |
| --- | --- | --- | --- |
| 1 | 0 | 2 | [false] |
| 3 | 6 | 1 | [false] |
| 1 | 0 | 2 | [true] |
| 3 | 6 | 1 | [true] |

**相关信息**

* [createRuleEngine](../c/createRuleEngine.html "createRuleEngine")
* [deleteRule](../d/deleteRule.html "deleteRule")

