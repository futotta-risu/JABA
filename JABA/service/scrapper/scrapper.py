import datetime
from datetime import timedelta

import json

from pathlib import Path

import os.path
import os

import snscrape.modules.twitter as snstwitter

import pandas as pd

from .cleaner import clean_tweet

# Name of the columns for the dataframes
column_names = [
    'Datetime',
    'Tweet Id',
    'Text', 
    'NumReplies',
    'NumRetweets',
    'NumLikes', 
    'IDOriginalRetweeted', 
    'Username',
    'isVerified'
]


# Condition query for data scrapping
condition_query = '{query} since:{since} until:{until} lang:{lang}'

DIRECTORY = 'data/tweets/{day}'
FILE_NAME = DIRECTORY + '/tweet_list.csv'
SPAM_FILE_NAME = DIRECTORY + '/spam_tweet_list.csv'


def create_data_log(directory, tweet_limit):
    data = {'tweet_limit':tweet_limit}
    with open(directory + '/log.json', 'w') as f:
        json.dump(data, f)

def format_conditional_query(query, date_from, date_until, lang):
    """
        Formats the conditional query
    """
    return condition_query.format(query = query, since=str(date_from), until=str(date_until), lang=lang)

def get_tweet_data(tweet):
    """
        Cleans and separates needed data from Tweet class to list.
        
        Parameters:
        tweet (Tweet [snstwitter])
        
        Returns:
        List of Date, ID, Tweet Text, Reply Count, Retweet Count, Like Count, Parent Tweet ID, Username, IsVerified
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
        tweet.user.verified
    ]


def get_file_names(date):
    
    directory = DIRECTORY.format(day = str(date))
    file_name = FILE_NAME.format(day =str(date))
    spam_file_name = SPAM_FILE_NAME.format(day = str(date))
    
    return directory, file_name, spam_file_name
    
def file_exists(date_from):
    _ , file_name, _ = get_file_names(date_from)
    
    return os.path.isfile(file_name)
        
    
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
    
    data_dup = data[data["Text"].duplicated()]['Text'].value_counts().rename_axis('unique_texts').reset_index(name='counts')
    data.drop_duplicates(subset ="Text", keep = False, inplace=True)
    
    return data, data_dup
    
    
def save_file(tweet_list, date_from, max_tweets):
    """
        Saves the file if it doesn't exist
    """
    directory, file_name, spam_file_name = get_file_names(date_from)
    
    tweet_df = pd.DataFrame(tweet_list, columns=column_names)
    tweet_df = tweet_df[ (tweet_df['Text'].notna()) & tweet_df['Text']]
    
    tweet_df, tweet_df_dup = filter_spam(tweet_df)
    
    Path(directory).mkdir(parents=True, exist_ok=True)

    tweet_df.to_csv(file_name, sep=';', index=False)
    tweet_df_dup.to_csv(spam_file_name, sep=';', index=False)
    
    create_data_log(directory, max_tweets)

def get_tweet_from_file(date):
    _, file_name, _ = get_file_names(date)
    tweet_df = pd.read_csv(file_name, sep=';')
    tweet_df["Datetime"] = pd.to_datetime(tweet_df["Datetime"])
    return tweet_df
    
def get_tweets(query, date_from, date_until, tweet_limit = -1, lang="en", verbose = False):
    """
        Function to scrap tweet between dates and save them
        
        Parameters:
        date_from (datetime.date): Fecha de comienzo del scrapping
        date_until (datetime.date): Fecha hasta la que se realiza el scrapping. Fecha no incluida.
        tweet_limit (int): Limite de tweets al dia. -1 si no se quiere limite
    """
    while(date_from != date_until):
        tweet_list = []
        if file_exists(date_from):
            date_from += timedelta(days=1)
            continue
            
        if verbose:
            print("Day " + str(date_from))

        format_string = format_conditional_query(query, date_from, date_from + timedelta(days=1), lang)
        
        for i, tweet in enumerate(snstwitter.TwitterSearchScraper(format_string).get_items()):
            if i >= tweet_limit and tweet_limit != -1:
                break
                
            if verbose and i%2500==0:
                print(str(date_from),": ", i , " / " , tweet_limit)
            
            tweet_list += [get_tweet_data(tweet)]
        
        save_file(tweet_list, date_from, tweet_limit)
        
        date_from += timedelta(days=1)


