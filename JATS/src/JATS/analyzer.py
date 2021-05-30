import os

import pandas as pd

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

from .cleaner import *

nltk.download([     
    "names",
    "stopwords",
    "state_union",
    "twitter_samples",
    "movie_reviews",
    "averaged_perceptron_tagger",
    "vader_lexicon",
    "punkt",
])

from textblob import TextBlob

class Analyzer:
    
    bitcoin_dict = {
        'down': -2,
        'up': +2,
        'bounce' : +1,
        'shitcoin': -2,
        'moon': +3,
        'sell': -1.5,
        'selling': -1.5,
        'sold':-1.5,
        'buy':+1.5,
        'buying':+1.5,
        'bought':+1.5,
        'profit': +1,
        'bearish': -3,
        'bullish':+3,
        'dump': -3,
        'pump': +3,
        'fakeout': -3

    }
    
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.sia.lexicon.update(self.bitcoin_dict)
        
    def get_sentiment(self, text, algorithm = "nltk"):
        """
            Analyzes text.

            Parameters:
            text(string): Sentence

            Returns:
            Compound sentiment from NLTK polarity

        """
        sentiment = 0
        if algorithm == "nltk":
            text = total_clean(text)
            sentiment = self.sia.polarity_scores(text)['compound']
        elif algorithm == "textblob":
            sentiment = TextBlob(text).sentiment.polarity
        
        return sentiment
        
        
    def analyze(self, data, ubication, round = "min", algorithm="nltk"):
        """
            Analyzes temporal data and saves it to a file.
            
            Parameters:
            data (Pandas DataFrame): DataFrame with at least the following columns
                - "DateTime": Time of the data
                - "Text": Sentence
            ubication (String): Path to the folder for the new file
            round (String): Where to approximate the "DateTime" column
        """
        
        data['round_time'] = ""
        data["round_time"] = pd.to_datetime(data["round_time"])
        
        data['round_time'] = data['Datetime'].round(round)
        
        for index, row in data.iterrows():
            data.loc[index, 'sentiment'] = self.get_sentiment(data['Text'].iloc[index], algorithm)
        
        # We remove the zeros because they dont give any information. 
        # Neutrality is normaly due to inconsisten sentiment analisys
        data = data[data["sentiment"] != 0] 
        
        sentiment_frame = data.groupby('round_time', as_index=False).agg({'sentiment':'mean'})
        sentiment_frame.to_csv(os.path.join(ubication, "sentiment_file_" + algorithm + ".csv"), sep=';', index=False)