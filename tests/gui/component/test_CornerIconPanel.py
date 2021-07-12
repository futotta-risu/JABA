import pytest

from gui.component.CornerIconPanel import CornerIconPanel

from PyQt5.QtWidgets import QLabel


def test_cornericonpanel_constructor(qtbot):
    # Given
    label = QLabel('Label')
    label2 = QLabel('Label2')

    # When
    try:
        CornerIconPanel(label, label2)
        # Then
    except Exception:
        pytest.fail("Could not create CornerIconPanel")
