from src.settings.constants import Translation
from src.settings.settings import AppSettings


def translate_country(eng_country: str) -> str | None:
    """Перевод названия страны"""
    if AppSettings.translations is True:
        translated_country = Translation.COUNTRY.get(eng_country)
        if translated_country:
            return translated_country
        else:
            return None
    else:
        return None
