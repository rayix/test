#!/usr/bin/env python3
"""Backtest trading strategy: Buy on 20% drop, Sell on 20% rise."""

import pandas as pd
from fetch_stock_data import fetch_stock_data, STOCK_SYMBOL, YEARS


class BacktestStrategy:
    """20% Drop/Rise Trading Strategy Backtest."""
    
    def __init__(self, data, threshold=0.20):
        """
        Initialize backtest strategy.
        
        Args:
            data (pd.DataFrame): Historical stock data
            threshold (float): Buy/Sell threshold (default 20%)
        """
        self.data = data.copy()
        self.threshold = threshold
        self.trades = []
        self.signals = []
        self.position = None  # 'buy' or None
        self.entry_price = None
        self.entry_date = None
        self.highest_price = None
        self.lowest_price = None
    
    def run(self):
        """Run the backtest strategy."""
        print(f"Running backtest strategy with {self.threshold*100:.0f}% threshold...")
        print(f"Stock: {STOCK_SYMBOL}")
        print(f"Data points: {len(self.data)}")
        print()
        
        for idx, (date, row) in enumerate(self.data.iterrows()):
            price = row['Close']
            
            if self.position is None:
                # No position - look for BUY signal (20% drop)
                if self.highest_price is None:
                    self.highest_price = price
                else:
                    drop_percent = (self.highest_price - price) / self.highest_price
                    
                    if drop_percent >= self.threshold:
                        # BUY signal
                        self.position = 'buy'
                        self.entry_price = price
                        self.entry_date = date
                        self.lowest_price = price
                        self.highest_price = price
                        
                        self.signals.append({
                            'date': date,
                            'signal': 'BUY',
                            'price': price,
                            'reason': f'{drop_percent*100:.2f}% drop from ${self.highest_price:.2f}'
                        })
                    elif price > self.highest_price:
                        self.highest_price = price
            else:
                # In position - look for SELL signal (20% rise)
                if self.lowest_price is None:
                    self.lowest_price = price
                else:
                    rise_percent = (price - self.lowest_price) / self.lowest_price
                    
                    if rise_percent >= self.threshold:
                        # SELL signal
                        profit = price - self.entry_price
                        profit_percent = (profit / self.entry_price) * 100
                        days_held = (date - self.entry_date).days
                        
                        self.trades.append({
                            'entry_date': self.entry_date,
                            'entry_price': self.entry_price,
                            'exit_date': date,
                            'exit_price': price,
                            'profit': profit,
                            'profit_percent': profit_percent,
                            'days_held': days_held
                        })
                        
                        self.signals.append({
                            'date': date,
                            'signal': 'SELL',
                            'price': price,
                            'reason': f'{rise_percent*100:.2f}% rise from ${self.lowest_price:.2f}'
                        })
                        
                        self.position = None
                        self.entry_price = None
                        self.entry_date = None
                        self.highest_price = price
                        self.lowest_price = None
                    elif price < self.lowest_price:
                        self.lowest_price = price
    
    def print_results(self):
        """Print backtest results."""
        if not self.trades:
            print("No completed trades found.")
            return
        
        trades_df = pd.DataFrame(self.trades)
        
        total_profit = trades_df['profit'].sum()
        total_profit_percent = trades_df['profit_percent'].mean()
        winning_trades = (trades_df['profit'] > 0).sum()
        losing_trades = (trades_df['profit'] < 0).sum()
        win_rate = (winning_trades / len(trades_df)) * 100 if len(trades_df) > 0 else 0
        
        print("="*80)
        print("BACKTEST RESULTS")
        print("="*80)
        print(f"Strategy: Buy on 20% drop, Sell on 20% rise")
        print(f"Stock: {STOCK_SYMBOL}")
        print(f"Period: {self.data.index[0].date()} to {self.data.index[-1].date()}")
        print()
        print("SUMMARY:")
        print(f"  Total Trades: {len(trades_df)}")
        print(f"  Winning Trades: {winning_trades}")
        print(f"  Losing Trades: {losing_trades}")
        print(f"  Win Rate: {win_rate:.2f}%")
        print(f"  Total Profit: ${total_profit:.2f}")
        print(f"  Average Profit per Trade: ${trades_df['profit'].mean():.2f}")
        print(f"  Average Profit %: {total_profit_percent:.2f}%")
        print(f"  Best Trade: ${trades_df['profit'].max():.2f} ({trades_df['profit_percent'].max():.2f}%)")
        print(f"  Worst Trade: ${trades_df['profit'].min():.2f} ({trades_df['profit_percent'].min():.2f}%)")
        print(f"  Average Days per Trade: {trades_df['days_held'].mean():.1f}")
        print()
        print("="*80)
        print("DETAILED TRADES:")
        print("="*80)
        
        for idx, trade in enumerate(trades_df.iterrows(), 1):
            t = trade[1]
            print(f"\nTrade #{idx}:")
            print(f"  Entry:  {t['entry_date'].date()} @ ${t['entry_price']:.2f}")
            print(f"  Exit:   {t['exit_date'].date()} @ ${t['exit_price']:.2f}")
            print(f"  Profit: ${t['profit']:.2f} ({t['profit_percent']:.2f}%)")
            print(f"  Days Held: {t['days_held']}")
        
        print()
        print("="*80)
        
        # Save to CSV
        trades_df.to_csv('backtest_trades.csv', index=False)
        print(f"Trades saved to backtest_trades.csv")
    
    def get_trades_df(self):
        """Return trades as DataFrame."""
        return pd.DataFrame(self.trades)


def main():
    """Main function."""
    print("Stock Backtest Strategy")
    print("="*80)
    print()
    
    # Fetch stock data
    data = fetch_stock_data(STOCK_SYMBOL, YEARS)
    
    if data is None:
        print("Failed to fetch stock data.")
        return
    
    print()
    
    # Run backtest
    backtest = BacktestStrategy(data, threshold=0.20)
    backtest.run()
    
    # Print results
    backtest.print_results()


if __name__ == "__main__":
    main()
