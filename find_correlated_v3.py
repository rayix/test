#!/usr/bin/env python3
"""Find HK stocks correlated with 7226.HK - fast targeted approach."""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
import time
warnings.filterwarnings('ignore')

TARGET = "7226.HK"
YEARS = 3

# Focused list of MAJOR active Hong Kong stocks (~150 real active stocks)
HK_ACTIVE = [
    # === Hang Seng constituents (real active) ===
    "0001.HK", "0002.HK", "0003.HK", "0005.HK", "0006.HK",
    "0011.HK", "0012.HK", "0016.HK", "0017.HK", "0027.HK",
    "0066.HK", "0083.HK", "0101.HK", "0168.HK", "0175.HK",
    "0269.HK", "0288.HK", "0291.HK", "0318.HK", "0322.HK",
    "0386.HK", "0388.HK", "0669.HK", "0688.HK", "0739.HK",
    "0760.HK", "0820.HK", "0856.HK", "0861.HK", "0880.HK",
    "0883.HK", "0902.HK", "0939.HK", "0941.HK", "0960.HK",
    "0981.HK", "0992.HK", "0998.HK",
    # Banks & Financial
    "1038.HK", "1044.HK", "1288.HK", "1336.HK", "1339.HK",
    "1658.HK", "1988.HK", "2318.HK", "2328.HK", "2382.HK",
    "2628.HK", "3328.HK", "3690.HK", "3968.HK",
    # Energy & Utilities
    "0267.HK", "0836.HK", "0857.HK", "1088.HK", "1171.HK",
    "1335.HK", "1818.HK", "2314.HK", "2678.HK", "3229.HK",
    "3315.HK", "3636.HK",
    # Real Estate
    "0489.HK", "0604.HK", "0813.HK", "0823.HK", "0912.HK",
    "1031.HK", "1109.HK", "1177.HK", "1201.HK", "1234.HK",
    "1755.HK", "1995.HK", "2128.HK", "2329.HK", "2359.HK",
    "2638.HK", "2768.HK", "2866.HK", "3308.HK", "3311.HK",
    "3377.HK", "3383.HK", "3900.HK", "6030.HK", "6098.HK",
    "6160.HK", "6818.HK",
    # Tech & Internet
    "0494.HK", "0700.HK", "1028.HK", "1090.HK", "1347.HK",
    "1448.HK", "1494.HK", "1508.HK", "1810.HK", "1870.HK",
    "1890.HK", "2007.HK", "2319.HK", "2611.HK", "3001.HK",
    "3015.HK", "3257.HK", "3312.HK", "3345.HK", "3519.HK",
    "3558.HK", "3660.HK", "3799.HK", "3816.HK", "3864.HK",
    "3948.HK", "4190.HK",
    # Consumer & Retail
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
    # Major ETFs
    "2800.HK", "2833.HK", "3008.HK", "3012.HK", "3033.HK",
    "3046.HK", "3055.HK", "3068.HK", "3083.HK", "3088.HK",
    "3100.HK", "3110.HK", "3112.HK", "3122.HK", "3130.HK",
    "3147.HK", "3150.HK", "3156.HK", "3165.HK", "3188.HK",
    "3205.HK", "3218.HK", "3223.HK", "3234.HK", "3239.HK",
    "3263.HK", "3273.HK", "3283.HK", "3288.HK",
]

HK_ACTIVE = sorted(list(set(HK_ACTIVE)))
if TARGET in HK_ACTIVE:
    HK_ACTIVE.remove(TARGET)

print(f"Target: {TARGET}")
print(f"Total stocks to check: {len(HK_ACTIVE)}")

end_date = datetime.now()
start_date = end_date - timedelta(days=365 * YEARS)

# Fetch target
print(f"\nFetching {TARGET}...")
target_data = yf.download(TARGET, start=start_date, end=end_date, progress=False)
if target_data.empty:
    print(f"ERROR: No data for {TARGET}"); exit(1)
if isinstance(target_data.columns, pd.MultiIndex):
    target_data.columns = target_data.columns.get_level_values(0)
target_close = target_data['Close']
if hasattr(target_close, 'iloc'):
    target_close = target_close.iloc[:, 0] if target_close.shape[1] > 1 else target_close.iloc[:, 0]
target_close = target_close.dropna()
print(f"  {len(target_close)} rows loaded")

# Batch download: 10 at a time, 1s delay between batches
all_data = {}
BATCH = 10
DELAY = 1.5  # seconds between batches

