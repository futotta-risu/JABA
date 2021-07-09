import pyqtgraph as pg

from PyQt5 import Qt, QtCore, QtGui

from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import (QLabel, QPushButton)
from PyQt5.QtWidgets import (QVBoxLayout, QGridLayout)
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import (QMenu, QAction, QMenuBar)
from PyQt5.QtWidgets import (QSplitter, QSizePolicy)

from gui.view.configuration_view import ConfigurationDialog
from gui.component.QCoolContainer import QCoolContainer
from gui.component.table.SentimentTable import SentimentTable
from gui.component.calendar.CoolCalendar import CoolCalendar
from gui.component.label.CoolCenterTitleLabel import CoolCenterTitleLabel
from gui.component.CornerIconPanel import CornerIconPanel

from gui.component.style.styles import main_style


class MainView(QMainWindow):
    '''
        Main view from the program.

    '''

    calendar_colors = {"data": "#18BEBE", "sentiment": "blue"}

    layout_mode = 0
    layout_icons = [('Grid', 'media/icons/grid-layout.png'), ('Flow', 'media/icons/list-layout.png')]

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
        self.load_plots_config(real_filename='data/plotty/default_v1')

    def _load_window_properties(self):
        ''' Loads the windows properties such as title, icon or size '''
        self.setWindowTitle("Just Another Bitcoin Analyzer")

        # Iconos diseñados por Freepik from www.flaticon.es
        self.setWindowIcon(QtGui.QIcon('media/icons/pizza.png'))

        self.setMinimumSize(1200, 600)

        # Set the plot background as white
        pg.setConfigOption('background', 'w')

    def _load_window_components(self):
        ''' Loads the window components '''
        self.calendar = CoolCalendar()
        self.sample_table = SentimentTable()

        self.east_widget = QWidget()
        self.east_layout = QVBoxLayout()
        self.east_widget.setLayout(self.east_layout)
        self.east_widget.setObjectName("Background")

        self.calendar_container = QCoolContainer(self.calendar)
        self.calendar_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self.message_sample_layout = QVBoxLayout()
        self.message_sample_widget = QCoolContainer()
        self.message_sample_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.message_sample_widget.setLayout(self.message_sample_layout)

        self.message_sample_layout.addWidget(CoolCenterTitleLabel("Top Tweets"))
        self.message_sample_layout.addWidget(self.sample_table, stretch=1)

        self.east_layout.addWidget(self.calendar_container)
        self.east_layout.addWidget(self.message_sample_widget, stretch=1)

        self.center_widget = QWidget()
        self.center_layout = QVBoxLayout()
        self.center_widget.setLayout(self.center_layout)
        self.center_widget.setObjectName("Background")

        self.dashboard_label = QLabel("JABA Dashboard")
        self.dashboard_label.setAlignment(QtCore.Qt.AlignCenter)
        self.dashboard_label.setObjectName("DashboardLabel")

        self.view_mode_button = QPushButton("")
        self.view_mode_button.setObjectName("ViewModeButton")
        self.view_mode_button.setIcon(QIcon('media/icons/grid-layout.png'))

        self.plot_list_widget = QWidget()
        self.plot_list_layout = QVBoxLayout()
        self.plot_list_widget.setLayout(self.plot_list_layout)
        self.plot_list_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.header = CornerIconPanel(self.dashboard_label, self.view_mode_button)
        self.header.setObjectName('TitleWidgetHeader')

        self.title_widget = QCoolContainer(self.header)
        self.title_widget.setObjectName('TitleWidget')

        self.title_widget.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.title_widget.setStyleSheet('background-color: #18BEBE')

        self.center_layout.addWidget(self.title_widget)
        self.center_layout.addWidget(self.plot_list_widget, stretch=1)

        self.vertical_split = QSplitter(QtCore.Qt.Horizontal)
        self.vertical_split.setObjectName("Background")

        self.vertical_split.addWidget(self.center_widget)
        self.vertical_split.setStretchFactor(0, 3)

        self.vertical_split.addWidget(self.east_widget)
        self.vertical_split.setStretchFactor(1, 1)

        self.setCentralWidget(self.vertical_split)

        self.show()

    def resizeEvent(self, event):
        self.sample_table.resizeRowsToContents()
        QtGui.QMainWindow.resizeEvent(self, event)

    def __refresh_table(self, data):
        ''' Refresh the table with new data '''
        while (self.sample_table.rowCount() > 1):
            self.sample_table.removeRow(1)

        for text, sentiment in data:
            self.sample_table.addRow(text, sentiment)

        self.sample_table.resizeRowsToContents()

    def _connect_window_components(self):
        self.calendar.clicked.connect(self.update_plot)
        self.view_mode_button.clicked.connect(self._change_view_mode)

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
        date_colors = self._controller.get_date_properties()  # TODO Add this function

        cell_format = QtGui.QTextCharFormat()

        for date, status in date_colors:
            cell_format.setForeground(QtGui.QColor(self.calendar_colors[status]))

            temp_font = QtGui.QFont()
            temp_font.setBold(True)
            cell_format.setFont(temp_font)
            if date.isValid():
                self.calendar.setDateTextFormat(date, cell_format)

    def automatic_scrapper(self):
        self._controller.startAutoScrapWorker()

    def analyze_date(self):
        date = self.calendar.selectedDate()
        self._controller.startScrapWorker(date=date.toPyDate())

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

        self.add_custom_plot(id, name, widget)

    def _refresh_plot_widgets(self):
        configs = self._controller.get_plots()

        for config in configs:
            config['widget'].setParent(None)

        QWidget().setLayout(self.plot_list_layout)

        if self.layout_mode == 0:
            self.plot_list_layout = QVBoxLayout()
        else:
            self.plot_list_layout = QGridLayout()

        self.plot_list_widget.setLayout(self.plot_list_layout)

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
        name_label_temp.setAlignment(QtCore.Qt.AlignCenter)

        delete_button = QPushButton("")
        delete_button.resize(25, 40)
        delete_button.setObjectName("DeleteButton")
        delete_button.clicked.connect(
            lambda _, dtype=id: self._delete_plot(dtype))

        temp_plot_l.addWidget(CornerIconPanel(name_label_temp, delete_button))
        temp_plot_l.addWidget(widget)

        if self.layout_mode == 0:
            self.plot_list_layout.addWidget(temp_plot_w)
        else:
            count = self.plot_list_layout.count()
            self.plot_list_layout.addWidget(temp_plot_w, count // 2, count % 2)

    def _delete_plot(self, id):
        self._controller.delete_plot(id)
        self._refresh_plot_widgets()

    def _change_view_mode(self):

        self.layout_mode = (self.layout_mode + 1) % len(self.layout_icons)
        self.view_mode_button.setIcon(QIcon(self.layout_icons[self.layout_mode][1]))

        self._refresh_plot_widgets()

    def open_configuration(self):
        configuration_dialog = ConfigurationDialog(self._controller)
        configuration_dialog.exec_()

    def save_plots_config(self):
        fileName, _ = QtGui.QFileDialog.getSaveFileName(self, 'Save File')

        self._controller.save_plot_config(fileName)

    def load_plots_config(self, real_filename=None):
        if real_filename:
            fileName = real_filename
        else:
            fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)")

        plot_configs = self._controller.load_plot_config(fileName)

        for config in plot_configs:
            id, name, widget = self._controller.create_plot(config)
            self.add_custom_plot(id, name, widget)
