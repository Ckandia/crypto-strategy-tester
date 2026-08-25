# Crypto Strategy Tester — Binance Theory Test v1

BACKTESTING ONLY. This version does not place Binance orders and does not need an API key.

Theory tested:
- trade with the prevailing trend
- require a market-structure breakout
- require momentum confirmation
- require above-average volume
- use ATR/structure-based stops
- take partial profits at 1R and 2R
- trail the remaining position

It uses Binance USD-M Futures historical candles, so both LONG and SHORT signals can be tested.

## Run in GitHub Codespaces

Upload all files to a GitHub repository, then open:
Code -> Codespaces -> Create codespace on main

In the terminal:

```bash
pip install -r requirements.txt
python main.py
```

No API key is required.

The program creates:
- results/summary.txt
- results/trades.csv
- results/equity.csv

Default test:
BTCUSDT, 15m, 2025-01-01 through 2026-08-01.

Edit config.py to change symbol, timeframe, dates, risk, fees, and strategy thresholds.

IMPORTANT: A positive backtest is not proof of future profitability. We will next perform out-of-sample testing and then demo/forward testing before considering any live trading.

Never put Binance API keys or secrets into this repository.
