from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import News
from api.serializers import NewsSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@require_http_methods(["POST"])
def news_crawled(request):
    return HttpResponse("todo")


class PostCrawledNews(APIView):
    def post(self, request, format=None):
        return Response(None, status=status.HTTP_200_OK)


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
