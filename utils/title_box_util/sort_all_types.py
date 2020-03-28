from utils.title_box_util.news_title_box_util import extract_boxes
from data.api import content_db_connector



def sort_all():
    box_types_set = set()
    newses = content_db_connector.fetch_news_collection(5000)
    for news in newses:
        res = extract_boxes(news["title"])
        if len(res) > 0:
            for t in res:
                box_types_set.add(t)

    return box_types_set


if __name__ == "__main__":
    res = sort_all()
    for i in res:
        print(i)
