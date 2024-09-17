class Translation:
    """Списки перевода"""
    COUNTRY: dict = {"DK": "Дания", "RU": "Россия", "GB": "Великобритания",
                     "FI": "Финляндия", "SE": "Швеция", "IE": "Ирландия",
                     "DE": "Германия", "CH": "Швейцария"}

    ENG_UI: dict = {"app_toolbar": "App", "translation": "Translation into russian",
                    "search_log_file": "Find log file",
                    "last_server": "Get server from last log file",
                    "help_text": "log name: network-connection", "settings": "Settings",
                    "version_checker": "Version checker", "server_ping": "Enable server ping"}
    ENG_FUNC: dict = {"search_file": "open file", "ping_result": "Ping-result  -",
                      "file_dont_selected": "file dont selected", "city": "City -",
                      "country": "Country -", "server_ip": "server IP -",
                      "outdated_version": "Outdated version", "last_version": "Last version",
                      "actual_version": "Actual version - ", "app_version": "App version - ",
                      "github_releases": "github - ", "releases_link": "Link to actual releases"
                      }

    RU_UI: dict = {"app_toolbar": "Приложение", "translation": "Перевод на нанглийский",
                   "search_log_file": "Поиск log файла",
                   "last_server": "Сервер из последнего лога",
                   "help_text": "Название лога: network-connection",
                   "settings": "Настройки", "version_checker": "Проверка версии",
                   "server_ping": "Включить пинг сервера"}
    RU_FUNC: dict = {"search_file": "открыть файл",
                     "ping_result": "Результаты пинга  -",
                     "file_dont_selected": "Файл не выбран", "city": "Город -",
                     "country": "Страна -", "server_ip": "IP сервера -",
                     "outdated_version": "Устаревшая версия", "last_version": "Последняя версия",
                     "actual_version": "Актуальная версия - ",
                     "app_version": "Версия приложения - ", "github_releases": "github - ",
                     "releases_link": "Ссылка на актуальный релиз"}
