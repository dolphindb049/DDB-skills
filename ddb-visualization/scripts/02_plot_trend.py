# --- USER CONFIG ---
CSV_DATA_PATH = "d:/work/202507_202510_product/stock_trend_data.csv"
OUTPUT_FILE = "stock_trend_plot.png"
# -------------------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

def plot_from_csv():
    # 1. 检查数据文件是否存在
    if not os.path.exists(CSV_DATA_PATH):
        print(f"Error: Data file not found at {CSV_DATA_PATH}")
        print("Please run '01_fetch_trend_data.dos' first to generate the data.")
        return

    print(f"Loading data from {CSV_DATA_PATH}...")
    try:
        # DolphinDB saveText 默认可能是逗号分隔，无表头或有表头取决于配置，通常包含表头
        df = pd.read_csv(CSV_DATA_PATH)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    if df.empty:
        print("Data is empty.")
        return

    # 2. 数据预处理
    # 假设列名为 trade_date, ts_code, close
    # 检查列名是否符合预期，如果不符合则尝试推断
    required_cols = {'trade_date', 'close', 'ts_code'}
    if not required_cols.issubset(df.columns):
        print(f"Warning: Columns {df.columns} do not match expected {required_cols}")
        # 尝试使用第一列作为 Date, 最后一列作为 Close
    
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    
    # 3. 绘图
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    
    # 支持中文显示 (尝试设置字体，如果失败则回退)
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial'] 
    plt.rcParams['axes.unicode_minus'] = False 

    try:
        sns.lineplot(data=df, x='trade_date', y='close', hue='ts_code', marker='o', markersize=4)
    except Exception as e:
        print(f"Plotting error: {e}")
        return
    
    plt.title('Stock Price Trend Analysis (DolphinDB Data)', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Closing Price', fontsize=12)
    plt.legend(title='Stock Code')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 4. 保存图片
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, OUTPUT_FILE)
    
    plt.savefig(output_path)
    print(f"Plot saved to: {output_path}")

if __name__ == "__main__":
    plot_from_csv()
