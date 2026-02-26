# files

## 语法

`files(directory, [pattern])`

## 参数

**directory** 是表示目录路径的字符串。

**pattern** 是表示在该目录下搜索的文件名的模式的字符串。

## 详情

该函数必须要用户登录后才能执行。

如果没有指定 *pattern*，返回一个包含目录中的文件和子目录信息的表。

如果指定了 *pattern*，*函数返回一个包含文件名中包含了pattern* 的文件和子目录的表。

## 例子

```
files("/home/06_DolphinDB/01_App/DolphinDB_Win_V0.2");
```

| filename | isDir | fileSize | lastAccessed | lastModified |
| --- | --- | --- | --- | --- |
| LICENSE\_AND\_AGREEMENT.txt | 0 | 22558 | 1495508675000 | 1483773234998 |
| README\_WIN.txt | 0 | 5104 | 1495508675000 | 1483866232680 |
| server | 1 | 0 | 1496624932437 | 1496624932437 |
| THIRD\_PARTY\_SOFTWARE\_LICENS... | 0 | 8435 | 1495508675000 | 1483628426506 |

```
files("/home/06_DolphinDB/01_App/DolphinDB_Win_V0.2", "readme%");
```

| filename | isDir | fileSize | lastAccessed | lastModified |
| --- | --- | --- | --- | --- |
| README\_WIN.txt | 0 | 5104 | 1495508675000 | 1483866232680 |

```
select * from files("/home/06_DolphinDB/01_App/DolphinDB_Win_V0.2") where filename like "README%";
```

| filename | isDir | fileSize | lastAccessed | lastModified |
| --- | --- | --- | --- | --- |
| README\_WIN.txt | 0 | 5104 | 1495508675000 | 1483866232680 |

