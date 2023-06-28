from enum import Enum

class Language(Enum):
    en = 'en'
    de = 'de'
    ru = 'ru'
    fr = 'fr'
    lt = 'lt'
    zh = 'zh'
    ja = 'ja'
    uk = 'uk'
    be = 'be'
    ba = 'ba'

    def cast_to_language_enum(value):
        try:
            return Language.__members__[value]
        except KeyError:
            raise ValueError(f"Invalid language: {value}")