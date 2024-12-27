import sys
from pathlib import Path


class InstagramData:
    """
    A class to represent the Instagram data.
    
    Attributes:
        main_path (str): The main path to the Instagram data.
        post_comments (Path): The path to the post comments JSON file.
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
        self.followers_path = None
        self.following_path = None
        self.liked_comments = None
        self.liked_posts = None
        self.post_comments = None


    def init_paths(self):
        """
        Initializes the paths for post comments, followers, 
        following, liked comments, and liked posts.

        :return: None
        """
        self.followers_path = Path(self.main_path + '/connections/followers_and_following/followers_1.json')
        self.following_path = Path(self.main_path + '/connections/followers_and_following/following.json')
        self.liked_comments = Path(self.main_path + '/your_instagram_activity/likes/liked_comments.json')
        self.liked_posts = Path(self.main_path + '/your_instagram_activity/likes/liked_posts.json')
        self.post_comments = Path(self.main_path + '/your_instagram_activity/comments/post_comments_1.json')


    def check_paths(self):
        """
        Checks if the initialized paths exist and raises a FileNotFoundError 
        if any path does not exist.

        :return: None
        :raise FileNotFoundError: If any initialized path does not exist.
        """
        paths = [self.followers_path, self.following_path, self.liked_comments, self.liked_posts,
                 self.post_comments]
        print()
        for path in paths:
            if path and path.exists():
                print(f"{path} loaded.")
            else:
                print(f"ERROR: {path} does not exist.")
                sys.exit()
