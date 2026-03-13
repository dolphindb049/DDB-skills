'''
Author: huyukai yuai.hu@dolphindb.com
Date: 2025-12-25 11:41
LastEditors: huyukai yukai.hu@dolphindb.com
LastEditTime: 2025-12-25 11:41
FilePath: \PythonModules\TushareToDDB\dataSource\index_member_all.py
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
logging_index_member_all = logging.getLogger('logging_sw_daily')
logging_index_member_all.setLevel(logging.INFO)
# 日志输出到文件
fileHandler_index_member_all = logging.FileHandler(basic.logDir + "/index_member_all.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileHandler_index_member_all.setFormatter(formatter)
# 日志输出到控制台
console_index_member_all = logging.StreamHandler() 
console_index_member_all.setFormatter(formatter)
# 将 Handler 添加到 logging
logging_index_member_all.addHandler(fileHandler_index_member_all)
logging_index_member_all.addHandler(console_index_member_all)

def get_data(ts_code, appender, pro, dataSource, s, maxRetries):
    retry_count = 0  # 初始化重试计数器
    max_retries = maxRetries  # 最大重试次数
    while retry_count < max_retries:
        try:
            data = pro.index_member_all(l1_code=ts_code)
            data['in_date'] = pd.to_datetime(data['in_date'], format='%Y%m%d')
            data['out_date'] = pd.to_datetime(data['out_date'], format='%Y%m%d')
            data['update_time'] = datetime.now()
            appender.append(data)
            logging_sw_daily.info("Data of %s %s has been written.", dataSource, ts_code)
            return
        except Exception as e:
            retry_count += 1
            s.run('writeLogLevel(WARNING, "'+'easyTushareImport - '+dataSource+' - Failed to get data of '+dataSource+' '+ts_code+'. Will retry in 10 seconds. Error: '+str(e).replace('"',"'")+'")')
            logging_sw_daily.warning("Failed to get data of %s %s. Will retry in 10 seconds. Error: %s", dataSource, ts_code, e)
            time.sleep(10)
    # 如果达到最大重试次数，记录错误并抛出异常
    logging_index_member_all.error("Failed to get data of %s after %d attempts. Exiting.", dataSource, max_retries)
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
    logging_index_member_all.info("The %s data import is starting.", dbname)
    # 初始化python写入接口
    appender = ddb.TableAppender(dbPath='dfs://'+dbname, tableName=dataSource, ddbSession=s)

    pro = ts.pro_api(token)

    # 按一级行业代码导入数据
    index_codes = s.run("select ts_code from loadTable('dfs://basic_factor', 'index_basic') where  publisher like '%申%' and  name not like '%退市%' and category = '一级行业指数'")

    for index_code in index_codes.values:
        #print(index_code)
        get_data(index_code[0], appender, pro, dataSource, s, maxRetries)
        time.sleep(6)
    
    logging_index_member_all.info("The %s data import is complete.", dataSource)
