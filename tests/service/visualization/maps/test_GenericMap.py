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

def test_get_attr_with_types():
    map = GenericMap({'variable': 'col1'})

    assert map.getAttrsWithTypes() == {}


def test_applies_raises_not_implemented():
    map = GenericMap({'variable': 'col1'})

    with pytest.raises(NotImplementedError):
        map.apply({})

def test_get_attr_with_types():
    map = GenericMap({'variable': 'col1'})

    map.setAttrs({'cucu':'tras'})

    assert map.attrs == {'cucu':'tras'}