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
        "taker_buy_ratio"
    ]
    if any(pd_is_bad(row.get(f)) for f in fields):
        return None

    close = float(row["close"])
    open_p = float(row["open"])
    volume_ratio = float(row["volume"]) / float(row["avg_volume"])
    taker_buy_ratio = float(row["taker_buy_ratio"])

    # Must have above-average volume to avoid dead periods
    volume_spike = volume_ratio >= cfg.VOLUME_MULTIPLIER

    # === LONG: Sellers exhausted ===
    # Taker buy ratio very LOW (< 30%) means 70%+ was aggressive selling
    # Sellers are exhausted -> reversal up
    sellers_exhausted = taker_buy_ratio <= cfg.TAKER_BUY_RATIO_MIN
    green_reversal = close > open_p  # buyers stepping in

    if volume_spike and sellers_exhausted and green_reversal:
        stop = float(row["prior_swing_low"])
        if stop < close:
            return Signal("LONG", 100, f"seller_exhaustion; taker={taker_buy_ratio:.0%},vol={volume_ratio:.2f}x", stop)

    # === SHORT: Buyers exhausted ===
    # Taker buy ratio very HIGH (> 70%) means 70%+ was aggressive buying
    # Buyers are exhausted -> reversal down
    buyers_exhausted = taker_buy_ratio >= cfg.TAKER_BUY_RATIO_MAX
    red_reversal = close < open_p  # sellers stepping in

    if volume_spike and buyers_exhausted and red_reversal:
        stop = float(row["prior_swing_high"])
        if stop > close:
            return Signal("SHORT", 100, f"buyer_exhaustion; taker={taker_buy_ratio:.0%},vol={volume_ratio:.2f}x", stop)

    return None
