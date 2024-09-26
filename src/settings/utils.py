import json
import os

import requests
from PySide6.QtCore import QLocale
from loguru import logger

from src.settings.constants import Translation
from src.settings.settings import AppSettings


@logger.catch
def create_lang_settings_json() -> None:
    """Создание настроек для перевода"""
    lang = QLocale.system().name()
    json_settings = json.dumps({"lang": lang, "translation": True})
    settings_path = os.path.exists("settings")
    if settings_path:
        with open("settings/settings.json", "w") as file:
            file.write(json_settings)
    else:
        os.mkdir("settings")
        with open("settings/settings.json", "w") as file:
            file.write(json_settings)


@logger.catch
def translation_lang() -> str | None:
    """Получение название файла перевода"""
    settings_path = os.path.exists("settings/settings.json")
    if settings_path is False:
        create_lang_settings_json()
    try:
        with open("settings/settings.json", "r") as file:
            data = json.load(file)
        translation_settings = data.get("translation")
        if translation_settings is True:
            lang = data.get("lang")
            path = os.path.exists(f"src/static/localization/{lang}.qm")
            if path is True:
                return lang
            else:
                logger.info(f"file - {lang}.qm dont exist")
                return None
        else:
            logger.info(f"translation manual off")
            return None
    except Exception as exception:
        logger.info(f"translation error - {exception}")


def translate_country(eng_country: str) -> str:
    """сохранение города если не переведен"""
    lang = translation_lang()
    if lang:
        translated_country = Translation.COUNTRY.get(eng_country)
        if translated_country:
            return translated_country
        else:
            with open("translation.txt", "a") as file:
                file.write(f"\n| INFO | eng country - {eng_country}")
            return eng_country
    else:
        return eng_country


@logger.catch
def get_server_ip_from_log(log_file: str) -> str:
    """Получение ip сервера из лога"""
    content_split = log_file.split("\n")
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
    logger.info(f"server ip - {server_address}")
    return server_address


@logger.catch
def get_info_about_ip(server_ip: str) -> dict:
    """Информация об Ip адресе"""
    response = requests.get(url=f"https://ipinfo.io/{server_ip}/json")
    data = response.json()
    logger.info(f"request data - {data}")
    return data


@logger.catch
def check_app_version() -> dict | bool:
    """Проверка версии приложения"""
    response = requests.get(
        url="https://api.github.com/repos/ledxdeliveryflopp/eft_server_analyzer"
            "/releases/latest")
    data = response.json()
    version_github = data["tag_name"]
    app_version = AppSettings.app_version
    logger.info(f"git V - {version_github}, app V - {app_version}")
    if app_version != version_github:
        github_page = data["html_url"]
        return {"git_version": version_github, "app_version": app_version, "git": github_page}
    else:
        return True

