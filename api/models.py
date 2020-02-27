from djongo import models


class RawNews(models.Model):
    class Meta:
        db_table = 'raw'
    _id = models.ObjectIdField()
    article_id = models.CharField(max_length=20)
    time = models.DateTimeField()
    title = models.CharField(max_length=200)
    article_url = models.URLField(max_length=200, unique=True)
    origin_url = models.URLField(max_length=200, null=True, blank=True)
    body_html = models.TextField()
    provider = models.CharField(max_length=20)
