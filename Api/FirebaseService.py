import pyrebase
import json

import requests

config = {
    "apiKey": "AIzaSyCTJfguq-ZI4zbPdLZKRMqHuvK4bTaV49k",
    "authDomain": "evileye-quorraengine.firebaseapp.com",
    "databaseURL": "https://evileye-quorraengine.firebaseio.com",
    "storageBucket": "evileye-quorraengine.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def stream_handler(message):
    path = message["path"]
    data = message["data"]
    event = message["event"]

    print(json.dumps(data, indent=4, sort_keys=True))

    # print(data["newsTitle"])
    # print(data["newsContent"])
    # print(data["newsTime"])
    # print(data["providerId"])
    # print(data["realKey"])
    # print(data["relatedCompanyCodes"])

def streamData():
    # newsStream = db.child("News").order_by_key().limit_to_last(10).stream(stream_handler, stream_id="lim")
    my_stream2 = db.child("News").stream(stream_handler, stream_id="nolim")


def GetFirebaseNewsData(limit=None):
    builder = db.child("News").order_by_key()
    if limit is not None:
        builder.limit_to_last(limit)

    try:
        allNews = builder.get()
    except requests.exceptions.HTTPError as e:
        pass

    resultList = []
    for news in allNews.each():
        resultList.append(news.val())
    return resultList


def GetAllNewsDataByShallow(limit=None):
    allNewsKeys = db.child("News").shallow().get().val()
    processCount = 0
    for key in allNewsKeys:
        processCount += 1
        newsItem = db.child("News").child(key).get()
        print("Retrieved", processCount, "of", len(allNewsKeys), newsItem.val())



def GetRoot():
    try:
        result = db.get()
    except requests.exceptions.HTTPError as e:
        print("Exception", e)
        # TODO
        result = GetFirebaseNewsData(limit=999999999)
    f = open("root.json", 'w')
    f.write(result)
    f.close()
    print(result)


if __name__ == "__main__":
    # streamData()
    # GetRoot()
    GetAllNewsDataByShallow()
    # newsList = GetAllNewsData(None)
    # print(newsList)