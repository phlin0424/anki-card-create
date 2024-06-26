from models import AnkiNoteModel


def test_anki_note_model():
    """test 1: Create a note by manually input the text"""
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
    """test 2: Create a note by manually input the text without back"""
    note = AnkiNoteModel(
        deckName="korean",
        modelName="Basic (裏表反転カード付き)+sentense",
        front="안녕하세요",
    )

    assert note.deckName == "korean"
    assert note.modelName == "Basic (裏表反転カード付き)+sentense"
    assert note.front == "안녕하세요"
    assert note.frontLang == "ko"
