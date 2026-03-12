#!/usr/bin/env python
# coding: utf-8

import argparse
import datetime as dt
import time
from pathlib import Path

import pandas as pd
import tushare as ts

import basic
from dataSource.stock_minute_1m_lib import (
    configure_logger,
    fetch_realtime_batch_frame,
    get_active_symbols,
    minute_task_defaults,
    resolve_symbols,
)


def parse_args() -> argparse.Namespace:
    defaults = minute_task_defaults()
    parser = argparse.ArgumentParser(description="Probe rt_min realtime batch capacity for the current Tushare account")
    parser.add_argument("--token", default=basic.token, help="Tushare token")
    parser.add_argument("--symbols", nargs="*", help="Explicit TS codes to use as the probe pool")
    parser.add_argument("--all-active-symbols", action="store_true", help="Use the active A-share stock list as the probe pool")
    parser.add_argument("--limit-symbols", type=int, default=1200, help="Limit the probe pool size when using active symbols")
    parser.add_argument("--batch-sizes", nargs="+", type=int, default=[10, 50, 100, 200, 500, 800, 1000], help="Batch sizes to test")
    parser.add_argument("--freq", default=defaults["freq"], help="Minute frequency")
    parser.add_argument("--pause", type=float, default=defaults["pause"], help="Pause between probe calls in seconds")
    parser.add_argument("--retry-wait", type=float, default=defaults["retryWait"], help="Minimum wait in seconds before retrying a failed Tushare request")
    parser.add_argument("--max-retries", type=int, default=1, help="Maximum retries per probe batch")
    parser.add_argument("--log-dir", default=basic.logDir, help="Log directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logger = configure_logger("logger_ProbeRtMinCapacity", Path(args.log_dir), "ProbeRtMinCapacity.log")

    if args.all_active_symbols:
        symbols = get_active_symbols(args.token, limit_symbols=args.limit_symbols)
    else:
        symbols = resolve_symbols(args.token, explicit_symbols=args.symbols, limit_symbols=args.limit_symbols)
    if not symbols:
        raise ValueError("No symbols resolved for rt_min probe.")

    ts.set_token(args.token)
    trade_date = dt.datetime.now().date()
    probe_rows = []

    for batch_size in args.batch_sizes:
        selected_symbols = symbols[:batch_size]
        started_at = time.time()
        status = "ok"
        error_message = ""
        try:
            frame = fetch_realtime_batch_frame(
                ts_codes=selected_symbols,
                freq=args.freq,
                logger=logger,
                max_retries=args.max_retries,
                pause=args.pause,
                retry_wait=args.retry_wait,
                trade_date=trade_date,
            )
        except Exception as exc:
            frame = pd.DataFrame()
            status = "error"
            error_message = str(exc)

        elapsed_seconds = round(time.time() - started_at, 3)
        returned_rows = len(frame)
        returned_symbols = int(frame["ts_code"].nunique()) if not frame.empty else 0
        max_rows_per_symbol = int(frame.groupby("ts_code").size().max()) if not frame.empty else 0
        likely_truncated = returned_rows >= 1000 or returned_symbols < len(selected_symbols)

        probe_rows.append(
            {
                "batch_size": batch_size,
                "requested_symbols": len(selected_symbols),
                "returned_symbols": returned_symbols,
                "returned_rows": returned_rows,
                "max_rows_per_symbol": max_rows_per_symbol,
                "elapsed_seconds": elapsed_seconds,
                "likely_truncated": likely_truncated,
                "status": status,
                "error": error_message,
            }
        )
        logger.info(
            "Probe batch_size=%d returned_symbols=%d returned_rows=%d max_rows_per_symbol=%d elapsed=%.3fs status=%s",
            batch_size,
            returned_symbols,
            returned_rows,
            max_rows_per_symbol,
            elapsed_seconds,
            status,
        )
        if error_message:
            logger.warning("Probe batch_size=%d error=%s", batch_size, error_message)
        time.sleep(args.pause)

    summary = pd.DataFrame(probe_rows)
    logger.info("rt_min probe summary:\n%s", summary.to_string(index=False))
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()