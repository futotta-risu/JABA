import pytest
from service.visualization.maps.datetime.RoundDateMap import RoundDateMap

import pandas as pd

def test_round_map_contructor():
    try:
        map = RoundDateMap({'round':'min'})
    except Exception:
        pytest.fail("Round Date Map creation error")
    
def test_round_map_contructor_with_attrs_as_None():
    try:
        map = RoundDateMap(None)
    except Exception:
        pytest.fail("Round Date Map creation error")
        
def test_round_map_contructor_with_attrs_but_not_round():
    try:
        map = RoundDateMap({'rund':3})
    except Exception:
        pytest.fail("Round Date Map creation error")      
        
def test_count_get_arrt_with_types():
    map = RoundDateMap({'round':'min'})
    
    assert "round" in map.getAttrsWithTypes()