from src.rag.client import client

if __name__ == "__main__":
    try:
        client.collections.delete_all()
        print("dbを削除しました")
    finally:
        client.close()
