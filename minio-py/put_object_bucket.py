from minio import Minio

client = Minio(
        "localhost:9000",
        access_key="teste123",
        secret_key="teste123",
        secure=False,
    )

result = client.fput_object(
    "content", 
    "testando_put.txt", 
    "C:\\Users\\tonyb\\OneDrive\\Desktop\\minio\\123.txt",
)
print(
    "created {0} object; etag: {1}, version-id: {2}".format(
        result.object_name, result.etag, result.version_id,
    ),
)