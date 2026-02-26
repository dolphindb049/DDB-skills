# lockUser

## 语法

`lockUser(userId)`

## 参数

**userId** 是表示用户名的字符串。

## 详情

锁定用户 *userId*。该函数仅限管理员用户调用，调用时须开启配置项 *enhancedSecurityVerification*。

## 例子

```
lockUser("user1")
```

相关函数：[unlockUser](../u/unlockUser.md)

