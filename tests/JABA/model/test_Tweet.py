import pytest

import pandas as pd

from model.Tweet import Tweet

def test_create_tweet():
    tweet = Tweet()
    
    assert tweet != null
    
def test_name_tweet():
    tweet = Tweet()
    
    assert tweet.name == 'Tweet'
    
def test_setModelType():
    tweet = Tweet()
    
    df = pd.DataFrame(columns=tweet.column_names)
    
    try:
        tweet(df)
    except MyError:
        pytest.fail("Pandas error")