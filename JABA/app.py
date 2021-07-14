import sys

from loguru import logger

from PyQt5.QtWidgets import QApplication

from gui.model.MainWindowModel import MainWindowModel
from gui.controller.MainController import MainController
from gui.view.MainView import MainView

from log import start_log


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        logger.info("App starting")

        self.model = MainWindowModel()
        self.main_controller = MainController(self.model)
        self.main_view = MainView(self.model, self.main_controller)
        self.main_view.show()

if __name__ == '__main__':

    start_log()
    app = App(sys.argv)
    sys.exit(app.exec_())
