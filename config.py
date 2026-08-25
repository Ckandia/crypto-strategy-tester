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
ATR_STOP_MULTIPLIER = 1.5
BREAKOUT_LOOKBACK = 20
VOLUME_PERIOD = 20
VOLUME_MULTIPLIER = 1.20
RSI_PERIOD = 14
RSI_LONG_MIN = 55
RSI_SHORT_MAX = 45
ADX_PERIOD = 14
ADX_MIN = 18

# === PROFIT TARGETS (bigger = hold longer for bigger wins) ===
TP1_R = 1.5
TP2_R = 3.0

# === HOW MUCH TO SELL AT EACH TARGET (smaller = keep more for the big run) ===
TP1_CLOSE_FRACTION = 0.20
TP2_CLOSE_FRACTION = 0.20

TRAIL_ATR_MULTIPLIER = 1.5

# === ENTRY SCORE (higher = pickier, only takes the best trades) ===
ENTRY_SCORE = 80

MAX_POSITIONS = 1

# Out-of-sample dates (leave "" to ignore for now)
OOS_START = ""
OOS_END = ""

# Save equity curve chart?
SAVE_CHART = True
