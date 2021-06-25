import pandas as pd

from model.ScrapModel import ScrapModel

from model.Tweet import Tweet
from model.Bitcoin import Bitcoin
from model.Sentiment import Sentiment

def createModelFrame(dtype):
    
    models = [
        model_class() for model_class in ScrapModel.__subclasses__()
        if model_class.name == dtype
    ]
    
    if not models:
        raise NotImplementedError()

    return models[0].createModelFrame()
    
