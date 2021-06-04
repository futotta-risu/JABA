from PyQt5.QtCore import QObject, pyqtSignal


class Model(QObject):
    thread_count_changed = pyqtSignal(int)
    scrapping_changed = pyqtSignal(bool)
    
    @property
    def thread_count(self):
        return self._thread_count

    @property
    def thread_count_str(self):
        return str(self._thread_count)
    
    @thread_count.setter
    def thread_count(self, value):
        self._thread_count = value
        self.thread_count_changed.emit(value)
    
    
    @property
    def scrapping(self):
        return self._scrapping
    
    @scrapping.setter
    def scrapping(self, value):
        self._scrapping = value
        self.scrapping_changed.emit(value)
    
    def __init__(self):
        super().__init__()

        self._thread_count = 0
        self._scrapping = False