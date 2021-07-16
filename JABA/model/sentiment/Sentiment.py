import pandas as pd

from model.ScrapModel import ScrapModel
from model.social.Tweet import Tweet


class Sentiment(ScrapModel):

    name = "Sentiment"

    def __init__(self):
        self.__tweet = Tweet()

        self.column_names = ["sentiment"] + self.__tweet.column_names

    def setModelTypes(self, df):
        df["sentiment"] = pd.to_numeric(df["sentiment"])

        df = self.__tweet.setModelTypes(df)

        return df

    def createModelFrame(self):
        return self.setModelTypes(pd.DataFrame(columns=self.column_names))
