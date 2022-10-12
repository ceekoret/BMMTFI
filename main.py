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
robintrack_data_folder = r"data/popularity_export"
robintrack = t.Robintrack(robintrack_data_folder)



# --- Data cleaning ---
robintrack.filter_data()







