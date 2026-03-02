#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import pandas as pd

from pricing_common import connect_ddb, load_config, read_json_records


def _curve_date(trade_date: pd.Timestamp, tenor: str) -> pd.Timestamp:
    base = pd.Timestamp(trade_date)
    normalized = str(tenor).upper().strip()
    if normalized.endswith("D"):
        return base + pd.DateOffset(days=int(normalized[:-1]))
    if normalized.endswith("W"):
        return base + pd.DateOffset(weeks=int(normalized[:-1]))
    if normalized.endswith("M"):
        return base + pd.DateOffset(months=int(normalized[:-1]))
    if normalized.endswith("Y"):
        return base + pd.DateOffset(years=int(normalized[:-1]))
    return base


def append_raw_bond_info(session, db_path: str, frame: pd.DataFrame) -> None:
    if frame.empty:
        return
    payload = frame.copy()
    payload["firstAccrDate"] = pd.to_datetime(payload["firstAccrDate"])
    payload["maturityDate"] = pd.to_datetime(payload["maturityDate"])
    session.upload({"tmp_raw_bond": payload})
    session.run(
        f'''
loadTable("{db_path}", "raw_bond_info").append!(
    select symbol(string(secID)) as secID,
           symbol(string(ticker)) as ticker,
           symbol(string(exchangeCD)) as exchangeCD,
           string(secShortName) as secShortName,
           string(issuer) as issuer,
           symbol(string(couponTypeCD)) as couponTypeCD,
           symbol(string(cpnFreqCD)) as cpnFreqCD,
           symbol(string(paymentCD)) as paymentCD,
           double(coupon) as coupon,
           date(firstAccrDate) as firstAccrDate,
           date(maturityDate) as maturityDate,
           string(typeName) as typeName,
           symbol(string(typeID)) as typeID,
           symbol(string(listStatusCD)) as listStatusCD
    from tmp_raw_bond
)
'''
    )


def append_raw_cfets(session, db_path: str, frame: pd.DataFrame) -> None:
    if frame.empty:
        return
    payload = frame.copy()
    payload["tradeDate"] = pd.to_datetime(payload["tradeDate"])
    session.upload({"tmp_raw_cfets": payload})
    session.run(
        f'''
loadTable("{db_path}", "raw_cfets_valuation").append!(
    select date(tradeDate) as tradeDate,
           symbol(string(secID)) as secID,
           symbol(string(ticker)) as ticker,
           string(secShortName) as secShortName,
           string(bondType) as bondType,
           double(grossPx) as grossPx,
           double(netPx) as netPx,
           double(ytm) as ytm,
           string(couponType) as couponType,
           double(modifiedDuration) as modifiedDuration,
           double(convexity) as convexity,
           double(baseRate) as baseRate
    from tmp_raw_cfets
)
'''
    )


def append_raw_irs_curve(session, db_path: str, frame: pd.DataFrame) -> None:
    if frame.empty:
        return
    payload = frame.copy()
    payload["tradeDate"] = pd.to_datetime(payload["tradeDate"])
    payload["curveDate"] = payload.apply(
        lambda row: _curve_date(pd.Timestamp(row["tradeDate"]), str(row["maturity"])),
        axis=1,
    )
    session.upload({"tmp_raw_curve": payload})
    session.run(
        f'''
loadTable("{db_path}", "raw_irs_curve").append!(
    select date(tradeDate) as tradeDate,
           date(curveDate) as curveDate,
           string(curveName) as curveName,
           symbol(string(curveCD)) as curveCD,
           symbol(string(curveTypeCD)) as curveTypeCD,
           symbol(string(priceTypeCD)) as priceTypeCD,
           string(maturity) as maturity,
           double(yield) as curveYield
    from tmp_raw_curve
)
'''
    )


def append_raw_ib_market(session, db_path: str, frame: pd.DataFrame) -> None:
    if frame.empty:
        return
    payload = frame.copy()
    payload["tradeDate"] = pd.to_datetime(payload["tradeDate"])
    if "turnoverValue" not in payload.columns:
        payload["turnoverValue"] = pd.NA
    session.upload({"tmp_raw_ib": payload})
    session.run(
        f'''
loadTable("{db_path}", "raw_ib_bond_market").append!(
    select date(tradeDate) as tradeDate,
           symbol(string(secID)) as secID,
           symbol(string(ticker)) as ticker,
           string(secShortName) as secShortName,
           symbol(string(exchangeCD)) as exchangeCD,
           double(closePrice) as closePrice,
           double(wAvgPrice) as wAvgPrice,
           double(preCloseYield) as preCloseYield,
           double(wAvgYield) as wAvgYield,
           double(turnoverVol) as turnoverVol,
           double(turnoverValue) as turnoverValue
    from tmp_raw_ib
)
'''
    )


def append_case2_basket(session, db_path: str, frame: pd.DataFrame) -> None:
    if frame.empty:
        return
    payload = frame.copy()
    payload["tradeDate"] = pd.to_datetime(payload["tradeDate"])
    payload["firstAccrDate"] = pd.to_datetime(payload["firstAccrDate"])
    payload["maturityDate"] = pd.to_datetime(payload["maturityDate"])
    session.upload({"tmp_case2": payload})
    session.run(
        f'''
loadTable("{db_path}", "case2_bond_basket").append!(
    select date(tradeDate) as tradeDate,
           symbol(string(secID)) as secID,
           symbol(string(ticker)) as ticker,
           string(secShortName) as secShortName,
           date(firstAccrDate) as firstAccrDate,
           date(maturityDate) as maturityDate,
           double(coupon) as coupon,
           symbol(string(cpnFreqCD)) as cpnFreqCD,
           symbol(string(couponTypeCD)) as couponTypeCD,
           string(typeName) as typeName,
           double(ytm) as ytm,
           double(netPx) as netPx
    from tmp_case2
)
'''
    )


def main() -> None:
    config = load_config()
    base_dir = Path(__file__).resolve().parents[1] / "reference" / "sample_data"

    raw_bond = read_json_records(str(base_dir / "raw_bond_info.json"))
    raw_cfets = read_json_records(str(base_dir / "raw_cfets_valuation.json"))
    raw_curve = read_json_records(str(base_dir / "raw_irs_curve.json"))
    raw_market = read_json_records(str(base_dir / "raw_ib_bond_market.json"))
    case2_basket = read_json_records(str(base_dir / "case2_bond_basket.json"))

    session = connect_ddb(config)
    append_raw_bond_info(session, config.db_path, raw_bond)
    append_raw_cfets(session, config.db_path, raw_cfets)
    append_raw_irs_curve(session, config.db_path, raw_curve)
    append_raw_ib_market(session, config.db_path, raw_market)
    append_case2_basket(session, config.db_path, case2_basket)

    counts = session.run(
        f'''
select * from (
    select "raw_bond_info" as tableName, count(*) as rows from loadTable("{config.db_path}", "raw_bond_info")
    union all
    select "raw_cfets_valuation" as tableName, count(*) as rows from loadTable("{config.db_path}", "raw_cfets_valuation")
    union all
    select "raw_irs_curve" as tableName, count(*) as rows from loadTable("{config.db_path}", "raw_irs_curve")
    union all
    select "raw_ib_bond_market" as tableName, count(*) as rows from loadTable("{config.db_path}", "raw_ib_bond_market")
    union all
    select "case2_bond_basket" as tableName, count(*) as rows from loadTable("{config.db_path}", "case2_bond_basket")
)
'''
    )
    print(counts)


if __name__ == "__main__":
    main()
