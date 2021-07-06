import pytest
from service.visualization.types.maps.GenericMap import GenericMap

import pandas as pd

def test_sqrt_map_contructor():
    try:
        map = GenericMap({'variable':'col1'})
    except Exception:
        pytest.fail("Log Map creation error")
    
def test_get_name():
    map = GenericMap({'variable':'col1'})
    
    assert map.getName() == "Generic Map"