from typing import Optional

from config import settings
from langdetect import detect
from pydantic import BaseModel, model_validator, ConfigDict
from config import settings
from googletrans import Translator
from typing import List
from pathlib import Path


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
    frontLang: str = "ko"  # Default expected language for the 'front' field

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


class AnkiNoteResponse(AnkiNoteModel):
    status_code: int
    result: None | int
    error: None | str
    audio: Optional[None | str]
    model_config = ConfigDict(from_attributes=True)


class AnkiSendMediaResponse(BaseModel):
    audio_path: str
    audio_file_name: str
    status_code: int
    result: None | str = None
    error: None | str = None


class AnkiNotes(BaseModel):
    """A schema for the input of CardCreator"""

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
        # Translate the word if the "back" field is not specified.
        if translated_word is None:
            translator = Translator()
            translation = translator.translate(input_str, src="ko", dest="ja")
            translated_word = translation.text

        # Create the Anki note model
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

        with open(data_fname, "r") as f:
            voc_list = f.read().split("\n")

        translator = Translator()

        anki_notes_list = []
        for word in voc_list:
            translation = translator.translate(word, src="ko", dest="ja")
            translated_word = translation.text
            anki_note = AnkiNoteModel(
                deckName=deck_name,
                modelName=model_name,
                front=word,
                back=translated_word,
            )
            anki_notes_list.append(anki_note)

        return cls(anki_notes=anki_notes_list)
