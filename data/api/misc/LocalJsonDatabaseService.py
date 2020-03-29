import json
from pprint import pprint
from typing import List
import os

from datetime import datetime

# File
from conf import DATA_SOURCE_ROOT
from data.local.news_models import NewsDataModel, CreateNewNewsModelFromJson


def GetLocalNewsData(max: int = 1000, hasMaxValue: bool = True) -> List[NewsDataModel]:
    # if request is under 10000, use min version
    if hasMaxValue and max < 10000:
        file = "evileye-quorraengine-News-export-min.json"
    else:
        file = "evileye-quorraengine-News-export.json"

    filename = os.path.join(DATA_SOURCE_ROOT, file)
    rootJson = json.load(open(filename))

    newsDataList = []

    jsonKeys = rootJson.keys()

    for newsDataKey in jsonKeys:

        newNewsData = CreateNewNewsModelFromJson(rootJson[newsDataKey])
        newsDataList.append(newNewsData)
        if hasMaxValue and len(newsDataList) >= max:
            break

    return newsDataList


def PrintAllTitle():
    newsDataSamples = GetLocalNewsData(max=5000, hasMaxValue=True)
    for s in newsDataSamples:
        print(s.newsTime, s.newsTitle)

    return newsDataSamples


if __name__ == "__main__":

    print("TOTAL: ", len(GetLocalNewsData(hasMaxValue=False)))

    st = datetime.now()
    newsList = GetLocalNewsData(max=100, hasMaxValue=True)
    et = datetime.now()
    print(len(newsList))
    print("time took: ", et - st)

    for news in newsList:
        print(news.get_news_content())
