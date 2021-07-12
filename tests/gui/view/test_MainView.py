import pytest

from gui.view.MainView import MainView

from unittest.mock import Mock


def test_mainview_constructor(qtbot):
    # Given
    model = Mock()
    model.max_threads.return_value = 12
    model.auto_scraping.return_value = False

    controller = Mock()
    controller.get_dates.return_value = []
    controller.get_plots.return_value = []
    controller.load_plot_config.return_value = []

    # When
    try:
        MainView(model, controller)
        # Then
        assert True
    except Exception:
        pytest.fail("Could not create MainWindow")
