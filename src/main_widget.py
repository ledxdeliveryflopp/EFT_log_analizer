from loguru import logger
from PySide6 import QtWidgets
from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction

from src.settings.thread_manager import ThreadManager
from src.server_analyze.widget import ServerAnalyzeWidget
from src.settings.widget import SettingsWidget
from src.version.widget import VersionCheckerWidget


class MainWindow(QtWidgets.QMainWindow, ThreadManager):

    @logger.catch
    def __init__(self) -> None:
        super().__init__()
        self.timer = QTimer()
        self.translation_button_status = None
        self.ping_button_status = None
        self.setWindowTitle("Eft-server-analyzer")
        self.settings_menu_button = QAction(self.tr("Settings"), self)
        self.settings_menu_button.triggered.connect(self.open_settings_widget)
        self.version_menu_button = QAction(self.tr("Version checker"), self)
        self.version_menu_button.triggered.connect(self.open_app_version_widget)

        self.menu = self.menuBar()
        self.settings_menu = self.menu.addMenu(self.tr("App"))
        self.settings_menu.addAction(self.settings_menu_button)
        self.settings_menu.addSeparator()
        self.settings_menu.addAction(self.version_menu_button)

        self.version_widget = VersionCheckerWidget(main_widget=self)
        self.analyze_widget = ServerAnalyzeWidget()
        self.settings_widget = SettingsWidget(settings_menu=self.settings_menu,
                                              settings_menu_button=self.settings_menu_button,
                                              version_menu_button=self.version_menu_button,
                                              analyze_widget=self.analyze_widget)

        # self.settings_widget.set_translation()
        self.setCentralWidget(self.analyze_widget)

    @logger.catch
    def block_settings_menu(self)  -> None:
        """Блокировка настроек при активных потоках(кроме этого)"""
        logger.info(f"{self.block_settings_menu.__name__} - thread start")
        active_thread = self.get_active_thread_count()
        thread = active_thread
        while thread > 1:
            thread = self.get_active_thread_count()
            self.settings_menu.setEnabled(False)
        else:
            self.settings_menu.setDisabled(False)
            logger.info(f"{self.block_settings_menu.__name__} - thread stop")

    @logger.catch
    def open_settings_widget(self) -> None:
        """Открытие виджета настроек"""
        self.settings_widget.store_main_widget(widget=self)
        self.settings_widget.show()

    @logger.catch
    def open_app_version_widget(self) -> None:
        self.version_widget.show()
