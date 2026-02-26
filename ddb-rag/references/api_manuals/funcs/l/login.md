# login

## 语法

`login(userId, password)`

## 参数

**userId** 是表示用户名的字符串。它只能包含字母、数字和下划线，并且不能以数字开头。长度不能超过30个字符。

**password** 是表示密码的字符串。它不能包含空格和控制字符。长度必须在8到20个字符之间。

## 详情

用户可在控制节点或数据节点/计算节点上登录。

从 2.00.10.10 开始，用户可以通过配置项 *enhancedSecurityVerification*
控制在登录时是否约束密码重试的次数。若不设置 *enhancedSecurityVerification*，则不约束；若设置
*enhancedSecurityVerification*=true，则当某个用户登录时，在1分钟内连续5次输入错误密码，系统会锁定这个用户的登录。10分钟后才允许该用户再次登录。

## 例子

```
login("JohnSmith", "Qb05078.");
```

