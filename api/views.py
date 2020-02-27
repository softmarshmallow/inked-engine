from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.models import RawNews
from api.serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey | IsAuthenticatedOrReadOnly]
    queryset = RawNews.objects.all()
    serializer_class = NewsSerializer


class NewsListCreateView(generics.ListCreateAPIView):
    permission_classes = [HasAPIKey]

    model = RawNews
    serializer_class = NewsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, many=True)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
