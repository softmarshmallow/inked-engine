from django.urls import re_path, path
from . import consumers

from django.conf.urls import url
from channels.routing import URLRouter
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
import django_eventstream


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
    re_path(r'ws/news/', consumers.ProcessedNewsConsumer),
]


sse_urlpatterns = [
    url(r'^events/', AuthMiddlewareStack(
        URLRouter(django_eventstream.routing.urlpatterns)
    ), {'channels': ['time']}),
    url(r'', AsgiHandler),
]
