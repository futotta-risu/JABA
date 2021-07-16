import pytest

from gui.component.FlowLayout import FlowLayout

from PyQt5.QtCore import Qt, QRect

from PyQt5.QtWidgets import QLabel

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

def test_heightForWidth(qtbot):
    layout = FlowLayout()

    try:
        layout.heightForWidth(32)
    except Exception:
        pytest.fail("Exception trying to get minimumSize in FlowLayout")
    
def test_sizeHint(qtbot):
    layout = FlowLayout()

    try:
        layout.sizeHint()
    except Exception:
        pytest.fail("Exception trying to get minimumSize in FlowLayout")
    
def test_minimumSize(qtbot):
    layout = FlowLayout()
    layout.addWidget(QLabel("Test2"))
    try:
        layout.minimumSize()
    except Exception:
        pytest.fail("Exception trying to get minimumSize in FlowLayout")

def test_expandingDirections(qtbot):
    layout = FlowLayout()

    assert layout.expandingDirections() == Qt.Orientations(Qt.Orientation(0))

def test_set_geometry(qtbot):
    layout = FlowLayout()
    layout.addWidget(QLabel("Test2"))
    layout.addWidget(QLabel("Test2"))
    layout.addWidget(QLabel("Test2"))
    layout.addWidget(QLabel("Test2"))
    layout.addWidget(QLabel("Test2"))

    try:
        layout.setGeometry(QRect(100,100,500,500))
    except Exception:
        pytest.fail("FlowLayout setGeometry should not raise Exception")
