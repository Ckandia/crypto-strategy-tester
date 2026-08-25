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

def rsi(series, period):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    ag = gain.ewm(alpha=1/period, adjust=False).mean()
    al = loss.ewm(alpha=1/period, adjust=False).mean()
    rs = ag / al.replace(0, np.nan)
    return (100 - 100/(1+rs)).fillna(50)

def adx(df, period):
    up = df["high"].diff()
    down = -df["low"].diff()
    plus = pd.Series(np.where((up > down) & (up > 0), up, 0.0), index=df.index)
    minus = pd.Series(np.where((down > up) & (down > 0), down, 0.0), index=df.index)
    tr = true_range(df)
    avtr = tr.ewm(alpha=1/period, adjust=False).mean()
    pdi = 100 * plus.ewm(alpha=1/period, adjust=False).mean() / avtr.replace(0, np.nan)
    mdi = 100 * minus.ewm(alpha=1/period, adjust=False).mean() / avtr.replace(0, np.nan)
    dx = 100 * (pdi-mdi).abs() / (pdi+mdi).replace(0, np.nan)
    return dx.ewm(alpha=1/period, adjust=False).mean().fillna(0)

def add_indicators(df, cfg):
    x = df.copy()
    x["ema_fast"] = ema(x["close"], cfg.EMA_FAST)
    x["ema_mid"] = ema(x["close"], cfg.EMA_MID)
    x["ema_slow"] = ema(x["close"], cfg.EMA_SLOW)
    x["atr"] = atr(x, cfg.ATR_PERIOD)
    x["rsi"] = rsi(x["close"], cfg.RSI_PERIOD)
    x["adx"] = adx(x, cfg.ADX_PERIOD)
    x["avg_volume"] = x["volume"].rolling(cfg.VOLUME_PERIOD).mean()
    x["breakout_high"] = x["high"].rolling(cfg.BREAKOUT_LOOKBACK).max().shift(1)
    x["breakout_low"] = x["low"].rolling(cfg.BREAKOUT_LOOKBACK).min().shift(1)
    x["prior_swing_low"] = x["low"].rolling(cfg.BREAKOUT_LOOKBACK).min().shift(1)
    x["prior_swing_high"] = x["high"].rolling(cfg.BREAKOUT_LOOKBACK).max().shift(1)
    return x
