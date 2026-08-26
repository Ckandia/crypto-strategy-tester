SYMBOL = "BTCUSDT"
INTERVAL = "15m"
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

# === STOP LOSS: tighter = cut losers faster ===
ATR_STOP_MULTIPLIER = 1.0

BREAKOUT_LOOKBACK = 20
VOLUME_PERIOD = 20
VOLUME_MULTIPLIER = 1.20
RSI_PERIOD = 14
RSI_LONG_MIN = 55
RSI_SHORT_MAX = 45
ADX_PERIOD = 14

# === TREND STRENGTH: higher = only strong trends ===
ADX_MIN = 22

# === PROFIT TARGETS: bigger = let winners run ===
TP1_R = 2.0
TP2_R = 4.0

# === SELL LESS EARLY: keep 70% for the big run ===
TP1_CLOSE_FRACTION = 0.15
TP2_CLOSE_FRACTION = 0.15

# === TRAILING STOP: looser = don't kill winners ===
TRAIL_ATR_MULTIPLIER = 2.5

# === ENTRY SCORE: slightly easier to pass since we added a chop filter ===
ENTRY_SCORE = 75

MAX_POSITIONS = 1

# Out-of-sample dates (leave "" to ignore for now)
OOS_START = ""
OOS_END = ""

# Save equity curve chart?
SAVE_CHART = True
