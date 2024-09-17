import requests
from loguru import logger

from src.settings.constants import Translation
from src.settings.settings import AppSettings


def translate_country(eng_country: str) -> str:
    """Перевод названия страны"""
    if AppSettings.translations is True:
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
