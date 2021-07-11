import pytest

import pandas as pd

from gui.component.FlowLayout import FlowLayout

from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)


def test_create_flowlayout():
    layout = FlowLayout()
    
    assert layout != None


def test_has_height_for_width():
    layout = FlowLayout()
    
    assert layout.hasHeightForWidth()
    
def test_count():
    layout = FlowLayout()
    
    assert layout.count() == 0
