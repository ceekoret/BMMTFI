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

from pathlib import Path
import os.path



# Directory where Reddit data is saved
reddit_dir = r"C:/Users/Ck0rt/Documents/Large files/School/MSc Finance & Investments/Thesis/Reddit/posts"

# Starting datetime
start_date = dt.datetime(2018, 4, 1, 0, 0)
end_date = dt.datetime(2020, 9, 1, 0, 0)

subreddits = ['wallstreetbets', 'stocks', 'investing', 'stockmarket', 'pennystocks']

save = False
for subreddit in subreddits:
    # Create folder to save output
    folder_loc = os.path.join(reddit_dir, subreddit).replace('\\', '/')
    print(folder_loc)
    Path(folder_loc).mkdir(parents=True, exist_ok=True)

    date_time = start_date
    while date_time < end_date:
        # Create 1 month search period in epoch time
        year_and_month = date_time.strftime('%Y_%m')
        start = int(date_time.timestamp())
        end = date_time + relativedelta(months=1)
        end = int(end.timestamp())

        # Create file to save output
        file_loc = os.path.join(folder_loc, year_and_month).replace('\\', '/') + ".csv"

        # Check if file already exists and skip API request if file exists
        if os.path.isfile(file_loc) and save:
            print(f"File exists: [{file_loc}]")
            date_time = date_time + relativedelta(months=1)

            continue

        # Api cooldown time
        time.sleep(3)
        print(f"Now collecting data for [{subreddit}] in [{date_time.strftime('%B %Y')}]")

        # Request data from Pushshift
        start_time = time.time()
        posts = api.search_submissions(subreddit=subreddit, limit=300000, after=start, before=end)
        print(f'Retrieved {len(posts)} posts from Pushshift in [{time.time() - start_time}] seconds')
        print(posts)
        print(type(posts))
        exit()
        # Save output to CSV via dataframe
        reddit_df = pd.DataFrame(posts)

        columns = ['author', 'created_utc', 'full_link', 'id', 'num_comments', 'score', 'selftext',
                   'subreddit', 'subreddit_id', 'subreddit_subscribers', 'title', 'url']

        if save:
            reddit_df.to_csv(file_loc, header=True, index=False, columns=columns)
            print(f"Saving csv at [{file_loc}]")
        else:
            print(reddit_df)

        # Adding 1 month to date_time tracker
        date_time = date_time + relativedelta(months=1)

