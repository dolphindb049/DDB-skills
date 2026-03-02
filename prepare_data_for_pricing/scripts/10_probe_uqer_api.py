#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from pricing_common import DatayesClient, load_config


def main() -> None:
    config = load_config()
    client = DatayesClient(config.token)
    pricing_date = config.pricing_date
    first_ticker = config.tickers[0]

    api_cases = [
        ("getBond", "/api/bond/getBond.json", {"ticker": first_ticker}),
        (
            "getBondCfNew",
            "/api/bond/getBondCfNew.json",
            {"ticker": first_ticker, "beginDate": pricing_date, "endDate": pricing_date},
        ),
        ("getBondTicker", "/api/bond/getBondTicker.json", {"pagenum": 1, "pagesize": 20}),
        ("getBondType", "/api/bond/getBondType.json", {"ticker": first_ticker}),
        (
            "getCFETSValuation",
            "/api/bond/getCFETSValuation.json",
            {"ticker": first_ticker, "beginDate": pricing_date, "endDate": pricing_date},
        ),
        (
            "getBondCmIrsCurve",
            "/api/bond/getBondCmIrsCurve.json",
            {
                "beginDate": pricing_date,
                "endDate": pricing_date,
                "curveCD": "01",
                "curveTypeCD": "2",
                "priceTypeCD": "2",
            },
        ),
        ("getFutu", "/api/future/getFutu.json", {"pagenum": 1, "pagesize": 20}),
        ("getFutuCtd", "/api/future/getFutuCtd.json", {"tradeDate": pricing_date}),
        (
            "getMktFutd",
            "/api/market/getMktFutd.json",
            {"beginDate": pricing_date, "endDate": pricing_date, "pagenum": 1, "pagesize": 20},
        ),
        (
            "getMktIBBondd",
            "/api/market/getMktIBBondd.json",
            {"beginDate": pricing_date, "endDate": pricing_date, "pagenum": 1, "pagesize": 20},
        ),
    ]

    summaries: list[dict] = []

    for name, endpoint, params in api_cases:
        try:
            df = client.get(endpoint, params)
            sample = df.head(1).to_dict(orient="records")
            summaries.append(
                {
                    "api": name,
                    "endpoint": endpoint,
                    "params": params,
                    "status": "ok",
                    "rowCount": int(len(df)),
                    "columns": list(df.columns),
                    "sample": sample[0] if sample else {},
                }
            )
            print(f"[OK] {name}: rows={len(df)} cols={len(df.columns)}")
        except Exception as error:
            summaries.append(
                {
                    "api": name,
                    "endpoint": endpoint,
                    "params": params,
                    "status": "error",
                    "error": str(error),
                }
            )
            print(f"[ERR] {name}: {error}")

    output_path = Path(__file__).resolve().parents[1] / "reference" / "sample_data" / "api_probe_summary.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summaries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"saved: {output_path}")


if __name__ == "__main__":
    main()
