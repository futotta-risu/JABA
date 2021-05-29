import pandas as pd

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

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
    
    
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        
    def get_sentiment(self, text):
        """
            Analyzes text.

            Parameters:
            text(string): Sentence

            Returns:
            Compound sentiment from NLTK polarity

        """
        polarity = self.sia.polarity_scores(text)
        
        return polarity['compound']
    
    def analyze(self, data, ubication, round = "min"):
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
            data.loc[index, 'sentiment'] = self.get_sentiment(data['Text'].iloc[index])
         
        sentiment_frame = data.groupby('round_time', as_index=False).agg({'sentiment':'mean'})
        
        sentiment_frame.to_csv(ubication + "/sentiment_file.csv", sep=';', index=False)