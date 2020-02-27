from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'news', views.NewsViewSet)
router.register(r'news/batch', views.NewsListCreateView)

urlpatterns = [
    path('', include(router.urls)),
]