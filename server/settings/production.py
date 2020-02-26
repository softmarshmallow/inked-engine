from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES['default']['CLIENT'] = {
    'host': '52.78.69.94',
    'port': 27017,
    'username': 'admin',
    'password': 'SHARED@password'
}