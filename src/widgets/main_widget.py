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

        self.server_ping = QAction("Ping server", self)
        self.server_ping.triggered.connect(self.set_server_ping)
        self.server_ping.setCheckable(True)

        self.menu = self.menuBar()
        self.settings_menu = self.menu.addMenu("Settings")
        self.settings_menu.addAction(self.translation)
        self.settings_menu.addSeparator()
        self.settings_menu.addAction(self.server_ping)

        self.set_translation()

    @logger.catch
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
                self.server_ping.setText(new_lang.get("server_ping"))
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
                self.server_ping.setText(new_lang.get("server_ping"))
                analyze_widget = ServerAnalyzeWidget()
                analyze_widget.search_log_button.setText(new_lang.get("search_log_file"))
                analyze_widget.last_log_button.setText(new_lang.get("last_server"))
                if analyze_widget.help_text_status is False:
                    analyze_widget.help_text.setText(new_lang.get("help_text"))
                self.setCentralWidget(analyze_widget)
        else:
            self.translation.setChecked(False)

    @logger.catch
    def set_server_ping(self) -> None:
        """Активация и диактивация пинга сервера"""
        active_thread = self.get_active_thread_count()
        if active_thread == 0:
            if self.server_ping.isChecked() is True:
                AppSettings.server_ping = True
            elif self.server_ping.isChecked() is False:
                AppSettings.server_ping = False
        else:
            self.server_ping.setChecked(False)
