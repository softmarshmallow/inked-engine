import json
from datetime import datetime
import os
from pprint import pprint
from bs4 import BeautifulSoup as bs4
import sys

from dateutil.rrule import rrule, DAILY

DATA_ROOT = "/Users/softmarshmallow/Documents/Apps/Inked/Crawlers/inkedNewsCrawler/data"
DEFAULT_DATE = datetime(2018, 4, 23)


def get_date_str(date: datetime):
    return date.strftime("%Y%m%d")


def get_link_file_path(date: datetime, from_s3=False) -> str:
    date_str = get_date_str(date)
    file_name = 'naver_news_link_data/naver_date_article_links_%s.json' % date_str
    if from_s3:
        return file_name
    else:
        file_name = os.path.join(DATA_ROOT, file_name)
        return file_name


def get_content_file_path(date: datetime, from_s3=False) -> str:
    date_str = get_date_str(date)
    file_name = 'naver_news_content_data/naver_date_article_contents_%s.json' % date_str
    if from_s3:
        return file_name
    else:
        file_name = os.path.join(DATA_ROOT, file_name)
        return file_name


def get_article_head_list(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE):
    print("reading files....")
    head_list = []
    dates = rrule(DAILY, dtstart=start_date, until=end_date)
    for date in dates:
        path = get_link_file_path(date)
        with open(path) as p:
            data = json.load(p)

        head_list.extend(data)
        # for record in data:
        #     print(record)
        #     head_list.append(record)

    return head_list


def get_title_list(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE):
    title_list = []
    head_list = get_article_head_list(start_date=start_date, end_date=end_date)
    for head in head_list:
        title = head["title"]
        title_list.append(title)
    return title_list


def get_all_article_detail_list():
    start = datetime(1990, 1, 1)
    end = datetime(2018, 8, 1)
    return get_article_detail_list(start_date=start, end_date=end, max=None)


def get_article_detail_list(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE, max=1):
    print("reading files....")
    detail_list = []
    dates = rrule(DAILY, dtstart=start_date, until=end_date)
    count = 0
    for date in dates:
        path = get_content_file_path(date)
        try:
            with open(path) as p:
                data = json.load(p)

            # detail_data_list = []
            date_records = []
            for record in data:
                if record is not None:
                    record["body_text"] = bs4(record["body_html"], 'lxml').get_text()
                    date_records.append(record)
                    count += 1
                    if max is not None and count >= max:
                        break
            detail_list.extend(date_records)
        except FileNotFoundError:
            ...

    return detail_list


def get_article_content_list(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE, max=1):
    content_list = []
    detail_list = get_article_detail_list(start_date=start_date, end_date=end_date, max=max)
    count = 0
    for detail in detail_list:
        if detail is None:
            print(detail, "ERR")
        else:
            content = detail["body_text"]
            content_list.append(content)

            count += 1
            if count >= max:
                break
    return content_list


def get_news_data():
    # get_article_detail_list()
    ...


if __name__ == "__main__":
    data = get_title_list()
    print(len(data))
    data = get_article_content_list()
    pprint(data)
