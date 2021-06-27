import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
import time
import datetime
import re
import os
from sklearn.model_selection import train_test_split


def drop_unused_t_columns(dataframe):
    unused_columns = ['Text', 'Tweet Id', 'NumReplies', 'NumRetweets', 'IDOriginalRetweeted', 'isVerified'  ]
    return dataframe.drop(unused_columns,  axis=1)

def prepare_t_data(dataframe):
    dataframe["Datetime"] = pd.to_datetime(dataframe["Datetime"])
    dataframe['sentiment_v'] = ( 1 + np.log2(1 + dataframe['NumLikes']) ) * dataframe['sentiment'] 
    dataframe["round_datetime"] = dataframe["Datetime"].dt.floor("30T")
    
    dataframe["date"] = dataframe["Datetime"].dt.date
    dataframe = dataframe.set_index('date')
    
    dataframe = dataframe.groupby(['round_datetime', 'Username']).agg({'sentiment_v' : 'sum' , 'Datetime':'count'})

    dataframe['sentiment_v2'] = np.log2(1+dataframe['Datetime']) / dataframe['Datetime'] * dataframe['sentiment_v']
    return dataframe.groupby('round_datetime').sum()

def get_t_data(date_init, date_limit, t_path, t_file, s_file):
    frames = []
    date_from = datetime.datetime.strptime(date_init, '%Y-%m-%d').date()
    date_until = datetime.datetime.strptime(date_limit, '%Y-%m-%d').date()
    
    if date_from >= date_until:
        return pd.DataFrame()
    
    while date_from < date_until:
        
        folder = os.path.join(t_path, str(date_from))
        # TODO Check if file exists
        if date_from.day == 1 and date_from.month == 1:
            print(f"Current Date {str(date_from)}")

        tweet_file = os.path.join(folder, t_file)
        sentiment_file = os.path.join(folder, s_file)

        tweet_df = pd.read_csv(tweet_file, sep=";")
        tweet_df = drop_unused_t_columns(tweet_df)

        sent_df = pd.read_csv(sentiment_file, sep=";")

        tweet_df = prepare_t_data(tweet_df.join(sent_df))
        
        frames += [tweet_df]
        
        date_from = date_from + timedelta(days=1)
    
    return pd.concat(frames, ignore_index=False)


def get_twitter_data(date_init, date_limit):
    t_path = "JABA/data/tweets"
    t_file = "tweet_list.csv"
    s_file = "tweet_sentiment_nltk.csv"
    return get_t_data(date_init, date_limit, t_path, t_file, s_file)
    

def get_bitcoin_data(date_init, date_limit):
    b_path = "JABA/data/bitcoin"
    b_file = "bitcoin.csv"

    frames = []
    date_from = datetime.datetime.strptime(date_init, '%Y-%m-%d').date()
    date_until = datetime.datetime.strptime(date_limit, '%Y-%m-%d').date()

    while date_from < date_until:

        folder = os.path.join(b_path, str(date_from))
        btc_file = os.path.join(folder, b_file)
        # TODO Check if file exists
        if date_from.day == 1 and date_from.month == 1:
            print(f"Current Date {str(date_from)}")

        b_df = pd.read_csv(btc_file, sep=";")
        frames += [b_df]

        date_from = date_from + timedelta(days=1)

    btc_df = pd.concat(frames, ignore_index=False)
    print("Extraction Completed!")
    
    # Pasar los formatos a los tipos correspondientes
    btc_df['round_datetime'] = pd.to_datetime(btc_df['round_datetime'])
    btc_df['timestamp'] = pd.to_datetime(btc_df['timestamp'])

    # Pasar las fechas a index para filtrar datos entre fechas indicadas
    btc_df = btc_df.set_index('round_datetime')

    # Filtrar entre fechas
    btc_df = btc_df[date_init:date_limit]

    # Aproximar a periodos de 30 minutos
    btc_df['timestamp_round'] = btc_df['timestamp'].dt.floor('30T')

    # Sustituir los 0's por el último valos no-zero
    btc_df['Close'] = btc_df['Close'].replace(to_replace=0, method='ffill')

    # Agrupar y hacer la media
    btc_df = btc_df.groupby("timestamp_round").mean()
    return btc_df
    
    
def get_complete_df(date_init, date_limit):
    twitter_df = get_twitter_data(date_init, date_limit)
    btc_df = get_bitcoin_data(date_init, date_limit)
    
    btc_df.index = btc_df.index.tz_localize(None)
    twitter_df.index = twitter_df.index.tz_localize(None)
    
    complete_df = pd.merge(twitter_df,btc_df, how='inner', left_index=True, right_index=True)
    return complete_df

def train_test_splitter(X, Y, test_size):
    X_train, X_test, y_train, y_test = train_test_split(X, 
                                                        Y, 
                                                        test_size = 0.2, 
                                                        random_state = 0)

    print("Training set has {} samples.".format(X_train.shape[0]))
    print("Testing set has {} samples.".format(X_test.shape[0]))
    
    return X_train, X_test, y_train, y_test

