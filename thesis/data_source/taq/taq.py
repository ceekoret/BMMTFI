"""
This file will glue together all functionality built around the TAQ data set. Period 02/05/2018 - 13/08/2020.
The following stocks will be used from the data set:
---  Top 10 largest stocks  ---
F.csv       913121
GE.csv      857937
AAPL.csv    720906
MSFT.csv    654240
AAL.csv     638794
DIS.csv     598965
DAL.csv     572754
TSLA.csv    563437
CCL.csv     481811
GPRO.csv    475018
---  5 other random stocks  ---
FPXI
GLL
LADR
NFLX
ZYNE

WORKFLOW: dirty_data --> clean_unsplit --> clean_data --> daily_data
"""
import pandas
from .flatten_csv import csv_clean, csv_separate, csv_daily, loop_years
from .data_filter import filter_data
from .data_analyse import analyse_data
from thesis.tools import FileTools


class TAQ:
    def __init__(self, dir_path):
        self.raw_file_dir = dir_path

        self.dirty_data = dir_path + "/" + "dirty_data"
        self.clean_data = dir_path + "/" + "clean_data"
        self.clean_unsplit = dir_path + "/" + "clean_unsplit"
        self.daily_data = dir_path + "/" + "daily_data"
        self.daily_data_merged = dir_path + "/" + "daily_data_merged"

    def flatten_csv(self):
        # loop_years(self, "csv_clean")
        # loop_years(self, "csv_separate")
        loop_years(self, "csv_daily")

        # csv_clean(self.dirty_data, self.clean_unsplit)
        # csv_separate(save_location, self.clean_data)
        # csv_daily(self.clean_data)
        # ToDo merge daily_data for each year

    def filter_data(self):
        filter_data(self.rawfiledir, self.filteredfile_dir)

    def analyse_data(self):
        analyse_data(self)

    @staticmethod
    def test():
        print("test123")
