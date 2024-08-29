import requests

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QFileDialog
from loguru import logger


class ServerAnalyzeWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.help_text_status = False
        self.last_log = None

        self.layout = QtWidgets.QVBoxLayout(self)

        self.result_text = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.help_text = QtWidgets.QLabel("название лога: network-connection",
                                          alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.search_log_button = QtWidgets.QPushButton("Найти log файл")
        self.last_log_button = QtWidgets.QPushButton("Получить информацию с последнего лога")

        self.last_log_button.clicked.connect(self.get_last_log)
        self.search_log_button.clicked.connect(self.get_server_info)

        self.layout.addWidget(self.search_log_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.help_text, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.last_log_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

    @logger.catch
    def get_server_from_log_file(self):
        """Поиск ip сервера в log файле"""
        log_file = QFileDialog.getOpenFileName(self, 'Открыть файл', filter="log(*.log)")[0]
        if not log_file:
            return None
        with open(file=log_file, mode="r") as file:
            content = file.read()
        content_split = content.split("\n")
        result_list = [string for string in content_split if
                       "Enter to the 'Connected' state" in string]
        result_list_len = len(result_list) - 1
        last_connection_log = result_list[result_list_len]
        self.last_log = log_file
        server_address = last_connection_log.split(" ")
        server_address = server_address[8:]
        server_address = server_address[0]
        server_address = server_address.split(",")
        server_address = server_address[0]
        server_address = server_address.split(":")
        server_address = server_address[0]
        logger.info(f"Slice result - {server_address}")
        return server_address

    @logger.catch
    def get_server_info(self):
        """Получение информации о сервере"""
        server_address = self.get_server_from_log_file()
        if not server_address and self.help_text_status is False:
            self.help_text.setText("Не выбран файл")
            return None
        if not server_address and self.help_text_status is True:
            self.result_text.setText("Не выбран файл")
            return None
        response = requests.get(url=f"https://ipinfo.io/{server_address}/json")
        data = response.json()
        country = data.get("country")
        city = data.get("city")
        if self.help_text_status is False:
            self.destroy_help_text()
        self.layout.addWidget(self.result_text)
        self.result_text.setText(f"Город - {city}, Страна - {country}, IP сервера - {server_address}")

    @logger.catch
    def get_last_log(self):
        with open(file=self.last_log, mode="r") as file:
            content = file.read()
        content_split = content.split("\n")
        result_list = [string for string in content_split if
                       "Enter to the 'Connected' state" in string]
        result_list_len = len(result_list) - 1
        last_connection_log = result_list[result_list_len]
        server_address = last_connection_log.split(" ")
        server_address = server_address[8:]
        server_address = server_address[0]
        server_address = server_address.split(",")
        server_address = server_address[0]
        server_address = server_address.split(":")
        server_address = server_address[0]
        logger.info(f"Slice result - {server_address}")
        response = requests.get(url=f"https://ipinfo.io/{server_address}/json")
        data = response.json()
        country = data.get("country")
        city = data.get("city")
        if self.help_text_status is False:
            self.destroy_help_text()
        self.layout.addWidget(self.result_text)
        self.result_text.setText(f"Город - {city}, Страна - {country}, IP сервера - {server_address}")

    @logger.catch
    def destroy_help_text(self):
        """Удаление информационного текста"""
        self.help_text.deleteLater()
        self.help_text_status = True
