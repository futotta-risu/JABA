import os
from pathlib import Path

import nltk
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

from .cleaner import *
from .file_manager import FileManagerInterface
from .scrapper import ScrapperFileManager

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


class AnalyzerFileManager(FileManagerInterface):
    def __init__(self):
        super().__init__()

        self.FILE_NAME = os.path.join(self.DIRECTORY,
                                      "tweet_sentiment_{algorithm}.csv")

    def get_file_name(self, args: dict):
        return self.FILE_NAME.format(day=args["date"],
                                     algorithm=args["algorithm"])

    def open_file(self, args: dict):
        """
        Returns the dataframe from the scrapper class
        """
        scrappeFM = ScrapperFileManager()
        tweet_df = scrappeFM.open_file(args)

        file_name = self.get_file_name(args)
        data = pd.read_csv(file_name, sep=";")
        data["sentiment"] = pd.to_numeric(data["sentiment"])

        data = tweet_df.join(data)

        return data

    def save_file(self, data, args: dict):
        """
        Saves the file if it doesn't exist
        """
        file_name = self.get_file_name(args)

        Path(self.DIRECTORY).mkdir(parents=True, exist_ok=True)
        data.to_csv(file_name, sep=";", index=False)


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
        "low": -3,
        "hold": +2,
        "hodl": +3,
        "liquidation": -5,
        "drop": -2,
        "dropped": -3,
        "carbon": -2,
        "inflation": +2,
        "rally": +3,
    }

    def __init__(self):
        self.file_manager = AnalyzerFileManager()
        self.sia = SentimentIntensityAnalyzer()
        self.sia.lexicon.update(self.bitcoin_dict)

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

    def analyze(self,
                date, 
                data_file_manager,
                round="min",
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

            data.loc[index, "sentiment"] = self.get_sentiment(
                data["Text"].iloc[index], algorithm)

        self.file_manager.save_file(data["sentiment"], args = args)