import weaviate.classes as wvc
from weaviate.classes.config import Configure, DataType, Multi2VecField, Property
from weaviate.collections.collection import Collection

from src.rag.client import client
from src.rag.search_model import SearchModel


def setup(collection_name: str, search_model: SearchModel = SearchModel.TEXT) -> Collection:
    if client.collections.exists(collection_name):
        print(f"Collection {collection_name} already exists")
        return client.collections.get(collection_name)

    if search_model == SearchModel.IMAGE_TEXT:
        collection = client.collections.create(
            name=collection_name,
            properties=[
                Property(name="info", data_type=DataType.TEXT),
                Property(name="image", data_type=DataType.BLOB),
                Property(name="image_path", data_type=DataType.TEXT),
            ],
            vectorizer_config=[
                Configure.NamedVectors.multi2vec_clip(
                    name="image_sample_vector",
                    # Define the fields to be used for the vectorization - using image_fields, text_fields, video_fields
                    image_fields=[Multi2VecField(name="image", weight=0.9)],
                    text_fields=[
                        Multi2VecField(name="info", weight=0.1),
                        Multi2VecField(
                            name="image_path", weight=0
                        ),  # これは関係ないのでsearchに含めない
                    ],
                )
            ],
            # Additional parameters not shown
        )
    elif search_model == SearchModel.TEXT:
        collection = client.collections.create(
            name=collection_name,
            vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
            generative_config=wvc.config.Configure.Generative.openai(),  # Ensure the `generative-openai` module is used for generative queries
        )
        # collection = client.collections.create(
        #     name=collection,
        #     vectorizer_config=wvc.config.C    onfigure.Vectorizer.text2vec_ollama(
        #         api_endpoint=config.OLLAMA_ENDPOINT, model=config.OLLAMA_EMBED_MODEL
        #     ),  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        # )#ollamaのベクトル化は後回し

    return collection


def setup_base64_collection(
    collection_name: str, search_model: SearchModel = SearchModel.TEXT
) -> Collection:
    """
    Base64のデータを扱うためのcollectionを作成する
    """
    if client.collections.exists(collection_name):
        print(f"Collection {collection_name} already exists")
        return client.collections.get(collection_name)

    if search_model == SearchModel.IMAGE_TEXT:
        collection = client.collections.create(
            name=collection_name,
            properties=[
                Property(name="info", data_type=DataType.TEXT),
                Property(name="base64_content", data_type=DataType.TEXT),
            ],
            vectorizer_config=[
                Configure.NamedVectors.multi2vec_clip(
                    name="image_sample_vector",
                    # Define the fields to be used for the vectorization - using image_fields, text_fields, video_fields
                    image_fields=[Multi2VecField(name="base64_content", weight=0.9)],
                    text_fields=[
                        Multi2VecField(name="info", weight=0.1),
                    ],
                )
            ],
            # Additional parameters not shown
        )
    elif search_model == SearchModel.TEXT:
        collection = client.collections.create(
            name=collection_name,
            vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
            generative_config=wvc.config.Configure.Generative.openai(),  # Ensure the `generative-openai` module is used for generative queries
        )
        # collection = client.collections.create(
        #     name=collection,
        #     vectorizer_config=wvc.config.C    onfigure.Vectorizer.text2vec_ollama(
        #         api_endpoint=config.OLLAMA_ENDPOINT, model=config.OLLAMA_EMBED_MODEL
        #     ),  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        # )#ollamaのベクトル化は後回し

    return collection


if __name__ == "__main__":
    collection = setup("text_search_model_sample", search_model=SearchModel.TEXT)
    assert isinstance(collection, Collection)
    client.close()
