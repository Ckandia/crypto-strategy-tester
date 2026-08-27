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
        "ema_slow","atr","avg_volume","volume",
        "open","high","low","close",
        "prior_swing_low","prior_swing_high"
    ]
    if any(pd_is_bad(row.get(f)) for f in fields):
        return None

    close = float(row["close"])
    open_p = float(row["open"])
    high = float(row["high"])
    low = float(row["low"])
    atr = float(row["atr"])
    if atr <= 0:
        return None

    volume_ratio = float(row["volume"]) / float(row["avg_volume"])
    volume_spike = volume_ratio >= cfg.VOLUME_MULTIPLIER

    # === LONG: Buy the dip to support in an uptrend ===
    # 1. Trend is UP (price above EMA 200)
    trend_up = close > row["ema_slow"]

    # 2. Price tested support (came within 0.5% of prior swing low or touched it)
    #    AND closed back ABOVE it (rejection/bounce)
    swing_low = float(row["prior_swing_low"])
    tested_support = low <= swing_low * (1 + cfg.LEVEL_BUFFER)
    bounced = close > swing_low

    # 3. Buyers stepping in (green candle)
    green_candle = close > open_p

    if trend_up and tested_support and bounced and green_candle and volume_spike:
        stop = min(swing_low, close - cfg.ATR_STOP_MULTIPLIER * atr) if hasattr(cfg, 'ATR_STOP_MULTIPLIER') else swing_low
        if stop < close:
            return Signal("LONG", 100, f"support_bounce; vol={volume_ratio:.2f}x,swing={swing_low:.0f}", stop)

    # === SHORT: Sell the rally to resistance in a downtrend ===
    # 1. Trend is DOWN (price below EMA 200)
    trend_down = close < row["ema_slow"]

    # 2. Price tested resistance (came within 0.5% of prior swing high or touched it)
    #    AND closed back BELOW it (rejection)
    swing_high = float(row["prior_swing_high"])
    tested_resistance = high >= swing_high * (1 - cfg.LEVEL_BUFFER)
    rejected = close < swing_high

    # 3. Sellers stepping in (red candle)
    red_candle = close < open_p

    if trend_down and tested_resistance and rejected and red_candle and volume_spike:
        stop = max(swing_high, close + cfg.ATR_STOP_MULTIPLIER * atr) if hasattr(cfg, 'ATR_STOP_MULTIPLIER') else swing_high
        if stop > close:
            return Signal("SHORT", 100, f"resistance_reject; vol={volume_ratio:.2f}x,swing={swing_high:.0f}", stop)

    return None
