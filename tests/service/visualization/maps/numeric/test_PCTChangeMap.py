import pytest

from service.visualization.maps.numeric.PCTChangeMap import PCTChangeMap

import pandas as pd


def test_pct_map_contructor():
    try:
        PCTChangeMap({'variable': 'col1'})
    except Exception:
        pytest.fail("Log Map creation error")


def test_pct_map_apply():
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    map = PCTChangeMap({'variable': 'col1'})

    df = map.apply(df)

    assert 'col1_PCT' in df.columns
