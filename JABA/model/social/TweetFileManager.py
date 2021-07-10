import os
from pathlib import Path

import pandas as pd

import json

from model.FileManager import FileManagerInterface


class TweetFileManager(FileManagerInterface):
    def __init__(self):
        self.FILE_NAME = self.DIRECTORY + "/tweet_list.csv"
        self.SPAM_FILE_NAME = self.DIRECTORY + "/spam_tweet_list.csv"

    def get_file_name(self, args: dict):
        """
        Returns the file names of the scrapper class

        Returns:
        FILE_NAME, SPAM_FILE_NAME
        """
        if args['date'] is None:
            raise TypeError('Date should not be None')
            
        file_name = self.FILE_NAME.format(day=args["date"])
        spam_file_name = self.SPAM_FILE_NAME.format(day=args["date"])

        return file_name, spam_file_name

    def open_file(self, args: dict):
        """
        Returns the dataframe from the scrapper class
        """
        file_name, _ = self.get_file_name(args)
        data = pd.read_csv(file_name, sep=";")
        data["Datetime"] = pd.to_datetime(data["Datetime"])

        return data

    def save_file(self, data, args: dict):
        """
        Saves the file if it doesn't exist
        """
        file_names = self.get_file_name(args)
        self.DIRECTORY = self.DIRECTORY.format(day=args["date"])
        Path(self.DIRECTORY).mkdir(parents=True, exist_ok=True)

        for index, file_name in enumerate(file_names):
            data[index].to_csv(file_name, sep=";", index=False)

        self.create_data_log(args["status"])

    def file_exists(self, date):
        file_name, _ = self.get_file_name({'date': date})
        return os.path.isfile(file_name)

    def create_data_log(self, status):
        with open(self.DIRECTORY + "/log.json", "w") as f:
            json.dump(status, f)
