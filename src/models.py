from typing import Optional, Union

from langdetect import detect
from pydantic import BaseModel, model_validator

from src import DECK_NAME, MODEL_NAME


class AnkiNoteModel(BaseModel):
    deckName: str = DECK_NAME
    modelName: str = MODEL_NAME
    front: str
    back: str = None
    sentence: Optional[str] = None
    translated_sentence: Optional[str] = None
    audio: Optional[str] = None
    frontLang: str = "ko"  # Default expected language for the 'front' field
    # backLang: str = [
    #     "ja",
    #     "ko",
    #     "zh-tw",
    #     "zh-cn",
    # ]  # Default expected language for the 'back' field

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

        # if detected_back_lang not in back_lang:
        #     raise ValueError(
        #         f"Expected language for 'back' field is '{back_lang}', but detected '{detected_back_lang}'."
        #     )

        return self


class AnkiNoteResponse(AnkiNoteModel):
    status_code: int
    result: Union[None, int]
    error: Union[None, str]

    class Config:
        from_attributes = True


class AnkiSendMediaResponse(BaseModel):
    audio_path: str
    audio_file_name: str
    status_code: int
    result: Union[None, str] = None
    error: Union[None, str] = None
