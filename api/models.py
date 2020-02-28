from djongo import models


class RawNews(models.Model):
    class Meta:
        db_table = 'raw'
    _id = models.ObjectIdField()
    article_id = models.CharField(max_length=100)
    time = models.DateTimeField()
    title = models.CharField(max_length=500)
    article_url = models.URLField(max_length=500, unique=True)
    origin_url = models.URLField(max_length=500, null=True, blank=True)
    body_html = models.TextField()
    provider = models.CharField(max_length=50)
