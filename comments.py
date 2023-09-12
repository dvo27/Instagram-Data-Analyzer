import json
import pandas as pd
import main
import instagram_data_class as ig_data
import message


def create_post_df(path_input, instagram_data):
    """
    Creates a data frame of comments sent by the user under posts sorted
    by sent date from oldest to most recent.
    :param path_input: Path to post comment JSON file
    :param instagram_data: InstagramData class object
    :return: Created DataFrame
    """
    try:
        with open(path_input, encoding='utf-8') as f:
            post_comments_json = json.load(f)

        post_comments_list = [cmt['string_map_data'] for cmt in post_comments_json['comments_media_comments']
                              if 'Comment' in cmt['string_map_data']]

        df = pd.DataFrame(post_comments_list)

        # Grab values from their dict forming to only show in column
        df['Comment'] = df['Comment'].str.get('value')
        df['Media Owner'] = df['Media Owner'].str.get('value')
        df['Time'] = df['Time'].str.get('timestamp')

       # Decoding comments to the correct encoding
        df['Comment'] = message.decode_messages(df['Comment'])

        # Sort DataFrame by time
        df = df.sort_values(by=['Time'])

        # Convert UNIX timestamp to datetime object
        df['Time'] = pd.to_datetime(df['Time'], unit='s')

        # Convert to the desired timezone
        df['Time'] = df['Time'].dt.tz_localize('UTC').dt.tz_convert('US/Pacific')

        # Convert datetime object to desired string format
        df['Time'] = df['Time'].dt.strftime('%m-%d-%Y %H:%M:%S')

        return df
    except (AttributeError, TypeError) as error:
        print(f'ERROR: {error}')


def first_five_post_comments(df: pd.DataFrame):
    """
    Prints out the five first ever comments the user made with info on
    whose post the comments were under and their dates

    :param df: Pandas DataFrame of post comments data
    """
    print('Your First Five Comments: ')
    print(df.head().to_string(index=False))


def top_five_accounts(df: pd.DataFrame):
    """
    Prints a DataFrame containing the top 5 accounts that the user has
    commented under and the number of comments under that account
    :param df: Pandas DataFrame of post comments data
    """
    print('Accounts With The Most Comments Under:')
    print(df['Media Owner'].value_counts().head().to_string())


def comment_menu(instagram_data: ig_data.InstagramData):
    print('\nWelcome To The Comment Data Section!')
    print('------------------------------------')
    menu_choice = input('\nPlease choose an option below!:'
                        '\n[1] : See Post Comments Data\n'
                        '[2] : See Reported Comments Data\n'
                        '[3] : See Reels Comments Data\n'
                        '\n[return] : Return to main menu\n'
                        '-------------------------------------\n')
    while menu_choice != 'return':
        df = create_post_df(instagram_data.post_comments, instagram_data)
        if menu_choice == '1':
            first_five_post_comments(df)
            print()
            top_five_accounts(df)
            comment_menu(instagram_data)
        elif menu_choice == '2':
            print('2')
            comment_menu(instagram_data)
        elif menu_choice == '3':
            print('3')
            comment_menu(instagram_data)
        else:
            print('ERROR: Invalid choice, please try again')
            comment_menu(instagram_data)
    print()
    main.main(instagram_data)