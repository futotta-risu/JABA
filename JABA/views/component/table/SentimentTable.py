from PyQt5 import Qt, QtCore, QtGui, QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class SentimentTable(QTableWidget):
    
    def __init__(self):
        super().__init__()
        self.verticalHeader().setVisible(False)
        self.setRowCount(1) 
        self.setColumnCount(2)
        self.setShowGrid(False)
        
        table_header_font = self.horizontalHeader().font()
        table_header_font.setPointSize(10)
        table_header_font.setBold(True)
        self.horizontalHeader().setFont( table_header_font )
        
        self.setHorizontalHeaderItem(0, QTableWidgetItem('Text'))
        self.setHorizontalHeaderItem(1, QTableWidgetItem('Sentiment'))
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch) 
        
        self.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        