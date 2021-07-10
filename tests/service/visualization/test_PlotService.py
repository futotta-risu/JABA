import pytest
from service.visualization.PlotService import PlotService

import pandas as pd

def test_plot_service_constructior():
    config = PlotService()
    
    assert True
    
def test_get_id():
    config = PlotService()
    
    assert config.getPlotID() == 2
    
def test_reset_id():
    config = PlotService()
    
    config.resetID()
    
    assert config.id == 1