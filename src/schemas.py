from enum import Enum


class InputLang(str, Enum):
    ko: str = "ko"


class TranslatedLang(str, Enum):
    en: str = "en"
    ja: str = "ja"
