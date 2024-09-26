import sys

from PySide6.QtCore import QTranslator
from loguru import logger
from PySide6 import QtWidgets

from src.main_widget import MainWindow
from src.settings.utils import translation_lang


def start_app() -> None:
    app = QtWidgets.QApplication(sys.argv)
    translator = QTranslator()
    lang = translation_lang()
    logger.info(f"lang - {lang}")
    if lang:
        translator.load(f"src/static/localization/{lang}.qm")
        app.installTranslator(translator)
    window = MainWindow()
    app.setStyle('Windows')
    window.resize(700, 600)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    logger.add("application.log", rotation="100 MB",
               format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}")
    start_app()

