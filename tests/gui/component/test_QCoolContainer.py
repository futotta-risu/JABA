import pytest

from gui.component.QCoolContainer import QCoolContainer


def test_qcoolcontainer_constructor(qtbot):
    try:
        QCoolContainer()
    except Exception:
        pytest.fail("Could not create QCoolContainer")
