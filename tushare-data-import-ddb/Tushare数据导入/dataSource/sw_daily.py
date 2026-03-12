'''
Author: huyukai yuai.hu@dolphindb.com
Date: 2025-12-25 11:41
LastEditors: huyukai yukai.hu@dolphindb.com
LastEditTime: 2025-12-25 11:41
FilePath: \PythonModules\TushareToDDB\dataSource\sw_daily.py
Description: 申万行业日线行情导数程序
'''
#!/usr/bin/env python
# coding: utf-8
import basic
import tushare as ts
import pandas as pd
from datetime import datetime
import time
import dolphindb as ddb
import logging
import warnings
warnings.filterwarnings("ignore")

# 设置日志配置
logging_sw_daily = logging.getLogger('logging_sw_daily')
logging_sw_daily.setLevel(logging.INFO)
# 日志输出到文件
fileHandler_sw_daily = logging.FileHandler(basic.logDir + "/sw_daily.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileHandler_sw_daily.setFormatter(formatter)
# 日志输出到控制台
console_sw_daily = logging.StreamHandler() 
console_sw_daily.setFormatter(formatter)
# 将 Handler 添加到 logging
logging_sw_daily.addHandler(fileHandler_sw_daily)
logging_sw_daily.addHandler(console_sw_daily)

def get_data(index_code, appender, pro, dataSource, s, maxRetries):
    retry_count = 0  # 初始化重试计数器
    max_retries = maxRetries  # 最大重试次数
    while retry_count < max_retries:
        try:
            data = pro.sw_daily(ts_code=index_code)
            data['trade_date'] = pd.to_datetime(data['trade_date'], format='%Y%m%d')
            data['update_time'] = datetime.now()
            appender.append(data)
            logging_sw_daily.info("Data of %s %s has been written.", dataSource, index_code)
            return
        except Exception as e:
            retry_count += 1
            s.run('writeLogLevel(WARNING, "'+'easyTushareImport - '+dataSource+' - Failed to get data of '+dataSource+' '+index_code+'. Will retry in 10 seconds. Error: '+str(e).replace('"',"'")+'")')
            logging_sw_daily.warning("Failed to get data of %s %s. Will retry in 10 seconds. Error: %s", dataSource, index_code, e)
            time.sleep(10)
    # 如果达到最大重试次数，记录错误并抛出异常
    logging_sw_daily.error("Failed to get data of %s after %d attempts. Exiting.", dataSource, max_retries)
    raise Exception(f"Failed to get data of {dataSource} after {max_retries} attempts. Exiting.")


def main(session, startDate, endDate, token, dataSource, maxRetries):
    # 与 DolphinDB 建立会话和连接
    s = ddb.session(session["host"], session["port"], session["username"], session["password"])
    # 初始化库表：指数基本信息
    scripts = """
    use DolphinDBModules::EasyTushare::createDBTB
    createIndexBasic()
    """
    #s.run(scripts)
    print("token:", token)
    dbname = s.run("getDBname('{}')".format(dataSource))  
    logging_sw_daily.info("The %s data import is starting.", dbname)
    # 初始化python写入接口
    appender = ddb.TableAppender(dbPath='dfs://'+dbname, tableName=dataSource, ddbSession=s)

    pro = ts.pro_api(token)
    
    index_codes = s.run("select ts_code from loadTable('dfs://basic_factor', 'index_basic') where  publisher like '%申%' and  name not like '%退市%' and category = '一级行业指数'")
    #print(index_codes)
    # 按交易日期循环获取数据并写入DolphinDB
    #trade_dates = pro.trade_cal(exchange='SSE', start_date=startDate, end_date=endDate, is_open='1', fields='cal_date')

    for index_code in index_codes.values:
        print(index_code)
        get_data(index_code[0], appender, pro, dataSource, s, maxRetries)
        time.sleep(6)
    
    logging_sw_daily.info("The %s data import is complete.", dataSource)
