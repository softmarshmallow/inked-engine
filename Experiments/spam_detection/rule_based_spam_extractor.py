import os, sys
import json

from data.model.news import News

RSC_ROOT = os.path.join(os.path.dirname(__file__), 'rsc')
TITLE_TOKENS_RSC_ROOT = os.path.join(RSC_ROOT, 'title_spam_token')



doc = ""

# region title token rule based spam extractor


general_json = os.path.join(TITLE_TOKENS_RSC_ROOT, 'general.json')
title_rule_based_spam_tokens = []
with open(general_json) as json_file:
    data = json.load(json_file)
    for i in data:
        title_rule_based_spam_tokens.append(i)


def spam_detect_title(title: str) -> (bool, str):
    for t in title_rule_based_spam_tokens:
        if t in title:
            return True, t
    return False, "no spam token detected"

# endregion title token rule based spam extractor


def spam(news: News) -> bool:
    is_title_spam = spam_detect_title(news.title)
    return is_title_spam[0]


def __test():
    from data.api.content_db_connector import fetch_news_collection
    newses = fetch_news_collection(lim=2000)
    for news in newses:
        print(spam(news), news.title)

if __name__ == "__main__":
    __test()
