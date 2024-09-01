from PySide6 import QtWidgets
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar
from loguru import logger

from src.settings.settings import AppSettings, get_translated_dict
from src.widgets.server_analyze_widget import ServerAnalyzeWidget


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.toolbar = QToolBar("settings", self)
        self.addToolBar(self.toolbar)

        self.translation = QAction("Translation into russian", self)

        self.translation.triggered.connect(self.set_translation)
        self.translation.setCheckable(True)
        self.toolbar.addAction(self.translation)
        self.set_translation()

    def set_translation(self):
        """Перевод приложения на русский или английский"""
        if self.translation.isChecked() is True:
            AppSettings.translations = True
            new_lang = get_translated_dict()
            analyze_widget = ServerAnalyzeWidget()
            logger.info(f"translation on, button: {self.translation.isChecked()},"
                        f" settings: {AppSettings.translations}")
            self.translation.setText(new_lang.get("translation"))
            analyze_widget.search_log_button.setText(new_lang.get("search_log_file"))
            analyze_widget.last_log_button.setText(new_lang.get("last_server"))
            if analyze_widget.help_text_status is False:
                analyze_widget.help_text.setText(new_lang.get("help_text"))
            self.setCentralWidget(analyze_widget)
        if self.translation.isChecked() is False:
            AppSettings.translations = False
            new_lang = get_translated_dict()
            analyze_widget = ServerAnalyzeWidget()
            logger.info(f"translation off, button: {self.translation.isChecked()},"
                        f" settings: {AppSettings.translations}")
            self.translation.setText(new_lang.get("translation"))
            analyze_widget.search_log_button.setText(new_lang.get("search_log_file"))
            analyze_widget.last_log_button.setText(new_lang.get("last_server"))
            if analyze_widget.help_text_status is False:
                analyze_widget.help_text.setText(new_lang.get("help_text"))
            self.setCentralWidget(analyze_widget)
