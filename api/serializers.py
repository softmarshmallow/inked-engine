from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import serializers

from api.models import RawNews, TagHolder
from django_utils.serializer_factory import serializer_factory


class MetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagHolder
        fields = ['spam_human', 'spam_robot',]
        abstract = True


def news_meta_serializer_factory(mdl):
    myserializer = serializer_factory(
        mdl,fields=["spam_human","spam_robot"],
    )
    return myserializer


class NewsSerializer(serializers.ModelSerializer):
    # meta = serializers.SerializerMethodField() #MetaSerializer() #news_meta_serializer_factory(RawNews)

    class Meta:
        model = RawNews
        fields = ['article_id', 'time', 'title', 'article_url', 'origin_url', 'body_html', 'provider',] #  'meta',
        # validators = []

    def create(self, validated_data):
        news = RawNews.objects.create(**validated_data)
        return news
