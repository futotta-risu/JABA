import pytest

import pandas as pd

from gui.component.FlowLayout import FlowLayout

import sys
from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)


def test_create_flowlayout(qtbot):
    layout = FlowLayout()
    
    assert layout != None


def test_has_height_for_width(qtbot):
    layout = FlowLayout()
    
    assert layout.hasHeightForWidth()
    
def test_count(qtbot):
    layout = FlowLayout()
    
    assert layout.count() == 0
