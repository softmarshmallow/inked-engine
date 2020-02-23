from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets

from api.models import News
from api.serializers import NewsSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
