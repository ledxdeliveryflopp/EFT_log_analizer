import sys

from PySide6 import QtWidgets
from loguru import logger

from src.widgets.main_widget import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.setStyle('Windows')
    window.resize(700, 600)
    logger.add("application.log", rotation="100 MB",
               format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}")
    window.show()
    sys.exit(app.exec())
