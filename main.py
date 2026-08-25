from pathlib import Path
import config
from data import fetch_klines
from indicators import add_indicators
from backtest import run_backtest

def money(x):
    return f"${x:,.2f}"

def main():
    out=Path("results")
    out.mkdir(exist_ok=True)

    print("="*60)
    print("CRYPTO STRATEGY TESTER v1")
    print("BINANCE HISTORICAL BACKTEST — NO LIVE TRADING")
    print("="*60)

    df=fetch_klines(config.BASE_URL,config.SYMBOL,config.INTERVAL,config.START_DATE,config.END_DATE)
    df=add_indicators(df,config)

    print("\nRunning backtest...")
    s,trades,equity=run_backtest(df,config)

    trades.to_csv(out/"trades.csv",index=False)
    equity.to_csv(out/"equity.csv",index=False)

    pf="infinity" if s["profit_factor"]==float("inf") else f'{s["profit_factor"]:.2f}'
    summary=f"""
CRYPTO STRATEGY TESTER RESULTS
==============================
Symbol:              {config.SYMBOL}
Interval:            {config.INTERVAL}
Period:              {config.START_DATE} to {config.END_DATE}

Starting balance:   {money(config.STARTING_BALANCE)}
Net profit:          {money(s["net_profit"])}
Ending balance:      {money(config.STARTING_BALANCE+s["net_profit"])}
Return:              {s["return_pct"]:.2f}%

Trades:              {s["trades"]}
Wins:                {s["wins"]}
Losses:              {s["losses"]}
Win rate:            {s["win_rate"]:.2f}%
Profit factor:       {pf}
Average win:         {money(s["avg_win"])}
Average loss:        {money(s["avg_loss"])}
Maximum drawdown:    {s["max_drawdown_pct"]:.2f}%

Longest win streak:  {s["max_win_streak"]}
Longest loss streak: {s["max_loss_streak"]}

Risk/trade:          {config.RISK_PER_TRADE*100:.2f}%
Fee assumption:      {config.FEE_RATE*100:.3f}% per side
Slippage:            {config.SLIPPAGE_BPS:.1f} bps per side

This is historical research, not a guarantee of future performance.
"""
    print(summary)
    (out/"summary.txt").write_text(summary.strip(),encoding="utf-8")
    print(f"Results saved in: {out.resolve()}")

if __name__=="__main__":
    main()
