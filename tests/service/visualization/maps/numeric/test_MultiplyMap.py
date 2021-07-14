import pytest
from service.visualization.maps.numeric.MultiplyMap import MultiplyMap

import pandas as pd


def test_log_map_contructor():
    try:
        MultiplyMap({'variable': 'col1'})
    except Exception:
        pytest.fail("Log Map creation error")


def test_log_map_apply():
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    map = MultiplyMap({'variable': 'col1', 'second': 'col2'})

    df = map.apply(df)

    assert df['col1*col2'].loc[0] == 3
    assert df['col1*col2'].loc[1] == 8

def test_log_map_apply_with_None_second():
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    map = MultiplyMap({'variable': 'col1', 'second': None})

    with pytest.raises(Exception):
        map.apply(df)

def test_log_map_apply_without_second():
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    map = MultiplyMap({'variable': 'col1'})

    with pytest.raises(Exception):
        map.apply(df)

def test_multiply_map_get_attrs_types():
    map = MultiplyMap({'variable': 'col1'})
    
    assert map.getAttrsWithTypes() == {"second": ("Variable", "")}
