# -*- coding: utf-8 -*-
import pandas as pd
import requests
import json
from typing import Optional, List
import time
from datetime import datetime

class UqerDataDownloader:
    """通联数据API下载器"""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = 'https://api.datayes.com/data/v1'
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept-Encoding": "gzip, deflate"
        }
    
    def download_data(self, api_endpoint: str, params: dict = None, 
                     page_size: int = 100000, max_pages: int = None) -> pd.DataFrame:
        """通用数据下载方法"""
        if params is None:
            params = {}
        
        # 构建查询字符串
        query_params = '&'.join([f"{k}={v}" for k, v in params.items() if v is not None])
        if query_params:
            query_params = '&' + query_params
        
        dataframes = []
        page = 1
        
        while True:
            if max_pages and page > max_pages:
                break
                
            # 构建完整URL
            api_url = f"{api_endpoint}?field={query_params}&pagenum={page}&pagesize={page_size}"
            
            print(f"正在获取第{page}页数据...")
            
            try:
                response = requests.get(f"{self.base_url}{api_url}", headers=self.headers)
                
                if response.status_code != 200:
                    print(f"HTTP错误: {response.status_code}")
                    break
                
                result = response.json()
                
                if result.get('retCode') != 1:
                    print(f"API错误: {result.get('retMsg', '未知错误')}")
                    break
                
                # 转换为DataFrame
                df = pd.DataFrame(result['data'])
                dataframes.append(df)
                
                print(f"第{page}页获取成功，数据量: {len(df)}")
                
                # 如果返回的数据少于page_size，说明已经是最后一页
                if len(df) < page_size:
                    break
                    
                page += 1
                time.sleep(0.1)
                
            except Exception as e:
                print(f"第{page}页下载失败: {str(e)}")
                break
        
        if not dataframes:
            print("没有获取到任何数据")
            return pd.DataFrame()
        
        result_df = pd.concat(dataframes, ignore_index=True)
        print(f"数据下载完成，总计 {len(result_df)} 条记录")
        
        return result_df

