import pytest
from service.visualization.maps.MapFactory import MapFactory


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
