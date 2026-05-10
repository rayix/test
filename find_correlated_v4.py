#!/usr/bin/env python3
"""Find HK stocks correlated with 7226.HK using direct Yahoo Finance v8 API."""

import urllib.request
import json
import time
import numpy as np
import pandas as pd
from datetime import datetime

TARGET = "7226.HK"

# MAJOR active Hong Kong stocks (curated, ~280 real active stocks)
HK_STOCKS = sorted(list(set([
    # === Hang Seng Index constituents ===
    "0001.HK", "0002.HK", "0003.HK", "0005.HK", "0006.HK",
    "0011.HK", "0012.HK", "0016.HK", "0017.HK", "0027.HK",
    "0066.HK", "0083.HK", "0101.HK", "0168.HK", "0175.HK",
    "0269.HK", "0288.HK", "0291.HK", "0318.HK", "0322.HK",
    "0386.HK", "0388.HK", "0669.HK", "0688.HK", "0739.HK",
    "0760.HK", "0820.HK", "0856.HK", "0861.HK", "0880.HK",
    "0883.HK", "0902.HK", "0939.HK", "0941.HK", "0960.HK",
    "0981.HK", "0992.HK", "0998.HK",
    # === Banks & Finance ===
    "1038.HK", "1044.HK", "1288.HK", "1336.HK", "1339.HK",
    "1658.HK", "1988.HK", "2318.HK", "2328.HK", "2382.HK",
    "2628.HK", "3328.HK", "3690.HK", "3968.HK",
    # === Energy & Utilities ===
    "0267.HK", "0836.HK", "0857.HK", "1088.HK", "1171.HK",
    "1335.HK", "1818.HK", "2314.HK", "2678.HK", "3229.HK",
    "3315.HK", "3636.HK",
    # === Real Estate ===
    "0489.HK", "0604.HK", "0813.HK", "0823.HK", "0912.HK",
    "1031.HK", "1109.HK", "1177.HK", "1201.HK", "1234.HK",
    "1755.HK", "1995.HK", "2128.HK", "2329.HK", "2359.HK",
    "2638.HK", "2768.HK", "2866.HK", "3308.HK", "3311.HK",
    "3377.HK", "3383.HK", "3900.HK", "6030.HK", "6098.HK",
    "6160.HK", "6818.HK",
    # === Tech & Internet ===
    "0494.HK", "0700.HK", "1028.HK", "1090.HK", "1347.HK",
    "1448.HK", "1494.HK", "1508.HK", "1810.HK", "1870.HK",
    "1890.HK", "2007.HK", "2319.HK", "2611.HK", "3001.HK",
    "3015.HK", "3257.HK", "3312.HK", "3345.HK", "3519.HK",
    "3558.HK", "3660.HK", "3799.HK", "3816.HK", "3864.HK",
    "3948.HK", "4190.HK",
    # === Consumer & Retail ===
    "0177.HK", "0218.HK", "0241.HK", "0330.HK", "0390.HK",
    "0520.HK", "0531.HK", "0592.HK", "0602.HK", "0610.HK",
    "0655.HK", "0682.HK", "0780.HK", "0830.HK", "0893.HK",
    "0934.HK", "1045.HK", "1052.HK", "1060.HK", "1099.HK",
    "1112.HK", "1135.HK", "1146.HK", "1164.HK", "1181.HK",
    "1190.HK", "1211.HK", "1249.HK", "1297.HK", "1313.HK",
    "1343.HK", "1456.HK", "1509.HK", "1513.HK", "1548.HK",
    "1579.HK", "1708.HK", "1731.HK", "1766.HK", "1788.HK",
    "1816.HK", "1848.HK", "1858.HK", "1860.HK", "1877.HK",
    "1881.HK", "1898.HK", "1910.HK", "1919.HK", "1928.HK",
    "1951.HK", "1963.HK", "1970.HK", "1971.HK", "1985.HK",
    "2013.HK", "2020.HK", "2057.HK", "2078.HK", "2092.HK",
    "2111.HK", "2138.HK", "2165.HK", "2192.HK", "2202.HK",
    "2232.HK", "2255.HK", "2266.HK", "2282.HK", "2298.HK",
    "2333.HK", "2342.HK", "2371.HK", "2383.HK", "2400.HK",
    "2442.HK", "2455.HK", "2462.HK", "2498.HK", "2522.HK",
    "2558.HK", "2562.HK", "2590.HK", "2599.HK", "2606.HK",
    "2616.HK", "2618.HK", "2651.HK", "2656.HK", "2686.HK",
    "2698.HK", "2700.HK", "2718.HK", "2720.HK", "2722.HK",
    "2769.HK", "2771.HK", "2777.HK", "2789.HK", "2809.HK",
    "2828.HK", "2845.HK", "2855.HK", "2877.HK", "2883.HK",
    "2890.HK", "2908.HK", "2912.HK", "2914.HK", "2916.HK",
    "2917.HK", "2930.HK", "2933.HK",
    # === Major ETFs ===
    "2800.HK", "2833.HK", "3008.HK", "3012.HK", "3033.HK",
    "3046.HK", "3055.HK", "3068.HK", "3083.HK", "3088.HK",
    "3100.HK", "3110.HK", "3112.HK", "3122.HK", "3130.HK",
    "3147.HK", "3150.HK", "3156.HK", "3165.HK", "3188.HK",
    "3205.HK", "3218.HK", "3223.HK", "3234.HK", "3239.HK",
    "3263.HK", "3273.HK", "3283.HK", "3288.HK",
])))

