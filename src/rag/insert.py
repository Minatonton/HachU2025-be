import weaviate.classes as wvc

from src.rag.client import client
from src.rag.model import ImageInfo
from weaviate.collections.collection import Collection
from src.rag.setup import setup
import base64
from src.rag.search_model import SearchModel

def to_base64(image_path: str) -> str:
    """画像をbase64に変換する"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def insert(collection: Collection, data: list[ImageInfo],search_model:SearchModel=SearchModel.IMAGE_TEXT)->None:
    if search_model == SearchModel.IMAGE_TEXT:
        with collection.batch.dynamic() as batch:
            for src_obj in data:
                poster_b64 = to_base64(src_obj.image_path)
                weaviate_obj = {
                    "info": src_obj.info,
                    "image": poster_b64,  # Add the image in base64 encoding
                    "image_path": src_obj.image_path
                }

                # The model provider integration will automatically vectorize the object
                batch.add_object(
                    properties=weaviate_obj,
                    # vector=vector  # Optionally provide a pre-obtained vector
                    )

    elif search_model == SearchModel.TEXT:
        data_for_insert = [info.model_dump() for info in data]
        collection.data.insert_many(data_for_insert)

if __name__ == "__main__":
    search_model=SearchModel.TEXT
    data = [ImageInfo(image_path="src/data/dog.png", info="This is a picture of dog"), ImageInfo(image_path="src/data/cat.png", info="This is a picture of cat")]
    collection = setup("text_mode_sample",search_model=search_model)
    insert(collection, data,search_model=search_model)
    client.close()