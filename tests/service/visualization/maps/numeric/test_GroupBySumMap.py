import pytest
from service.visualization.maps.numeric.GroupBySumMap import GroupBySumMap

import pandas as pd

def test_group_by_sum_map_contructor():
    try:
        map = GroupBySumMap({'variable':'col2'})
    except Exception:
        pytest.fail("Gorup Mean Map creation error")
    
def test_group_by_sum_map_apply():
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 3]})
    map = GroupBySumMap({'variable':'col2'})
    
    df = map.apply(df)
    
    assert df['col1'].loc[0] == 3 and df['col2'].loc[0] == 3