if TARGET in HK_STOCKS:
    HK_STOCKS.remove(TARGET)

print(f"Target: {TARGET}")
print(f"Stocks to check: {len(HK_STOCKS)}")

# ---- Direct Yahoo Finance v8 API ----
def fetch_yahoo_v8(ticker, max_retries=3):
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
           f"?interval=1d&range=3y")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Origin": "https://finance.yahoo.com",
        "Referer": "https://finance.yahoo.com/",
    }
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            result = data.get("chart", {}).get("result", [])
            if result:
                timestamps = result[0].get("timestamp", [])
                closes = (result[0]
                          .get("indicators", {})
                          .get("quote", [{}])[0]
                          .get("close", []))
                if closes and len(closes) > 30:
                    # Build aligned series
                    dates = pd.to_datetime(timestamps, unit="s")
                    series = pd.Series(closes, index=dates)
                    series = series.dropna()
                    if len(series) > 30:
                        return series
            return None
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    return None

# ---- Fetch target ----
print(f"\nFetching {TARGET}...")
target_series = fetch_yahoo_v8(TARGET)
if target_series is None:
    print(f"ERROR: Could not fetch {TARGET}")
    exit(1)
print(f"  Got {len(target_series)} data points")
print(f"  Range: {target_series.index[0].date()} to {target_series.index[-1].date()}")

# ---- Fetch all stocks in batches ----
# Yahoo Finance seems to allow reasonable requests with this header
# Use 10 stocks per request, 0.8s delay between requests
BATCH = 10
DELAY = 0.8
all_data = {}
total_batches = (len(HK_STOCKS) + BATCH - 1) // BATCH

print(f"\nFetching {len(HK_STOCKS)} stocks in {total_batches} batches...")
for batch_num in range(total_batches):
    start_i = batch_num * BATCH
    batch = HK_STOCKS[start_i:start_i + BATCH]
    
    if (batch_num + 1) % 10 == 1 or batch_num == 0:
        print(f"  Batch {batch_num + 1}/{total_batches}: {batch[0]} ...")
    
    # Fetch each stock in batch (one by one for reliability)
    for ticker in batch:
        series = fetch_yahoo_v8(ticker)
        if series is not None:
            all_data[ticker] = series
        time.sleep(0.1)  # small delay between individual requests
    
    time.sleep(DELAY)

print(f"\nValid data fetched: {len(all_data)} stocks")

# ---- Calculate correlations ----
print("Computing correlations...")
results = []

target_aligned = target_series.sort_index()
for ticker, prices in all_data.items():
    try:
        prices_aligned = prices.sort_index()
        # Align on common dates
        common_idx = target_aligned.index.intersection(prices_aligned.index)
        if len(common_idx) < 30:
            continue
        
        t = target_aligned.loc[common_idx]
        p = prices_aligned.loc[common_idx]
        
        corr = t.corr(p)
        if not np.isnan(corr):
            results.append({
                "ticker": ticker,
                "correlation": round(float(corr), 4),
                "abs_correlation": round(float(abs(corr)), 4),
                "data_points": len(common_idx),
            })
    except Exception:
        pass

