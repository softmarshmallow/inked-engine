import os, sys
import json

from data.model.news import News

RSC_ROOT = os.path.join(os.path.dirname(__file__), 'rsc')
TITLE_TOKENS_RSC_ROOT = os.path.join(RSC_ROOT, 'title_spam_token')

doc = ""

# region title token rule based spam extractor

title_match_based_spam_tokens = []
uses = ['general.json', 'advertise.json', 'covid.json', 'criminal.json', 'disaster.json', 'misc.json']
for u in uses:
    general_json = os.path.join(TITLE_TOKENS_RSC_ROOT, u)
    with open(general_json) as json_file:
        data = json.load(json_file)
        for i in data:
            title_match_based_spam_tokens.append(i)


title_box_based_spam_tokens = []
uses = ['boxed.json']
for u in uses:
    general_json = os.path.join(TITLE_TOKENS_RSC_ROOT, u)
    with open(general_json) as json_file:
        data = json.load(json_file)
        for i in data:
            title_box_based_spam_tokens.append(i)


def spam_detect_title(title: str) -> (bool, str):
    for t in title_match_based_spam_tokens:
        if t in title:
            return True, f"token detected {t}"
    for t in title_box_based_spam_tokens:
        if t in title:
            return True, f"box detected, {t}"
    return False, "no spam token detected"


# endregion title token rule based spam extractor


def spam(news: News) -> (bool, str):
    is_title_spam = spam_detect_title(news.title)
    return is_title_spam



if __name__ == "__main__":
    ...