import pytest
from service.visualization.maps.MapFactory import MapFactory

import pandas as pd

def test_map_factory_constructior():
    factory = MapFactory()
    
    assert True
    
def test_get_map_list():
    factory = MapFactory()
    
    assert len(factory.getMapList()) > 0 
    
    
def test_get_art():
    factory = MapFactory()
        
    assert factory.getAttrsWithTypes('SumConstMap') is not None