print(f"\nDownloading {len(HK_ACTIVE)} stocks in batches of {BATCH}...")
for i in range(0, len(HK_ACTIVE), BATCH):
    batch = HK_ACTIVE[i:i+BATCH]
    batch_num = i // BATCH + 1
    total_batches = (len(HK_ACTIVE) + BATCH - 1) // BATCH
    
    if batch_num % 5 == 1:
        print(f"  Batch {batch_num}/{total_batches}: {batch[0]} ... {batch[-1]}")
    
    try:
        data = yf.download(batch, start=start_date, end=end_date, progress=False, threads=True, timeout=15)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        
        for ticker in batch:
            try:
                col = data['Close'][ticker] if ticker in data['Close'].columns else None
                if col is not None:
                    c = col.dropna()
                    if not c.empty and len(c) > 30:
                        all_data[ticker] = c
            except Exception:
                pass
    except Exception as e:
        pass  # skip bad batches
    
    time.sleep(DELAY)

print(f"\nValid data: {len(all_data)} stocks")

# Calculate correlations
print("Computing correlations...")
results = []
for ticker, prices in all_data.items():
    try:
        at, ao = target_close.align(prices, join='inner')
        if len(at) < 30:
            continue
        corr = at.corr(ao)
        if not np.isnan(corr):
            results.append({
                'ticker': ticker,
                'correlation': round(corr, 4),
                'abs_correlation': round(abs(corr), 4),
                'data_points': len(at)
            })
    except:
        pass

df = pd.DataFrame(results).sort_values('abs_correlation', ascending=False)
print(f"Calculated: {len(df)} correlations\n")

# ---- OUTPUT ----
sep = "="*72

# Positive
print(f"\n{sep}")
print("POSITIVE CORRELATIONS (corr -> +1) - Move in SAME direction")
print(sep)
print(f"{'#':<4}{'Ticker':<12}{'Corr':>10}{'Points':>8}  Visualization")
print("-"*55)
for rank, row in enumerate(df[df['correlation'] > 0].head(20).itertuples(), 1):
    bar = "█" * int(row.abs_correlation * 20)
    print(f"#{rank:<3}{row.ticker:<12}{row.correlation:>+10.4f}{row.data_points:>8}  {bar}")

# Negative
print(f"\n{sep}")
print("NEGATIVE CORRELATIONS (corr -> -1) - Move in OPPOSITE direction")
print(sep)
print(f"{'#':<4}{'Ticker':<12}{'Corr':>10}{'Points':>8}  Visualization")
print("-"*55)
for rank, row in enumerate(df[df['correlation'] < 0].tail(20).sort_values('correlation').itertuples(), 1):
    bar = "█" * int(row.abs_correlation * 20)
    print(f"#{rank:<3}{row.ticker:<12}{row.correlation:>+10.4f}{row.data_points:>8}  {bar}")

# Distribution
print(f"\n{sep}")
print("CORRELATION DISTRIBUTION")
print(sep)
print(f"Total: {len(df)} | Mean={df['correlation'].mean():.3f} | Median={df['correlation'].median():.3f} | Std={df['correlation'].std():.3f}")
print()
print(f"  corr >  0.90 (near +1):  {len(df[df['correlation'] > 0.90])}")
print(f"  0.70 < corr <= 0.90:    {len(df[(df['correlation'] > 0.70) & (df['correlation'] <= 0.90)])}")
print(f"  0.50 < corr <= 0.70:    {len(df[(df['correlation'] > 0.50) & (df['correlation'] <= 0.70)])}")
print(f"  0.30 < corr <= 0.50:    {len(df[(df['correlation'] > 0.30) & (df['correlation'] <= 0.50)])}")
print(f"  -0.30 <= corr <= 0.30:  {len(df[(df['correlation'] >= -0.30) & (df['correlation'] <= 0.30)])}")
print(f"  -0.50 < corr < -0.30:  {len(df[(df['correlation'] < -0.30) & (df['correlation'] >= -0.50)])}")
print(f"  -0.70 < corr < -0.50:  {len(df[(df['correlation'] < -0.50) & (df['correlation'] >= -0.70)])}")
print(f"  -0.90 < corr < -0.70:  {len(df[(df['correlation'] < -0.70) & (df['correlation'] >= -0.90)])}")
print(f"  corr <  -0.90 (near -1): {len(df[df['correlation'] < -0.90])}")

df.to_csv('correlation_results.csv', index=False)
print(f"\nSaved: correlation_results.csv ({len(df)} rows)")
