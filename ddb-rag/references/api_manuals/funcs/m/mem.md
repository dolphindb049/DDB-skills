# mem

## 语法

`mem([freeUnusedBlocks=false])`

## 参数

**freeUnusedBlocks** 是一个布尔值，表示是否释放未使用的内存块。默认值为 false。

## 详情

显示本地节点内存使用情况。

结果中，allocatedBytes 为已分配内存；freeBytes 是可用内存。两者之差为已占用内存。

如果 *freeUnusedBlocks* =true，系统将会释放未使用的内存块。

## 例子

```
undef all;

t1=table(1 2 3 as a, `x`y`z as b, 10.8 7.6 3.5 as c)
mem();

// output
freeBytes->492904
allocatedBytes->8454144

x=bigarray(INT,100000,10000000)
mem();

// output
freeBytes->491056
allocatedBytes->12648448

undef all;
mem();

// output
freeBytes->4687936
allocatedBytes->12648448
```

