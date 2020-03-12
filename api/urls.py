import django_eventstream
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'news', views.NewsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(r'news/batch', views.NewsListCreateView.as_view()),
    path(r'news/recent', views.OptimizedNewsViewSet.as_view()),
    path(r'news/spam', views.SpamNewsView.as_view()),
    path('events/', include(django_eventstream.urls), {'channels': ['time']}),
]
