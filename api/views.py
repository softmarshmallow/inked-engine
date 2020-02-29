from datetime import datetime, timedelta, time

from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.models import RawNews
from api.serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey | IsAuthenticatedOrReadOnly]
    queryset = RawNews.objects.order_by('-time')
    serializer_class = NewsSerializer


# returns only today's data
class OptimizedNewsViewSet(generics.ListAPIView):
    permission_classes = [HasAPIKey | IsAuthenticatedOrReadOnly]

    today = datetime.now().date()
    yesterday = today + timedelta(-1)
    tomorrow = today + timedelta(1)
    time_range_start = datetime.combine(yesterday, time())
    time_range_end = datetime.combine(tomorrow, time())
    queryset = RawNews.objects.filter(time__gte=time_range_start, time__lte=time_range_end, ).order_by('-time')
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

