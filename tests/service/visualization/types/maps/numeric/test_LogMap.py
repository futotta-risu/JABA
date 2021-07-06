import pytest
from service.visualization.types.maps.numeric.LogMap import LogMap

import pandas as pd

def test_log2_map_contructor():
    try:
        map = LogMap({'variable':'col1'})
    except Exception:
        pytest.fail("Log Map creation error")
    
def test_log2_map_apply():
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    map = LogMap({'variable':'col1'})
    
    df = map.apply(df)
    
    assert df['col1'].loc[0] == 0 and df['col2'].loc[0] == 3