def main():
    """主函数 - 下载2022年至今的数据"""
    
    token = '4c89993d518c6cb4105870590b923416ecc61d0da7b438f6ace0bb036040a7c4'
    downloader = UqerDataDownloader(token)
    
    print(f"开始下载2022年至今数据，当前时间: {datetime.now()}")
    print("=" * 80)
    
    # 统一时间参数：2022年至今
    time_params = {
        'beginDate': '20220101',
        'endDate': '20250904'  # 到今天
    }
    
    publish_params = {
        'beginPublishDate': '20220101',
        'endPublishDate': '20250904'
    }
    
    # ========== 基础数据表 ==========
    
    # # 1. 债券基本信息 (主表)
    # print("\n1. 债券基本信息 (2022-至今)...")
    # print("-" * 50)
    # bond_data = downloader.download_data('/api/bond/getBond.json', params=publish_params)
    # if not bond_data.empty:
    #     bond_data.to_csv('bond_basic_info.csv', index=False, encoding='utf-8-sig')
    #     print(f"✓ 债券基本信息已保存，共 {len(bond_data)} 条记录")
    
    # # 2. 债券代码对照表
    # print("\n2. 债券代码对照表...")
    # print("-" * 50)
    # bond_ticker_data = downloader.download_data('/api/bond/getBondTicker.json')
    # if not bond_ticker_data.empty:
    #     bond_ticker_data.to_csv('bond_ticker_mapping.csv', index=False, encoding='utf-8-sig')
    #     print(f"✓ 债券代码对照表已保存，共 {len(bond_ticker_data)} 条记录")
    
    # # 3. 期货合约信息
    # print("\n3. 期货合约信息...")
    # print("-" * 50)
    # future_info_data = downloader.download_data('/api/future/getFutu.json')
    # if not future_info_data.empty:
    #     future_info_data.to_csv('future_contract_info.csv', index=False, encoding='utf-8-sig')
    #     print(f"✓ 期货合约信息已保存，共 {len(future_info_data)} 条记录")
    
    # ========== 依赖数据表（样本） ==========

    # 从现有的 CSV 文件中加载债券基本信息
    bond_data = pd.read_csv('bond_basic_info.csv')

    if not bond_data.empty:
        # 获取样本债券ticker
        sample_tickers = bond_data['ticker'].dropna().unique().astype(str).tolist()
        print(f"\n获取到 {len(sample_tickers)} 个债券ticker用于样本下载")
        
        # 4. 债券现金流 (快速循环)
        print("\n4. 债券现金流 (样本)...")
        print("-" * 50)
        all_cf_data = []
        success_count = 0
        target_count = 50  # 目标获取50个有数据的债券
        
        for i, ticker in enumerate(sample_tickers):
            if success_count >= target_count:
                break
                
            print(f"  [{success_count+1}/{target_count}] 下载 {ticker}...", end='')
            
            try:
                cf_data = downloader.download_data('/api/bond/getBondCfNew.json', 
                    params={'ticker': ticker, 'beginDate': '20220101', 'endDate': '20250904'}, 
                    max_pages=1)
                if not cf_data.empty:
                    all_cf_data.append(cf_data)
                    success_count += 1
                    print(f" ✓ ({len(cf_data)}条)")
                else:
                    print(" ×")
            except Exception as e:
                print(f" 错误: {e}")
            
            # 每10个添加一次延时
            if (i + 1) % 10 == 0:
                time.sleep(0.2)
        
        if all_cf_data:
            combined_cf = pd.concat(all_cf_data, ignore_index=True)
            combined_cf.to_csv('bond_cashflow_sample.csv', index=False, encoding='utf-8-sig')
            print(f"✓ 债券现金流样本已保存，共 {len(combined_cf)} 条记录 (来自{success_count}个债券)")
        else:
            print("× 没有获取到债券现金流数据")
        
        # 5. 债券类型 (快速循环)
        print("\n5. 债券类型 (样本)...")
        print("-" * 50)
        all_type_data = []
        success_count = 0
        target_count = 30
        
        for i, ticker in enumerate(sample_tickers):
            if success_count >= target_count:
                break
                
            print(f"  [{success_count+1}/{target_count}] 下载 {ticker}...", end='')
            
            try:
                bond_type_data = downloader.download_data('/api/bond/getBondType.json', 
                    params={'ticker': ticker}, max_pages=1)
                if not bond_type_data.empty:
                    all_type_data.append(bond_type_data)
                    success_count += 1
                    print(f" ✓ ({len(bond_type_data)}条)")
                else:
                    print(" ×")
            except Exception as e:
                print(f" 错误: {e}")
            
            if (i + 1) % 10 == 0:
                time.sleep(0.2)
        
        if all_type_data:
            combined_type = pd.concat(all_type_data, ignore_index=True)
            combined_type.to_csv('bond_type_sample.csv', index=False, encoding='utf-8-sig')
            print(f"✓ 债券类型样本已保存，共 {len(combined_type)} 条记录 (来自{success_count}个债券)")
        else:
            print("× 没有获取到债券类型数据")
        
        # 6. 外汇交易中心估值 (快速循环)
        print("\n6. 外汇交易中心估值 (样本)...")
        print("-" * 50)
        all_cfets_data = []
        success_count = 0
        target_count = 20
        
        for i, ticker in enumerate(sample_tickers):
            if success_count >= target_count:
                break
                
            print(f"  [{success_count+1}/{target_count}] 下载 {ticker}...", end='')
            
            try:
                cfets_data = downloader.download_data('/api/bond/getCFETSValuation.json', 
                    params={'ticker': ticker, 'beginDate': '20240101', 'endDate': '20250904'},
                    max_pages=1)
                if not cfets_data.empty:
                    all_cfets_data.append(cfets_data)
                    success_count += 1
                    print(f" ✓ ({len(cfets_data)}条)")
                else:
                    print(" ×")
            except Exception as e:
                print(f" 错误: {e}")
            
            if (i + 1) % 10 == 0:
                time.sleep(0.2)
        
        if all_cfets_data:
            combined_cfets = pd.concat(all_cfets_data, ignore_index=True)
            combined_cfets.to_csv('cfets_valuation_sample.csv', index=False, encoding='utf-8-sig')
            print(f"✓ 外汇交易中心估值样本已保存，共 {len(combined_cfets)} 条记录 (来自{success_count}个债券)")
        else:
            print("× 没有获取到外汇交易中心估值数据")
    
    # ========== 宏观数据 ==========
    
    # # 7. 利率互换曲线 (2024-2025)
    # print("\n7. 利率互换曲线...")
    # print("-" * 50)
    # irs_data = downloader.download_data('/api/bond/getBondCmIrsCurve.json', params={
    #     'beginDate': '20240101', 'endDate': '20250904',
    #     'curveCD': '01', 'curveTypeCD': '2', 'priceTypeCD': '2'
    # })
    # if not irs_data.empty:
    #     irs_data.to_csv('bond_irs_curve.csv', index=False, encoding='utf-8-sig')
    #     print(f"✓ 利率互换曲线已保存，共 {len(irs_data)} 条记录")
    
    # ========== 期货数据 ==========
    
    # 8. 国债期货最便宜可交割券
    print("\n8. 国债期货最便宜可交割券...")
    print("-" * 50)

    # 定义时间范围参数
    ctd_params = {
        'tradeDate': '20250903'  # 交易日期
    }

    ctd_data = downloader.download_data('/api/future/getFutuCtd.json', params=ctd_params, max_pages=2)
    if not ctd_data.empty:
        ctd_data.to_csv('future_ctd.csv', index=False, encoding='utf-8-sig')
        print(f"✓ 国债期货CTD已保存，共 {len(ctd_data)} 条记录")
    
    # ========== 行情数据（限制数据量） ==========
    
    # # 9. 期货日行情 (2024-2025)
    # print("\n9. 期货日行情 (2024-2025)...")
    # print("-" * 50)
    # future_daily_data = downloader.download_data('/api/market/getMktFutd.json', 
    #     params={'beginDate': '20240101', 'endDate': '20250904'}, max_pages=30)
    # if not future_daily_data.empty:
    #     future_daily_data.to_csv('future_daily_market.csv', index=False, encoding='utf-8-sig')
    #     print(f"✓ 期货日行情已保存，共 {len(future_daily_data)} 条记录")
    
    # # 10. 银行间现券日行情 (2024-2025)
    # print("\n10. 银行间现券日行情 (2024-2025)...")
    # print("-" * 50)
    # ib_bond_data = downloader.download_data('/api/market/getMktIBBondd.json', 
    #     params={'beginDate': '20240101', 'endDate': '20250904'}, max_pages=30)
    # if not ib_bond_data.empty:
    #     ib_bond_data.to_csv('interbank_bond_daily.csv', index=False, encoding='utf-8-sig')
    #     print(f"✓ 银行间现券日行情已保存，共 {len(ib_bond_data)} 条记录")
    
    print("\n" + "=" * 80)
    print("🎉 数据下载完成！")
    print(f"完成时间: {datetime.now()}")
    
    print("\n📁 生成的CSV文件:")
    files = [
        'bond_basic_info.csv',           # 债券基本信息(2022-2025)
        'bond_ticker_mapping.csv',       # 债券代码对照表
        'future_contract_info.csv',      # 期货合约信息
        'bond_cashflow_sample.csv',      # 债券现金流(样本)
        'bond_type_sample.csv',          # 债券类型(样本)
        'cfets_valuation_sample.csv',    # 外汇交易中心估值(样本)
        'bond_irs_curve.csv',            # 利率互换曲线(2024-2025)
        'future_ctd.csv',                # 国债期货CTD(2022-2025)
        'future_daily_market.csv',       # 期货日行情(2024-2025)
        'interbank_bond_daily.csv'       # 银行间债券日行情(2024-2025)
    ]

    file_descriptions = [
        "债券基本信息(2022-2025)",
        "债券代码对照表",
        "期货合约信息",
        "债券现金流(样本)",
        "债券类型(样本)",
        "外汇交易中心估值(样本)",
        "利率互换曲线(2024-2025)",
        "国债期货CTD(2022-2025)",
        "期货日行情(2024-2025)",
        "银行间债券日行情(2024-2025)"
    ]

    for i, (file, description) in enumerate(zip(files, file_descriptions), 1):
        print(f"  {i:2d}. {file} - {description}")

if __name__ == "__main__":
    main()