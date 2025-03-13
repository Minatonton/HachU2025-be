from weaviate.classes.query import MetadataQuery
from weaviate.collections.classes.internal import QueryReturn
from weaviate.exceptions import WeaviateQueryError

from src.rag.client import client
from src.rag.model import ImageInfo


def search(
    query: str, limit: int = 10, collection_name: str = "text_search_model_sample"
) -> list[ImageInfo]:
    collections = client.collections.get(collection_name)
    if not collections.exists():
        print(f"Collection {collection_name} does not exist")
        return []
    try:
        response = collections.query.near_text(
            query=query,  # The model provider integration will automatically vectorize the query
            limit=limit,
        )
    except WeaviateQueryError:
        print("Perhaps the collection is empty")
        return []
    assert isinstance(response, QueryReturn)
    return [ImageInfo(**obj.properties, id=obj.uuid) for obj in response.objects]  # type: ignore


def search_with_filter(
    query: str,
    limit: int = 10,
    collection_name: str = "text_search_model_sample",
    certainty_threshold: float | None = None,
) -> list[ImageInfo]:  # ベクトル検索
    collections = client.collections.get(collection_name)
    if not collections.exists():
        print(f"Collection {collection_name} does not exist")
        return []
    try:
        response = collections.query.near_text(
            query=query, limit=limit, return_metadata=MetadataQuery.full()
        )
    except WeaviateQueryError:
        print("Perhaps the collection is empty")
        return []
    assert isinstance(response, QueryReturn)

    # 閾値でのフィルター
    if certainty_threshold is not None:
        response.objects = [
            obj
            for obj in response.objects
            if obj.metadata.certainty is not None and certainty_threshold <= obj.metadata.certainty
        ]

    return [ImageInfo(**obj.properties, id=obj.uuid) for obj in response.objects]  # type: ignore


def search_hybrid(
    query: str,
    limit: int = 10,
    collection_name: str = "text_search_model_sample",
    certainty_threshold: float | None = None,
) -> list[ImageInfo]:  # ハイブリッド検索
    collections = client.collections.get(collection_name)
    if not collections.exists():
        print(f"Collection {collection_name} does not exist")
        return []

    try:
        response = collections.query.hybrid(
            query=query, limit=limit, return_metadata=MetadataQuery.full()
        )
    except WeaviateQueryError:
        print("Perhaps the collection is empty")
        return []
    assert isinstance(response, QueryReturn)

    # 閾値でのフィルター
    if certainty_threshold is not None:
        response.objects = [
            obj
            for obj in response.objects
            if obj.metadata.certainty is not None and certainty_threshold <= obj.metadata.certainty
        ]

    return [ImageInfo(**obj.properties, id=obj.uuid) for obj in response.objects]  # type: ignore


def search_bm25(
    query: str,
    limit: int = 10,
    collection_name: str = "text_search_model_sample",
    certainty_threshold: float | None = None,
) -> list[ImageInfo]:  # BM25
    collections = client.collections.get(collection_name)
    if not collections.exists():
        print(f"Collection {collection_name} does not exist")
        return []
    try:
        response = collections.query.bm25(
            query=query, limit=limit, return_metadata=MetadataQuery.full()
        )
    except WeaviateQueryError:
        print("Perhaps the collection is empty")
        return []
    assert isinstance(response, QueryReturn)

    # 閾値でのフィルター
    if certainty_threshold is not None:
        response.objects = [
            obj
            for obj in response.objects
            if obj.metadata.certainty is not None and certainty_threshold <= obj.metadata.certainty
        ]

    return [ImageInfo(**obj.properties, id=obj.uuid) for obj in response.objects]  # type: ignore


if __name__ == "__main__":
    queries = [
        "dog",
        "cat",
    ]
    for query in queries:
        print(query)
        print("search result:", search(query, 1))
        print("search_with_filter result:", search_with_filter(query, 1))
        print("search_hybrid result:", search_hybrid(query, 1))
        print("search_bm25 result:", search_bm25(query, 1))
    client.close()
