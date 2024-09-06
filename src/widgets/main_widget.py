from PySide6 import QtWidgets
from PySide6.QtGui import QAction
from loguru import logger

from src.settings.settings import AppSettings, get_translated_dict
from src.settings.thread_manager import ThreadManager
from src.widgets.server_analyze_widget import ServerAnalyzeWidget


class MainWindow(QtWidgets.QMainWindow, ThreadManager):

    def __init__(self) -> None:
        super().__init__()
        self.translation = QAction("Translation into russian", self)
        self.translation.triggered.connect(self.set_translation)
        self.translation.setCheckable(True)

        self.menu = self.menuBar()
        self.settings_menu = self.menu.addMenu("Settings")
        self.settings_menu.addAction(self.translation)
        self.settings_menu.addSeparator()

        self.set_translation()

    def set_translation(self) -> None:
        """Перевод приложения на русский или английский"""
        active_thread = self.get_active_thread_count()
        if active_thread == 0:
            if self.translation.isChecked() is True:
                """Русский язык"""
                AppSettings.translations = True
                new_lang = get_translated_dict()
                logger.info(f"translation on, button: {self.translation.isChecked()},"
                            f" settings: {AppSettings.translations}")
                self.settings_menu.setTitle(new_lang.get("settings"))
                self.translation.setText(new_lang.get("translation"))
                analyze_widget = ServerAnalyzeWidget()
                analyze_widget.search_log_button.setText(new_lang.get("search_log_file"))
                analyze_widget.last_log_button.setText(new_lang.get("last_server"))
                if analyze_widget.help_text_status is False:
                    analyze_widget.help_text.setText(new_lang.get("help_text"))
                self.setCentralWidget(analyze_widget)
            if self.translation.isChecked() is False:
                """Английский язык"""
                AppSettings.translations = False
                new_lang = get_translated_dict()
                logger.info(f"translation off, button: {self.translation.isChecked()},"
                            f" settings: {AppSettings.translations}")
                self.settings_menu.setTitle(new_lang.get("settings"))
                self.translation.setText(new_lang.get("translation"))
                analyze_widget = ServerAnalyzeWidget()
                analyze_widget.search_log_button.setText(new_lang.get("search_log_file"))
                analyze_widget.last_log_button.setText(new_lang.get("last_server"))
                if analyze_widget.help_text_status is False:
                    analyze_widget.help_text.setText(new_lang.get("help_text"))
                self.setCentralWidget(analyze_widget)
        else:
            self.translation.setChecked(False)
