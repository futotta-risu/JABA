from PyQt5 import Qt, QtCore, QtGui, QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class CoolCalendar(QCalendarWidget):
    
    def __init__(self):
        super().__init__()
        
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.setHorizontalHeaderFormat(0)
        