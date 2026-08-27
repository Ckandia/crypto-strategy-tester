import numpy as np
import pandas as pd

def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def true_range(df):
    prev = df["close"].shift(1)
    return pd.concat([
        df["high"] - df["low"],
        (df["high"] - prev).abs(),
        (df["low"] - prev).abs()
    ], axis=1).max(axis=1)

def atr(df, period):
    return true_range(df).ewm(alpha=1/period, adjust=False).mean()

def add_indicators(df, cfg):
    x = df.copy()
    # Trend
    x["ema_slow"] = ema(x["close"], cfg.EMA_SLOW)
    # Volatility
    x["atr"] = atr(x, cfg.ATR_PERIOD)
    # Volume
    x["avg_volume"] = x["volume"].rolling(cfg.VOLUME_PERIOD).mean()
    # Support / Resistance levels
    x["prior_swing_low"] = x["low"].rolling(cfg.BREAKOUT_LOOKBACK).min().shift(1)
    x["prior_swing_high"] = x["high"].rolling(cfg.BREAKOUT_LOOKBACK).max().shift(1)
    return x
