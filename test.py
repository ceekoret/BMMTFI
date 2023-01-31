import os
import pandas as pd
import csv
import numpy as np

import sys


def loop_tickers(func):
    'Decorator that loops all (ticker) files in the directory.'

    def wrap(*args, **kwargs):
        if 'file_dir' in kwargs:
            for filename in os.listdir(filedir):
                csv_path = os.path.join(filedir, filename)

                # checking if it is a file
                if os.path.isfile(csv_path):
                    #                     print(csv_path)
                    result = func(csv_path=csv_path, *args, **kwargs)

        else:
            raise ValueError(
                "Wrapper can not loop, as no file directory given. Please specify which folder needs to be "
                "looped by setting 'file_dir' variable.")

        return result

    return wrap


@loop_tickers
def filter_data(csv_path, *args, **kwargs):
    ticker = csv_path.split("\\")[-1].split(".")[0]
    print(
        f"Now executing function 'filter_data' for ticker [{ticker}], variables:\n - csv_path: [{csv_path}]"
        f"\n - kwargs: [{kwargs}])")

    # Setting start count and chunk size
    row_count = 0
    chunksize = 10 ** 6
    header = True
    # Start counting the rows in the csv, chunk by chunk
    for df in pd.read_csv(csv_path, chunksize=chunksize):
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

        print(df)
        print(df.groupby('date').sum())

        #     -----------------     Converting to daily data new data     -----------------

        # Taking daily sums and averages
        df = (df.groupby('date').agg(
            {'price': 'mean', 'size': 'sum', 'buy': 'sum', 'sell': 'sum', 'buy_vol': 'sum', 'sell_vol': 'sum'})
              .round(2)
              .rename(columns={'size': 'total_vol'}))

        print(df)
        print("-----------------------")

        df.insert(0, 'date', df.index)
        df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')

        df['total_bs'] = df['buy'] + df['sell']
        df['total_vol'] = df['buy_vol'] + df['sell_vol']

        print(df)
        print(df.shape)
        exit()
        print(df)
        exit()

    # Save results


#     print(f"Saving results for [{ticker}], found [{row_count}] total rows\n")

#     return row_count


filedir = r"E:/Users/Christiaan/Large_Files/Thesis/taq/unfiltered"
filter_data(file_dir=filedir)

# import wrds
#
# conn = wrds.Connection()
# print(conn.list_libraries())
# company_narrow = conn.get_table(library='comp', table='company',
#                                 columns = ['conm', 'gvkey', 'cik'], obs=5)
# filedir = r"C:\Users\Ck0rt\Documents\Large files\School\MSc Finance & Investments\Thesis\Robintrack\popularity_export"
#
# bin_500 = 0
# bin_1000 = 0
# bin_10000 = 0
# bin_100000 = 0
# bin_plus = 0
#
#
# for filename in os.listdir(filedir):
#     csv_path = os.path.join(filedir, filename)
#
#     # checking if it is a file
#     if os.path.isfile(csv_path):
#         print(f"Now analysing data for Robintrack file: {filename}")
#         df = pd.read_csv(csv_path)
#
#         average_users = df.users_holding.mean().round()
#
#         if average_users <= 500:
#             bin_500 += 1
#         elif average_users <= 1000:
#             bin_1000 += 1
#         elif average_users <= 10000:
#             bin_10000 += 1
#         elif average_users <= 100000:
#             bin_100000 += 1
#         else:
#             bin_plus += 1
#
#
# print(f"Number of stocks in bin_500: {bin_500}")
# print(f"Number of stocks in bin_1000: {bin_1000}")
# print(f"Number of stocks in bin_10000: {bin_10000}")
# print(f"Number of stocks in bin_100000: {bin_100000}")
# print(f"Number of stocks in bin_plus: {bin_plus}")
#
# exit()



# all_files = r"C:/Users/Ck0rt/Documents/Large files/School/MSc Finance & Investments/Thesis/TAQ/daily_data_merged"
# all_files2 = r"C:\Users\Ck0rt\PycharmProjects\MasterThesis_BMMTFI\data\robintrack\filtered_data"
#
# # create here a list of files you want to merge into the an Excel file
# files = [all_files2 + "/" + company for company in os.listdir(all_files)]
# sheet_names = os.listdir(all_files)
# print(files)
#
# writer = pd.ExcelWriter('out2.xlsx', engine='xlsxwriter')
#
# for i, file in enumerate(files):
#     df = pd.read_csv(file, sep=",")
#
#     df.to_excel(writer, sheet_name=str(sheet_names[i]))
#
# writer.save()