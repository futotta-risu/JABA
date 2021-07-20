import pytest

from gui.view.AddPlotView import AddPlotView

from unittest.mock import Mock


def test_add_plot_view_constructor(qtbot):
    # Given
    controller = Mock()
    model = Mock()
    # When
    try:
        AddPlotView(qtbot, controller, model)
        # Then
        assert True
    except Exception:
        pytest.fail("Could not create Plot Config")

def test___load_map_config_Text(qtbot):
    # Given
    controller = Mock()
    model = Mock()

    config = AddPlotView(qtbot, controller, model)

    try:
        config._AddPlotView__load_map_config('SqrtMap')
        config._AddPlotView__load_map_config('LogMap')
    except Exception:
        pytest.fail("Changing maps should not fail")

def test___load_map_config_Variable(qtbot):
    # Given
    controller = Mock()
    model = Mock()

    config = AddPlotView(qtbot, controller, model)

    try:
        config._AddPlotView__load_map_config('SqrtMap')
        config._AddPlotView__load_map_config('MultiplyMap')
    except Exception:
        pytest.fail("Changing maps should not fail")

def test_transform_map(qtbot, mocker):
    mocker.patch('PyQt5.QtWidgets.QComboBox.currentText', side_effect=['Tweet', 'NumReplies'])
    controller = Mock()
    model = Mock()
    model.map_list = []

    config = AddPlotView(qtbot, controller, model)
    config._AddPlotView__load_map_config('SqrtMap')
    
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

    controller = Mock()
    model = Mock()
    model.map_list = []

    config = AddPlotView(qtbot, controller, model)
    config._AddPlotView__load_map_config('SqrtMap')
    config.transform_map('SqrtMap')

    config._AddPlotView__save_and_exit()
    
    mock.assert_called_once()