import pytest

from gui.component.BorderLayout import BorderLayout

from PyQt5.QtWidgets import QLabel


def test_create_borderlayout(qtbot):
    try:
        BorderLayout()
    except Exception:
        pytest.fail("Could not create BorderLayout")


def test_create_borderlayout_with_margin(qtbot):
    try:
        BorderLayout(margin=3)
    except Exception:
        pytest.fail("Could not create BorderLayout")


def test_has_height_for_width(qtbot):
    layout = BorderLayout()

    assert not layout.hasHeightForWidth()


def test_count(qtbot):
    layout = BorderLayout()

    assert layout.count() == 0


def test_add_widget(qtbot):
    layout = BorderLayout()
    label = QLabel("test")

    try:
        layout.addWidget(label, BorderLayout.North)
    except Exception:
        pytest.fail("BorderLayout addWidget should not raise Exception")
