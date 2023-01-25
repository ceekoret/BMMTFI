import pandas as pd
import os
import datetime as dt
import time
from dateutil.relativedelta import relativedelta

import pandas as pd
import praw
from pmaw import PushshiftAPI
api = PushshiftAPI(num_workers=10)
# api_praw = PushshiftAPI(praw=reddit)

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)


import praw
from datetime import datetime

# Create a Reddit instance
reddit = praw.Reddit(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET', user_agent='YOUR_USER_AGENT')

# Select the subreddit you want to scrape
subreddit = reddit.subreddit('learnprogramming')

# Set the start and end dates for the time period you want to scrape
start_date = datetime(2019, 11, 1)  # November 1st, 2019
end_date = datetime(2019, 11, 30)  # November 30th, 2019

# Retrieve all comments from the subreddit that were made within the specified time period
for submission in subreddit.comments(limit=None):
    comment_time = datetime.fromtimestamp(comment.created_utc)  # Convert the comment's creation timestamp to a datetime object
    if start_date <= comment_time <= end_date:
        print(comment.body)



# pd.set_option('display.max_rows', 1000)
# pd.set_option('display.max_columns', 500)
#
# # Read a CSV file into a Pandas DataFrame
# df = pd.read_csv(r"C:\Users\Ck0rt\Documents\Large files\School\MSc Finance & Investments\Thesis\Reddit\posts\wallstreetbets\2020_01.csv")
#


# Print the first few rows of the DataFrame
# print(df)

# def list_files(dir):
#     r = []
#     for root, dirs, files in os.walk(dir):
#         for name in files:
#             r.append(os.path.join(root, name))
#     return r
#
#
# base_url = r"C:/Users/Ck0rt/Documents/Large files/School/MSc Finance & Investments/Thesis/Reddit/posts"
#
# df = pd.DataFrame()
#
# for root, dirs, files in os.walk(base_url):
#     # Loop through all files in the current directory
#     for file in files:
#         # Check if the file is a CSV file
#         if file.endswith('.csv'):
#             # Append the CSV file to the dataframe
#             df = df.append(pd.read_csv(os.path.join(root, file)))
#
#
#
