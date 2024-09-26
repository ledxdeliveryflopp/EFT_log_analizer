from loguru import logger
from PySide6 import QtWidgets
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu

from src.settings.settings import AppSettings
from src.settings.thread_manager import ThreadManager


class SettingsWidget(QtWidgets.QWidget, ThreadManager):

    def __init__(self, settings_menu: QMenu, analyze_widget, settings_menu_button: QAction,
                 version_menu_button: QAction) -> None:
        super().__init__()
        self.settings_menu: QMenu = settings_menu
        self.settings_menu_button: QAction = settings_menu_button
        self.version_menu_button: QAction = version_menu_button
        self.analyze_widget = analyze_widget
        self.main_widget = None
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setWindowTitle(self.tr("Settings"))

        self.ping_button_status = None

        self.ping_button = QtWidgets.QPushButton(self.tr("Server ping"))
        self.ping_button.clicked.connect(self.set_server_ping)
        self.ping_button.setCheckable(True)

        self.layout.addWidget(self.ping_button)

    @logger.catch
    def set_server_ping(self) -> None:
        """Активация и диактивация пинга сервера"""
        active_thread = self.get_active_thread_count()
        button_status = self.ping_button.isChecked()
        if not self.ping_button_status and active_thread == 0:
            self.ping_button_status = button_status
        if active_thread == 0:
            if button_status is True:
                AppSettings.server_ping = True
            elif button_status is False:
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
