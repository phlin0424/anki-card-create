from card_creator import CardCreator
from models import AnkiNotes


def test_add_note_to_anki(setup_anki_mock, global_data):
    # Assuming 'add_note_to_anki' is a function in your module that makes the post request
    anki_notes = AnkiNotes.from_input_word(
        input_str="죄송합니다",
        deck_name=global_data["deck_name"],
        model_name=global_data["model_name"],
    ).anki_notes

    # Call the function that makes the API request
    card_creator = CardCreator(anki_notes)
    response_list = card_creator.send_notes(audio=False)

    # Check that the response is as expected
    # assert response.json() == expected_response
    assert response_list[0].status_code == 200
