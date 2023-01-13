# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from presentation import view_manager as vm

def main():
    """ This function is the entry point of the application.
    """    
    app = QApplication(sys.argv)
    my_app = vm.Gui().get_instance() # Calls the main window.
    my_app.show()
    my_app.setWindowTitle("To-do list!")
    my_app.setWindowIcon(QtGui.QIcon("app/presentation/icon.png"))
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
