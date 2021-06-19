from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

import PyQt5.QtCore as QtCore

class QCoolContainer(QWidget):
    
    styleSheet = """
        QCoolContainer{
            background-color: white;
            border: 1px solid #a6a6a6;
            border-radius: 8px;

        }
    """
    
    def __init__(self):        
        super(QCoolContainer, self).__init__()
        
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet(self.styleSheet)
        
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(8)
        shadow.setOffset(0, 0)
        
        self.setGraphicsEffect(shadow)
        