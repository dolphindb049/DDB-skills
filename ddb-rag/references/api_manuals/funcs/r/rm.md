# rm

## 语法

`rm(filename)`

## 参数

**filename** 是要删除的文件的名称。

## 详情

删除一个文件。该命令必须要用户登录后才能执行。

## 例子

```
files("/home/test");
```

| filename | isDir | fileSize | lastAccessed | lastModified |
| --- | --- | --- | --- | --- |
| abc.txt | 0 | 15 | 1496650187443 | 1496647459999 |
| dir1 | 1 | 0 | 1496650004836 | 1496650004836 |
| dir2 | 1 | 0 | 1496650002210 | 1496650002210 |
| dir3 | 1 | 0 | 1496649999597 | 1496649999597 |

```
rm("/home/test/abc.txt");       // delete file abc.txt

files("/home/test");
```

| filename | isDir | fileSize | lastAccessed | lastModified |
| --- | --- | --- | --- | --- |
| dir1 | 1 | 0 | 1496650004836 | 1496650004836 |
| dir2 | 1 | 0 | 1496650002210 | 1496650002210 |
| dir3 | 1 | 0 | 1496649999597 | 1496649999597 |

