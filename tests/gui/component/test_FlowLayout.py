import pytest

from gui.component.FlowLayout import FlowLayout


def test_create_flowlayout(qtbot):
    try:
        FlowLayout()
    except Exception:
        pytest.fail("Could not create FlowLayout")


def test_has_height_for_width(qtbot):
    layout = FlowLayout()

    assert layout.hasHeightForWidth()


def test_count(qtbot):
    layout = FlowLayout()

    assert layout.count() == 0
