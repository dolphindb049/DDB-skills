# unlockUser

## 语法

`unlockUser(userId)`

## 参数

**userId** 是表示用户名的字符串。

## 详情

解锁用户 *userId*。该函数仅限管理员用户调用，调用时须开启配置项 *enhancedSecurityVerification*。

## 例子

```
unlockUser("user1")
```

相关函数：[lockUser](../l/lockUser.md)

