from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QScrollArea, QSplitter
from PyQt5.QtWidgets import (
    QPushButton,
    QFileDialog,
    QCalendarWidget,
    QLabel,
    QComboBox,
    QAction,
    QMenuBar,
    QMenu,
)
from PyQt5.QtCore import (
    QObject,
    QThreadPool,
    pyqtSignal,
    QRunnable,
    pyqtSlot,
    QSettings,
)
from PyQt5 import QtCore, QtGui, Qt

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

from .configuration_view import ConfigurationDialog

active_thread_str = "There are {threads} running threads."


class MainView(QMainWindow):

    calendar_colors = {"data": "green", "sentiment": "blue"}

    def __init__(self, model, controller):
        super().__init__()

        self._model = model
        self._controller = controller

        self._load_window_properties()
        self._create_menu_bar()
        self._load_window_components()
        self._connect_window_components()

        self._init_window()

    def _load_window_properties(self):
        self.setWindowTitle("JABA")

    def _load_window_components(self):
        self.top_layout = QGridLayout()
        self.button_menu_layout = QVBoxLayout()

        self.combo_sentiment_algorithm = QComboBox(self)
        self.combo_sentiment_algorithm.addItem("nltk")
        self.combo_sentiment_algorithm.addItem("textblob")

        self.sentiment_plot_button = QPushButton("Plot Sentiment")
        self.analyze_date_button = QPushButton("Analyze Day")
        self.auto_scrap = QPushButton("Auto Scrap")

        self.button_menu_layout.addWidget(self.combo_sentiment_algorithm)
        self.button_menu_layout.addWidget(self.sentiment_plot_button)
        self.button_menu_layout.addWidget(self.analyze_date_button)
        self.button_menu_layout.addWidget(self.auto_scrap)

        self.button_menu_container = QWidget()
        self.button_menu_container.setLayout(self.button_menu_layout)

        self.calendar = QCalendarWidget(self)

        self.message_sample_scroll = QScrollArea()
        self.message_sample = QVBoxLayout()

        self.message_sample.addWidget(QLabel("Sample tweets from the day "))

        self.message_sample_scroll.setFixedWidth(600)
        self.message_sample_scroll.setWidgetResizable(True)
        self.message_sample_scroll.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff
        )
        self.message_sample_scroll.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn
        )

        self.message_sample_widget = QWidget()

        self.message_sample_widget.setLayout(self.message_sample)

        self.message_sample_scroll.setWidget(self.message_sample_widget)

        self.top_layout.addWidget(self.button_menu_container, 1, 1)
        self.top_layout.addWidget(self.calendar, 1, 2)

        self.top_container = QWidget()
        self.top_container.setLayout(self.top_layout)

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setYRange(-1, 1)

        self.graphWidgetHist = pg.PlotWidget()
        self.graphWidgetHist.setYRange(-0.1, 1.1)

        self.thread_count_label = QLabel(active_thread_str.format(threads="0"))

        self.center_layout = QVBoxLayout()
        self.center_layout.addWidget(self.top_container)
        self.center_layout.addWidget(self.graphWidget)
        self.center_layout.addWidget(self.graphWidgetHist)

        self.center_widget = QWidget()
        self.center_widget.setLayout(self.center_layout)

        self.vertical_split = QSplitter(QtCore.Qt.Horizontal)
        self.vertical_split.addWidget(self.center_widget)
        self.vertical_split.addWidget(self.message_sample_scroll)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.vertical_split)
        self.layout.addWidget(self.thread_count_label)

        self.container = QWidget()
        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)

        self.show()

    def _create_menu_bar(self):
        menu_bar = QMenuBar(self)

        self.open_parameters = QAction("&Parameters", self)
        self.open_parameters.triggered.connect(self.open_configuration)
        configuration_menu = QMenu("&Configuration", self)
        configuration_menu.addAction(self.open_parameters)

        help_menu = QMenu("&Help", self)
        menu_bar.addMenu(configuration_menu)
        menu_bar.addMenu(help_menu)

        self.setMenuBar(menu_bar)

    def _connect_window_components(self):

        self.sentiment_plot_button.clicked.connect(self.load_graph)

        self.analyze_date_button.clicked.connect(self.analyze_date)
        self.auto_scrap.clicked.connect(self.automatic_scrapper)

        self._model.thread_count_changed.connect(self.on_thread_count_changed)
        self._model.thread_count_changed.connect(self._controller.automatic_scrapper)

    def _init_window(self):
        self._reset_calendar_color()
        self._reset_sample()

    def _reset_calendar_color(self):
        date_colors = self._controller.get_date_properties()  # TODO Add this function

        cell_format = QtGui.QTextCharFormat()

        for date, status in date_colors:
            cell_format.setBackground(QtGui.QColor(self.calendar_colors[status]))

            if date.isValid():
                self.calendar.setDateTextFormat(date, cell_format)

    @pyqtSlot(int)
    def on_thread_count_changed(self, value):
        self.thread_count_label.setText(
            active_thread_str.format(threads=self._model.thread_count_str)
        )

    def automatic_scrapper(self):
        self._model.scrapping = True
        self._controller.automatic_scrapper()

    def analyze_date(self):
        date = self.calendar.selectedDate()
        self._controller.analyze_date(date.toPyDate())

    def _reset_sample(self):
        for i in reversed(range(self.message_sample.count())):
            self.message_sample.itemAt(i).widget().deleteLater()

        self.message_sample.addWidget(QLabel("Sample tweets from the day"))

    def load_graph(self):
        """
        Draw sentiment graph
        """

        date = self.calendar.selectedDate()
        algorithm = str(self.combo_sentiment_algorithm.currentText())

        (
            index,
            sentiment,
            dist_index,
            distribution,
        ) = self._controller.get_sentiment_plot_data(date, algorithm)
        sample = self._controller.get_message_sample_with_sentiment(date, algorithm)

        self.graphWidget.clear()
        self.graphWidget.plot(index, sentiment)
        self.graphWidgetHist.clear()
        self.graphWidgetHist.plot(dist_index, distribution)
        self.graphWidgetHist.setYRange(-0.1, max(distribution) + 0.1)

        self._reset_sample()
        for text, sentiment in sample:
            label = QLabel(f"{text} ({sentiment})")
            label.setWordWrap(True)
            self.message_sample.addWidget(label)

    def open_configuration(self):
        settings = self._controller.get_settings()
        configuration_dialog = ConfigurationDialog(self._controller)
        configuration_dialog.exec_()
