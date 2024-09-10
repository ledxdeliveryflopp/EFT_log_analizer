from loguru import logger
from PySide6 import QtWidgets
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu

from src.settings.settings import AppSettings, get_translated_dict
from src.settings.thread_manager import ThreadManager


class SettingsWidget(QtWidgets.QWidget, ThreadManager):

    def __init__(self, settings_menu: QMenu, analyze_widget, settings_menu_button: QAction) -> None:
        super().__init__()
        self.settings_menu: QMenu = settings_menu
        self.settings_menu_button: QAction = settings_menu_button
        self.analyze_widget = analyze_widget
        self.main_widget = None
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setWindowTitle("Settings")

        self.translation_button_status = None
        self.ping_button_status = None

        self.translation_button = QtWidgets.QPushButton("Translation into russian", self)
        self.translation_button.clicked.connect(self.set_translation)
        self.translation_button.setCheckable(True)

        self.ping_button = QtWidgets.QPushButton("Server ping")
        self.ping_button.clicked.connect(self.set_server_ping)
        self.ping_button.setCheckable(True)

        self.layout.addWidget(self.ping_button)
        self.layout.addWidget(self.translation_button)
        # self.settings_menu.triggered.connect(lambda: self.thread_manager.start(self.block_settings_menu))

    # @logger.catch
    # def block_settings_menu(self):
    #     """Блокировка настроек при активных потоках(кроме этого)"""
    #     logger.info(f"{self.block_settings_menu.__name__} - thread start")
    #     active_thread = self.get_active_thread_count()
    #     thread = active_thread
    #     while thread > 1:
    #         thread = self.get_active_thread_count()
    #         self.settings_menu.setEnabled(False)
    #     else:
    #         self.settings_menu.setDisabled(False)
    #         logger.info(f"{self.block_settings_menu.__name__} - thread stop")

    @logger.catch
    def set_translation(self) -> None:
        """Перевод приложения на русский или английский"""
        active_thread = self.get_active_thread_count()
        button_status = self.translation_button.isChecked()
        if not self.translation_button_status and active_thread == 0:
            self.translation_button_status = button_status
        if active_thread == 0:
            if button_status is True:
                """Русский язык"""
                AppSettings.translations = True
                new_lang = get_translated_dict()
                logger.info(f"translation on, button: {self.translation_button.isChecked()},"
                            f" settings: {AppSettings.translations}")
                self.settings_menu.setTitle(new_lang.get("app_toolbar"))
                self.settings_menu_button.setText(new_lang.get("settings"))
                self.translation_button.setText(new_lang.get("translation"))
                self.ping_button.setText(new_lang.get("server_ping"))
                self.analyze_widget.search_log_button.setText(new_lang.get("search_log_file"))
                self.analyze_widget.last_log_button.setText(new_lang.get("last_server"))
                if self.analyze_widget.help_text_status is False:
                    self.analyze_widget.help_text.setText(new_lang.get("help_text"))
                self.analyze_widget.result_text.setText("")
            if button_status is False:
                """Английский язык"""
                AppSettings.translations = False
                new_lang = get_translated_dict()
                logger.info(f"translation off, button: {self.translation_button.isChecked()},"
                            f" settings: {AppSettings.translations}")
                self.settings_menu.setTitle(new_lang.get("app_toolbar"))
                self.settings_menu_button.setText(new_lang.get("settings"))
                self.translation_button.setText(new_lang.get("translation"))
                self.ping_button.setText(new_lang.get("server_ping"))
                self.analyze_widget.search_log_button.setText(new_lang.get("search_log_file"))
                self.analyze_widget.last_log_button.setText(new_lang.get("last_server"))
                if self.analyze_widget.help_text_status is False:
                    self.analyze_widget.help_text.setText(new_lang.get("help_text"))
                self.analyze_widget.result_text.setText("")
        else:
            self.translation_button.setChecked(self.translation_button_status)
            self.translation_button_status = None

    @logger.catch
    def set_server_ping(self) -> None:
        """Активация и диактивация пинга сервера"""
        active_thread = self.get_active_thread_count()
        button_status = self.ping_button.isChecked()
        if not self.ping_button_status and active_thread == 0:
            self.ping_button_status = button_status
        if active_thread == 0:
            if self.ping_button.isChecked() is True:
                AppSettings.server_ping = True
            elif self.ping_button.isChecked() is False:
                AppSettings.server_ping = False
        else:
            self.ping_button.setChecked(self.ping_button_status)
            self.ping_button_status = None

    def store_main_widget(self, widget):
        """Сохранить класс главного окна"""
        self.main_widget = widget

    def block_main_widget(self):
        """Заблокировать главное окно"""
        self.main_widget.setEnabled(False)

    def unblock_main_widget(self):
        """Разблокировать главное окно"""
        self.main_widget.setEnabled(True)

    def showEvent(self, event):
        self.block_main_widget()

    def closeEvent(self, event):
        self.unblock_main_widget()
