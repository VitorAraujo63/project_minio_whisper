from minio import Minio
import conn


client = Minio(
        "localhost:9000",
        access_key="SBf9qUCTCs93oFuXJrWi",
        secret_key="60k62Dzl39qdBCBvMgbnoQsrAiARlJO7SLHlylbp",
        secure=False,
)

client.fget_object("teste666", "tacaamae_ver_kickaa.txt", "jeann.txt")