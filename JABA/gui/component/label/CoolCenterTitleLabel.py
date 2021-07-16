from PyQt5 import QtCore, QtWidgets


class CoolCenterTitleLabel(QtWidgets.QLabel):

    def __init__(self, text):
        super().__init__(text)

        self.setObjectName("SectionLabel")

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.setAlignment(QtCore.Qt.AlignCenter)
