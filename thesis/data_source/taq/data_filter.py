"""
The data from Robintrack and TAQ is quite large and contains quite a lot of information which is not necessary for this research.
Hence we will be filtered and adjust some of this data with the code in this file.
"""
import os
import pandas as pd
import numpy as np
from thesis.tools import FileTools
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)


def filter_data(filedir, filteredfile_dir):
    """
    The TAQ data set contains will be filtered according to the Boehmer, Jones, Zhang & Zhang (2021) method.

    This means that observations will be kept with
    - exchange code 'D', and
    - sub penny prices which are:
      - != 0.0000
      - < 0.0040 and > 0.0060

    :param filedir: Directory where TAQ files can be found.
    :param filteredfile_dir: Directory where to store filtered files.
    :return: Returns the filtered files to the directory mentioned above.
    """

    for filename in os.listdir(filedir):
        csv_path = os.path.join(filedir, filename)

        # checking if it is a file
        if os.path.isfile(csv_path):
            print(f"Now filtering data for Robintrack file: {filename}")

            # Create dataframe and make sure timestamp is read as datetime
            df = pd.read_csv(csv_path)

            #                 --- Removing data ---
            # Removing unnecessary columns
            df = df.drop(columns=['SYM_SUFFIX'])

            # Removing all observations where the Exchange code (EX) is not 'D'
            df = df[df['EX'] == 'D']

            # Creating penny column - pennies incl sub-pennies
            # df['penny'] = df['PRICE'] - df['PRICE'].apply(np.floor)

            # Creating sub_pennies column
            df['sub_penny'] = (df['PRICE'] - (df['PRICE'] * 100).apply(np.floor)/100).round(4)
            n = 170000
            # print(df.iloc[n:n+500])

            """ To be safe, Boehmer et al. (2021) remove trades with prices equal to 0.0000 and 
            prices between than 0.0040 and 0.0060"""
            # Removing trades with sub penny prices of 0
            df = df[~(df['sub_penny'] == 0.0000)]
            # Removing trades which are: 0.0040 <= penny prices >= 0.0060
            df = df[(df['sub_penny'] < 0.0040) | (df['sub_penny'] > 0.0060)]

            #                 --- Creating new data ---
            # Categorize a trade as buy or sell. Also buy/sell volumes
            df['buysell'] = np.where(((df['sub_penny'] > 0.0000) & (df['sub_penny'] < 0.0050)), "sell", "buy")
            df['buy'] = np.where(df['buysell'] == "buy", 1, 0)
            df['sell'] = np.where(df['buysell'] == "sell", 1, 0)
            df['buy_vol'] = np.where(df['buysell'] == "buy", df['SIZE'], 0)
            df['sell_vol'] = np.where(df['buysell'] == "sell", df['SIZE'], 0)

            # Taking daily sums and averages
            df = (df.groupby('DATE').agg({'PRICE': 'mean', 'SIZE': 'sum', 'buy': 'sum', 'sell': 'sum', 'buy_vol': 'sum', 'sell_vol': 'sum'})
                  .round(2)
                  .rename(columns={'PRICE': 'price', 'SIZE': 'total_vol'}))

            df.insert(0, 'date', df.index)
            df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')

            df['total_bs'] = df['buy'] + df['sell']
            df['total_vol'] = df['buy_vol'] + df['sell_vol']

            # ToDo total_bs and total_vol needs to be rolling average
            rolling_window = 3
            df['bs_change'] = (df['buy'] - df['sell']) / df['total_bs'].rolling(rolling_window).mean()
            df['vol_change'] = (df['buy_vol'] - df['sell_vol']) / df['total_vol'].rolling(rolling_window).mean()
            df['bs_change'] = df['bs_change'].round(4)
            df['vol_change'] = df['vol_change'].round(4)

            #                 --- Analyzing new data ---
            # # Create column with numerical trade differences
            # df['change_bs'] = df['net_bs'].diff()

            # # Create column with percentual user difference
            # df['pct_change'] = df['users_holding'].pct_change().round(4)

            print(df)
            print(df.dtypes)
            exit()
            save_location = f"{filteredfile_dir}/{filename}"
            FileTools.df_to_csv(df, save_location)




