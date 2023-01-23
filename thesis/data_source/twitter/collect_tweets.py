# Import libraries
import pandas as pd
import tweepy
import time
import datetime
from dateutil.relativedelta import relativedelta
from .t_functions import query_builder as tf
from pathlib import Path
import os.path

# import API keys
from API_KEYS import twitter_keys
bearer_token = twitter_keys.bearer_token

client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
# ticker_list = ['TSLA', 'MU', 'SNAP', 'AMD', 'DIS', 'MSFT', 'AAPL', 'AMZN', 'SQ', 'BABA', 'V', 'NFLX', 'IQ', 'ATVI', 'SHOP', 'BA', 'NVDA', 'GE', 'WMT', 'SBUX', 'F', 'TLRY', 'LULU', 'BAC', 'GME']

"""
The following variables are used:
@start_time is both the starting moment for 
- the Twitter API to start searching 
- the while-loop.
@end_time is the end moment for the Twitter API to stop searching.
@end_date is date after which the while-loop stops.
"""


def process_pages(pages_list):
    result = []
    user_dict = {}
    # Loop through each response object
    for page in pages_list:
        # Take all of the users, and put them into a dictionary of dictionaries with the info we want to keep
        for user in page.includes['users']:
            user_dict[user.id] = {'username': user.username,
                                  'followers': user.public_metrics['followers_count'],
                                  'tweets': user.public_metrics['tweet_count'],
                                  'description': user.description,
                                  'location': user.location
                                  }
        for tweet in page.data:
            # For each tweet, find the author's information
            author_info = user_dict[tweet.author_id]
            # Put all of the information we want to keep in a single dictionary for each tweet
            result.append({'author_id': tweet.author_id,
                           'username': author_info['username'],
                           'author_followers': author_info['followers'],
                           'author_tweets': author_info['tweets'],
                           'author_description': author_info['description'],
                           'author_location': author_info['location'],
                           'text': tweet.text,
                           'created_at': tweet.created_at,
                           'lang': tweet.lang,
                           'retweets': tweet.public_metrics['retweet_count'],
                           'replies': tweet.public_metrics['reply_count'],
                           'likes': tweet.public_metrics['like_count'],
                           'quote_count': tweet.public_metrics['quote_count']
                           })

    # Change this list of dictionaries into a dataframe
    df = pd.DataFrame(result)
    return df


def collect_tweets(query, start_time, end_time, max_results=500):
    # query = '$MSFT'
    tweet_fields = ['created_at', 'lang', 'geo', 'public_metrics', 'source']
    user_fields = ['username', 'public_metrics', 'description', 'location']
    expansions = 'author_id'
    # start_time = '2019-01-01T00:00:00Z'
    # end_time = '2019-01-01T06:00:00Z'
    # max_results = 10

    # API call
    print(f"Now collecting Tweets using query: {query}\nPeriod: {start_time} - {end_time}")
    pages_list = []
    total_tweets = 0
    for page in tweepy.Paginator(client.search_all_tweets,
                                 query=query,
                                 tweet_fields=tweet_fields,
                                 user_fields=user_fields,
                                 expansions=expansions,
                                 start_time=start_time,
                                 end_time=end_time,
                                 max_results=max_results):
        time.sleep(2)
        pages_list.append(page)
        tweet_count = page.meta['result_count']
        total_tweets = total_tweets + tweet_count
        print(f"This page returned [{tweet_count}] results")

    print(f"Finished collecting, found a total of [{total_tweets}] Tweets")
    if total_tweets > 0:
        df = process_pages(pages_list)
    else:
        print("Returning empty df, as total_tweets = 0")
        df = pd.DataFrame()
    return df


done_list = ['TSLA', 'GME', 'LULU', 'ATVI', 'IQ', 'WMT', 'SBUX', 'F', 'TLRY', 'BAC', 'SHOP','MU', 'SNAP', 'AMD', 'DIS', 'SQ', 'BABA', 'V', 'BA', 'NVDA', 'GE', 'AAPL', 'AMZN', 'MSFT', 'NFLX']
# todo_list = []
# ToDo $TLRY IS MISSING MONTHS!!!!

ticker_list = []
# Directory where Reddit data is saved

twitter_dir = r"E:/Users/Christiaan/Large_Files/Thesis/Twitter/unmerged"


def loop_tweet_collection(save=False):
    if save:
        for ticker in ticker_list:
            # Create folder to save output
            folder_loc = os.path.join(twitter_dir, ticker).replace('\\', '/')
            Path(folder_loc).mkdir(parents=True, exist_ok=True)
            print(f"Now working in folder: {folder_loc}")

            # Setting start and end dates
            start_time = datetime.datetime(2018, 4, 1, 0, 0, 0)
            end_date = datetime.datetime(2020, 9, 1, 0, 0, 0)

            # Loop through dates
            while start_time < end_date:
                # Create file to save output
                year_and_month_and_day = start_time.strftime('%Y_%m_%d')
                file_loc = os.path.join(folder_loc, year_and_month_and_day).replace('\\', '/') + ".csv"
                # print(f"Created file at: {file_loc}")
                # Check if file already exists and skip API request if file exists
                if os.path.isfile(file_loc):
                    print(f"File exists: [{file_loc}]")
                    start_time = start_time + relativedelta(days=1)

                    continue

                # print("FILE DOES NOT EXIST, STARTING API")
                end_time = start_time + relativedelta(days=1)
                query = tf.query_builder(ticker)
                # print(f"Now calling api (query = {query}) for period: {start_time} - {end_time} ")
                print(f"Saving output at: {file_loc}\n")
                df = collect_tweets(query, start_time, end_time, max_results=450)

                # Saving file
                df.to_csv(file_loc, encoding='utf-8')

                # Increment the start_time by 1 month (or day)
                start_time = start_time + relativedelta(days=1)




