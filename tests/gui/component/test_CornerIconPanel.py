import pytest

import pandas as pd

from gui.component.CornerIconPanel import CornerIconPanel

from PyQt5.QtWidgets import QLabel

def test_cornericonpanel_constructor(qtbot):
    # Given
    label = QLabel('Label')
    label2 = QLabel('Label2')
    
    # When
    container = CornerIconPanel(label, label2)
    
    # Then
    assert container is not None