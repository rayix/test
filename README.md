# Stock Data Fetcher

A Python project to fetch historical stock data from Yahoo Finance.

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/rayix/test.git
cd test
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Fetch stock data

```bash
python fetch_stock_data.py
```

This will fetch 5 years of day-end data for 7299.HK (Hong Kong stock) and save it to `stock_data.csv`.

### Customize the stock symbol and date range

Edit `fetch_stock_data.py` to change:
- `STOCK_SYMBOL` - The stock ticker (default: "7299.HK")
- `YEARS` - Number of years of historical data (default: 5)

## Output

The script generates:
- `stock_data.csv` - CSV file with historical stock data
- Console output with data summary

## Data Columns

- **Date** - Trading date
- **Open** - Opening price
- **High** - Highest price of the day
- **Low** - Lowest price of the day
- **Close** - Closing price
- **Adj Close** - Adjusted closing price
- **Volume** - Trading volume

## Project Structure

```
test/
├── main.py                # Entry point
├── fetch_stock_data.py    # Stock data fetcher
├── requirements.txt       # Dependencies
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## License

MIT
