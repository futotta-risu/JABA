import pytest

import pandas as pd

from gui.component.QCoolContainer import QCoolContainer

def test_qcoolcontainer_constructor(qtbot):
    container = QCoolContainer()
    assert container is not None