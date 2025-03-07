from src.rag import search
from src.rag.client import client

if __name__ == "__main__":
    try:
        collections = client.collections.get("text_search_model_sample")
        print(collections.config)
        query = "そばがたべたい"
        img_info = search.search(query, limit=1)
        print(img_info[0].info)
    finally:
        client.close()
