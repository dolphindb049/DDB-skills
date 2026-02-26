# isColumnarTuple

## 语法

`isColumnarTuple(X)`

## 参数

`X` 是一个元组。

## 详情

判断一个元组是否是 columnar tuple。

## 例子

```
tp = [[1,2,3], [4,5,6], [7,8]]
isColumnarTuple(tp)
    false

tp.setColumnarTuple!()
isColumnarTuple(tp)
    true
```

```

id = 3 2 1 4
val = [`aa`bb, `aa`cc`dd, `bb, `cc`dd]
t = table(id, val)

isColumnarTuple(t.val)
    true

isColumnarTuple(t.id)
    false

exec isColumnarTuple(val) from t
    true

av = array(INT[], 0, 10).append!([1 1 1 3, 2 4 2 5, 8 9 7 1, 5 4 3])
t = table(id, av)
isColumnarTuple(t.av)
    false
```

