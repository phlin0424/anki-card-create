from pathlib import Path
from typing import Dict

import pytest
from models import AnkiNoteResponse


@pytest.fixture(scope="session")
def global_data() -> Dict[str, str]:
    return {
        "dir_path": Path(__file__).resolve().parent,
        "test_word": "안녕하세요",
        "test_word_in_txt": ["죄송합니다", "이거 얼마예요"],
        "test_file_name": "test_data.txt",
        "deck_name": "test",
        "model_name": "Basic (裏表反転カード付き)+sentense",
        "audio_name": "naver_hello_korean_test.mp3",
    }


@pytest.fixture(scope="session")
def setup_anki_mock(mocker):
    # Sample data to mimic the AnkiConnect response
    expected_response = {
        "result": 1496198395707,
        "error": None,
    }
    # Mock requests.post to return a mock response object with .json() method
    mocker.patch(
        "requests.post",
        return_value=mocker.Mock(status_code=200, json=lambda: expected_response),
    )
    yield mocker


@pytest.fixture(scope="function")
def response_anki_note(global_data):
    # status_code: int
    # result: Union[None, int]
    # error: Union[None, str]
    # deckName: str = DECK_NAME
    # modelName: str = MODEL_NAME
    # front: str
    # back: str = None
    # sentence: Optional[str] = None
    # translated_sentence: Optional[str] = None
    # audio: Optional[str] = None
    # frontLang: str = "ko"
    response_content = {
        "status_code": 200,
        "result": 1496198395707,
        "error": None,
        "deckName": global_data["deck_name"],
        "front": global_data["test_word"],
        "modelName": global_data["model_name"],
    }
    return response_content
