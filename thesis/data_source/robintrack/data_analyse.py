"""
The filtered Robintrack data will be analysed here. For example, the daily changes in holders will be calculated.
"""
import os
import pandas as pd
from thesis.tools import FileTools
pd.set_option('display.max_rows', 500)

def analyse_data(filteredfile_dir):
    for filename in os.listdir(filteredfile_dir):
        csv_path = os.path.join(filteredfile_dir, filename)

        # checking if it is a file
        if os.path.isfile(csv_path):
            print(f"Now analysing data for Robintrack file: {filename}")

            # Create dataframe and make sure timestamp is read as datetime
            df = pd.read_csv(csv_path)

            # Create column with numerical user difference
            df['change'] = df['users_holding'].diff()

            # Create column with percentual user difference
            df['pct_change'] = df['users_holding'].pct_change().round(4)

            # Dropping na values (this should only be the first column)
            df = df.dropna()

            FileTools.df_to_csv(df, csv_path)

