import logging
from abc import ABC, abstractmethod

import translators as ts

from anki_card_create.models.translator_input import TranslatorInput

logging.basicConfig(level=logging.INFO)


class TranslatorStrategy(ABC):
    @abstractmethod
    def translate(self, word: str) -> str | None:
        """Translate a single word or text string into the target language.

        Args:
            word: The text string or word to translate.

        Returns:
            The translated string if successful, or None if the translation
            returned an empty result.
        """


class SimpleGoogleTranslatorStrategy:
    def __init__(self, translation_input: TranslatorInput) -> None:
        self._source = translation_input.source
        self._target = translation_input.target

    def translate(self, word: str) -> str | None:
        """Translate a single word or text string into the target language.

        Args:
            word: The text string or word to translate.

        Returns:
            The translated string if successful, or None if the translation
            returned an empty result.
        """
        result = ts.translate_text(
            word,
            translator="google",
            from_language=self._source,
            to_language=self._target,
        )
        return result or None


class AITranslatorStrategy:
    def __init__(self, translation_input: TranslatorInput) -> None:
        self._translator = translation_input

    def translate(self, word: str) -> str | None:
        """Translate a single word or text string into the target language.

        Args:
            word: The text string or word to translate.

        Returns:
            The translated string if successful, or None if the translation
            returned an empty result.
        """
        raise NotImplementedError("AI translation is not implemented yet.")


class TranslationTool:
    """Delegates text translation to either a simple engine or an AI-based strategy.

    Attributes:
        _strategy: The active translation strategy instance used to perform translations.
    """

    def __init__(self, translation_input: TranslatorInput) -> None:
        """Initializes the TranslationTool with the appropriate strategy.

        Args:
            translation_input: Configuration containing translation parameters,
                such as source/target languages and whether to enable AI translation.
        """
        self._strategy = self._init_strategy(translation_input)

    def _init_strategy(self, input: TranslatorInput) -> TranslatorStrategy:
        """Instantiates and returns the appropriate translation strategy.

        Args:
            input: The translation configuration and settings.

        Returns:
            An instance of `AITranslatorStrategy` if `input.ai` is True,
            otherwise an instance of `SimpleGoogleTranslatorStrategy`.
        """
        if not input.ai:
            return SimpleGoogleTranslatorStrategy(input)
        return AITranslatorStrategy(input)

    def translate(self, word: str) -> str | None:
        """Translates the given text using the initialized strategy.

        Args:
            word: The text or word to translate.

        Returns:
            The translated string if successful, or None if the translation fails
            or yields an empty result.
        """
        return self._strategy.translate(word)
