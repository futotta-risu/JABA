import pandas as pd
from model.Sentiment import Sentiment
from model.Tweet import Tweet
from model.Bitcoin import Bitcoin

def createModelFrame(type):
    model = None
    if type == "Tweet":
        model = Tweet()
    elif type == "Sentiment":
        model = Sentiment()
    elif type == "Bitcoin":
        model = Bitcoin()
    if model == None:
        return pd.DataFrame()

    return model.createModelFrame()
