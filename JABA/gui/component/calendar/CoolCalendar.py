from PyQt5 import QtWidgets, QtGui


class CoolCalendar(QtWidgets.QCalendarWidget):

    color = QtGui.QColor('#18BEBE')
    
    def __init__(self):
        super().__init__()

        self.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.setHorizontalHeaderFormat(0)
    
    def set_color(self, new_color):
        self.color = QtGui.QColor(new_color)
    
    def reset_dates(self, dates):   
        ''' Resets the dates colors of the calendar '''
        
        for date in dates:
            if not date.isValid():
                continue
                
            temp_font = QtGui.QFont()
            temp_font.setBold(True)    
            
            cell_format = QtGui.QTextCharFormat()
            cell_format.setForeground(self.color)            
            cell_format.setFont(temp_font)
            
            self.setDateTextFormat(date, cell_format)