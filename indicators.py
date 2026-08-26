import pandas as pd

def add_indicators(df, cfg):
    x = df.copy()
    # Volume
    x["avg_volume"] = x["volume"].rolling(cfg.VOLUME_PERIOD).mean()
    # Swing levels
    x["prior_swing_low"] = x["low"].rolling(cfg.BREAKOUT_LOOKBACK).min().shift(1)
    x["prior_swing_high"] = x["high"].rolling(cfg.BREAKOUT_LOOKBACK).max().shift(1)
    # Previous candle for engulfing check
    x["prev_open"] = x["open"].shift(1)
    x["prev_close"] = x["close"].shift(1)
    return x
