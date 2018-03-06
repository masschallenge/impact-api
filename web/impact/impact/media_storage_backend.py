from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorageBackend(S3Boto3Storage):
    custom_domain = False
    default_acl = 'private'
    file_overwrite = False
