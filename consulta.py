from minio import Minio
import urllib3

client = Minio("localhost:9000",
        acess_key="SBf9qUCTCs93oFuXJrWi",
        secret_key="60k62Dzl39qdBCBvMgbnoQsrAiARlJO7SLHlylbp",
        secure=True,
        http_client=urllib3.ProxyManager(
            "http://localhost:9000",
            timeout=urllib3.Timeout.DEFAULT_TIMEOUT,
            cert_reqs="CERT_REQUIRED",
            retries=urllib3.Retry(
                total=5,
                backoff_factor=0.2,
                status_forcelist=[500, 502, 503, 504]
            ),
            ),
    )

consulta = client.list_buckets()

for buket in consulta:
    print(consulta.name, consulta.creation_date)
