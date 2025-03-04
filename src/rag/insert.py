import weaviate.classes as wvc

from src.rag.client import client
from src.rag.model import ImageInfo


def setup(collection: str, data: list[ImageInfo]):
    if client.collections.exists(collection):
        client.close()
        raise ValueError(f"Collection {collection} already exists")
    else:
        reports = client.collections.create(
            name=collection,
            vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
            generative_config=wvc.config.Configure.Generative.openai(),  # Ensure the `generative-openai` module is used for generative queries
        )
        # reports = client.collections.create(
        #     name=collection,
        #     vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_ollama(
        #         api_endpoint=config.OLLAMA_ENDPOINT, model=config.OLLAMA_EMBED_MODEL
        #     ),  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        # )#ollamaのベクトル化は後回し
        data_for_insert = [info.model_dump() for info in data]
        reports.data.insert_many(data_for_insert)

if __name__ == "__main__":
    setup("image_sample", [ImageInfo(image_path="src/data/dog.png", info="This is a picture of dog"), ImageInfo(image_path="src/data/cat.png", info="This is a picture of cat")])
    client.close()