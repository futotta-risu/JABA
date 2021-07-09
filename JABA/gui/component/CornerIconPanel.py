from PyQt5.QtWidgets import QSplitter

from PyQt5.QtCore import Qt


class CornerIconPanel(QSplitter):

    def __init__(self, label, icon):
        super().__init__(Qt.Horizontal)

        self.addWidget(label)
        self.addWidget(icon)

        self.setStretchFactor(0, 3)
        self.setStretchFactor(1, 1)

        self.setObjectName("PlotHeaderSplit")
