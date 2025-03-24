from deep_translator import GoogleTranslator
from pydantic import BaseModel
from schemas import InputLang, TranslatedLang


class TranslatorModel(BaseModel):
    """A data model to create the translator module."""

    source: InputLang = "ko"
    target: TranslatedLang = "ja"
    ai: bool = False


class TranslationTool:
    def __init__(self, translation_input: TranslatorModel):
        # Save the AI flag
        self.ai = translation_input.ai

        # If the AI flag is not specified, use the simple translator
        if not translation_input.ai:
            # If not using ai to translate:
            translator = GoogleTranslator(
                source=translation_input.source, target=translation_input.target
            )
            self.translator = translator

    def translate(self, word: str) -> str | None:
        if not self.ai:
            translation = self.translator.translate(word)

            return translation
