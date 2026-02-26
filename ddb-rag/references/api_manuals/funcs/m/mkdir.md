# mkdir

## 语法

`mkdir(directory)`

## 参数

**directory** 为要创建的目录的名字。

## 详情

创建一个目录。该函数必须要用户登录后才能执行。

## 例子

```
files("/home/test");
```

| filename | isDir | fileSize | lastAccessed | lastModified |
| --- | --- | --- | --- | --- |
| dir3 | 1 | 0 | 1496649999597 | 1496649999597 |

```
mkdir("/home/test/dir1");
mkdir("/home/test/dir2");
mkdir("/home/test/dir3");
// output
The directory [/home/test/dir3] already exists.
```

```
files("/home/test");
```

| filename | isDir | fileSize | lastAccessed | lastModified |
| --- | --- | --- | --- | --- |
| dir1 | 1 | 0 | 1496651628372 | 1496651628372 |
| dir2 | 1 | 0 | 1496651645598 | 1496651645598 |
| dir3 | 1 | 0 | 1496649999597 | 1496649999597 |

