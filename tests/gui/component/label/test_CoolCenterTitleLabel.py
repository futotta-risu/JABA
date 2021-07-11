import pytest

import pandas as pd

from gui.component.label.CoolCenterTitleLabel import CoolCenterTitleLabel

from PyQt5.QtWidgets import QLabel

def test_coolcentertitlelabel_constructor(qtbot):
    # Given
    
    # When
    container = CoolCenterTitleLabel("Title")
    
    # Then
    assert container is not None