# getFunctionViews

## 语法

`getFunctionViews()`

## 参数

无

## 详情

获取函数视图。返回一张表，包含两个字段：

* name：函数名。
* body：函数体。对于直接通过 dom 模块封装的视图，或使用 use <moduleName> 的方式加载
  dom 模块后再封装其中函数得到的函数视图，该字段将显示函数名，不会显示其函数体。

管理员执行该函数，返回所有用户创建的函数视图；拥有 VIEW\_OWNER 权限的用户执行该函数只返回该用户创建的函数视图。

## 例子

```
getFunctionViews()
```

| name | body |
| --- | --- |
| countTradeAll | countTradeAll |

