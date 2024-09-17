import subprocess
from functools import partial

from loguru import logger
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QFileDialog

from src.settings.settings import AppSettings, get_translated_func
from src.settings.thread_manager import ThreadManager
from src.settings.utils import (
    get_info_about_ip,
    get_server_ip_from_log,
    translate_country,
)


class ServerAnalyzeWidget(QtWidgets.QWidget, ThreadManager):
    """Виджет анализа сервера"""

    def __init__(self) -> None:
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
    def check_active_thread_block_button(self) -> bool:
        """Блокировка кнопок поиска и последнего лога при активных потоках"""
        active_thread = self.get_active_thread_count()
        if active_thread > 0:
            self.search_log_button.blockSignals(True)
            return True
        else:
            return False

    @logger.catch
    def get_server_from_log_file(self, saved_log=None) -> None | str | bool:
        """Поиск ip сервера в log файле"""
        active_thread = self.check_active_thread_block_button()
        if active_thread is False:
            if not saved_log:
                log_file = QFileDialog.getOpenFileName(self, self.lang.get("search_file"), filter="log(*.log)")[0]
                if not log_file:
                    return None
                with open(file=log_file, mode="r") as file:
                    content = file.read()
                server_address = get_server_ip_from_log(log_file=content)
                self.last_log = log_file
                return server_address
            else:
                with open(file=saved_log, mode="r") as file:
                    content = file.read()
                server_address = get_server_ip_from_log(log_file=content)
                return server_address
        else:
            return True

    @logger.catch
    def ping_server(self, server_ip) -> None:
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
    def get_server_info(self) -> None:
        """Получение информации о сервере"""
        self.hide_ping_result()
        lang = get_translated_func()
        server_ip = self.get_server_from_log_file()
        if not server_ip and self.help_text_status is False:
            self.help_text.setText(lang.get("file_dont_selected"))
            self.hide_ping_result()
            self.hide_result_text()
            return None
        elif server_ip is True:
            self.search_log_button.blockSignals(False)
            return None
        if self.help_text_status is False:
            self.hide_help_text()
        if AppSettings.server_ping is True:
            self.thread_manager.start(partial(self.ping_server, f"{server_ip}"))
        data = get_info_about_ip(server_ip=server_ip)
        country = data.get("country")
        city = data.get("city")
        translated_country_name = translate_country(eng_country=country)
        self.layout.addWidget(self.result_text)
        self.result_text.show()
        self.result_text.setText(
            f"{lang.get('city')} {city}, {lang.get('country')} {translated_country_name},"
            f" {lang.get('server_ip')} {server_ip}")

    @logger.catch
    def get_last_log(self) -> None:
        """Получение информации с последнего лога"""
        self.hide_ping_result()
        self.hide_result_text()
        lang = get_translated_func()
        server_ip = self.get_server_from_log_file(saved_log=self.last_log)
        if AppSettings.server_ping is True:
            self.thread_manager.start(partial(self.ping_server, f"{server_ip}"))
        data = get_info_about_ip(server_ip=server_ip)
        country = data.get("country")
        city = data.get("city")
        translated_country_name = translate_country(eng_country=country)
        self.layout.addWidget(self.result_text)
        self.result_text.show()
        self.result_text.setText(
            f"{lang.get('city')} {city}, {lang.get('country')} {translated_country_name},"
            f" {lang.get('server_ip')} {server_ip}")

    @logger.catch
    def hide_help_text(self) -> None:
        """Удаление информационного текста"""
        self.help_text.hide()
        self.help_text_status = True

    @logger.catch
    def hide_ping_result(self) -> None:
        """Удаление информационного текста"""
        self.ping_result.hide()
        self.ping_result_status = True

    @logger.catch
    def hide_result_text(self) -> None:
        self.result_text.hide()
        self.result_text_status = True
