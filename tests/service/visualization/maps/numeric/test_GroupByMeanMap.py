import pytest
from service.visualization.maps.numeric.GroupByMeanMap import GroupByMeanMap

import pandas as pd

def test_group_by_mean_map_contructor():
    try:
        map = GroupByMeanMap({'variable':'col2'})
    except Exception:
        pytest.fail("Gorup Mean Map creation error")
    
def test_group_by_mean_map_apply():
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 3]})
    map = GroupByMeanMap({'variable':'col2'})
    
    df = map.apply(df)
    
    assert df['col1'].loc[0] == 1.5 and df['col2'].loc[0] == 3