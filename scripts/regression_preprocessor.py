import pandas as pd
import numpy as np
from tqdm import tqdm
import sys
import os

if __name__ == "__main__":
    input_dir = "../data/raw/one_week"
    output_dir = "../data/processed"
    group = "1min" # Examples:- "10s", "1min"/"1T", "1H", "1D", "1W"
    
    # for file in os.listdir(input_dir):
    #     print(file)
    file_paths = [os.path.join(input_dir, file) for file in os.listdir(input_dir) if file.endswith(".csv")]
    prev_path = [None] + file_paths[:-1]
    trades = pd.DataFrame()
    pbar  = tqdm(zip(file_paths,prev_path))
    for file, prev_file in tqdm(zip(file_paths, prev_path), total=len(file_paths), desc="Processing hourly trade files"):
        df = pd.read_csv(file)
        if prev_file is not None:
            prev_df = pd.read_csv(prev_file)
            df = pd.concat([prev_df, df], ignore_index=True)

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["bought"] = np.where(df["side"] == "buy", df["amount"], 0)
        df["sold"] = np.where(df["side"] == "sell", df["amount"], 0)

        df.drop(columns= ["side"], axis=1)
        # "timestamp", "open_price", "close_price", "log_volume", "log_return", "lag1_return", "volatility"
        # try:
        df_agg = (
            df.set_index("timestamp")
            .resample(group)
            .apply(lambda x: pd.Series({
                "open_price": x["price"].iloc[0] if len(x) > 0 else np.nan,
                "close_price": x["price"].iloc[-1] if len(x) > 0 else np.nan,
                "log_volume": np.log(x["cost"].sum() + 1),
                "buy_sell_imbalance": (
                    (x.loc[x["side"] == "buy", "amount"].sum() - 
                        x.loc[x["side"] == "sell", "amount"].sum()) /
                    (x.loc[x["side"] == "buy", "amount"].sum() + 
                        x.loc[x["side"] == "sell", "amount"].sum() + 1e-8)
                ),

            }))
            .reset_index()
        )
        # except Exception as e:
        #     print(df)
        #     print(e)
        #     sys.exit(0)

        df_agg["log_return"] = np.log(df_agg["close_price"] / df_agg["close_price"].shift(1))
        df_agg["lag1_return"] = df_agg["log_return"].shift(1)
        df_agg["volatility"] = df_agg["log_return"].rolling(window=10).std()

        # Due to this Volayility calculation the first 9 mins will have NULL values and as we lots of data i am removing those
        df_agg = df_agg.dropna()
        if prev_file is not None:
            _, _, date, hour = file.split("_")
            file_hour = pd.to_datetime(f"{date} {hour[:2]}:00:00")

            if file_hour is not None:
                df_agg = df_agg[df_agg["timestamp"].dt.floor("H") == file_hour]
            else:
                print(f"Could not extract hour from {file}; keeping all rows.")
        
        trades = pd.concat([trades, df_agg], ignore_index=True)

trades = trades.sort_values(by="timestamp").reset_index(drop=True)

print(f"\nTrades\t:\t{len(trades)}\n")
output_file = os.path.join(output_dir, f"regression_{group}_data.csv")
trades.to_csv(output_file, index=False)