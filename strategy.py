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
        "ema_slow","avg_volume","volume","open","close",
        "prior_swing_low","prior_swing_high",
        "taker_buy_ratio"
    ]
    if any(pd_is_bad(row.get(f)) for f in fields):
        return None

    close = float(row["close"])
    open_p = float(row["open"])
    volume_ratio = float(row["volume"]) / float(row["avg_volume"])
    taker_buy_ratio = float(row["taker_buy_ratio"])

    # Must have above-average volume
    volume_spike = volume_ratio >= cfg.VOLUME_MULTIPLIER

    # === BULL MARKET: Price above EMA 200 ===
    # In a bull market, when buyers are exhausted (taker ratio > 70%)
    # and a red candle appears, SELL the pullback
    if close > row["ema_slow"] and volume_spike:
        buyers_exhausted = taker_buy_ratio >= cfg.TAKER_BUY_RATIO_MAX
        red_candle = close < open_p
        if buyers_exhausted and red_candle:
            stop = float(row["prior_swing_high"])
            if stop > close:
                return Signal("SHORT", 100, f"bull_exhaustion; taker={taker_buy_ratio:.0%},vol={volume_ratio:.2f}x", stop)

    # === BEAR MARKET: Price below EMA 200 ===
    # In a bear market, when sellers are exhausted (taker ratio < 30%)
    # and a green candle appears, BUY the bounce
    if close < row["ema_slow"] and volume_spike:
        sellers_exhausted = taker_buy_ratio <= cfg.TAKER_BUY_RATIO_MIN
        green_candle = close > open_p
        if sellers_exhausted and green_candle:
            stop = float(row["prior_swing_low"])
            if stop < close:
                return Signal("LONG", 100, f"bear_exhaustion; taker={taker_buy_ratio:.0%},vol={volume_ratio:.2f}x", stop)

    return None
