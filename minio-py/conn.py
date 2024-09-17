from minio import Minio

def connect():
    Minio(
        "localhost:9000",
        access_key="SBf9qUCTCs93oFuXJrWi",
        secret_key="60k62Dzl39qdBCBvMgbnoQsrAiARlJO7SLHlylbp",
        secure=False,
    )