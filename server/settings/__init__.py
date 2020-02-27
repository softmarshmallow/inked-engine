import os
# setting is production by default
stage = os.getenv('STAGE', 'production')
print(f"stage is {stage}")
if stage == 'production':
    from .production import *
elif stage is 'development':
    from .development import *
else:
    # if env settings exists, but does not match any, load development as default
    from .development import *
