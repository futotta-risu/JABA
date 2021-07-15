import pytest

from gui.view.plot_config import PlotConfigure

from unittest.mock import Mock


def test_plot_config_constructor(qtbot):
    # Given

    # When
    try:
        PlotConfigure(qtbot)
        # Then
        assert True
    except Exception:
        pytest.fail("Could not create Plot Config")

def test___load_map_config_Text(qtbot):
    # Given
    config = PlotConfigure(qtbot)

    try:
        config._PlotConfigure__load_map_config('SqrtMap')
        config._PlotConfigure__load_map_config('LogMap')
    except Exception:
        pytest.fail("Changing maps should not fail")

def test___load_map_config_Variable(qtbot):
    # Given
    config = PlotConfigure(qtbot)

    try:
        config._PlotConfigure__load_map_config('SqrtMap')
        config._PlotConfigure__load_map_config('MultiplyMap')
    except Exception:
        pytest.fail("Changing maps should not fail")

def test_transform_map(qtbot, mocker):
    mocker.patch('PyQt5.QtWidgets.QComboBox.currentText', side_effect=['Tweet', 'NumReplies'])

    config = PlotConfigure(qtbot)
    config._PlotConfigure__load_map_config('SqrtMap')
    
    try:
        config.transform_map('SqrtMap')
    except Exception:
        pytest.fail('Transform map should not raise exception.')

def test_save_and_exit(qtbot, mocker):
    mocker.patch(
        'PyQt5.QtWidgets.QComboBox.currentText',
        side_effect=['Tweet', 'NumReplies','Tweet','Range Index', 'NumReplies']
        )
        
    mock = mocker.patch('PyQt5.QtWidgets.QDialog.close')

    config = PlotConfigure(qtbot)
    config._PlotConfigure__load_map_config('SqrtMap')
    config.transform_map('SqrtMap')

    config._PlotConfigure__save_and_exit()
    
    mock.assert_called_once()