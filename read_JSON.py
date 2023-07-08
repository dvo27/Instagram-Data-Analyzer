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
    :return: Column of only the messages from the dataframe
    """
    # Creates a copy of the df removing the following phrases within the content column
    content_df = df.loc[
        df['content'].str.contains("sent an attachment.|shared a story.|Liked a message|Reacted|to your message") == False].copy()
    content_df['content'].dropna(inplace=True)  # Skips all NotANumber values
    content_column = content_df['content']  # Returns the content column of the newly copied dataframe
    return content_column


def five_most_common_words(df: pd.DataFrame):
    """
    Prints a dataframe with the 5 most common words and their counts.
    :param df: A Dataframe object containing the data from the messages with a user
    """
    content_column = filter_msg_content(df)

    # Creates and prints a list of tuples with the five most common words and their counts
    common_word_counter = Counter(" ".join(content_column).split()).most_common(5)
    common_word_df = pd.DataFrame(common_word_counter, columns=['Word', 'Count'])
    return f'\nYour Five Most Common Words: \n{common_word_df}'


def get_message_df_length(df):
    """
    Get the number of messages sent within a DM conversation.
    :param df: A Dataframe object containing the data from the messages with a user
    :return: F-string containing the amount of messages in a conversation excluding action statements
    """
    content_column = filter_msg_content(df)
    return f'The number of messages in the conversation: \n{content_column.size}'


def get_first_five_messages(df):
    content_df = df.loc[
        df['content'].str.contains(
            "sent an attachment.|shared a story.|Liked a message|Reacted|to your message") == False].copy()
    content_df['content'].dropna(inplace=True)


def message_data():
    print('\nWelcome To The Message Data Section!')
    print('--------------------------------------')
    try:
        file_path = input('Please input path to message data file, ending in .json: ')
        df = create_msg_df(file_path)

        print(five_most_common_words(df))
        print()
        print(get_message_df_length(df))
    except FileNotFoundError:
        print('\nERROR: The given directory does not exist or is not a valid path')
