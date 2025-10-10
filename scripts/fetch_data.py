import ccxt
import pandas as pd
import time
from datetime import datetime
import os

# === Initialize Binance ===
binance = ccxt.binance()

symbol = 'BTC/USDT'
start_time = int(pd.Timestamp('2025-10-01 00:00:00').timestamp() * 1000)
end_time   = int(pd.Timestamp('2025-10-08 00:00:00').timestamp() * 1000)

# === Output directory ===
output_dir = "../data/raw/one_week"
os.makedirs(output_dir, exist_ok=True)

# === Fetch parameters ===
all_trades = []
since = start_time
chunk_size = 1000   # trades per API call
save_every = 10     # batches before saving

batch_count = 0
print(f"Starting from: {pd.to_datetime(since, unit='ms')}")

while since < end_time:
    try:
        trades = binance.fetch_trades(symbol, since=since, limit=chunk_size)
    except Exception as e:
        print(f"\nError fetching trades: {e}. Retrying in 10s...")
        time.sleep(10)
        continue

    if not trades:
        print("\nNo more trades returned. Exiting loop.")
        break

    all_trades.extend(trades)
    since = trades[-1]['timestamp'] + 1
    batch_count += 1

    # Save periodically
    if batch_count % save_every == 0:
        df_chunk = pd.DataFrame(all_trades)
        df_chunk['timestamp'] = pd.to_datetime(df_chunk['timestamp'], unit='ms', errors='coerce')
        df_chunk = df_chunk.dropna(subset=['timestamp'])

        # Extract date + hour string (YYYY-MM-DD_HH)
        df_chunk['date_time'] = df_chunk['timestamp'].dt.strftime("%Y-%m-%d_%H")

        # === Split and save per hour ===
        for dt_str, group in df_chunk.groupby('date_time'):
            out_path = os.path.join(output_dir, f"trades_{dt_str}.csv")
            write_header = not os.path.exists(out_path)
            group.to_csv(out_path, mode='a', index=False, header=write_header)
            print(f"\nSaved {len(group)} trades → {out_path}")

        all_trades = []  # clear buffer

    # Progress update
    human_time = pd.to_datetime(since, unit='ms')
    print(f"\rFetched up to: {human_time}", end="", flush=True)

    # Avoid rate-limit issues
    time.sleep(0.5)

# === Final save for leftover trades ===
if all_trades:
    df_final = pd.DataFrame(all_trades)
    df_final['timestamp'] = pd.to_datetime(df_final['timestamp'], unit='ms', errors='coerce')
    df_final = df_final.dropna(subset=['timestamp'])
    df_final['date_time'] = df_final['timestamp'].dt.strftime("%Y-%m-%d_%H")

    for dt_str, group in df_final.groupby('date_time'):
        out_path = os.path.join(output_dir, f"trades_{dt_str}.csv")
        write_header = not os.path.exists(out_path)
        group.to_csv(out_path, mode='a', index=False, header=write_header)
        print(f"\nFinal save: {len(group)} trades → {out_path}")

print(f"\nDone! Trades saved to hourly CSV files in: {output_dir}")
