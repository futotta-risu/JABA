from PyQt5 import Qt, QtCore, QtGui, QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class CornerIconPanel(QSplitter):
    
    def __init__(self, label, icon):
        super().__init__(QtCore.Qt.Horizontal)
        
        self.addWidget(label)
        self.addWidget(icon)
        
        self.setStretchFactor(0,3)
        self.setStretchFactor(1,1)
        
        self.setObjectName("PlotHeaderSplit")
        