import base64
import io

import requests
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

load_dotenv()


def image_url_to_base64(image_url, max_width=400, max_height=200, quality=75):
    response = requests.get(image_url)
    if response.status_code == 200:
        image = Image.open(io.BytesIO(response.content))

        # 画像をリサイズ（長辺がmax_width or max_height以下）
        image.thumbnail((max_width, max_height))

        # 画像を圧縮してBase64に変換
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG", quality=quality)  # JPEG形式 & 画質圧縮
        return base64.b64encode(buffered.getvalue()).decode()

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
