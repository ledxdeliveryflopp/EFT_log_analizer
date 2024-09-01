from src.settings.constants import Translation


class AppSettings:
    translations: bool = False

    def get_ui_translation(self) -> dict:
        """Возврат словаря с переводом ui"""
        if self.translations is False:
            return Translation.ENG_UI
        else:
            return Translation.RU_UI


def get_translated_dict():
    settings = AppSettings()
    ui_dict = settings.get_ui_translation()
    return ui_dict
