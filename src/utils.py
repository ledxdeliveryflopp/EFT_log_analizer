from src.constants import Translation


def translate_country(eng_country: str) -> str | None:
    """Перевод названия страны"""
    print(eng_country)
    translated_country = Translation.COUNTRY.get(eng_country)
    if translated_country:
        return translated_country
    else:
        return None
