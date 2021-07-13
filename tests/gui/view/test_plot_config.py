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