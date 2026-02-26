# wc

## 语法

`wc(X)`

## 参数

**X** 是一个字符串。它可以是标量或向量。

## 详情

返回 *X* 中包含的单词数量。

## 例子

```
wc(`apple);
// output
1

wc("This is a 7th generation iphone!");
// output
6

wc("This is a 7th generation iphone!" "I wonder what the 8th generation looks like");
// output
[6,8]
```

