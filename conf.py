import sys
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)
CREDENTIALS_ROOT = os.path.join(BASE_DIR, "credentials")
DATA_SOURCE_ROOT = os.path.join(BASE_DIR, "data/local")

# region
'''
CHOOSE DATA SOURCE
// naver / ebest //
'''
# DEFAULT_NEWS_DATABASE = 'naver'
DEFAULT_NEWS_DATABASE = 'ebest'
# endregion


if __name__ == "__main__":
    print(BASE_DIR)
    print(DATA_SOURCE_ROOT)