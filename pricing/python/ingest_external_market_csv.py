#!/usr/bin/env python3
"""
将外部市场价 CSV 导入 pricing_market_external。
CSV 至少包含列: pricingDate,instrumentId,marketPrice
可选列: source,priceType
"""

import argparse
import pandas as pd
import dolphindb as ddb


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--host", default="192.168.100.43")
    parser.add_argument("--port", type=int, default=8671)
    parser.add_argument("--user", default="admin")
    parser.add_argument("--password", default="123456")
    parser.add_argument("--db-path", default="dfs://bond_pricing_workflow_v2")
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    for c in ["pricingDate", "instrumentId", "marketPrice"]:
        if c not in df.columns:
            raise ValueError(f"Missing required column: {c}")

    if "source" not in df.columns:
        df["source"] = "external_csv"
    if "priceType" not in df.columns:
        df["priceType"] = "NET"

    df["pricingDate"] = pd.to_datetime(df["pricingDate"]).dt.date
    df["sourceTs"] = pd.Timestamp.now()

    sess = ddb.session()
    sess.connect(args.host, args.port, args.user, args.password)
    sess.upload({"tmp_ext": df})

    sess.run(f'''
append!(loadTable("{args.db_path}", "pricing_market_external"),
    select date(pricingDate) as pricingDate,
           string(instrumentId) as instrumentId,
           double(marketPrice) as marketPrice,
           string(priceType) as priceType,
           string(source) as source,
           timestamp(sourceTs) as sourceTs
    from tmp_ext)
''')

    print(f"Imported {len(df)} rows into pricing_market_external")


if __name__ == "__main__":
    main()
