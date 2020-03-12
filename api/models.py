from django import forms
from djongo import models


class TagHolder(models.Model):
    spam_human = models.BooleanField(default=None, null=True)
    spam_robot = models.BooleanField(default=None, null=True)

    class Meta:
        abstract = True


class TagHolderForm(forms.ModelForm):
    class Meta:
        model = TagHolder
        fields = (
            'spam_human', 'spam_robot'
        )


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
    meta = models.EmbeddedField(
        model_container=TagHolder,
        model_form_class=TagHolderForm
    )

