import pytest

import pandas as pd

from model.sentiment.Sentiment import Sentiment


def test_create_sentiment():
    try:
        Sentiment()
    except Exception:
        pytest.fail("Could not create Sentiment.")


def test_setModelType():
    sentiment = Sentiment()

    df = pd.DataFrame(columns=sentiment.column_names)

    try:
        sentiment.setModelTypes(df)
    except Exception:
        pytest.fail("Pandas error")
