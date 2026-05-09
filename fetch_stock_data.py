#!/usr/bin/env python3
"""Fetch historical stock data from Yahoo Finance."""

from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

# Configuration
STOCK_SYMBOL = "7299.HK"  # Hong Kong stock - 7299
YEARS = 5
OUTPUT_FILE = "stock_data.csv"


def fetch_stock_data(symbol, years):
    """
    Fetch historical stock data from Yahoo Finance.
    
    Args:
        symbol (str): Stock ticker symbol (e.g., "7299.HK")
        years (int): Number of years of historical data to fetch
    
    Returns:
        pd.DataFrame: Historical stock data
    """
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * years)
    
    print(f"Fetching data for {symbol}...")
    print(f"Date range: {start_date.date()} to {end_date.date()}")
    print()
    
    try:
        # Download data from Yahoo Finance
        data = yf.download(symbol, start=start_date, end=end_date, progress=True)
        
        if data.empty:
            print(f"Error: No data found for {symbol}")
            return None
        
        return data
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def save_to_csv(data, filename):
    """
    Save stock data to CSV file.
    
    Args:
        data (pd.DataFrame): Stock data
        filename (str): Output CSV filename
    """
    data.to_csv(filename)
    print(f"Data saved to {filename}")


def print_summary(data, symbol):
    """
    Print summary statistics of stock data.
    
    Args:
        data (pd.DataFrame): Stock data
        symbol (str): Stock ticker symbol
    """
    print(f"\n{'='*60}")
    print(f"Summary for {symbol}")
    print(f"{'='*60}")
    print(f"Total records: {len(data)}")
    print(f"Date range: {data.index[0].date()} to {data.index[-1].date()}")
    print(f"\nPrice Statistics (Close):")
    print(f"  Highest: {data['Close'].max():.2f}")
    print(f"  Lowest:  {data['Close'].min():.2f}")
    print(f"  Average: {data['Close'].mean():.2f}")
    print(f"  Latest:  {data['Close'][-1]:.2f}")
    print(f"\nVolume Statistics:")
    print(f"  Average Daily Volume: {data['Volume'].mean():,.0f}")
    print(f"\nFirst 5 records:")
    print(data.head())
    print(f"\nLast 5 records:")
    print(data.tail())
    print(f"{'='*60}\n")


def main():
    """Main function."""
    print("Stock Data Fetcher - Yahoo Finance")
    print("="*60)
    
    # Fetch data
    data = fetch_stock_data(STOCK_SYMBOL, YEARS)
    
    if data is not None:
        # Save to CSV
        save_to_csv(data, OUTPUT_FILE)
        
        # Print summary
        print_summary(data, STOCK_SYMBOL)
        
        print("✓ Success! Stock data has been fetched and saved.")
    else:
        print("✗ Failed to fetch stock data.")


if __name__ == "__main__":
    main()
