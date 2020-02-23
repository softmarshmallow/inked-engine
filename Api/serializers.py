from rest_framework import serializers

from api.models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'content', 'time']

    def create(self, validated_data):
        news = News.objects.create(**validated_data)
        return news
