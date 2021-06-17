import pyqtgraph as pg
from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QRunnable
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from pyqtgraph import plot
from pyqtgraph import PlotWidget


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
        self.initial_date_pick.setDate(
            self.settings.value("initial_date", type=QDate))

    def save_settings(self):
        self.settings.setValue("initial_date", self.initial_date_pick.date())
        self._controller.set_settings(self.settings)
        self.close()
