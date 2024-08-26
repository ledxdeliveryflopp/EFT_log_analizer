from PySide6 import QtWidgets
from src.widgets.log_search_widget import SearchLogWidget


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.log_widget = SearchLogWidget()
        self.setCentralWidget(self.log_widget)
