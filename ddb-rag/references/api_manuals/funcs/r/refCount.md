# refCount

## 语法

`refCount(varname)`

## 参数

**varname** 是一个字符串，表示变量名称。

## 详情

计算某个对象被引用的数量。

## 例子

```
db=database("",VALUE,1 2 3)
refCount(`db);
// output
1

db1=db
db2=db
refCount(`db);
// output
3
```

