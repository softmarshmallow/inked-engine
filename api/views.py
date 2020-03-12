from datetime import datetime, timedelta, time

from django.http import Http404
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.models import RawNews
from api.serializers import NewsSerializer


def get_time_range_start(date_diff = -1):
    today = datetime.now().date()
    yesterday = today + timedelta(date_diff)
    time_range_start = datetime.combine(yesterday, time())
    return time_range_start


class SpamNewsView(APIView):
    permission_classes = [HasAPIKey | IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        time_range_start = get_time_range_start(-5)
        queryset = RawNews.objects.filter(time__gte=time_range_start, meta={"spam_human": True}).order_by('-time')[:1]
        if len(queryset) == 0:
            raise Http404
        else:
            data = NewsSerializer(queryset[0])
            if data.is_valid():
                return Response(data.data)
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        request.data
        spam = request.data['spam']
        serializer = NewsSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

