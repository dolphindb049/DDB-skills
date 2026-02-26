# --- USER CONFIG ---
# DolphinDB Connection Config
DDB_HOST = "192.168.100.43" # Default from server.py analysis
DDB_PORT = 7739
DDB_USER = "admin"
DDB_PASS = "123456"

# Data Fetching Config
DOS_SCRIPT_PATH = ".github/skills/ddb-visualization/scripts/01_fetch_trend_data.dos"
CSV_DATA_PATH = "d:/work/202507_202510_product/stock_trend_data.csv"

# Plotting Config
OUTPUT_FILE = "stock_trend_plot.png"
# -------------------

import dolphindb as ddb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

def fetch_data():
    print(f"Connecting to DolphinDB at {DDB_HOST}:{DDB_PORT}...")
    s = ddb.session()
    try:
        is_connected = s.connect(DDB_HOST, DDB_PORT, DDB_USER, DDB_PASS)
        if not is_connected:
            raise ConnectionError("Connection failed")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return False

    print(f"Reading script from {DOS_SCRIPT_PATH}...")
    try:
        with open(DOS_SCRIPT_PATH, 'r', encoding='utf-8') as f:
            script_content = f.read()
            
        # Remove the conflicting saveText line since we want to fetch data to Python memory
        # We will parse the script or just append a return statement if needed
        # But wait, the script already returns 'result' at the end or calls saveText. 
        # Let's replace the last saveText block to just return result.
        
        # A simple hack: we remove the saveText lines for local execution
        lines = script_content.split('\n')
        filtered_lines = [line for line in lines if "saveText" not in line]
        
        # Ensure the script returns the table 'result'
        # The script ends with "print(...)". We need to ensure it returns the table.
        # We can append "result" at the very end.
        runnable_script = "\n".join(filtered_lines) + "\nresult"
        
    except Exception as e:
        print(f"❌ Error reading script file: {e}")
        return False

    print("Executing script on DolphinDB Server...")
    try:
        # Result will be a pandas DataFrame if it's a table
        df = s.run(runnable_script)
        
        if isinstance(df, pd.DataFrame):
            print(f"✅ Data fetched successfully: {len(df)} rows.")
            # Save locally
            df.to_csv(CSV_DATA_PATH, index=False)
            print(f"Saved to local CSV: {CSV_DATA_PATH}")
            return True
        else:
            print(f"⚠️ Query returned unexpected type: {type(df)}")
            print(df)
            return False

    except Exception as e:
        print(f"❌ Execution error: {e}")
        return False

def plot_data():
    if not os.path.exists(CSV_DATA_PATH):
        print(f"❌ Data file not found: {CSV_DATA_PATH}")
        return

    print("Loading data for plotting...")
    try:
        df = pd.read_csv(CSV_DATA_PATH)
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        
        plt.figure(figsize=(12, 6))
        sns.set_style("whitegrid")
        # Try to support Chinese fonts
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial'] 
        plt.rcParams['axes.unicode_minus'] = False 

        sns.lineplot(data=df, x='trade_date', y='close', hue='ts_code', marker='o', markersize=4)
        
        plt.title('Stock Price Trend Analysis', fontsize=16)
        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.legend(title='Stock Code')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save in current directory
        plt.savefig(OUTPUT_FILE)
        print(f"✅ Plot saved to: {os.path.abspath(OUTPUT_FILE)}")
        
    except Exception as e:
        print(f"❌ Plotting error: {e}")

if __name__ == "__main__":
    # 1. Fetch Data
    if fetch_data():
        # 2. Plot Data
        plot_data()
