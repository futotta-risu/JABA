import os
from pathlib import Path

import pandas as pd

from model.FileManager import FileManagerInterface
from model.social.TweetFileManager import TweetFileManager


class SentimentFileManager(FileManagerInterface):
    '''
        Handles the file system for the analyzer methods.
    '''

    def __init__(self):
        super().__init__()

        self.FILE_NAME = os.path.join(self.DIRECTORY,
                                      "tweet_sentiment_{algorithm}.csv")

    def get_file_name(self, args: dict):
        return self.FILE_NAME.format(day=args["date"],
                                     algorithm=args["algorithm"])

    def open_file(self, args: dict):
        """
        Returns the dataframe from the scrapper class
        """

        tweet_file_manager = TweetFileManager()
        tweet_df = tweet_file_manager.open_file(args)

        file_name = self.get_file_name(args)
        data = pd.read_csv(file_name, sep=";")
        data["sentiment"] = pd.to_numeric(data["sentiment"])
        data = tweet_df.join(data)

        return data

    def save_file(self, data, args: dict):
        """
        Saves the file if it doesn't exist
        """
        file_name = self.get_file_name(args)

        Path(self.DIRECTORY).mkdir(parents=True, exist_ok=True)
        data.to_csv(file_name, sep=";", index=False)
