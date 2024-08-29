from PySide6 import QtWidgets

from src.widgets.server_analyze_widget import ServerAnalyzeWidget


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.analyze_widget = ServerAnalyzeWidget()
        self.setCentralWidget(self.analyze_widget)

