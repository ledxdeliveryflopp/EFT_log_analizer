import requests

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QFileDialog
from loguru import logger


class SearchLogWidget(QtWidgets.QTableWidget):

    def __init__(self):
        super().__init__()
        self.help_text_status = False
        self.text = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.button = QtWidgets.QPushButton("Найти log файл")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.help_text = QtWidgets.QLabel("название лога: network-connection",
                                          alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.help_text)
        self.button.clicked.connect(self.get_server_info)

    @logger.catch
    def get_log_file(self):
        """Поиск ip сервера в log файле"""
        log_file = QFileDialog.getOpenFileName(self, 'Открыть файл')[0]
        with open(file=log_file, mode="r") as file:
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
        return server_address

    @logger.catch
    def get_server_info(self):
        """Получение информации о сервере"""
        server_address = self.get_log_file()
        response = requests.get(url=f"https://ipinfo.io/{server_address}/json")
        data = response.json()
        country = data.get("country")
        city = data.get("city")
        if self.help_text_status is False:
            self.destroy_help_text()
        self.layout.addWidget(self.text)
        self.text.setText(f"Город - {city}, Страна - {country}, IP сервера - {server_address}")

    @logger.catch
    def destroy_help_text(self):
        """Удаление информационного текста """
        self.help_text.deleteLater()
        self.help_text_status = True
