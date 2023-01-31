import os
import pandas as pd
import csv
import numpy as np

path = r"E:/Users/Christiaan/Large_Files/Thesis/taq/unfiltered/GME.csv"
df = pd.read_csv(path)
print(df)

#     -----------------     Filtering data     -----------------
# Removing all observations where the Exchange code (EX) is not 'D'
df = df[df['ex'] == 'D']

# Creating a new column which contains the sub penny prices
df['sub_penny'] = (df['price'] - (df['price'] * 100).apply(np.floor) / 100).round(4)

# Removing all sub penny prices which are a round penny (i.e. equal to 0.0000 or 0.0010)
df = df[~(df['sub_penny'] == 0.0000)]
df = df[~(df['sub_penny'] > 0.0099)]

# Removing all sub penny prices which are in the 0.4 - 0.6 range
df = df[(df['sub_penny'] <= 0.0040) | (df['sub_penny'] >= 0.0060)]

#     -----------------     Creating new data     -----------------
# Categorize a trade as buy or sell. Also buy/sell volumes
df['buysell'] = np.where(((df['sub_penny'] > 0.0000) & (df['sub_penny'] < 0.0050)), "sell", "buy")

# To count buys and sells, I specify 1 or 0 for both buy and sell.
# Being a buy automatically means having a 0 for sell. This is done to easily count total trades.
df['buy'] = np.where(df['buysell'] == "buy", 1, 0)
df['sell'] = np.where(df['buysell'] == "sell", 1, 0)

# Next, I specify whether the volume is buy or sell.
df['buy_vol'] = np.where(df['buysell'] == "buy", df['size'], 0)
df['sell_vol'] = np.where(df['buysell'] == "sell", df['size'], 0)

#     -----------------     Converting to daily data new data     -----------------
# Taking daily sums and averages for the columns. The dictionary indicates which one is taken.
df = (df.groupby('date').agg(
    {'price': 'mean', 'size': 'sum', 'buy': 'sum', 'sell': 'sum', 'buy_vol': 'sum', 'sell_vol': 'sum'})
      .round(2)
      .rename(columns={'size': 'total_vol'}))

# Resetting 'date' index and converting it to datetime
df = df.reset_index()
df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y-%m-%d')

# Creating total amount of traders, total volume and total amount of money traded
df['total_bs'] = df['buy'] + df['sell']
df['total_vol'] = df['buy_vol'] + df['sell_vol']
df['total_price'] = df['price'] * df['total_vol']

