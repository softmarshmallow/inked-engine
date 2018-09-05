import sys
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_SOURCE_ROOT = os.path.join(BASE_DIR, "DataSource")
DEFAULT_NEWS_DATABASE = 'naver'

if __name__ == "__main__":
    print(BASE_DIR)
    print(DATA_SOURCE_ROOT)