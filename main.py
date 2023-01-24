"""
Author: Christiaan K
Student number: ******
Univerity: Erasmus University Rotterdam - Rotterdam School of Management
Degree: MSc Finance & Investments
Course: FI master thesis (BMMTFI)

FILE INFORMATION
This file will describe all the steps required in order to end up with the same research results.

DATA SOURCES
Robintrack: https://robintrack.net/data-download
Trade and Quote (TAQ) database: https://wrds-www.wharton.upenn.edu/pages/get-data/nyse-trade-and-quote/millisecond-trade-and-quote-daily-product-2003-present-updated-daily/consolidated-trades/
Twitter: ...
Reddit: ...
"""

import thesis as t

# path to Robintrack csv folder
# robintrack_data_folder = r"C:/Users/Ck0rt/Documents/Large files/School/MSc Finance & Investments/Thesis/Robintrack/popularity_export"
robintrack_data_folder = r"data/robintrack/popularity_export"
robintrack = t.Robck(robintrack_data_folder)

TAQ_data_folder = r"C:/Users/Ck0rt/Documents/Large files/School/MSc Finance & Investments/Thesis/TAQ"
TAQ = t.TAQ(TAQ_data_folder)

twitter = t.Twitter()

# --- Robintrack ---
# robintrack.filter_data()
# robintrack.analyse_data()

# --- TAQ ---
# robintrack.filter_data()

# TAQ.flatten_csv()
TAQ.analyse_data()

# --- Twitter ---
twitter.loop_tweet_collection(save=False)

# Is this change going to work??



