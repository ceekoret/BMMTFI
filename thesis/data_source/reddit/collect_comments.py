import requests
from datetime import datetime
import datetime as dt
from dateutil.relativedelta import relativedelta
import traceback
import time
import json
import sys
import csv
import json
import pandas as pd
import numpy as np
from pathlib import Path
import os.path

output_format = "csv"
convert_to_ascii = False  # don't touch this unless you know what you're doing
convert_thread_id_to_base_ten = True  # don't touch this unless you know what you're doing


def write_human_line(handle, obj, is_submission, convert_to_ascii):
    handle.write(str(obj['score']))
    handle.write(" : ")
    handle.write(datetime.fromtimestamp(obj['created_utc']).strftime("%Y-%m-%d"))
    if is_submission:
        handle.write(" : ")
        if convert_to_ascii:
            handle.write(obj['title'].encode(encoding='ascii', errors='ignore').decode())
        else:
            handle.write(obj['title'])
    handle.write(" : u/")
    handle.write(obj['author'])
    handle.write(" : ")
    handle.write(f"https://www.reddit.com{obj['permalink']}")
    handle.write("\n")
    if is_submission:
        if obj['is_self']:
            if 'selftext' in obj:
                if convert_to_ascii:
                    handle.write(obj['selftext'].encode(encoding='ascii', errors='ignore').decode())
                else:
                    handle.write(obj['selftext'])
        else:
            handle.write(obj['url'])
    else:
        if convert_to_ascii:
            handle.write(obj['body'].encode(encoding='ascii', errors='ignore').decode())
        else:
            handle.write(obj['body'])
    handle.write("\n-------------------------------\n")


def write_json_line(handle, obj):
    handle.write(json.dumps(obj))
    handle.write("\n")

# This function converts parent_id from base10 float/int to string
import math


def base36encode(number):
    if math.isnan(number):
        return None
    if isinstance(number, float):
        number = int(number)
    if not isinstance(number, (float, int)):
        return None
    if number == 0:
        return None
    base36 = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = ""
    while number:
        number, i = divmod(number, 36)
        result = base36[i] + result
    return result


def write_csv_line(obj, is_submission):
    # Return different dictionaries for posts or comment searches
    if is_submission:
        # "No customised post return fields, if you want to scrape posts pls update"
        return obj
    else:
        row_dict = {'author': obj.get("author", np.nan),
                    'author_fullname': obj.get("author_fullname", np.nan),
                    'created_utc': obj.get("created_utc", np.nan),
                    'utc_datetime_str': obj.get("utc_datetime_str", np.nan),
                    'permalink': obj.get("permalink", np.nan),
                    'score': obj.get("score", np.nan),
                    'score_hidden': obj.get("score_hidden", np.nan),
                    'total_awards_received': obj.get("total_awards_received", np.nan),
                    'body': obj.get("body", np.nan),
                    'is_submitter': obj.get("is_submitter", np.nan),
                    'id': obj.get("id", np.nan),
                    'link_id': obj.get("link_id", np.nan),
                    'parent_id': obj.get("parent_id", np.nan),
                    'nest_level': obj.get("nest_level", np.nan),
                    'subreddit': obj.get("subreddit", np.nan),
                    'subreddit_id': obj.get("subreddit_id", np.nan)}
        if isinstance(row_dict['parent_id'], int):
            row_dict['parent_id'] = base36encode(row_dict['parent_id'])
        return row_dict


