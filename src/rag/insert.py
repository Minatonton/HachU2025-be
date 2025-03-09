from uuid import uuid4

from weaviate.collections.collection import Collection

from src.rag.client import client
from src.rag.model import ImageInfo
from src.rag.search_model import SearchModel
from src.rag.setup import setup
from src.rag.utils import to_base64


def insert(
    collection: Collection,
    data: list[ImageInfo],
    search_model: SearchModel = SearchModel.IMAGE_TEXT,
) -> None:
    if search_model == SearchModel.IMAGE_TEXT:
        with collection.batch.dynamic() as batch:
            for src_obj in data:
                poster_b64 = to_base64(src_obj.image_path)
                weaviate_obj = {
                    "info": src_obj.info,
                    "image": poster_b64,  # Add the image in base64 encoding
                    "image_path": src_obj.image_path,
                }
                # The model provider integration will automatically vectorize the object
                batch.add_object(
                    properties=weaviate_obj,
                    uuid=str(src_obj.id),
                    # vector=vector  # Optionally provide a pre-obtained vector
                )

    elif search_model == SearchModel.TEXT:
        for src_obj in data:
            collection.add_object(
                properties={"info": src_obj.info, "image_path": src_obj.image_path},
                uuid=str(src_obj.id),
            )


if __name__ == "__main__":
    search_model = SearchModel.TEXT
    data = [
        ImageInfo(id=uuid4(), image_path="src/data/dog.png", info="This is a picture of dog"),
        ImageInfo(id=uuid4(), image_path="src/data/cat.png", info="This is a picture of cat"),
    ]
    collection = setup("text_search_model_sample", search_model=search_model)
    insert(collection, data, search_model=search_model)
    client.close()
