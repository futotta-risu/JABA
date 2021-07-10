import pytest
from service.visualization.maps.numeric.GroupByCountMap import GroupByCountMap

import pandas as pd

def test_group_by_count_map_contructor():
    try:
        map = GroupByCountMap({'variable':'col1'})
    except Exception:
        pytest.fail("Count Map creation error")
    
def test_group_by_count_map_apply():
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 3]})
    map = GroupByCountMap({'variable':'col2'})
    
    df = map.apply(df)
    
    assert df['col1'].loc[0] == 2 and df['col2'].loc[0] == 3