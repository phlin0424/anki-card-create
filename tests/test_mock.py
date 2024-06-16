from src.card_creator import AnkiNotes, CardCreator


def test_add_note_to_anki(mocker, global_data):
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
    assert response_list[0].result == expected_response["result"]
    assert response_list[0].error == expected_response["error"]
    assert response_list[0].status_code == 200
