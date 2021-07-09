import pandas as pd

from PyQt5 import Qt

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import (QLabel, QPushButton)
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout)
from PyQt5.QtWidgets import (QGridLayout, QFormLayout)
from PyQt5.QtWidgets import (QComboBox, QLineEdit)

from service.visualization.maps.MapFactory import MapFactory
from service.visualization.PlotConfiguration import PlotConfiguration

from gui.component.FlowLayout import FlowLayout
from gui.component.QCoolContainer import QCoolContainer
from gui.component.style.styles import main_style

from model.ScrapModel import ScrapModel
from model.ModelFactory import createModelFrame


class QFormLabel(QLabel):
    def __init__(self, text):
        super(QFormLabel, self).__init__(text)
        self.setObjectName("FormLabel")


class PlotConfigure(QDialog):
    def __init__(self, parent):
        super(PlotConfigure, self).__init__()

        self.initial_frame = pd.DataFrame()
        self.final_frame = self.initial_frame.copy(deep=True)

        self.__saved = False
        self.__configuration = None
        self.map_list = []

        self.attrs_types = {}
        self.attrs_widgets = {}

        self.loadWidget()
        self.__load_data_model()

        self.__load_frame_map()

    def loadWidget(self):

        self.main_layout = QVBoxLayout()

        self.setStyleSheet(main_style)

        self.bottom_pane_l = QHBoxLayout()
        self.bottom_pane_w = QWidget()
        self.bottom_pane_w.setLayout(self.bottom_pane_l)

        self.closeButton = QPushButton("Save")
        self.closeButton.clicked.connect(lambda: self.__save_and_exit())

        self.bottom_pane_l.addWidget(self.closeButton)

        self.configureMenu_l = QGridLayout()
        for i in range(1, 4):
            self.configureMenu_l.setColumnStretch(i, 1)
        self.configureMenu_w = QWidget()
        self.configureMenu_w.setLayout(self.configureMenu_l)

        self.config_menu_1_l = QVBoxLayout()
        self.config_menu_1_w = QWidget()
        self.config_menu_1_w.setLayout(self.config_menu_1_l)
        self.configureMenu_l.addWidget(self.config_menu_1_w, 1, 1)

        self.plot_name_l = QFormLayout()
        self.plot_name_w = QCoolContainer()
        self.plot_name_w.setLayout(self.plot_name_l)
        self.name_edit = QLineEdit()
        self.name_edit.setObjectName("NameEdit")
        self.plot_name_l.addRow(QFormLabel("Name"), self.name_edit)

        self.config_menu_1_l.addWidget(self.plot_name_w)

        self.data_model_l = QHBoxLayout()
        self.data_model_w = QCoolContainer()
        self.data_model_w.setLayout(self.data_model_l)

        self.data_model_combobox = QComboBox()

        model_name = [
            model_class.name for model_class in ScrapModel.__subclasses__()
        ]

        self.data_model_combobox.addItems(model_name)

        self.data_model_load = QPushButton("Load Model")

        self.data_model_l.addWidget(QFormLabel("Data Model"))
        self.data_model_l.addWidget(self.data_model_combobox)
        self.data_model_l.addWidget(self.data_model_load)

        self.config_menu_1_l.addWidget(self.data_model_w)

        self.model_desc_l = QVBoxLayout()
        self.model_desc_w = QCoolContainer()
        self.model_desc_w.setLayout(self.model_desc_l)

        self.model_desc_label = QFormLabel("Model Description")
        self.model_desc_label.setAlignment(Qt.AlignCenter)
        self.model_desc_l.addWidget(self.model_desc_label)

        self.model_desc_name_l = QHBoxLayout()
        self.model_desc_name_w = QWidget()
        self.model_desc_name_w.setLayout(self.model_desc_name_l)
        self.initial_frame_label = QFormLabel("Initial Frame")
        self.initial_frame_label.setAlignment(Qt.AlignCenter)
        self.final_frame_label = QFormLabel("Final Frame")
        self.final_frame_label.setAlignment(Qt.AlignCenter)
        self.model_desc_name_l.setContentsMargins(0, 0, 0, 0)

        self.model_desc_name_l.addWidget(self.initial_frame_label)
        self.model_desc_name_l.addWidget(self.final_frame_label)

        self.model_desc_inner_l = QHBoxLayout()
        self.model_desc_inner_w = QWidget()
        self.model_desc_inner_w.setLayout(self.model_desc_inner_l)
        self.model_desc_inner_l.setContentsMargins(5, 0, 5, 5)

        self.model_initial_desc_l = QGridLayout()
        self.model_initial_desc_w = QWidget()
        self.model_initial_desc_w.setLayout(self.model_initial_desc_l)
        self.model_desc_inner_l.addWidget(self.model_initial_desc_w)

        self.model_initial_desc_w.setObjectName("InnerModelDescription1m83b9s")

        self.model_final_desc_l = QGridLayout()
        self.model_final_desc_w = QWidget()
        self.model_final_desc_w.setLayout(self.model_final_desc_l)
        self.model_desc_inner_l.addWidget(self.model_final_desc_w)

        self.model_desc_l.addWidget(self.model_desc_name_w)
        self.model_desc_l.addWidget(self.model_desc_inner_w)

        self.config_menu_1_l.addWidget(self.model_desc_w)

        self.dataPick_w = QCoolContainer()
        self.dataPick_l = QFormLayout()
        self.dataPick_w.setLayout(self.dataPick_l)

        self.index_combo = QComboBox()
        self.data_combo = QComboBox()

        self.dataPick_l.addRow(QFormLabel("Index"), self.index_combo)
        self.dataPick_l.addRow(QFormLabel("Data"), self.data_combo)

        self.config_menu_1_l.addWidget(self.dataPick_w)

        self.mapping_hist_p_w = QCoolContainer()
        self.mapping_hist_p_l = QVBoxLayout()
        self.mapping_hist_p_w.setLayout(self.mapping_hist_p_l)

        self.mapping_hist_label = QFormLabel("Mapping History")
        self.mapping_hist_label.setAlignment(Qt.AlignCenter)
        self.mapping_hist_p_l.addWidget(self.mapping_hist_label)

        self.mapping_hist_l = QVBoxLayout()
        self.mapping_hist_w = QWidget()
        self.mapping_hist_w.setLayout(self.mapping_hist_l)
        self.mapping_hist_p_l.addWidget(self.mapping_hist_w)
        self.config_menu_1_l.addWidget(self.mapping_hist_p_w)

        self.config_menu_2_l = FlowLayout()
        self.config_menu_2_w = QCoolContainer()
        self.config_menu_2_w.setLayout(self.config_menu_2_l)
        self.config_menu_2_w.setContentsMargins(10, 10, 10, 10)
        self.configureMenu_l.addWidget(self.config_menu_2_w, 1, 2)

        self.config_menu_3_l = QVBoxLayout()
        self.config_menu_3_w = QCoolContainer()
        self.config_menu_3_w.setLayout(self.config_menu_3_l)
        self.configureMenu_l.addWidget(self.config_menu_3_w, 1, 3)

        self.variable_pick = QComboBox()
        self.config_menu_3_l.addWidget(self.variable_pick)

        self.attr_edit_l = QFormLayout()
        self.attr_edit_w = QWidget()
        self.attr_edit_w.setLayout(self.attr_edit_l)
        self.config_menu_3_l.addWidget(self.attr_edit_w)

        self.save_map_button = QPushButton("Save")
        self.config_menu_3_l.addWidget(self.save_map_button)

        self.main_layout.addWidget(self.configureMenu_w)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.bottom_pane_w)

        self.data_model_load.clicked.connect(lambda: self.__load_data_model())

        self.setLayout(self.main_layout)

    def __load_map_history(self):

        for i in reversed(range(self.mapping_hist_l.count())):
            self.mapping_hist_l.itemAt(i).widget().setParent(None)

        for fmap in self.map_list:
            self.mapping_hist_l.addWidget(QLabel(fmap.getName()))

    def __load_frame_descriptions(self):
        self.__refresh_combo()

        intial_types = self.initial_frame.dtypes.reset_index(name="type")

        intial_types["type"] = intial_types["type"].astype("str")

        for i in reversed(range(self.model_initial_desc_l.count())):
            self.model_initial_desc_l.itemAt(i).widget().setParent(None)

        for index, row in intial_types.iterrows():
            self.model_initial_desc_l.addWidget(QLabel(str(row["index"])),
                                                index + 1, 1)
            self.model_initial_desc_l.addWidget(QLabel(str(row["type"])),
                                                index + 1, 2)

        final_types = self.final_frame.dtypes.reset_index(name="type")

        final_types["type"] = final_types["type"].astype("str")

        for i in reversed(range(self.model_final_desc_l.count())):
            self.model_final_desc_l.itemAt(i).widget().setParent(None)

        for index, row in final_types.iterrows():
            self.model_final_desc_l.addWidget(QLabel(str(row["index"])),
                                              index + 1, 1)
            self.model_final_desc_l.addWidget(QLabel(str(row["type"])),
                                              index + 1, 2)

    def __load_frame_map(self):

        for map_function in (MapFactory()).getMapList():
            map_button = QPushButton(map_function.getName())
            map_button.setObjectName("MapButton")

            map_button.clicked.connect(
                lambda _, dtype=map_function.__name__: self.__load_map_config(dtype))

            self.config_menu_2_l.addWidget(map_button)

    def __refresh_combo(self):
        self.index_combo.clear()
        self.data_combo.clear()

        self.index_combo.addItem("Range Index")
        self.index_combo.addItems(self.final_frame.columns.to_list())

        self.data_combo.addItems(self.final_frame.columns.to_list())

    def __get_attrs(self):
        temp_attrs = {}
        for key in self.attrs_widgets:
            if self.attrs_types[key][0] == 'Text':
                temp_attrs[key] = self.attrs_widgets[key].text()
            elif self.attrs_types[key][0] == 'Variable':
                temp_attrs[key] = self.attrs_widgets[key].currentText()

        return temp_attrs

    def __load_map_config(self, map_function):
        self.variable_pick.clear()
        self.variable_pick.addItems(self.final_frame.columns.to_list())

        # We don't check the Exception since it happends if not connected to anything
        try:
            self.save_map_button.clicked.disconnect()
        except Exception:
            pass

        strategy = MapFactory()

        self.attrs_types = strategy.getAttrsWithTypes(map_function)
        self.attrs_widgets = {}

        for i in reversed(range(self.attr_edit_l.count())):
            self.attr_edit_l.itemAt(i).widget().setParent(None)

        for key in self.attrs_types:
            if self.attrs_types[key][0] == 'Text':
                temp_widget = QLineEdit()
                temp_widget.setText(self.attrs_types[key][1])
            elif self.attrs_types[key][0] == 'Variable':
                temp_widget = QComboBox()
                temp_widget.addItems(self.final_frame.columns.to_list())

            self.attrs_widgets[key] = temp_widget
            self.attr_edit_l.addRow(QLabel(key), temp_widget)

        self.save_map_button.clicked.connect(
            lambda: self.transform_map(map_function))

    def transform_map(self, map_function):
        strategy = MapFactory()

        args = self.__get_attrs()
        args["variable"] = self.variable_pick.currentText()

        self.final_frame, fmap = strategy.apply(map_function, self.final_frame,
                                                args)

        self.map_list += [fmap]

        self.__load_frame_descriptions()
        self.__load_map_history()

    def __load_data_model(self):
        self.initial_frame = createModelFrame(
            self.data_model_combobox.currentText())
        self.final_frame = self.initial_frame.copy(deep=True)
        self.__load_frame_descriptions()

    def getPlotConfiguration(self):
        return self.__configuration

    def is_saved(self):
        return self.__saved

    def __save_and_exit(self):
        self.__configuration = PlotConfiguration(
            self.name_edit.text(),
            self.initial_frame,
            self.final_frame,
            self.map_list,
            self.data_model_combobox.currentText(),
            self.index_combo.currentText(),
            self.data_combo.currentText(),
        )

        self.__saved = True

        self.close()
