import pytest

from service.visualization.maps.numeric.Log2Map import Log2Map

import pandas as pd


def test_log_map_contructor():
    try:
        Log2Map({'variable': 'col1'})
    except Exception:
        pytest.fail("Log Map creation error")


def test_log_map_apply():
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    map = Log2Map({'variable': 'col1'})

    df = map.apply(df)

    assert df['col1'].loc[0] == 0 and df['col1'].loc[1] == 1 and df['col2'].loc[0] == 3
