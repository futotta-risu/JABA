import pytest
from service.visualization.PlotService import PlotService


def test_plot_service_constructior():
    try:
        PlotService()
    except Exception:
        pytest.fail("Could not create PlotService")


def test_get_id():
    config = PlotService()

    assert config.getPlotID() == 2


def test_reset_id():
    config = PlotService()

    config.resetID()

    assert config.id == 1
