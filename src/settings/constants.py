class Translation:
    """Списки перевода"""
    COUNTRY: dict = {"DK": "Дания", "RU": "Россия", "GB": "Великобритания", "FI": "Финляндия",
                     "SE": "Швеция", "IE": "Ирландия", "DE": "Германия", "CH": "Швейцария"}

    ENG_UI: dict = {"toolbar": "settings", "translation": "Translation into russian",
                    "search_log_file": "Find log file",
                    "last_server": "Get server from last log file",
                    "help_text": "log name: network-connection", "settings": "Settings"}
    ENG_FUNC: dict = {"search_file": "open file", "ping_result": "Ping-result  -",
                      "file_dont_selected": "file dont selected", "city": "City -",
                      "country": "Country -", "server_ip": "server IP -"}

    RU_UI: dict = {"translation": "Перевод на английский", "search_log_file": "Поиск log файла",
                   "last_server": "Сервер из последнего лога",
                   "help_text": "Название лога: network-connection", "settings": "Настройки"}
    RU_FUNC: dict = {"search_file": "открыть файл", "ping_result": "Результаты пинга  -",
                     "file_dont_selected": "Файл не выбран", "city": "Город -",
                     "country": "Страна -", "server_ip": "IP сервера -"}
