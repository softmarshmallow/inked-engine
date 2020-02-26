import os
from .base import *

# setting is production by default
stage = os.getenv('STAGE', 'production')
if stage is 'production':
    from .production import *
elif stage is 'development':
    from .development import *
