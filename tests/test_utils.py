from anki_card_create.models.kanki_input import KankiInput
from anki_card_create.models.translator_input import TranslatorInput
from anki_card_create.services.translators import TranslationTool


def test_translation_tool() -> None:
    """TESTCASE1: Test the translation tool."""
    tool = TranslationTool(TranslatorInput(source="ko", target="ja", ai=False))
    assert tool.translate("안녕") == "こんにちは"


def test_create_anki_notes_from_input(global_data) -> None:
    """TESTCASE2: Create anki notes from a single input and generate the translation automatically."""
    anki_notes = KankiInput.from_input_word(
        input_str="죄송합니다",
        deck_name=global_data["deck_name"],
        model_name=global_data["model_name"],
    ).anki_notes
    assert len(anki_notes) == 1
    assert anki_notes[0].front == "죄송합니다"
    assert anki_notes[0].back == "申し訳ありません"
