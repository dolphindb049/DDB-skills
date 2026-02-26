# dropStreamGraph

## 语法

`dropStreamGraph(name)`

## 参数

**name** 字符串标量，表示流图的名字。可以传入完整的流图全限定名（如
catalog\_name.orca\_graph.graph\_name），也可以仅提供流图名（如 factors）；系统会根据当前的 catalog
设置自动补全为对应的全限定名。

## 详情

销毁指定流图。销毁成功后，流图状态转为 destroyed，但流图记录不会被删除。

在集群部署模式下，执行该操作的用户必须是管理员用户或拥有流图创建时所用计算组的 COMPUTE\_GROUP\_EXEC
权限。若在单节点部署环境中使用，则无需进行权限校验。

## 例子

```
dropStreamGraph("demo.orca_graph.indicators")

getStreamGraphMeta("demo.orca_graph.indicators")["status"]
// Output: ["destroyed"]
```

