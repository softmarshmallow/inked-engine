from django.urls import path, include
from rest_framework import routers
from . import views
from .models import RawNews
from .serializers import NewsSerializer

router = routers.DefaultRouter()
router.register(r'news', views.NewsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(r'news/batch', views.NewsListCreateView.as_view(queryset=RawNews.objects.all(), serializer_class=NewsSerializer))
]