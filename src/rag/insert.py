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
    search_model = SearchModel.TEXT
    data = [
        ImageInfo(
            id=uuid4(),
            image_url="https://www.illust-box.jp/db_img/sozai/00010/108487/watermark.jpg",
            info="This is a picture of dog",
        ),
        ImageInfo(
            id=uuid4(),
            image_url="https://png.pngtree.com/png-clipart/20230623/original/pngtree-happy-cute-cat-vector-png-image_9205055.png",
            info="This is a picture of cat",
        ),
    ]
    collection = setup("text_search_model_sample", search_model=search_model)
    insert(collection, data, search_model=search_model)
    client.close()
