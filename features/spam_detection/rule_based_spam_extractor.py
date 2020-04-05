import os, sys
import json
import logging

from data.model.news import News, SpamMark, SpamTag

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


TITLE_MIN_LENGTH = 21
def spam_detect_title(title: str) -> (SpamTag, str):
    if len(title) < TITLE_MIN_LENGTH:
        return SpamTag.SPAM, f"title too short {len(title)}"
    for t in title_match_based_spam_tokens:
        if t in title:
            return SpamTag.SPAM, f"token detected {t}"
    for t in title_box_based_spam_tokens:
        if t in title:
            return SpamTag.SPAM, f"box detected, {t}"
    return SpamTag.NOTSPAM, "no spam rule detected"


# endregion title token rule based spam extractor


def spam(news: News) -> SpamMark:
    try:
        is_title_spam = spam_detect_title(news.title)
        spam_mark_data = {"spam": is_title_spam[0], "reason": is_title_spam[1]}
        return SpamMark(**spam_mark_data)
    except Exception as e:
        logging.error("error while extracting spam", e)



if __name__ == "__main__":
    ...