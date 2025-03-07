import base64

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def to_base64(image_path: str) -> str:
    """画像をbase64に変換する"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_text_from_image(image_path: str) -> str:
    """openaiのapiでimageをtext化する"""

    base64_image = to_base64(image_path)
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

    assert isinstance(response.choices[0].message.content, str)

    return response.choices[0].message.content


def get_text_from_base64(base64_content: str) -> str:
    """openaiのapiでbase64のimageをtext化する"""

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
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_content}"},
                    },
                ],
            }
        ],
    )

    assert isinstance(response.choices[0].message.content, str)

    return response.choices[0].message.content
