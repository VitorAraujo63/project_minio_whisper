from minio import Minio

client = Minio(
        "localhost:9000",
        access_key="SBf9qUCTCs93oFuXJrWi",
        secret_key="60k62Dzl39qdBCBvMgbnoQsrAiARlJO7SLHlylbp",
        secure=False,
    )

# List objects information whose names starts with "my/prefix/".
objects = client.list_objects("teste", prefix="teste123.txt", recursive=True)
for obj in objects:
    print(obj)