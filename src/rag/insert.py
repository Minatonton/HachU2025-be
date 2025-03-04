import weaviate.classes as wvc

from src.rag.client import client
from src.rag.model import ImageInfo
from weaviate.collections.collection import Collection
from src.rag.setup import setup

def insert(collection: Collection, data: list[ImageInfo]):
    data_for_insert = [info.model_dump() for info in data]
    collection.data.insert_many(data_for_insert)

if __name__ == "__main__":
    data = [ImageInfo(image_path="src/data/dog.png", info="This is a picture of dog"), ImageInfo(image_path="src/data/cat.png", info="This is a picture of cat")]
    collection = setup("image_sample")
    insert(collection, data)
    client.close()