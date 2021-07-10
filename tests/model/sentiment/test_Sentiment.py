import pytest

import pandas as pd

from model.sentiment.Sentiment import Sentiment

def test_create_sentiment():
    sentiment = Sentiment()
    
    assert sentiment != None

    
def test_setModelType():
    sentiment = Sentiment()
    
    df = pd.DataFrame(columns=sentiment.column_names)
    
    try:
        sentiment.setModelTypes(df)
    except Exception:
        pytest.fail("Pandas error")