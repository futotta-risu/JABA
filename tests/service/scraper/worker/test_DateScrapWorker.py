import pytest

from gui.controller.MainController import MainController

from unittest.mock import Mock

from PyQt5.QtCore import QSettings, QDate

from service.scraper.worker.DateScrapWorker import DateScrapWorker

import datetime
import pandas as pd

def test_datescrapworker_constructor(qtbot, mocker):
    # Given
    try:
        DateScrapWorker()
    except Exception:
        pytest.fail("Could not create worker")
   
def test_datescrapwroker_run(qtbot, mocker):
    mocker.patch('service.scraper.social.TwitterScraper.TwitterScraper.scrap', return_value=None)
    mock = mocker.patch('service.scraper.sentiment.analyzer.Analyzer.analyze')

    worker = DateScrapWorker()
    worker.set_date(QDate(2010, 2, 3))

    worker.run()

    mock.assert_called_once()

def test_datescrapwroker_run_exception(qtbot, mocker):
    mocker.patch('service.scraper.social.TwitterScraper.TwitterScraper.scrap', return_value=None)
    mock = mocker.patch('service.scraper.sentiment.analyzer.Analyzer.analyze')

    worker = DateScrapWorker()

    with pytest.raises(Exception):
        worker.run()
