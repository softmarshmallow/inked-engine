from django.urls import path
from . import views

urlpatterns = [
    path(r'news/tools/duplicate-check', views.DuplicateCheckView.as_view()),
    path(r'news/analyze', views.AnalyzeNewsView.as_view()),
    path(r'news/index', views.IndexNewsView.as_view()),
]
