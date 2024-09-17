from minio import Minio

client = Minio(
    "localhost:9000",
    access_key="SBf9qUCTCs93oFuXJrWi",
    secret_key="60k62Dzl39qdBCBvMgbnoQsrAiARlJO7SLHlylbp",
    secure=False,
)

# client = Minio(
#     "play.min.io",
#     access_key="Q3AM3UQ867SPQQA43P2F",
#     secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
# )

bucket = input('What is a name of your bucket: ')

if client.bucket_exists(bucket):
    print(bucket, "exists")
else:
    print(bucket, "does not exist")