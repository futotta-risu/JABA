import pytest

import pandas as pd

from gui.component.BorderLayout import BorderLayout


def test_create_borderlayout():
    layout = BorderLayout()
    
    assert layout != None

def test_create_borderlayout_with_margin():
    layout = BorderLayout(margin = 3)
    
    assert layout != None

def test_has_height_for_width():
    layout = BorderLayout()
    
    assert not layout.hasHeightForWidth()
    
def test_count():
    layout = BorderLayout()
    
    assert layout.count() == 0
