from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class StaticRootStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = settings.AWS_STATIC_LOCATION
    default_acl = 'public-read'


class MediaRootStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = settings.AWS_MEDIA_LOCATION
    default_acl = 'public-read'
