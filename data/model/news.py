from datetime import datetime
from enum import Enum

import arrow

import logging
class News:
    def __init__(self, **kwargs):
        self.id: str = None  # optional
        self.origin_url: str = None  # optional
        self.title: str
        self.content: str
        self.time: datetime
        self.provider: str
        self.meta: NewsMeta = NewsMeta()

        if kwargs is not None and kwargs != {}:  # dict base serialization
            try:
                if 'id' in kwargs:
                    self.id = kwargs['id']
                elif '_id' in kwargs:
                    self.id = str(kwargs['_id'])  # mongodb id field

                try:
                    self.origin_url = kwargs['originUrl']
                except KeyError as e:
                    pass
                self.title = kwargs['title']
                self.content = kwargs['content']
                self.time = arrow.get(kwargs['time']).datetime
                self.provider = kwargs['provider']
                self.meta = NewsMeta(**kwargs['meta'])
            except KeyError as e:
                logging.error("err", e)

    def serialize(self, debug=False):
        if debug:
            # shorter serialization for debug logging purpose
            content = self.content[0:30],
        else:
            content = self.content

        origin_url = None
        if self.origin_url is not None:
            origin_url = self.origin_url

        item = {
            "id": self.id,
            "time": self.time.isoformat(),
            "title": self.title,
            "originUrl": origin_url,
            "content": content,
            "provider": self.provider,
            "meta": self.meta.serialize()
        }
        return item

    def index_serialize(self):
        origin_url = None
        if self.origin_url is not None:
            origin_url = self.origin_url

        item = {
            "id": self.id,
            "time": self.time.isoformat(),
            "title": self.title,
            "originUrl": origin_url,
            "content": self.content,
            "provider": self.provider,
            "meta": self.meta.index_serialize()
        }
        return item

    def __str__(self):
        return str(self.serialize(debug=True))


class NewsMeta:
    def __init__(self, **kwargs):
        self.source = None
        self.spam_marks: [SpamMark] = []
        self.summary = None
        self.subject = None
        self.category: NewsCategory = None
        if kwargs is not None and kwargs != {}:
            try:
                if "spamMarks" in kwargs:
                    self.spam_marks = [SpamMark(**s) for s in kwargs['spamMarks']]
                self.source = kwargs['source']
                self.summary = kwargs['summary']
                self.subject = kwargs['subject']
                self.category = kwargs['category']
            except KeyError as e:
                logging.error("err", e)

    def is_spam(self):
        for s in self.spam_marks:
            if s.spam == SpamTag.SPAM:
                return True
        return False

    def serialize(self):
        item = {
            "spamMarks": [m.serialize() for m in self.spam_marks],
            "source": self.source,
            "summary": self.summary,
            "subject": self.subject,
            "category": self.category,
        }
        return item

    def index_serialize(self):
        item = {
            "spamMarks": [m.index_serialize() for m in self.spam_marks],
            "source": self.source,
            "summary": self.summary,
            "subject": self.subject,
            "category": self.category,
            "isSpam": self.is_spam()
        }
        return item


class SpamTag(Enum):
    SPAM = "SPAM"
    NOTSPAM = "NOTSPAM"
    UNTAGGED = "UNTAGGED"

    @classmethod
    def from_str(cls, label):
        if label == 'SpamTag.SPAM':
            return cls.SPAM
        elif label == "SpamTag.NOTSPAM":
            return cls.NOTSPAM
        elif label == "SpamTag.UNTAGGED":
            return cls.UNTAGGED
        else:
            raise NotImplementedError(f"no SpamTag found with label {label}")


class NewsCategory(Enum):
    WEATHER = "WEATHER"
    UNCATEGORIZED = "UNCATEGORIZED"


class SpamMark:
    def __init__(self, **kwargs):
        self.spam: SpamTag
        self.reason: str
        # self.at: datetime = at

        if kwargs is not None and kwargs != {}:
            self.spam = kwargs["spam"]
            self.reason = kwargs["reason"]

    def spam_str(self):
        try:
            return self.spam.value
        except Exception:
            return self.spam

    def serialize(self):
        return {
            "spam": self.spam_str(),
            "reason": self.reason
        }

    def index_serialize(self):
        return {
            "spam": self.spam_str(),
            "reason": self.reason
        }


class SingleAnalysisResult:
    def __init__(self, spam_marks: [SpamMark] = [], summary=None, subject=None,
                 category: NewsCategory = None, categories: [NewsCategory] = []):
        self.spam_marks: [SpamMark] = spam_marks
        self.summary: str = summary
        self.subject: str = subject
        self.category: NewsCategory = category
        self.categories: [NewsCategory] = categories
        self.tags: [str] = []

    def serialize(self):
        category = None
        if self.category is not None:
            category = self.category.value

        return {
            "spamMarks": [m.serialize() for m in self.spam_marks],
            "summary": self.summary,
            "subject": self.subject,
            "category": category,
            "categories": [c.value for c in self.categories],
            "tags": self.tags
        }

    def index_serialize(self):
        category = None
        if self.category is not None:
            category = self.category.value

        return {
            "spamMarks": [m.index_serialize() for m in self.spam_marks],
            "summary": self.summary,
            "subject": self.subject,
            "category": category,
            "categories": [c.value for c in self.categories],
            "tags": self.tags
        }
