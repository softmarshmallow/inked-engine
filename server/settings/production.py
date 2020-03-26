from .base import *

DEBUG = True


DATABASES['default']['CLIENT'] = {
    'host': '52.78.69.94',
    'port': 27017,
    'username': 'admin',
    'password': 'SHARED@password'
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = "AKIAUMSBTS5KYZKBCN5P"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "inked-service-server-statics"
STATIC_URL = f'https://inked-service-server-statics.s3.ap-northeast-2.amazonaws.com/'
