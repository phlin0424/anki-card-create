from translation import TranslationTool, TranslatorModel


def test_translation_tool():
    tool = TranslationTool(TranslatorModel(source="ko", target="ja", ai=False))
    assert tool.translate("안녕") == "こんにちは"
