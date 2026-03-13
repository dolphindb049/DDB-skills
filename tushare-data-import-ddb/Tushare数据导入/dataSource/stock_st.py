'''
Author: tanhua hua.tan@dolphindb.com
Date: 2025-11-10 17:34:29
LastEditors: tanhua hua.tan@dolphindb.com
LastEditTime: 2025-11-10 17:37:40
FilePath: \TushareDDB创建库表_全量增量代码\dataSource\stock_st.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
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
logger_stock_st = logging.getLogger('logger_stock_st')
logger_stock_st.setLevel(logging.INFO)
# 日志输出到文件
fileHandler_stock_st = logging.FileHandler(basic.logDir + "/stock_st.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileHandler_stock_st.setFormatter(formatter)
# 日志输出到控制台
console_stock_st = logging.StreamHandler() 
console_stock_st.setFormatter(formatter)
# 将 Handler 添加到 Logger
logger_stock_st.addHandler(fileHandler_stock_st)
logger_stock_st.addHandler(console_stock_st)

def get_data(trade_date, appender, token, dataSource, s, maxRetries):
    pro = ts.pro_api(token)
    retry_count = 0  # 初始化重试计数器
    max_retries = maxRetries  # 最大重试次数
    while retry_count < max_retries:
        try:
            data = pro.stock_st(trade_date=trade_date)
            data['trade_date'] = pd.to_datetime(data['trade_date'], format='%Y%m%d')
            data['update_time'] = datetime.now()
            appender.append(data)
            logger_stock_st.info("Data of %s for %s has been written.", dataSource, trade_date)
            return
        except Exception as e:
            retry_count += 1
            s.run('writeLogLevel(WARNING, "'+'easyTushareImport - '+dataSource+' - Failed to get data of '+dataSource+' '+trade_date+'. Will retry in 10 seconds. Error: '+str(e).replace('"',"'")+'")')
            logger_stock_st.warning("Failed to get data of %s %s. Will retry in 10 seconds. Error: %s", dataSource, trade_date, e)
            time.sleep(10)
    # 如果达到最大重试次数，记录错误并抛出异常
    logger_stock_st.error("Failed to get data of %s after %d attempts. Exiting.", dataSource, max_retries)
    raise Exception(f"Failed to get data of {dataSource} after {max_retries} attempts. Exiting.")

def main(session, startDate, endDate, token, dataSource, maxRetries):
    # 与 DolphinDB 建立会话和连接
    # print(session)
    s = ddb.session(session["host"], session["port"], session["username"], session["password"])
    s.run("share(table(1:0, `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]),'tt')")
    # 初始化库表：沪深股票 - 基础数据 - 股本情况（盘前）
    scripts = """
    use DolphinDBModules::EasyTushare::createDBTB
    createStockST()
    """
    #s.run(scripts)
    dbname = s.run("getDBname('{}')".format(dataSource))  
    print(dbname)
    # 初始化python写入接口
    appender = ddb.TableAppender(dbPath='dfs://'+dbname, tableName=dataSource, ddbSession=s)   
    pro = ts.pro_api(token)

    trade_dates = pro.trade_cal(exchange='SSE', is_open='1', start_date=startDate, end_date=endDate, fields='cal_date')

    for trade_date in trade_dates['cal_date'].values:
        logger_stock_st.info("开始处理 %s 的数据 。", trade_date)
        #time.sleep(1)
        get_data(trade_date, appender, token, dataSource, s, maxRetries)

    logger_stock_st.info("The %s data import is complete.", dataSource)
