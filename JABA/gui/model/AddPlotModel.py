from PyQt5.QtCore import QObject, pyqtSignal


class AddPlotModel(QObject):

    def __init__(self):
        super().__init__()

        self._saved = False
        self.__configuration = None
        self._map_list = []

    @property
    def saved(self):
        return self._saved

    @saved.setter
    def saved(self, value):
        self._saved = value

    @property
    def map_list(self):
        return self._map_list

    def add_map(self, map):
        self._map_list += [map]
    
    def clear_maps(self):
        self._map_list = []