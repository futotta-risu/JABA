import datetime

from datetime import timedelta

import pandas as pd

import snscrape.modules.twitter as snstwitter

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

    def scrap(self, date_from, date_until, limit=-1, lang="en", verbose=False):
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

    def scrap(self, date_from, date_until, limit=-1, lang="en", verbose=False):
        """
        Function to scrap tweet between dates and save them

        Parameters:
        date_from (datetime.date): Fecha de comienzo del scrapping
        date_until (datetime.date): Fecha hasta la que se realiza el scrapping. Fecha no incluida.
        tweet_limit (int): Limite de tweets al dia. -1 si no se quiere limite
        """
        
        logger.info(f"Scraping data from Twitter from {date_from} with limit {limit}")
        
        while date_from != date_until:
            tweet_list = []
            if self.fileManager.file_exists(date_from):
                date_from += timedelta(days=1)
                continue

            if verbose:
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                print(f"{current_time}: Day {date_from}")

            format_string = self.format_conditional_query(
                date_from, date_from + timedelta(days=1), lang)

            for i, tweet in enumerate(
                    snstwitter.TwitterSearchScraper(
                        format_string).get_items()):
                if limit != -1:
                    if i >= limit:
                        break

                if verbose and i % 2500 == 0:
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    print(current_time, ": ", str(date_from), "(", i, " / ", limit, ")")

                tweet_list += [self.get_tweet_data(tweet)]

            tweets, spam_tweets = self.filter_spam(tweet_list)

            self.fileManager.save_file([tweets, spam_tweets], {'date': date_from, 'status': limit})

            date_from += timedelta(days=1)

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

    def format_conditional_query(self, date_from, date_until, lang):
        """
        Formats the conditional query
        """

        return self.query.format(since=str(date_from),
                                 until=str(date_until),
                                 lang=lang)
