import pytest

from gui.component.BorderLayout import BorderLayout

from PyQt5.QtWidgets import QLabel

from PyQt5.QtCore import QRect

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

def test_set_geometry(qtbot):
    layout = BorderLayout()
    layout.addWidget(QLabel("Test2"), BorderLayout.North)
    layout.addWidget(QLabel("Test2"), BorderLayout.West)
    layout.addWidget(QLabel("Test2"), BorderLayout.East)
    layout.addWidget(QLabel("Test2"), BorderLayout.Center)
    layout.addWidget(QLabel("Test2"), BorderLayout.South)
    try:
        layout.setGeometry(QRect(100,100,500,500))
    except Exception:
        pytest.fail("BorderLayout setGeometry should not raise Exception")

def test_calculate_size(qtbot):
    layout = BorderLayout()
    layout.addWidget(QLabel("Test2"), BorderLayout.North)
    layout.addWidget(QLabel("Test2"), BorderLayout.West)
    layout.addWidget(QLabel("Test2"), BorderLayout.East)
    layout.addWidget(QLabel("Test2"), BorderLayout.Center)
    layout.addWidget(QLabel("Test2"), BorderLayout.South)
    try:
        layout.calculateSize(BorderLayout.MinimumSize)
        layout.calculateSize(BorderLayout.SizeHint)
    except Exception:
        pytest.fail("BorderLayout setGeometry should not raise Exception")