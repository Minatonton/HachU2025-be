from uuid import uuid4

from weaviate.collections.collection import Collection

from src.rag.client import client
from src.rag.model import ImageInfo
from src.rag.search_model import SearchModel
from src.rag.setup import setup
from src.rag.utils import image_url_to_base64


def insert(
    collection: Collection,
    data: list[ImageInfo],
    search_model: SearchModel = SearchModel.IMAGE_TEXT,
) -> None:
    if search_model == SearchModel.IMAGE_TEXT:
        with collection.batch.dynamic() as batch:
            for src_obj in data:
                poster_b64 = image_url_to_base64(src_obj.image_url)
                weaviate_obj = {
                    "info": src_obj.info,
                    "image": poster_b64,  # Add the image in base64 encoding
                    "image_url": src_obj.image_url,
                }
                # The model provider integration will automatically vectorize the object
                batch.add_object(
                    properties=weaviate_obj,
                    uuid=str(src_obj.id),
                    # vector=vector  # Optionally provide a pre-obtained vector
                )

    elif search_model == SearchModel.TEXT:
        for src_obj in data:
            collection.data.insert(
                properties={"info": src_obj.info, "image_url": src_obj.image_url},
                uuid=str(src_obj.id),
            )


if __name__ == "__main__":
    search_model = SearchModel.IMAGE_TEXT
    data = [
        ImageInfo(
            id=uuid4(),
            image_url="https://plus.unsplash.com/premium_photo-1666777247416-ee7a95235559?q=80&w=2574&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            info="This is a picture of dog",
        ),
    ]
    collection = setup("image_search_model_sample", search_model=search_model)
    insert(collection, data, search_model=search_model)
    client.close()
