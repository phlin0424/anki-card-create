from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

DIR_PATH = Path(__file__).resolve().parent.parent
API_URL = "http://127.0.0.1:8765"
MP3_PATH = DIR_PATH / "data"


class Config(BaseSettings):
    dir_path: Path = Field(
        default=DIR_PATH,
        description="The directory path for the application.",
    )

    mp3_path: Path = Field(
        default=DIR_PATH / "data",
        description="The directory path for the TTS generate audios.",
    )
    api_url: str = Field(
        default=API_URL,
        description="The url for AnkiConnector API",
    )
    deck_name: str = Field(
        default="korean",
        description="Target deck name",
    )
    model_name: str = Field(
        default="Basic (裏表反転カード付き)+sentense",
        description="The model name of the card being sent to Anki.",
    )
    model_config = ConfigDict(protected_namespaces=("settings_",))


settings = Config()
