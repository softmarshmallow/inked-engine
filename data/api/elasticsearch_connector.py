from elasticsearch import Elasticsearch

es = Elasticsearch()


def create_initial_index():
    request_body = {
        "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 1,
            "analysis": {
                "tokenizer": {
                    "nori_user_dict": {
                        "type": "nori_tokenizer",
                        "decompound_mode": "mixed",
                        # "user_dictionary": "userdict_ko.txt"
                    }
                },
                "analyzer": {
                    "default": {
                        "type": "custom",
                        "tokenizer": "nori_user_dict"
                    }
                }
            }
        },

        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "content": {"type": "text"},
                "provider": {"type": "keyword"},
                "time": {"type": "date"},
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


def add_news(title, content, provider, time):
    doc = {
        "title": title,
        "content": content,
        "provider": provider,
        "time": time,
    }
    res = es.index(index='news', body=doc)
    print(res['result'])


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
    newses = content_db_connector.fetch_raw_collection(100)
    from bs4 import BeautifulSoup

    for news in newses:
        html = news['body_html']
        soup = BeautifulSoup(html, 'lxml')
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out
        # get text
        text = soup.get_text()
        add_news(news['title'], content=text, provider=news['provider'], time=news['time'])


if __name__ == "__main__":
    create_initial_index()
    migrate_news_test()
    # add_news()
    search_news("기자")
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
