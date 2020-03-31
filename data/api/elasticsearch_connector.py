import json

from elasticsearch import Elasticsearch
from conf import CREDENTIALS_ROOT
from data.model.news import News
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

with open(os.path.join(CREDENTIALS_ROOT, "es-connection.json")) as json_file:
    data = json.load(json_file)
    hosts = data["hosts"]
    port = data["port"]

es = Elasticsearch(
    hosts=hosts,
    port=port,
    scheme="https",
)


def create_initial_index():
    request_body = {
        "settings": {
            "number_of_shards": 2,
            "number_of_replicas": 1,
            "analysis": {
                "analyzer": {
                    "korean": {
                        "type": "custom",
                        "tokenizer": "seunjeon_default_tokenizer",
                        "char_filter": ["html_cleaner"]
                    },
                },
                "tokenizer": {
                    "seunjeon_default_tokenizer": {
                        "type": "seunjeon_tokenizer",
                        "index_eojeol": False,
                        "user_words": []
                    }
                },
                "char_filter": {
                    "html_cleaner": {
                        "type": "html_strip",
                        "escaped_tags": []
                    }
                }
            }
        },

        "mappings": {
            "properties": {
                "title": {"type": "text", "analyzer": "korean", "index": True},
                "content": {"type": "text", "analyzer": "korean", "index": True},
                "provider": {"type": "keyword"},
                "time": {"type": "date"},
                "meta": {
                    "type": "nested",
                    "properties": {
                        "summary": {"type": "text"},
                        "subject": {"type": "text"},
                        "category": {"type": "keyword"}
                        # TODO provide more meta fields including array
                    }
                }
            }
        }
    }
    exists = es.indices.exists('news')
    if exists:
        print("already exists 'news' index...")
        return
    else:
        print("creating 'news' index...")
        res = es.indices.create(index='news', body=request_body)
        print(res)


def add_news(news: News) -> dict:
    # clean content
    html = news.content
    soup = BeautifulSoup(html, 'lxml')
    # kill all script and style elements
    for script in soup(["script", "style", "a", "img", "video"]):
        script.extract()  # rip it out
    text = soup.get_text()
    news.content = text

    doc = {
        "title": news.title,
        "content": news.content,
        "provider": news.provider,
        "time": news.time,
        "meta": {
            "summary": news.meta.summary,
            "subject": news.meta.subject,
            "category": news.meta.category,
        }
    }
    res = es.index(index='news', body=doc, id=news.id)
    return res


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
    from data.api import content_db_connector
    newses = content_db_connector.fetch_news_collection(lim=0)

    print(len(newses))
    for news in tqdm(newses):
        res = add_news(news)
        # print(res)


if __name__ == "__main__":
    create_initial_index()
    migrate_news_test()
    # add_news()
    # search_news("기자")
#
#


#
# res = es.get(index="test-index", id=1)
# print(res['_source'])
#
# es.indices.refresh(index="test-index")
#
# res = es.search(index="test-index", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total']['value'])
# for hit in res['hits']['hits']:
#     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
