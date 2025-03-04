import weaviate.classes as wvc

from src.rag.client import client
from src.rag.model import ImageInfo
from weaviate.collections.collection import Collection

def setup(collection: str):
    if client.collections.exists(collection):
        client.close()
        raise ValueError(f"Collection {collection} already exists")
    else:
        collection = client.collections.create(
            name=collection,
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
    collection = setup("image_sample")
    assert isinstance(collection, Collection)
    client.close()