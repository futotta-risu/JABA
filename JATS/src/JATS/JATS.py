import datetime
from datetime import timedelta

from pathlib import Path

import os.path

import snscrape.modules.twitter as snstwitter

import pandas as pd

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
FILE_NAME = DIRECTORY + '/tweet_list{status}.csv'
FILE_NAME_FINAL = DIRECTORY + '/tweet_list.csv'


def format_conditional_query(query, date_from, date_until, lang):
    """
        Formats the conditional query
    """
    return condition_query.format(query = query, since=str(date_from), until=str(date_until), lang=lang)

def get_tweet_data(tweet):
    return [
                tweet.date, tweet.id, tweet.content,
                tweet.replyCount, tweet.retweetCount,
                tweet.likeCount, tweet.retweetedTweet,
                tweet.user.username, tweet.user.verified
            ]


def get_file_names(directory, file_name, date_from, date_until, finished = False):
    
    directory.format(since=str(date_from), until=str(date_until))
    file_name.format(since=str(date_from), until=str(date_until))
    
    if "status" in file_name:
        file_name.format(status = "" if finished else "_unfinished")
    
    return directory, file_name
    
def file_exists(date_from, date_until):
    _ , file_name = get_file_names(DIRECTORY, FILE_NAME_FINAL, date_from, date_until)
    
    return os.path.isfile(file_name)
        
    

def save_file(tweet_list, date_from, date_until, max_tweets):
    """
        Saves the file if it doesn't exist
    """
    directory, file_name = get_file_names(DIRECTORY, FILE_NAME_FINAL, date_from, date_until, max_tweets == -1)
    
    tweet_df = pd.DataFrame(tweet_list, columns=columnNames)
    
    Path(directory).mkdir(parents=True, exist_ok=True)
    tweet_df.to_csv(file_name, sep=',', index=False)


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