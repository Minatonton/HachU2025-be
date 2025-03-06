from pathlib import Path

from scripts.image_to_text import get_text_from_image
from src.rag import insert, setup
from src.rag.client import client
from src.rag.model import ImageInfo
from src.rag.search_model import SearchModel


def get_dog_cat_data() -> list[ImageInfo]:
    data: list[ImageInfo] = [
        ImageInfo(image_path="src/data/dog.png", info="犬の写真だよ"),
        ImageInfo(image_path="src/data/cat.png", info="猫の写真だよ"),
    ]
    return data


def get_data_1() -> list[ImageInfo]:
    """お城とオムライスの写真で精度検証"""
    data: list[ImageInfo] = []

    img_path_list: list[Path] = [
        Path("scripts/poc_search_image/data/IMG_1611.jpg"),  # 松本城
        Path("scripts/poc_search_image/data/IMG_1755.jpg"),  # オムライス
    ]

    for img_path in img_path_list:
        img_description = get_text_from_image(img_path)
        print(img_description)
        data.append(ImageInfo(image_path=str(img_path), info=img_description))
    return data


def get_data_1_no_api() -> list[ImageInfo]:
    data: list[ImageInfo] = [
        ImageInfo(
            image_path="scripts/poc_search_image/data/IMG_1611.jpg",
            info="この画像には、コンサートホールの内部が写っています。ステージには椅子や楽器が並べられており、コンサートの準備が行われているようです。観客席には人々が座っており、ホールの構造が見えます。背景には大きなパイプオルガンも見えます。",
        ),
        ImageInfo(
            image_path="scripts/poc_search_image/data/IMG_1755.jpg",
            info="これはオムライスの画像です。卵がご飯の上に乗っていて、デミグラスソースがかかっています。スプーンも添えられていますね。",
        ),
    ]
    return data


def get_data_2() -> list[ImageInfo]:
    """もっといろんな写真"""
    data: list[ImageInfo] = []
    img_path_list: list[Path] = [
        Path("scripts/poc_search_image/data/IMG_1611.jpg"),
        Path("scripts/poc_search_image/data/IMG_1699.jpg"),
        Path("scripts/poc_search_image/data/IMG_1702.jpg"),
        Path("scripts/poc_search_image/data/IMG_1730.jpg"),
        Path("scripts/poc_search_image/data/IMG_1747.jpg"),
        Path("scripts/poc_search_image/data/IMG_1755.jpg"),
    ]

    for img_path in img_path_list:
        img_description = get_text_from_image(img_path)
        print(img_description)
        data.append(ImageInfo(image_path=str(img_path), info=img_description))
    return data


if __name__ == "__main__":
    try:
        search_model = SearchModel.TEXT
        collection = setup.setup("text_search_model_sample", search_model)
        data = get_data_2()
        insert.insert(collection, data, search_model=search_model)
        print("dbできたよ")
    finally:
        client.close()
