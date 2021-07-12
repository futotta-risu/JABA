import pytest
from service.visualization.maps.numeric.SqrtMap import SqrtMap

import pandas as pd


def test_sqrt_map_contructor():
    try:
        SqrtMap({'variable': 'col1'})
    except Exception:
        pytest.fail("Log Map creation error")


def test_sqrt_map_apply():
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    map = SqrtMap({'variable': 'col1'})

    df = map.apply(df)

    assert df['col1'].loc[0] == 1.0 and df['col2'].loc[0] == 3
    assert pytest.approx(df['col1'].loc[1], 0.1) == 1.41
