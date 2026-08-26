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
        "ema_fast","ema_mid","ema_slow","atr","adx",
        "avg_volume","breakout_high",
        "prior_swing_low"
    ]
    if any(pd_is_bad(row.get(f)) for f in fields):
        return None

    close = float(row["close"])
    atr = float(row["atr"])
    if atr <= 0:
        return None

    volume_ratio = float(row["volume"]) / float(row["avg_volume"])

    # === LONG-ONLY SIMPLE RULES ===
    # 1. Trend is up: close > fast > mid > slow
    trend_up = (close > row["ema_fast"] and 
                row["ema_fast"] > row["ema_mid"] and 
                row["ema_mid"] > row["ema_slow"])

    # 2. Breakout with buffer (avoid fake-outs)
    breakout_level = float(row["breakout_high"])
    breakout_buffer = close * 0.0015
    clear_breakout = close > breakout_level + breakout_buffer

    # 3. Volume confirmation
    volume_ok = volume_ratio >= cfg.VOLUME_MULTIPLIER

    # 4. Trend strength
    adx_ok = row["adx"] >= cfg.ADX_MIN

    if trend_up and clear_breakout and volume_ok and adx_ok:
        stop = min(float(row["prior_swing_low"]), close - cfg.ATR_STOP_MULTIPLIER * atr)
        if stop < close:
            return Signal("LONG", 100, f"uptrend+breakout+volume; vol={volume_ratio:.2f}x", stop)

    # No short trades — we only ride the bull trend
    return None
