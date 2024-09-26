import sys

from subprocess import Popen
from PySide6 import QtWidgets, QtCore
from loguru import logger

from src.settings.thread_manager import ThreadManager
from src.settings.utils import check_app_version


class VersionCheckerWidget(QtWidgets.QWidget, ThreadManager):
    """Виджет проверки версии"""

    def __init__(self, main_widget) -> None:
        super().__init__()
        self.setWindowTitle("Version checker")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.main_widget = main_widget


        self.message = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.actual_version = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.app_version = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.github_page = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.message)

    @logger.catch
    def start_updater(self, program, exit_code=0) -> None:
        """Запуск обновления и закрытие приложения"""
        Popen(program)
        sys.exit(exit_code)

    @logger.catch
    def start_update(self) -> None:
        self.start_updater(["updater.exe"])

    def store_main_widget(self, widget) -> None:
        """Сохранить класс виджета настроек"""
        self.main_widget = widget

    def block_main_widget(self) -> None:
        self.main_widget.setEnabled(False)

    def unblock_main_widget(self) -> None:
        self.main_widget.setEnabled(True)

    def closeEvent(self, event) -> None:
        self.unblock_main_widget()

    @logger.catch
    def showEvent(self, event) -> None:
        self.block_main_widget()
        version = check_app_version()
        if version is True:
            self.message.setText(self.tr("last version"))
        else:
            update_button = QtWidgets.QPushButton(self.tr("update"), self)
            update_button.clicked.connect(self.start_update)
            self.message.setText(self.tr('outdated version'))
            self.app_version.setText(f"{self.tr('app version')} {version.get('app_version')}")
            self.actual_version.setText(f"{self.tr('actual version')} {version.get('git_version')}")
            self.github_page.setText(f"{self.tr('github releases')}"
                                     f" <a href={version.get('git')}>"
                                     f"{self.tr('releases link')}</a>")
            self.github_page.setOpenExternalLinks(True)
            self.layout.addWidget(self.app_version)
            self.layout.addWidget(self.actual_version)
            self.layout.addWidget(self.github_page)
            self.layout.addWidget(update_button)

