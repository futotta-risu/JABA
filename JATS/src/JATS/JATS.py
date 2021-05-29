import datetime
from datetime import timedelta

import json

from pathlib import Path

import os.path

import snscrape.modules.twitter as snstwitter

import pandas as pd

from .cleaner import clean_tweet

# Name of the columns for the dataframes
columnNames = [
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

DIRECTORY = 'data/tweets/{since}/{until}'
FILE_NAME = DIRECTORY + '/tweet_list.csv'



def create_data_log(directory, tweet_limit):
    data = {'tweet_limit':tweet_limit}
    with open(directory+'/data.json', 'w') as f:
        json.dump(data, f)

def format_conditional_query(query, date_from, date_until, lang):
    """
        Formats the conditional query
    """
    return condition_query.format(query = query, since=str(date_from), until=str(date_until), lang=lang)

def get_tweet_data(tweet):
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


def get_file_names(date_from, date_until, finished = False):
    
    directory = DIRECTORY.format(since=str(date_from), until=str(date_until))
    file_name = FILE_NAME.format(since=str(date_from), until=str(date_until))
    
    return directory, file_name
    
def file_exists(date_from, date_until):
    _ , file_name = get_file_names(date_from, date_until)
    
    return os.path.isfile(file_name)
        
    

def save_file(tweet_list, date_from, date_until, max_tweets):
    """
        Saves the file if it doesn't exist
    """
    directory, file_name = get_file_names(date_from, date_until, max_tweets == -1)
    
    tweet_df = pd.DataFrame(tweet_list, columns=columnNames)
    
    Path(directory).mkdir(parents=True, exist_ok=True)
    tweet_df.to_csv(file_name, sep=';', index=False)
    create_data_log(directory, max_tweets)

def get_tweets(query, date_from, date_until, tweet_limit = -1, lang="en", verbose = False):
    """
        Function to scrap tweet between dates
        
        Parameters:
        date_from (datetime.date): Fecha de comienzo del scrapping
        date_until (datetime.date): Fecha hasta la que se realiza el scrapping. Fecha no incluida.
        tweet_limit (int): Limite de tweets al dia. -1 si no se quiere limite
        
        Returns:
        Lista de Valores del tweet
    """
    tweet_list = []
    while(date_from != date_until):
        if file_exists(date_from, date_until):
            date_from += timedelta(days=1)
            continue
            
        if verbose:
            print("Day " + str(date_from))

        format_string = format_conditional_query(query, date_from, date_from + timedelta(days=1), lang)
        
        for i, tweet in enumerate(snstwitter.TwitterSearchScraper(format_string).get_items()):
            if i >= tweet_limit and tweet_limit != -1:
                break
                
            if verbose and i%2500==0:
                print(i , " / " , tweet_limit)
            
            tweet_list += [get_tweet_data(tweet)]
        
        save_file(tweet_list, date_from, date_until, tweet_limit)
        
        date_from += timedelta(days=1)

    return tweet_list