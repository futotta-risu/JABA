import pytest

from gui.controller.MainController import MainController

from unittest.mock import Mock


def test_maincontroller_constructor(qtbot):
    # Given
    model = Mock()
    model.max_threads = 12
    model.auto_scraping = False

    # When
    try:
        MainController(model)
        # Then
    except Exception:
        pytest.fail("Could not create MainController")
