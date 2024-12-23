"""
Message Analysis Module

This module provides a collection of functions to process, analyze, 
and visualize Instagram direct messages (DMs) from JSON files. Main features include:
- Loading and processing message JSON files into a Pandas DataFrame.
- Decoding messages from their original encoding to UTF-8.
- Generating various visualizations of the messages, such as:
    - A pie chart illustrating the distribution of chats between participants.
    - A heatmap showing message frequency for each hour across months.
    - A time series graph for daily message counts.
- Extracting message content while filtering out system-generated content and actions.
- Providing summaries like the five most common words used in messages.
- Interactively prompting users for a JSON file and shows available analyses and visualizations.
This module depends on several external libraries including pandas, seaborn, and matplotlib. 
Additionally, it relies on the 'main' module for certain operations.

Note: To ensure correct execution, the provided JSON file should adhere to a specific structure,
especially when keys like 'messages' are accessed directly.
"""

import json
from collections import Counter
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import instagram_data_class as ig_data
import main


def create_msg_df(input_path) -> pd.DataFrame:
    """
    Loads JSON from path and creates a dataframe from message section of JSON
    :param input_path: A Path object of a path to a message JSON file
    :return: A dataframe containing information in the message JSON file
    """
    try:
        with open(input_path, encoding='UTF-8') as message_file:
            message_json = json.load(message_file)

        # Enter the actual messages section from JSON data
        messages_dict = message_json['messages']

        # Create DF
        df = pd.DataFrame.from_dict(messages_dict)

        # Convert timestamps from milliseconds
        df['timestamp_ms'] = pd.to_datetime(df['timestamp_ms'], unit='ms')

        return df
    except (AttributeError, TypeError) as error:
        print(f'ERROR: {error}')


def decode_messages(messages: pd.Series) -> pd.Series:
    """
    Decode words from their original encoding to UTF-8.
    :param messages: Series containing the messages to be decoded
    :return: Decoded messages series
    """
    decoded_messages = messages.apply(lambda message: message.encode('latin-1').decode('utf-8'))
    return decoded_messages


def plot_message_distribution_graph(df: pd.DataFrame) -> None:
    """
    Plots a pie chart showing the distribution of chats sent between each participant
    of a direct message conversation
    :param df: A Pandas Dataframe of an Instagram direct message JSON file
    """
    # Filter out dataframe for only messages, timestamps, and sender names
    df = df.loc[:, ['content', 'timestamp_ms', 'sender_name']]

    # Remove all NaN elements, correctly encode messages, & convert timestamps
    df.dropna(inplace=True)
    df['content'] = decode_messages(df['content'])

    # Plot figure
    plt.figure(figsize=(8, 8))
    df["sender_name"].value_counts().plot(kind='pie', autopct='%1.2f%%', shadow=True,
                                          fontsize=15.0, title='Percentage of sent texts in conversation')
    with plt.ion():
        plt.show(block=False)


def plot_message_heatmap(df: pd.DataFrame) -> None:
    """
    Plots a heatmap showing the number of messages sent between each hour of the day
    across all months of a year
    :param df: A Pandas Dataframe of an Instagram direct message JSON file
    """
    time_data = df.copy()

    # drop columns we don't need
    time_data.drop(["share", "reactions", "photos", "audio_files", "videos"], axis=1, inplace=True, errors='ignore')

    # drop rows where timestamp_ms is NaN
    time_data.dropna(subset=['timestamp_ms'], inplace=True)

    # convert timestamp_ms to datetime if it is not already
    if not pd.api.types.is_datetime64_any_dtype(time_data['timestamp_ms']):
        time_data['timestamp_ms'] = pd.to_datetime(time_data['timestamp_ms'], unit='ms')

    # convert timezone
    time_data['timestamp_ms'] = time_data['timestamp_ms'].dt.tz_localize('UTC').dt.tz_convert('US/Pacific')

    time_data['month'] = time_data['timestamp_ms'].dt.month
    time_data['hour'] = time_data['timestamp_ms'].dt.hour

    # count messages using timestamp_ms column
    df_heatmap = time_data.groupby(['hour', 'month'])['timestamp_ms'].count().reset_index()
    df_heat2 = df_heatmap.pivot(index="hour", columns="month", values="timestamp_ms")
    df_heat2 = df_heat2.fillna(0)

    # configure plot settings and plot
    fig, ax = plt.subplots(figsize=(12, 9))
    cmap = sns.cubehelix_palette(as_cmap=True, reverse=True)
    cmap.set_bad(color="gray")
    sns.heatmap(df_heat2, cmap=cmap, mask=df_heat2.isnull(), annot=True, fmt='g')
    plt.title('Number of Texts Per Hour Each Month', size=14)
    with plt.ion():
        plt.show(block=False)

