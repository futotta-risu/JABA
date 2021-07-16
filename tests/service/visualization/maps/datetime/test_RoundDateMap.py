import pytest
from service.visualization.maps.datetime.RoundDateMap import RoundDateMap

import pandas as pd
import datetime

def test_round_map_contructor():
    try:
        RoundDateMap({'round': 'min'})
    except Exception:
        pytest.fail("Round Date Map creation error")


def test_round_map_contructor_with_attrs_as_None():
    try:
        RoundDateMap(None)
    except Exception:
        pytest.fail("Round Date Map creation error")


def test_round_map_contructor_with_attrs_but_not_round():
    try:
        RoundDateMap({'rund': 3})
    except Exception:
        pytest.fail("Round Date Map creation error")


def test_count_get_arrt_with_types():
    map = RoundDateMap({'round': 'min'})

    assert "round" in map.getAttrsWithTypes()

def test_apply():
    map = RoundDateMap({'round': 'min', 'variable':'time'})

    now = datetime.datetime.now()

    data = pd.DataFrame({'time':[now, now]})
    data = map.apply(data)
    
    assert 'round_time' in data.columns
