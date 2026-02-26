# call

## 语法

`call(func, args...)`

## 参数

* **func** 是一个函数名。
* **args** 是函数func的参数。

## 详情

用指定的参数调用一个函数。常常用在 [each](each.md)/[peach](peach.md) 或 [loop](loop.md)/[ploop](ploop.md) 中，用来调用一批函数。

## 例子

```
call(sum, 1..10);
// output
55
// 等同于sum(1..10)

each(call, [avg, sum], [0..10, 0..100]);
// output
[5,5050]

each(call{, 1..3},(sin,log));
// 注意call{, 1..3}是一个部分应用
```

| sin | log |
| --- | --- |
| 0.841471 | 0 |
| 0.909297 | 0.693147 |
| 0.14112 | 1.098612 |

