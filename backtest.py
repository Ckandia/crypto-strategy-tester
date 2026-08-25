import pandas as pd
from dataclasses import dataclass
from strategy import get_signal

@dataclass
class Position:
    side: str
    entry: float
    stop: float
    qty: float
    remaining: float
    tp1: float
    tp2: float
    tp1_hit: bool
    tp2_hit: bool
    trail: float
    entry_time: object
    score: float

def slip(price, side, entry, bps):
    f = bps / 10000
    if side == "LONG":
        return price * (1 + f if entry else 1 - f)
    return price * (1 - f if entry else 1 + f)

def fees(notional, rate):
    return abs(notional) * rate

def close_piece(pos, qty, price, cfg):
    exit_price = slip(price, pos.side, False, cfg.SLIPPAGE_BPS)
    gross = (exit_price - pos.entry) * qty if pos.side == "LONG" else (pos.entry - exit_price) * qty
    cost = fees(pos.entry * qty, cfg.FEE_RATE) + fees(exit_price * qty, cfg.FEE_RATE)
    return gross - cost, exit_price, cost

def record(pos, row, exit_price, qty, net, reason, cost):
    return {
        "entry_time": pos.entry_time,
        "exit_time": row["close_time"],
        "side": pos.side,
        "entry": pos.entry,
        "exit": exit_price,
        "qty": qty,
        "net_pnl": net,
        "exit_reason": reason,
        "signal_score": pos.score,
        "fees": cost
    }

def stats(trades, equity, start):
    if not trades:
        return dict(trades=0, wins=0, losses=0, win_rate=0, net_profit=0, return_pct=0,
                    profit_factor=0, max_drawdown_pct=0, avg_win=0, avg_loss=0,
                    max_win_streak=0, max_loss_streak=0)

    p = [float(t["net_pnl"]) for t in trades]
    wins = [x for x in p if x > 0]
    losses = [x for x in p if x < 0]
    gross_profit = sum(wins)
    gross_loss = abs(sum(losses))

    e = pd.Series(equity, dtype=float)
    dd = (e - e.cummax()) / e.cummax()
    max_dd = abs(float(dd.min())) * 100

    ws = ls = mws = mls = 0
    for x in p:
        if x > 0:
            ws += 1
            ls = 0
            mws = max(mws, ws)
        else:
            ls += 1
            ws = 0
            mls = max(mls, ls)

    return {
        "trades": len(p),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": len(wins) / len(p) * 100,
        "net_profit": sum(p),
        "return_pct": sum(p) / start * 100,
        "profit_factor": gross_profit / gross_loss if gross_loss else float("inf"),
        "max_drawdown_pct": max_dd,
        "avg_win": sum(wins) / len(wins) if wins else 0,
        "avg_loss": sum(losses) / len(losses) if losses else 0,
        "max_win_streak": mws,
        "max_loss_streak": mls
    }

