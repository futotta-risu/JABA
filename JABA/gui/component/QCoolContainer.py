from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QHBoxLayout

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class QCoolContainer(QWidget):

    styleSheet = """
        QCoolContainer{
            background-color: white;
            border-radius: 8px;

        }
    """

    def __init__(self, widget=None):
        super(QCoolContainer, self).__init__()

        if widget is not None:
            layout = QHBoxLayout()
            self.setLayout(layout)
            layout.addWidget(widget)

        self._init_style()

    def _init_style(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(self.styleSheet)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QColor(150, 150, 150))
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 0)

        self.setGraphicsEffect(shadow)
