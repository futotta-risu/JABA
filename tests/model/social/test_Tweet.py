import pytest

import pandas as pd

from model.social.Tweet import Tweet


def test_create_tweet():
    try:
        Tweet()
    except Exception:
        pytest.fail("Could not create Tweet")


def test_setModelType():
    tweet = Tweet()

    df = pd.DataFrame(columns=tweet.column_names)

    try:
        tweet.setModelTypes(df)
    except Exception:
        pytest.fail("Pandas error")
