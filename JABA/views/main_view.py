import pyqtgraph as pg

from PyQt5 import Qt, QtCore, QtGui, QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from pyqtgraph import plot
from pyqtgraph import PlotWidget

from .configuration_view import ConfigurationDialog
from .component.QCoolContainer import QCoolContainer
from .component.FlowLayout import FlowLayout

from .component.BorderLayout import BorderLayout
from views.style.styles import *



active_thread_str = "There are {threads} running threads."

class MainView(QMainWindow):
    '''
        Main view from the program.
        
        
    '''
    calendar_colors = {"data": "#18BEBE", "sentiment": "blue"}

    plot_list = {}

    
    def __init__(self, model, controller):
        super().__init__()
        
        self.view_mode = 'Flow'
        
        self._model = model
        self._controller = controller
        
        self.setStyleSheet(main_style)

        self._load_window_properties()
        self._load_window_components()
        self._connect_window_components()

        self._create_menu_bar()
        
        self._init_window()
        self.load_plots_config(real_filename = 'data/plotty/default_v1')
        
    def _load_window_properties(self):
        self.setWindowTitle("Just Another Bitcoin Analyzer")
        
    def _load_window_components(self):        
        self.top_layout = QHBoxLayout()
        
        #Iconos diseñados por Freepik from www.flaticon.es
        self.setWindowIcon(QtGui.QIcon('media/icons/pizza.png'))
        
        self.calendar = QCalendarWidget(self)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setHorizontalHeaderFormat(0)
        self.top_layout.addWidget(self.calendar)

        self.top_container = QCoolContainer()
        self.top_container.setLayout(self.top_layout)
        self.top_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
        

        self.message_sample = QVBoxLayout()

        self.message_sample_label = QLabel("Top Tweets")
        self.message_sample_label.setObjectName("SectionLabel")
        self.message_sample.addWidget(self.message_sample_label)
        self.message_sample_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.message_sample_label.setAlignment(Qt.AlignCenter)

        self.message_sample_table = QTableWidget()
        self.message_sample_table.verticalHeader().setVisible(False)
        self.message_sample_table.setRowCount(1) 
        self.message_sample_table.setColumnCount(2)
        self.message_sample_table.setShowGrid(False)
        
        table_header_font = self.message_sample_table.horizontalHeader().font()
        table_header_font.setPointSize(10)
        table_header_font.setBold(True)
        self.message_sample_table.horizontalHeader().setFont( table_header_font )
        
        self.message_sample_table.setHorizontalHeaderItem(0, QTableWidgetItem('Text'))
        self.message_sample_table.setHorizontalHeaderItem(1, QTableWidgetItem('Sentiment'))
        self.message_sample_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch) 
        
        self.message_sample_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.message_sample_table.setFocusPolicy(Qt.NoFocus);
        
        self.message_sample.addWidget(self.message_sample_table, stretch = 1)
        
        self.message_sample_widget = QWidget()
        self.message_sample_widget_l = QVBoxLayout()
        self.message_sample_widget.setLayout(self.message_sample_widget_l)
        self.message_sample_widget.setObjectName("Background")
        
        
        self.message_sample_w = QCoolContainer()
        self.message_sample_w.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        self.message_sample_w.setLayout(self.message_sample)
        
        self.message_sample_widget_l.addWidget(self.top_container)
        self.message_sample_widget_l.addWidget(self.message_sample_w, stretch = 1)

        
        
        pg.setConfigOption('background', 'w')

        self.center_layout = QVBoxLayout()

        self.plot_list_layout = QVBoxLayout()

        self.plot_L_widget = QWidget()
        self.plot_L_widget.setLayout(self.plot_list_layout)
        self.plot_L_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        self.dashboard_container_w = QCoolContainer()
        self.dashboard_container_l = QHBoxLayout()
        self.dashboard_container_w.setLayout(self.dashboard_container_l)
        
        self.dashboard_container_w.setAttribute(Qt.WA_StyledBackground, True)
        self.dashboard_container_w.setStyleSheet('''
            background-color: #18BEBE;
            border-radius: 8px;
            margin: 0px 8px 0px 8px;
        ''')
        
        self.dashboard_label = QLabel("JABA Dashboard")
        
        self.dashboard_label.setAlignment(Qt.AlignCenter)
        self.dashboard_label.setObjectName("DashboardLabel")
        
        self.view_mode_button = QPushButton("")
        self.view_mode_button.setObjectName("ViewModeButton")
        self.view_mode_button.setIcon(QIcon('media/icons/grid-layout.png'))
        self.view_mode_button.clicked.connect(self._change_view_mode)
        
        
        self.dashboard_header = QSplitter(QtCore.Qt.Horizontal)
        self.dashboard_header.setObjectName("PlotHeaderSplit")
        
        self.dashboard_header.addWidget(self.dashboard_label)
        self.dashboard_header.addWidget(self.view_mode_button)
        
        self.dashboard_header.setStretchFactor(0,3)
        self.dashboard_header.setStretchFactor(1,0)
        
        self.dashboard_container_l.addWidget(self.dashboard_header)
        
        self.center_layout.addWidget(self.dashboard_container_w)
        self.center_layout.addWidget(self.plot_L_widget, stretch=1)

        self.center_widget = QWidget()
        self.center_widget.setLayout(self.center_layout)
        self.center_widget.setObjectName("Background")
        
        self.vertical_split = QSplitter(QtCore.Qt.Horizontal)
        self.vertical_split.addWidget(self.center_widget)
        self.vertical_split.addWidget(self.message_sample_widget)
        
        self.vertical_split.setStretchFactor(0,3)
        self.vertical_split.setStretchFactor(1,1)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.vertical_split)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.container.setObjectName("Background")

        self.setCentralWidget(self.container)
        
        self.setMinimumSize(1200, 600)
        
        self.show()
    
    def resizeEvent(self, event):
        self.message_sample_table.resizeRowsToContents()
        QtGui.QMainWindow.resizeEvent(self, event)

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
            
            temp_font = sentiment_item.font()
            temp_font.setBold(True)
            temp_font.setPointSize(12)
            sentiment_item.setFont(temp_font)
            
            temp_color = QtGui.QColor(
                    100 + (1 - sentiment) / 2 * 155,
                    100 + (1 + sentiment) / 2 * 155,
                    100 + (1 + sentiment) / 2 * 155
                ) 
            sentiment_item.setForeground(QtGui.QBrush(temp_color))
            
            self.message_sample_table.setItem(
                rowPosition-1,
                1,
                sentiment_item
            )
        self.message_sample_table.resizeRowsToContents()
        
    def _connect_window_components(self):
        self._model.thread_count_changed.connect(self.on_thread_count_changed)
        self._model.thread_count_changed.connect(
            self._controller.automatic_scrapper)
        self.calendar.clicked.connect(self.update_plot)
        #self.graphWidgetBTC.scene().sigMouseMoved.connect(self.onMouseMoved)
        
    def _create_menu_bar(self):
        menu_bar = QMenuBar(self)
        
        self.scrap_date_button = QAction("&Scrap Date", self)
        self.scrap_date_button.triggered.connect(self.analyze_date)
        self.auto_scrap_date_button = QAction("&Auto Scrap", self)
        self.auto_scrap_date_button.triggered.connect(self.automatic_scrapper)
        data_menu = QMenu("&Data", self)
        data_menu.addAction(self.scrap_date_button)
        data_menu.addAction(self.auto_scrap_date_button)
        
        self.save_plots_button = QAction("&Save Plot", self)
        self.save_plots_button.triggered.connect(self.save_plots_config)
        self.load_plots_button = QAction("&Load Plot", self)
        self.load_plots_button.triggered.connect(self.load_plots_config)
        self.add_plot_button = QAction("&Add Plot", self)
        self.add_plot_button.triggered.connect(self.open_configure)
        plots_menu = QMenu("&Plots", self)
        plots_menu.addAction(self.add_plot_button)
        plots_menu.addAction(self.save_plots_button)
        plots_menu.addAction(self.load_plots_button)
        

        self.open_parameters = QAction("&Parameters", self)
        self.open_parameters.triggered.connect(self.open_configuration)
        configuration_menu = QMenu("&Configuration", self)
        configuration_menu.addAction(self.open_parameters)

        menu_bar.addMenu(data_menu)
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
            cell_format.setForeground(QtGui.QColor(self.calendar_colors[status]))
            
            temp_font = QtGui.QFont()
            temp_font.setBold(True)
            cell_format.setFont(temp_font)
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
        algorithm = str(self._controller.get_analysis_method())
        
        sample = self._controller.get_message_sample_with_sentiment(
            date, algorithm)
        
        self.__refresh_table(sample)
        
        
        self._controller.update_plots(
            self.calendar.selectedDate().toPyDate(),
            self._controller.get_analysis_method(),
        )
        
    def open_configure(self):
        id, name, widget = self._controller.open_configure()
        if id is None:
            return
        
        self.add_custom_plot( id, name, widget)
        
    
    def _refresh_plot_widgets(self):
        configs = self._controller.get_plots()
        
        for config in configs: 
            config['widget'].setParent(None)
            
        QWidget().setLayout(self.plot_list_layout)
        
        if self.view_mode == 'Flow':
            self.plot_list_layout = QVBoxLayout()
        else:
            self.plot_list_layout = QGridLayout()
            
        self.plot_L_widget.setLayout(self.plot_list_layout)
        
        
        for config in configs:
            self.add_custom_plot(config["id"], config["config"].name, config["widget"])
    
    def add_custom_plot(self, id, name, widget):
        '''
            Parameters:
                layout: Grid or Flow
        '''
        self.plot_list[id] = widget
        
        temp_plot_w = QCoolContainer()
        temp_plot_l = QVBoxLayout()
        temp_plot_w.setLayout(temp_plot_l)
        
        name_label_temp = QLabel(name)
        name_label_temp.setObjectName("PlotLabel")
        name_label_temp.setAlignment(Qt.AlignCenter)
        
        delete_button = QPushButton("")
        delete_button.resize(25,40)
        delete_button.setObjectName("DeleteButton")
        delete_button.clicked.connect(
                lambda _, dtype=id : self._delete_plot(dtype))
        
        v_split = QSplitter(QtCore.Qt.Horizontal)
        v_split.setObjectName("PlotHeaderSplit")
        v_split.addWidget(name_label_temp)
        v_split.addWidget(delete_button)
        v_split.setStretchFactor(0,3)
        v_split.setStretchFactor(1,0)
        
        temp_plot_l.addWidget(v_split)
        temp_plot_l.addWidget(widget)
        
        if self.view_mode == 'Flow':
            self.plot_list_layout.addWidget(temp_plot_w)
        else:
            count = self.plot_list_layout.count()
            self.plot_list_layout.addWidget(temp_plot_w, count//2, count%2)
            
    def _delete_plot(self, id):
        self._controller.delete_plot(id)
        self._refresh_plot_widgets()
    
    def _reset_sample(self):
        for i in reversed(range(self.message_sample.count())):
            self.message_sample.itemAt(i).widget().deleteLater()

        self.message_sample.addWidget(QLabel("Sample tweets from the day"))
    
    def _change_view_mode(self):
        if self.view_mode == 'Grid':
            self.view_mode = 'Flow'
            self.view_mode_button.setIcon(QIcon('media/icons/grid-layout.png'))
        else:
            self.view_mode = 'Grid'
            self.view_mode_button.setIcon(QIcon('media/icons/list-layout.png'))
            
            
        self._refresh_plot_widgets()
        
        
    def open_configuration(self):
        settings = self._controller.get_settings()
        configuration_dialog = ConfigurationDialog(self._controller)
        configuration_dialog.exec_()
    
    def save_plots_config(self):
        fileName, _ = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        
        self._controller.save_plot_config(fileName)
        
    def load_plots_config(self, real_filename = None):
        if real_filename:
            fileName = real_filename
        else:
            fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)")
        
        plot_configs = self._controller.load_plot_config(fileName)
        
        for config in plot_configs:
            id, name, widget = self._controller.create_plot(config)
            self.add_custom_plot(id, name, widget)
    
    