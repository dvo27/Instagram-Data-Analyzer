import json
from collections import Counter
import pandas as pd
from pathlib import Path


# /Users/danielvo/Downloads/ovleinad_20230412/messages/inbox/jessicalin_827275248663098/message_1.json

class Instagram_Data:
    def __init__(self):
        pass


def message_data():
    try:
        with open(Path(input('Please input path to message data file: '))) as message_path:
            # Loads JSON from path and creates a dataframe from message section of JSON
            message_json = json.load(message_path)
            messages_dict = message_json['messages']
            df = pd.DataFrame.from_dict(messages_dict)

            # Skips action messages
            content_df = df.loc[df['content'].str.contains("sent an attachment.|shared a story.|Liked a message") == False].copy()
            content_column = content_df['content']  # Returns the content column of the newly copied dataframe
            content_df.dropna(inplace=True)  # Skips all NotANumber values

            # Creates list of tuples with five most common words + counts and returns
            five_most_common_words = Counter(" ".join(content_column).split()).most_common(5)
            print(five_most_common_words)
    except FileNotFoundError:
        print('ERROR: The given directory does not exist or is not a valid path')


message_data()
