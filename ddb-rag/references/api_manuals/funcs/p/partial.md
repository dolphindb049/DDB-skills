# partial

## 语法

`partial(func, args...)`

## 参数

**func** 是 DolphinDB 中的函数。

**args...** 是函数的参数。

## 详情

创建一个部分应用。

## 例子

```
partial(add,1)(2);
// output
3

def f(a,b):a pow b
g=partial(f, 2)
g(3);
// output
8
```

