#!/usr/bin/env python3
"""Find Hong Kong stocks with high correlation to 7226.HK - curated active stocks."""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
import time
warnings.filterwarnings('ignore')

TARGET = "7226.HK"
YEARS = 3

# Curated list of ACTIVE Hong Kong stocks (real, liquid stocks)
# Covers major sectors: Banks, Energy, Telecom, Tech, Real Estate, Consumer, etc.
HK_STOCKS = [
    # === Hang Seng Index Components (most active) ===
    "0001.HK", "0002.HK", "0003.HK", "0005.HK", "0006.HK",
    "0011.HK", "0012.HK", "0016.HK", "0017.HK", "0027.HK",
    "0066.HK", "0083.HK", "0101.HK", "0168.HK", "0175.HK",
    "0269.HK", "0288.HK", "0291.HK", "0318.HK", "0322.HK",
    "0386.HK", "0388.HK", "0669.HK", "0688.HK", "0739.HK",
    "0760.HK", "0820.HK", "0856.HK", "0861.HK", "0880.HK",
    "0883.HK", "0902.HK", "0939.HK", "0941.HK", "0960.HK",
    "0981.HK", "0992.HK", "0998.HK",
    # === Banks & Finance ===
    "1038.HK", "1044.HK", "1117.HK", "1157.HK", "1288.HK",
    "1336.HK", "1339.HK", "1347.HK", "1658.HK", "1988.HK",
    "2018.HK", "2318.HK", "2328.HK", "2382.HK", "2628.HK",
    "3328.HK", "3690.HK", "3968.HK",
    # === Energy & Utilities ===
    "0267.HK", "0650.HK", "0836.HK", "0857.HK", "1088.HK",
    "1171.HK", "1335.HK", "1685.HK", "1818.HK", "2065.HK",
    "2314.HK", "2678.HK", "2738.HK", "3229.HK", "3300.HK",
    "3315.HK", "3320.HK", "3322.HK", "3636.HK", "3868.HK",
    # === Real Estate ===
    "0489.HK", "0604.HK", "0813.HK", "0823.HK", "0912.HK",
    "1031.HK", "1109.HK", "1177.HK", "1201.HK", "1234.HK",
    "1755.HK", "1995.HK", "2128.HK", "2329.HK", "2359.HK",
    "2638.HK", "2768.HK", "2866.HK", "3308.HK", "3311.HK",
    "3377.HK", "3383.HK", "3900.HK", "6030.HK", "6098.HK",
    "6160.HK", "6818.HK", "6837.HK",
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
    "2917.HK", "2930.HK", "2933.HK", "2966.HK", "2988.HK",
    # === IPO / Growth stocks (post-2020) ===
    "0002.HK", "0960.HK", "2011.HK", "2051.HK", "2076.HK",
    "2100.HK", "2110.HK", "2131.HK", "2137.HK", "2155.HK",
    "2169.HK", "2172.HK", "2186.HK", "2193.HK", "2203.HK",
    "2210.HK", "2281.HK", "2283.HK", "2291.HK", "2293.HK",
    "2295.HK", "2303.HK", "2305.HK", "2309.HK", "2313.HK",
    "2315.HK", "2325.HK", "2337.HK", "2340.HK", "2341.HK",
    "2345.HK", "2347.HK", "2355.HK", "2362.HK", "2373.HK",
    "2378.HK", "2381.HK", "2385.HK", "2388.HK", "2390.HK",
    "2392.HK", "2398.HK", "2412.HK", "2432.HK", "2440.HK",
    "2441.HK", "2448.HK", "2450.HK", "2453.HK", "2456.HK",
    "2457.HK", "2460.HK", "2463.HK", "2468.HK", "2479.HK",
    "2486.HK", "2496.HK", "2499.HK", "2500.HK", "2501.HK",
    "2516.HK", "2518.HK", "2523.HK", "2527.HK", "2531.HK",
    "2547.HK", "2555.HK", "2560.HK", "2566.HK", "2572.HK",
    "2582.HK", "2586.HK", "2598.HK", "2600.HK", "2601.HK",
    "2607.HK", "2610.HK", "2613.HK", "2615.HK", "2617.HK",
    "2623.HK", "2634.HK", "2644.HK", "2647.HK", "2648.HK",
    "2650.HK", "2653.HK", "2658.HK", "2662.HK", "2663.HK",
    "2666.HK", "2669.HK", "2672.HK", "2673.HK", "2683.HK",
    "2690.HK", "2691.HK", "2692.HK", "2695.HK", "2696.HK",
    "2699.HK", "2708.HK", "2712.HK", "2713.HK", "2715.HK",
    "2716.HK", "2717.HK", "2728.HK", "2731.HK", "2733.HK",
    "2736.HK", "2737.HK", "2752.HK", "2772.HK", "2778.HK",
    "2780.HK", "2790.HK", "2795.HK", "2805.HK", "2818.HK",
    "2820.HK", "2822.HK", "2823.HK", "2826.HK", "2827.HK",
    "2830.HK", "2831.HK", "2833.HK", "2843.HK", "2850.HK",
    "2858.HK", "2860.HK", "2863.HK", "2868.HK", "2872.HK",
    "2875.HK", "2880.HK", "2886.HK", "2888.HK", "2891.HK",
    "2898.HK", "2900.HK", "2906.HK", "2911.HK", "2913.HK",
    "2915.HK", "2922.HK", "2931.HK", "2932.HK", "2936.HK",
    "2940.HK", "2942.HK", "2944.HK", "2954.HK", "2958.HK",
    "2961.HK", "2970.HK", "2978.HK", "2982.HK", "2984.HK",
    "2985.HK", "2986.HK", "2993.HK", "2999.HK",
    # === ETFs (Hong Kong major ETFs) ===
    "2800.HK", "2833.HK", "3008.HK", "3012.HK", "3033.HK",
    "3046.HK", "3055.HK", "3068.HK", "3083.HK", "3088.HK",
    "3100.HK", "3110.HK", "3112.HK", "3122.HK", "3130.HK",
    "3147.HK", "3150.HK", "3156.HK", "3165.HK", "3188.HK",
    "3205.HK", "3218.HK", "3223.HK", "3234.HK", "3239.HK",
    "3263.HK", "3273.HK", "3283.HK", "3288.HK", "3303.HK",
    "3319.HK", "3323.HK", "3331.HK", "3341.HK", "3353.HK",
    "3365.HK", "3377.HK", "3383.HK", "3401.HK", "3413.HK",
    "3431.HK", "3443.HK", "3455.HK", "3467.HK", "3479.HK",
    "3491.HK", "3503.HK", "3515.HK", "3527.HK", "3539.HK",
    "3551.HK", "3563.HK", "3575.HK", "3587.HK", "3599.HK",
    "3611.HK", "3623.HK", "3635.HK", "3647.HK", "3659.HK",
    "3671.HK", "3683.HK", "3695.HK", "3707.HK", "3719.HK",
    "3731.HK", "3743.HK", "3755.HK", "3767.HK", "3779.HK",
    "3791.HK", "3803.HK", "3815.HK", "3827.HK", "3839.HK",
    "3851.HK", "3863.HK", "3875.HK", "3887.HK", "3899.HK",
    "3911.HK", "3923.HK", "3935.HK", "3947.HK", "3959.HK",
    "3971.HK", "3977.HK", "3983.HK", "3989.HK", "3995.HK",
]

