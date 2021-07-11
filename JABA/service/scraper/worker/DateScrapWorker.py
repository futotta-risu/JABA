from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QRunnable


from model.social.TweetFileManager import TweetFileManager

from service.scraper.social.TwitterScraper import TwitterScraper
from service.scraper.sentiment.analyzer import Analyzer

from datetime import timedelta


class Signals(QObject):
    finished = pyqtSignal()


class DateScrapWorker(QRunnable):
    '''
        Thread which scraps tweets and analyzes them. The thread need a date_from to work.

        Emits a finished signal in case of automatic scrapping.
    '''

    def __init__(self):
        super().__init__()
        self.signal = Signals()

    def set_date(self, date_from):
        self.date_from = date_from

    def run(self):
        if self.date_from is None:
            raise Exception()

        scrapper = TwitterScraper()
        analyzer = Analyzer()

        scrapper.scrap(self.date_from)
        analyzer.analyze(self.date_from, TweetFileManager())

        self.signal.finished.emit()
