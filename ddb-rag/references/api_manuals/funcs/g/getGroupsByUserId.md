# getGroupsByUserId

## 语法

`getGroupsByUserId(userId)`

## 参数

**userId** 是表示用户名的字符串。

## 详情

返回用户所在的组。

注： 该函数只能由管理员在控制节点、数据节点和计算节点运行。

## 例子

```
getGroupsByUserId("admin")

// output
["MVP","MYMVP"]
```

