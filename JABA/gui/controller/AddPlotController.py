from PyQt5.QtCore import QObject, pyqtSignal


class AddPlotController(QObject):

    def __init__(self, model):
        super().__init__()
        self._model = model

