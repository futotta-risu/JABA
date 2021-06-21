import pandas as pd

from .Tweet import Tweet


class Sentiment:
    def __init__(self):
        self.__tweet = Tweet()

        self.column_names = ["sentiment"] + self.__tweet.column_names

    def setModelTypes(self, df):
        df["sentiment"] = pd.to_numeric(df["sentiment"])

        df = self.__tweet.setModelTypes(df)

        return df

    def createModelFrame(self):
        return self.setModelTypes(pd.DataFrame(columns=self.column_names))
