from enum import Enum
import spacy

nlp_en = spacy.load("en_core_web_sm")
nlp_zh = spacy.load("zh_core_web_sm")
nlp_de = spacy.load("de_core_news_sm")
nlp_fr = spacy.load("fr_core_news_sm")
nlp_ja = spacy.load("ja_core_news_sm")
nlp_lt = spacy.load("lt_core_news_sm")
nlp_ru = spacy.load("ru_core_news_sm")
nlp_uk = spacy.load("uk_core_news_sm")
nlp_es = spacy.load("es_core_news_sm")

nlp_dict = {
    "en": nlp_en,
    "zh": nlp_zh,
    "de": nlp_de,
    "fr": nlp_fr,
    "ja": nlp_ja,
    "lt": nlp_lt,
    "uk": nlp_uk,
    "ru": nlp_ru,
    "ba": nlp_ru,
    "be": nlp_ru,
    "es": nlp_es,
}



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
    es = 'es'
    hy = "hy"


    @classmethod
    def has_member_key(cls, key):
        return key in cls.__members__
    
    def get_spacy_nlp(language):
        try:
            return nlp_dict[language.value]
        except KeyError:
            raise ValueError(f"No spacy nlp for {language}")
    
    def get_supported_ner(language):
        davlan_ner = [
            Language.en, 
            Language.de,
            Language.es,
            Language.fr,
            Language.zh,
        ]
        babelscape_ner = [
            Language.en,
            Language.es,
            Language.fr,
            Language.de,
            Language.ru
        ]
        if language in davlan_ner:
            return "davlan_ner"
        elif language in babelscape_ner:
            return "babelscape_ner"
        else:
            return "no_ner"