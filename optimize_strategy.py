#!/usr/bin/env python3
"""Optimize backtest strategy parameters for 7226.HK."""

import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '.')
from fetch_stock_data import fetch_stock_data, STOCK_SYMBOL, YEARS


class BacktestStrategy:
    """Backtest with configurable buy/sell thresholds."""

    def __init__(self, data, buy_threshold=0.20, sell_threshold=0.20, min_hold_days=0):
        self.data = data.copy()
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.min_hold_days = min_hold_days
        self.trades = []
        self.signals = []
        self.position = None
        self.entry_price = None
        self.entry_date = None
        self.highest_price = None
        self.lowest_price = None

    def run(self):
        for date, row in self.data.iterrows():
            price = float(row['Close'])

            if self.position is None:
                if self.highest_price is None:
                    self.highest_price = price
                else:
                    drop_percent = (self.highest_price - price) / self.highest_price
                    if drop_percent >= self.buy_threshold:
                        self.position = 'buy'
                        self.entry_price = price
                        self.entry_date = date
                        self.lowest_price = price
                        self.highest_price = price
                        self.signals.append({'date': date, 'signal': 'BUY', 'price': price})
                    elif price > self.highest_price:
                        self.highest_price = price
            else:
                days_held = (date - self.entry_date).days
                if self.lowest_price is None:
                    self.lowest_price = price
                else:
                    rise_percent = (price - self.lowest_price) / self.lowest_price
                    if rise_percent >= self.sell_threshold and days_held >= self.min_hold_days:
                        profit = price - self.entry_price
                        profit_percent = (profit / self.entry_price) * 100
                        self.trades.append({
                            'entry_date': self.entry_date,
                            'entry_price': self.entry_price,
                            'exit_date': date,
                            'exit_price': price,
                            'profit': profit,
                            'profit_percent': profit_percent,
                            'days_held': days_held
                        })
                        self.position = None
                        self.entry_price = None
                        self.entry_date = None
                        self.highest_price = price
                        self.lowest_price = None
                    elif price < self.lowest_price:
                        self.lowest_price = price

    def get_stats(self):
        if not self.trades:
            return {
                'total_trades': 0, 'win_rate': 0, 'total_profit': -9999,
                'avg_profit_pct': 0, 'sharpe': -9999, 'max_drawdown': 0,
                'best_trade_pct': 0, 'avg_days': 0, 'winning_trades': 0, 'losing_trades': 0
            }
        df = pd.DataFrame(self.trades)
        winning = (df['profit'] > 0).sum()
        win_rate = winning / len(df) * 100
        total_profit = df['profit'].sum()
        avg_profit_pct = df['profit_percent'].mean()
        # Simple Sharpe (avg return / std, annualized)
        std_val = df['profit_percent'].std()
        avg_days = df['days_held'].mean()
        if std_val > 0 and avg_days > 0:
            sharpe = (avg_profit_pct / std_val) * np.sqrt(252 / avg_days)
        else:
            sharpe = 0
        return {
            'total_trades': len(df),
            'winning_trades': int(winning),
            'losing_trades': int(len(df) - winning),
            'win_rate': win_rate,
            'total_profit': total_profit,
            'avg_profit_pct': avg_profit_pct,
            'sharpe': sharpe,
            'max_drawdown': df['profit_percent'].min(),
            'best_trade_pct': df['profit_percent'].max(),
            'avg_days': avg_days,
        }


def main():
    print("Loading stock data...")
    data = fetch_stock_data(STOCK_SYMBOL, YEARS)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    thresholds = [round(x * 0.05, 2) for x in range(1, 11)]   # 0.05 .. 0.50
    min_hold_days_list = [0, 5, 10, 20, 30]

    total_combos = len(thresholds) ** 2 * len(min_hold_days_list)
    print(f"\nGrid search: {len(thresholds)} buy x {len(thresholds)} sell x {len(min_hold_days_list)} min_days = {total_combos} combinations\n")

    best_result = None
    best_params = None
    all_results = []

    for buy_t in thresholds:
        for sell_t in thresholds:
            for min_days in min_hold_days_list:
                bt = BacktestStrategy(data, buy_threshold=buy_t, sell_threshold=sell_t, min_hold_days=min_days)
                bt.run()
                stats = bt.get_stats()
                if stats['total_trades'] == 0:
                    continue
                r = {'buy_t': buy_t, 'sell_t': sell_t, 'min_days': min_days, **stats}
                all_results.append(r)

                if stats['total_profit'] > (best_result['total_profit'] if best_result else -9999):
                    best_result = stats
                    best_params = {'buy_t': buy_t, 'sell_t': sell_t, 'min_days': min_days}

    results_df = pd.DataFrame(all_results)
    top5 = results_df.nlargest(5, 'total_profit')

    print("=" * 80)
    print("TOP 5 最优参数组合（按总收益排序）")
    print("=" * 80)
    for rank, row in enumerate(top5.itertuples(), 1):
        print(f"\n#{rank}  买入阈值: {row.buy_t*100:.0f}%  卖出阈值: {row.sell_t*100:.0f}%  最短持仓: {row.min_days}天")
        print(f"     总收益: ${row.total_profit:.2f}  胜率: {row.win_rate:.1f}%  ({row.winning_trades}胜/{row.losing_trades}负)")
        print(f"     均收益%: {row.avg_profit_pct:+.2f}%  最大亏损: {row.max_drawdown:.2f}%  夏普比: {row.sharpe:.2f}  交易次数: {row.total_trades}")

    bp = best_params
    bt2 = BacktestStrategy(data, buy_threshold=bp['buy_t'], sell_threshold=bp['sell_t'], min_hold_days=bp['min_days'])
    bt2.run()
    df2 = pd.DataFrame(bt2.trades)

    print("\n" + "=" * 80)
    print("BEST STRATEGY")
    print("=" * 80)
    print(f"  买入阈值: {bp['buy_t']*100:.0f}%  (高点回落 {bp['buy_t']*100:.0f}% 买入)")
    print(f"  卖出阈值: {bp['sell_t']*100:.0f}%  (低点回升 {bp['sell_t']*100:.0f}% 卖出)")
    print(f"  最短持仓: {bp['min_days']} 天")
    print()
    print(f"  总收益:    ${best_result['total_profit']:.2f}")
    print(f"  胜率:      {best_result['win_rate']:.1f}%  ({best_result['winning_trades']}胜/{best_result['losing_trades']}负)")
    print(f"  均收益%:   {best_result['avg_profit_pct']:+.2f}%")
    print(f"  最大亏损:  {best_result['max_drawdown']:.2f}%")
    print(f"  最佳交易:  +{best_result['best_trade_pct']:.2f}%")
    print(f"  均持仓:    {best_result['avg_days']:.1f} 天")
    print(f"  夏普比率:  {best_result['sharpe']:.2f}")

    print(f"\nDETAILED TRADES ({len(df2)} trades):")
    print("-" * 80)
    for i, t in enumerate(df2.itertuples(), 1):
        sign = "+" if t.profit > 0 else "-"
        print(f"  #{i:02d}  {str(t.entry_date)[:10]} -> {str(t.exit_date)[:10]}  "
              f"${t.entry_price:.2f} -> ${t.exit_price:.2f}  "
              f"{sign}${abs(t.profit):.2f} ({sign}{abs(t.profit_percent):.1f}%)  {t.days_held}d")

    results_df.sort_values('total_profit', ascending=False).to_csv('optimization_results.csv', index=False)
    print(f"\nAll {len(results_df)} results saved to optimization_results.csv")


if __name__ == "__main__":
    main()
