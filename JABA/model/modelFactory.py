from model.Tweet import Tweet
from model.Sentiment import Sentiment

import pandas as pd


def createModelFrame(type):
    model = None
    if type == "Tweet":
        model = Tweet()
    elif type == "Sentiment":
        model = Sentiment()

    if model == None:
        return pd.DataFrame()

    return model.createModelFrame()
