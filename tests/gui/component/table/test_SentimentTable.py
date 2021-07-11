import pytest

import pandas as pd

from gui.component.table.SentimentTable import SentimentTable

from PyQt5.QtWidgets import QLabel

import sys
from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)

def test_sentimenttable_constructor(qtbot):
    # Given
    
    # When
    container = SentimentTable()
    
    # Then
    assert container is not None
    
def test_sentimenttable_add_row(qtbot):
    # Given
    container = SentimentTable()
    
    # When
    try:
        container.addRow("Text", 0.4)
        # Then
    except:
        pytest.fail("Sentiment Table addRow should not raise.")