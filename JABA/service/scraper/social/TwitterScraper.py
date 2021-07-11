import datetime

from datetime import timedelta

import pandas as pd

from snscrape.modules.twitter import TwitterSearchScraper

from service.scraper.cleaner import clean_tweet
from model.social.TweetFileManager import TweetFileManager
from model.social.Tweet import Tweet

from loguru import logger


class IScrapper:
    # Namespace for the scrapper in order to save files
    namespace = "IScrapper"

    # Query to be scrapped from the page
    query = "default_query"

    # Conditions of the query
    condition_query = "default_conditional_query"

    def scrap(self, date_from, limit=-1, lang="en"):
        pass


# TODO Change the spelling
class TwitterScraper(IScrapper):
    '''
        Twitter scraper class which extracts the data of a certain query.
    '''

    namespace = "twitter"
    query = '"BTC" OR "bitcoin" since:{since} until:{until} lang:{lang}'

    def __init__(self):
        self.fileManager = TweetFileManager()

    def scrap(self, date_from, limit=-1, lang="en"):
        """
        Function to scrap tweet between dates and save them

        Parameters:
            date_from (datetime.date): Fecha de comienzo del scrapping
            tweet_limit (int): Límite de tweets al dia o -1 para sin límite.
        """

        logger.info(f"Scraping data from Twitter from {date_from} with limit {limit}")

        tweet_list = []
        if self.fileManager.file_exists(date_from):
            return

        format_string = self.format_query(date_from, lang)

        for i, tweet in enumerate(TwitterSearchScraper(format_string).get_items()):

            if limit != -1 and i >= limit:
                break

            tweet_list += [self.get_tweet_data(tweet)]

        tweets, spam_tweets = self.filter_spam(tweet_list)

        self.fileManager.save_file([tweets, spam_tweets], {'date': date_from, 'status': limit})

    def filter_spam(self, data):
        """
        Filters the spam from the data.

        The data is filtered from the Text column.

        Parameters:
        data (Pandas Dataframe): Dataframe from tweets. See column_names.

        Returns:
        Filtered data (Pandas Dataframe) Data without the spam
        Spam (Pandas Dataframe) Spam filtered from the data
        """

        tweet = Tweet()
        data = pd.DataFrame(data, columns=tweet.column_names)
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

    def format_query(self, date_from, lang):
        ''' Formats the conditional query '''

        date_until = date_from + timedelta(days=1)

        return self.query.format(since=str(date_from),
                                 until=str(date_until),
                                 lang=lang)
