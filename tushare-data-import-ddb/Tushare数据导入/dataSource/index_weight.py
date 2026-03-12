'''
Author: tanhua hua.tan@dolphindb.com
Date: 2025-11-10 17:34:29
LastEditors: tanhua hua.tan@dolphindb.com
LastEditTime: 2025-11-11 17:56:00
FilePath: \TushareDDB创建库表_全量增量代码\dataSource\index_weight.py
Description: 主要指数成分股
'''
#!/usr/bin/env python
# coding: utf-8
import basic
import tushare as ts
import pandas as pd
from datetime import datetime, timedelta
import time
import dolphindb as ddb
import logging
import warnings
warnings.filterwarnings("ignore")

# 设置日志配置
logger_index_weight = logging.getLogger('logger_index_weight')
logger_index_weight.setLevel(logging.INFO)
# 日志输出到文件
fileHandler_index_weight = logging.FileHandler(basic.logDir + "/index_weight.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileHandler_index_weight.setFormatter(formatter)
# 日志输出到控制台
console_index_weight = logging.StreamHandler() 
console_index_weight.setFormatter(formatter)
# 将 Handler 添加到 Logger
logger_index_weight.addHandler(fileHandler_index_weight)
logger_index_weight.addHandler(console_index_weight)

def get_data(ts_code, trade_date, appender, token, dataSource, s, maxRetries):
    pro = ts.pro_api(token)
    retry_count = 0  # 初始化重试计数器
    max_retries = maxRetries  # 最大重试次数

    while retry_count < max_retries:
        try:
            # 获取指数成分股数据
            data = pro.index_weight(index_code=ts_code, trade_date=trade_date)
     
            if data is not None and not data.empty:
                data['trade_date'] = pd.to_datetime(data['trade_date'], format='%Y%m%d')
                data['update_time'] = datetime.now()
                
                # 定义完整的列顺序，确保与DolphinDB表结构完全匹配
                required_columns = ['index_code', 'con_code', 'trade_date', 'weight', 'update_time']
                
                # 按指定顺序选择列
                data = data[required_columns]
                
                appender.append(data)
                logger_index_weight.info("Data of %s for %s has been written. Records: %d", ts_code, trade_date, len(data))
                return
            else:
                logger_index_weight.info("No data of %s for %s", ts_code, trade_date)
                return
                
        except Exception as e:
            retry_count += 1
            s.run('writeLogLevel(WARNING, "'+'easyTushareImport - '+dataSource+' - Failed to get data of '+ts_code+' '+trade_date+'. Will retry in 10 seconds. Error: '+str(e).replace('"',"'")+'")')
            logger_index_weight.warning("Failed to get data of %s %s. Will retry in 10 seconds. Error: %s", ts_code, trade_date, e)
            time.sleep(10)
    # 如果达到最大重试次数，记录错误并抛出异常
    logger_index_weight.error("Failed to get data of %s after %d attempts. Exiting.", ts_code, max_retries)
    raise Exception(f"Failed to get data of {ts_code} after {max_retries} attempts. Exiting.")

def main(session, startDate, endDate, token, dataSource, maxRetries):
    """
    主函数 - 获取指定指数的成分股数据
    
    Parameters:
    session: DolphinDB会话配置
    startDate: 开始日期
    endDate: 结束日期  
    token: Tushare token
    dataSource: 数据源名称
    maxRetries: 最大重试次数
    """
    # 与 DolphinDB 建立会话和连接
    s = ddb.session(session["host"], session["port"], session["username"], session["password"])
    

    # 从index_basic表获取指数列表
    try:
        index_list = s.run("exec distinct ts_code from loadTable('dfs://basic_factor', 'index_basic') where ts_code is not null")
        logger_index_weight.info("Found %d indices from index_basic table", len(index_list))
    except Exception as e:
        logger_index_weight.error("Failed to get index list from index_basic table: %s", e)
        # 如果无法从数据库获取，使用默认的主要指数
        index_list = ['000852.SH', '000300.SH', '000016.SH']  # 中证1000、沪深300、上证50
        logger_index_weight.info("Using default index codes: %s", index_list)

    logger_index_weight.info("Start importing index weight data for %d indices. Date range: %s to %s", 
                           len(index_list), startDate, endDate)
    
    # 初始化库表：指数成分股
    scripts = """
    use DolphinDBModules::EasyTushare::createDBTB
    createIndexWeight()
    """
    #s.run(scripts)
    dbname = s.run("getDBname('{}')".format(dataSource))  
    
    pro = ts.pro_api(token)

    # 获取交易日历
    trade_dates = pro.trade_cal(exchange='SSE', is_open='1', start_date=startDate, end_date=endDate, fields='cal_date')

    total_indices = len(index_list)
    total_dates = len(trade_dates)
    logger_index_weight.info("Total indices: %d, Total trading days: %d", total_indices, total_dates)

    # 为每个指数代码获取数据
    for i, ts_code in enumerate(index_list):
        try:
            logger_index_weight.info("Processing index %s (%d/%d)", ts_code, i+1, total_indices)
            
            # 为每个指数创建appender
            appender = ddb.TableAppender(dbPath='dfs://'+dbname, tableName=dataSource, ddbSession=s)
            
            date_count = 0
            for trade_date in trade_dates['cal_date'].values:
                date_count += 1
                logger_index_weight.info("Processing %s for date %s (%d/%d)", ts_code, trade_date, date_count, total_dates)
                get_data(ts_code, trade_date, appender, token, dataSource, s, maxRetries)
                # 添加请求间隔，避免频繁调用
                time.sleep(0.5)
                
        except Exception as e:
            logger_index_weight.error("Failed to process index %s: %s", ts_code, e)
            continue

    logger_index_weight.info("The %s data import is complete. Processed %d indices.", dataSource, total_indices)

