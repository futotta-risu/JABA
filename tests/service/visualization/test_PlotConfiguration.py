import pytest
from service.visualization.PlotConfiguration import PlotConfiguration

import pandas as pd


def test_plot_configuration_constructior():
    try:
        PlotConfiguration(
            'Name',
            pd.DataFrame(),
            pd.DataFrame(),
            [],
            'Integer',
            'Range',
            'Column2'
        )
    except Exception:
        pytest.fail("Could not create PlotConfiguration")
