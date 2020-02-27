from .base import *

DATABASES['default']['CLIENT'] = {
    'host': 'localhost',
    'port': 27017,
}

REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
    'rest_framework.permissions.AllowAny',
]