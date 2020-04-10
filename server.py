import os
import sys

from PyQt5 import QtCore, QtWidgets,uic
import PyQtWebEngine

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    path_ui = os.path.join(os.path.dirname(__file__), "test.ui")
    window = uic.loadUi(path_ui)
    window.widget.load(QtCore.QUrl("https://stackoverflow.com/"))
    window.show()
    sys.exit(app.exec_())