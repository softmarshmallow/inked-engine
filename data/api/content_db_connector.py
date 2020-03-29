from datetime import datetime

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


def build_time_query(time_from=None, time_to=None):
    if time_from is not None or time_to is not None:
        query = {}
        if time_from is not None:
            query["$gte"] = time_from
        if time_to is not None:
            query["$lt"] = time_to
        return query
    else:
        return None


def fetch_news_collection(time_from: datetime=None, time_to: datetime=None, lim=10) -> [News]:
    """
    :param time_from: from
    :param time_to: to
    :param lim: set 0 for no limit
    :return: [News]
    """
    # region build query
    query = {}
    if time_from is not None or time_to is not None:
        query["time"] = build_time_query(time_from=time_from, time_to=time_to)
    # endregion build query

    result = []
    cursor: pymongo.cursor.Cursor = collection_news.find(
        query
    ).limit(lim)
    for r in cursor:
        result.append(News(**r))
    return result


if __name__ == "__main__":
    c = fetch_news_collection()
    print(c)
