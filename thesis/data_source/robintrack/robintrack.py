"""
This file will glue together all functionality built around the Robintrack data set.
"""
import pandas
from .data_filter import filter_data

class Robintrack:
    def __init__(self, dir_path):
        self.filedir = dir_path

    def filter_data(self):
        filter_data(self.filedir)

    @staticmethod
    def test():
        print("test123")