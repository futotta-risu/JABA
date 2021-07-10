import pytest

import pandas as pd

from gui.component.BorderLayout import BorderLayout

def test_create_borderlayout():
    layout = BorderLayout()
    
    assert layout != None

    