df = pd.DataFrame(results).sort_values("abs_correlation", ascending=False).reset_index(drop=True)
print(f"Calculated {len(df)} correlations\n")

# ---- Print results ----
sep = "=" * 72
bar_max = 20

# Positive
print(f"\n{sep}")
print("POSITIVE CORRELATIONS (corr -> +1) - Move in SAME direction")
print(sep)
print(f"{'#':<5}{'Ticker':<14}{'Corr':>10}{'Points':>8}  Visualization")
print("-" * 58)
for i, row in df[df["correlation"] > 0].head(20).iterrows():
    bar = "█" * int(row["abs_correlation"] * bar_max)
    rank = df[df["correlation"] > 0].index.get_loc(i) + 1
    print(f"#{rank:<4}{row['ticker']:<14}{row['correlation']:>+10.4f}{row['data_points']:>8}  {bar}")

# Negative
print(f"\n{sep}")
print("NEGATIVE CORRELATIONS (corr -> -1) - Move in OPPOSITE direction")
print(sep)
print(f"{'#':<5}{'Ticker':<14}{'Corr':>10}{'Points':>8}  Visualization")
print("-" * 58)
neg_df = df[df["correlation"] < 0].sort_values("correlation").head(20)
for i, row in neg_df.iterrows():
    bar = "█" * int(row["abs_correlation"] * bar_max)
    rank = df[df["correlation"] < 0].sort_values("correlation").index.get_loc(i) + 1
    print(f"#{rank:<4}{row['ticker']:<14}{row['correlation']:>+10.4f}{row['data_points']:>8}  {bar}")

# Distribution
print(f"\n{sep}")
print("CORRELATION DISTRIBUTION SUMMARY")
print(sep)
print(f"Total valid: {len(df)}  |  Mean={df['correlation'].mean():.3f}  |  "
      f"Median={df['correlation'].median():.3f}  |  Std={df['correlation'].std():.3f}")
print()
ranges = [
    ("corr >  0.90 (near +1)", df[df["correlation"] > 0.90]),
    ("0.70 < corr <= 0.90",   df[(df["correlation"] > 0.70) & (df["correlation"] <= 0.90)]),
    ("0.50 < corr <= 0.70",   df[(df["correlation"] > 0.50) & (df["correlation"] <= 0.70)]),
    ("0.30 < corr <= 0.50",   df[(df["correlation"] > 0.30) & (df["correlation"] <= 0.50)]),
    ("-0.30 <= corr <= 0.30", df[(df["correlation"] >= -0.30) & (df["correlation"] <= 0.30)]),
    ("-0.50 < corr < -0.30", df[(df["correlation"] < -0.30) & (df["correlation"] >= -0.50)]),
    ("-0.70 < corr < -0.50", df[(df["correlation"] < -0.50) & (df["correlation"] >= -0.70)]),
    ("-0.90 < corr < -0.70", df[(df["correlation"] < -0.70) & (df["correlation"] >= -0.90)]),
    ("corr < -0.90 (near -1)", df[df["correlation"] < -0.90]),
]
for label, sub in ranges:
    print(f"  {label:<25} {len(sub):>5} stocks")

# Save
df.to_csv("correlation_results.csv", index=False)
print(f"\nSaved: correlation_results.csv ({len(df)} rows)")

# Final highlight
print(f"\n{sep}")
print("TOP 10 MOST CORRELATED (positive - move together)")
print(sep)
for rank, row in enumerate(df.head(10).itertuples(), 1):
    bar = "█" * int(row.abs_correlation * bar_max)
    print(f"  #{rank:2d}  {row.ticker:<14} {row.correlation:+.4f}  {bar}")

print(f"\n{sep}")
print("TOP 10 MOST ANTI-CORRELATED (negative - move opposite)")
print(sep)
for rank, row in enumerate(df.tail(10).sort_values("correlation").itertuples(), 1):
    bar = "█" * int(row.abs_correlation * bar_max)
    print(f"  #{rank:2d}  {row.ticker:<14} {row.correlation:+.4f}  {bar}")
