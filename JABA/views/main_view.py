import pyqtgraph as pg

from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from pyqtgraph import plot
from pyqtgraph import PlotWidget

from .configuration_view import ConfigurationDialog
from .component.QCoolContainer import QCoolContainer
from views.style.styles import *



active_thread_str = "There are {threads} running threads."

class MainView(QMainWindow):

    calendar_colors = {"data": "green", "sentiment": "blue"}

    plot_list = {}

    
    def __init__(self, model, controller):
        super().__init__()
        
        self._model = model
        self._controller = controller
        
        self.setStyleSheet(main_style)

        self._load_window_properties()
        self._load_window_components()
        self._connect_window_components()

        self._create_menu_bar()
        
        self._init_window()
        
    def _load_window_properties(self):
        self.setWindowTitle("My App")
        
    def _load_window_components(self):        
        self.top_layout = QGridLayout()
        

        self.button_menu_layout = QVBoxLayout()
        
        self.combo_sentiment_algorithm = QComboBox(self)


        # TODO Change this to factory dataGet
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
        

        self.message_sample = QVBoxLayout()

        self.message_sample_label = QLabel("Top Tweets")
        self.message_sample_label.setObjectName("SectionLabel")
        self.message_sample.addWidget(self.message_sample_label)
        self.message_sample_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.message_sample_label.setAlignment(Qt.AlignCenter)

        self.message_sample_table = QTableWidget()
        
        self.message_sample_table.setRowCount(1) 
        self.message_sample_table.setColumnCount(2)
        
        self.message_sample_table.setHorizontalHeaderItem(0, QTableWidgetItem('Text'))
        self.message_sample_table.setHorizontalHeaderItem(1, QTableWidgetItem('Sentiment'))
        self.message_sample_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch) 
        
        self.message_sample.addWidget(self.message_sample_table, stretch = 1)
        
        self.message_sample_widget = QWidget()
        self.message_sample_widget_l = QVBoxLayout()
        self.message_sample_widget.setLayout(self.message_sample_widget_l)
        self.message_sample_widget.setObjectName("Background")
        
        
        self.message_sample_w = QCoolContainer()
        self.message_sample_w.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        self.message_sample_w.setLayout(self.message_sample)
        
        self.message_sample_widget_l.addWidget(self.message_sample_w, stretch = 1)

        self.top_layout.addWidget(self.button_menu_container, 1, 1)
        self.top_layout.addWidget(self.calendar, 1, 2)

        self.top_container = QCoolContainer()
        self.top_container.setLayout(self.top_layout)
        self.top_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        pg.setConfigOption('background', 'w')

        self.center_layout = QVBoxLayout()

        self.plot_list_layout = QVBoxLayout()

        self.plot_L_widget = QWidget()
        self.plot_L_widget.setLayout(self.plot_list_layout)

        self.center_layout.addWidget(self.top_container)
        

        self.center_layout.addWidget(self.plot_L_widget)

        self.center_widget = QWidget()
        self.center_widget.setLayout(self.center_layout)
        self.center_widget.setObjectName("Background")
        
        self.vertical_split = QSplitter(QtCore.Qt.Horizontal)
        self.vertical_split.addWidget(self.center_widget)
        self.vertical_split.addWidget(self.message_sample_widget)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.vertical_split)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.container.setObjectName("Background")

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
        
        #self.graphWidgetBTC.scene().sigMouseMoved.connect(self.onMouseMoved)
        
    def _create_menu_bar(self):
        menu_bar = QMenuBar(self)
        
        self.save_plots_button = QAction("&Save Plot", self)
        self.save_plots_button.triggered.connect(self.save_plots_config)
        self.load_plots_button = QAction("&Load Plot", self)
        self.load_plots_button.triggered.connect(self.load_plots_config)
        plots_menu = QMenu("&Plots", self)
        plots_menu.addAction(self.save_plots_button)
        plots_menu.addAction(self.load_plots_button)
        

        self.open_parameters = QAction("&Parameters", self)
        self.open_parameters.triggered.connect(self.open_configuration)
        configuration_menu = QMenu("&Configuration", self)
        configuration_menu.addAction(self.open_parameters)

        
        menu_bar.addMenu(plots_menu)
        menu_bar.addMenu(configuration_menu)
        

        self.setMenuBar(menu_bar)


    def _init_window(self):
        self._reset_calendar_color()
        
        self.__refresh_table([])


    def _reset_calendar_color(self):
        date_colors = self._controller.get_date_properties() #TODO Add this function
        
        cell_format = QtGui.QTextCharFormat()
        
        for date, status in date_colors:
            cell_format.setBackground(QtGui.QColor(self.calendar_colors[status]))
            
            if date.isValid():
                self.calendar.setDateTextFormat(date, cell_format)
    
    @pyqtSlot(int)
    def on_thread_count_changed(self, value):
        self.statusBar().showMessage(
            active_thread_str.format(threads=self._model.thread_count_str)
        )

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
        
        
        self._controller.update_plots(
            self.calendar.selectedDate().toPyDate(),
            self.combo_sentiment_algorithm.currentText(),
        )
        
    def open_configure(self):
        id, name, widget = self._controller.open_configure()
        if id == None:
            return
        
        self.add_custom_plot( id, name, widget)
        
    
    def add_custom_plot(self, id, name, widget):
        
        self.plot_list[id] = widget
        
        temp_plot_w = QCoolContainer()
        temp_plot_l = QVBoxLayout()
        temp_plot_w.setLayout(temp_plot_l)
        
        name_label_temp = QLabel(name)
        name_label_temp.setObjectName("PlotLabel")
        name_label_temp.setAlignment(Qt.AlignCenter)
        
        temp_plot_l.addWidget(name_label_temp)
        temp_plot_l.addWidget(widget)
        
        self.plot_list_layout.addWidget(temp_plot_w)
    
    def _reset_sample(self):
        for i in reversed(range(self.message_sample.count())):
            self.message_sample.itemAt(i).widget().deleteLater()

        self.message_sample.addWidget(QLabel("Sample tweets from the day"))


    def open_configuration(self):
        settings = self._controller.get_settings()
        configuration_dialog = ConfigurationDialog(self._controller)
        configuration_dialog.exec_()
    
    def save_plots_config(self):
        fileName, _ = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        
        self._controller.save_plot_config(fileName)
        
    def load_plots_config(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
        
        plot_configs = self._controller.load_plot_config(fileName)
        
        for config in plot_configs:
            id, name, widget = self._controller.create_plot(config)
            self.add_custom_plot(id, name, widget)
