import pandas as pd

from model.ScrapModel import ScrapModel

from model.social.Tweet import Tweet
from model.bitcoin.Bitcoin import Bitcoin
from model.sentiment.Sentiment import Sentiment

# TODO Change this with real factory
def createModelFrame(dtype):
    
    models = [
        model_class() for model_class in ScrapModel.__subclasses__()
        if model_class.name == dtype
    ]
    
    if not models:
        raise NotImplementedError()

    return models[0].createModelFrame()
    
