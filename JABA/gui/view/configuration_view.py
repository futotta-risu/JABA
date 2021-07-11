from PyQt5 import Qt

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (QLabel, QPushButton)
from PyQt5.QtWidgets import (QFormLayout)
from PyQt5.QtWidgets import (QDateEdit, QComboBox)

from loguru import logger


class ConfigurationDialog(QDialog):
    def __init__(self, controller):
        super().__init__()

        logger.info("Starting configuration dialog.")

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
        form_layout.addRow(QLabel("Initial Date"), self.initial_date_pick)

        self.combo_sentiment_algorithm = QComboBox(self)
        self.combo_sentiment_algorithm.addItems(self._controller.get_analysis_methods())

        form_layout.addRow(QLabel("Sentiment Algorithm"), self.combo_sentiment_algorithm)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)

        form_layout.addRow(QLabel("Save"), self.save_button)

    def _set_settings_values(self):
        self.initial_date_pick.setDate(
            self.settings.value("initial_date", type=Qt.QDate))
        index = self._controller.get_analysis_methods().index(self._controller.get_analysis_method())
        self.combo_sentiment_algorithm.setCurrentIndex(index)

    def save_settings(self):
        self.settings.setValue("initial_date", self.initial_date_pick.date())
        self.settings.setValue("analysis_algorithm", self.combo_sentiment_algorithm.currentValue())
        self._controller.set_settings(self.settings)
        self.close()
