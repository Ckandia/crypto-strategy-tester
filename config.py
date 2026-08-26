SYMBOL = "BTCUSDT"
INTERVAL = "5m"              # CHANGED: 5-minute candles
BASE_URL = "https://fapi.binance.com"

START_DATE = "2025-01-01"
END_DATE = "2026-08-01"
STARTING_BALANCE = 1000.0

RISK_PER_TRADE = 0.005
FEE_RATE = 0.0005

# CHANGED: More slippage on fast 5m moves
SLIPPAGE_BPS = 3.0

EMA_FAST = 20
EMA_MID = 50
EMA_SLOW = 200
ATR_PERIOD = 14

# CHANGED: Wider stop — 5m has more noise that knocks you out
ATR_STOP_MULTIPLIER = 2.0

BREAKOUT_LOOKBACK = 20
VOLUME_PERIOD = 20
VOLUME_MULTIPLIER = 1.20
RSI_PERIOD = 14
ADX_PERIOD = 14

# CHANGED: Stronger trend required — 5m is full of fake trends
ADX_MIN = 25

# Single target at 3R
TP1_R = 3.0
TP1_CLOSE_FRACTION = 0.0
TP2_R = 3.0
TP2_CLOSE_FRACTION = 0.0

# CHANGED: Looser trail — 5m wiggles too much
TRAIL_ATR_MULTIPLIER = 3.0

ENTRY_SCORE = 0

MAX_POSITIONS = 1
OOS_START = ""
OOS_END = ""
SAVE_CHART = True
