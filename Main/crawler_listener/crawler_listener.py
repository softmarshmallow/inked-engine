from threading import Thread

from flask import Flask, jsonify, request

from DataModels.news_models import NewsDataModel
from Main.main import UNPROCESSED_CRAWLED_DATA_POOL

app = Flask(__name__)

callback = None

@app.route('/api/news', methods=['POST'])
def new_crawled_item():
    content = request.json
    if validate_content(content):
        on_item_crawled(content)
    return jsonify({"received": True})


def validate_content(content):
    return True


def on_item_crawled(crawled_data):
    UNPROCESSED_CRAWLED_DATA_POOL.append(crawled_data)

    try:
        # Data As Model
        formed_data = NewsDataModel(
            id=crawled_data["article_id"],
            newsContent=crawled_data["body_html"],
            newsTitle=crawled_data["title"],
            newsTime=crawled_data["time"],
            compTags=[],
            providerId=crawled_data["provider"],
        )

        callback(formed_data)
        print("add_to_pool:: ", crawled_data)
    except Exception as e:
        print(e)


def run_threaded():
    ThreadedListener().start()


class ThreadedListener(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        app.run()


if __name__ == "__main__":
    app.run()
