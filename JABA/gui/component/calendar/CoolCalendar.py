from PyQt5 import QtWidgets


class CoolCalendar(QtWidgets.QCalendarWidget):

    def __init__(self):
        super().__init__()

        self.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.setHorizontalHeaderFormat(0)
