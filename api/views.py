from rest_framework import viewsets
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.models import RawNews
from api.serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey | IsAuthenticatedOrReadOnly]
    queryset = RawNews.objects.all()
    serializer_class = NewsSerializer
