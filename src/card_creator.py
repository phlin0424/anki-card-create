import json
import logging
import os
from pathlib import Path
from typing import List

import requests
from config import settings
from models import AnkiNoteModel, AnkiNoteResponse, AnkiSendMediaResponse
from requests import Response
from utils import MediaAdditionError, create_audio, create_message

logging.basicConfig(level=logging.INFO)


def anki_invoke(action: str, params: dict):
    response: Response = requests.post(
        settings.api_url,
        json={"action": action, "version": 6, "params": params},
    )
    return response


class CardCreator:
    def __init__(self, anki_notes: List[AnkiNoteModel]):
        self._anki_notes = anki_notes

    @property
    def anki_notes(self):
        return self._anki_notes

    @staticmethod
    def create_response(
        anki_note: AnkiNoteResponse,
        connector_response: requests.Response,
        audio: str = None,
    ) -> AnkiNoteResponse:
        response_json = connector_response.json()
        response_json["status_code"] = connector_response.status_code

        anki_note_dict = anki_note.model_dump()
        anki_note_dict.update(
            {
                "status_code": response_json["status_code"],
                "audio": audio,
                "result": response_json["result"],
                "error": response_json["error"],
            }
        )

        return AnkiNoteResponse(**anki_note_dict)

    @staticmethod
    def send_media(audio_path: Path | str) -> AnkiSendMediaResponse:
        """Send the created mp3 file to Anki collection folder (collection.media/)

        Args:
            audio_path (Union[Path, str]): _description_

        Returns:
            _type_: _description_
        """
        # Convert the path into a Path datatype
        if not isinstance(audio_path, Path):
            audio_path = Path(audio_path)

        # Create the payload fot the anki connector request
        audio_filename = audio_path.name.__str__()
        audio_file_path = audio_path.__str__()
        params = {
            "filename": audio_filename,
            "path": audio_file_path,
        }

        # Send the request
        response = anki_invoke(action="storeMediaFile", params=params)

        return AnkiSendMediaResponse(
            audio_path=audio_file_path,
            audio_file_name=audio_filename,
            status_code=response.status_code,
            result=json.loads(response.text)["result"],
            error=json.loads(response.text)["error"],
        )

    def send_notes(self, audio: bool = True) -> List[AnkiNoteResponse]:
        response_json_list = []
        for anki_note in self._anki_notes:
            audio_str = ""
            if audio:
                # Create the mp3 file
                audio_path = create_audio(anki_note.front)

                # Send the mp3 to Anki's media folder
                media_response = self.send_media(audio_path)
                if media_response.error is not None:
                    raise MediaAdditionError(media_response)

                # Create a str for denoting the media file
                audio_str = f"[sound:{media_response.audio_file_name}]"

                # remove the audio file that has been sent:
                os.remove(audio_path)

            # Create the Anki payload based on the created anki-note
            note = {
                "deckName": anki_note.deckName,
                "modelName": anki_note.modelName,
                "fields": {
                    "表面": anki_note.front + audio_str,
                    "裏面": anki_note.back,
                },
            }
            params = {"note": note}

            # Send the request to add note into the specified deck, using anki connector
            response = anki_invoke(action="addNote", params=params)

            # Translate the process result to a readable message
            if audio:
                card_create_response = self.create_response(
                    anki_note=anki_note,
                    connector_response=response,
                    audio=media_response.audio_file_name,
                )
            else:
                card_create_response = self.create_response(
                    anki_note=anki_note,
                    connector_response=response,
                )
            # Append the response message into a list
            response_json_list.append(card_create_response)

            # Logging the response of creating the cards
            logging.info(
                create_message(
                    card_create_response,
                )
            )

            # Logging the created audio name of the audio flag is specified
            if audio:
                logging.info(f"audio: {media_response.audio_file_name}")

        return response_json_list
