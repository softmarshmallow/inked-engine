from djongo import models


class News(models.Model):
    _id = models.ObjectIdField() # djongo mongo obj id
    title = models.CharField(max_length=100)
    content = models.TextField()
    time = models.DateTimeField()
    origin = models.URLField()
