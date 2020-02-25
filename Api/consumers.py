import json
from datetime import datetime

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


MAIN_STREAM_GROUP = 'news-stream-main-channel'


class ProcessedNewsConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connect(self):
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            MAIN_STREAM_GROUP,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            MAIN_STREAM_GROUP,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        news = text_data_json['news']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            MAIN_STREAM_GROUP,
            {
                'type': 'new_news',
                'news': news
            }
        )

    # Receive message from room group
    def new_news(self, event):
        message = event['news']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'news': message,
            'at': 'todo: add time data here'
        }))