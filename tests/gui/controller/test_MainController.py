import pytest

from gui.controller.MainController import MainController

from unittest.mock import Mock

from PyQt5.QtCore import QSettings

from service.visualization.PlotConfiguration import PlotConfiguration

def test_maincontroller_constructor(qtbot, mocker):
    # Given
    model = Mock()
    model.max_threads = 12
    model.auto_scraping = False
    
    mocker.patch('os.listdir', return_value=['2017-02-02', '2017/02/03', '2017-42-03'])

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

def test_main_controller_change_automatic_scrapper(qtbot):
    # Given
    model = Mock()
    model.max_threads = 12
    model.auto_scraping = False
    controller = MainController(model)
    
    # When
    try:
        controller.change_automatic_scrapper()
        # Then
    except Exception:
        pytest.fail("Changing to automaic scrapper should not raise")

def test_init_settings_on_not_previusly_loaded(mocker):
    # Given
    mocker.patch('PyQt5.QtCore.QSettings.value', side_effect=[BaseException(), 5])
    mock_sync = mocker.patch('PyQt5.QtCore.QSettings.sync')
    model = Mock()
    model.max_threads = 12
    model.auto_scraping = False
    controller = MainController(model)

    mock_sync.assert_called_once()
    

def test_set_settings(mocker):
    settings = QSettings('Test', 'Test settings')
    
    mocker.patch('PyQt5.QtCore.QSettings.value', return_value=12)
    mock_sync = mocker.patch('PyQt5.QtCore.QSettings.sync')
    model = Mock()
    model.max_threads = 12
    model.auto_scraping = False
    controller = MainController(model)

    controller.set_settings(settings)

    mock_sync.assert_called_once()

def test_get_settings(mocker):
    model = Mock()
    model.max_threads = 12
    model.auto_scraping = False
    controller = MainController(model)

    result = controller.get_settings()

    assert result is not None

def test_save_plot_config(mocker):
    mocker_patch = mocker.patch('pickle.dump')

    model = Mock()
    model.max_threads = 12
    model.auto_scraping = False
    controller = MainController(model)

    controller.save_plot_config('test_dump.py')

    mocker_patch.assert_called_once()

def test_open_configure(mocker):
    config = PlotConfiguration('name', 'ini', 'fin', 'map', 'var', 'ind', 'data')
    
    mocker.patch('gui.view.plot_config.PlotConfigure.show')
    mocker.patch('gui.view.plot_config.PlotConfigure.exec_')
    mocker.patch('gui.view.plot_config.PlotConfigure.is_saved', return_value=True)
    mock_p = mocker.patch('gui.view.plot_config.PlotConfigure.getPlotConfiguration', return_value=config)

    model = Mock()
    model.max_threads = 12
    model.auto_scraping = False
    controller = MainController(model)

    a,b,c = controller.open_configure()

    assert a is not None and c is not None
    assert b != ""

def test_open_configure_no_saved(mocker):
    config = PlotConfiguration('name', 'ini', 'fin', 'map', 'var', 'ind', 'data')

    mocker.patch('PyQt5.QtWidgets.QDialog.show')
    mocker.patch('PyQt5.QtWidgets.QDialog.exec_')
    mocker.patch('gui.view.plot_config.PlotConfigure.is_saved', return_value=False)
    mock_p = mocker.patch('gui.view.plot_config.PlotConfigure.getPlotConfiguration', return_value=config)

    model = Mock()
    model.max_threads = 12
    model.auto_scraping = False
    controller = MainController(model)

    a,b,c = controller.open_configure()

    assert a is None and c is None
    assert b == ""

def test_update_plots(mocker):
    mocker_patch = mocker.patch('service.visualization.PlotService.PlotService.updatePlots')

    model = Mock()
    model.max_threads = 12
    model.auto_scraping = False
    controller = MainController(model)

    controller.update_plots('2012-02-02','nltk')

    mocker_patch.assert_called_once()


def test_get_plots(mocker):
    model = Mock()
    model.max_threads = 12
    model.auto_scraping = False
    controller = MainController(model)

    result = controller.get_plots()

    assert result is not None

def test_delete_plot(mocker):
    model = Mock()
    model.max_threads = 12
    model.auto_scraping = False
    controller = MainController(model)

    controller.plot_configurations = [{'id':1}, {'id':2}, {'id':3}]

    result = controller.delete_plot(2)

    assert len(controller.plot_configurations) == 2 

def test_delete_plot_on_non_existent(mocker):
    model = Mock()
    model.max_threads = 12
    model.auto_scraping = False
    controller = MainController(model)

    controller.plot_configurations = [{'id':1}, {'id':2}, {'id':3}]

    result = controller.delete_plot(10)

    assert len(controller.plot_configurations) == 3
