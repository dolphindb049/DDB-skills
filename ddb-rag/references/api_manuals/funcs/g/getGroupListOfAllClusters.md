# getGroupListOfAllClusters

## 语法

`getGroupListOfAllClusters()`

## 参数

无

## 详情

查询多集群系统中所有集群的用户组信息。只能由管理员在 MoM（Master of Master，管理集群）上执行该函数。

**返回值**：一个字典，其中：

* key：集群名称。
* value：用户组名称列表。

## 例子

```
getGroupListOfAllClusters()

/* Output:
masterOfMaster->["group1"]
MoMSender->["group2"]
*/
```

