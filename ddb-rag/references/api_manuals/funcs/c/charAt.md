# charAt

## 语法

`charAt(X, Y)`

## 参数

**X** 是字符串标量或向量。

**Y** 是整型标量或与 *X* 长度相同的整型向量。

## 详情

返回字符串中指定位置的字符。返回的结果是 CHAR 类型。

## 例子

```
s=charAt("abc",2);
s;
// output
'c'

typestr(s);
// output
CHAR

charAt(["hello","world"],[3,4]);
// output
['l','d']
```

