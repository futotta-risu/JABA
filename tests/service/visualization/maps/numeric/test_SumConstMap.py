import pytest

from service.visualization.maps.numeric.SumConstMap import SumConstMap

import pandas as pd


def test_sum_map_contructor():
    try:
        SumConstMap({'variable': 'col1'})
    except Exception:
        pytest.fail("Log Map creation error")


def test_sum_map_contructor_with_val():
    try:
        SumConstMap({'variable': 'col1', 'val': '2'})
    except Exception:
        pytest.fail("Log Map creation error")


def test_sum_map_apply():
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

    map = SumConstMap({'variable': 'col1'})

    df = map.apply(df)

    assert df['col1'].loc[0] == 2 and df['col2'].loc[0] == 3


def test_sum_map_apply_val():
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

    map = SumConstMap({'variable': 'col1', 'val': '2'})

    df = map.apply(df)

    assert df['col1'].loc[0] == 3 and df['col2'].loc[0] == 3
