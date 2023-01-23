"""
This file will glue together all functionality built around the Robintrack data set.
"""
import pandas
from .data_filter import filter_data
from .data_analyse import analyse_data
from thesis.tools import FileTools

class Robintrack:
    def __init__(self, dir_path):
        self.rawfiledir = dir_path
        self.filteredfile_dir = FileTools.change_dir("filtered_data", dir_path)

    def filter_data(self):
        filter_data(self.rawfiledir, self.filteredfile_dir)

    def analyse_data(self):
        analyse_data(self.filteredfile_dir)

    @staticmethod
    def test():
        print("test123")
