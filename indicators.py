import numpy as np
import pandas as pd

def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def add_indicators(df, cfg):
    x = df.copy()
    # Trend line (bull/bear market divider)
    x["ema_slow"] = ema(x["close"], cfg.EMA_SLOW)
    # Volume
    x["avg_volume"] = x["volume"].rolling(cfg.VOLUME_PERIOD).mean()
    # Stop levels
    x["prior_swing_low"] = x["low"].rolling(cfg.BREAKOUT_LOOKBACK).min().shift(1)
    x["prior_swing_high"] = x["high"].rolling(cfg.BREAKOUT_LOOKBACK).max().shift(1)
    # Taker buy ratio (aggressive buyer %)
    x["taker_buy_ratio"] = x["taker_buy_base"] / x["volume"].replace(0, np.nan)
    return x
