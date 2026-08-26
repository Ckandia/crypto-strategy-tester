import numpy as np
import pandas as pd

def add_indicators(df, cfg):
    x = df.copy()
    # Volume
    x["avg_volume"] = x["volume"].rolling(cfg.VOLUME_PERIOD).mean()
    # Swing levels for stops
    x["prior_swing_low"] = x["low"].rolling(cfg.BREAKOUT_LOOKBACK).min().shift(1)
    x["prior_swing_high"] = x["high"].rolling(cfg.BREAKOUT_LOOKBACK).max().shift(1)
    # Taker buy ratio: what % of volume is aggressive buyers?
    x["taker_buy_ratio"] = x["taker_buy_base"] / x["volume"].replace(0, np.nan)
    return x