# Remove duplicates
HK_STOCKS = sorted(list(set(HK_STOCKS)))
# Remove target from list
if TARGET in HK_STOCKS:
    HK_STOCKS.remove(TARGET)

print(f"Target: {TARGET}")
print(f"Total stocks to check: {len(HK_STOCKS)}")
print()

# Date range
end_date = datetime.now()
start_date = end_date - timedelta(days=365 * YEARS)

# Fetch target data
print(f"Fetching {TARGET}...")
try:
    target_data = yf.download(TARGET, start=start_date, end=end_date, progress=False)
    if target_data.empty:
        print(f"ERROR: No data for {TARGET}")
        exit(1)
    
    if isinstance(target_data.columns, pd.MultiIndex):
        target_data.columns = target_data.columns.get_level_values(0)
    
    target_close = target_data['Close'].dropna()
    if hasattr(target_close, 'iloc'):
        target_close = target_close.iloc[:, 0] if target_close.shape[1] > 1 else target_close.iloc[:, 0]
    
    print(f"  Got {len(target_close)} rows, {target_close.index[0].date()} to {target_close.index[-1].date()}")
except Exception as e:
    print(f"ERROR fetching {TARGET}: {e}")
    import traceback; traceback.print_exc()
    exit(1)

# Fetch stocks ONE AT A TIME with small delays to avoid rate limiting
# This is slower but more reliable
all_data = {}
failed = []
print(f"\nFetching {len(HK_STOCKS)} stocks one by one (with delays)...")
for i, ticker in enumerate(HK_STOCKS):
    if i % 50 == 0:
        print(f"  Progress: {i}/{len(HK_STOCKS)} stocks processed...")
    
    try:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False, timeout=10)
        if not data.empty:
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            col = data['Close']
            if hasattr(col, 'iloc'):
                col = col.iloc[:, 0] if col.shape[1] > 1 else col.iloc[:, 0]
            if not col.dropna().empty and len(col.dropna()) > 30:
                all_data[ticker] = col.dropna()
    except Exception:
        failed.append(ticker)
    
    # Small delay every 10 requests to avoid rate limiting
    if i % 10 == 9:
        time.sleep(0.5)

