import pyqtgraph as pg


import seaborn as sns
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QRunnable
from PyQt5.QtCore import QThreadPool
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QWidget

from pyqtgraph import plot
from pyqtgraph import PlotWidget

from .configuration_view import ConfigurationDialog


active_thread_str = "There are {threads} running threads."


class MainView(QMainWindow):

    calendar_colors = {"data": "green", "sentiment": "blue"}

    plot_list = {}

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

        self.combo_sentiment_algorithm.addItems(["nltk", "textblob"])

        self.analyze_date_button = QPushButton("Analyze Day")
        self.auto_scrap = QPushButton("Auto Scrap")
        self.update_plot_button = QPushButton("Update Plot")
        self.configure_button = QPushButton("Add Plot")


        self.button_menu_layout.addWidget(self.combo_sentiment_algorithm)
        self.button_menu_layout.addWidget(self.analyze_date_button)
        self.button_menu_layout.addWidget(self.auto_scrap)

        self.button_menu_layout.addWidget(self.update_plot_button)
        self.button_menu_layout.addWidget(self.configure_button)


        self.button_menu_container = QWidget()
        self.button_menu_container.setLayout(self.button_menu_layout)

        self.calendar = QCalendarWidget(self)

        self.message_sample_scroll = QScrollArea()
        self.message_sample = QVBoxLayout()

        self.message_sample.addWidget(QLabel("Sample tweets from the day "))

        self.message_sample_table = QTableWidget()
        
        
        
        self.message_sample_table.setRowCount(1) 
        self.message_sample_table.setColumnCount(2)
        
        self.message_sample_table.setHorizontalHeaderItem(0, QTableWidgetItem('Text'))
        self.message_sample_table.setHorizontalHeaderItem(1, QTableWidgetItem('Sentiment'))
        self.message_sample_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch) 
        
        self.message_sample.addWidget(self.message_sample_table)
        

        self.message_sample_scroll.setFixedWidth(600)
        self.message_sample_scroll.setWidgetResizable(True)
        self.message_sample_scroll.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.message_sample_scroll.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)

        self.message_sample_widget = QWidget()

        self.message_sample_widget.setLayout(self.message_sample)

        self.message_sample_scroll.setWidget(self.message_sample_widget)

        self.top_layout.addWidget(self.button_menu_container, 1, 1)
        self.top_layout.addWidget(self.calendar, 1, 2)

        self.top_container = QWidget()
        self.top_container.setLayout(self.top_layout)

        self.graphWidgetBTC = pg.PlotWidget()


        self.combo_plotType = QComboBox(self)
        self.combo_plotType.addItem("boxplot")
        self.combo_plotType.addItem("violinplot")

        self.fig = Figure()
        self.axes = self.fig.add_subplot()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Expanding)
        self.canvas.updateGeometry()

        self.thread_count_label = QLabel(active_thread_str.format(threads="0"))

        self.center_layout = QVBoxLayout()

        self.thread_count_label = QLabel(active_thread_str.format(threads="0"))

        self.plot_list_layout = QVBoxLayout()

        self.plot_L_widget = QWidget()
        self.plot_L_widget.setLayout(self.plot_list_layout)

        self.center_layout.addWidget(self.top_container)
        

        self.center_layout.addWidget(self.plot_L_widget)

        self.center_layout.addWidget(self.graphWidgetBTC)
        self.center_layout.addWidget(self.combo_plotType)
        self.center_layout.addWidget(self.canvas)


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


    def __refresh_table(self, data):
        while (self.message_sample_table.rowCount() > 1):
            self.message_sample_table.removeRow(1)
        
        for text, sentiment in data:
            rowPosition = self.message_sample_table.rowCount()
            self.message_sample_table.insertRow(rowPosition)
            
            self.message_sample_table.setItem(
                rowPosition-1, 
                0,
                QtGui.QTableWidgetItem(text)
            )
            
            sentiment_item = QTableWidgetItem("{:.2f}".format(sentiment))
            sentiment_item.setTextAlignment(QtCore.Qt.AlignCenter)
            sentiment_item.setBackground(
                QtGui.QColor(
                    (1 - sentiment) / 2 * 255,
                    (1 + sentiment) / 2 * 255,
                    0
                ) 
            )
            
            
            self.message_sample_table.setItem(
                rowPosition-1,
                1,
                sentiment_item
            )
        
    def _connect_window_components(self):
        self.analyze_date_button.clicked.connect(self.analyze_date)
        self.auto_scrap.clicked.connect(self.automatic_scrapper)
        self.configure_button.clicked.connect(self.open_configure)
        self.update_plot_button.clicked.connect(self.update_plot)
        self._model.thread_count_changed.connect(self.on_thread_count_changed)
        self._model.thread_count_changed.connect(
            self._controller.automatic_scrapper)
        
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


    def _init_window(self):
        self._reset_calendar_color()
        
        self.__refresh_table([])


    def _reset_calendar_color(self):
        date_colors = self._controller.get_date_properties(
        )  # TODO Add this function

        cell_format = QtGui.QTextCharFormat()

        for date, status in date_colors:
            cell_format.setBackground(
                QtGui.QColor(self.calendar_colors[status]))

            if date.isValid():
                self.calendar.setDateTextFormat(date, cell_format)

    @pyqtSlot(int)
    def on_thread_count_changed(self, value):
        self.thread_count_label.setText(
            active_thread_str.format(threads=self._model.thread_count_str))

    def automatic_scrapper(self):
        self._model.scrapping = True
        self._controller.automatic_scrapper()

    def analyze_date(self):
        date = self.calendar.selectedDate()
        self._controller.analyze_date(date.toPyDate())


    def update_plot(self):
        date = self.calendar.selectedDate()
        algorithm = str(self.combo_sentiment_algorithm.currentText())
        
        sample = self._controller.get_message_sample_with_sentiment(
            date, algorithm)
        
        self.__refresh_table(sample)
        
        self.load_btc_price_graph(date)
        
        self._controller.update_plots(
            self.calendar.selectedDate().toPyDate(),
            self.combo_sentiment_algorithm.currentText(),
        )
        
    def open_configure(self):
        id, widget = self._controller.open_configure()
        self.plot_list[id] = widget
        self.plot_list_layout.addWidget(widget)

    def _reset_sample(self):
        for i in reversed(range(self.message_sample.count())):
            self.message_sample.itemAt(i).widget().deleteLater()

        self.message_sample.addWidget(QLabel("Sample tweets from the day"))

    def load_btc_price_graph(self, date):
        """
        Draw btc price graph in a given date
        """
        plotX = str("open")
        plotType = str(self.combo_plotType.currentText())
        (
            index_BTC, price_BTC
        ) = self._controller.get_btc_price_plot_data(date, plotX)
        
        self.graphWidgetBTC.clear()
        self.graphWidgetBTC.plot(range(1,1+len(index_BTC)), price_BTC)
        
        btc_df = self._controller.get_btc_price_subdf(date)
        self.axes.clear()

        if plotType == "boxplot":
            sns.boxplot(x=plotX, data=btc_df, ax=self.axes)
        elif plotType == "violinplot":
            sns.violinplot(x=plotX, data=btc_df, ax=self.axes)

        self.fig.canvas.draw_idle()

    def open_configuration(self):
        settings = self._controller.get_settings()
        configuration_dialog = ConfigurationDialog(self._controller)
        configuration_dialog.exec_()

