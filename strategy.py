import pandas as pd
import numpy as np
from dataclasses import dataclass

@dataclass
class Signal:
    side: str
    score: float
    reason: str
    stop_reference: float

def pd_is_bad(v):
    return pd.isna(v) or v is None

def get_signal(row, cfg):
    fields = [
        "avg_volume","volume","open","close",
        "prior_swing_low","prior_swing_high",
        "prev_open","prev_close"
    ]
    if any(pd_is_bad(row.get(f)) for f in fields):
        return None

    close = float(row["close"])
    open_p = float(row["open"])
    prev_close = float(row["prev_close"])
    prev_open = float(row["prev_open"])

    volume_ratio = float(row["volume"]) / float(row["avg_volume"])
    volume_spike = volume_ratio >= cfg.VOLUME_MULTIPLIER

    # === LONG: Bullish Engulfing ===
    # Yesterday red, today green, today's body swallows yesterday's whole
    prev_bearish = prev_close < prev_open
    current_bullish = close > open_p
    engulfs_long = (open_p <= prev_close) and (close >= prev_open)
    bullish_engulfing = prev_bearish and current_bullish and engulfs_long

    if volume_spike and bullish_engulfing:
        stop = float(row["prior_swing_low"])
        if stop < close:
            return Signal("LONG", 100, f"engulfing_long+vol; vol={volume_ratio:.2f}x", stop)

    # === SHORT: Bearish Engulfing ===
    # Yesterday green, today red, today's body swallows yesterday's whole
    prev_bullish = prev_close > prev_open
    current_bearish = close < open_p
    engulfs_short = (open_p >= prev_close) and (close <= prev_open)
    bearish_engulfing = prev_bullish and current_bearish and engulfs_short

    if volume_spike and bearish_engulfing:
        stop = float(row["prior_swing_high"])
        if stop > close:
            return Signal("SHORT", 100, f"engulfing_short+vol; vol={volume_ratio:.2f}x", stop)

    return None
