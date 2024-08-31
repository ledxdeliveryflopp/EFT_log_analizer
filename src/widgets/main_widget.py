from PySide6 import QtWidgets
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar
from loguru import logger

from src.settings.settings import AppSettings
from src.widgets.server_analyze_widget import ServerAnalyzeWidget


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.analyze_widget = ServerAnalyzeWidget()
        self.setCentralWidget(self.analyze_widget)

        self.toolbar = QToolBar("Settings", self)
        self.addToolBar(self.toolbar)

        self.translation = QAction("Translation into russian", self)

        self.translation.triggered.connect(self.set_translation)
        self.translation.setCheckable(True)
        self.toolbar.addAction(self.translation)

    def set_translation(self):
        """Перевод приложения на русский или английский"""
        if self.translation.isChecked() is True:
            AppSettings.translations = True
            logger.info(f"translation on, button: {self.translation.isChecked()},"
                        f" settings: {AppSettings.translations}")
            self.translation.setText("Перевод на английский")

            self.analyze_widget.help_text.setText("Название лога: network-connection")
            self.analyze_widget.last_log_button.setText("Информация с последнего лога")
            if self.analyze_widget.help_text_status is False:
                self.analyze_widget.search_log_button.setText("Найти лог файл")
            self.setCentralWidget(self.analyze_widget)
        if self.translation.isChecked() is False:
            AppSettings.translations = False
            logger.info(f"translation off, button: {self.translation.isChecked()},"
                        f" settings: {AppSettings.translations}")
            self.translation.setText("Translation into russian")
            self.analyze_widget.search_log_button.setText("Find log file")
            self.analyze_widget.last_log_button.setText("Get server from last log file")
            if self.analyze_widget.help_text_status is False:
                self.analyze_widget.help_text.setText("log name: network-connection")
            self.setCentralWidget(self.analyze_widget)
