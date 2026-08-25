import time
from datetime import datetime, timezone
import pandas as pd
import requests

COLS = [
    "open_time","open","high","low","close","volume","close_time",
    "quote_volume","trades","taker_buy_base","taker_buy_quote","ignore"
]

def to_millis(date_string):
    dt = datetime.strptime(date_string, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)

def fetch_klines(base_url, symbol, interval, start_date, end_date, limit=1500):
    start_ms = to_millis(start_date)
    end_ms = to_millis(end_date)
    url = f"{base_url}/fapi/v1/klines"
    rows = []
    cursor = start_ms

    print(f"Downloading {symbol} {interval} candles...")
    while cursor < end_ms:
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": cursor,
            "endTime": end_ms,
            "limit": limit,
        }
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break

        rows.extend(batch)
        last_open = batch[-1][0]
        next_cursor = last_open + 1
        if next_cursor <= cursor:
            break
        cursor = next_cursor

        print(f"  {len(rows):,} candles downloaded", end="\r")
        time.sleep(0.15)

        if len(batch) < limit:
            break

    if not rows:
        raise RuntimeError("No candles returned. Check symbol, dates, interval and network access.")

    df = pd.DataFrame(rows, columns=COLS)
    numeric = ["open","high","low","close","volume","quote_volume","trades","taker_buy_base","taker_buy_quote"]
    for c in numeric:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms", utc=True)

    df = df.drop_duplicates("open_time").sort_values("open_time").reset_index(drop=True)
    end_dt = pd.Timestamp(end_date, tz="UTC")
    df = df[df["open_time"] < end_dt].copy()

    print(f"\nLoaded {len(df):,} candles.")
    return df
