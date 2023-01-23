"""
This file will glue together all functionality built around the Robintrack data set.
"""
import pandas
from .collect_tweets import loop_tweet_collection
from thesis.tools import FileTools

class Twitter:
    def __init__(self, dir_path):
        self.rawfiledir = dir_path

    def loop_tweet_collection(self, save=False):
        loop_tweet_collection(save)


    @staticmethod
    def test():
        print("test123")
