# loadModel

## 语法

`loadModel(file)`

## 参数

**file** 是模型所在的本地文件的路径。

## 详情

把模型加载到内存中，以字典的形式返回模型。

```
x1 = rand(100.0, 100)
x2 = rand(100.0, 100)
b0 = 6
b1 = 1
b2 = -2
err = norm(0, 10, 100)
y = b0 + b1 * x1 + b2 * x2 + err
t = table(x1, x2, y)
model = randomForestRegressor(sqlDS(<select * from t>), `y, `x1`x2)
saveModel(model, "/home/DolphinDB/Data/regressionModel.txt");

model = loadModel("/home/DolphinDB/Data/regressionModel.txt")
yhat = predict(model, t);
```

