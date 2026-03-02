#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import pandas as pd

from pricing_common import DatayesClient, load_config, pick_fixed_bond_rows


def _first_row(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}
    return df.head(1).to_dict(orient="records")[0]


def main() -> None:
    config = load_config()
    client = DatayesClient(config.token)
    pricing_date = config.pricing_date

    base_dir = Path(__file__).resolve().parents[1] / "reference" / "sample_data"
    base_dir.mkdir(parents=True, exist_ok=True)

    curve_df = client.get(
        "/api/bond/getBondCmIrsCurve.json",
        {
            "beginDate": pricing_date,
            "endDate": pricing_date,
            "curveCD": "01",
            "curveTypeCD": "2",
            "priceTypeCD": "2",
        },
    )
    curve_df.to_json(base_dir / "raw_irs_curve.json", orient="records", force_ascii=False, indent=2)

    selected_bond_rows: list[dict] = []
    selected_cfets_rows: list[dict] = []

    for ticker in config.tickers:
        bond_df = client.get("/api/bond/getBond.json", {"ticker": ticker})
        picked = pick_fixed_bond_rows(bond_df, ticker)
        if picked.empty:
            continue
        row = picked.iloc[0].to_dict()
        selected_bond_rows.append(row)

        cfets_df = client.get(
            "/api/bond/getCFETSValuation.json",
            {"ticker": str(ticker), "beginDate": pricing_date, "endDate": pricing_date},
        )
        if not cfets_df.empty:
            selected_cfets_rows.extend(cfets_df.to_dict(orient="records"))

    pd.DataFrame(selected_bond_rows).to_json(
        base_dir / "raw_bond_info.json", orient="records", force_ascii=False, indent=2
    )
    pd.DataFrame(selected_cfets_rows).to_json(
        base_dir / "raw_cfets_valuation.json", orient="records", force_ascii=False, indent=2
    )

    market_df = client.get(
        "/api/market/getMktIBBondd.json",
        {"beginDate": pricing_date, "endDate": pricing_date, "pagenum": 1, "pagesize": 200},
    )
    market_df.to_json(base_dir / "raw_ib_bond_market.json", orient="records", force_ascii=False, indent=2)

    known_treasury_tickers = [
        "240025",
        "250015",
        "250013",
        "250012",
        "250010",
        "250011",
        "250001",
        "240021",
        "2400102",
        "2500004",
        "2500005",
    ]
    market_tickers = market_df["ticker"].dropna().astype(str).unique().tolist()[:48]
    candidate_tickers = list(dict.fromkeys(known_treasury_tickers + market_tickers))

    case2_rows: list[dict] = []
    for ticker in candidate_tickers:
        if len(case2_rows) >= 6:
            break
        try:
            bond_df = client.get("/api/bond/getBond.json", {"ticker": ticker})
            fixed_rows = pick_fixed_bond_rows(bond_df, ticker)
            if fixed_rows.empty:
                continue
            fixed_rows = fixed_rows[fixed_rows["typeName"].astype(str).str.contains("国债", na=False)]
            if fixed_rows.empty:
                continue

            bond_row = fixed_rows.iloc[0].to_dict()
            cfets_df = client.get(
                "/api/bond/getCFETSValuation.json",
                {"ticker": str(ticker), "beginDate": pricing_date, "endDate": pricing_date},
            )
            if cfets_df.empty:
                continue
            cfets_row = cfets_df.iloc[0].to_dict()

            case2_rows.append(
                {
                    "ticker": str(ticker),
                    "secID": str(bond_row.get("secID")),
                    "secShortName": str(bond_row.get("secShortName")),
                    "firstAccrDate": str(bond_row.get("firstAccrDate")),
                    "maturityDate": str(bond_row.get("maturityDate")),
                    "coupon": float(bond_row.get("coupon", 0.0)),
                    "cpnFreqCD": str(bond_row.get("cpnFreqCD")),
                    "couponTypeCD": str(bond_row.get("couponTypeCD")),
                    "typeName": str(bond_row.get("typeName")),
                    "ytm": float(cfets_row.get("ytm", 0.0)),
                    "netPx": float(cfets_row.get("netPx", 0.0)),
                    "tradeDate": str(cfets_row.get("tradeDate")),
                }
            )
        except Exception as error:
            print(f"skip ticker={ticker}: {error}")
            continue

    pd.DataFrame(case2_rows).to_json(
        base_dir / "case2_bond_basket.json", orient="records", force_ascii=False, indent=2
    )

    print("=== download summary ===")
    print(f"irs_curve rows: {len(curve_df)}")
    print(f"case1 bond rows: {len(selected_bond_rows)}")
    print(f"case1 cfets rows: {len(selected_cfets_rows)}")
    print(f"market rows: {len(market_df)}")
    print(f"case2 basket rows: {len(case2_rows)}")
    print(f"sample curve row: {_first_row(curve_df)}")


if __name__ == "__main__":
    main()
