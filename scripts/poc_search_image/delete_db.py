import sys

sys.path.append("/home/ri4385/emuni/hack_u_2025/HachU2025-be/")


from src.rag.client import client

if __name__ == "__main__":
    try:
        client.collections.delete_all()
        print("dbを削除しました")
    finally:
        client.close()
