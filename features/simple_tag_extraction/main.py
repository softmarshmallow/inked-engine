from data.model.news import News
from utils.title_box_util.news_title_box_util import extract_boxes
from bs4 import BeautifulSoup


class SimpleTagExtractor:
    def __init__(self, news: News):
        self.news = news
        self.tags = []
        self.soup = BeautifulSoup(self.news.content, 'lxml')

    def extract(self):
        self.tags += self.__extract_box()
        if self.__extract_photo():
            self.tags.append("photo")
        if self.__extract_video():
            self.tags.append("video")
        return self.tags

    def __extract_box(self):
        return [t.innerBoxContent for t in extract_boxes(self.news.title)]

    def __extract_photo(self):
        if self.soup.find('img'):
            return True
        return False

    def __extract_video(self):
        if self.soup.find('video'):
            return True
        return False

    def __extract_content_length(self):
        ...
