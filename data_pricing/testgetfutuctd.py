# -*- coding: utf-8 -*-
import pandas as pd
import requests

# 单独测试国债期货最便宜可交割券接口
token = '4c89993d518c6cb4105870590b923416ecc61d0da7b438f6ace0bb036040a7c4'
headers = {
    "Authorization": f"Bearer {token}",
    "Accept-Encoding": "gzip, deflate"
}

# 测试不同的参数组合
test_cases = [
    {
        'name': '测试1: 近期活跃合约',
        'params': {
            'ticker': 'T2412',  # 2024年12月交割的国债期货
            'beginDate': '20240801',
            'endDate': '20240831'
        }
    },
    {
        'name': '测试2: 不指定具体日期',
        'params': {
            'ticker': 'T2412'
        }
    },
    {
        'name': '测试3: 使用tradeDate',
        'params': {
            'tradeDate': '20240815'
        }
    }
]

for test in test_cases:
    print(f"\n{test['name']}")
    print("-" * 40)
    
    query_params = '&'.join([f"{k}={v}" for k, v in test['params'].items()])
    api_url = f"/api/future/getFutuCtd.json?field=&{query_params}"
    
    response = requests.get(f"https://api.datayes.com/data/v1{api_url}", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"retCode: {result.get('retCode')}")
        print(f"retMsg: {result.get('retMsg')}")
        if result.get('retCode') == 1 and result.get('data'):
            df = pd.DataFrame(result['data'])
            print(f"数据量: {len(df)}")
            print(f"字段: {list(df.columns)}")
        else:
            print("无数据返回")
    else:
        print(f"HTTP错误: {response.status_code}")