def download_from_url(filename, url_base, output_format, start_datetime, end_datetime, is_submission, convert_to_ascii,
                      debug=False):
    print(f"Now searching for period {end_datetime} until {start_datetime}")
    count = 0
    if output_format == "human" or output_format == "json":
        if convert_to_ascii:
            handle = open(filename, 'w', encoding='ascii')
        else:
            handle = open(filename, 'w', encoding='UTF-8')

    previous_epoch = int(start_datetime.timestamp())
    break_out = False
    first_save = True
    while True:
        new_url = url_base + str(previous_epoch)
        json_text = requests.get(new_url, headers={'User-Agent': "Post downloader by /u/Watchful1"})
        time.sleep(1)  # pushshift has a rate limit, if we send requests too fast it will start returning error messages

        if debug:
            print(new_url)

        try:
            json_data = json_text.json()
        except json.decoder.JSONDecodeError:
            time.sleep(1)
            continue

        if 'data' not in json_data:
            break
        objects = json_data['data']
        if len(objects) == 0:
            break
        #         df = pd.DataFrame(objects)
        #         df.to_csv("test1233.csv")

        row_list = []
        for obj in objects:

            previous_epoch = obj['created_utc'] - 1
            if end_datetime is not None and datetime.utcfromtimestamp(previous_epoch) < end_datetime:
                break_out = True
                break
            count += 1

            # Check if comment body exists, removing comment from df is it doesnt exist
            if obj['body'] == "[removed]":
                continue

            try:
                if output_format == "human":
                    write_human_line(handle, obj, is_submission, convert_to_ascii)
                elif output_format == "csv":
                    row_list.append(write_csv_line(obj, is_submission))
                elif output_format == "json":
                    write_json_line(handle, obj)
            except Exception as err:
                if 'permalink' in obj:
                    print(f"Couldn't print object: https://www.reddit.com{obj['permalink']}")
                else:
                    print(f"Couldn't print object, missing permalink: {obj['id']}")
                print(err)
                print(traceback.format_exc())

        # Create dataframe from rowlist (which can be saved later)
        df = pd.DataFrame(row_list)

        # Columns to keep
        columns = ['author',
                   'author_fullname',
                   'created_utc',
                   'utc_datetime_str',
                   'permalink',
                   'score',
                   'score_hidden',
                   'total_awards_received',
                   'body',
                   'is_submitter',
                   'id',
                   'link_id',
                   'parent_id',
                   'nest_level',
                   'subreddit',
                   'subreddit_id']
        # When you want to receive the whole dataframe, uncomment the line below
        # columns = df.columns

        # Check if file exists, if so append dataframe. Else create new dataframe.
        if len(df.index) == 0:
            print(f"No observations found, saving empty dataframe")
            df.to_csv(filename)
        elif first_save:
            print(f"Saving new dataframe at {filename} with [{len(df.index)}] obs")
            df.to_csv(filename, encoding='utf-8', index=False, columns=columns)
            first_save = False
        else:
            print(f"Appending to {filename} with [{len(df.index)}] obs")
            df.to_csv(filename, mode='a', header=False, index=False, columns=columns)

        if break_out:
            break

    if output_format == "human" or output_format == "json":
        handle.close()


# if __name__ == "__main__":
def run(start_time, end_time, subreddit="", username="", thread_id="", comments_save_loc="comments.csv", debug=False):
    filter_string = None
    if username == "" and subreddit == "" and thread_id == "":
        print("Fill in username, subreddit or thread id")
        sys.exit(0)
    if output_format not in ("human", "csv", "json"):
        print("Output format must be one of human, csv, json")
        sys.exit(0)

    filters = []
    if username:
        filters.append(f"author={username}")
    if subreddit:
        filters.append(f"subreddit={subreddit}")
    if thread_id:
        if convert_thread_id_to_base_ten:
            filters.append(f"link_id={int(thread_id, 36)}")
        else:
            filters.append(f"link_id=t3_{thread_id}")
    filter_string = '&'.join(filters)

    url_template = "https://api.pushshift.io/reddit/{}/search?limit=1000&order=desc&{}&before="

    if not thread_id:
        test = "remove this when done"
    #         download_from_url(posts_save_loc, url_template.format("submission", filter_string), output_format, start_time, end_time, True, convert_to_ascii)
    download_from_url(comments_save_loc, url_template.format("comment", filter_string), output_format, start_time,
                      end_time, False, convert_to_ascii, debug=False)


reddit_dir = r"E:\Users\Christiaan\Large_Files\Thesis\reddit\comments"

# Starting datetime
start_date = dt.datetime(2018, 4, 1, 0, 0)
end_date = dt.datetime(2020, 9, 1, 0, 0)

subreddits = ['wallstreetbets', 'stocks', 'investing', 'stockmarket', 'pennystocks']
# subreddits = ['pennystocks']

save = True
for subreddit in subreddits:
    # Create folder to save output
    folder_loc = os.path.join(reddit_dir, subreddit).replace('\\', '/')
    Path(folder_loc).mkdir(parents=True, exist_ok=True)

    date_time = start_date
    while date_time < end_date:
        # Create 1 month search period in epoch time
        year_and_month = date_time.strftime('%Y_%m')

        # As the search run() and download_from_url() function work time backwards, start time and end time are swapped
        end = date_time
        start = date_time + relativedelta(months=1)

        # Create file to save output
        file_loc = os.path.join(folder_loc, year_and_month).replace('\\', '/') + ".csv"
        print(file_loc)
        # Check if file already exists and skip API request if file exists
        if os.path.isfile(file_loc) and save:
            print(f"File exists: [{file_loc}]")
            date_time = date_time + relativedelta(months=1)

            continue

        if save:
            run(start_time=start, end_time=end, subreddit=subreddit, comments_save_loc=file_loc, debug=False)
        else:
            print("Save is off")

        # Adding 1 month to date_time tracker
        date_time = date_time + relativedelta(months=1)