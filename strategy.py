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
        "avg_volume","breakout_high","breakout_low",
        "prior_swing_low","prior_swing_high"
    ]
    if any(pd_is_bad(row.get(f)) for f in fields):
        return None

    close = float(row["close"])
    atr = float(row["atr"])
    if atr <= 0:
        return None

    volume_ratio = float(row["volume"]) / float(row["avg_volume"])

    long_score = 0
    long_score += 10 if close > row["ema_fast"] else 0
    long_score += 10 if row["ema_fast"] > row["ema_mid"] else 0
    long_score += 15 if row["ema_mid"] > row["ema_slow"] else 0
    long_score += 10 if row["rsi"] >= cfg.RSI_LONG_MIN else 0
    long_score += 10 if row["adx"] >= cfg.ADX_MIN else 0
    long_score += 15 if volume_ratio >= cfg.VOLUME_MULTIPLIER else 0
    long_score += 20 if close > row["breakout_high"] else 0

    short_score = 0
    short_score += 10 if close < row["ema_fast"] else 0
    short_score += 10 if row["ema_fast"] < row["ema_mid"] else 0
    short_score += 15 if row["ema_mid"] < row["ema_slow"] else 0
    short_score += 10 if row["rsi"] <= cfg.RSI_SHORT_MAX else 0
    short_score += 10 if row["adx"] >= cfg.ADX_MIN else 0
    short_score += 15 if volume_ratio >= cfg.VOLUME_MULTIPLIER else 0
    short_score += 20 if close < row["breakout_low"] else 0

    # === FALSE BREAKOUT FILTER ===
    # Price must push at least 0.15% past the breakout level.
    # This stops the bot from buying fake breakouts that immediately reverse.
    breakout_buffer = close * 0.0015

    if long_score >= cfg.ENTRY_SCORE and long_score > short_score:
        # Must be clearly above the breakout, not just 1 tick
        if close <= row["breakout_high"] + breakout_buffer:
            return None
        stop = min(float(row["prior_swing_low"]), close - cfg.ATR_STOP_MULTIPLIER * atr)
        if stop < close:
            return Signal("LONG", long_score, f"trend+breakout+momentum+volume; volume={volume_ratio:.2f}x", stop)

    if short_score >= cfg.ENTRY_SCORE and short_score > long_score:
        # Must be clearly below the breakout, not just 1 tick
        if close >= row["breakout_low"] - breakout_buffer:
            return None
        stop = max(float(row["prior_swing_high"]), close + cfg.ATR_STOP_MULTIPLIER * atr)
        if stop > close:
            return Signal("SHORT", short_score, f"trend+breakout+momentum+volume; volume={volume_ratio:.2f}x", stop)

    return None
