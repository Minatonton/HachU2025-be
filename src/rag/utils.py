import base64

import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def image_url_to_base64(image_url):
    """画像のurlをbase64に変換する"""
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = response.content
        base64_encoded = base64.b64encode(image_data).decode("utf-8")
        return base64_encoded
    raise Exception(f"Failed to fetch image, status code: {response.status_code}")


def get_text_from_image_url(image_url: str) -> str:
    """openaiのapiでimage(url)をtext化する"""
    base64_image = image_url_to_base64(image_url)
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
