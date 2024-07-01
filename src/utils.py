import uuid
from pathlib import Path
from typing import Union

from config import settings
from models import AnkiNoteResponse, AnkiSendMediaResponse
from navertts import NaverTTS


def create_message(card_create_response: AnkiNoteResponse) -> str:
    """Generate a readable message based on the response of Anki connector after sending the notes.

    Args:
        card_create_response (AnkiNoteResponse): _description_

    Returns:
        str: The message.
    """
    # Check if the deck exists and the note was added successfully
    if card_create_response.status_code == 200:
        word_being_sent = f"{card_create_response.front}, {card_create_response.back}"
        if card_create_response.error is not None:
            # Check if the error message indicates that the deck does not exist
            if "deck not found" in card_create_response.error:
                return word_being_sent + ":Error: Deck does not exist"
            else:
                return word_being_sent + f": Error: {card_create_response.error}"
        else:
            return word_being_sent + ": Note added successfully"
    else:
        return word_being_sent + ": Error adding note to deck"


def create_audio(
    text: str, path: Union[Path, str] = settings.mp3_path
) -> Union[Path, str]:
    """Create an audio file (.mp3) for the input korean word. Based on Naver TTS API.

    Args:
        text (str): Korean word.
        path (Union[Path, str], optional): _description_. Defaults to MP3_PATH.

    Returns:
        Union[Path, str]: The path of the output audio file.
            For example: User/path/to/directory/naver_e9633695-8fce-4ea3-901a-489863a9214e.mp3
    """
    # texts = [note.front for note in self._anki_notes]
    if not isinstance(path, Path):
        path = Path(path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    tts = NaverTTS(text)
    audio_filename = path / f"naver_{uuid.uuid4()}.mp3"
    tts.save(audio_filename)
    return audio_filename


class MediaAdditionError(Exception):
    """Exception raised when adding media fails."""

    def __init__(self, response: AnkiSendMediaResponse, message="Failed to add media"):
        self.status_code = response.status_code
        message = response.error
        self.message = f"{message}. Status code: {self.status_code}"
        super().__init__(self.message)
