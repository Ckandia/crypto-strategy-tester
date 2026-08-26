import pandas as pd

def add_indicators(df, cfg):
    x = df.copy()
    # Only volume and raw price levels
    x["avg_volume"] = x["volume"].rolling(cfg.VOLUME_PERIOD).mean()
    x["prior_swing_low"] = x["low"].rolling(cfg.BREAKOUT_LOOKBACK).min().shift(1)
    x["prior_swing_high"] = x["high"].rolling(cfg.BREAKOUT_LOOKBACK).max().shift(1)
    return x
