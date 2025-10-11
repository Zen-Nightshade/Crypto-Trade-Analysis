import pandas as pd
import os

input_dir = "../data/raw"
output_dir = "../data/raw/one_week"
chunksize = 500_000  # adjust based on your system memory

os.makedirs(output_dir, exist_ok=True)


csv_files = [f for f in os.listdir(input_dir) if f.endswith(".csv")]

if not csv_files:
    print(f"No CSV files found in {input_dir}")
else:
    print(f"Found {len(csv_files)} CSV file(s) in {input_dir}:")
    for f in csv_files:
        print(f" - {f}")

for csv_file in csv_files:
    file_path = os.path.join(input_dir, csv_file)
    print(f"\nProcessing {csv_file}...")

    for i, chunk in enumerate(pd.read_csv(file_path, chunksize=chunksize)):
        print(f"  Chunk {i}...")

        chunk["timestamp"] = pd.to_datetime(chunk["timestamp"], errors="coerce")

        chunk = chunk.dropna(subset=["timestamp"])

        chunk["date_time"] = chunk["timestamp"].dt.strftime("%Y-%m-%d_%H")

        # Split this chunk by date+hour
        for dt_str, group in chunk.groupby("date_time"):
            out_path = os.path.join(output_dir, f"trades_{dt_str}.csv")

            # Append if exists, else create new
            write_header = not os.path.exists(out_path)
            group.to_csv(out_path, mode="a", index=False, header=write_header)

            print(f"    → Wrote {len(group):,} rows for {dt_str} → {out_path}")

print("\nDone! All trades split by date+hour.")
