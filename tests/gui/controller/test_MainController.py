import pytest

from gui.controller.MainController import MainController

from unittest.mock import Mock


def test_maincontroller_constructor(qtbot, mocker):
    # Given
    model = Mock()
    model.max_threads = 12
    model.auto_scraping = False
    
    mocker.patch('os.listdir', return_value=['2017/02/02', '2017/02/03', '2017/42/03'])

    # When
    try:
        MainController(model)
        # Then
    except Exception:
        pytest.fail("Could not create MainController")

def test_maincontroller_get_analysis_method(qtbot):
    # Given
    model = Mock()
    model.max_threads = 12
    model.auto_scraping = False
    controller = MainController(model)
    
    # When
    methods = controller.get_analysis_methods()
    
    # Then
    assert methods == ['nltk', 'textblob']
