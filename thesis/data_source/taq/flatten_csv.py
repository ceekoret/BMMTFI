import os
import pandas as pd
import numpy as np
from thesis.tools import FileTools


def csv_clean(file_path, save_location):
    print(f"Cleaning {file_path}")
    open(save_location, 'w').close()
    header = True

    chunksize = 10 ** 6
    with pd.read_csv(file_path, chunksize=chunksize) as reader:
        for chunk in reader:

            print(chunk)

            # Removing unnecessary columns
            df = chunk.drop(columns=['SYM_SUFFIX'])

            # Removing all observations where the Exchange code (EX) is not 'D'
            df = df[df['EX'] == 'D']
            df['sub_penny'] = (df['PRICE'] - (df['PRICE'] * 100).apply(np.floor) / 100).round(4)
            df = df[~(df['sub_penny'] == 0.0000)]
            df = df[(df['sub_penny'] < 0.0040) | (df['sub_penny'] > 0.0060)]
            print(len(df.index))

            df.to_csv(save_location, header=header, index=False, mode='a')
            header = False


def csv_separate(file_path, save_dir):
    print(f"Separating {file_path}")
    df = pd.read_csv(file_path)

    company_list = df['SYM_ROOT'].unique()
    for company in company_list:
        save_df = df[df['SYM_ROOT'] == company]
        print(save_df)

        save_location = save_dir + "/" + company + ".csv"
        open(save_location, 'w').close()
        print(save_location)

        save_df.to_csv(save_location, header=True, index=False, mode='w')


def csv_daily(file_path, save_location):
    print(f"Convert to daily data: {file_path}")
    open(save_location, 'w').close()

    df = pd.read_csv(file_path)

    # df = df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])


    #                 --- Creating new data ---
    # Categorize a trade as buy or sell. Also buy/sell volumes
    df['buysell'] = np.where(((df['sub_penny'] > 0.0000) & (df['sub_penny'] < 0.0050)), "sell", "buy")
    df['buy'] = np.where(df['buysell'] == "buy", 1, 0)
    df['sell'] = np.where(df['buysell'] == "sell", 1, 0)
    df['buy_vol'] = np.where(df['buysell'] == "buy", df['SIZE'], 0)
    df['sell_vol'] = np.where(df['buysell'] == "sell", df['SIZE'], 0)

    # Taking daily sums and averages
    df = (df.groupby('DATE').agg(
        {'PRICE': 'mean', 'SIZE': 'sum', 'buy': 'sum', 'sell': 'sum', 'buy_vol': 'sum', 'sell_vol': 'sum'})
          .round(2)
          .rename(columns={'PRICE': 'price', 'SIZE': 'total_vol'}))

    df.insert(0, 'date', df.index)
    df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')

    df['total_bs'] = df['buy'] + df['sell']
    df['total_vol'] = df['buy_vol'] + df['sell_vol']

    FileTools.df_to_csv(df, save_location)


def loop_years(paths, task):
    if task == "csv_clean":

        filedir = paths.dirty_data
    elif task == "csv_separate":
        filedir = paths.clean_unsplit
    elif task == "csv_daily":
        filedir = paths.clean_data
    else:
        # print("Incorrect task chosen. Options are: 'csv_clean', 'csv_separate' and 'csv_daily'.")
        raise ValueError("Incorrect task chosen. Options are: 'csv_clean', 'csv_separate' and 'csv_daily'.")

    for year in os.listdir(filedir):
        year_dir = os.path.join(filedir, year)

        for filename in os.listdir(year_dir):
            csv_path = os.path.join(year_dir, filename)

            # checking if it is a file
            if os.path.isfile(csv_path):
                file_path = csv_path

                # Perform function
                if task == "csv_clean":
                    save_location = paths.clean_unsplit + f"/{year}/" + filename
                    csv_clean(file_path, save_location)
                elif task == "csv_separate":
                    save_dir = paths.clean_data + f"/{year}"
                    csv_separate(file_path, save_dir)
                elif task == "csv_daily":
                    save_location = paths.daily_data + f"/{year}/" + filename
                    csv_daily(file_path, save_location)

