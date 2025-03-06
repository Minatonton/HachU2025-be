import base64


def to_base64(image_path: str) -> str:
    """画像をbase64に変換する"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
