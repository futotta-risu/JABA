import pytest
from service.visualization.maps.general.CountMap import CountMap

import pandas as pd

def test_count_map_contructor():
    try:
        map = CountMap({'variable':'col1'})
    except Exception:
        pytest.fail("Count Map creation error")
    
def test_count_map_apply():
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 3]})
    map = CountMap({'variable':'col1'})
    
    df = map.apply(df)
    
    assert df['count'].loc[0] == 2 and df['count'].loc[1] == 2