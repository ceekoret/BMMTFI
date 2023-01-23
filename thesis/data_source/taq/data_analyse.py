"""
The filtered Robintrack data will be analysed here. For example, the daily changes in holders will be calculated.
"""
import os
import pandas as pd
from thesis.tools import FileTools
pd.set_option('display.max_rows', 500)


def analyse_data(paths):
    filedir = paths.daily_data_merged
    print(filedir)

    for filename in os.listdir(filedir):
        csv_path = os.path.join(filedir, filename)

        # checking if it is a file
        if os.path.isfile(csv_path):
            print(f"Now analysing data for Robintrack file: {filename}")

            # Create dataframe and make sure timestamp is read as datetime
            df = pd.read_csv(csv_path)


            # ToDo total_bs and total_vol needs to be rolling average
            rolling_window = 14
            df['bs_change'] = (df['buy'] - df['sell']) / df['total_bs'].rolling(rolling_window).mean()
            df['vol_change'] = (df['buy_vol'] - df['sell_vol']) / df['total_vol'].rolling(rolling_window).mean()
            df['bs_change'] = df['bs_change'].round(4)
            df['vol_change'] = df['vol_change'].round(4)
            df = df.dropna()

            FileTools.df_to_csv(df, csv_path)