def run_backtest(df, cfg):
    balance = float(cfg.STARTING_BALANCE)
    equity = [balance]
    trades = []
    pos = None

    for i in range(1, len(df) - 1):
        row = df.iloc[i]
        nxt = df.iloc[i + 1]

        if pos is not None:
            high = float(row["high"])
            low = float(row["low"])
            atr = float(row["atr"]) if pd.notna(row["atr"]) else 0.0

            if pos.side == "LONG":
                if low <= pos.stop:
                    net, ex, cost = close_piece(pos, pos.remaining, pos.stop, cfg)
                    balance += net
                    trades.append(record(pos, row, ex, pos.remaining, net, "STOP", cost))
                    pos = None
                else:
                    if not pos.tp1_hit and high >= pos.tp1:
                        q = min(pos.qty * cfg.TP1_CLOSE_FRACTION, pos.remaining)
                        net, ex, cost = close_piece(pos, q, pos.tp1, cfg)
                        balance += net
                        pos.remaining -= q
                        pos.tp1_hit = True
                        pos.stop = pos.entry
                        trades.append(record(pos, row, ex, q, net, "TP1", cost))

                    if pos.tp1_hit and not pos.tp2_hit and high >= pos.tp2:
                        q = min(pos.qty * cfg.TP2_CLOSE_FRACTION, pos.remaining)
                        net, ex, cost = close_piece(pos, q, pos.tp2, cfg)
                        balance += net
                        pos.remaining -= q
                        pos.tp2_hit = True
                        trades.append(record(pos, row, ex, q, net, "TP2", cost))

                    if pos.tp2_hit and pos.remaining > 0:
                        trail = float(row["close"]) - cfg.TRAIL_ATR_MULTIPLIER * atr
                        pos.trail = trail if pos.trail is None else max(pos.trail, trail)
                        pos.stop = max(pos.stop, pos.trail)

            else:  # SHORT
                if high >= pos.stop:
                    net, ex, cost = close_piece(pos, pos.remaining, pos.stop, cfg)
                    balance += net
                    trades.append(record(pos, row, ex, pos.remaining, net, "STOP", cost))
                    pos = None
                else:
                    if not pos.tp1_hit and low <= pos.tp1:
                        q = min(pos.qty * cfg.TP1_CLOSE_FRACTION, pos.remaining)
                        net, ex, cost = close_piece(pos, q, pos.tp1, cfg)
                        balance += net
                        pos.remaining -= q
                        pos.tp1_hit = True
                        pos.stop = pos.entry
                        trades.append(record(pos, row, ex, q, net, "TP1", cost))

                    if pos.tp1_hit and not pos.tp2_hit and low <= pos.tp2:
                        q = min(pos.qty * cfg.TP2_CLOSE_FRACTION, pos.remaining)
                        net, ex, cost = close_piece(pos, q, pos.tp2, cfg)
                        balance += net
                        pos.remaining -= q
                        pos.tp2_hit = True
                        trades.append(record(pos, row, ex, q, net, "TP2", cost))

                    if pos.tp2_hit and pos.remaining > 0:
                        trail = float(row["close"]) + cfg.TRAIL_ATR_MULTIPLIER * atr
                        pos.trail = trail if pos.trail is None else min(pos.trail, trail)
                        pos.stop = min(pos.stop, pos.trail)

        # Look for new entry only if flat
        if pos is None:
            sig = get_signal(row, cfg)
            if sig:
                entry = slip(float(nxt["open"]), sig.side, True, cfg.SLIPPAGE_BPS)
                distance = (entry - sig.stop_reference) if sig.side == "LONG" else (sig.stop_reference - entry)
                if distance <= 0:
                    continue

                risk = balance * cfg.RISK_PER_TRADE
                qty = risk / distance
                if qty <= 0 or pd.isna(qty):
                    continue

                if sig.side == "LONG":
                    tp1 = entry + distance * cfg.TP1_R
                    tp2 = entry + distance * cfg.TP2_R
                else:
                    tp1 = entry - distance * cfg.TP1_R
                    tp2 = entry - distance * cfg.TP2_R

                pos = Position(
                    side=sig.side,
                    entry=entry,
                    stop=sig.stop_reference,
                    qty=qty,
                    remaining=qty,
                    tp1=tp1,
                    tp2=tp2,
                    tp1_hit=False,
                    tp2_hit=False,
                    trail=None,
                    entry_time=nxt["open_time"],
                    score=sig.score
                )
                # Entry fee is handled inside close_piece when position closes

        equity.append(balance)

    # Close any open position at the last candle
    if pos is not None:
        last = df.iloc[-1]
        net, ex, cost = close_piece(pos, pos.remaining, float(last["close"]), cfg)
        balance += net
        trades.append(record(pos, last, ex, pos.remaining, net, "END_OF_TEST", cost))

    equity.append(balance)
    return stats(trades, equity, cfg.STARTING_BALANCE), pd.DataFrame(trades), pd.DataFrame({"equity": equity})
