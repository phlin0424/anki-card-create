from models import AnkiNoteModel, AnkiNotes
import logging

logger = logging.getLogger(__name__)


def test_anki_note_model():
    """TESTCASE1: Create a note by manually input the text"""
    note = AnkiNoteModel(
        deckName="korean",
        modelName="Basic (裏表反転カード付き)+sentense",
        front="안녕하세요",
        back="こんにちは",
    )

    assert note.deckName == "korean"
    assert note.modelName == "Basic (裏表反転カード付き)+sentense"
    assert note.front == "안녕하세요"
    assert note.back == "こんにちは"
    assert note.frontLang == "ko"


def test_anki_note_model_no_back():
    """TESTCASE2: Create a note by manually input the text without back"""

    note = AnkiNoteModel(
        deckName="korean",
        modelName="Basic (裏表反転カード付き)+sentense",
        front="안녕하세요",
    )

    assert note.deckName == "korean"
    assert note.modelName == "Basic (裏表反転カード付き)+sentense"
    assert note.front == "안녕하세요"
    assert note.frontLang == "ko"


def test_create_anki_notes_from_txt(global_data, create_test_data):
    """TESTCASE3: Create anki notes from a given txt file."""
    logger.info("TESTCASE3")
    logger.info(global_data["dir_path"] / global_data["test_file_name"])

    anki_notes = AnkiNotes.from_txt(
        data_fname=global_data["dir_path"] / global_data["test_file_name"],
    ).anki_notes

    assert len(anki_notes) == 2
    assert anki_notes[0].front == "죄송합니다"
    assert anki_notes[1].front == "이거 얼마예요"
    assert anki_notes[0].back == "ごめん"
    assert anki_notes[1].back == "いくらですか"


def test_create_anki_notes_from_input(global_data):
    """TESTCASE4: Create anki notes from a single input"""

    anki_notes = AnkiNotes.from_input_word(
        input_str="죄송합니다",
        deck_name=global_data["deck_name"],
        model_name=global_data["model_name"],
    ).anki_notes
    assert len(anki_notes) == 1
    assert anki_notes[0].front == "죄송합니다"
    assert anki_notes[0].back == "ごめん"
