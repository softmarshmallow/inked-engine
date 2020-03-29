from datetime import datetime
import arrow


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
                print(e)

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

    def __str__(self):
        return str(self.serialize(debug=True))


class NewsMeta:
    def __init__(self, **kwargs):
        self.source = None
        if kwargs is not None and kwargs != {}:
            try:
                self.source = kwargs['source']
            except KeyError as e:
                print(e)

    def serialize(self):
        item = {
            "source": self.source,
        }
        return item
