# DStream::reactiveStatelessEngine

## 语法

`DStream::reactiveStatelessEngine(metrics)`

## 详情

创建流计算响应式无状态引擎。参考：[createReactiveStatelessEngine](../c/createReactiveStatelessEngine.md)。

**返回值**：一个 DStream 对象。

## 参数

**metrics** 字典向量，其中的每一个元素都是一个字典，代表数据间的一个依赖关系，每个字典的结构如下：

* “outputName”->productName:metricName
* “formula“-><A\*B>
* “A“->productName:metricName
* “B“->productName:metricName

其中，键值 outputName 对应的 productName 和 metricName 将分别作为输出表的第一列和第二列；键值 A 和 B 对应的
productName 和 metricName 唯一确定了依赖的数据所在位置，既可以是输入表的数据，也可以是输出表中的数据；键值 formula
对应的元代码，用于表示数据间的依赖关系，上例中 outputName = A \* B。

## 例子

```
if (!existsCatalog("orca")) {
	createCatalog("orca")
}
go
use catalog orca

// 如已存在流图，则先销毁该流图
// dropStreamGraph('engine')

g = createStreamGraph('engine')

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

g.source("input", 1000:0, `product`factor`value, [STRING, STRING, DOUBLE])
.reactiveStatelessEngine(metrics)
.sink("output")
g.submit()
go

products = take("product_A", 2)
factors = ["factor1", "factor2"]
values = [1.0, 2.0]
tmp = table(products as product, factors as factor, values as value)
appendOrcaStreamTable("input", tmp)

products = take("product_B", 1)
factors = take("factor1", 1)
values = take(1.0, 1)
tmp = table(products as product, factors as factor, values as value)
appendOrcaStreamTable("input", tmp)

select * from orca_table.output
```

| productName | metricName | metricsResults |
| --- | --- | --- |
| product\_B | value |  |
| product\_C | value |  |
| product\_B | value | 4 |
| product\_C | value |  |

