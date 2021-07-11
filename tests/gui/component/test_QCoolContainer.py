import pytest

import pandas as pd

from gui.component.QCoolContainer import QCoolContainer

import sys
from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)

def test_qcoolcontainer_constructor(qtbot):
    container = QCoolContainer()
    assert container is not None