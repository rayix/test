# 7226.HK Stock Backtest Strategy & Correlation Analysis

## Project Overview
This project analyzes Hong Kong stock **7226.HK** (Towngas Smart Energy) for:
- **Correlation Analysis**: Finding HK stocks with high positive/negative correlation to 7226.HK
- **Backtest Strategy**: Testing trading strategies based on correlated stocks

## Target Stock
- **Code**: 7226.HK
- **Name**: Towngas Smart Energy (港华智能能源)
- **Sector**: Smart Energy / Utilities

## Scripts

### 1. fetch_stock_data.py
Fetches historical stock data using yfinance.

```bash
python fetch_stock_data.py
```

### 2. find_correlated_v4.py
Analyzes correlations between 7226.HK and other HK stocks using direct Yahoo Finance v8 API.

```bash
python find_correlated_v4.py
```
Output: `correlation_results.csv`

### 3. optimize_strategy.py
Backtests trading strategies based on correlation signals.

```bash
python optimize_strategy.py
```

## Correlation Analysis Results

### Top Positive Correlations (move together with 7226.HK)
| Ticker | Correlation |
|--------|-------------|
| 3033.HK | +0.866 |
| 3088.HK | +0.861 |
| 0241.HK | +0.838 |
| 3636.HK | +0.821 |
| 2828.HK | +0.809 |

### Top Negative Correlations (move opposite to 7226.HK)
| Ticker | Correlation |
|--------|-------------|
| 1870.HK | -0.673 |
| 1234.HK | -0.484 |
| 2768.HK | -0.480 |
| 3288.HK | -0.450 |
| 1171.HK | -0.438 |

## Data Period
- **Date Range**: 2023-05-08 to 2026-05-08 (3 years)
- **Data Points**: ~736 trading days

## Requirements
- Python 3.12+
- pandas, numpy
- yfinance (for data fetching)
- Direct Yahoo Finance API (for correlation analysis)

## Setup
```bash
pip install pandas numpy yfinance
```

## License
MIT
