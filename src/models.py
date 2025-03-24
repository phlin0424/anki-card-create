from pathlib import Path
from typing import List, Optional

from config import settings
from langdetect import detect
from pydantic import BaseModel, ConfigDict, model_validator
from schemas import InputLang, TranslatedLang
from translation import TranslationTool, TranslatorModel


class AnkiNoteModel(BaseModel):
    """Schema for the input to create an Anki card.

    Args:
        BaseModel (_type_): _description_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """

    deckName: str = settings.deck_name
    modelName: str = settings.model_name
    front: str
    back: str = None
    sentence: Optional[str] = None
    translated_sentence: Optional[str] = None
    audio: Optional[str] = None
    frontLang: InputLang = settings.using_lang
    backLang: TranslatedLang = settings.translate_lang

    @model_validator(mode="after")
    def check_languages(self):
        front_lang = self.frontLang
        # back_lang = self.backLang

        # Detect languages of `front` and `back` fields
        detected_front_lang = detect(self.front)
        # detected_back_lang = detect(self.back)

        # Validate detected languages against expected languages
        if front_lang != detected_front_lang:
            raise ValueError(
                f"Expected language for 'front' field is '{front_lang}', but detected '{detected_front_lang}'."
            )

        return self


class AnkiNotes(BaseModel):
    """A schema for the input of Kanki command line."""

    # A List for the created Anki notes.
    anki_notes: List[AnkiNoteModel]
    model_config = ConfigDict(protected_namespaces=("settings_",))

    @classmethod
    def from_input_word(
        cls,
        input_str: str,
        translated_word: str = None,
        deck_name: str = settings.deck_name,
        model_name: str = settings.model_name,
    ) -> "AnkiNotes":
        """Create a single Ankinote that will be sent to Anki via an input word (str).

        Args:
            input_str (str): A string of the front word.
            translated_word (str, optional): Back word of the Anki note. Defaults to None.
            deck_name (str, optional): The deck name that the created note will be sent. Defaults to settings.deck_name.
            model_name (str, optional): The model name that will be used to format the created note. Defaults to settings.model_name.

        Returns:
            _type_: _description_
        """
        # Create the Anki note model
        if translated_word is None:
            # If the translated word is not provided
            # Validate the language of the word in the same time
            anki_note = AnkiNoteModel(
                deckName=deck_name,
                modelName=model_name,
                front=input_str,
            )

            # Create a translator
            translator_settings = TranslatorModel(
                source=settings.using_lang,
                target=settings.translate_lang,
                ai=settings.ai,
            )
            translator = TranslationTool(translator_settings)

            # Execute translation
            translated_word = translator.translate(anki_note.front)

            # Fill the translated word into the anki note
            anki_note.back = translated_word

        else:
            # If the translated word is provided
            anki_note = AnkiNoteModel(
                deckName=deck_name,
                modelName=model_name,
                front=input_str,
                back=translated_word,
            )

        anki_notes_list = [anki_note]
        return cls(anki_notes=anki_notes_list)

    @classmethod
    def from_txt(
        cls,
        data_fname: str | Path = settings.dir_path / "data" / "example.txt",
        deck_name: str = settings.deck_name,
        model_name: str = settings.model_name,
    ) -> "AnkiNotes":
        """Create a list of Anki note based on a file which contains multiple words.
        The translated words will be automatically generated from the korean word
        listed on the front side.

        Args:
            data_fname (str, optional): The input file path. Defaults to settings.dir_path/"data"/"example.txt".
            deck_name (str, optional): The deck name that the created note will be sent. Defaults to settings.deck_name.
            model_name (str, optional): The model name that will be used to format the created note. Defaults to settings.model_name.

        Returns:
            AnkiNotes: _description_
        """

        # Read the vocabularies from a given text file
        with open(data_fname, "r") as f:
            rows = f.read().split("\n")

        # Allowing reading translated words if being given
        voc_list = []
        translated_list = []
        for n, row in enumerate(rows):
            split_row = row.split(",")
            if len(split_row) == 2:
                voc_list.append(split_row[0])
                translated_list.append(split_row[1])
            elif len(split_row) == 1:
                voc_list.append(split_row[0])
                translated_list.append(None)
            else:
                raise ValueError(
                    f"Format of input file is not available at line {n+1}: {row}"
                )

        # Create a translator for translating the word
        translator_settings = TranslatorModel(
            source=settings.using_lang, target=settings.translate_lang, ai=settings.ai
        )
        translator = TranslationTool(translator_settings)

        # Create anki notes one by one
        anki_notes_list = []
        for word, translated in zip(voc_list, translated_list):
            # Validate the read word first.
            # It the word is not korean, raising errors
            anki_note = AnkiNoteModel(
                deckName=deck_name,
                modelName=model_name,
                front=word,
            )

            # Create the back side (translation) of the Ankinote
            if not translated:
                # Translate the word into japanese if translated word is not provided
                translated = translator.translate(word)

            anki_note.back = translated

            # Append the anki note into a list
            anki_notes_list.append(anki_note)

        return cls(anki_notes=anki_notes_list)


class AnkiNoteResponse(AnkiNoteModel):
    """Response model for sending the created notes to the Anki DB."""

    status_code: int
    result: None | int
    error: None | str
    audio: Optional[None | str]
    model_config = ConfigDict(from_attributes=True)


class AnkiSendMediaResponse(BaseModel):
    """Response after sending the created mp3 file to Anki collection folder"""

    audio_path: str
    audio_file_name: str
    status_code: int
    result: None | str = None
    error: None | str = None
