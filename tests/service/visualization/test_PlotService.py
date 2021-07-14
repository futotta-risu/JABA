import pytest
from service.visualization.PlotService import PlotService
from service.visualization.PlotConfiguration import PlotConfiguration

from service.visualization.maps.numeric.SqrtMap import SqrtMap

from pyqtgraph import PlotWidget
from PyQt5.QtCore import QDate
import pandas as pd

from model.bitcoin.Bitcoin import Bitcoin

from datetime import datetime



def test_plot_service_constructior():
    try:
        PlotService()
    except Exception:
        pytest.fail("Could not create PlotService")


def test_get_id():
    config = PlotService()

    assert config.getPlotID() == 2


def test_reset_id():
    service = PlotService()

    service.resetID()

    assert service.id == 1

def test_getDataPriorities():
    service = PlotService()
    
    assert service.getDataPriorities("Bitcoin") == 2
    assert service.getDataPriorities("Sentiment") == 0
    assert service.getDataPriorities("Tweet") == 1

def test_reorderConfiguration(mocker):
    bitcoin_frame = Bitcoin().createModelFrame()
    map_list = [SqrtMap({'variable': 'Close'})]
    now = datetime.now()
    
    config = PlotConfiguration(
        'BTC', bitcoin_frame, bitcoin_frame,
        map_list, "Bitcoin", "Range Index", 'Close'
    )
    
    r_config = {'config': config, 'widget': PlotWidget(), 'id': 1}
    frame = pd.DataFrame({'Close' : [133,133], 'timestamp':[now,now], 'round_datetime':[now, now]})
    
    mocker.patch('pandas.read_csv', return_value=frame)
    
    service= PlotService()
    
    try:
        service.updatePlots([r_config], '2010/05/05', 'nltk')
    except Exception:
        pytest.fail("updatePlots should not fail")