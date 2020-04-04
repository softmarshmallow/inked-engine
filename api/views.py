import json
from datetime import datetime, timedelta, time

from django.http import Http404, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views import View
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.models import RawNews, TagHolder, TagHolderForm
from api.serializers import NewsSerializer
from data.model.news import News

# region tools
from main.main import NewsAnalyzer, NewsIndexer
import logging

class DuplicateCheckView(View):
    def post(self, request, *args, **kwargs):
        try:
            json_data = json.loads(request.body)
            from features.duplicate_check.duplicate_check import check_duplicates_from_database
            res = check_duplicates_from_database(target=News(**json_data))
            return JsonResponse(res.serialize())
        except Exception as e:
            return HttpResponseBadRequest(reason=str(e))


# endregion


class IndexNewsView(View):
    def post(self, request, *args, **kwargs):
        try:
            json_data = json.loads(request.body)
            news = News(**json_data)
            indexer = NewsIndexer(news)
            res = indexer.index()
            return JsonResponse(res)
        except Exception as e:
            return HttpResponseBadRequest(reason=str(e))


class AnalyzeNewsView(View):
    def post(self, request, *args, **kwargs):
        try:
            json_data = json.loads(request.body)
            news = News(**json_data)
            analyzer = NewsAnalyzer(news=news)
            res = analyzer.analyze()
            analyzer = None
            return JsonResponse(res.serialize())
        except Exception as e:
            logging.error("error while handing request", e)
            return HttpResponseBadRequest(e)


def get_time_range_start(date_diff=-1):
    today = datetime.now().date()
    yesterday = today + timedelta(date_diff)
    time_range_start = datetime.combine(yesterday, time())
    return time_range_start


class SpamNewsView(APIView):
    permission_classes = [HasAPIKey | IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        time_range_start = get_time_range_start(-5)
        queryset = RawNews.objects.filter(time__gte=time_range_start,
                                          meta={"spam_human": None}).order_by('-time')[:1]
        if len(queryset) == 0:
            raise Http404
        else:
            try:
                data = NewsSerializer(queryset[0])
                return Response(data.data)
            except Exception as e:
                return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        id = request.data['id']  # article id
        is_spam = request.data['is_spam']
        time_range_start = get_time_range_start(-5)
        news = RawNews.objects.filter(time__gte=time_range_start, article_id=id).update(
            meta={'spam_human': is_spam})
        return Response(news, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewsViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey | IsAuthenticatedOrReadOnly]
    queryset = RawNews.objects.order_by('-time')
    serializer_class = NewsSerializer


# returns only today's data
class OptimizedNewsViewSet(generics.ListAPIView):
    permission_classes = [HasAPIKey | IsAuthenticatedOrReadOnly]

    time_range_start = get_time_range_start(-1)
    queryset = RawNews.objects.filter(time__gte=time_range_start, ).order_by('-time')
    serializer_class = NewsSerializer


class NewsListCreateView(generics.ListCreateAPIView):
    permission_classes = [HasAPIKey]

    model = RawNews
    serializer_class = NewsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
