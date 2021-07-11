import pytest

import pandas as pd

from gui.component.FlowLayout import FlowLayout

def test_create_flowlayout(qtbot):
    layout = FlowLayout()
    
    assert layout != None


def test_has_height_for_width(qtbot):
    layout = FlowLayout()
    
    assert layout.hasHeightForWidth()
    
def test_count(qtbot):
    layout = FlowLayout()
    
    assert layout.count() == 0
