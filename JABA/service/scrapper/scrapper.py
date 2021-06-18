import datetime
import json
import os.path
from datetime import timedelta
from pathlib import Path

import pandas as pd
import snscrape.modules.twitter as snstwitter

from .cleaner import clean_tweet
from .file_manager import *

# Name of the columns for the dataframes
column_names = [
    "Datetime",
    "Tweet Id",
    "Text",
    "NumReplies",
    "NumRetweets",
    "NumLikes",
    "IDOriginalRetweeted",
    "Username",
    "isVerified",
]


class ScrapperFileManager(FileManagerInterface):
    def __init__(self):
        self.FILE_NAME = self.DIRECTORY + "/tweet_list.csv"
        self.SPAM_FILE_NAME = self.DIRECTORY + "/spam_tweet_list.csv"

    def get_file_name(self, args: dict):
        """
        Returns the file names of the scrapper class

        Returns:
        FILE_NAME, SPAM_FILE_NAME
        """

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

        Path(self.DIRECTORY).mkdir(parents=True, exist_ok=True)

        for index, file_name in enumerate(file_names):
            data[index].to_csv(file_name, sep=";", index=False)

        self.create_data_log(args["status"])

    def create_data_log(self, status):
        with open(self.DIRECTORY + "/log.json", "w") as f:
            json.dump(status, f)


class IScrapper:

    # Namespace for the scrapper in order to save files
    namespace = "IScrapper"

    # Query to be scrapped from the page
    query = "default_query"

    # Conditions of the query
    condition_query = "default_conditional_query"

    def scrap(self, date_from, date_until, limit=-1, lang="en", verbose=False):
        pass


class TwitterScrapper(IScrapper):
    namespace = "twitter"
    query = '"BTC" OR "bitcoin" since:{since} until:{until} lang:{lang}'

    def __init__(self):
        self.fileManager = ScrapperFileManager()

    def scrap(self, date_from, date_until, limit=-1, lang="en", verbose=False):
        """
        Function to scrap tweet between dates and save them

        Parameters:
        date_from (datetime.date): Fecha de comienzo del scrapping
        date_until (datetime.date): Fecha hasta la que se realiza el scrapping. Fecha no incluida.
        tweet_limit (int): Limite de tweets al dia. -1 si no se quiere limite
        """
        while date_from != date_until:
            tweet_list = []
            if self.fileManager.file_exists(date_from):
                date_from += timedelta(days=1)
                continue

            if verbose:
                print("Day " + str(date_from))

            format_string = self.format_conditional_query(
                date_from, date_from + timedelta(days=1), lang)

            for i, tweet in enumerate(
                    snstwitter.TwitterSearchScraper(
                        format_string).get_items()):
                if limit != -1:
                    if i >= limit:
                        break

                if verbose and i % 2500 == 0:
                    print(str(date_from), ": ", i, " / ", tweet_limit)

                tweet_list += [self.get_tweet_data(tweet)]

            tweets, spam_tweets = self.filter_spam(tweet_list)

            self.fileManager.save_file([tweets, spam_tweets], date_from,
                                       tweet_limit)

            date_from += timedelta(days=1)

    def filter_spam(data):
        """
        Filters the spam from the data.

        The data is filtered from the Text column.

        Parameters:
        data (Pandas Dataframe): Dataframe from tweets. See column_names.

        Returns:
        Filtered data (Pandas Dataframe) Data without the spam
        Spam (Pandas Dataframe) Spam filtered from the data
        """

        data = pd.DataFrame(tweet_list, columns=column_names)
        data = data[(data["Text"].notna()) & data["Text"]]

        data_spam = (data[data["Text"].duplicated()]["Text"].value_counts().
                     rename_axis("unique_texts").reset_index(name="counts"))

        data.drop_duplicates(subset="Text", keep=False, inplace=True)

        return data, data_spam

    def get_tweet_data(self, tweet):
        """
        Cleans and separates needed data from Tweet class to list.

        Parameters:
        tweet (Tweet [snstwitter])

        Returns:
        List of Date, ID, Tweet Text, Reply Count,
            Retweet Count, Like Count, Parent Tweet ID, Username, IsVerified
        """
        return [
            tweet.date,
            tweet.id,
            clean_tweet(tweet.content),
            tweet.replyCount,
            tweet.retweetCount,
            tweet.likeCount,
            tweet.retweetedTweet,
            tweet.user.username,
            tweet.user.verified,
        ]

    def format_conditional_query(date_from, date_until, lang):
        """
        Formats the conditional query
        """

        return self.query.format(since=str(date_from),
                                 until=str(date_until),
                                 lang=lang)
