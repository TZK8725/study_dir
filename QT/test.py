import sys
import menu_bar
from PyQt5.QtWidgets import QApplication, QMainWindow


if __name__ == "__main__":

    app = QApplication(sys.argv)

    mainWindow = QMainWindow()
    ui = menu_bar.Ui_MainWindow()

    ui.setupUi(mainWindow)
    
    mainWindow.show()
    sys.exit(app.exec_())