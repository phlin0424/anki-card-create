from pathlib import Path
from typing import Dict

import pytest
import os
from navertts import NaverTTS


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


@pytest.fixture(scope="function")
def setup_anki_mock(mocker, response_anki_note):
    # Mock requests.post to return a mock response object with .json() method
    mock_anki_invoke = mocker.patch("card_creator.anki_invoke")

    # Define the side effect function to handle different actions
    def anki_invoke_side_effect(action, params):
        if action == "addNote":
            expected_response = {
                "result": 1496198395707,
                "error": None,
            }
            return mocker.Mock(status_code=200, json=lambda: expected_response)
        elif action == "storeMediaFile":
            expected_response = {
                "result": "test.mp3",
                "error": None,
            }
            return mocker.Mock(status_code=200, json=lambda: expected_response)
        return mocker.Mock(status_code=400, json={"error": "not expected actions"})

    mock_anki_invoke.side_effect = anki_invoke_side_effect

    yield mocker


@pytest.fixture(scope="module")
def create_test_data(global_data) -> None:
    """create the test data at the file path being specified"""
    input_word = global_data["test_word_in_txt"]
    file_path = global_data["dir_path"] / global_data["test_file_name"]
    with open(file_path, "w") as f:
        for i, word in enumerate(input_word):
            if i > 0:
                f.write("\n")
            f.write(word)
    yield
    os.remove(file_path)  # Cleanup after the module tests are done


@pytest.fixture(scope="module")
def create_test_audio(global_data) -> str:
    tts = NaverTTS(global_data["test_word"])
    audio_name = global_data["dir_path"] / global_data["audio_name"]
    tts.save(audio_name)
    yield audio_name
    os.remove(audio_name)  # Cleanup after the module tests are done
