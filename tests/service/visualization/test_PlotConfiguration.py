import pytest
from service.visualization.PlotConfiguration import PlotConfiguration

import pandas as pd

def test_plot_configuration_constructior():
    config = PlotConfiguration(
        'Name',
        pd.DataFrame(),
        pd.DataFrame(),
        [],
        'Integer',
        'Range',
        'Column2')
    
    assert True