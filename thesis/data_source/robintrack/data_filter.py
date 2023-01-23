"""
The data from Robintrack and TAQ is quite large and contains quite a lot of information which is not necessary for this research.
Hence we will be filtered and adjust some of this data with the code in this file.
"""
import os
import pandas as pd
from thesis.tools import FileTools
pd.set_option('display.max_rows', 500)


def filter_data(filedir, filteredfile_dir):
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
            print(f"Now filtering data for Robintrack file: {filename}")

            # Create dataframe and make sure timestamp is read as datetime
            df = pd.read_csv(csv_path)
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

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

            """
            Robintrack seems to have had periods where there program ran into some errors.
            These errors resulted in apparent:
            - over activity: too many measurements were done --> Solution: removing duplicates
            - under activity: little or no measurements were done --> Solution: adding missing values
            """
            # Remove duplicates.
            df = df.drop_duplicates(subset=['hour', 'date'], keep='last')

            # If you want to end up with hourly data, then missing values need to be added.
            # ToDo... Missing values

            # Else, if you want daily data you need average user count of each day:
            df = df.groupby(['date']).mean().round().astype(int)

            save_location = f"{filteredfile_dir}/{filename}"
            FileTools.df_to_csv(df, save_location)




