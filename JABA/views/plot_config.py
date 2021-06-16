from PyQt5.QtWidgets import QMainWindow,  QWidget
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout,  QScrollArea, QSplitter
from PyQt5.QtWidgets import QPushButton, QFileDialog, QCalendarWidget, QLabel, QComboBox
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5 import QtCore, QtGui, Qt

from model.modelFactory import createModelFrame
from service.visualization.types.maps.MapFactory import MapFactory


class PlotConfigure(QMainWindow):
    
    frame_maps = ["count"]
    
    def __init__(self, type, *args, **kwargs):
        super(PlotConfigure, self).__init__(*args, **kwargs)
        self.initial_frame = createModelFrame(type)
        self.final_frame = self.initial_frame
        self.loadWidget()
        
        self.__load_frame_descriptions()
        self.__load_frame_map()
    
    def loadWidget(self):
        
        self.bottom_pane_l = QHBoxLayout()
        self.bottom_pane_w = QWidget()
        
        
        self.configureMenu_l = QGridLayout()
        self.configureMenu_w = QWidget()
        
        
        self.config_menu_1_l = QVBoxLayout()
        self.config_menu_1_w = QWidget()
        self.config_menu_1_w.setLayout(self.config_menu_1_l)
        self.configureMenu_l.addWidget(self.config_menu_1_w, 1,1)
        
        self.model_initial_desc_l = QGridLayout()
        self.model_initial_desc_w = QWidget()
        self.model_initial_desc_w.setLayout(self.model_initial_desc_l)
        self.config_menu_1_l.addWidget(self.model_initial_desc_w)
        
        self.model_final_desc_l = QGridLayout()
        self.model_final_desc_w = QWidget()
        self.model_final_desc_w.setLayout(self.model_final_desc_l)
        self.config_menu_1_l.addWidget(self.model_final_desc_w)
        
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
        
        self.configureMenu_w.setLayout(self.configureMenu_l)
        self.setCentralWidget(self.configureMenu_w)
        
        self.show()
        
    def __load_frame_descriptions(self):
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
        for frame_map in self.frame_maps:
            
            mapRow_l = QHBoxLayout()
            mapRow_w = QWidget()
            
            map_button = QPushButton("Exec")
            
            map_button.clicked.connect(lambda:self.transform_map(frame_map))
            
            mapRow_l.addWidget(QLabel(frame_map))
            mapRow_l.addWidget(map_button)
            mapRow_w.setLayout(mapRow_l)
            
            self.config_menu_2_l.addWidget(mapRow_w)
        
    def transform_map(self, map_type):
        strategy = MapFactory()
        
        self.final_frame = strategy.apply(map_type, self.final_frame)
        
        self.__load_frame_descriptions()