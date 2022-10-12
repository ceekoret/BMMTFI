"""
The data from Robintrack and TAQ is quite large and contains quite a lot of information which is not necessary for this research.
Hence we will be filtered and adjust some of this data with the code in this file.
"""
import os
import pandas as pd
pd.set_option('display.max_rows', 500)


def adjust_time():
    return ""


def filter_data(filedir):
    """
    The Robintrack data set contains irrelevant data points. These data points are measured outside trade times.
    This can be the case either
    - during the weekend, or
    - during the weekday outside trading hours
      Trading hours are weekdays from (Robinhood, 2022a):
      - 09:30 to 16:00 Eastern Daylight Time (ET)
      - 15:30 to 22:00 Central European Time (CET)
      - 13:30 to 20:00 Coordinated Universal Time (UTC)

    The Robintrack data set is based on UTC times.
    Hence I will be deleting all observations outside of the above-mentioned time frame.

    This function will filter the csv files based on the filters above.
    :param filedir: The directory path where all csv files are located. The function will loop all the files in here.
    :return: Returns the cleaned data set for each stock.
    """
    for filename in os.listdir(filedir):
        csv_path = os.path.join(filedir, filename)

        # checking if it is a file
        if os.path.isfile(csv_path):
            print(csv_path)

            # Create dataframe and make sure timestamp is read as datetime
            df = pd.read_csv(csv_path)
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            print(len(df.index))

            # Round datetime to nearest hour.
            # 05:30:00 --> 5:00:00
            # 05:30:01 --> 6:00:00
            df['hour'] = df['timestamp'].dt.round('H').dt.strftime('%H:%M')
            df['date'] = df['timestamp'].dt.round('H').dt.date
            df['dayname'] = df['timestamp'].dt.round('H').dt.day_name()

            # Remove all observations which are:
            # - not weekdays
            df = df[~((df['dayname'] == "Saturday") | (df['dayname'] == "Sunday"))]
            # - smaller than 13:00* (UTC)
            #   *the half and hour does not make a difference, seeing as measurements are done hourly.
            # - greater than 20:00 (UTC)
            df = df[(df['hour'] >= "13:00") & (df['hour'] <= "20:00")]


            # TO DO
            # Remove duplicates
            # Treat missing values
            # df.sort_values('users_holding').drop_duplicates(subset=['hour', 'date'], keep='last')
            # print(df.groupby('date').size().head(300))

            print(len(df.index))
            df.groupby(['date', 'hour']).drop_duplicates(['date', 'hour'], keep='first')
            print(len(df.index))

            # print(df[['timestamp', 'hour', 'date', 'dayname', 'users_holding']].iloc[100:200])

            exit()


