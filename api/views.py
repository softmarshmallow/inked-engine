from rest_framework import viewsets

from api.models import RawNews
from api.serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = RawNews.objects.all()
    serializer_class = NewsSerializer
