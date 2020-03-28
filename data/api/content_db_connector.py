import pymongo
from pymongo import MongoClient
import urllib.parse
import json
import os
from conf import CREDENTIALS_ROOT

# simple connector returns data from mongodb
# connects to service server's raw collection database,
# which is crawler's raw data management collection
from data.model.news import News

with open(os.path.join(CREDENTIALS_ROOT, "db-connection.json")) as json_file:
    data = json.load(json_file)
    url = data["url"]
    username = urllib.parse.quote_plus(data["user"])
    password = urllib.parse.quote_plus(data["password"])
    database = data["database"]

client = MongoClient('mongodb://%s:%s@%s' % (username, password, url))
db = client[database]
collection_news = db.News


def fetch_news_collection(lim=10) -> [News]:
    result = []
    cursor: pymongo.cursor.Cursor = collection_news.find().limit(lim)
    for r in cursor:
        result.append(News(**r))
    return result


if __name__ == "__main__":
    c = fetch_news_collection()
    print(c)
