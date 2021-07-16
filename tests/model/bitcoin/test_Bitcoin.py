import pytest

import pandas as pd

from model.bitcoin.Bitcoin import Bitcoin


def test_create_bitcoin():
    try:
        Bitcoin()
    except Exception:
        pytest.fail("Could not create Bitcoin model")


def test_setModelType():
    bitcoin = Bitcoin()

    df = pd.DataFrame(columns=bitcoin.column_names)

    try:
        bitcoin.setModelTypes(df)
    except Exception:
        pytest.fail("Pandas error")
