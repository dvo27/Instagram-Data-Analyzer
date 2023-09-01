import json
import pandas as pd
import datetime
import main


def create_following_df(path_input):
    """
    Creates a Dataframe from the following.json file.
    :param path_input: Path to the following.json file.
    :return: Dataframe containing the following data.
    """
    try:
        with open(path_input, encoding='utf-8') as f:
            following_json = json.load(f)
        following_data_list = [f['string_list_data'][0] for f in following_json['relationships_following']]
        df = pd.DataFrame(following_data_list)
        return df
    except (AttributeError, TypeError) as f:
        print(f'\nERROR: {f}')
        print('\nERROR: Please place the following.json file located in the followers_and_following folder')
        follow_data()


def create_follower_df(path_input):
    """
    Creates a DataFrame from the follower_1.json file.
    :param path_input: Path to the follower JSON file.
    :return: DataFrame containing the follower data.
    """
    try:
        with open(path_input, encoding='utf-8') as f:
            follower_json = json.load(f)
        following_data_list = [f['string_list_data'][0] for f in follower_json]
        df = pd.DataFrame(following_data_list)
        return df
    except (AttributeError, TypeError) as f:
        print(f'\nERROR: {f}')
        print('\nPlease place the follower_1.json file located in the followers_and_following folder')
        follow_data()


def sort_df_time(df):
    """
    Sorts a DataFrame based on the 'timestamp' column.

    :param df: DataFrame to be sorted.
    :return: Sorted DataFrame.
    """
    return df.sort_values(by=['timestamp'])


def format_timestamp(timestamps):
    """
    Formats timestamps in a Series to a specific date-time format.

    :param timestamps: Series of timestamps.
    :return: Formatted timestamps as Series.
    """
    formatted_timestamps = timestamps.apply(
        lambda time: datetime.datetime.fromtimestamp(time).strftime('%m-%d-%Y %H:%M'))
    return formatted_timestamps


def first_five_following(df):
    """
    Retrieves the first five followings from a DataFrame and formats the timestamps.

    :param df: DataFrame containing following data.
    :return: F-string with the first five followings.
    """
    first_five_head = sort_df_time(df).head()
    first_five_head['timestamp'] = format_timestamp(first_five_head['timestamp'])
    first_five_head = first_five_head.to_string()
    return f'\nYour First Five Followings: \n{first_five_head}\n'


def recent_five_following(df):
    """
    Retrieves the most recent five followings from a DataFrame and formats the timestamps.

    :param df: DataFrame containing following data.
    :return: F-string with the most recent five followings.
    """
    first_five_head = sort_df_time(df).tail()
    first_five_head['timestamp'] = format_timestamp(first_five_head['timestamp'])
    first_five_head = first_five_head.to_string()
    return f'\nYour Most Recent Five Followings: \n{first_five_head}\n'


def following_data():
    """
    Retrieves and displays following data.

    Asks for the path to the 'following.json' file and displays the first five and most recent five followings.
    """
    try:
        file_input = input('Please enter path to followers_and_following/following.json file: \n')

        follower_df = create_following_df(file_input)
        print(first_five_following(follower_df))
        print(recent_five_following(follower_df))
    except FileNotFoundError:
        print('\nERROR: The given directory does not exist or is not a valid path')


def not_following_back():
    """
    Displays users who are not following the user back.

    Asks for the paths to the 'followers_1.json' and 'following.json' files.
    Displays the users who are not following back based on the data in these files.
    """
    try:
        followers_path = input('Please enter the path to followers_and_following/followers_1.json: \n')
        following_path = input('Please enter path to followers_and_following/following.json file: \n')


        follower_df = create_follower_df(followers_path)[['href', 'value']]
        following_df = create_following_df(following_path)[['href', 'value']]

        non_follow_back_df = follower_df.merge(following_df.drop_duplicates(), on=['href', 'value'], how='right', indicator=True)
        non_follow_back_df = non_follow_back_df[non_follow_back_df['_merge'] == 'right_only'][['href', 'value']]
        non_follow_back_df.rename(columns={
            'href': 'Profile Link', 'value': 'Username'}, inplace=True)
        non_follow_back_df = non_follow_back_df.to_string()

        print('\nUsers Not Following You Back:')
        print(non_follow_back_df)

    except FileNotFoundError:
        print('\nERROR: The given directory does not exist or is not a valid path')


def follow_data():
    print('\nWelcome To The Follow Data Section!')
    print('------------------------------------')
    menu_choice = input('\nPlease choose an option below!:'
                        '\n[1] : Get Following Data\n'
                        '[2] : Check Who Isn\'t Following You Back\n'
                        '\n[return] : Return to main menu\n'
                        '-------------------------------------\n')
    while menu_choice != 'return':
        if menu_choice == '1':
            following_data()
            follow_data()
        elif menu_choice == '2':
            not_following_back()
            follow_data()
        else:
            print('ERROR: Invalid choice')
            follow_data()
    else:
        print()
        main.main()
