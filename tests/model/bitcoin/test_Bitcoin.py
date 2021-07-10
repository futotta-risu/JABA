import pytest

import pandas as pd

from model.bitcoin.Bitcoin import Bitcoin

def test_create_bitcoin():
    bitcoin = Bitcoin()
    
    assert bitcoin != None

    
def test_setModelType():
    bitcoin = Bitcoin()
    
    df = pd.DataFrame(columns=bitcoin.column_names)
    
    try:
        bitcoin.setModelTypes(df)
    except Exception:
        pytest.fail("Pandas error")