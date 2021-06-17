from PyQt5.QtWidgets import QDialog,  QWidget
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout,  QScrollArea, QSplitter
from PyQt5.QtWidgets import QPushButton, QFileDialog, QCalendarWidget, QLabel, QComboBox
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5 import QtCore, QtGui, Qt

from model.modelFactory import createModelFrame
from service.visualization.types.maps.MapFactory import MapFactory
from service.visualization.types.PlotConfiguration import PlotConfiguration

import pandas as pd

class PlotConfigure(QDialog):
       
    def __init__(self, parent):
        super(PlotConfigure, self).__init__()
        
        self.initial_frame = pd.DataFrame()
        self.final_frame = self.initial_frame.copy(deep = True)
        
        self.__saved = False
        self.__configuration = None
        self.map_list = []
        
        self.loadWidget()
        self.__load_data_model()
        
        self.__load_frame_map()
        
        
    
    def loadWidget(self):
        
        self.main_layout = QVBoxLayout()
        
        self.bottom_pane_l = QHBoxLayout()
        self.bottom_pane_w = QWidget()
        self.bottom_pane_w.setLayout(self.bottom_pane_l)
        
        self.closeButton = QPushButton("Save")
        self.closeButton.clicked.connect(lambda : self.__save_and_exit())
        
        self.bottom_pane_l.addWidget(self.closeButton)
        
        self.configureMenu_l = QGridLayout()
        self.configureMenu_w = QWidget()
        self.configureMenu_w.setLayout(self.configureMenu_l)
        
        self.config_menu_1_l = QVBoxLayout()
        self.config_menu_1_w = QWidget()
        self.config_menu_1_w.setLayout(self.config_menu_1_l)
        self.configureMenu_l.addWidget(self.config_menu_1_w, 1,1)
        
        self.data_model_l = QHBoxLayout()
        self.data_model_w = QWidget()
        self.data_model_w.setLayout(self.data_model_l)
        
        
        self.data_model_combobox = QComboBox()
        self.data_model_combobox.addItems(["Tweet", "Sentiment"])
        
        self.data_model_load = QPushButton("Load Model")
        
        
        self.data_model_l.addWidget(QLabel("Data Model"))
        self.data_model_l.addWidget(self.data_model_combobox)
        self.data_model_l.addWidget(self.data_model_load)
        
        self.config_menu_1_l.addWidget(self.data_model_w)
        
        self.model_desc_l = QHBoxLayout()
        self.model_desc_w = QWidget()
        self.model_desc_w.setLayout(self.model_desc_l)
        
        self.model_initial_desc_l = QGridLayout()
        self.model_initial_desc_w = QWidget()
        self.model_initial_desc_w.setLayout(self.model_initial_desc_l)
        self.model_desc_l.addWidget(self.model_initial_desc_w)
        
        self.model_final_desc_l = QGridLayout()
        self.model_final_desc_w = QWidget()
        self.model_final_desc_w.setLayout(self.model_final_desc_l)
        self.model_desc_l.addWidget(self.model_final_desc_w)
        
        self.config_menu_1_l.addWidget(self.model_desc_w)
        
        self.index_combo = QComboBox()
        self.config_menu_1_l.addWidget(QLabel("Index"))
        self.config_menu_1_l.addWidget(self.index_combo)
        
        self.data_combo = QComboBox()
        self.config_menu_1_l.addWidget(QLabel("Data"))
        self.config_menu_1_l.addWidget(self.data_combo)
        
        
        self.mapping_hist_label = QLabel("Mapping History")
        self.config_menu_1_l.addWidget(self.mapping_hist_label)
        
        self.mapping_hist_l = QVBoxLayout()
        self.mapping_hist_w = QWidget()
        self.mapping_hist_w.setLayout(self.mapping_hist_l)
        self.config_menu_1_l.addWidget(self.mapping_hist_w)
        
        self.config_menu_2_l = QVBoxLayout()
        self.config_menu_2_w = QWidget()
        self.config_menu_2_w.setLayout(self.config_menu_2_l)
        self.configureMenu_l.addWidget(self.config_menu_2_w, 1,2)
        
        
        self.config_menu_3_l = QVBoxLayout()
        self.config_menu_3_w = QWidget()
        self.config_menu_3_w.setLayout(self.config_menu_3_l)
        self.configureMenu_l.addWidget(self.config_menu_3_w, 1,3)
        
        self.variable_pick = QComboBox()
        self.config_menu_3_l.addWidget(self.variable_pick)
        
        self.save_map_button = QPushButton("Save")
        self.config_menu_3_l.addWidget(self.save_map_button)
        
        self.main_layout.addWidget(self.configureMenu_w)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.bottom_pane_w)
        
        self.data_model_load.clicked.connect(lambda : self.__load_data_model())
        
        self.setLayout(self.main_layout)
        
        
    def __load_map_history(self):
        
        for i in reversed(range(self.mapping_hist_l.count())): 
            self.mapping_hist_l.itemAt(i).widget().setParent(None)
            
        for fmap in self.map_list:
            self.mapping_hist_l.addWidget(QLabel(fmap.getName()))
    
    def __load_frame_descriptions(self):
        self.__refresh_combo()
        
        intial_types = self.initial_frame.dtypes.reset_index(name="type")
        
        intial_types['type'] = intial_types['type'].astype('str') 
        
        for i in reversed(range(self.model_initial_desc_l.count())): 
            self.model_initial_desc_l.itemAt(i).widget().setParent(None)
            
        for index, row in intial_types.iterrows():
            self.model_initial_desc_l.addWidget(QLabel(str(row["index"])), index+1, 1)
            self.model_initial_desc_l.addWidget(QLabel(str(row["type"])), index+1, 2)
        
        final_types = self.final_frame.dtypes.reset_index(name="type")
        
        final_types['type'] = final_types['type'].astype('str') 
        
        for i in reversed(range(self.model_final_desc_l.count())): 
            self.model_final_desc_l.itemAt(i).widget().setParent(None)
            
        for index, row in final_types.iterrows():
            self.model_final_desc_l.addWidget(QLabel(str(row["index"])), index+1, 1)
            self.model_final_desc_l.addWidget(QLabel(str(row["type"])), index+1, 2)
        
    def __load_frame_map(self):
        
        for map_function in (MapFactory()).getMapList():
            
            mapRow_l = QHBoxLayout()
            mapRow_w = QWidget()
            
            map_button = QPushButton("Exec")
            
            print("La variable " + map_function)
            map_button.clicked.connect(lambda _, dtype=map_function : self.__load_map_config(dtype))
            map_button.clicked.connect(lambda _, dtype=map_function : print(dtype))
            
            mapRow_l.addWidget(QLabel(map_function))
            mapRow_l.addWidget(map_button)
            mapRow_w.setLayout(mapRow_l)
            
            self.config_menu_2_l.addWidget(mapRow_w)
    
    def __refresh_combo(self):
        self.index_combo.clear()
        self.data_combo.clear()
        
        self.index_combo.addItems(self.final_frame.columns.to_list())
        self.index_combo.addItem("NewEmpty")
        self.data_combo.addItems(self.final_frame.columns.to_list())
    
    def __load_map_config(self, map_function):
        print("Loading with map " + str(map_function))
        self.variable_pick.addItems(self.final_frame.columns.to_list())
        
        # We don't check the Exception since it happends if not connected to anything
        try: 
            self.save_map_button.clicked.disconnect() 
        except Exception: 
            pass 
        
        self.save_map_button.clicked.connect(lambda:self.transform_map(map_function))
    
        
    def transform_map(self, map_function):
        print("Loading2 with map " + str(map_function))
        strategy = MapFactory()
        
        args = {'variable' : self.variable_pick.currentText()}
        
        self.final_frame, fmap = strategy.apply(map_function, self.final_frame, args)
        
        self.map_list += [fmap]
        
        self.__load_frame_descriptions()
        self.__load_map_history()
        
    def __load_data_model(self):    
        self.initial_frame = createModelFrame(self.data_model_combobox.currentText())
        self.final_frame = self.initial_frame.copy(deep = True)
        self.__load_frame_descriptions()
        
    def getPlotConfiguration(self):
        return self.__configuration
    
    def is_saved(self):
        return self.__saved
    
    def __save_and_exit(self):
        self.__configuration = PlotConfiguration(
            self.initial_frame, self.final_frame, 
            self.map_list, self.data_model_combobox.currentText(), 
            self.index_combo.currentText(), self.data_combo.currentText()
        )
        
        self.__saved = True
        
        self.close()