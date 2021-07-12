import pytest
from service.visualization.maps.GenericMap import GenericMap


def test_sqrt_map_contructor():
    try:
        GenericMap({'variable': 'col1'})
    except Exception:
        pytest.fail("Log Map creation error")


def test_get_name():
    map = GenericMap({'variable': 'col1'})

    assert map.getName() == "Generic Map"
