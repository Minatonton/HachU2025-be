import base64
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def encode_image(image_path: Path) -> str:
    """base64にenocode"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_text_from_image(image_path: Path) -> str:
    """openaiのapiでimageをtext化する"""

    base64_image = encode_image(image_path)
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "この画像には何が写っていますか?",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    image_path: Path = Path("src/data/cat.png")
    text = get_text_from_image(image_path)
    print(text)
