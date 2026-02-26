# StreamGraph::name

## 语法

`StreamGraph::name`

## 详情

获取流图的全限定名（Fully Qualified Name, FQN）。

**返回值：**STRING 类型

## 例子

获取 [StreamGraph::submit](StreamGraph_submit.md) 函数文档的例子中所提交流图 g
的全限定名：

```
g.name()
// Output: 'demo.orca_graph.indicators'
```

