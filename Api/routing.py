from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
    re_path(r'ws/news/', consumers.ProcessedNewsConsumer),
]


# from channels.routing import URLRouter
# from channels.http import AsgiHandler
# from channels.auth import AuthMiddlewareStack
# import django_eventstream
#
# urlpatterns = [
#     path(r'^events/', AuthMiddlewareStack(
#         URLRouter(django_eventstream.routing.urlpatterns)
#     ), {'channels': ['test']}),
#     path(r'', AsgiHandler),
# ]