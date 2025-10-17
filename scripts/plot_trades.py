import pandas as pd
import matplotlib.pyplot as plt
import os

def prepareDF(filepath):
        df = pd.read_csv(filepath)
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["minute"] = df["timestamp"].dt.minute
        return df

def getTradesPerMinute(filepath):
        df = prepareDF(filepath)
        counts = df.groupby("minute").size()

        return counts

def getTradeCostsPerMinute(filepath):
        df = prepareDF(filepath)
        sizes = df.groupby("minute")["cost"].sum()

        return sizes

def plotArray(counts, title, xlabel, ylabel, filename):
        plt.figure(figsize=(10,5))
        plt.plot(counts.index, counts.values, marker='o')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.savefig(filename, format='jpg')
        # plt.show()


def autoCorrelationFunction(counts, filename):
        pd.plotting.autocorrelation_plot(counts)
        plt.savefig(filename, format='jpg')
        # plt.show()


if __name__ == "__main__":
        os.makedirs("../figures", exist_ok=True)
        filepath = "../data/raw/one_week/trades_2025-10-01_00.csv"
        counts = getTradesPerMinute(filepath)
        sizes = getTradeCostsPerMinute(filepath)

        autoCorrelationFunction(counts, "../figures/TradeCountACF.jpg")
        autoCorrelationFunction(sizes, "../figures/TradeCostACF.jpg")
        plotArray(counts, "Trades per Minute", "Minutes", "Number of Trades", "../figures/Trades_per_minute.jpg")
        plotArray(sizes, "Trade Costs per Minute", "Minutes", "Cost of Trades", "../figures/Trade_costs_per_minute.jpg")
