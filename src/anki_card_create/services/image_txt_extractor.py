import logging

from google import genai
from google.genai import types
from PIL import Image

logger = logging.getLogger(__name__)


class ImageTxtExtractor:
    def __init__(self, api_key: str | None = None) -> None:
        self.client = genai.Client(api_key=api_key)

    def extract_text(self, img_path: str) -> str | None:
        """Extract text from image using Google Gen AI. The output is in CSV format.

        Args:
            img_path (str): The path to the image file.

        Returns:
            str: The extracted text from the image.
        """
        user_prompt = (
            "この画像を分析し、含まれる韓国語の単語をメインに抽出し、韓国語と日本語を並べてCSV形式で出力してください。"
        )
        system_instruction = """
        あなたは、ユーザーの要求に応じて画像の内容を分析し、その結果を他のテキストを含まずに、純粋なCSVデータのみで返すAIです。
        出力をCSV形式（列の区切り文字はカンマ、行の区切り文字は改行）に厳密に従ってください。出力には、説明や追加のコメント、コードブロック（```csv...```）
        を含めないでください。"""

        try:
            img = Image.open(img_path)
        except FileNotFoundError:
            logger.info("Error: Image file not found.")

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[user_prompt, img],
            config=types.GenerateContentConfig(system_instruction=system_instruction),
        )

        return response.text
