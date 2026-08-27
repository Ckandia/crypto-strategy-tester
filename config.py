SYMBOL = "BTCUSDT"
INTERVAL = "15m"
BASE_URL = "https://fapi.binance.com"

START_DATE = "2025-01-01"
END_DATE = "2026-08-01"
STARTING_BALANCE = 1000.0

RISK_PER_TRADE = 0.005
FEE_RATE = 0.0005
SLIPPAGE_BPS = 2.0

# === TREND ===
EMA_SLOW = 200
ATR_PERIOD = 14

# === LEVELS (Support/Resistance) ===
BREAKOUT_LOOKBACK = 20
# How close price must come to test support/resistance (0.005 = 0.5%)
LEVEL_BUFFER = 0.005

# === VOLUME ===
VOLUME_PERIOD = 20
VOLUME_MULTIPLIER = 1.20

# === EXIT ===
# Dynamic stop follows price (0.005 = 0.5% behind best price)
TRAIL_PERCENT = 0.005
# Safety target at 3R
TP1_R = 3.0
TP1_CLOSE_FRACTION = 0.0

ENTRY_SCORE = 0
MAX_POSITIONS = 1
OOS_START = ""
OOS_END = ""
SAVE_CHART = True
