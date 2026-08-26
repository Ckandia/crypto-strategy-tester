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
        "ema_fast","ema_mid","ema_slow","atr","rsi","adx",
        "avg_volume","volume","open","high","low","close",
        "prior_swing_low"
    ]
    if any(pd_is_bad(row.get(f)) for f in fields):
        return None

    close = float(row["close"])
    open_p = float(row["open"])
    atr = float(row["atr"])
    if atr <= 0:
        return None

    volume_ratio = float(row["volume"]) / float(row["avg_volume"])

    trend_up = (close > row["ema_fast"] and 
                row["ema_fast"] > row["ema_mid"] and 
                row["ema_mid"] > row["ema_slow"])

    rsi_pullback = 35 <= row["rsi"] <= 50
    bullish_candle = close > open_p
    volume_ok = volume_ratio >= cfg.VOLUME_MULTIPLIER
    adx_ok = row["adx"] >= cfg.ADX_MIN

    if trend_up and rsi_pullback and bullish_candle and volume_ok and adx_ok:
        stop = min(float(row["prior_swing_low"]), close - cfg.ATR_STOP_MULTIPLIER * atr)
        if stop < close:
            return Signal("LONG", 100, f"pullback; vol={volume_ratio:.2f}x,rsi={row['rsi']:.1f}", stop)

    return None
