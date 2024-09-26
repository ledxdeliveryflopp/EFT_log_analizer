import filecmp
import os
import shutil
import urllib.request
import requests
from loguru import logger
from py7zr import py7zr

logger.add("updater.log", rotation="100 MB",
           format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}")


@logger.catch
def download_update() -> None:
    """Скачивание архива"""
    response = requests.get(
        url="https://api.github.com/repos/ledxdeliveryflopp/eft_server_analyzer"
            "/releases/latest")
    data = response.json()
    download_url = data["assets"][0]["browser_download_url"]
    urllib.request.urlretrieve(download_url, "update.7z")
    logger.info("zip file downloaded")


@logger.catch
def unzip_update() -> None:
    """распаковка архива в временную папку"""
    os.mkdir("temp-update")
    with py7zr.SevenZipFile("update.7z", mode='r') as update_zip:
        update_zip.extractall(path="temp-update")
        logger.info("zip extracted")
    os.remove("update.7z")
    logger.info("zip deleted")


@logger.catch
def update_files() -> None:
    """Обновление файлов"""
    compare = filecmp.cmp('temp-update/eft-server-analyzer.exe', "eft-server-analyzer.exe")
    if compare is False:
        logger.info("file compared, files are different")
        shutil.copyfile("temp-update/eft-server-analyzer.exe", "eft-server-analyzer.exe")
        shutil.rmtree("temp-update")
        logger.info("temp dir removed")


@logger.catch
def start_update() -> None:
    """Запуск обновления"""
    download_update()
    logger.info(f"{download_update.__name__} - finished")
    unzip_update()
    logger.info(f"{unzip_update.__name__} - finished")
    update_files()
    logger.info(f"{update_files.__name__} - finished")


if __name__ == "__main__":
    start_update()
