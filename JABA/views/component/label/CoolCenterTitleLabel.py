from PyQt5 import Qt, QtCore, QtGui, QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class CoolCenterTitleLabel(QLabel):
    
    def __init__(self, text):
        super().__init__(text)
        
        self.setObjectName("SectionLabel")
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setAlignment(Qt.AlignCenter)
        