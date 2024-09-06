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