def plot_message_time_series(df: pd.DataFrame) -> None:
    """
    Plots a time series graph of the number of messages sent per day across chat history
    :param df: A Pandas Dataframe of an Instagram direct message JSON file
    """
    time_data = df.copy()

    # Drop NaN rows and columns we don't need
    time_data.dropna(inplace=True)
    time_data.drop(["share", "reactions", "photos", "audio_files", "videos"], 
                   axis=1, inplace=True, errors='ignore')

    # Convert date column to datetime & group data by date
    time_data['date'] = pd.to_datetime(df.timestamp_ms).dt.date
    daily_counts = time_data.groupby('date').size()

    # configure plot settings and plot
    plt.figure(figsize=(12, 6))
    plt.plot(daily_counts.index, daily_counts.values)
    plt.xlabel('Date')
    plt.ylabel('Number of Messages')
    plt.title('Number of Messages Sent Each Day')
    plt.xticks(rotation=45)
    plt.tight_layout()
    with plt.ion():
        plt.show(block=False)


def filter_msg_content(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates new DF skipping action messages, returning the messages while 
    skipping over all NotANumber values

    :param df: A Pandas Dataframe of an Instagram direct message JSON file
    :return: Column of only the messages from the dataframe
    """
    # Creates a copy of the df removing the following phrases within the content column
    content_df = df.loc[
        df['content'].str.contains(
            "sent an attachment.|shared a story.|Liked a message|Reacted|to your message") == False].copy()
    content_df['content'].dropna(inplace=True)  # Skips all NotANumber values
    content_column = content_df['content']  # Returns the content column of the newly copied dataframe
    return content_column


def five_most_common_words(word_column: pd.Series) -> str:
    """
    Prints a dataframe with the 5 most common words and their counts.
    :param word_column: A Pandas Series consisting of words/messages
    """

    # Creates and prints a list of tuples with the five most common words and their counts
    common_word_counter = Counter(" ".join(word_column).split()).most_common(5)
    common_word_df = pd.DataFrame(common_word_counter, columns=['Word', 'Count'])
    common_word_df = common_word_df.to_string(index=False)
    return f'\nYour Five Most Common Words: \n{common_word_df}'


def get_message_df_length(word_column: pd.Series) -> int:
    """
    Get the number of messages sent within a DM conversation.
    :param word_column: A Pandas Series consisting of words/messages
    :return: F-string containing the amount of messages in a conversation excluding action statements
    """
    return word_column.size


def get_first_five_messages(df: pd.DataFrame):
    """
    Gets the first five messages in a DM conversation and shows each sender and the timestamp
    along with their message.
    :param df: A Pandas Dataframe of an Instagram direct message JSON file
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
    reversed_filtered_df_head['timestamp_ms'] = pd.to_datetime(reversed_filtered_df_head['timestamp_ms'], unit='ms')
    reversed_filtered_df_head['sender_name'] = decode_messages(reversed_filtered_df_head['sender_name'])
    
    # Renaming columns to fit new changes
    reversed_filtered_df_head.rename(columns={
        'sender_name': 'sender_name', 'timestamp_ms': 'timestamp', 'content': 'message'}, inplace=True)
    reversed_filtered_df_head = reversed_filtered_df_head.to_string(index=False, justify='left')

    return f'\nYour First Five Messages: \n{reversed_filtered_df_head}\n'


def message_data(instagram_data: ig_data.InstagramData):
    """
    Prompts the user to input a file path to a message JSON file and presents
    corresponding data visualizations
    """
    print('\nWelcome To The Message Data Section!')
    print('------------------------------------')
    print('To return to the main menu please type "return"')


    while True:
        try:
            file_path = input('\nPlease enter the path to a .json file in any file located in /messages/inbox: \n')
            if file_path == 'return':
                print()
                main.main(instagram_data)
                break
            elif file_path.endswith('.json'):
                try:
                    df = create_msg_df(file_path)

                    print(five_most_common_words(filter_msg_content(df)))
                    print(get_first_five_messages(df))
                    print(f'\nNumber Of Messages In The Conversation: '
                          f'\n{get_message_df_length(filter_msg_content(df))}')
                    plot_message_distribution_graph(df)
                    plot_message_heatmap(df)
                    plot_message_time_series(df)

                except (FileNotFoundError, json.JSONDecodeError):
                    print('\nERROR: The given file path does not exist or is not a valid path')
                    print('Please check the inputted directory path')
            else:
                print('\nERROR: Invalid input. Please enter a valid path ending with .json or type "return" to go back to the main menu.')

        except Exception as e:
            print(f'\nAn unexpected error occurred: {e}')
