import pyqtgraph as pg

from PyQt5 import Qt, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from pyqtgraph import plot, PlotWidget


class ConfigurationDialog(QDialog):
    def __init__(self, controller):
        super().__init__()
        self._controller = controller
        self.settings = controller.get_settings()

        self._load_window_properties()
        self._load_window_components()
        self._set_settings_values()

        self.show()

    def _load_window_properties(self):
        self.setFixedSize(400, 200)
        self.setWindowTitle("Configuration")

    def _load_window_components(self):
        container = QWidget(self)
        form_layout = QFormLayout()
        container.setLayout(form_layout)
        
        self.initial_date_pick = QDateEdit(calendarPopup=True)
        form_layout.addRow( QLabel("Initial Date"), self.initial_date_pick)

        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        
        form_layout.addRow(QLabel("Save"), self.save_button)

        

    def _set_settings_values(self):
        self.initial_date_pick.setDate(
            self.settings.value("initial_date", type=QDate))

    def save_settings(self):
        self.settings.setValue("initial_date", self.initial_date_pick.date())
        self._controller.set_settings(self.settings)
        self.close()