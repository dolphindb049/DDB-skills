# strip

## 语法

`strip(X)`

## 参数

**X** 是字符串标量或向量。

## 详情

去掉首尾所有空格，制表符，换行和回车符号。

## 例子

```
x="\nhello world\t\n";
x;

// output
hello world

strip x;
// output
hello world
```

相关函数：[trim](../t/trim.md)

