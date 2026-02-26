# getIPBlackList

## 语法

`getIPBlackList()`

## 参数

无

## 详情

查看当前集群的 IP 黑名单。

返回一个 STRING 向量。

## 例子

```
addIPBlackList(["1.1.1.1", "2.2.2.2", "3.3.3.3"])
removeIPBlackList("2.2.2.2")
getIPBlackList()
// output: ["1.1.1.1", "3.3.3.3"]
```

相关函数：[addIPBlackList](../a/addipblacklist.md)、[removeIPBlackList](../r/removeipblacklist.md)

