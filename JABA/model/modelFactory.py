from model.Tweet import Tweet

import pandas as pd

def createModelFrame(type):
    if type == "Tweet":
        tweet = Tweet()
        return tweet.createModelFrame()
    
    return pd.DataFrame()