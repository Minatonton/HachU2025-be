import weaviate
from weaviate.config import AdditionalConfig, ConnectionConfig


def check_connection(client):
    try:
        if client.is_ready():
            print("✅ Weaviate is reachable!")
        else:
            print("⚠️ Weaviate is not ready.")
    except Exception as e:
        print(f"❌ Connection error: {e}")


if __name__ == "__main__":
    client = weaviate.connect_to_local(
        host="localhost",
        headers={"X-OpenAI-Api-Key": "OPENAIAI_KEY"},
        additional_config=AdditionalConfig(
            connection=ConnectionConfig(
                session_pool_connections=30,
                session_pool_maxsize=200,
                session_pool_max_retries=3,
            ),
            timeout=(6000, 18000),
        ),
    )

    check_connection(client)

    client.close()
