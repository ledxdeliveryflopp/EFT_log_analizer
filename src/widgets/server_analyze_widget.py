import subprocess
from functools import partial
import requests

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QFileDialog
from loguru import logger

from src.settings.settings import get_translated_func
from src.settings.thread_manager import ThreadManager
from src.settings.utils import translate_country


class ServerAnalyzeWidget(QtWidgets.QWidget, ThreadManager):

    def __init__(self):
        super().__init__()
        self.lang = get_translated_func()

        self.help_text_status = False
        self.ping_result_status = False
        self.last_log = None
        self.result_text_status = None

        self.layout = QtWidgets.QVBoxLayout(self)

        self.result_text = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ping_result = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.help_text = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.search_log_button = QtWidgets.QPushButton()
        self.last_log_button = QtWidgets.QPushButton()

        self.last_log_button.clicked.connect(self.get_last_log)
        self.search_log_button.clicked.connect(self.get_server_info)

        self.layout.addWidget(self.search_log_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.help_text, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.last_log_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

    @logger.catch
    def check_active_thread_block_button(self):
        """Блокировка кнопок поиска и последнего лога при активных потоках"""
        active_thread = self.get_active_thread_count()
        if active_thread > 0:
            self.search_log_button.blockSignals(True)
            return True
        else:
            return False

    @logger.catch
    def get_server_from_log_file(self):
        """Поиск ip сервера в log файле"""
        active = self.check_active_thread_block_button()
        if active is False:
            log_file = QFileDialog.getOpenFileName(self, self.lang.get("search_file"), filter="log(*.log)")[0]
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
            logger.info(f"server ip - {server_address}")
            return server_address
        else:
            return True

    @logger.catch
    def ping_server(self, server_ip):
        """Пинг сервера"""
        logger.info(f"{self.ping_server.__name__} - thread start")
        command = subprocess.run(["ping", f"{server_ip}"], stdout=subprocess.PIPE, text=True,
                                 encoding="cp866", creationflags=subprocess.CREATE_NO_WINDOW)
        logger.info(f"ping status code - {command.returncode}")
        command_result_split = command.stdout.split("\n")
        command_result_slice = command_result_split[8:]
        command_result = command_result_slice[0]
        logger.info(f"ping result - {command_result}")
        self.layout.addWidget(self.ping_result)
        self.ping_result.setText(f"{self.lang.get('ping_result')}{command_result}")
        logger.info(f"{self.ping_server.__name__} - thread stop")
        self.ping_result.show()

    @logger.catch
    def get_server_info(self):
        """Получение информации о сервере"""
        self.destroy_ping_result()
        server_ip = self.get_server_from_log_file()
        if not server_ip:
            self.help_text.setText(self.lang.get("file_dont_selected"))
            self.destroy_ping_result()
            self.destroy_result_text()
            return None
        elif server_ip is True:
            self.search_log_button.blockSignals(False)
            return None
        if self.help_text_status is False:
            self.destroy_help_text()
        self.thread_manager.start(partial(self.ping_server, f"{server_ip}"))
        response = requests.get(url=f"https://ipinfo.io/{server_ip}/json")
        data = response.json()
        country = data.get("country")
        city = data.get("city")
        translated_country_name = translate_country(eng_country=country)
        self.layout.addWidget(self.result_text)
        self.result_text.setText(f"{self.lang.get('city')} {city}, {self.lang.get('country')} {translated_country_name},"
                                 f" {self.lang.get('server_ip')} {server_ip}")

    @logger.catch
    def get_last_log(self):
        self.destroy_ping_result()
        self.destroy_result_text()
        """Получение информации с последнего лога"""
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
        self.thread_manager.start(partial(self.ping_server, f"{server_address}"))
        response = requests.get(url=f"https://ipinfo.io/{server_address}/json")
        data = response.json()
        country = data.get("country")
        city = data.get("city")
        if self.help_text_status is False:
            self.destroy_help_text()
        translated_country_name = translate_country(eng_country=country)
        if self.result_text_status is True:
            self.result_text.show()
        self.layout.addWidget(self.result_text)
        self.result_text.setText(
            f"{self.lang.get('city')} {city}, {self.lang.get('country')} {translated_country_name},"
            f" {self.lang.get('server_ip')} {server_address}")

    @logger.catch
    def destroy_help_text(self):
        """Удаление информационного текста"""
        self.help_text.hide()
        self.help_text_status = True

    @logger.catch
    def destroy_ping_result(self):
        """Удаление информационного текста"""
        self.ping_result.hide()
        self.ping_result_status = True

    @logger.catch()
    def destroy_result_text(self):
        self.result_text.hide()
        self.result_text_status = True
