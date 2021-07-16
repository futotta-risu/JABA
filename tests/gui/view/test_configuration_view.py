import pytest

from gui.view.configuration_view import ConfigurationDialog

from unittest.mock import Mock

from PyQt5.QtCore import QSettings


def test_configuration_dialog_constructor(qtbot):
    # Given
    settings = QSettings('test-settings', 'Test dialog')
    controller_mock = Mock()
    controller_mock.get_settings.return_value = settings
    controller_mock.get_analysis_methods.return_value = ['nltk','textblob']
    controller_mock.get_analysis_method.return_value = 'nltk'
    controller_mock.set_settings.return_value = None

    # When
    try:
        ConfigurationDialog(controller_mock)
        # Then
        assert True
    except Exception:
        pytest.fail("Could not create Configuration Dialog")

def test_configuration_dialog_save_settings(qtbot):
    # Given
    settings = QSettings('test-settings', 'Test dialog')
    controller_mock = Mock()
    controller_mock.get_settings.return_value = settings
    controller_mock.get_analysis_methods.return_value = ['nltk','textblob']
    controller_mock.get_analysis_method.return_value = 'nltk'
    controller_mock.set_settings.return_value = None

    dialog = ConfigurationDialog(controller_mock)

    # When
    try:
        dialog.save_settings()
        # Then
        assert True
    except Exception:
        pytest.fail("Could not create Configuration Dialog")