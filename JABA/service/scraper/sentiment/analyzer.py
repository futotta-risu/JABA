import os
from pathlib import Path

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

import pandas as pd

from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob

from service.scraper.cleaner import *
from model.sentiment.SentimentFileManager import SentimentFileManager


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


class Analyzer:

    bitcoin_dict = {
        "down": -2,
        "up": +2,
        "bounce": +3,
        "shitcoin": -3,
        "moon": +3,
        "sell": -3.5,
        "selling": -3.5,
        "sold": -3.5,
        "buy": +3.5,
        "buying": +3.5,
        "bought": +3.5,
        "profit": +5,
        "bearish": -5,
        "bullish": +5,
        "dump": -5,
        "pump": +5,
        "dip": -3,
        "dipping": -3,
        "fakeout": -5,
        "long": +3,
        "short": -3,
        "high": +3,
        'higher': +2,
        "low": -3,
        "lower": -2,
        "hold": +2,
        "hodl": +3,
        "liquidation": -5,
        "drop": -2,
        "dropped": -3,
        "carbon": -2,
        "inflation": +2,
        "rally": +3,
        'fees': -3,
        'invest': +1,
        'phising': -3,
        'scam': -5,
        'shit': -3,
        'scamed': -3,
        'scamming': -3,
        'breakout': +3,
        'fake': -3,
        'away': -3,
        'garbage': -3,
        'pull': -2,
        'push': +2,
        'free': -1, # Mostly spam
        'ransomware': -3,
        'unstoppable': +2,
        'gamble': -10,
        'gambling': -10,
        'strong': +5,
        'weak': -5,
        'run': +2,
        
    }

    def __init__(self):
        self.file_manager = SentimentFileManager()
        self.sia = SentimentIntensityAnalyzer()
        self.sia.lexicon.update(self.bitcoin_dict)

    @staticmethod
    def get_algorithms():
        return ['nltk', 'textblob']
        
    def get_sentiment(self, text, algorithm="nltk"):
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
            sentiment = self.sia.polarity_scores(text)["compound"]
        elif algorithm == "textblob":
            sentiment = TextBlob(text).sentiment.polarity

        return sentiment
    
    # TODO Delete the round parameter
    def analyze(self,
                date, 
                data_file_manager,
                algorithm="nltk",
                verbose=False):
        """
        Analyzes temporal data and saves it to a file.

        Parameters:
        data (Pandas DataFrame): DataFrame with at least the following columns
            - "DateTime": Time of the data
            - "Text": Sentence
        ubication (String): Path to the folder for the new file
        round (String): Where to approximate the "DateTime" column
        """
        args = {'date': date, 'algorithm': algorithm }
        data = data_file_manager.open_file(args)
        
        for index, row in data.iterrows():
            if verbose:
                if index % 1000 == 0:
                    print(f"Actual analyzed index: {index}")
            
            sentiment = self.get_sentiment(row["Text"], algorithm)
            data.loc[index, "sentiment"] = sentiment

        self.file_manager.save_file(data["sentiment"], args = args)
    
    
    def get_cosine_similarity(self, cleaned_texts):
        """
        Calculates the Cosine Similarity of Strings given a list of them.
        Texts must be cleaned before the analisis
        """

        vectorizer = CountVectorizer().fit_transform(cleaned_texts)
        vectors = vectorizer.toarray()

        return cosine_similarity(vectors)

    def analyze_similarity(self, tweet_df):
        """
        Insert a new column with the clustered group number into the given dataframe of tweets.
        The column is called 'Prediction'
        """

        tweet_df = tweet_df.dropna(axis=0, subset=["Text"])
        csim = self.get_cosine_similarity(tweet_df["Text"])
        clustering = DBSCAN(eps=1.04, min_samples=5).fit(csim)
        unique_elements, counts_elements = np.unique(clustering.labels_,
                                                     return_counts=True)
        tweet_df["Prediction"] = clustering.labels_.tolist()

        return tweet_df

    def remove_similar_tweets(self, tweet_df):
        """
        Remove from the received Dataframe the tweet_groups where the username is similar.
        """

        for i in range(0, tweet_df["Prediction"].value_counts().size - 1):
            tweet_group = tweet_df.loc[tweet_df["Prediction"] == i]
            csim = self.get_cosine_similarity(tweet_group["Username"])
            lower = []
            for j in range(0, len(csim)):
                for i in range(0, len(csim)):
                    if j > i:
                        lower.append(csim[j][i])
                    else:
                        pass
            lowerSum = sum(lower)

            # El parametro 0.1 hace referencia a la cantidad de repeticiones en el
            # grupo de tweets, siendo 1 el maximo numero de repeticiones
            if lowerSum / sum(range(len(csim))) > 0.1:
                tweet_df.drop(tweet_group.index, inplace=True)

        return tweet_df