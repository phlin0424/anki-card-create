from src.utils import create_message
from src.models import AnkiSendMediaResponse


def test_create_message(response_anki_note: AnkiSendMediaResponse):
    message = create_message(response_anki_note)
    pass
