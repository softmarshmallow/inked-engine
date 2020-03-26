## settings. how to set up your own `production.py`



example
``` python

DATABASES['default']['CLIENT'] = {
    'host': 'xx.xx.xx.xx',
    'port': 27017,
    'username': 'admin',
    'password': 'yourSecure!password'
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = "XXXXXXXXXXXXXX"
AWS_SECRET_ACCESS_KEY = "gd/+XXXXXXXXXXXX"
AWS_STORAGE_BUCKET_NAME = "your-own-aws-s3-bucket-name"
STATIC_URL = f'https://XXXXX.amazonaws.com/'

```