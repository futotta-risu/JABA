import pandas as pd
from model.Sentiment import Sentiment
from model.Tweet import Tweet


def createModelFrame(type):
    model = None
    if type == "Tweet":
        model = Tweet()
    elif type == "Sentiment":
        model = Sentiment()

    if model == None:
        return pd.DataFrame()

    return model.createModelFrame()
