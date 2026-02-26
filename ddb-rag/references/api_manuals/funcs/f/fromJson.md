# fromJson

## 语法

`fromJson(X)`

## 参数

**X** 是符合 DolphinDB 规范的 JSON 字符串数据。

## 详情

将符合 DolphinDB 规范的 JSON 格式的字符串转换为 DolphinDB 对象。

符合 DolphinDB 规范的 JSON
字符串应至少包含3个键值对："form"（数据结构）、"type"（数据类型）、"value"（值）。键值对 "value" 的值为实际数据。

当数据结构为表时，键值对 "name" 可用来指定列名；若为其他数据结构，键值对 ''name" 无意义。

## 例子

```
x=1 2 3
y=toJson(x)
y;
// output
{"name":"x","form":"vector","type":"int","size":"3","value":[1,2,3]}

fromJson(y);
// output
[1,2,3]
```

相关函数：[toJson](../t/toJson.md)

