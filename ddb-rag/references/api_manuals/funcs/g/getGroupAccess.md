# getGroupAccess

## 语法

`getGroupAccess(groupIds)`

## 参数

**groupIds** 表示组名的字符串标量或向量。

## 详情

返回组的权限。只能由管理员执行该函数。

注：

* 自 3.00.2 版本起，支持获取访问计算节点组的权限。
* 自 3.00.0 版本起，支持获取访问 catalog 的相关权限。

## 例子

```
getGroupAccess("myGroup")
```

