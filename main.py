"""
This module provides a way to work with Instagram data.

It includes the class 'InstagramData' to handle the Instagram data files (post comments, followers, 
following, liked comments, and liked posts) and their paths, as well as a function 'test_and_init' 
to initialize the InstagramData object and check the file paths, and a 'main' function that prompts 
the user to either get direct messages with a specific user, get follow data, or quit the program.

Classes:
    InstagramData: A class to represent the Instagram data.

Functions:
    test_and_init(): Initializes the InstagramData object and checks the file paths.
    main(): Presents a menu to the user and executes the selected option.
"""

import sys
from pathlib import Path
import message as msg
import followers as follow
import comments as cmt


class InstagramData:
    """
    A class to represent the Instagram data.
    
    Attributes:
        main_path (str): The main path to the Instagram data.
        post_comments_path (Path): The path to the post comments JSON file.
        followers_path (Path): The path to the followers JSON file.
        following_path (Path): The path to the following JSON file.
        liked_comments (Path): The path to the liked comments JSON file.
        liked_posts (Path): The path to the liked posts JSON file.
    
    Methods:
        init_paths(): Initializes the paths for post comments, 
                      followers, following, liked comments, and liked posts.
        check_paths(): Checks if the initialized paths exist and raises an 
                       exception if any path does not exist.
    """


    def __init__(self, main_path) -> None:
        """
        Initializes the Instagram_data object with the main path to the Instagram data.

        :param main_path: The main path to the Instagram data.
        :type main_path: str
        """
        self.main_path = main_path
        self.post_comments_path = None
        self.followers_path = None
        self.following_path = None
        self.liked_comments = None
        self.liked_posts = None


    def init_paths(self):
        """
        Initializes the paths for post comments, followers, 
        following, liked comments, and liked posts.

        :return: None
        """
        self.post_comments_path = Path(self.main_path + '/comments/post_comments.json')
        self.followers_path = Path(self.main_path + '/followers_and_following/followers_1.json')
        self.following_path = Path(self.main_path + '/followers_and_following/following.json')
        self.liked_comments = Path(self.main_path + '/likes/liked_comments.json')
        self.liked_posts = Path(self.main_path + '/likes/liked_posts.json')


    def check_paths(self):
        """
        Checks if the initialized paths exist and raises a FileNotFoundError 
        if any path does not exist.

        :return: None
        :raise FileNotFoundError: If any initialized path does not exist.
        """
        paths = [self.post_comments_path, self.followers_path, self.following_path,
                 self.liked_comments, self.liked_posts]
        print()
        for path in paths:
            if path and path.exists():
                print(f"{path} exists.")
            else:
                print(f"ERROR: {path} does not exist.")
                sys.exit()


def test_and_init():
    """
    Prompts the user for the main path to their Instagram data, initializes an InstagramData object 
    with the provided path, initializes the paths for post comments, followers, following, 
    liked comments, and liked posts, and checks if the initialized paths exist.

    :return: None
    """
    main_path = input('Please put in the path to your Instagram Data: \n')
    instagram_data_obj = InstagramData(main_path)
    instagram_data_obj.init_paths()
    instagram_data_obj.check_paths()

    return instagram_data_obj



def main():
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
    
    valid_options = ['1', '2', 'Q', 'q']
    menu_choice = input('\nPlease choose an option below!:'
                        '\n[1] : Get DMs With Specific User Data\n'
                        '[2] : Get Follow Data\n'
                        '[3] : Check Comments & Liked Data\n'
                        '[Q] : Quit Program\n'
                        '-------------------------------------\n')

    if menu_choice not in valid_options:
        print('\nInvalid option! Please try again.\n')
        main()
    else:
        if menu_choice == '1':
            msg.message_data()
        elif menu_choice == '2':
            follow.follow_data(ig_data)
        elif menu_choice == '3':
            cmt.comment_menu()
        elif menu_choice == 'Q' or 'q':
            print('\nEnding program...Goodbye!')
            sys.exit()


if __name__ == '__main__':
    ig_data = test_and_init()
    main()
