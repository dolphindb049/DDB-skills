# listAllMarkets

## 语法

`listAllMarkets()`

## 参数

**marketName** 字符串标量，表示要删除的交易日历标识，例如“XNYS”。

## 详情

获取当前节点所有的交易日历。

**返回值：**一个包含节点上所有交易日历标识的向量

## 例子

```
listAllMarkets()
// ["XTSE","XCSE","XLIM","ADDA","XSTO","XIST","AIXK","SSE","XMIL","XFRA","INE","XMEX","XBUD","XICE","XDUB","SHFE","CMES","XOSL","DCE","CCFX","CFFEX","XIDX","BVMF","XBOG","XKAR","XSAU","XBUE","XTKS","XBSE","XMOS"...]
```

**相关函数：**[addMarketHoliday](../a/addMarketHoliday.md)、[deleteMarketHoliday](../d/deleteMarketHoliday.md)