print(f"\nGot valid data for {len(all_data)} stocks")
print(f"Failed/Delisted: {len(failed)} stocks")
if failed[:20]:
    print(f"First failures: {failed[:20]}")
print()

# Calculate correlations
print("Calculating correlations...")
results = []

for ticker, prices in all_data.items():
    try:
        # Align dates
        aligned_target, aligned_other = target_close.align(prices, join='inner')
        
        if len(aligned_target) < 30:
            continue
        
        corr = aligned_target.corr(aligned_other)
        
        if not np.isnan(corr):
            results.append({
                'ticker': ticker,
                'correlation': corr,
                'abs_correlation': abs(corr),
                'data_points': len(aligned_target)
            })
    except Exception as e:
        pass

if not results:
    print("No correlations calculated!")
    exit(1)

df = pd.DataFrame(results)
df = df.sort_values('abs_correlation', ascending=False)

# Top positive correlations (close to 1)
print("\n" + "="*70)
print("POSITIVE CORRELATIONS (corr -> 1) - Move together")
print("="*70)
print(f"{'Rank':<6}{'Ticker':<12}{'Corr':>10}{'Data Pts':>10}")
print("-"*38)

top_pos = df[df['correlation'] > 0].head(30)
for rank, row in enumerate(top_pos.itertuples(), 1):
    print(f"#{rank:<5}{row.ticker:<12}{row.correlation:>10.4f}{row.data_points:>10}")

# Top negative correlations (close to -1)
print("\n" + "="*70)
print("NEGATIVE CORRELATIONS (corr -> -1) - Move opposite")
print("="*70)
print(f"{'Rank':<6}{'Ticker':<12}{'Corr':>10}{'Data Pts':>10}")
print("-"*38)

top_neg = df[df['correlation'] < 0].tail(30).sort_values('correlation')
for rank, row in enumerate(top_neg.itertuples(), 1):
    print(f"#{rank:<5}{row.ticker:<12}{row.correlation:>10.4f}{row.data_points:>10}")

# Summary stats
print("\n" + "="*70)
print("CORRELATION DISTRIBUTION SUMMARY")
print("="*70)
print(f"Total valid correlations: {len(df)}")
print(f"Mean: {df['correlation'].mean():.4f}  |  Median: {df['correlation'].median():.4f}  |  Std: {df['correlation'].std():.4f}")
print()
print(f"corr >  0.90 (near +1):  {len(df[df['correlation'] > 0.90])}")
print(f"0.70 < corr <= 0.90:    {len(df[(df['correlation'] > 0.70) & (df['correlation'] <= 0.90)])}")
print(f"0.50 < corr <= 0.70:    {len(df[(df['correlation'] > 0.50) & (df['correlation'] <= 0.70)])}")
print(f"-0.50 <= corr <= 0.50:  {len(df[(df['correlation'] >= -0.50) & (df['correlation'] <= 0.50)])}")
print(f"-0.70 <= corr < -0.50: {len(df[(df['correlation'] < -0.50) & (df['correlation'] >= -0.70)])}")
print(f"-0.90 <= corr < -0.70: {len(df[(df['correlation'] < -0.70) & (df['correlation'] >= -0.90)])}")
print(f"corr < -0.90 (near -1): {len(df[df['correlation'] < -0.90])}")

# Save results
df.to_csv('correlation_results.csv', index=False)
print(f"\nAll {len(df)} results saved to correlation_results.csv")

# Final highlight: most correlated and most anti-correlated
print("\n" + "="*70)
print("TOP 10 MOST CORRELATED (positive - move together)")
print("="*70)
for rank, row in enumerate(df.head(10).itertuples(), 1):
    bar = "█" * int(row.abs_correlation * 20)
    print(f"  #{rank:2d}  {row.ticker:<10}  {row.correlation:+.4f}  {bar}")

print("\n" + "="*70)
print("TOP 10 MOST ANTI-CORRELATED (negative - move opposite)")
print("="*70)
for rank, row in enumerate(df.tail(10).sort_values('correlation').itertuples(), 1):
    bar = "█" * int(row.abs_correlation * 20)
    print(f"  #{rank:2d}  {row.ticker:<10}  {row.correlation:+.4f}  {bar}")
