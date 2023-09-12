"""
This module facilitates the interaction with and analysis of Instagram data.

It leverages the InstagramData class to initialize and manage paths pertaining to various 
elements of Instagram data including post comments, followers, followings, liked comments, 
and liked posts. The module offers functions to both initialize the InstagramData object 
with necessary paths and to present a user menu for diverse data retrieval and analysis operations.

Classes:
    InstagramData: A class housed in the 'instagram_data_class' module, utilized here to represent
    and manage the Instagram data paths and file operations.

Functions:
    test_and_init(): Prompts the user to input the primary path of their Instagram data, initializes 
    an InstagramData object with the given path, further initiates various data paths 
    (like post comments, followers, etc.), and verifies the existence of these paths. 
    Returns the initialized InstagramData object.
    
    main(instagram_data: ig_data.InstagramData): Facilitates user interaction with the program 
    through a menu-driven interface. Based on user input, it triggers specific data retrieval 
    and analysis operations pertaining to messages, follow data, comments, or liked posts, 
    or exits the program.
"""

import sys
import instagram_data_class as ig_data
import message as msg
import followers as follow
import comments as cmt
import liked

# TODO: Comment throughout functions in all modules

# comments.py:
# TODO: Introduce handling for multi file post comments

# message.py:
# TODO: find a way to close matplotlib gui after a run of a given message path
# TODO: bug when rerunning another message while graph still open


def test_and_init():
    """
    Prompts the user for the main path to their Instagram data, initializes an InstagramData object 
    with the provided path, initializes the paths for post comments, followers, following, 
    liked comments, and liked posts, and checks if the initialized paths exist.

    :return: None
    """
    main_path = input('Please put in the path to your Instagram Data: \n')
    instagram_data_obj = ig_data.InstagramData(main_path)
    instagram_data_obj.init_paths()
    instagram_data_obj.check_paths()

    return instagram_data_obj


def main(instagram_data: ig_data.InstagramData):
    """
    Presents a menu to the user and executes the selected option.

    The user is presented with a menu of three options:
    1. Get DMs With Specific User Data
    2. Get Follow Data
    Q. Quit Program

    If the user selects '1', the message_data function of the message module is executed.
    If the user selects '2', the follow_data function of the follow module is executed.
    If the user selects 'Q' or 'q', the program is terminated.

    If an invalid option is entered, the menu is presented again.

    :return: None
    """

    valid_options = ['1', '2', '3', '4', 'Q', 'q']
    menu_choice = input('\nPlease choose an option below!:'
                        '\n[1] : Get DMs With Specific User Data\n'
                        '[2] : Get Follow Data\n'
                        '[3] : Check Comments Data\n'
                        '[4] : Check Liked Data\n'
                        '[Q] : Quit Program\n'
                        '-------------------------------------\n')

    if menu_choice not in valid_options:
        print('\nInvalid option! Please try again.\n')
        main(instagram_data)
    else:
        if menu_choice == '1':
            msg.message_data(instagram_data)
        elif menu_choice == '2':
            follow.follow_data(instagram_data)
        elif menu_choice == '3':
            cmt.comment_menu(instagram_data)
        elif menu_choice == '4':
            liked.liked_menu(instagram_data)
        elif menu_choice in ('Q', 'q'):
            print('\nEnding program...Goodbye!')
            sys.exit()


if __name__ == '__main__':
    ig_data_obj = test_and_init()
    main(ig_data_obj)
