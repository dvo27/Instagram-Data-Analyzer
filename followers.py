import json
import pandas as pd
import datetime

file_input = input('give me following file: ')



def create_follower_df(path_input):
    with open(path_input, encoding='utf-8') as f:
        following_json = json.load(f)
    following_data = [f['string_list_data'][0] for f in following_json['relationships_following']]
    df = pd.DataFrame(following_data)
    return df


def sort_df_time(df):
    return df.sort_values(by=['timestamp'])


def format_timestamp(timestamps):
    formatted_timestamps = timestamps.apply(
        lambda time: datetime.datetime.fromtimestamp(time).strftime('%m-%d-%Y %H:%M'))
    return formatted_timestamps


def first_five_following(df):
    first_five_head = sort_df_time(df).head()
    first_five_head['timestamp'] = format_timestamp(first_five_head['timestamp'])
    first_five_head = first_five_head.to_string()
    return f'\nYour First Five Followings: \n{first_five_head}\n'


follower_df = create_follower_df(file_input)

print(first_five_following(follower_df))
