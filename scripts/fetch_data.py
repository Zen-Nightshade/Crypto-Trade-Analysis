import ccxt
import pandas as pd
import time

# Initialize Binance
binance = ccxt.binance()

symbol = 'BTC/USDT'
start_time = int(pd.Timestamp('2025-10-02 00:00:00').timestamp() * 1000)  # in ms
end_time   = int(pd.Timestamp('2025-10-09 00:00:00').timestamp() * 1000)  # in ms

all_trades = []
since = start_time

while since < end_time:
    trades = binance.fetch_trades(symbol, since=since, limit=1000)
    if not trades:
        break
    
    all_trades.extend(trades)
    
    # Update 'since' to the timestamp of the last trade + 1ms
    since = trades[-1]['timestamp'] + 1
    
    # Avoid hitting API rate limits
    time.sleep(0.5)

# Convert to DataFrame
# print(all_trades[:5])
df = pd.DataFrame(all_trades)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df = df[df['timestamp'] <= pd.to_datetime(end_time, unit='ms')]
df.to_csv("../data/raw/one_week_trades.csv", index=False)
