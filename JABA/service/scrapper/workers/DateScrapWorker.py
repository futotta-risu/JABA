from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QRunnable
from PyQt5.QtCore import QThreadPool
from PyQt5.QtCore import QSettings


from service.scrapper.scrapper import TwitterScrapper
from service.scrapper.scrapper import ScrapperFileManager
from service.scrapper.analyzer import Analyzer


from datetime import timedelta

class Signals(QObject):
    finished = pyqtSignal()
    
class DateScrapWorker(QRunnable):
    '''
        Thread which scraps tweets and analyzes them. The thread need a date_from to work.
        
        Emits a finished signal in case of automatic scrapping.
    '''
    
    signal = Signals()
    
    def set_date(self, date_from):
        self.date_from = date_from
    
    def run(self):
        if self.date_from == None:
            raise Exception()
        
        scrapper = TwitterScrapper()
        analyzer = Analyzer()
        
        scrapper.scrap(self.date_from, self.date_from + timedelta(days=1), verbose=True)
        analyzer.analyze(self.date_from, ScrapperFileManager())

        self.signal.finished.emit()