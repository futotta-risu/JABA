import pytest
from service.visualization.maps.MapFactory import MapFactory

import pandas as pd

def test_map_factory_constructior():
    try:
        MapFactory()
    except Exception:
        pytest.fail("Could not create Map Factory")


def test_get_map_list():
    factory = MapFactory()

    assert len(factory.getMapList()) > 0


def test_get_art():
    factory = MapFactory()

    assert factory.getAttrsWithTypes('SumConstMap') is not None

def test_get_art_in_not_implemented():
    factory = MapFactory()
    with pytest.raises(NotImplementedError):
        factory.getAttrsWithTypes('TestMapNotImplemented')

def test_apply():
    factory = MapFactory()
    args = {'variable':'col1'}
    data = pd.DataFrame({'col1':[1,2]})
    assert factory.apply('SumConstMap', data, args=args) is not None