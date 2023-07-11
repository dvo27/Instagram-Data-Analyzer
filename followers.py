import json
import pandas as pd
import datetime
import main


def create_follower_df(path_input):
    with open(path_input, encoding='utf-8') as f:
        following_json = json.load(f)
    following_data_list = [f['string_list_data'][0] for f in following_json['relationships_following']]
    df = pd.DataFrame(following_data_list)
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


def following_data():
    try:
        file_input = input('Enter path to followers_and_following/following.json file: \n')

        follower_df = create_follower_df(file_input)
        print(first_five_following(follower_df))
    except FileNotFoundError:
        print('\nERROR: The given directory does not exist or is not a valid path')


def follow_data():
    print('\nWelcome To The Follow Data Section!')
    print('------------------------------------')
    menu_choice = input('\nPlease choose an option below!:'
                        '\n[1] : Get Following Data\n'
                        '[return] : Return to main menu\n'
                        '-------------------------------------\n')
    while menu_choice != 'return':
        if menu_choice == '1':
            following_data()
            follow_data()
        else:
            print('ERROR: Invalid choice')
            follow_data()
    else:
        print()
        main.main()
