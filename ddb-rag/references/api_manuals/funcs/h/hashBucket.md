# hashBucket

## 语法

`hashBucket(X, buckets)`

## 参数

**X** 可以是标量或向量。

**buckets** 是一个正整数。

## 详情

计算 *X* 的哈希值。哈希分区是基于分区列元素的哈希值。

## 例子

```
hashBucket(34 45 67, 10);

// output
[4,5,7]

hashBucket(`AAPL`TSLA`GS`MS`GE`BA`UAL`WMT, 10);

// output
[9,4,1,8,3,7,5,2]
```

