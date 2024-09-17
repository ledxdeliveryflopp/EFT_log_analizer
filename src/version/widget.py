from PySide6 import QtWidgets, QtCore
from loguru import logger

from src.settings.settings import get_translated_func
from src.settings.utils import check_app_version


class VersionCheckerWidget(QtWidgets.QWidget):
    """Виджет проверки версии"""

    def __init__(self, main_widget):
        super().__init__()
        self.setWindowTitle("Version checker")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.main_widget = main_widget

        self.message = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.actual_version = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.app_version = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.github_page = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.message)

    def store_main_widget(self, widget):
        """Сохранить класс виджета настроек"""
        self.main_widget = widget

    def block_main_widget(self):
        self.main_widget.setEnabled(False)

    def unblock_main_widget(self):
        self.main_widget.setEnabled(True)

    def closeEvent(self, event):
        self.unblock_main_widget()

    @logger.catch
    def showEvent(self, event) -> None:
        self.block_main_widget()
        version = check_app_version()
        lang = get_translated_func()
        if version is True:
            self.message.setText(lang.get("last_version"))
        else:
            self.message.setText(lang.get('outdated_version'))
            self.app_version.setText(f"{lang.get('app_version')} {version.get('app_version')}")
            self.actual_version.setText(f"{lang.get('actual_version')} {version.get('git_version')}")
            self.github_page.setText(f"{lang.get('github_releases')}"
                                     f" <a href={version.get('git')}>{lang.get('releases_link')}</a>")
            self.github_page.setOpenExternalLinks(True)
            self.layout.addWidget(self.app_version)
            self.layout.addWidget(self.actual_version)
            self.layout.addWidget(self.github_page)
