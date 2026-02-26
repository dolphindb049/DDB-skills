# createReactiveStatelessEngine

## 语法

`createReactiveStatelessEngine(name, metrics, outputTable)`

## 详情

很多时候，数据之间具有很强的依赖关系，某些数据可能依赖于其他数据的最新值。每当所依赖的数据有更新时，希望这些数据可以同步更新。应对此场景，可以使用响应式无状态引擎。

创建一个响应式无状态引擎。该引擎可以定义依赖关系，每当所依赖的数据注入，便会根据最新的所依赖的数据计算出最新结果，将其输出到输出表。

返回一个表对象，向该表写入数据意味着将数据注入引擎。

该表的结构如下

| name | typeString |
| --- | --- |
| productName | STRING |
| metricName | STRING |
| value | DOUBLE |

## 计算规则

引擎每有一批数据注入，会根据参数 metrics
中定义的依赖关系，将任何直接依赖或间接依赖这批数据的数据输出，每次输出的条数等于直接或间接依赖这批数据的变量个数。即使这个变量的值没有改变，也会输出。

## 参数

**name** 字符串标量，表示引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**metrics** 字典向量，其中的每一个元素都是一个字典，代表数据间的一个依赖关系，每个字典的结构如下：

* “outputName”->productName:metricName
* “formula“-><A\*B>
* “A“->productName:metricName
* “B“->productName:metricName

其中，键值 outputName 对应的 productName 和 metricName 将分别作为输出表的第一列和第二列；键值 A 和 B 对应的
productName 和 metricName 唯一确定了依赖的数据所在位置，既可以是输入表的数据，也可以是输出表中的数据；键值 formula
对应的元代码，用于表示数据间的依赖关系，上例中 outputName = A \* B。

**outputTable** 输出表，必须为以下结构：

* productName，可以为 STRING 或 SYMBOL 类型。
* metricName，可以为 STRING 或 SYMBOL 类型。
* 计算所得指标的值，即 metrics 中 formula 计算得到的结果，可以为 DOUBLE 或 FLOAT 类型。

## 例子

现有一个窄表，表中信息如下

| productName | metricName | value |
| --- | --- | --- |
| product\_A | factor1 | 1 |
| product\_A | factor2 | 2 |
| product\_B | factor1 | 1 |
| product\_B | value | 4 |
| product\_C | factor1 | 2 |
| product\_C | value | 8 |

上表中，product\_A:factor1, product\_A:factor2, product\_B:factor1, product\_C:factor1
完全由外部输入决定；一些数据依赖其他数据的值
product\_B:value=product\_A:factor1+product\_A:factor2+product\_B:factor1，product\_C:value=product\_B:value\*product\_C:factor1

根据以上信息，通过以下脚本创建引擎

```
// 创建输出表
names = `product`metric`value
types = [STRING, STRING, DOUBLE]
outputTable = table(1:0, names, types)

// 创建 metrics 描述数据间的依赖关系
metrics = array(ANY, 0, 0)
metric1 = dict(STRING,ANY)
// 依赖关系 product_B:value=product_A:factor1+product_A:factor2+product_B:factor1
metric1["outputName"] = `product_B:`value
metric1["formula"] = <A+B+C>
metric1["A"] = `product_A:`factor1
metric1["B"] = `product_A:`factor2
metric1["C"] = `product_B:`factor1
metrics.append!(metric1)
// 依赖关系 product_C:value=product_B:value*product_C:factor1
metric2 = dict(STRING, ANY)
metric2["outputName"] =`product_C:`value
metric2["formula"] = <A*B>
metric2["A"] = `product_B:`value
metric2["B"] = `product_C:`factor1
metrics.append!(metric2)

// 创建引擎
engine1 = createReactiveStatelessEngine("engine1", metrics, outputTable)
```

每次插入数据，无论插入的数据量有多大，都只会返回一次。

第一次插入2条数据，此时，两个依赖关系所需的数据尚不完整，无法计算得到需要的结果，所以输出表中对应值为空。

```
insert into engine1 values(["product_A","product_A"],["factor1","factor2"],[1,2])
outputTable
```

| product | metric | value |
| --- | --- | --- |
| product\_B | value |  |
| product\_C | value |  |

第二次插入1条数据，此时，第一个依赖关系所需数据已经完整，故得到结果，第二个依赖关系所需数据仍不完整，对应值为空。

```
insert into engine1 values("product_B","factor1",1)
outputTable
```

| product | metric | value |
| --- | --- | --- |
| product\_B | value |  |
| product\_C | value |  |
| product\_B | value | 4 |
| product\_C | value |  |

第三次插入1条数据，此时，第二个依赖关系所需数据完整，输出对应结果。

```
insert into engine1 values("product_C","factor1",2)
outputTable
```

| product | metric | value |
| --- | --- | --- |
| product\_B | value |  |
| product\_C | value |  |
| product\_B | value | 4 |
| product\_C | value |  |
| product\_C | value | 8 |

第四次插入1条数据，此时，由于数据被修改，依赖此数据的相关数据均会受到影响，并将更新后的结果输出。

```
insert into engine1 values("product_C","factor1",3)
outputTable
```

| product | metric | value |
| --- | --- | --- |
| product\_B | value |  |
| product\_C | value |  |
| product\_B | value | 4 |
| product\_C | value |  |
| product\_C | value | 8 |
| product\_C | value | 12 |

注意，数据更新后，即使依赖此数据的相关数据的值最终没有变化，也会将最新结果输出

```
insert into engine1 values(["product_A","product_A"],["factor1","factor2"],[2,1])
outputTable
```

| product | metric | value |
| --- | --- | --- |
| product\_B | value |  |
| product\_C | value |  |
| product\_B | value | 4 |
| product\_C | value |  |
| product\_C | value | 8 |
| product\_C | value | 12 |
| product\_B | value | 4 |
| product\_C | value | 12 |

如果只想获得变量的最新状态，可以创建键值表作为输出表

```
kt = keyedTable(`product`metric, 1:0, `product`metric`value, [STRING, STRING, DOUBLE])
```

