# writeLine

## 语法

`writeLine(handle, string,
[windowsLineEnding])`

## 参数

可选的布尔型参数 *windowsLineEnding* 是行结束符。如果这个参数没有指定，有三种情况：

* 如果句柄是一个套接字，行结束符是 \r\n
* 如果句柄是一个文件，且操作系统不是 Windows，行结束符是 \n
* 如果句柄是一个文件，且操作系统是 Windows，行结束符是 \r\n

## 详情

在给定的句柄中写一行。函数自动将一个行分隔符添加到字符串结尾。所以字符串不应该以行分隔符结尾。如果该操作成功，函数返回 1；否则，将抛出一个
IOException。

## 例子

```
x=`IBM`MSFT`GOOG`YHOO`ORCL
eachRight(writeLine, file("test.txt","w"), x);
// output
[1,1,1,1,1]

fin = file("test.txt")
do{
   x=fin.readLine()
   if(x.isVoid()) break
   print x
}
while(true);

// output
IBM
MSFT
GOOG
YHOO
ORCL
```

