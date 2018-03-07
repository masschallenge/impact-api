from storages.backends.s3boto3 import S3Boto3Storage  # pragma: no cover


class MediaStorageBackend(S3Boto3Storage):  # pragma: no cover
    custom_domain = False  # pragma: no cover
    default_acl = 'private'  # pragma: no cover
    file_overwrite = False  # pragma: no cover
