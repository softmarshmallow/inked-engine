from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import serializers
from api.models import RawNews
from django.forms.models import model_to_dict


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawNews
        fields = ['article_id', 'time', 'title', 'article_url', 'origin_url', 'body_html', 'provider']

    def create(self, validated_data):
        article_url = validated_data['article_url']
        if not RawNews.objects.filter(article_url=article_url).exists():
            news = RawNews.objects.create(**validated_data)
            on_new_news_crawl(NewsSerializer(news).data)
            return news
        else:
            raise ValueError(f'news data with article_url ${article_url} already exists.')


def on_new_news_crawl(news):
    from api.consumers import MAIN_STREAM_GROUP
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        MAIN_STREAM_GROUP,
        {
            'type': 'new_news',
            'news': news
        }
    )