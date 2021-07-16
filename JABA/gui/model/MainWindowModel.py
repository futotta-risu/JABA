from PyQt5.QtCore import QObject, pyqtSignal


class MainWindowModel(QObject):
    auto_scraping_changed = pyqtSignal(bool)

    @property
    def max_threads(self):
        return self._max_threads

    @property
    def auto_scraping(self):
        return self._auto_scraping

    @auto_scraping.setter
    def auto_scraping(self, value):
        self._auto_scraping = value
        self.auto_scraping_changed.emit(value)

    def __init__(self):
        super().__init__()

        self._message_sample = []
        self._max_threads = 12
        self._auto_scraping = False
