# isNothing

## 语法

`isNothing(X)`

## 参数

**X** 可以是标量或向量。

## 详情

"Nothing" 是两个 VOID 类型的对象之一。

`isNothing` 用于检查一个函数被调用时，函数的参数是否被传了值进来。

## 例子

```
f=def(x,y): isNothing(y);
f(5,);
// output
true

f(5, NULL);
// output
false
```

