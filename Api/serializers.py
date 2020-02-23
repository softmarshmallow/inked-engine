from rest_framework import serializers

from api.models import News


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'content', 'time']
