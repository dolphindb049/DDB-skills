# getIPWhiteList

## 语法

`getIPWhiteList()`

## 参数

无

## 详情

查看当前集群的 IP 白名单。

返回一个 STRING 向量。

## 例子

```
addIPWhiteList(["1.1.1.1", "2.2.2.2", "3.3.3.3"])
removeIPWhiteList("2.2.2.2")
getIPWhiteList()
// output: ["1.1.1.1", "3.3.3.3"]
```

相关函数：[addIPWhiteList](../a/addipwhitelist.md)、[removeIPWhiteList](../r/removeipwhitelist.md)

