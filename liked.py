import json
import pathlib
import pandas as pd
import instagram_data_class as ig_data
import main


def create_liked_comments_df(file_path: pathlib.Path):
    try:
        with open(file_path, encoding='UTF-8') as f:
            liked_cmt_json = json.load(f)
        post_owner = pd.DataFrame([cmt['title'] for cmt in liked_cmt_json['likes_comment_likes']])
        metadata_df = pd.DataFrame([cmt['string_list_data'][0] for cmt in liked_cmt_json['likes_comment_likes']])
        df = post_owner.merge(metadata_df)
        # df = pd.DataFrame({'post_owner': post_owner, 'href': href})
        print(df)
    except (AttributeError, TypeError) as error:
        print(f'ERROR: {error}')

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
            
            
    main.main(instagram_data)
