import pyqtgraph as pg
from PyQt5 import Qt, QtCore, QtGui
from PyQt5.QtCore import (QDate, QObject, QRunnable, QSettings, QThreadPool,
                          pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import (QComboBox, QDateEdit, QDialog, QFileDialog,
                             QFormLayout, QGridLayout, QLabel, QMainWindow,
                             QPushButton, QScrollArea, QSplitter, QVBoxLayout,
                             QWidget)
from pyqtgraph import PlotWidget, plot


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

        initial_date_lbl = QLabel("Initial Date")
        self.initial_date_pick = QDateEdit(calendarPopup=True)

        form_layout = QFormLayout()
        form_layout.addRow(initial_date_lbl, self.initial_date_pick)

        initial_save_lbl = QLabel("Save")
        self.save_button = QPushButton("Save")
        form_layout.addRow(initial_save_lbl, self.save_button)

        self.save_button.clicked.connect(self.save_settings)

        container.setLayout(form_layout)

    def _set_settings_values(self):
        self.initial_date_pick.setDate(self.settings.value("initial_date", type=QDate))

    def save_settings(self):
        self.settings.setValue("initial_date", self.initial_date_pick.date())
        self._controller.set_settings(self.settings)
        self.close()
