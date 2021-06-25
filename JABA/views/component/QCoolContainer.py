from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

import PyQt5.QtCore as QtCore
from PyQt5.QtGui import QColor

class QCoolContainer(QWidget):
    
    styleSheet = """
        QCoolContainer{
            background-color: white;
            border-radius: 8px;

        }
    """
    
    def __init__(self):        
        super(QCoolContainer, self).__init__()
        
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet(self.styleSheet)
        
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QColor(150, 150, 150))
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 0)
        
        self.setGraphicsEffect(shadow)
        