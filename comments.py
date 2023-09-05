import json
import pandas as pd
import main


def create_post_df(path_input, instagram_data):
    try:
        with open(path_input, encoding='utf-8') as f:
            post_comments_json = json.load(f)
        post_comments_list = [post_comments_json]
        print(post_comments_list)
        # df = pd.DataFrame.from_dict(post_comments_json['comments_media_comments'][0])
        # print(df)
    except (AttributeError, TypeError) as error:
        print(f'ERROR: {error}')


def comment_menu(instagram_data):
    print('\nWelcome To The Comment Data Section!')
    print('------------------------------------')
    menu_choice = input('\nPlease choose an option below!:'
                        '\n[1] : See Post Comments Data\n'
                        '[2] : See Reported Comments Data\n'
                        '[3] : See Reels Comments Data\n'
                        '\n[return] : Return to main menu\n'
                        '-------------------------------------\n')
    while menu_choice != 'return':
        if menu_choice == '1':
            create_post_df(instagram_data.post_comments, instagram_data)
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
    main.main()