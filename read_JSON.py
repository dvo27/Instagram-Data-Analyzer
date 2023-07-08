import json
from collections import Counter
import pandas as pd


def create_msg_df(input_path):
    """
    Loads JSON from path and creates a dataframe from message section of JSON
    :param input_path: A Path object of a path to a message JSON file
    :return: A dataframe containing information in the message JSON file
    """
    with open(input_path) as message_file:
        message_json = json.load(message_file)
    messages_dict = message_json['messages']
    df = pd.DataFrame.from_dict(messages_dict)
    return df


def filter_msg_content(df):
    """
    Creates new df skipping action messages, returning the messages while skipping over all NotANumber values
    :param df: A dataframe of message JSON file
    :return:
    """
    content_df = df.loc[
        df['content'].str.contains("sent an attachment.|shared a story.|Liked a message|Reacted|to your message") == False].copy()
    content_df['content'].dropna(inplace=True)  # Skips all NotANumber values
    content_column = content_df['content']  # Returns the content column of the newly copied dataframe
    return content_column


def five_most_common_words(input_path):
    """
    Prints a dataframe with the 5 most common words and their counts.
    :param input_path: A Path object of a path to a message JSON file
    """
    df = create_msg_df(input_path)
    content_column = filter_msg_content(df)

    # Creates and prints a list of tuples with the five most common words and their counts
    common_word_counter = Counter(" ".join(content_column).split()).most_common(5)
    common_word_df = pd.DataFrame(common_word_counter, columns=['Word', 'Count'])
    return f'\nYour Five Most Common Words: \n{common_word_df}'


def get_message_df_length(input_path):
    """
    Get the number of messages sent within a DM conversation.
    :param input_path: A Path object of a path to a message JSON file
    :return:
    """
    df = create_msg_df(input_path)
    content_column = filter_msg_content(df)
    return f'The number of messages in the conversation: \n{content_column.size}'


def message_data():
    try:
        file_path = input('Please input path to message data file, ending in .json: ')
        print(five_most_common_words(file_path))
        print()
        print(get_message_df_length(file_path))
    except FileNotFoundError:
        print('ERROR: The given directory does not exist or is not a valid path')
