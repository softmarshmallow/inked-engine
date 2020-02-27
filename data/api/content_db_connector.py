import pymongo
from pymongo import MongoClient

# simple connector returns data from mongodb
# connects to service server's raw collection database,
# which is crawler's raw data management collection


client = MongoClient('localhost', 27017)
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
