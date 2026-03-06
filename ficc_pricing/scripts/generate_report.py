# /// script
# requires-python = ">=3.8"
# dependencies = ["dolphindb", "pandas", "tabulate"]
# ///

import argparse
import dolphindb as ddb
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Generate concise report from shared tables")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7731)
    parser.add_argument("--user", default="admin")
    parser.add_argument("--password", default="123456")
    parser.add_argument("--pricing-date", default="2026.03.04")
    args = parser.parse_args()

    s = ddb.session()
    s.connect(args.host, args.port, args.user, args.password)

    s.run(f"pDate={args.pricing_date}")

    def fetch_if_exists(shared_name: str):
        exists = bool(s.run(f"exists('{shared_name}')"))
        if not exists:
            return pd.DataFrame()
        return s.run(f"select * from {shared_name} where pricingDate=pDate")

    readiness = fetch_if_exists("pricing_data_readiness_report")
    curve = fetch_if_exists("pricing_curve_dependency_report")
    engine = fetch_if_exists("pricing_engine_run_report")
    validation = fetch_if_exists("pricing_validation_report")

    print("=== FICC Pricing Pipeline Report ===")
    print(f"pricingDate: {args.pricing_date}")

    for name, df in [
        ("readiness", readiness),
        ("curve_dependency", curve),
        ("engine", engine),
        ("validation", validation),
    ]:
        print(f"\n--- {name} ---")
        if isinstance(df, pd.DataFrame) and not df.empty:
            print(df.to_string(index=False))
        else:
            print("(empty)")


if __name__ == "__main__":
    main()
