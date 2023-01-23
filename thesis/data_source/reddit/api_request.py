"""
Data from Robintrack starts on 02/05/2018. I collect data beginning with 1 month prior to this period, being 01/04/2018.
Data will be collected each month until the September.
"""

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



def fxn(item):
    if 'selftext' not in item:
        print("[selftest] is missing")
        return False

    #     for key in item:
    #         print(type(item[key]))
    #         print(f"{key} --- {item[key]} + {type(item[key])}")

    rules = [item['score'] > -100,
             item['num_comments'] > 0,
             item['selftext'] not in ("[removed]", "")]

    return all(rules)


start = int(dt.datetime(2021,1,1,0,0).timestamp())
end = int(dt.datetime(2021,2,1,0,0).timestamp())
subreddit="wallstreetbets"
limit=1000

start_time = time.time()

posts = api.search_submissions(subreddit="wallstreetbets", limit=limit, after=start, before=end, filter_fn=fxn)
print(f'Retrieved {len(posts)} posts from Pushshift')
print(f"--- Runtime with filter: {time.time() - start_time} seconds ---")

