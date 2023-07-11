import json
import datetime
from collections import Counter
import pandas as pd
import main


def create_msg_df(input_path):
    """
    Loads JSON from path and creates a dataframe from message section of JSON
    :param input_path: A Path object of a path to a message JSON file
    :return: A dataframe containing information in the message JSON file
    """
    with open(input_path, encoding='UTF-8') as message_file:
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
        df['content'].str.contains(
            "sent an attachment.|shared a story.|Liked a message|Reacted|to your message") == False].copy()
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
    common_word_df = common_word_df.to_string(index=False)
    return f'\nYour Five Most Common Words: \n{common_word_df}'


def get_message_df_length(df):
    """
    Get the number of messages sent within a DM conversation.
    :param df: A Dataframe object containing the data from the messages with a user
    :return: F-string containing the amount of messages in a conversation excluding action statements
    """
    content_column = filter_msg_content(df)
    return f'\nNumber Of Messages In The Conversation: \n{content_column.size}'


def decode_messages(messages):
    """
    Decode messages from their original encoding to UTF-8.
    :param messages: Series containing the messages to be decoded
    :return: Decoded messages
    """
    decoded_messages = messages.apply(lambda message: message.encode('latin-1').decode('utf-8'))
    return decoded_messages


def format_timestamps_ms(timestamps):
    """
    Format timestamps from milliseconds to a proper date format.
    :param timestamps: Series containing the timestamps to be formatted
    :return: Formatted timestamps
    """
    formatted_timestamps = timestamps.apply(lambda time: datetime.datetime.fromtimestamp(time / 1000)
                                            .strftime('%m-%d-%Y %H:%M'))
    return formatted_timestamps


def get_first_five_messages(df):
    """
    Gets the first five messages in a DM conversation and shows each sender and the timestamp
    along with their message.
    :param df: A DataFrame object containing the data from the messages with a user
    :return: F-string containing a DataFrame string of the first five messages
    """
    # Filter df from any action statements and remove any NotANumber values
    filtered_df = df.loc[
        df['content'].str.contains(
            "sent an attachment.|shared a story.|Liked a message|Reacted|to your message|liked a message") == False].copy()
    filtered_df['content'].dropna(inplace=True)

    # Get first five messages and reverse the order
    reversed_filtered_df_head = filtered_df.tail(5)[['sender_name', 'timestamp_ms', 'content']].iloc[::-1]

    # Decode messages & format timestamps
    reversed_filtered_df_head['content'] = decode_messages(reversed_filtered_df_head['content'])
    reversed_filtered_df_head['timestamp_ms'] = format_timestamps_ms(reversed_filtered_df_head['timestamp_ms'])

    # Renaming columns to fit new changes
    reversed_filtered_df_head.rename(columns={
        'sender_name': 'sender_name', 'timestamp_ms': 'timestamp', 'content': 'message'}, inplace=True)
    reversed_filtered_df_head = reversed_filtered_df_head.to_string(index=False, justify='left')

    return f'\nYour First Five Messages: \n{reversed_filtered_df_head}\n'


def message_data():
    print('\nWelcome To The Message Data Section!')
    print('------------------------------------')
    print('To return to the main menu please type "return"')
    try:
        file_path = input('\nPlease input path to message data file, ending in .json: \n')
        if file_path != 'return':
            df = create_msg_df(file_path)
            print(five_most_common_words(df))
            print(get_first_five_messages(df))
            print(get_message_df_length(df))
        else:
            print()
            main.main()
    except FileNotFoundError:
        print('\nERROR: The given directory does not exist or is not a valid path')
