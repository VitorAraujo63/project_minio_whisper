from minio import Minio
from minio.error import S3Error

def main():
    client = Minio(
        "localhost:9000",
        access_key="SBf9qUCTCs93oFuXJrWi",
        secret_key="60k62Dzl39qdBCBvMgbnoQsrAiARlJO7SLHlylbp",
        secure=False,
    )

    source_file = "C:\\Users\\tonyb\\OneDrive\\Desktop\\minio\\123.txt"

    bucket_name = "teste666"
    destination_file = "tacaamae_ver_kickaa.txt"

    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")

    # Upload the file, renaming it in the process
    client.fput_object(
        bucket_name, destination_file, source_file,
    )
    print(
        source_file, "successfully uploaded as object",
        destination_file, "to bucket", bucket_name,
    )

if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)