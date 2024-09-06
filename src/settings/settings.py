from src.settings.constants import Translation


class AppSettings:
    translations: bool = False

    def get_ui_translation(self) -> dict:
        """Возврат словаря с переводом ui"""
        if self.translations is False:
            return Translation.ENG_UI
        elif self.translations is True:
            return Translation.RU_UI

    def get_func_translation(self) -> dict:
        if self.translations is False:
            return Translation.ENG_FUNC
        elif self.translations is True:
            return Translation.RU_FUNC


def get_translated_dict() -> dict:
    settings = AppSettings()
    ui_dict = settings.get_ui_translation()
    return ui_dict


def get_translated_func() -> dict:
    settings = AppSettings()
    func_dict = settings.get_func_translation()
    return func_dict
