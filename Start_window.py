import sys

# 1. Import QApplication and all the required widgets
from PyQt5 import QtWidgets
from functools import partial
import GlobalVariables
# from SimpleFields import ElementsList

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("QMainWindow")
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        # self.setCentralWidget(QtWidgets.QLabel("I'm the Central Widget"))
        self.test_layout = QtWidgets.QStackedLayout()
        self.centralWidget().setLayout(self.test_layout)
        temp = QtWidgets.QPushButton()
        temp.setText('test')
        self.test_layout.addWidget(temp)
        self._createMenu()
        self._createToolBar()
        # self._createStatusBar()
        

    def _createMenu(self):
        menu = self.menuBar().addMenu("Menu")
        menu.addAction("&Load Mod", partial(self.testing, 'test load'))
        menu.addAction("&Save Mod", partial(self.testing, 'test save'))
        settings = self.menuBar().addMenu("Settings")
        settings.addAction("Labels visuals", partial(self.testing, 'labels'))
        settings.addAction("Input Fonts", partial(self.testing, 'fonts'))

    def _createToolBar(self):
        tools = QtWidgets.QToolBar()
        for element in GlobalVariables.elements:
            tools.addAction(element, partial(self.testing, element))
            self.addToolBar(tools)
        tools.addAction('Addition', partial(self.testing, 'Addition'))
        self.addToolBar(tools)

    # def _createStatusBar(self):
    #     status = QtWidgets.QStatusBar()
    #     status.showMessage("I'm the Status Bar")
    #     self.setStatusBar(status)

    def testing(self, value='test'):
        print('test = ' + value)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())