import pandas as pd
import numpy as np
import os

group = "10s" # Examples:- "10s", "1min"/"1T", "1H", "1D", "1W"
def vwap(x):
    amt_sum = x["amount"].sum()
    if amt_sum > 0:
        return (x["price"] * x["amount"]).sum() / amt_sum
    return x["price"].mean()

columns = ["timestamp", "symbol", "side", "price", "amount", "cost"]
input_dir = "../data/raw/one_week/"
output_dir = "../data/processed/trades_2025-10-01_to_2025-10-07_10s.csv"

file_paths = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".csv")]

trades = pd.DataFrame()
for file_path in file_paths:
    df = pd.read_csv(file_path)
    # print(file_path.split("/")[-1],len(df),sep="\t:\t")
    df = df[columns]
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    df["bought"] = np.where(df["side"] == "buy", df["amount"], 0)
    df["sold"] = np.where(df["side"] == "sell", df["amount"], 0)

    df.drop(columns= ["side"], axis=1)
    # "timestamp", "symbol", "price", "amount", "bought", "sold"
    symbol_value = df["symbol"].iloc[0]

    df_agg = (
        df.set_index("timestamp")
        .resample(group)
        .apply(lambda x: pd.Series({
            "bought": x["bought"].sum(),
            "sold": x["sold"].sum(),
            "amount": x["amount"].sum(),
            "price": vwap(x),
            "cost": x["cost"].sum(),
            "trade_count": len(x)

        }))
        .reset_index()
    )
    df_agg["symbol"] = symbol_value
    trades = pd.concat([trades, df_agg], ignore_index=True)

# trades["timestamp"] = pd.to_datetime(trades["timestamp"], errors="coerce")
trades = trades.sort_values(by="timestamp").reset_index(drop=True)

print(f"\nTrades\t:\t{len(trades)}\n")
trades.to_csv(output_dir, index=False)
