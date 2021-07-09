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
        
    def getColor(self, sentiment):
        ''' Gets the color based on the sentiment '''
        
        # Force the sentiment to a number in [-1, 1]
        sentiment = max(min(sentiment, 1), -1)
        
        return QtGui.QColor(
            100 + ( 1 - sentiment ) / 2 * 155,
            100 + ( 1 + sentiment ) / 2 * 155,
            100 + ( 1 + sentiment ) / 2 * 155
        ) 
    
    
    def addRow(self, text, sentiment):
        ''' Adds a new row to the table. The color of the sentiment is based on the value'''
        rowPosition = self.rowCount() - 1
        self.insertRow(rowPosition)

        text_item = QTableWidgetItem(text)
        sentiment_item = QTableWidgetItem("{:.2f}".format(sentiment))
        sentiment_item.setTextAlignment(QtCore.Qt.AlignCenter)
        
        temp_font = sentiment_item.font()
        temp_font.setBold(True)
        temp_font.setPointSize(12)
        sentiment_item.setFont(temp_font)
         
        cell_color = self.getColor(sentiment)
        brush = QtGui.QBrush(cell_color)
        sentiment_item.setForeground(brush)

        
        
        self.setItem(rowPosition, 0, text_item)
        self.setItem(rowPosition, 1, sentiment_item)