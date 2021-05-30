from PyQt5.QtCore import QObject

class Signals(QObject):
    finished = pyqtSignal()
    
class AnalyzeDateWorker(QRunnable):
    signal = Signals()
    
    def set_date(self, date_from):
        self.date_from = date_from
    
    def run(self):
        get_tweets(query, self.date_from, self.date_from + timedelta(days=1), verbose = True)
        self.signal.finished.emit()

class MainController(QObject):
    def __init__(self, model):
        super().__init__()
        
        self._model = model
        
    
    def analyze_date(self, date):
        AnalyzeDateWorker