import json

from elasticsearch import Elasticsearch
from conf import CREDENTIALS_ROOT
from data.model.news import News
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
from data.api import content_db_connector
import logging

with open(os.path.join(CREDENTIALS_ROOT, "es-connection.json")) as json_file:
    data = json.load(json_file)
    hosts = data["hosts"]
    port = data["port"]

es = Elasticsearch(
    hosts=hosts,
    port=port,
    scheme="http",
)


def get_user_dictionary():
    # TODO migrate to external file
    # https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-nori-tokenizer.html
    return ["n95", "n번방", "아비간", "CDBC", "수소차", "웹캠", "치료제", "3D프린터 3D 프린터"]


s_tokenizer = {
    "seunjeon_default_tokenizer": {
        "type": "seunjeon_tokenizer",
        "index_eojeol": False,
        "user_words": get_user_dictionary()
    }
}


# https://github.com/elastic/elasticsearch/blob/master/docs/plugins/analysis-nori.asciidoc
nori_tokenizer = {
    "nori_user_dict_tokenizer": {
        "type": "nori_tokenizer",
        "decompound_mode": "mixed",
        "user_dictionary_rules": get_user_dictionary()
    }
}


def create_initial_index(force=False):
    settings = {
        "number_of_shards": 2,
        "number_of_replicas": 1,
        "analysis": {
            "analyzer": {
                "korean": {
                    "type": "custom",
                    "tokenizer": "nori_user_dict_tokenizer",
                    "filter": ["nori_readingform"],
                    "char_filter": ["html_cleaner"]
                },
            },
            "tokenizer": nori_tokenizer,
            "char_filter": {
                "html_cleaner": {
                    "type": "html_strip",
                    "escaped_tags": []
                }
            }
        }
    }

    mappings = {
        "properties": {
            "title": {"type": "text", "analyzer": "korean", "index": True, "boost": 2},
            "content": {"type": "text", "analyzer": "korean", "index": True},
            "provider": {"type": "keyword"},
            "time": {"type": "date"},
            "meta": {
                "type": "nested",
                "properties": {
                    "summary": {"type": "text", "boost": 2},
                    "subject": {"type": "text", "boost": 2},
                    "category": {"type": "keyword"},
                    "categories": {"type": "nested"},
                    "spamMarks": {"type": "nested"},
                    "tags": {"type": "nested"},
                    "isSpam": {"type": "boolean"}
                    # TODO provide more meta fields including array
                }
            }
        }
    }
    request_body = {
        "settings": settings,
        "mappings": mappings
    }
    exists = es.indices.exists('news')
    if exists:
        if force:
            res = es.indices.delete('news')
            print(res)
            res = es.indices.create(index='news', body=request_body)
            print(res)
        else:
            es.indices.close(index="news")
            print("already exists 'news' index...")
            res = es.indices.put_settings(index='news', body=settings)
            print("update index settings", res)
            res = es.indices.put_mapping(index='news', body=mappings)
            print("update index mapping", res)
            es.indices.open(index="news")
        return
    else:
        print("creating 'news' index...")
        res = es.indices.create(index='news', body=request_body)
        print(res)


def add_news(news: News) -> dict:
    logging.info(f"start indexing news.. {news.id}")
    # clean content
    html = news.content
    soup = BeautifulSoup(html, 'lxml')
    # kill all script and style elements
    for script in soup(["script", "style", "a", "img", "video"]):
        script.extract()  # rip it out
    text = soup.get_text()
    news.content = text

    try:
        serialized = news.index_serialize()

        doc = {
            "title": news.title,
            "content": news.content,
            "provider": news.provider,
            "time": news.time,
            "meta": serialized["meta"]
        }
        res = es.index(index='news', body=doc, id=news.id)
        return res
    except Exception as e:
        logging.error("error while indexing", e)
        return None


def search_news(q):
    req_body = {
        "query": {
            "match": {
                "content": {
                    "query": q
                }
            }
        }
    }
    res = es.search(index='news', body=req_body)
    print(res['hits']['hits'])


def migrate_news_test():
    from datetime import datetime, timedelta
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    newses = content_db_connector.fetch_news_collection(lim=200, time_from=yesterday, time_to=today)

    print(len(newses))
    for news in tqdm(newses):
        # print(news.time)
        res = add_news(news)
        # print(res)


def reindexSingleNews(id):
    news = content_db_connector.fetch_one(id)
    add_news(news)


if __name__ == "__main__":
    create_initial_index(force=True)
    migrate_news_test()
