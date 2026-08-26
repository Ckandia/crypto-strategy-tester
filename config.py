SYMBOL = "BTCUSDT"
INTERVAL = "1h"              # CHANGED: 1 hour candles (cleaner trends)
BASE_URL = "https://fapi.binance.com"

START_DATE = "2025-01-01"
END_DATE = "2026-08-01"
STARTING_BALANCE = 1000.0

RISK_PER_TRADE = 0.005
FEE_RATE = 0.0005
SLIPPAGE_BPS = 2.0

EMA_FAST = 20
EMA_MID = 50
EMA_SLOW = 200
ATR_PERIOD = 14
ATR_STOP_MULTIPLIER = 1.5    # Wider stop — 1h moves are bigger
BREAKOUT_LOOKBACK = 20
VOLUME_PERIOD = 20
VOLUME_MULTIPLIER = 1.20
RSI_PERIOD = 14
RSI_LONG_MIN = 55
RSI_SHORT_MAX = 45
ADX_PERIOD = 14
ADX_MIN = 20                 # Slightly lower — 1h trends build slower

TP1_R = 2.0
TP2_R = 4.0
TP1_CLOSE_FRACTION = 0.15
TP2_CLOSE_FRACTION = 0.15
TRAIL_ATR_MULTIPLIER = 2.5

ENTRY_SCORE = 75

# === CHOP FILTER ===
# Only trade when current volatility (ATR) is at or above its recent average.
# 1.0 = average volatility. Below 1.0 = market is dead/choppy.
ATR_RATIO_MIN = 1.0

MAX_POSITIONS = 1
OOS_START = ""
OOS_END = ""
SAVE_CHART = True
