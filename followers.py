import json
import pandas as pd

file_input = input('give me following file: ')


def create_follower_df(file_input):
    with open(file_input, encoding='utf-8') as f:
        following_json = json.load(f)
    following_data = [f['string_list_data'][0] for f in following_json['relationships_following']]
    df = pd.DataFrame(following_data)
    return df


print(create_follower_df(file_input))
