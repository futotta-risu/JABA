import pytest

from gui.controller.MainController import MainController

from unittest.mock import Mock


def test_maincontroller_constructor(qtbot):
    # Given
    model = Mock()
    model.max_threads.return_value = 12
    model.auto_scraping.return_value = False

    # When
    try:
        MainController(model)
        # Then
    except Exception:
        pytest.fail("Could not create MainController")
