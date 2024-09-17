from loguru import logger
from PySide6 import QtWidgets

from src.main_widget import MainWindow

if __name__ == "__main__":
    import sys
    logger.add("application.log", rotation="100 MB",
               format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}")
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.setStyle('Windows')
    window.resize(700, 600)
    window.show()
    sys.exit(app.exec())
