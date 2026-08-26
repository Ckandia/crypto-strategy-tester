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
        "prior_swing_low"
    ]
    if any(pd_is_bad(row.get(f)) for f in fields):
        return None

    close = float(row["close"])
    open_p = float(row["open"])

    volume_ratio = float(row["volume"]) / float(row["avg_volume"])

    # === VOLUME ONLY ===
    # 1. Volume must be spiking (above average)
    volume_spike = volume_ratio >= cfg.VOLUME_MULTIPLIER

    # 2. Candle must be green (buyers in control)
    green_candle = close > open_p

    if volume_spike and green_candle:
        stop = float(row["prior_swing_low"])
        if stop < close:
            return Signal("LONG", 100, f"volume_spike; vol={volume_ratio:.2f}x", stop)

    # No short trades
    return None
