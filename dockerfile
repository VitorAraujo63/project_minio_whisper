FROM minio/minio

RUN -p 9000:9000 -p 9001:9001

VOLUME "C:\minio\data"

VOLUME "C:\minio\config\.env:etc/config.env"

ENV "MINIO_CONFIG_ENV_FILE=C:\minio\config\.env"

