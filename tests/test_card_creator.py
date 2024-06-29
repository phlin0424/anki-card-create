import os

import pytest
from card_creator import AnkiNotes, CardCreator
from navertts import NaverTTS


@pytest.fixture(scope="module")
def create_test_data(global_data) -> None:
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


def test_create_anki_notes_from_txt(global_data, create_test_data):
    """TESTCASE1: Create anki notes from a given txt file."""
    anki_notes = AnkiNotes.from_txt(
        data_fname=global_data["dir_path"] / global_data["test_file_name"],
    ).anki_notes
    assert len(anki_notes) == 2
    assert anki_notes[0].front == "죄송합니다"
    assert anki_notes[1].front == "이거 얼마예요"
    assert anki_notes[0].back == "ごめん"
    assert anki_notes[1].back == "いくらですか"


def test_create_anki_notes_from_input(global_data):
    """TESTCASE2: Create anki notes from a single input"""
    anki_notes = AnkiNotes.from_input_word(
        input_str="죄송합니다",
        deck_name=global_data["deck_name"],
        model_name=global_data["model_name"],
    ).anki_notes
    assert len(anki_notes) == 1
    assert anki_notes[0].front == "죄송합니다"
    assert anki_notes[0].back == "ごめん"


def test_send_anki_note_not_audio(global_data, create_test_data):
    """TESTCASE3: Send the created notes to the specified deck, without generating audios"""
    anki_notes = AnkiNotes.from_txt(
        data_fname=global_data["dir_path"] / global_data["test_file_name"],
        deck_name=global_data["deck_name"],
        model_name=global_data["model_name"],
    ).anki_notes
    card_creator = CardCreator(anki_notes)

    response_list = card_creator.send_notes(audio=False)
    assert len(response_list) == 2
    assert response_list[0].status_code == 200
    assert response_list[1].status_code == 200


def test_send_audio(global_data, create_test_audio):
    """TESTCASE4: Send the audio files to the Anki collection directory, without attaching it to the ankicard"""
    audio_path = global_data["dir_path"] / create_test_audio
    anki_notes = AnkiNotes.from_input_word(
        input_str="죄송합니다",
        deck_name=global_data["deck_name"],
        model_name=global_data["model_name"],
    ).anki_notes
    card_creator = CardCreator(anki_notes)

    response = card_creator.send_media(audio_path)
    assert response.error is None
    assert response.audio_file_name == global_data["audio_name"]


def test_send_anki_note_with_audio(global_data):
    """TESTCASE5: Create an Anki card with audio"""

    anki_notes = AnkiNotes.from_input_word(
        input_str=global_data["test_word"],
        deck_name=global_data["deck_name"],
        model_name=global_data["model_name"],
    ).anki_notes
    card_creator = CardCreator(anki_notes)
    response_list = card_creator.send_notes(audio=True)

    assert response_list[0].status_code == 200
