import pymongo
from pymongo import MongoClient
import urllib.parse
# simple connector returns data from mongodb
# connects to service server's raw collection database,
# which is crawler's raw data management collection

# fixme load from credentials
url = "ec2-52-78-69-94.ap-northeast-2.compute.amazonaws.com:27017"
username = urllib.parse.quote_plus('admin')
password = urllib.parse.quote_plus('SHARED@password')
client = MongoClient('mongodb://%s:%s@%s' % (username, password, url))
db = client['inked-content-db']
collection_raw = db.raw


def fetch_raw_collection(lim=10) -> []:
    result = []
    cursor: pymongo.cursor.Cursor = collection_raw.find().limit(lim)
    for r in cursor:
        result.append(r)
    return result


if __name__ == "__main__":
    c = fetch_raw_collection()
    print(c)
