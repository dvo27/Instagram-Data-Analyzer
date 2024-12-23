import json
import pathlib
import pandas as pd
import instagram_data_class as ig_data
import message as msg
import main


def create_liked_comments_df(file_path: pathlib.Path):
    try:
        # load the json data
        with open(file_path, encoding='UTF-8') as f:
            liked_cmt_json = json.load(f)

        # break up json into two dataframes
        post_owner = pd.DataFrame([cmt['title'] for cmt in liked_cmt_json['likes_comment_likes']])
        metadata_df = pd.DataFrame([cmt['string_list_data'][0] for cmt in liked_cmt_json['likes_comment_likes']])

        # combine dfs into one horizontal df with postowner, post href, comment value, and timestamp
        df = pd.concat([post_owner, metadata_df], axis=1)

        # delete the value column bc it just shows thumbs up emoji (user liked it)
        df = df.drop(['value'], axis=1)

        # convert the timestamp column to show correct date unit, not in ms
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

        print(df.head())

        return df
    except Exception as error:
        print(f'\nERROR: {error}')

def liked_menu(instagram_data: ig_data.InstagramData):
    print('\nWelcome To The Liked Data Section!')
    print('------------------------------------')
    menu_choice = input('\nPlease choose an option below!:'
                        '\n[1] : Check Liked Comments Data\n'
                        '[2] : Check Liked Posts Data\n'
                        '\n[return] : Return to main menu\n'
                        '-------------------------------------\n')
    while menu_choice != 'return':
        if menu_choice == '1':
            create_liked_comments_df(instagram_data.liked_comments)
            liked_menu(instagram_data)
        elif menu_choice == '2':
            print('\nliked post section coming soon')

            menu_choice = input('\nPlease choose an option below!:'
                                '\n[1] : Check Liked Comments Data\n'
                                '[2] : Check Liked Posts Data\n'
                                '\n[return] : Return to main menu\n'
                                '-------------------------------------\n')
        else:
            print('\nInvalid choice, please try again!')

            menu_choice = input('\nPlease choose an option below!:'
                                '\n[1] : Check Liked Comments Data\n'
                                '[2] : Check Liked Posts Data\n'
                                '\n[return] : Return to main menu\n'
                                '-------------------------------------\n')


    main.main(instagram_data)
